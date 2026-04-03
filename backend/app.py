import os
import torch
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
from lime.lime_text import LimeTextExplainer
from fastapi.middleware.cors import CORSMiddleware
import torch.nn.functional as F

app = FastAPI(title="Explainable Clickbait Detection API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the highly-accurate Fine-Tuned Local DistilBERT Model!
MODEL_NAME = "../local_model"

print(f"Loading model {MODEL_NAME}...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
model.eval()

# For LIME
explainer = LimeTextExplainer(class_names=["Non-Clickbait", "Clickbait"])

class PredictionRequest(BaseModel):
    headlines: List[str]

class PredictionResponse(BaseModel):
    predictions: List[Dict[str, Any]]

class ExplainRequest(BaseModel):
    headline: str

def predictor_wrapper(texts):
    # LIME requires a function that takes a list of strings and outputs probabilities (N, num_classes)
    inputs = tokenizer(texts, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    probs = F.softmax(outputs.logits, dim=1).numpy()
    return probs

@app.post("/predict", response_model=PredictionResponse)
async def predict(req: PredictionRequest):
    results = []
    for text in req.headlines:
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = model(**inputs)
        probs = F.softmax(outputs.logits, dim=1)[0].tolist()
        # the mrm8488 model mapping: 0 -> non-clickbait, 1 -> clickbait (usually)
        pred_label = 1 if probs[1] > probs[0] else 0
        confidence = probs[pred_label]
        results.append({
            "headline": text,
            "is_clickbait": bool(pred_label == 1),
            "confidence": confidence,
            "probabilities": probs
        })
    return PredictionResponse(predictions=results)

@app.post("/explain")
async def explain(req: ExplainRequest):
    try:
        exp = explainer.explain_instance(
            req.headline, 
            predictor_wrapper, 
            num_features=6, 
            num_samples=100
        )
        # return word importances
        return {"headline": req.headline, "explanation": exp.as_list()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("backend.app:app", host="0.0.0.0", port=8000, reload=True)
