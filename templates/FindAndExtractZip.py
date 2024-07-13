import os
import re
import zipfile

def find_and_extract_zip_files(folder_path):
    # Regular expression pattern to match the file names
    pattern = re.compile(r'SensorPushData(?: \(\d+\))?\.zip')

    # Iterate over all files in the folder
    for filename in os.listdir(folder_path):
        if pattern.match(filename):
            file_path = os.path.join(folder_path, filename)
            print(f'Found zip file: {filename}')
            
            # Extract and print the contents of the zip file
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.printdir()  # Print the list of files in the zip archive
                zip_ref.extractall(folder_path)  # Extract all files to the specified folder

if __name__ == "__main__":
    folder_path = './../../Downloads/'  # Replace with your folder path
    find_and_extract_zip_files(folder_path)
