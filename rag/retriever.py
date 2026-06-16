import os
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

# Connect to Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("fides")

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve(query, n_results=3):
    """Search Pinecone for relevant chunks."""
    
    # Convert question to embedding
    query_embedding = model.encode([query]).tolist()[0]
    
    # Search Pinecone
    results = index.query(
        vector=query_embedding,
        top_k=n_results,
        include_metadata=True
    )
    
    # Separate by source
    catechism_chunks = []
    bible_chunks = []
    
    for match in results["matches"]:
        source = match["metadata"]["source"]
        text = match["metadata"]["text"]
        if source == "catechism":
            catechism_chunks.append(text)
        else:
            bible_chunks.append(text)
    
    # Build context
    context = ""
    if catechism_chunks:
        context += "FROM THE CATECHISM:\n" + "\n\n".join(catechism_chunks)
    if bible_chunks:
        context += "\n\nFROM SCRIPTURE:\n" + "\n\n".join(bible_chunks)
    
    return context