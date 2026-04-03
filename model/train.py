import pandas as pd
import torch
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification, Trainer, TrainingArguments
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
import os

def compute_metrics(pred):
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)
    precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average='binary')
    acc = accuracy_score(labels, preds)
    return {
        'accuracy': acc,
        'f1': f1,
        'precision': precision,
        'recall': recall
    }

def main():
    print("Loading clickbait dataset...")
    # Using a hypothetical local CSV dataset
    dataset_path = "clickbait_data.csv"
    if not os.path.exists(dataset_path):
        print(f"Dataset {dataset_path} not found. Please provide a CSV with 'headline' and 'label' columns.")
        return

    df = pd.read_csv(dataset_path)
    train_texts, val_texts, train_labels, val_labels = train_test_split(
        df['headline'].tolist(), 
        df['label'].tolist(), 
        test_size=0.2,
        random_state=42
    )

    tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')

    train_encodings = tokenizer(train_texts, truncation=True, padding=True)
    val_encodings = tokenizer(val_texts, truncation=True, padding=True)

    class ClickbaitDataset(torch.utils.data.Dataset):
        def __init__(self, encodings, labels):
            self.encodings = encodings
            self.labels = labels

        def __getitem__(self, idx):
            item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
            item['labels'] = torch.tensor(self.labels[idx])
            return item

        def __len__(self):
            return len(self.labels)

    train_dataset = ClickbaitDataset(train_encodings, train_labels)
    val_dataset = ClickbaitDataset(val_encodings, val_labels)

    model = DistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased', num_labels=2)

    training_args = TrainingArguments(
        output_dir='./results',          
        num_train_epochs=3,              
        per_device_train_batch_size=16,  
        per_device_eval_batch_size=64,   
        warmup_steps=500,                
        weight_decay=0.01,               
        logging_dir='./logs',            
        logging_steps=10,
        eval_strategy="epoch"
    )

    trainer = Trainer(
        model=model,                         
        args=training_args,                  
        train_dataset=train_dataset,         
        eval_dataset=val_dataset,
        compute_metrics=compute_metrics
    )

    print("Starting training...")
    trainer.train()

    print("Evaluating model...")
    results = trainer.evaluate()
    print("Evaluation Results:", results)

    print("Saving model to ./local_model")
    model.save_pretrained('../local_model')
    tokenizer.save_pretrained('../local_model')

if __name__ == "__main__":
    main()
