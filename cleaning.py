import json

input_path = r"C:\Users\ranji\OneDrive\Desktop\json\arxiv-metadata-oai-snapshot.json"  # Update this path
output_path = r"C:\Users\ranji\OneDrive\Desktop\llama\arxiv-cleaned.json"  # Desired output path

with open(input_path, 'r', encoding='utf-8') as infile, open(output_path, 'w', encoding='utf-8') as outfile:
    for line_number, line in enumerate(infile, start=1):
        line = line.strip()
        if not line:
            continue  # Skip empty lines
        try:
            # Attempt to parse the JSON object
            json_obj = json.loads(line)
            # Write the valid JSON object to the output file
            json.dump(json_obj, outfile)
            outfile.write('\n')
        except json.JSONDecodeError as e:
            print(f"Skipping malformed JSON on line {line_number}: {e}")
            continue  # Skip malformed lines
