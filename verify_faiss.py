import faiss
import os
import sys

# Define the path to your FAISS index
FAISS_INDEX_PATH = r"C:\Users\ranji\OneDrive\Desktop\llama\faiss_arxiv.index"  # Update if different

# Check if the FAISS index file exists
if not os.path.exists(FAISS_INDEX_PATH):
    print(f"Error: The FAISS index file was not found at {FAISS_INDEX_PATH}. Please ensure it exists.")
    sys.exit(1)

# Load the FAISS index
try:
    index = faiss.read_index(FAISS_INDEX_PATH)
    print("FAISS index loaded successfully.")
    print(f"Number of vectors in the index: {index.ntotal}")
except Exception as e:
    print(f"An error occurred while loading the FAISS index: {e}")
    sys.exit(1)
