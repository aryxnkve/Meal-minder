import os
import pandas as pd
from openai import OpenAI
from pinecone import Pinecone

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DISHES_NAMESPACE = os.getenv("DISHES_NAMESPACE")
INGREDIENTS_NAMESPACE = os.getenv("INGREDIENTS_NAMESPACE")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

def get_similar_dish_ids(pref_dishes):
    # generate embeddings of user input
    if pref_dishes:
        openai_client = OpenAI(api_key='sk-proj-ZBfZ7XYA2wBf4KYy9YP1T3BlbkFJP1U2luk2vXfaovOKtFc1',)
        embedded_pref = openai_client.embeddings.create(input=pref_dishes,model=EMBEDDING_MODEL,dimensions=768).data[0].embedding

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
        print("Found below 10 similar dishes:")
        print(df)
        return list(df['id'])

    

