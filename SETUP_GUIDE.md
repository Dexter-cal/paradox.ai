# Prob AI v10.0.0 | Setup & Launch Guide

Prob AI is a sovereign discovery organism. Follow these steps to birth the intelligence from scratch.

## 1. Prerequisites
- **Python 3.10+** installed.
- **NVIDIA GPU** with 16GB+ VRAM (for local Llama-3/Phi-3 models).
- **Git** installed.

## 2. Comprehensive Installation

### Step A: Clone the Organism
```bash
git clone https://github.com/Dexter-cal/paradox.ai.git
cd paradox.ai
```

### Step B: Environment Setup
We recommend using a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step C: Install Dependencies
```bash
pip install -r requirements.txt
```

## 3. Configuration & Security

### Set your Access Key (Password)
By default, the password is `prob_access_2026`. Change it via environment variables:
```bash
export PROB_PASSWORD="your_secure_key_here"
export PROB_SECRET_KEY="random_hex_string"
```

## 4. Launching the Sovereign Dashboard

### Local Launch
```bash
python -m prob.ui.app
```
Then navigate to `http://localhost:5000`.

### Google Colab Launch (Public IP Security)
1. Open a Colab Notebook with GPU.
2. Run the `COLAB_GUIDE.md` cells.
3. Use the Cloudflared public URL.
4. **Important:** The Login Page will protect your instance from unauthorized access on the public web.

## 5. Step-by-Step Initialization

1. **Login:** Use your Sovereignty Key (Access Key) to enter the Nexus.
2. **Bootstrap:** Go to the **Discovery Hub** and click **Enable Download & Mission Start**.
   - Prob will autonomously install missing packages.
   - It will download the AI Brain in the background.
   - It will start researching frontiers immediately.
3. **Connect External Brains:** Go to **External Nexus** and input your Gemini/OpenAI API keys to bridge with global intelligence.
4. **Monitor Neural Trace:** Watch the right sidebar to see Prob's granular thoughts as it researchers.

## 6. Advanced Usage
- **Swarm Intelligence:** Deploy background research missions via the Swarm Console.
- **Neural Combat:** Initiate Curiosity Duels (Inquisitor vs Solver) to find knowledge gaps.
- **Axiom Distillation:** Condense findings into universal fundamental truths.

---
*Prob AI: Independent discovery. Universal intelligence.*
