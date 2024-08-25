__author__ = "Bobby"
__version__ = "1.0.0"
__license__ = "MIT"
__purpose__ = "Organize files in a directory by chapter"

#Claude.ai will be used for each step of this process.
#There are many files in the media directory, which correspond to 26 chapters of a book.
#We want to organize the files into the appropriate chapters.
#We will use the creation date/modification date of the files to determine which chapter they belong to.
#We will also use the file name to determine which chapter they belong to.
#We will create a new directory for each chapter, and move the files into the appropriate chapter.
#We will then show the user the organization of the files.
#We will ask the user to confirm the organization of the files, each step of the way.

#for adding a finer grained control of time so that files are grouped with more resolution.
from datetime import datetime, timedelta

#database functionality
import sqlite3
import pytesseract
from pdf2image import convert_from_path

#xlsx and csv preview functionality.
import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate

#For adding png, webp, pdf preview functionality.
import io
from PIL import Image
import fitz  # PyMuPDF library for PDF handling
import matplotlib.pyplot as plt
#For the main functionality.
import re
import os
import shutil
from datetime import datetime
from collections import defaultdict



#fine grained time based grouping of files.
def group_files_by_creation_time(directory, files, target_groups=26):
    file_times = []
    for file in files:
        creation_time = os.path.getctime(os.path.join(directory, file))
        file_times.append((file, datetime.fromtimestamp(creation_time)))
    
    file_times.sort(key=lambda x: x[1])  # Sort by creation time
    
    total_duration = (file_times[-1][1] - file_times[0][1]).total_seconds()
    group_duration = total_duration / target_groups
    
    groups = defaultdict(list)
    current_group_start = file_times[0][1]
    current_group = 0
    
    for file, time in file_times:
        if (time - current_group_start).total_seconds() > group_duration:
            current_group += 1
            current_group_start = time
        
        chapter = extract_chapter_number(file)
        groups[current_group].append((file, chapter))
    
    return groups

def show_groups(groups):
    for group, files in groups.items():
        print(f"\nGroup {group + 1}:")
        for file, chapter in files:
            print(f"  - {file} (Suggested chapter: {chapter if chapter else 'Unknown'})")

