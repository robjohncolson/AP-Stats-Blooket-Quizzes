import os
import re
import shutil
from datetime import datetime

def extract_chapter_number(filename):
    match = re.search(r'chapter[_\s]?(\d+)', filename, re.IGNORECASE)
    return int(match.group(1)) if match else None

def organize_files(source_folder):
    # Get all files in the source folder
    files = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]
    
    # Sort files by creation time
    files.sort(key=lambda x: os.path.getctime(os.path.join(source_folder, x)))
    
    # Group files by chapter
    chapter_files = {}
    for file in files:
        chapter = extract_chapter_number(file)
        if chapter:
            if chapter not in chapter_files:
                chapter_files[chapter] = []
            chapter_files[chapter].append(file)
    
    # Create chapter folders and move files
    for chapter, files in chapter_files.items():
        chapter_folder = os.path.join(source_folder, f"Chapter_{chapter:02d}")
        os.makedirs(chapter_folder, exist_ok=True)
        
        for file in files:
            source_path = os.path.join(source_folder, file)
            dest_path = os.path.join(chapter_folder, file)
            shutil.move(source_path, dest_path)
            print(f"Moved {file} to {chapter_folder}")

# Usage
source_folder = r"C:\path\to\your\folder"  # Replace with your folder path
organize_files(source_folder)
