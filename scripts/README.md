# Dependabot PR Merge Scripts

Automated scripts to merge dependabot PRs after triggering CI checks. These scripts handle the workflow of:
1. Cloning the repo to a temporary directory (to avoid branch checkout issues when you're on a feature branch)
2. Checking out the PR branch in the temp repo
3. Creating an empty commit to trigger CI
4. Waiting for CI to pass
5. Approving the PR
6. Merging the PR
7. Cleaning up the temporary directory

## Key Feature

**These scripts work seamlessly whether you're on a feature branch or main branch!** They use a temporary clone of the repository, so checking out dependabot branches won't affect your current working directory.

## Prerequisites

- `git` command-line tool
- `gh` (GitHub CLI) installed and authenticated
- Bash shell (macOS, Linux, or Git Bash on Windows)

## Scripts

### 1. `merge_dependabot_pr.sh` - Merge a Single PR

Automatically processes a single dependabot PR.

**Usage:**
```bash
./scripts/merge_dependabot_pr.sh <PR_NUMBER> [timeout_seconds]
```

**Examples:**
```bash
# Merge PR #89 with default 10-minute timeout
./scripts/merge_dependabot_pr.sh 89

# Merge PR #89 with custom 15-minute timeout
./scripts/merge_dependabot_pr.sh 89 900

# From project root
bash scripts/merge_dependabot_pr.sh 89
```

**Parameters:**
- `PR_NUMBER` (required): The number of the PR to process
- `timeout_seconds` (optional): Maximum time to wait for CI (default: 600 seconds = 10 minutes)

**Key Features:**

The script automatically optimizes how it triggers CI by:

1. **Smart Rebasing** (Preferred): First attempts to rebase the PR branch on the main branch
   - If successful without conflicts: pushes the rebased branch and skips to CI checks
   - Updates the PR with latest changes from main
   - Better for CI - may resolve issues that disappear with latest code

2. **Empty Commit Fallback**: If rebase fails (conflicts detected)
   - Aborts the rebase and falls back to creating an empty commit
   - Still triggers CI but maintains current branch content
   - Safe approach when conflicts would require manual resolution

**Output:**
The script provides colored output with status updates:
- 🔵 `[INFO]` - Informational messages
- 🟢 `[SUCCESS]` - Successful operations
- 🟡 `[WARNING]` - Warnings
- 🔴 `[ERROR]` - Errors

Example output showing successful rebase:
```
[INFO] Processing PR #88
[INFO] Attempting to rebase on main branch...
[INFO] Using main branch: origin/main
[SUCCESS] Rebase successful! Branch is now up-to-date with main
[INFO] Pushing rebased changes...
[SUCCESS] Rebased branch pushed successfully
[INFO] Waiting for CI checks to complete...
```

### 2. `merge_all_dependabot_prs.sh` - Merge All Open PRs (or Test One in Dev Mode)

Finds all open dependabot PRs and processes them. Includes an optional **dev mode** to test the script on a single PR before processing all of them.

**Usage:**
```bash
./scripts/merge_all_dependabot_prs.sh [--dev] [timeout_seconds]
```

**Examples:**
```bash
# Process all open PRs with default 10-minute timeout per PR
./scripts/merge_all_dependabot_prs.sh

# Process all open PRs with custom 15-minute timeout per PR
./scripts/merge_all_dependabot_prs.sh 900

# Dev mode: list PRs and let you choose which one to test
./scripts/merge_all_dependabot_prs.sh --dev

# Dev mode with custom timeout
./scripts/merge_all_dependabot_prs.sh --dev 900

# From project root
bash scripts/merge_all_dependabot_prs.sh --dev
```

**Parameters:**
- `--dev` (optional): Enable dev mode - lists all PRs and prompts you to select one to process. Useful for testing the script before running in batch mode.
- `timeout_seconds` (optional): Maximum time to wait for CI per PR (default: 600 seconds = 10 minutes)

### Dev Mode Workflow

Dev mode is perfect for testing before full automation:

```bash
# 1. Run in dev mode
./scripts/merge_all_dependabot_prs.sh --dev

# 2. Script lists available PRs:
# [1] PR #89: Bump ruff from 0.9.7 to 0.14.14
# [2] PR #90: Bump requests from 2.28.0 to 2.32.4
#
# Enter the number of the PR to process (or 'all' to process all):

# 3. Enter selection (e.g., "1" to test just PR #89)
1

# 4. Watch the script work on that single PR
# 5. Once confirmed it's working, run the full batch:
./scripts/merge_all_dependabot_prs.sh
```

**Output:**
Displays:
- List of all found open dependabot PRs
- Processing status for each PR
- Summary with number of successful/failed merges

## How It Works

### The Single PR Script Flow

1. **Validate Input**: Checks PR number exists and required tools are installed
2. **Setup Cleanup**: Ensures temp directory is deleted even if errors occur
3. **Get Repository Info**: Fetches the remote URL using GitHub CLI
4. **Create Temp Clone**: Creates a temporary directory and clones the full repository
5. **Fetch PR Details**: Gets the branch name for the PR
6. **Checkout Branch**: Checks out the PR branch in the temp repo
7. **Smart CI Trigger** (Two approaches - tries rebase first):
   - **Attempt Rebase** (Preferred): Tries to rebase the PR branch on main/master
     - ✅ If successful: Pushes the rebased, up-to-date branch
     - ❌ If conflicts detected: Aborts rebase and falls back to empty commit
   - **Empty Commit** (Fallback): Creates an empty commit to trigger CI
     - Used when rebase would create conflicts
     - Still effectively triggers fresh CI run from your user account
8. **Wait for CI**: Polls the PR status every 30 seconds until:
   - ✅ CI completes with SUCCESS
   - ⏱️ Timeout is reached
   - ❌ CI fails
9. **Approve**: Approves the PR if CI passed
10. **Merge**: Merges the PR with `--merge` strategy
11. **Cleanup**: Automatically removes the temp directory (via trap, even on error)

### The Batch PR Script Flow

1. **Query GitHub**: Finds all open PRs by dependabot user
2. **Display List**: Shows PR numbers and titles
3. **Dev Mode (Optional)**: If `--dev` flag is used, prompts user to select one PR
4. **Process Each**: Calls the single PR script for each found (or selected) PR
5. **Report Summary**: Shows total, successful, and failed PRs

## Error Handling

Both scripts include error handling for:
- Missing GitHub CLI or Git
- PR not found
- Failed git operations
- CI check failures
- Merge conflicts
- Timeout waiting for CI

If any step fails, the script exits with error code 1.

## Troubleshooting

### "GitHub CLI not installed"
Install `gh` from https://cli.github.com/

### "Failed to fetch PR details"
Ensure you're authenticated with:
```bash
gh auth login
```

### "Failed to merge PR"
Check:
- PR doesn't have merge conflicts
- PR has required approvals (if 2-approval rule is set)
- You have write access to the repository
- CI checks actually passed

### Script times out waiting for CI
- Increase the timeout parameter (longer job times may need 1800+ seconds)
- Check GitHub Actions logs in the PR for actual failure reasons

### "Cannot delete remote tracking branch"
This is usually not a fatal error. The PR is still merged successfully.

## Running from Any Branch

Unlike the initial workflow you performed manually, **these scripts can be run from any branch** (feature branches, develop, main, etc.) without affecting your current working directory:

```bash
# You're on your feature branch - no problem!
git checkout my-feature-branch

# Run the script from your feature branch directory
./scripts/merge_dependabot_pr.sh 89

# Your feature branch is untouched
# The temp repo handles all the merging
git status  # Still on my-feature-branch with all your work intact
```

## Running from Windows

If using Git Bash on Windows:
```bash
bash scripts/merge_dependabot_pr.sh 89
```

Or make the scripts executable in Windows:
```powershell
# In PowerShell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
bash scripts/merge_dependabot_pr.sh 89
```

## Running from CI/CD

These scripts can be integrated into GitHub Actions:

```yaml
name: Merge Dependabot PRs
on:
  schedule:
    # Run daily at 6 AM UTC
    - cron: '0 6 * * *'

jobs:
  merge:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Merge all dependabot PRs
        run: bash scripts/merge_all_dependabot_prs.sh 900
```

## Notes

- **Smart Rebase First**: The script attempts to rebase PR branches on main/master before using empty commits
  - Keeps PRs up-to-date with latest code (better for CI)
  - Safely falls back to empty commit if conflicts are detected
  - No manual intervention needed either way
- **Safe to run from any branch**: The scripts use a temporary clone, so your current working directory is never affected
- **Safe to run repeatedly**: They won't duplicate commits if already present
- **Automatic cleanup**: Even if the script fails, the temp directory is automatically cleaned up via signal trap
- **CI failures prevent merging**: If checks fail, the script stops and requires manual review
- **Empty Commit Fallback**: When rebase has conflicts, creates a fresh CI trigger with your authenticated GitHub user context (instead of dependabot's limited context which lacks access to secrets)
- **After merging**: The temp repo is discarded; your current branch remains unchanged
- **Works on feature branches**: You can safely run these scripts while working on any branch
