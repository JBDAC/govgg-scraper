#Step 2 of the 4 steps to download States Business files, see readme.txt
#reads the links.txt file of States Meetings produced by step one script. Each line has the format:
#https://www.gov.gg/article/195843/States-Meeting-on-21st-June-2023
#creates a hierarchical directory structure of yyy/mm/dd and writes the downloaded States Meeting html file there, prefixing that name with JBDAC_
#along with the original file. Only the JBDAC_ files are crawled in later steps, then they are removed at the end
#we do this so we know which ones to process in step 3 (there might be other files linked at that step starting with 'States business'!
# we will remove all JBDAC files at the end
#but at this stage we ALWAYS download the meetings files as they might have changed

import os
import re
import requests
import urllib3

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def download_file(url, destination, filename):
#    response = requests.get(url, allow_redirects=False) gov.gg certificates are crap!
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    response = requests.get(url, allow_redirects=False, verify=False)

    content_copy = response.content  # Make a copy of the content

    destination_path = os.path.join(destination, filename);
    newname = 'JBDAC_' + filename;
    destination_path_JBDAC = os.path.join(destination, newname);
    if response.status_code == 200:
        with open(destination_path, 'wb') as file:
            file.write(response.content)
            file.close()

        with open(destination_path_JBDAC, 'wb') as file:
            file.write(response.content)
            file.close()
        return True
    return False


def parse_html_for_links(url):
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text
        link_pattern = r'<a\s+(?:[^>]*?\s+)?href=(["\'])(.*?)\1'
        links = re.findall(link_pattern, html_content)
        return [link[1] for link in links]
    return []

def get_formatted_date(url):
    # Extract the date using regular expressions
    match = re.search(r'(\d{1,2})(?:st|nd|rd|th)?-(\w+)-(\d{4})', url)
    if match:
        day = match.group(1).zfill(2)
        month = match.group(2)
        year = match.group(3)
        month_dict = {
            'January': '01',
            'February': '02',
            'March': '03',
            'April': '04',
            'May': '05',
            'June': '06',
            'July': '07',
            'August': '08',
            'September': '09',
            'October': '10',
            'November': '11',
            'December': '12'
        }
        if month in month_dict:
            month = month_dict[month]
        return f"{year}/{month}/{day}"
    else:
        return None

# Example usage:
base_directory = './downloaded_files'
links_file = 'links.txt'
download_counter = 0

with open(links_file, 'r') as file:
    urls = file.read().splitlines()

for url in urls:
    if 'signin' in url:
        print(f"Skipping URL: {url} (Contains 'signin')")
        continue

    if 'https://www.gov.gg' not in url:
        print(f"Skipping URL: {url} (Not in 'https://www.gov.gg')")
        continue

    formatted_date = get_formatted_date(url)
    if formatted_date is None:
        print(f"Skipping URL: {url} (Invalid date format)")
        continue

    destination_directory = os.path.join(base_directory, formatted_date)
    create_directory(destination_directory)

    filename = url.split('/')[-1]
    destination_path = os.path.join(destination_directory, filename)

    if download_file(url, destination_directory, filename):
        print(f"Downloaded: {url} -> {destination_path}")
        download_counter += 1
    else:
        print(f"Failed to download: {url}")

    # Parse the downloaded HTML file for additional links
    html_links = parse_html_for_links(url)
    for link in html_links:
        if 'https://www.gov.gg' in link:
            file_url = link.split('#')[0]  # Remove fragment identifier
            file_destination_directory = destination_directory
           
