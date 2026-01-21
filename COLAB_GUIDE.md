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
!git clone https://github.com/Dexter-cal/paradox.ai.git
%cd paradox.ai

# 2. Install all sovereign dependencies
!pip install -r requirements.txt
!pip install flask-cloudflared

# 3. Set your Sovereignty Key (Access Key)
import os
os.environ["PROB_PASSWORD"] = "prob_access_2026" # Change this to your preferred password

# 4. Launch Prob AI with a secure public tunnel
from flask_cloudflared import _run_cloudflared
import threading
from prob.ui.app import app

# This creates the public link
public_url = _run_cloudflared(5000, 5000)
print(f"\n[SUCCESS] Prob Dashboard is booting up!")
print(f"[LINK] Open this URL to access Prob: {public_url}")
print("-" * 50)

# Start the server
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
### How to Update Prob AI
If you make changes to your GitHub repo (`paradox.ai`), you don't need to restart Colab.
1. Go to the **System Core** tab in the Prob Dashboard.
2. Click **Check for Updates**.
3. If an update is found, click **Apply GitHub Update**.
4. Prob will pull your latest code from GitHub automatically.
