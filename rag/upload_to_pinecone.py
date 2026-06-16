import os
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

# Connect to Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index("fides")

# Load embedding model
print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Chunk text helper
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

def upload_file(filepath, source_name):
    print(f"\nReading {source_name}...")
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    chunks = chunk_text(text)
    print(f"Created {len(chunks)} chunks")

    # Upload in batches
    batch_size = 100
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i+batch_size]
        embeddings = model.encode(batch).tolist()

        vectors = [
            {
                "id": f"{source_name}_chunk_{i+j}",
                "values": embeddings[j],
                "metadata": {"text": batch[j], "source": source_name}
            }
            for j in range(len(batch))
        ]

        index.upsert(vectors=vectors)
        print(f"Uploaded chunks {i} to {i+len(batch)}")

    print(f"Done! {source_name} uploaded successfully")

# Upload both documents
upload_file("data/catechism_full.txt", "catechism")
upload_file("data/bible.txt", "bible")

print("\n✝️ All documents uploaded to Pinecone!")
stats = index.describe_index_stats()
print(f"Total vectors in Pinecone: {stats['total_vector_count']}")
