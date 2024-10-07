import pandas as pd
import json
import os

# Define file paths
INPUT_JSON_PATH = r"C:\Users\ranji\OneDrive\Desktop\llama\data\arxiv-metadata-oai-snapshot.json"
OUTPUT_CSV_PATH = r"C:\Users\ranji\OneDrive\Desktop\llama\data\cs_arxiv_papers.csv"

# Check if input JSON file exists
if not os.path.exists(INPUT_JSON_PATH):
    print(f"Error: The input JSON file was not found at {INPUT_JSON_PATH}. Please verify the path.")
    exit(1)

# Define the chunk size
CHUNK_SIZE = 100000  # Adjust based on your system's capability

# Initialize a counter for processed records
processed_records = 0

# Initialize a list to hold filtered records
filtered_records = []

# Function to process and filter each record
def process_record(record):
    # Check if 'categories' field exists and starts with 'cs.'
    categories = record.get('categories', '')
    if isinstance(categories, str) and categories.startswith('cs.'):
        # Extract relevant fields
        filtered_record = {
            'id': record.get('id', ''),
            'submitter': record.get('submitter', ''),
            'authors': record.get('authors', ''),
            'title': record.get('title', ''),
            'comments': record.get('comments', ''),
            'journal_ref': record.get('journal-ref', ''),
            'doi': record.get('doi', ''),
            'report_no': record.get('report-no', ''),
            'categories': record.get('categories', ''),
            'license': record.get('license', ''),
            'abstract': record.get('abstract', ''),
            'update_date': record.get('update_date', ''),
            'authors_parsed': record.get('authors_parsed', [])
        }
        return filtered_record
    return None

# Open the output CSV file in write mode and write headers
with open(OUTPUT_CSV_PATH, 'w', encoding='utf-8') as csvfile:
    # Define the column names
    columns = [
        'id', 'submitter', 'authors', 'title', 'comments',
        'journal_ref', 'doi', 'report_no', 'categories',
        'license', 'abstract', 'update_date', 'authors_parsed'
    ]
    # Write the header
    csvfile.write(','.join(columns) + '\n')

# Read and process the JSON file line by line
with open(INPUT_JSON_PATH, 'r', encoding='utf-8') as f:
    for line in f:
        try:
            record = json.loads(line)
            filtered_record = process_record(record)
            if filtered_record:
                # Convert authors_parsed list to a string
                filtered_record['authors_parsed'] = json.dumps(filtered_record['authors_parsed'])
                # Create a CSV row
                row = ','.join(['"{}"'.format(str(filtered_record[col]).replace('"', '""')) for col in columns])
                # Append the row to the CSV file
                with open(OUTPUT_CSV_PATH, 'a', encoding='utf-8') as csvfile:
                    csvfile.write(row + '\n')
                processed_records += 1
                if processed_records % 10000 == 0:
                    print(f"Processed {processed_records} records.")
        except json.JSONDecodeError as e:
            print(f"JSONDecodeError: {e} - Skipping line.")
            continue
        except Exception as e:
            print(f"Unexpected error: {e} - Skipping line.")
            continue

print(f"Finished processing. Total records processed and written to CSV: {processed_records}")
