"""
POC to set the search bar to comics and type in a value.
then save the result of the search
"""
import os
import requests
from PIL import Image
import copy
import urllib.request
from bs4 import BeautifulSoup
from urllib.parse import quote

def results(url_, issue_, level_,):
    local_filename, headers = urllib.request.urlretrieve(url_, issue_ + level_)
    page = open(local_filename)
    return page

def grab_image(soup_, img_name):
    img_add = soup_.find(class_='itemimage')
    image_url = img_add['src']
    img = Image.open(requests.get(image_url, stream=True).raw)
    img.save(img_name + '.jpg')

def cleanfolder(filepath):
    for filename in os.listdir(filepath):
        os.unlink(filepath + filename)
        # print(filename)

base = 'https://www.atomicempire.com'
starter= '/Comic/TitleList?txt='
#issue = 'The Flash 761'
issue = 'Nightwing 76'
lz = 'processing\\'


fissue= issue.replace(' ', '_')
qissue = quote(issue)

address = base + starter + qissue

#search results assuming it matches to only one
page_search = results(address, lz + fissue, '_search.txt')
soup = BeautifulSoup(page_search, 'html.parser')
page_search.close()
line = soup.find(class_='row-title', href=True).get('href')

# Titles page it matches to only one
Title_Search = results(base + line, lz + fissue, '_titles.txt')
soup = BeautifulSoup(Title_Search, 'html.parser')
Title_Search.close()
line = soup.find(class_='col item-content pl-0').find('a', href=True).get('href')

# Issue page takes the first one
Issue_search = results(base + line, lz + fissue, '_issue.txt')
soup = BeautifulSoup(Issue_search, 'html.parser')
Issue_search.close()
find_me = soup.find(class_='issue-description')
roles = find_me.find_all(class_='creator-role')

#find the description
raw_issue_decription = copy.copy(find_me)
for child in raw_issue_decription.find_all('div'):
    child.decompose()

# finding the roles and names for the comic
for r in roles:
    x = r.find('span')
    y = r.find(class_='creator')
    print(x.text + '' + y.text)


str_descr = raw_issue_decription.text
pdescr = str.split(str_descr)
fdescr = " ".join(pdescr)
print(fdescr)

#getting the thumbnail image
grab_image(soup, lz + fissue)
cleanfolder(lz)
print('done')