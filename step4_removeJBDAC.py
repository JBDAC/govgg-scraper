#Step 4 of the 4 steps to download States Business files, see readme.txt
#this removes the files prefixed by JBDAC_ that step 2 saves for crawling

import os
def delete_files(directory):
    count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.startswith('JBDAC_'):
                file_path = os.path.join(root, file)
                os.remove(file_path)
                count += 1
                print(f"Deleted ({count}/{len(files)}): {file_path}")

# Example usage:
directory = './downloaded_files'
delete_files(directory)
