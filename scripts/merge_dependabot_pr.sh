#!/bin/bash

# Script to automatically merge dependabot PRs after triggering CI
# Usage: ./merge_dependabot_pr.sh <PR_NUMBER> [timeout_seconds]
# Example: ./merge_dependabot_pr.sh 89 600

set -e

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

# Main workflow
main() {
    log_info "Processing PR #${PR_NUMBER}"
    
    # Get PR details
    log_info "Fetching PR details..."
    PR_DATA=$(gh pr view "$PR_NUMBER" --json headRefName,statusCheckRollup 2>/dev/null) || {
        log_error "Failed to fetch PR #${PR_NUMBER}"
        exit 1
    }
    
    BRANCH_NAME=$(echo "$PR_DATA" | gh pr view "$PR_NUMBER" --json headRefName --jq '.headRefName')
    log_info "PR branch: $BRANCH_NAME"
    
    # Checkout the branch
    log_info "Checking out branch: $BRANCH_NAME"
    git fetch origin "$BRANCH_NAME:$BRANCH_NAME" 2>/dev/null || git fetch origin
    git checkout "$BRANCH_NAME" || {
        log_error "Failed to checkout branch $BRANCH_NAME"
        exit 1
    }
    
    # Create empty commit to trigger CI
    log_info "Creating empty commit to trigger CI..."
    if git commit --allow-empty -m "Trigger CI"; then
        log_success "Empty commit created"
    else
        log_warning "Could not create empty commit (might already be up to date)"
    fi
    
    # Push the commit
    log_info "Pushing changes..."
    git push origin "$BRANCH_NAME" || {
        log_error "Failed to push changes"
        exit 1
    }
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
            exit 1
        fi
        
        # Get current status
        STATUS_DATA=$(gh pr view "$PR_NUMBER" --json statusCheckRollup 2>/dev/null) || {
            log_warning "Could not fetch PR status, retrying..."
            sleep $POLL_INTERVAL
            continue
        }
        
        # Extract status and conclusion
        CHECK_STATUS=$(echo "$STATUS_DATA" | gh pr view "$PR_NUMBER" --json statusCheckRollup --jq '.statusCheckRollup[0].status' 2>/dev/null)
        CHECK_CONCLUSION=$(echo "$STATUS_DATA" | gh pr view "$PR_NUMBER" --json statusCheckRollup --jq '.statusCheckRollup[0].conclusion' 2>/dev/null)
        CHECK_NAME=$(echo "$STATUS_DATA" | gh pr view "$PR_NUMBER" --json statusCheckRollup --jq '.statusCheckRollup[0].name' 2>/dev/null)
        
        # Display progress
        printf "\r⏳ ${CHECK_NAME}: ${CHECK_STATUS} | Elapsed: ${ELAPSED}s / ${TIMEOUT}s"
        
        # Check if completed
        if [[ "$CHECK_STATUS" == "COMPLETED" ]]; then
            printf "\n"
            
            if [[ "$CHECK_CONCLUSION" == "SUCCESS" ]]; then
                log_success "CI checks passed!"
                break
            else
                log_error "CI checks failed with conclusion: $CHECK_CONCLUSION"
                exit 1
            fi
        fi
        
        sleep $POLL_INTERVAL
    done
    
    # Approve the PR
    log_info "Approving PR..."
    gh pr review "$PR_NUMBER" --approve || {
        log_error "Failed to approve PR"
        exit 1
    }
    log_success "PR approved"
    
    # Merge the PR
    log_info "Merging PR..."
    gh pr merge "$PR_NUMBER" --merge || {
        log_error "Failed to merge PR"
        exit 1
    }
    log_success "PR merged successfully!"
    
    # Return to main branch
    log_info "Switching back to main branch..."
    git checkout main
    git pull origin main
    
    log_success "All done! PR #${PR_NUMBER} has been processed and merged"
}

# Run main function
main
