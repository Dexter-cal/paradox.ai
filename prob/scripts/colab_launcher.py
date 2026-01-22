import os
import subprocess
import time
import sys

def run_command(command):
    print(f"Executing: {command}")
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in process.stdout:
        print(line, end="")
    process.wait()
    return process.returncode

def setup_colab():
    print("PROB AI | COLAB BOOTLOADER v1.0")
    print("-" * 40)

    # 1. Install Dependencies
    print("\n[1/4] Installing dependencies (this may take 2-3 minutes)...")
    run_command("pip install -r requirements.txt")
    run_command("pip install flask-cloudflared")

    # 2. Mount Google Drive for persistence
    print("\n[2/4] Setting up persistent storage...")
    try:
        from google.colab import drive
        drive.mount('/content/drive')
        print("Drive mounted. Redirecting memory to /content/drive/MyDrive/prob_memory")
        # Ensure directories exist
        os.makedirs("/content/drive/MyDrive/prob_memory", exist_ok=True)
        # We can symlink the memory dir
        if os.path.exists("prob/memory") and not os.path.islink("prob/memory"):
            run_command("mv prob/memory/* /content/drive/MyDrive/prob_memory/ 2>/dev/null || true")
            run_command("rm -rf prob/memory")
            run_command("ln -s /content/drive/MyDrive/prob_memory prob/memory")
    except ImportError:
        print("Not in Google Colab or Drive already mounted.")

    # 3. Pre-download recommended model if possible
    print("\n[3/4] Preparing Brain (LLaMA-3-8B Optimized)...")
    # This just ensures we are ready

    # 4. Launch the Dashboard with a public tunnel
    print("\n[4/4] Launching Prob AI Dashboard...")
    print("Look for the Cloudflare URL or the Google Proxy link below.")
    print("-" * 40)

    # Start the app in a background process
    # Note: In Colab, we might use google.colab.output.proxy_port(5000)
    try:
        from google.colab.output import proxy_port
        print(f"ACCESS URL: {proxy_port(5000)}")
    except:
        pass

    run_command("python -m prob.ui.app &")

    print("\nPROB AI IS NOW RUNNING.")
    print("Stay on this page to keep the server alive.")

    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        print("Shutting down...")

if __name__ == "__main__":
    setup_colab()
