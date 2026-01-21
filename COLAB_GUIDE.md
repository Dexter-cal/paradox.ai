# Prob AI: Ultimate Google Colab Launch Guide

Follow these exact steps to launch Prob AI on Google Colab.

### Step 1: Open Google Colab
Go to [colab.research.google.com](https://colab.research.google.com) and create a **New Notebook**.

### Step 2: Enable GPU
1. Click on **Runtime** in the top menu.
2. Select **Change runtime type**.
3. Under **Hardware accelerator**, select **T4 GPU**.
4. Click **Save**.

### Step 3: Copy and Paste this Script
Copy the entire block below into the first cell of your Colab notebook and press the **Play** button.

```python
# 1. Clone the Paradox.ai repository
import os
import sys

# Remove existing if any
!rm -rf paradox.ai

# Clone fresh
!git clone https://github.com/Dexter-cal/paradox.ai.git

# Move into the directory
%cd paradox.ai

# Add the current directory to sys.path so 'prob' can be found
sys.path.append(os.getcwd())

# 2. Install all sovereign dependencies
# Using --quiet to keep the output clean
!pip install -r requirements.txt --quiet
!pip install flask-cloudflared --quiet
!pip install duckduckgo-search --upgrade --quiet

# 3. Set your Sovereignty Key (Access Key)
os.environ["PROB_PASSWORD"] = "prob_access_2026" # Change this to your preferred password

# 4. Launch Prob AI with a secure public tunnel
from flask_cloudflared import _run_cloudflared
from prob.ui.app import app

# This creates the public link
# Note: It might take 10-20 seconds for the URL to appear
try:
    public_url = _run_cloudflared(5000, 5000)
    print(f"\n" + "="*50)
    print(f"[SUCCESS] Prob Dashboard is booting up!")
    print(f"[LINK] Open this URL to access Prob: {public_url}")
    print("="*50 + "\n")
except Exception as e:
    print(f"[ERROR] Tunnel failed: {e}")

# Start the server
# Use debug=False for stable public deployment
app.run(port=5000)
```

### Step 4: Open the Dashboard
1. Look for the line that says `[LINK] Open this URL to access Prob: https://xxxx.trycloudflare.com`.
2. Click the link.
3. You will see the **Prob Nexus Login Page**.
4. Enter your Access Key (default: `prob_access_2026`).

### Step 5: Birth the Organism
1. Once inside, go to the **Discovery Hub**.
2. Click **Birth Organism** (Enable Download & Mission Start).
3. Prob will now autonomously download its brain and begin researching.

---
### Troubleshooting
If you get `ModuleNotFoundError: No module named 'prob'`, make sure you ran the `%cd paradox.ai` and `sys.path.append(os.getcwd())` lines correctly.

---
### How to Update Prob AI
If you make changes to your GitHub repo (`paradox.ai`):
1. Go to the **System Core** tab in the Prob Dashboard.
2. Click **Check for Updates**.
3. Click **Apply GitHub Update**.
