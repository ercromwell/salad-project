
import sys
import urllib2
from HTMLParser import HTMLParser

links = open('/Users/jogaleotasprung/Desktop/links.txt','r')

i = 1
for line in links:
    url = line
    pageContents = urllib2.urlopen(url)
    
    filename = '/Users/jogaleotasprung/Desktop/salad_recipes/salads-'
    filename= filename + str(i) +'.txt'
    f = open(filename, 'w')
    f.write(pageContents.read())
    f.close()
    i = i+1
        #if i == 10:
        
#  break

