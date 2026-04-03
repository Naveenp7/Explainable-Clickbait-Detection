from transformers import AutoModelForSequenceClassification, AutoTokenizer

models_to_test = [
    "jy46604790/ClickBait-Detector",
    "amandakonet/clickbait_model",
    "akash1309/clickbait_detector",
    "eliasalvador/clickbait_detector",
    "distilbert-base-uncased-finetuned-sst-2-english"
]

for model in models_to_test:
    try:
        print(f"Trying {model}...")
        t = AutoTokenizer.from_pretrained(model)
        m = AutoModelForSequenceClassification.from_pretrained(model)
        print(f"SUCCESS: {model}")
        break  # exit as soon as one succeeds
    except Exception as e:
        print(f"FAILED: {model} with error {e}")
