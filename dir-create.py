__author__ = "bobby"
__version__ = "1.0"
__license__ = "MIT"

#dir-create.py
#py dir-create.py
#creates directories Ch1 through Ch26 in current directory.
import os

# Create directories Ch1 through Ch26
for i in range(1, 27):
    directory_name = f"Ch{i}"
    os.makedirs(directory_name, exist_ok=True)
    print(f"Created directory: {directory_name}")

