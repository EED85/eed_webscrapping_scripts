# Dependabot PR Merge Scripts

Automated scripts to merge dependabot PRs after triggering CI checks. These scripts handle the workflow of:
1. Checking out the PR branch
2. Creating an empty commit to trigger CI
3. Waiting for CI to pass
4. Approving the PR
5. Merging the PR

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

**Output:**
The script provides colored output with status updates:
- 🔵 `[INFO]` - Informational messages
- 🟢 `[SUCCESS]` - Successful operations
- 🟡 `[WARNING]` - Warnings
- 🔴 `[ERROR]` - Errors

### 2. `merge_all_dependabot_prs.sh` - Merge All Open PRs

Finds all open dependabot PRs and processes them one by one.

**Usage:**
```bash
./scripts/merge_all_dependabot_prs.sh [timeout_seconds]
```

**Examples:**
```bash
# Process all open PRs with default 10-minute timeout per PR
./scripts/merge_all_dependabot_prs.sh

# Process all open PRs with custom 15-minute timeout per PR
./scripts/merge_all_dependabot_prs.sh 900

# From project root
bash scripts/merge_all_dependabot_prs.sh
```

**Parameters:**
- `timeout_seconds` (optional): Maximum time to wait for CI per PR (default: 600 seconds = 10 minutes)

**Output:**
Displays:
- List of all found open dependabot PRs
- Processing status for each PR
- Summary with number of successful/failed merges

## How It Works

### The Single PR Script Flow

1. **Validate Input**: Checks PR number exists and required tools are installed
2. **Fetch PR Details**: Gets the branch name and current status
3. **Checkout Branch**: Switches to the PR branch
4. **Trigger CI**: Creates an empty commit with `--allow-empty` flag
5. **Push Changes**: Pushes the commit to trigger GitHub Actions
6. **Wait for CI**: Polls the PR status every 30 seconds until:
   - ✅ CI completes with SUCCESS 
   - ⏱️ Timeout is reached
   - ❌ CI fails
7. **Approve**: Approves the PR if CI passed
8. **Merge**: Merges the PR with `--merge` strategy
9. **Cleanup**: Switches back to main and pulls latest changes

### The Batch Script Flow

1. **Query GitHub**: Finds all open PRs by dependabot user
2. **Display List**: Shows PR numbers and titles
3. **Process Each**: Calls the single PR script for each found PR
4. **Report Summary**: Shows total, successful, and failed PRs

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

- The scripts are safe to run repeatedly - they won't duplicate commits if already present
- CI failures will prevent merging and require manual review
- The `--allow-empty` commit is used to trigger fresh CI runs with your GitHub user context instead of dependabot's limited context
- After merging, the scripts switch back to the main branch
