# Prob AI: Ultimate Google Colab Launch Guide (V12.2)

Follow these exact steps to launch Prob AI on Google Colab.

### Step 1: Open Google Colab
Go to [colab.research.google.com](https://colab.research.google.com) and create a **New Notebook**.

### Step 2: Enable GPU
1. Click on **Runtime** in the top menu.
2. Select **Change runtime type**.
3. Under **Hardware accelerator**, select **T4 GPU**.
4. Click **Save**.

### Step 3: Launch Option A (Cloudflared - Best for most)
Copy and paste this into a cell and press **Play**.

```python
# 1. Setup Environment
import os, sys
!rm -rf paradox.ai
!git clone https://github.com/Dexter-cal/paradox.ai.git
%cd paradox.ai
sys.path.append(os.getcwd())

# 2. Install Sovereign Dependencies
!pip install -r requirements.txt --quiet
!pip install flask-cloudflared --quiet

# 3. Security Key
os.environ["PROB_PASSWORD"] = "prob_access_2026"

# 4. Launch
from flask_cloudflared import _run_cloudflared
from prob.ui.app import app
try:
    public_url = _run_cloudflared(5000, 5000)
    print(f"\n[LINK] Open Prob AI here: {public_url}")
except:
    print("Cloudflared failed. Try Option B below.")
app.run(port=5000)
```

### Step 4: Launch Option B (Colab Proxy - If Option A shows 404)
If the link above doesn't work, stop the cell and run this one instead:

```python
from google.colab.output import eval_js
print(f"[LINK] Open Prob AI here: {eval_js('google.colab.kernel.proxyPort(5000)')}")
from prob.ui.app import app
app.run(port=5000)
```

---
### Important Note on 404 Errors
If you see a "404 Page Not Found" or "Refused to Connect":
1. Ensure the Flask cell is still running (you should see logs in Colab).
2. Use **Option B** (Colab Proxy) as it is directly integrated into Google's infrastructure.
3. Make sure you are logged into the same Google account in your browser.

---
### How to Update
1. Go to **System Core** in the Prob Dashboard.
2. Click **Check for Updates**.
3. Click **Apply GitHub Update**.
