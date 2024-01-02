import sys
import requests
from bs4 import BeautifulSoup
import re

url = "https://www.gov.gg/article/163276/States-Meeting-information-index#selectednavItem191711"

# Send a GET request to the URL and retrieve the webpage content
print("Downloading webpage...")
response = requests.get(url)
content = response.content

# Save the webpage content to a file called "local_copy.html"
with open("local_copy.html", "wb") as file:
    file.write(content)
print("Webpage downloaded and saved as local_copy.html.")

# Create a BeautifulSoup object with the local copy
print("Parsing the webpage...")
soup = BeautifulSoup(content, "html.parser")

# Find all anchor tags with href attribute containing "States-Meeting"
links = soup.find_all("a", href=re.compile("States-Meeting"))

# Get the years range from the command line arguments
year_start = int(sys.argv[1]) if len(sys.argv) > 1 else None
year_end = int(sys.argv[2]) if len(sys.argv) > 2 else None

# Write the links to a file called "links.txt" for the specified year range
print("Extracting links...")
with open("links.txt", "w") as links_file:
    for link in links:
        link_text = link.text
        match = re.search(r"\d{4}", link_text)  # Extract the first occurrence of a four-digit number from the link text
        if match:
            link_year = int(match.group())
            if not year_start or (year_start and (link_year == year_start or (year_end and link_year >= year_start and link_year <= year_end))):
                links_file.write(link.get("href") + "\n")

print("Links extracted and saved to links.txt for the year range", year_start if year_start else "all", "-", year_end if year_end else "all")
