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

import re
import os
import shutil
from datetime import datetime
from collections import defaultdict

def extract_chapter_number(filename):
    match = re.search(r'ch(?:apter)?[_\s]?(\d+)', filename, re.IGNORECASE)
    return int(match.group(1)) if match else None

def read_directory_contents(directory):
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

def group_files_by_creation_date(directory, files):
    groups = defaultdict(list)
    for file in files:
        creation_time = os.path.getctime(os.path.join(directory, file))
        date = datetime.fromtimestamp(creation_time).date()
        chapter = extract_chapter_number(file)
        groups[date].append((file, chapter))
    return groups

def show_groups(groups):
    for date, files in groups.items():
        print(f"\nGroup for {date}:")
        for file, chapter in files:
            print(f"  - {file} (Suggested chapter: {chapter if chapter else 'Unknown'})")

def get_chapter_assignments(groups):
    assignments = {}
    for date, files in groups.items():
        print(f"\nAssigning chapters for group {date}:")
        for file, suggested_chapter in files:
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

def move_files_to_chapters(directory, groups, assignments):
    for date, files in groups.items():
        chapter = assignments[date]
        chapter_dir = os.path.join(directory, f"Ch{chapter}")
        os.makedirs(chapter_dir, exist_ok=True)
        for file in files:
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
    
    # Step 2: Group files by creation date
    groups = group_files_by_creation_date(media_dir, files)
    
    # Step 3: Show groups to user
    show_groups(groups)
    
    # Step 4: Get chapter assignments from user
    assignments = get_chapter_assignments(groups)
    
    # Step 5: Move files to appropriate chapters
    move_files_to_chapters(media_dir, groups, assignments)
    
    # Step 6: Show organization result
    show_organization_result(media_dir)

if __name__ == "__main__":
    main()




