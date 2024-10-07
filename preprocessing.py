import pandas as pd

# Use a raw string or properly escaped string for the path
DATA_PATH = r"C:\Users\ranji\OneDrive\Desktop\llama\data\arxiv-metadata-oai-snapshot.json"

# Read the JSON file in chunks and concatenate
chunks = []

for chunk in pd.read_json(DATA_PATH, lines=True, chunksize=1000):
    chunks.append(chunk)

df = pd.concat(chunks, ignore_index=True)

print(df.head())
