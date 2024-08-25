__author__ = "Bobby"
__version__ = "1.0.0"
__license__ = "MIT"
__purpose__ = "Organize files in a directory by chapter"

#Claude.ai will be used for each step of this process.
#1.  First we need to read the contents of the directory "media".
#2.  After that, we should group file names by their creation date.
#3.  We should show the user what groups have been formed by their creation date.
#4.  Then, we should ask the user which groups belong into which chapter, of which there are 26.
#5.  After that, we should move the files into the appropriate chapter directory from the "media" directory.
#6.  Finally, we should show the user the result of the organization.

import os
import shutil
from datetime import datetime
from collections import defaultdict

def read_directory_contents(directory):
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

def group_files_by_creation_date(directory, files):
    groups = defaultdict(list)
    for file in files:
        creation_time = os.path.getctime(os.path.join(directory, file))
        date = datetime.fromtimestamp(creation_time).date()
        groups[date].append(file)
    return groups

def show_groups(groups):
    for date, files in groups.items():
        print(f"\nGroup for {date}:")
        for file in files:
            print(f"  - {file}")

def get_chapter_assignments(groups):
    assignments = {}
    for date in groups.keys():
        while True:
            try:
                chapter = int(input(f"Enter chapter number (1-26) for group {date}: "))
                if 1 <= chapter <= 26:
                    assignments[date] = chapter
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




