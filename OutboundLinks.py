# from BeautifulSoup import BeautifulSoup
# import urllib2
# import re

html_page = urllib2.urlopen("https://arstechnica.com")
soup = BeautifulSoup(html_page)
for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
    print (link.get('href'))