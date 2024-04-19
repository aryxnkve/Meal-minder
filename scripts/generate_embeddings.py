from transformers import BertModel, BertTokenizer
import torch

# Load pre-trained BERT model and tokenizer
model = BertModel.from_pretrained('bert-base-uncased')
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

def generate_embeddings(text):
    # Tokenize input text
    inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True)
    # Forward pass through BERT model
    with torch.no_grad():
        outputs = model(**inputs)
    # Extract embeddings (CLS token)
    embeddings = outputs.last_hidden_state[:, 0, :]
    return embeddings.numpy()

# Example usage
text = "Example text for embedding generation."
embeddings = generate_embeddings(text)