# Explainable Clickbait Detection System

A complete full-stack AI system that detects clickbait headlines and provides word-level explanations using LIME (Local Interpretable Model-Agnostic Explanations).

## Features
- **Accurate Detection**: Powered by a fine-tuned DistilBERT transformer running entirely locally.
- **Explainable AI (XAI)**: Understand *why* an AI model made its prediction with visual heatmaps indicating word importance.
- **Privacy-focused**: Runs computationally on your machine via FastAPI.
- **Web App**: A premium web portal for manual headline testing with fluid UI and Chart.js integration.
- **Browser Extension**: A Chrome extension that analyzes reading material in real-time, highlighting clickbait inline.

## 0. Installation & Prerequisites
Before setting up the model, ensure you have the necessary dependencies installed in your environment:

1.  **Clone/Download** this repository.
2.  **Initialize your environment** (recommended):
    ```bash
    python -m venv .venv
    .\.venv\Scripts\activate
    ```
3.  **Install Requirements**:
    ```bash
    pip install -r requirements.txt
    ```
*Note: This will install core libraries like `torch` (for AI processing), `transformers` (for the DistilBERT model), `fastapi` (for the backend), and `lime` (for explainability).*

## 1. Local Model Setup & Training
This system relies on highly localized, robust weights. You must first fine-tune the raw DistilBERT architecture onto your specific clickbait dataset!
1. Ensure your Python virtual environment is active: `.\.venv\Scripts\activate`
2. Place a CSV file containing your annotated training data into `model/clickbait_data.csv` (Must feature `headline` and `label` columns).
3. Execute the fine-tuning script:
```bash
python model/train.py
```
*This script tokenizes your data, loops through multiple epochs on your hardware, evaluates its accuracy metrics (F1/Precision/Recall), and exports the finalized checkpoint to the `local_model/` directory root.*

## 2. Starting the Backend API
Once your model finishes training and exports `.safetensors`, you can launch the inference API:
```bash
uvicorn backend.app:app --host 0.0.0.0 --port 8000
```
*The `app.py` logic automatically detects and parses the `/local_model` checkpoint you just generated.*

## 3. Web Application
Simply open `frontend/index.html` in your web browser or utilize an IDE Live Server tool. You can freely type test headlines to observe Chart.js behavior and LIME heatmaps.

## 4. Chrome Extension
1. Open Chrome, Edge, or Brave and navigate to `chrome://extensions/`
2. Enable the **Developer mode** toggle in the top right.
3. Click **Load unpacked** and select the `/extension` directory located in this project.
4. Browse any news aggregation site (Google News, Buzzfeed, etc.) and observe the tool dynamically checking titles against your personal AI model. Headlines determined as non-clickbait will be bordered in green, and clickbait in red! Hover over them for an analytical breakdown.
