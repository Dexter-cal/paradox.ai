import subprocess
import os
import sys

class UpdateEngine:
    def __init__(self, repo_path="."):
        self.repo_path = repo_path

    def check_for_updates(self):
        try:
            # Fetch latest info
            subprocess.check_call(["git", "fetch"], cwd=self.repo_path)
            # Check if local is behind remote
            status = subprocess.check_output(["git", "status", "-uno"], cwd=self.repo_path, text=True)
            if "Your branch is behind" in status:
                return True, "Updates available on GitHub."
            return False, "Prob is up to date."
        except Exception as e:
            return False, f"Update check failed: {str(e)}"

    def apply_update(self):
        """Pulls latest changes and notifies user to restart."""
        try:
            # 1. Stash any local changes to prevent merge conflicts
            subprocess.check_call(["git", "stash"], cwd=self.repo_path)
            # 2. Pull latest
            subprocess.check_call(["git", "pull"], cwd=self.repo_path)
            # 3. Re-install requirements just in case
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], cwd=self.repo_path)

            return True, "Update applied successfully. Please restart the Prob server to apply changes."
        except Exception as e:
            return False, f"Update failed: {str(e)}"
