#Step 3 of the 4 steps to download States Business files, see readme.txt
#we have stored the States Meetings files twice - once with the prefix JBDAC_ and once without. Only process those with JBDAC_ as some content might link to other 'States Meetings' files.
#and that would create chaos. As step 4 we can remove the files prefixed with JBDAC_

import sys
import requests
from bs4 import BeautifulSoup
import urllib3
import re
import os
from urllib.parse import urlparse, unquote

# In-memory list to store processed files
processed_files = []
excluded_domains = ['twitter.com', 'facebook.com']

# Function to extract URLs from HTML content
def extract_urls_from_html(html_content, excluded_domains):
    soup = BeautifulSoup(html_content, 'html.parser')
    download_urls = []

    # Check for <div id="downloadContainer"> section
    download_container = soup.find('div', id='downloadContainer')
    if download_container:
        download_urls += [a.get('href') for a in download_container.find_all('a') if a.get('href') and not any(domain in a.get('href') for domain in excluded_domains)]

    # Check for <div id="CenterContainer"> section
    center_container = soup.find('div', id='CenterContainer')
    if center_container:
        download_urls += [a.get('href') for a in center_container.find_all('a') if a.get('href') and not any(domain in a.get('href') for domain in excluded_domains)]

    return download_urls

# Function to sanitize a filename
def sanitize_filename(filename):
    # Remove characters that are not allowed in filenames
    sanitized = re.sub(r'[<>:"/\\|?*]', "", filename)
    return sanitized

# Function to download a file from a URL
def download_file(url, destination_path):
#    response = requests.get(url, stream=True, allow_redirects=False)

# Disable SSL certificate verification warning
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    response = requests.get(url, stream=True, allow_redirects=False, verify=False)	#broken certificates in states voting records

    if response.status_code == 200:
        with open(destination_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=128):
                file.write(chunk)

        # Save URL to a text file
        url_file_path = f"{destination_path}.loc"
        with open(url_file_path, "w") as url_file:
            url_file.write(url)

# Traverse the directory and its children
directory = './downloaded_files'

for root, dirs, files in os.walk(directory):
    for file in files:
        if 'JBDAC_States-Meeting' in file and file not in processed_files:  # Check if file contains 'JBDAC_States-Meeting' and is not processed
            file_path = os.path.join(root, file)

            # Read the file content with different encodings
            encodings = ['utf-8-sig', 'latin-1']
            content = None
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as file:
                        content = file.read()
                        break
                except UnicodeDecodeError:
                    pass

            if content is None:
                print(f"Ignored: {file_path} (unable to decode)")
                print()  # Print an empty line for separation
                continue

            # Check if the file contains HTML content
            elif '<html' in content.lower() or '<!doctype html' in content.lower():
                print(f"Processing: {file_path}")

                # Extract URLs from the HTML content
                urls = extract_urls_from_html(content, excluded_domains)

                for url in urls:
                    if 'statesvoting-records.gov.gg' in url:
                    	print(f"Skipping: {url} (difficult content, we need simple html tables)")
                    	continue  # Skip these URLs as they're difficult content, we need simple html tables.

                    if 'States-Meeting-information-index' in url:
                    	print(f"Skipping: {url} (main index!)")
                    	continue  # shouldn't be stored here as this is our true 'parent' doc

                    # Check if the URL belongs to gov.gg domain
                    if 'gov.gg' in url:
                        # Extract the filename from the URL
                        filename = os.path.basename(url)

                        # Download the file to the original directory if it doesn't exist
                        destination_path = os.path.join(root, filename)
                        if not os.path.exists(destination_path):
                            download_file(url, destination_path)
                            print(f"Downloaded: {url} -> {destination_path}")
                        else:
                            print(f"Skipping: {url} (Already downloaded)")
                    else:
                        print(f"Ignored: {url}")
            else:
                print(f"Ignored: {file_path} (not HTML)")

            print()  # Print an empty line for separation

            # Add the processed file to the list
            processed_files.append(file)
