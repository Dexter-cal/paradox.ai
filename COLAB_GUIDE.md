# Prob AI: Google Colab Deployment Guide

To run Prob AI v10.0.0 on Google Colab and access the Sovereign Dashboard:

### 1. Open a new Colab Notebook
Ensure you have "GPU" enabled in **Runtime -> Change runtime type**.

### 2. Clone and Setup
Run the following in a cell:
```python
!git clone https://github.com/your-username/prob-ai.git
%cd prob-ai
!pip install -r requirements.txt
!pip install flask-cloudflared
```

### 3. Launch with Tunnel
Prob is designed for autonomous bootloading. Run this to start the server and get a public URL:
```python
from flask_cloudflared import _run_cloudflared
import threading
from prob.ui.app import app

# This will give you a public URL to access the dashboard
public_url = _run_cloudflared(5000, 5000)
print(f"Prob Dashboard is live at: {public_url}")

app.run(port=5000)
```

### 4. Enable the Organism
Once the UI opens:
1. Go to the **Discovery Hub**.
2. Click **Enable Download & Mission Start**.
3. Prob will autonomously:
   - Check and install any missing dependencies.
   - Download the AI Brain (LLM) in the background.
   - Initialize the Swarm, Dream, and Singularity engines.
   - Start researching global frontiers even if you disconnect from the notebook.

---
*Note: For persistent memory, mount your Google Drive and update the paths in `prob/config/models.json`.*
