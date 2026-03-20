#!/bin/bash

# Script to automatically merge dependabot PRs after triggering CI
# This script clones the repo to a temp directory to avoid issues with checking out branches
# Usage: ./merge_dependabot_pr.sh <PR_NUMBER> [timeout_seconds]
# Example: ./merge_dependabot_pr.sh 89 600

# Note: Don't use 'set -e' here because we need custom error handling for cleanup

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PR_NUMBER="${1:-}"
TIMEOUT="${2:-600}"  # Default 10 minutes
POLL_INTERVAL=30      # Check status every 30 seconds
TEMP_DIR=""           # Will be set later

# Validation
if [[ -z "$PR_NUMBER" ]]; then
    echo -e "${RED}Error: PR number required${NC}"
    echo "Usage: $0 <PR_NUMBER> [timeout_seconds]"
    echo "Example: $0 89 600"
    exit 1
fi

if ! command -v gh &> /dev/null; then
    echo -e "${RED}Error: GitHub CLI (gh) not installed${NC}"
    exit 1
fi

if ! command -v git &> /dev/null; then
    echo -e "${RED}Error: Git not installed${NC}"
    exit 1
fi

# Helper functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

cleanup() {
    if [[ -n "$TEMP_DIR" ]] && [[ -d "$TEMP_DIR" ]]; then
        log_info "Cleaning up temp directory: $TEMP_DIR"
        rm -rf "$TEMP_DIR"
    fi
}

# Determine temp directory (cross-platform: Windows, macOS, Linux)
get_temp_dir() {
    if [[ -n "$TEMP" ]]; then
        echo "$TEMP"
    elif [[ -n "$TMP" ]]; then
        echo "$TMP"
    elif [[ -n "$TMPDIR" ]]; then
        echo "$TMPDIR"
    else
        echo "/tmp"
    fi
}

# Create temp directory with random suffix
create_temp_dir() {
    local base_temp=$(get_temp_dir)
    local random_suffix=$(openssl rand -hex 8 2>/dev/null || echo "$$")
    local temp_path="${base_temp}/eed_dependabot_$$_${random_suffix}"
    
    if mkdir -p "$temp_path" 2>/dev/null; then
        echo "$temp_path"
    else
        log_error "Failed to create temp directory at: $temp_path"
        return 1
    fi
}

# Setup cleanup trap
trap cleanup EXIT

# Main workflow
main() {
    log_info "Processing PR #${PR_NUMBER}"

    # Get current git remote URL
    CURRENT_DIR=$(pwd)
    if ! cd "$CURRENT_DIR" 2>/dev/null; then
        log_error "Cannot access current directory"
        return 1
    fi

    REPO_URL=$(gh repo view --json url --jq '.url' 2>/dev/null) || {
        log_error "Failed to get repository URL"
        return 1
    }

    log_info "Repository URL: $REPO_URL"

    # Create temp directory (cross-platform)
    TEMP_DIR=$(create_temp_dir) || {
        log_error "Failed to create temp directory"
        return 1
    }
    log_info "Created temp directory: $TEMP_DIR"

    # Clone the repo to temp directory
    log_info "Cloning repository to temp directory (this may take a moment)..."
    local clone_output
    clone_output=$(git clone "$REPO_URL" "$TEMP_DIR/repo" 2>&1)
    local clone_status=$?
    
    if [[ $clone_status -ne 0 ]]; then
        log_error "Failed to clone repository"
        log_error "Exit code: $clone_status"
        log_error "Output: $clone_output"
        return 1
    fi

    log_success "Repository cloned successfully"

    # Change to temp repo directory
    if ! cd "$TEMP_DIR/repo"; then
        log_error "Failed to cd into cloned repo"
        return 1
    fi
    log_success "Ready to process PR"

    # Get PR details
    log_info "Fetching PR details..."
    BRANCH_NAME=$(gh pr view "$PR_NUMBER" --json headRefName --jq '.headRefName' 2>/dev/null) || {
        log_error "Failed to fetch PR #${PR_NUMBER}"
        return 1
    }
    log_info "PR branch: $BRANCH_NAME"

    # Checkout the branch
    log_info "Checking out branch: $BRANCH_NAME"
    if ! git fetch origin "$BRANCH_NAME"; then
        log_error "Failed to fetch branch $BRANCH_NAME"
        return 1
    fi

    if ! git checkout "$BRANCH_NAME"; then
        log_error "Failed to checkout branch $BRANCH_NAME"
        return 1
    fi
    log_success "Checked out branch: $BRANCH_NAME"

    # Create empty commit to trigger CI
    log_info "Creating empty commit to trigger CI..."
    if git commit --allow-empty -m "Trigger CI" 2>&1 | grep -v "^ruff"; then
        log_success "Empty commit created"
    else
        log_warning "Could not create empty commit (might already be up to date)"
    fi

    # Push the commit
    log_info "Pushing changes..."
    if ! git push origin "$BRANCH_NAME"; then
        log_error "Failed to push changes"
        return 1
    fi
    log_success "Changes pushed"

    # Wait for CI to complete
    log_info "Waiting for CI checks to complete (timeout: ${TIMEOUT}s)..."
    START_TIME=$(date +%s)

    while true; do
        # Check elapsed time
        CURRENT_TIME=$(date +%s)
        ELAPSED=$((CURRENT_TIME - START_TIME))

        if [[ $ELAPSED -gt $TIMEOUT ]]; then
            log_error "CI checks timed out after ${TIMEOUT}s"
            return 1
        fi

        # Get current status
        CHECK_STATUS=$(gh pr view "$PR_NUMBER" --json statusCheckRollup --jq '.statusCheckRollup[0].status' 2>/dev/null)
        CHECK_CONCLUSION=$(gh pr view "$PR_NUMBER" --json statusCheckRollup --jq '.statusCheckRollup[0].conclusion' 2>/dev/null)
        CHECK_NAME=$(gh pr view "$PR_NUMBER" --json statusCheckRollup --jq '.statusCheckRollup[0].name' 2>/dev/null)

        if [[ -z "$CHECK_STATUS" ]]; then
            log_warning "Could not fetch PR status, retrying..."
            sleep $POLL_INTERVAL
            continue
        fi

        # Display progress
        printf "\r⏳ ${CHECK_NAME}: ${CHECK_STATUS} | Elapsed: ${ELAPSED}s / ${TIMEOUT}s"

        # Check if completed
        if [[ "$CHECK_STATUS" == "COMPLETED" ]]; then
            printf "\n"

            if [[ "$CHECK_CONCLUSION" == "SUCCESS" ]]; then
                log_success "CI checks passed!"
                break
            elif [[ -z "$CHECK_CONCLUSION" ]]; then
                log_warning "CI check completed but conclusion not yet available, waiting..."
                sleep $POLL_INTERVAL
                continue
            else
                log_error "CI checks failed with conclusion: $CHECK_CONCLUSION"
                return 1
            fi
        fi

        sleep $POLL_INTERVAL
    done

    # Approve the PR
    log_info "Approving PR..."
    if ! gh pr review "$PR_NUMBER" --approve; then
        log_error "Failed to approve PR"
        return 1
    fi
    log_success "PR approved"

    # Merge the PR
    log_info "Merging PR..."
    if ! gh pr merge "$PR_NUMBER" --merge; then
        log_error "Failed to merge PR"
        return 1
    fi
    log_success "PR merged successfully!"

    log_success "All done! PR #${PR_NUMBER} has been processed and merged"
    return 0
}

# Run main function
if main; then
    exit 0
else
    exit 1
fi
