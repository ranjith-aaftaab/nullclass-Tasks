import streamlit as st
import pandas as pd
import json
import os

# ------------------------------
# Load Datasets
# ------------------------------

CSV_PATH = r"C:\Users\ranji\OneDrive\Desktop\llama\data\cs_arxiv_papers.csv"  # Update this path
JSON_PATH = r"C:\Users\ranji\OneDrive\Desktop\llama\data\arxiv-metadata-oai-snapshot.json"  # Update this path

# Load CSV file
@st.cache
def load_csv_data(file_path):
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        return df
    else:
        st.error(f"File not found: {file_path}")
        return None

# Load JSON file
@st.cache
def load_json_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            data = [json.loads(line) for line in f]
        return data
    else:
        st.error(f"File not found: {file_path}")
        return None

# ------------------------------
# Streamlit App Layout
# ------------------------------

# Set page title
st.title('ArXiv Paper Chatbot')

# Load data
st.write("Loading datasets...")
df_csv = load_csv_data(CSV_PATH)
json_data = load_json_data(JSON_PATH)

if df_csv is not None and json_data is not None:
    st.write("Datasets loaded successfully!")
else:
    st.error("Error loading the datasets.")

# Show a sample of the data
if st.checkbox("Show sample data"):
    st.write(df_csv.head())

# ------------------------------
# User Interaction
# ------------------------------

# User input for question
st.write("Ask a question related to ArXiv papers:")
user_input = st.text_input("Type your question here:")

# Basic matching logic (this can be extended with NLP)
if user_input:
    st.write(f"Searching for relevant papers related to: {user_input}")
    
    # Simple keyword search in 'title' or 'abstract'
    matching_papers = df_csv[df_csv['title'].str.contains(user_input, case=False, na=False) | 
                             df_csv['abstract'].str.contains(user_input, case=False, na=False)]
    
    # Display the results
    if not matching_papers.empty:
        st.write(f"Found {len(matching_papers)} matching papers:")
        for index, row in matching_papers.iterrows():
            st.write(f"**Title**: {row['title']}")
            st.write(f"**Abstract**: {row['abstract']}")
            st.write(f"**Authors**: {row['authors']}")
            st.write("---")
    else:
        st.write("No matching papers found.")

# Optionally, you can implement a more advanced logic such as embeddings search using FAISS or another NLP-based model.
