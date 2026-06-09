import chromadb
from sentence_transformers import SentenceTransformer
import os

# Load embedding model
print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Set up ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")

# Delete existing collections and start fresh
for name in ["catechism", "bible"]:
    try:
        client.delete_collection(name)
        print(f"Cleared old {name} collection")
    except:
        pass

# Create collections
catechism_collection = client.get_or_create_collection("catechism")
bible_collection = client.get_or_create_collection("bible")

# Chunk by size with overlap
def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i+chunk_size])
        if len(chunk) > 50:
            chunks.append(chunk)
        i += chunk_size - overlap
    return chunks

def ingest_file(filepath, collection, name):
    print(f"\nReading {name}...")
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
    
    print(f"Total characters: {len(text):,}")
    chunks = chunk_text(text)
    print(f"Created {len(chunks)} chunks")
    
    print(f"Storing {name} in ChromaDB...")
    batch_size = 100
    
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i+batch_size]
        embeddings = model.encode(batch).tolist()
        collection.add(
            documents=batch,
            ids=[f"chunk_{j}" for j in range(i, i+len(batch))],
            embeddings=embeddings
        )
        print(f"Stored chunks {i} to {i+len(batch)}")
    
    print(f"Done! {name} chunks stored: {collection.count()}")

# Ingest both documents
ingest_file("data/catechism_full.txt", catechism_collection, "Catechism")
ingest_file("data/bible.txt", bible_collection, "Bible")

print("\n✝️ All documents ingested successfully!")
print(f"Catechism chunks: {catechism_collection.count()}")
print(f"Bible chunks: {bible_collection.count()}")