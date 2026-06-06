import chromadb
from sentence_transformers import SentenceTransformer
import os

# Load embedding model
print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Set up ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")

# Create or get collection
collection = client.get_or_create_collection("catechism")

# Read the catechism file
print("Reading catechism...")
with open("data/catechism.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Split into chunks by paragraph
chunks = []
current_chunk = ""

for line in text.split("\n"):
    if line.startswith("PARAGRAPH") and current_chunk:
        chunks.append(current_chunk.strip())
        current_chunk = line
    else:
        current_chunk += " " + line

if current_chunk:
    chunks.append(current_chunk.strip())

# Remove empty chunks
chunks = [c for c in chunks if len(c) > 20]

print(f"Found {len(chunks)} chunks")

# Add to ChromaDB
print("Storing in ChromaDB...")
collection.add(
    documents=chunks,
    ids=[f"chunk_{i}" for i in range(len(chunks))],
    embeddings=model.encode(chunks).tolist()
)

print("Done! Catechism is now stored in ChromaDB.")
print(f"Total chunks stored: {collection.count()}")
