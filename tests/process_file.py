import os
import json
import re
import sys

def extract_info(text):
    # This is a simplified extraction logic. 
    # A more robust solution would use more advanced NLP techniques 
    # to accurately identify and extract entities.
    return {
        "phone": re.findall(r'\b(?:\+?1[\s.-]?)?(?:\(?([2-9][0-8][0-9])\)?[\s.-]?)?([2-9][0-9]{2})[\s.-]?([0-9]{4})\b', text),
        "email": re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text),
        "website": re.findall(r'https?://(?:www\.)?[\w\d.-]+\.[a-zA-Z]{2,}(?:/[\w\d./?=#&%-]*)?', text)
    }

def process_file(filename):
    research_dir = "/home/ubuntu/.research_files/"
    filepath = os.path.join(research_dir, filename)
    with open(filepath, 'r') as f:
        content = f.read()
    
    info = extract_info(content)

    parts = filename.replace(".md", "").split('_')
    category = parts[0]
    subcategory = " ".join(parts[1:]) if len(parts) > 1 else ""

    # This is a placeholder for company name and other details
    # A more sophisticated script would parse the content to get these details
    new_data = {
        "category": category,
        "subcategory": subcategory,
        "company": " ".join(parts[2:]) if len(parts) > 2 else " ".join(parts[1:]),
        "phone": info.get("phone"),
        "email": info.get("email"),
        "website": info.get("website"),
        "hq": "N/A",
        "service_areas": "N/A",
        "raw_content": content
    }

    output_path = "/home/ubuntu/real_estate_guide/contact_databases.json"
    with open(output_path, 'r+') as f:
        data = json.load(f)
        data.append(new_data)
        f.seek(0)
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        process_file(sys.argv[1])
