import chromadb
from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")
catechism_collection = client.get_or_create_collection("catechism")
bible_collection = client.get_or_create_collection("bible")

def retrieve(query, n_results=3):
    """Search both Catechism and Bible for relevant chunks."""
    
    query_embedding = model.encode([query]).tolist()
    
    # Search Catechism
    catechism_results = catechism_collection.query(
        query_embeddings=query_embedding,
        n_results=n_results
    )
    
    # Search Bible
    bible_results = bible_collection.query(
        query_embeddings=query_embedding,
        n_results=n_results
    )
    
    # Combine results
    catechism_chunks = catechism_results["documents"][0]
    bible_chunks = bible_results["documents"][0]
    
    context = "FROM THE CATECHISM:\n" + "\n\n".join(catechism_chunks)
    context += "\n\nFROM SCRIPTURE:\n" + "\n\n".join(bible_chunks)
    
    return context