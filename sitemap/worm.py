import bs4 as bs
import urllib.request
import sys
import os.path

# Reads the table of contents to try and generate a sitemap for the serial.

# I would use the actual sitemap but this is easier since the sitemap is in reverse chronological
# order whereas this is in the actual chronological order and is formatted better.
source = urllib.request.urlopen('https://parahumans.wordpress.com/table-of-contents/').read()

# Creates required object.
soup = bs.BeautifulSoup(source,'lxml')

# Opens a text file and writes all required URL's into it.
# If the sitemap already exists, the script simply exits without an error.
sm_file = sys.argv[1]
if(os.path.isfile(sm_file)):
    print("Sitemap already exists, either from a previous scrape, or a custom sitemap.")
    print("Not generating sitemap.")
    sys.exit(0)
else:
    file = open(sm_file,"w")
    print("File opened\n")

# Finds all anchor tags and gets the links they point to.
for url in soup.find_all('a'):

# We do not need any URL's after this one, since this is the end of the serial.
    current = url.get('href')
# The final chapter's URL. We do not need any URL's after we reach this one.
    lastURL = "parahumans.wordpress.com/2013/11/19/interlude-end/"
    if(current==lastURL):

        file.write(lastURL)
        print("All done! URL file generated\n")
        break

# The URL's vary a lot with title so I had to get creative on how to get only those we needed. Not the best way but it works.
    Keywords = ['2012','2013','category']
    if any(keys in current for keys in Keywords):
        requiredURL = url.get('href')
        requiredURL = requiredURL.replace("½","&#189;")
        file.write(requiredURL + "\n")
        print("Getting link " + url.get('href') + "\n")

file.close()
