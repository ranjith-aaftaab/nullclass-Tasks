import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
import sys
from tqdm import tqdm
import torch  # Import torch to handle device selection

# ------------------------------
# Configuration Parameters
# ------------------------------

DATA_CSV_PATH = r"C:\Users\ranji\OneDrive\Desktop\llama\data\cs_arxiv_papers.csv"  # Update if different
FAISS_INDEX_PATH = r"C:\Users\ranji\OneDrive\Desktop\llama\faiss_arxiv.index"  # Update if different
BATCH_SIZE = 1000  # Number of records per batch; adjust based on your system
EMBEDDING_BATCH_SIZE = 64  # Batch size for SentenceTransformer; adjust as needed

# ------------------------------
# Validate File Paths
# ------------------------------

if not os.path.exists(DATA_CSV_PATH):
    print(f"Error: The CSV file was not found at {DATA_CSV_PATH}. Please ensure it exists.")
    sys.exit(1)

# ------------------------------
# Initialize SentenceTransformer Model
# ------------------------------

try:
    # Set device to CPU since there's no GPU
    device = "cpu"
    print(f"Using device: {device}")
    model = SentenceTransformer('all-MiniLM-L6-v2', device=device)
    print("SentenceTransformer model loaded successfully.")
except Exception as e:
    print(f"Error loading SentenceTransformer model: {e}")
    sys.exit(1)

# ------------------------------
# Initialize FAISS Index
# ------------------------------

try:
    # Determine embedding dimension from the model
    dummy_embedding = model.encode(["test"], batch_size=1)
    dimension = len(dummy_embedding[0])

    # Initialize FAISS index (Flat L2)
    index = faiss.IndexFlatL2(dimension)
    print(f"Initialized FAISS IndexFlatL2 with dimension: {dimension}")
except Exception as e:
    print(f"Error initializing FAISS index: {e}")
    sys.exit(1)

# ------------------------------
# Process CSV in Batches and Generate Embeddings
# ------------------------------

try:
    # Determine total number of rows for progress bar
    # Subtract 1 for the header
    with open(DATA_CSV_PATH, 'r', encoding='utf-8') as f:
        total_rows = sum(1 for _ in f) - 1

    print(f"Total records to process: {total_rows}")

    # Read CSV in chunks
    reader = pd.read_csv(DATA_CSV_PATH, chunksize=BATCH_SIZE)

    for chunk in tqdm(reader, total=(total_rows // BATCH_SIZE) + 1, desc="Processing Batches"):
        # Ensure 'abstract' column exists
        if 'abstract' not in chunk.columns:
            print("Error: 'abstract' column not found in the CSV.")
            continue

        # Handle missing abstracts
        abstracts = chunk['abstract'].fillna('').tolist()

        # Generate embeddings
        embeddings = model.encode(abstracts, batch_size=EMBEDDING_BATCH_SIZE, show_progress_bar=False)
        embeddings = np.array(embeddings).astype('float32')

        # Add embeddings to FAISS index
        index.add(embeddings)

    print(f"Total embeddings in FAISS index: {index.ntotal}")

except Exception as e:
    print(f"Error during embedding generation or FAISS indexing: {e}")
    sys.exit(1)

# ------------------------------
# Save FAISS Index
# ------------------------------

try:
    faiss.write_index(index, FAISS_INDEX_PATH)
    print(f"FAISS index saved successfully at {FAISS_INDEX_PATH}.")
except Exception as e:
    print(f"Error saving FAISS index: {e}")
    sys.exit(1)