#database functionality
def create_database():
    conn = sqlite3.connect('file_chapters.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS file_chapters
                 (filename TEXT PRIMARY KEY, chapter INTEGER)''')
    conn.commit()
    return conn

def get_chapter_from_db(conn, filename):
    c = conn.cursor()
    c.execute("SELECT chapter FROM file_chapters WHERE filename = ?", (filename,))
    result = c.fetchone()
    return result[0] if result else None

def save_chapter_to_db(conn, filename, chapter):
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO file_chapters (filename, chapter) VALUES (?, ?)",
              (filename, chapter))
    conn.commit()

def extract_text_from_image(file_path):
    try:
        return pytesseract.image_to_string(Image.open(file_path))
    except Exception as e:
        print(f"Error extracting text from image {file_path}: {str(e)}")
        return ""

def extract_text_from_pdf(file_path):
    try:
        pages = convert_from_path(file_path, first_page=1, last_page=2)
        text = ""
        for page in pages:
            text += pytesseract.image_to_string(page)
        return text
    except Exception as e:
        print(f"Error extracting text from PDF {file_path}: {str(e)}")
        return ""

def suggest_chapter(file_path):
    file_extension = os.path.splitext(file_path)[1].lower()
    content = ""
    
    if file_extension in ['.png', '.jpg', '.jpeg', '.webp']:
        content = extract_text_from_image(file_path)
    elif file_extension == '.pdf':
        content = extract_text_from_pdf(file_path)
    elif file_extension in ['.csv', '.xlsx', '.txt']:
        try:
            with open(file_path, 'r') as file:
                content = file.read()
        except Exception as e:
            print(f"Error reading file {file_path}: {str(e)}")
    
    # Simple keyword matching (can be expanded)
    for i in range(1, 27):
        if f"chapter {i}" in content.lower() or f"ch {i}" in content.lower():
            return i
    
    return None

def get_chapter_assignments(groups, media_dir):
    assignments = {}
    conn = create_database()
    
    for date, files in groups.items():
        print(f"\nAssigning chapters for group {date}:")
        for file, suggested_chapter in files:
            file_path = os.path.join(media_dir, file)
            db_chapter = get_chapter_from_db(conn, file)
            
            if db_chapter:
                assignments[file] = db_chapter
                print(f"Chapter {db_chapter} assigned to {file} (from database)")
                continue
            
            if suggested_chapter is None:
                suggested_chapter = suggest_chapter(file_path)
            
            generate_preview(file_path)
            
            while True:
                try:
                    if suggested_chapter:
                        chapter = input(f"Enter chapter number (1-26) for {file} [Suggested: {suggested_chapter}]: ")
                        chapter = int(suggested_chapter) if chapter == '' else int(chapter)
                    else:
                        chapter = int(input(f"Enter chapter number (1-26) for {file}: "))
                    if 1 <= chapter <= 26:
                        assignments[file] = chapter
                        save_chapter_to_db(conn, file, chapter)
                        break
                    else:
                        print("Please enter a number between 1 and 26.")
                except ValueError:
                    print("Please enter a valid number.")
    
    conn.close()
    return assignments

#For adding png, webp, pdf preview functionality.
def generate_preview(file_path):
    file_extension = os.path.splitext(file_path)[1].lower()
    
    if file_extension in ['.webp', '.png']:
        with Image.open(file_path) as img:
            plt.figure(figsize=(5, 5))
            plt.imshow(img)
            plt.axis('off')
            plt.show()
    elif file_extension == '.pdf':
        doc = fitz.open(file_path)
        page = doc.load_page(0)  # Load the first page
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        plt.figure(figsize=(5, 5))
        plt.imshow(img)
        plt.axis('off')
        plt.show()
        doc.close()
    elif file_extension in ['.csv', '.xlsx']:
        try:
            if file_extension == '.csv':
                df = pd.read_csv(file_path, nrows=5)
            else:  # .xlsx
                df = pd.read_excel(file_path, nrows=5)
            print(f"\nPreview of {os.path.basename(file_path)}:")
            print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))
            print("...")
        except Exception as e:
            print(f"Error previewing {file_path}: {str(e)}")
    else:
        print(f"Preview not available for {file_path}")

#For the main functionality.

def extract_chapter_number(filename):
    match = re.search(r'ch(?:apter)?[_\s]?(\d+)', filename, re.IGNORECASE)
    return int(match.group(1)) if match else None

def read_directory_contents(directory):
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]



#Modified for adding png, webp, pdf preview functionality.
def get_chapter_assignments(groups, media_dir):
    assignments = {}
    for date, files in groups.items():
        print(f"\nAssigning chapters for group {date}:")
        for file, suggested_chapter in files:
            file_path = os.path.join(media_dir, file)
            generate_preview(file_path)
            while True:
                try:
                    if suggested_chapter:
                        chapter = input(f"Enter chapter number (1-26) for {file} [Suggested: {suggested_chapter}]: ")
                        chapter = int(suggested_chapter) if chapter == '' else int(chapter)
                    else:
                        chapter = int(input(f"Enter chapter number (1-26) for {file}: "))
                    if 1 <= chapter <= 26:
                        assignments[file] = chapter
                        break
                    else:
                        print("Please enter a number between 1 and 26.")
                except ValueError:
                    print("Please enter a valid number.")
    return assignments

def move_files_to_chapters(directory, assignments):
    for file, chapter in assignments.items():
        chapter_dir = os.path.join(directory, f"Ch{chapter}")
        os.makedirs(chapter_dir, exist_ok=True)
        src = os.path.join(directory, file)
        dst = os.path.join(chapter_dir, file)
        shutil.move(src, dst)

def show_organization_result(directory):
    for chapter in range(1, 27):
        chapter_dir = os.path.join(directory, f"Ch{chapter}")
        if os.path.exists(chapter_dir):
            files = os.listdir(chapter_dir)
            print(f"\nChapter {chapter}:")
            for file in files:
                print(f"  - {file}")

def main():
    media_dir = "media"
    
    # Step 1: Read directory contents
    files = read_directory_contents(media_dir)
    
    # Step 2: Group files by creation time
    groups = group_files_by_creation_time(media_dir, files)
    
    # Step 3: Show groups to user
    show_groups(groups)
    
    # Step 4: Get chapter assignments from user
    assignments = get_chapter_assignments(groups, media_dir)
    
    # Step 5: Move files to appropriate chapters
    move_files_to_chapters(media_dir, assignments)
    
    # Step 6: Show organization result
    show_organization_result(media_dir)

if __name__ == "__main__":
    main()




