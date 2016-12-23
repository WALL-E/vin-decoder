#!/usr/bin/python


from bs4 import BeautifulSoup

soup = BeautifulSoup(open('LVSHCAMB1CE054249.html'), "html.parser")

print soup.table.prettify()

#for child in soup.table.children:
#    print child
