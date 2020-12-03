"""
POC to set the search bar to comics and type in a value.
then save the result of the search
"""
import os
import copy
import urllib.request
from urllib.parse import quote
import requests
from PIL import Image
from bs4 import BeautifulSoup

def make_soup(url_, issue_, level_,):
    """
        Copying network object denoted by the url_ to a local file.
        The file is then parsed by beautifulsoup (BS).
        The BS object object is reutrned.
    Args:
        url_ (string): The url that will be retrieving the information from
        issue_ (string): The formatted issue name that will be apart of the file name
        level_ (string): The ending of the file name the function is saving to.

    Returns:
        beautifulsoup: soup object ready to be filtered.
    """
    local_filename, headers = urllib.request.urlretrieve(url_, issue_ + level_)
    page_ = open(local_filename)
    soup_ = BeautifulSoup(page_,'html.parser')
    page_.close()
    return soup_

def grab_image(soup_, img_name):
    """
        Takes a beautifulsoup (BS) object, find the image url, and saves it locally.

    Args:
        soup_ (beautifulsoup): the soup object containing the markup where the image url is located
        img_name (string): the saving name (path) of the image.
    """
    img_add = soup_.find(class_='itemimage')
    image_url = img_add['src']
    img = Image.open(requests.get(image_url, stream=True).raw)
    img.save(img_name + '.jpg')

def cleanfolder(filepath):
    """
        Cleans out the contents of a giving folderpath.
    Args:
        filepath (string): full folderpath
    """
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
soup = make_soup(address, lz + fissue, '_search.txt')
line = soup.find(class_='row-title', href=True).get('href')

# Titles page it matches to only one
soup = make_soup(base + line, lz + fissue, '_titles.txt')
line = soup.find(class_='col item-content pl-0').find('a', href=True).get('href')

# Issue page takes the first one
soup = make_soup(base + line, lz + fissue, '_issue.txt')

find_me = soup.find(class_='issue-description')
roles = find_me.find_all(class_='creator-role')

# finding the roles and names for the comic
for r in roles:
    x = r.find('span')
    y = r.find(class_='creator')
    print(x.text + '' + y.text)

#find the description
raw_issue_decription = copy.copy(find_me)
for child in raw_issue_decription.find_all('div'):
    child.decompose()
str_descr = raw_issue_decription.text
pdescr = str.split(str_descr)
fdescr = " ".join(pdescr)
print(fdescr)

# Getting the cover image preview
grab_image(soup, lz + fissue)

#store the information somewhere

# Clean out the processing folder if no abends. if the error did occur you want to see where it failed and the extracts it was working with.
cleanfolder(lz)
print('done')

# todo: so much shit
# + should i do request cacheing ?
# + can i navigate to my prior orders?
# + can i do a title search and loop through downloading the information?
# + able to take a list of issues
# + able to rest between requests
# + look at what is in the headers of the make soup function
# + error planning
# + store the sting information
# + move or store pic somehwere
# + review nameing convention of pic based on how storage is done.
# + further refacotring and class creation
