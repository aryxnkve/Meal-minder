import pinecone

# Connect to Pinecone
pinecone.connect(api_key="YOUR_API_KEY")

# Create or get a Pinecone index
index_name = "your_index_name"
if index_name not in pinecone.list_indexes():
    pinecone.create_index(index_name, dimension=768)  # Adjust dimension based on your embeddings
index = pinecone.Index(index_name)

# Upload embeddings to Pinecone
index.upsert(items=['item_id'], vectors=[embeddings])