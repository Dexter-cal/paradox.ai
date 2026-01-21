import subprocess
import sys
import pkg_resources

class DependencyManager:
    def __init__(self):
        self.essential_packages = [
            "transformers", "torch", "bitsandbytes", "peft",
            "accelerate", "psutil", "pynvml", "flask",
            "duckduckgo_search", "matplotlib", "requests", "datasets"
        ]

    def check_and_install_all(self):
        """Checks all essential packages and installs missing ones."""
        results = []
        for pkg in self.essential_packages:
            if not self.is_installed(pkg):
                print(f"[DEP_MANAGER] Installing missing dependency: {pkg}")
                res = self.install(pkg)
                results.append(res)
            else:
                results.append(f"{pkg}: OK")
        return results

    def is_installed(self, package):
        try:
            pkg_resources.get_distribution(package)
            return True
        except pkg_resources.DistributionNotFound:
            return False

    def install(self, package):
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            return f"Installed {package}."
        except Exception as e:
            return f"Failed to install {package}: {e}"

    def get_status(self):
        status = {}
        for pkg in self.essential_packages:
            status[pkg] = self.is_installed(pkg)
        return status
