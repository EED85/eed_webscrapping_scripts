#!/bin/bash

# Script to find and merge all open dependabot PRs
# Usage: ./merge_all_dependabot_prs.sh [timeout_seconds]
# Example: ./merge_all_dependabot_prs.sh 600

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
TIMEOUT="${1:-600}"  # Default 10 minutes per PR
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MERGE_SCRIPT="$SCRIPT_DIR/merge_dependabot_pr.sh"

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
    log_info "Fetching open dependabot PRs..."

    # Get all open dependabot PRs
    PR_NUMBERS=$(gh pr list --author=dependabot --state=open --json number --jq '.[].number' 2>/dev/null)

    if [[ -z "$PR_NUMBERS" ]]; then
        log_success "No open dependabot PRs found"
        exit 0
    fi

    # Convert to array
    mapfile -t PR_ARRAY <<<"$PR_NUMBERS"
    TOTAL_PRS=${#PR_ARRAY[@]}

    log_info "Found $TOTAL_PRS open dependabot PR(s):"

    # Display PR info
    for PR_NUM in "${PR_ARRAY[@]}"; do
        TITLE=$(gh pr view "$PR_NUM" --json title --jq '.title' 2>/dev/null)
        echo "  - PR #$PR_NUM: $TITLE"
    done

    echo ""

    # Process each PR
    PROCESSED=0
    FAILED=0

    for PR_NUM in "${PR_ARRAY[@]}"; do
        ((PROCESSED++))
        log_info "Processing PR #$PR_NUM ($PROCESSED/$TOTAL_PRS)..."

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
    log_info "Total PRs: $TOTAL_PRS"
    log_success "Successfully processed: $((TOTAL_PRS - FAILED))"

    if [[ $FAILED -gt 0 ]]; then
        log_error "Failed: $FAILED"
        exit 1
    else
        log_success "All PRs processed successfully!"
        exit 0
    fi
}

# Run main function
main
