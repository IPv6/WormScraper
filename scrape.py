import bs4 as bs
import urllib.request
import sys
import os
from collections import OrderedDict

# Dictionary to store sitemap.
ScraperURL = []

# Reads which web series to scrape.
# Changes input to lower case for ease of use.
option = sys.argv[1].lower()

if len(sys.argv) > 2:
    # The directory to store the output file in.
    directory = sys.argv[2]
else:
    # If no directory is supplied default to the current directory.
    directory = os.getcwd()

validdir = os.path.isdir(directory)

if validdir is False:
    print("Invalid directory. Enter a valid directory.")

# Turn all inputs to lower case.
    option = input().lower()
# Runs the prerequisite python file which builds the sitemap.
# This can be done manually if needed.
try:
    os.system("python sitemap/" + option + ".py")
except Exception as exception:
    print(exception)
# Reads the sitemap data generated by the previous system call.
with open(option + '-sitemap.txt') as f:

# Loads data into dictionary and splits it by new line
# Each entry in the dictionary is now a seperate URL to be scraped.
    ScraperURL = f.read()
    ScraperURL = ScraperURL.split("\n")

"""

Turns out some anchor tags are repeated for no reason at all (Atleast no real reason that I can think of)
in both worm's and pact's table of contents, so I could either rescrape from sitemap which would make
the entire thing flow in reverse order because sitemap updates as story updates, or remove
duplicates from the list while preserving order. Which is what this piece of code does.

For future reference :

https://stackoverflow.com/questions/480214/how-do-you-remove-duplicates-from-a-list-in-whilst-preserving-order

"""
ScraperURL = list(OrderedDict.fromkeys(ScraperURL))

# Opens the file the output is to be written in.
file = open(directory + "/" + option + ".html","w",encoding="utf-8")

# Run scraper for every entry in the dictionary.
for url in ScraperURL:
    SourceURL = url
    if len(SourceURL) == 0:
        continue
    # Prints current URL being scraped for debugging convenience.
    print("Starting "+ SourceURL +"\n")
    # Open the url and read the source.
    source = urllib.request.urlopen(SourceURL).read()
    # Prints current URL being scraped for debugging convenience.
    print("// parsing "+ SourceURL +"\n")
    soup = bs.BeautifulSoup(source,'lxml')

    ###   Calibre detects titles and chapters inside h1 or h2 tags if they belong to the "chapter" class.
    ###   This ensures that caibre generates a page break during conversion.
    file.write("<h2 class=\"chapter\">" + soup.title.text + "</h2>")
    file.write("</br></br>")

    # For every single p tag, the text within is scraped and added to the current output file.
    holders = soup.find_all('div', class_='entry-content')
    for hld in holders:
        print("// entry-content found")
        for paragraph in hld.find_all('p'):
    # Some p tags are used in the source site for paragraph breaks. Ignores those.
            paragh = paragraph.get_text().strip()
            print("- p", paragh)
            if len(paragh) == 0:
                continue
            # Writes the text to output file.
            # Avoiding a few words by making sure they're not the current string extracted.
            listtoavoid = ["Next Chapter","Previous Chapter","Connecting to %s","<strike>","Fill in your details below"]
            if any(lta in paragh for lta in listtoavoid):
                print("// skipping navigation")
            else:
                file.write("<p>" + paragh + "</p>")

    # End of chapter shows in console output for user convenience.
    print("Done with Chapter "+SourceURL+"\n")
print("All done with " + option + ". Use Calibre to convert into preferred format. :]\n")
print("Removing sitemap files now.")
os.system("rm " + option + "-sitemap.txt")
file.close()
