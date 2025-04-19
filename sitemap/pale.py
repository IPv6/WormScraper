from bs4 import BeautifulSoup
import requests
import os.path
import sys
import bs4 as bs
import urllib.request
import os.path

source = urllib.request.urlopen('https://palewebserial.wordpress.com/table-of-contents/').read()

# Creates required object.
soup = bs.BeautifulSoup(source,'lxml')

# Opens a text file and writes all required URL's into it.
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
    current = url.get('href')

# The URL at which we need to stop scraping.
    lastURL = "https://palewebserial.wordpress.com/2023/10/08/loose-ends-e-6/"
# We do not need any URL's after this one, since this is the end of the serial.
    if(current==lastURL):
        file.write(lastURL)
        print("All done! URL file generated\n")
        break

# The URL's vary a lot with title so I had to get creative on how to get only those we needed. Not the best way but it works.
    Keywords = ['2014','2015','2016','2017','2018','2020','2021','2022','2023']
    if any(keys in current for keys in Keywords):
        if "https://" not in current:
                file.write("https://" + current + "\n")
        else:
            file.write(current + "\n")
            print("Getting link " + url.get('href') + "\n")
file.close()

# # Also unlike worm or pale there was no table of contents so I had to scrape from the sitemap.
# req = requests.get("https://palewebserial.wordpress.com/sitemap.xml")
# xml = req.text
# soup = BeautifulSoup(xml,"lxml")

# # Finds all url tags within the xml file.
# sitemapTags = soup.find_all("url")
# print("sitemapTags", sitemapTags)

# dictionary = {}
# i = 0

# # Opens the output sitemap file.
# if(os.path.isfile(sm_file)):
#     print("Sitemap already exists, either from a previous scrape, or user has generated a custom sitemap.\n")
#     print("Not generating sitemap.\n")
#     sys.exit(0)
# else:
#     file = open(sm_file,"w")
#     print("File opened\n")

# # Finds every url in the sitemap that hold 2014/15/16/17/18 since that's the naming convention followed,
# # and adds it to a dictionary.
# for sitemap in sitemapTags:
#     current = sitemap.findNext("loc").text
#     Keywords = ['2014','2015','2016','2017','2018','2020','2021','2022','2023']
#     if any(keys in current for keys in Keywords):
#         dictionary[i] = current
#         i+=1

# # The sitemap holds the urls in reverse chronological order so I can to reverse the entire URL list.
# while i > 0:
#     print("Getting link : " + dictionary[i-1] + "\n" )

# # Writing URL's in chronological order to the file.
#     file.write(dictionary[i-1])
#     file.write("\n")
#     i-=1

# print("All done! URL file generated. \n")
# file.close()
