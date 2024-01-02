The States of Guernsey's Website (www.gov.gg) has poor search facilities. Whether this is by incompetence or intent is unclear.

Openness, accountability and good corporate governance demand easy and fast access to information; this is particularly so with States Business - the meetings, Hansards, proposals etc.

A solution to this problem would be to scrape the content carefully and index it properly with a full-text search.
Recoll is a powerful open-source full-text search tool that efficiently indexes and retrieves information from various document formats, allowing users to quickly search and locate specific content within their collections of documents.
So we use Recoll with a web front end.

What follows is to download States Business from the gov.gg web server so that it can be properly indexed with a full-text search.
We convert the flat file structure on the States webserver to a date hierarchy. Steps:

Create a folder such as: /run/media/jbdac/nvme/gov/all/
This is our root.

Copy the Python scripts there and run them from a terminal opened at this location. The scrips will:

Download the specific States Business HTML file in our root folder by using the Python scripts supplied to extract the 300+ links (as of 21/06/2023) to relevant 'Meeting files' & store these links in a links.txt file.
Parse the links.txt file to download each 'Meeting file' from the States webserver, saving it in a created yyyy/mm/dd folder.
Recursively process this new hierarchy of files to extract the relevant proper document links to relevant documents such as Hansards etc for that meeting from each meeting file, and download the files into the relevant dated directories.

url = "https://www.gov.gg/article/163276/States-Meeting-information-index#selectednavItem191711"

To accomplish all of this, run, (from Terminal opened in the same directory):

python step1_generatelinks.py
(edit the links.txt file in a text editor to limit the dates for download, you may optionally specify a year or range of years as parameters)
python step2_download.py
python step3_getkids.py
python step4_removeJBDAC.py

The Python files are commented.
