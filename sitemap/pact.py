import bs4 as bs
import urllib.request
import sys
import os.path

# Reads the table of contents to try and generate a sitemap for the serial.

# I would use the actual sitemap but this is easier since the sitemap is in reverse chronological
# order whereas this is in the actual chronological order and is formatted better.
source = urllib.request.urlopen('https://pactwebserial.wordpress.com/table-of-contents/').read()

# Creates required object.
soup = bs.BeautifulSoup(source,'lxml')


sm_file = sys.argv[1]
# Opens a text file and writes all required URL's into it.
if(os.path.isfile(sm_file)):
	print("Sitemap already exists, using it.")
	sys.exit(0)
else:
	file = open(sm_file,"w")
	print("Creating Sitemap using Table-of-contents.")
	print("WARNING: Table-of-contents CONTAIN ERRORS. Custom fix needed for some chapters (7,8,10,15,16)")

	# Finds all anchor tags and gets the links they point to.
	for url in soup.find_all('a'):
		current = url.get('href')

		# The URL at which we need to stop scraping.
		lastURL = "https://pactwebserial.wordpress.com/2015/02/28/judgment-16-12/"
		# We do not need any URL's after this one, since this is the end of the serial.
		if(current==lastURL):
			file.write(lastURL)
			print("All done! URL file generated\n")
			break

		# The URL's vary a lot with title so I had to get creative on how to get only those we needed. Not the best way but it works.
		Keywords = ['2013','2014','2015']
		if any(keys in current for keys in Keywords):
			if "https://" not in current:
				file.write("https://" + current + "\n")
			else:
				# broken links in Table of content WTF - many of them... monkey-patching futile
				#if current == "https://pactwebserial.wordpress.com/2014/06/10/void-7-5/":
				#	file.write("https://pactwebserial.wordpress.com/2014/06/03/void-7-3/" + "\n")
				#	file.write("https://pactwebserial.wordpress.com/2014/06/07/void-7-4/" + "\n")
				file.write(current + "\n")
				print("Getting link " + url.get('href') + "\n")
file.close()
