import pandas as pd

DATA_PATH = r"C:\Users\ranji\OneDrive\Desktop\llama\data\arxiv-metadata-oai-snapshot.json"
chunksize = 1000

# Initialize a dictionary to hold category counts
category_counts = {}

# Process each chunk individually
for chunk in pd.read_json(DATA_PATH, lines=True, chunksize=chunksize):
    # Extract primary categories
    chunk['primary_category'] = chunk['categories'].apply(lambda x: x.split(' ')[0] if isinstance(x, str) else '')
    
    # Count categories in the chunk
    counts = chunk['primary_category'].value_counts()
    
    # Update the overall counts
    for category, count in counts.items():
        if category in category_counts:
            category_counts[category] += count
        else:
            category_counts[category] = count

# Convert the counts dictionary to a DataFrame for better visualization
category_df = pd.DataFrame(list(category_counts.items()), columns=['Category', 'Count'])
category_df.sort_values(by='Count', ascending=False, inplace=True)

print(category_df.head())

# Optional: Save the category counts to a CSV file
category_df.to_csv('category_counts.csv', index=False)
print("Category counts saved to 'category_counts.csv'")
