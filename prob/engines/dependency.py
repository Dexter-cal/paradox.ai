import subprocess
import sys

class DependencyEngine:
    def __init__(self):
        pass

    def install_package(self, package_name):
        """Installs a python package via pip."""
        print(f"Prob is installing dependency: {package_name}...")
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", package_name],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return f"Successfully installed {package_name}."
            else:
                return f"Failed to install {package_name}. Error: {result.stderr}"
        except Exception as e:
            return f"Error during installation of {package_name}: {e}"

    def install_from_requirements(self, requirements_path):
        """Installs packages from a requirements file."""
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", requirements_path],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return "Successfully installed all dependencies from requirements."
            else:
                return f"Failed to install requirements. Error: {result.stderr}"
        except Exception as e:
            return f"Error during requirements installation: {e}"
