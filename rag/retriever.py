import chromadb
from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("catechism")

def retrieve(query, n_results=3):
    """Search ChromaDB for relevant chunks based on the user's question."""
    
    # Convert question to embedding
    query_embedding = model.encode([query]).tolist()
    
    # Search ChromaDB
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results
    )
    
    # Return the relevant chunks as a single string
    chunks = results["documents"][0]
    return "\n\n".join(chunks)
