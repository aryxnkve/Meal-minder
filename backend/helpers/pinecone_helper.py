import os
import pandas as pd
from openai import OpenAI
from pinecone import Pinecone
import torch
from transformers import DistilBertModel, DistilBertTokenizer


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DISHES_NAMESPACE = os.getenv("DISHES_NAMESPACE")
INGREDIENTS_NAMESPACE = os.getenv("INGREDIENTS_NAMESPACE")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

def get_similar_dish_ids(pref_dishes):
    # generate embeddings of user input
    if pref_dishes:
        embedded_pref = get_text_embedding(pref_dishes)
        # Query namespace passed as parameter using title vector
        pinecone = Pinecone(api_key=PINECONE_API_KEY)
        pine_index = pinecone.Index(name=PINECONE_INDEX_NAME)
        query_result = pine_index.query(vector=embedded_pref, 
                                      namespace=DISHES_NAMESPACE, 
                                      top_k=10)
        
        if not query_result.matches:
            print('No similar dishes found')
    
        matches = query_result.matches
        ids = [res.id for res in matches]
        scores = [res.score for res in matches]
        df = pd.DataFrame({'id':ids, 
                        'score':scores
                        })
        
        return list(df['id'])

def get_text_embedding(text, model_name='distilbert-base-uncased'):
    # Load the tokenizer and model
    tokenizer = DistilBertTokenizer.from_pretrained(model_name)
    model = DistilBertModel.from_pretrained(model_name)
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
        print(outputs)
        embeddings = outputs.last_hidden_state.mean(dim=1).numpy().tolist()

    return embeddings

