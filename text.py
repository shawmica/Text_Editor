import os
import re

def search_phrase_in_files(folder_path, phrase):
    results = []

    # Walk through all files and subdirectories
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name.endswith('.txt'):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r', encoding='utf-8') as file:
                    for line_num, line in enumerate(file, 1):
                        if re.search(phrase, line):
                            results.append({
                                'file_path': file_path,
                                'location': line_num,
                                'line': line.strip()
                            })

    return results

# Example usage:
folder_path = "D:\\accadamic\\Research"
phrase = "hi"
search_results = search_phrase_in_files(folder_path, phrase)

for result in search_results:
    print(f"File: {result['file_path']}, Location: {result['location']}, Line: {result['line']}")