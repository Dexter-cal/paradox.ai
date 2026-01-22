# PROB AI | ULTIMATE GOOGLE COLAB GUIDE

## Step 1: Open a New Notebook
Go to [colab.research.google.com](https://colab.research.google.com) and create a new Python 3 notebook.

## Step 2: Enable GPU
1. Go to **Edit** > **Notebook settings**.
2. Select **T4 GPU** (or better) from the Hardware accelerator dropdown.
3. Click **Save**.

## Step 3: Clone and Launch
Copy and paste the following code into a Colab cell and run it:

```python
# 1. Clone the repository
!git clone https://github.com/your-repo/prob-ai.git
%cd prob-ai

# 2. Run the specialized Colab Launcher
!python prob/scripts/colab_launcher.py
```

## How the Launcher Works
The `colab_launcher.py` script performs the following:
1. **Dependency Injection:** Installs all required libraries (`transformers`, `bitsandbytes`, `flask-cloudflared`, etc.).
2. **Persistence:** Mounts your Google Drive so your Memory and Knowledge Graph are never lost.
3. **Optimized Loading:** Forces the Brain to use 4-bit quantization to fit the LLaMA-3-8B model into the T4 GPU's 16GB VRAM.
4. **Public Tunnel:** Uses Cloudflared or Google's native proxy to give you a public URL to access the Prob Dashboard.

## Login Credentials
- **Access Key:** `prob_access_2026` (Change this in `prob/ui/app.py` for better security).

## Tips
- **Keep it Alive:** Use the "Autonomous Loop" feature in the UI to keep the Colab instance active.
- **Background Mode:** Prob runs the server in the background, so you can still use the Colab cells for manual commands.
