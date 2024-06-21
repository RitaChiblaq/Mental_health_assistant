import faiss
from sentence_transformers import SentenceTransformer

# Initialize model for sentence embeddings
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Initialize FAISS index
dimension = 384  # Dimension of embeddings
index = faiss.IndexFlatL2(dimension)


# Function to add user messages to the index
def add_to_index(message, index):
    embedding = model.encode([message])
    index.add(embedding)


# Function to search similar messages
def search_index(query, index, k=5):
    query_embedding = model.encode([query])
    D, I = index.search(query_embedding, k)
    return I