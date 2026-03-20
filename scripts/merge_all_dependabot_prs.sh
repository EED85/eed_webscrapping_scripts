#!/bin/bash

# Script to find and merge all open dependabot PRs
# Each PR is processed in a temp cloned repo to avoid branch checkout issues
# Usage: ./merge_all_dependabot_prs.sh [--dev] [timeout_seconds]
# Examples:
#   ./merge_all_dependabot_prs.sh                    # Merge all PRs with default timeout
#   ./merge_all_dependabot_prs.sh 900                # Merge all PRs with custom timeout
#   ./merge_all_dependabot_prs.sh --dev              # Dev mode: select one PR to test
#   ./merge_all_dependabot_prs.sh --dev 900          # Dev mode with custom timeout

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
DEV_MODE=false
TIMEOUT="600"  # Default 10 minutes per PR
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MERGE_SCRIPT="$SCRIPT_DIR/merge_dependabot_pr.sh"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --dev)
            DEV_MODE=true
            shift
            ;;
        *)
            # Assume it's the timeout
            TIMEOUT="$1"
            shift
            ;;
    esac
done

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

# Validation
if ! command -v gh &> /dev/null; then
    log_error "GitHub CLI (gh) not installed"
    exit 1
fi

if [[ ! -f "$MERGE_SCRIPT" ]]; then
    log_error "merge_dependabot_pr.sh script not found at $MERGE_SCRIPT"
    exit 1
fi

if [[ ! -x "$MERGE_SCRIPT" ]]; then
    log_warning "Making $MERGE_SCRIPT executable..."
    chmod +x "$MERGE_SCRIPT"
fi

# Main workflow
main() {
    local mode="batch"
    [[ "$DEV_MODE" == "true" ]] && mode="dev"

    log_info "Running in $mode mode (timeout: ${TIMEOUT}s)"
    log_info "Fetching open dependabot PRs..."

    # Get all open dependabot PRs
    PR_NUMBERS=$(gh pr list --author=dependabot --state=open --json number --jq '.[].number' 2>/dev/null)

    if [[ -z "$PR_NUMBERS" ]]; then
        log_success "No open dependabot PRs found"
        return 0
    fi

    # Convert to array
    mapfile -t PR_ARRAY <<<"$PR_NUMBERS"
    TOTAL_PRS=${#PR_ARRAY[@]}

    log_info "Found $TOTAL_PRS open dependabot PR(s):"
    echo ""

    # Display PR info with numbers
    declare -a PR_DISPLAY_INDICES
    for i in "${!PR_ARRAY[@]}"; do
        PR_NUM="${PR_ARRAY[$i]}"
        TITLE=$(gh pr view "$PR_NUM" --json title --jq '.title' 2>/dev/null)
        DISPLAY_INDEX=$((i + 1))
        PR_DISPLAY_INDICES[$i]=$DISPLAY_INDEX
        printf "  [%d] PR #%-4d: %s\n" "$DISPLAY_INDEX" "$PR_NUM" "$TITLE"
    done

    echo ""

    # In dev mode, prompt user to select a PR
    SELECTED_PRS=()
    if [[ "$DEV_MODE" == "true" ]]; then
        log_info "Dev mode: Select a PR to test the script"
        echo "Enter the number of the PR to process (or 'all' to process all):"
        read -r -p "Selection: " selection

        if [[ "$selection" == "all" ]]; then
            SELECTED_PRS=("${PR_ARRAY[@]}")
            echo ""
            log_warning "Dev mode: Processing ALL PRs (not just one)"
        elif [[ "$selection" =~ ^[0-9]+$ ]] && [[ $selection -ge 1 ]] && [[ $selection -le $TOTAL_PRS ]]; then
            SELECTED_INDEX=$((selection - 1))
            SELECTED_PRS=("${PR_ARRAY[$SELECTED_INDEX]}")
            echo ""
            log_info "Dev mode: Processing PR #${SELECTED_PRS[0]} only"
        else
            log_error "Invalid selection: $selection"
            return 1
        fi
    else
        # Batch mode: process all
        SELECTED_PRS=("${PR_ARRAY[@]}")
    fi

    echo ""

    # Process selected PRs
    PROCESSED=0
    FAILED=0
    TOTAL_SELECTED=${#SELECTED_PRS[@]}

    for PR_NUM in "${SELECTED_PRS[@]}"; do
        ((PROCESSED++))
        log_info "Processing PR #$PR_NUM ($PROCESSED/$TOTAL_SELECTED)..."

        if "$MERGE_SCRIPT" "$PR_NUM" "$TIMEOUT"; then
            log_success "PR #$PR_NUM processed successfully"
        else
            log_error "Failed to process PR #$PR_NUM"
            ((FAILED++))
        fi

        echo ""
    done

    # Summary
    log_info "========== SUMMARY =========="
    if [[ "$DEV_MODE" == "true" ]]; then
        log_info "Dev Mode Complete"
    fi
    log_info "Total PRs processed: $TOTAL_SELECTED / $TOTAL_PRS"
    log_success "Successfully processed: $((TOTAL_SELECTED - FAILED))"

    if [[ $FAILED -gt 0 ]]; then
        log_error "Failed: $FAILED"
        return 1
    else
        [[ "$DEV_MODE" == "true" ]] && log_success "Dev mode test successful! You can now run: $0" || log_success "All PRs processed successfully!"
        return 0
    fi
}

# Run main function
if main; then
    exit 0
else
    exit 1
fi
