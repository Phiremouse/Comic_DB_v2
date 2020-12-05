import os
import copy
import urllib.request
from urllib.parse import quote
import requests
from PIL import Image
from bs4 import BeautifulSoup
# todo:
# + since the object is initliaized i dont need the saving of the txt file. if it errors out then yeah totes need it.
# + is there a way to write doc strings for attributes (Properties)
# + error control
# creating new branch to remove the text files for everypull


class AtomicEmpire:
    def __init__(self):
        self.base = 'https://www.atomicempire.com'
        self.url_issue_query = '/Comic/TitleList?txt='
        self.dest_folder = 'processing\\'

    def get_issue_info(self, issue_):
        self.issue = issue_
        self.fissue = self.issue.replace(' ', '_')
        self.qissue = quote(self.issue)

        self.__search_site()
        self.__search_title()
        self.__search_issue()

    def __search_site(self):
        self.address = self.base + self.url_issue_query + self.qissue
        #search results assuming it matches to only one
        self.soup_site = self.__make_soup(self.address, self.dest_folder + self.fissue, '_search.txt')
        self.line_site = self.soup_site.find(class_='row-title', href=True).get('href')

    def __search_title(self):
        self.soup_title = self.__make_soup(self.base + self.line_site, self.dest_folder + self.fissue, '_titles.txt')
        self.line_title = self.soup_title.find(class_='col item-content pl-0').find('a', href=True).get('href')

    def __search_issue(self):
        self.soup_issue = self.__make_soup(self.base + self.line_title, self.dest_folder + self.fissue, '_issue.txt')
        self.issue_card = self.soup_issue.find(class_='issue-description')
        self.roles = self.issue_card.find_all(class_='creator-role')

    def create_image(self):
        self.__grab_image(self.soup_issue, self.dest_folder + self.fissue)

    def create_creator_list(self):
        # finding the roles and names for the comic
        self.creators = {}

        for role in self.roles:
            c_role = role.find('span')
            c_name = role.find(class_='creator')
            self.creators[c_role.text] = c_name.text
            print(c_role.text + '' + c_name.text)

    def create_issue_description(self):
        #find the description
        self.issue_card_copy = copy.copy(self.issue_card)
        for child in self.issue_card_copy.find_all('div'):
            child.decompose()
        str_descr = self.issue_card_copy.text
        pdescr = str.split(str_descr)
        self.issue_description = " ".join(pdescr)
        # print(fdescr)

    def __make_soup(self, url_, issue_, level_,):
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
        soup_ = BeautifulSoup(page_, 'html.parser')
        page_.close()
        return soup_

    def __grab_image(self, soup_, img_name):
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

    def __cleanfolder(self, filepath):
        """
            Cleans out the contents of a giving folderpath.
        Args:
            filepath (string): full folderpath
        """
        for filename in os.listdir(filepath):
            os.unlink(filepath + filename)
            # print(filename)
