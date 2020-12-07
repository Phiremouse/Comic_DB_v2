import os
import copy
import urllib.request
from urllib.parse import quote
import requests
from PIL import Image
from bs4 import BeautifulSoup
# todo:
# + is there a way to write doc strings for attributes (Properties)
# + error control



class AtomicEmpire:
    """[summary]
    """
    def __init__(self):
        self.base = 'https://www.atomicempire.com'
        self.url_issue_query = '/Comic/TitleList?txt='
        self.dest_folder = 'processing\\'
        self.test_output = False
        self.keywords = ['Annual', '2nd Printing']

    def get_issue_info(self, issue_):
        self.issue = issue_
        self.fissue = self.issue.replace(' ', '_')
        self.qissue = quote(self.issue)

        self.__search_site()
        self.__search_title()
        self.__search_issue()
        self.__create_creator_list()
        self.__create_issue_description()
        self.__create_image()

    def __soup_bowl(self, url_, *Download_Info):
        if self.test_output:
            temp_soup = self.__make_soup(url_, *Download_Info)
        else:
            temp_soup = self.__make_soup(self.address)
        return temp_soup

    def __search_site(self):
        self.address = self.base + self.url_issue_query + self.qissue
        #search results assuming it matches to only one.it usually defaults to the newest one.
        #Batman: Black and White 2013 vs 2020
        self.soup_site = self.__soup_bowl(self.address, self.dest_folder, self.fissue, '_search.html')
        self.line_site = self.soup_site.find(class_='row-title', href=True).get('href')

    def __search_title(self):
        # make this a conditional statment using a class attribute called self.test_output
        self.soup_title = self.__soup_bowl(self.base + self.line_site, self.dest_folder, self.fissue, '_titles.html')
        self.line_slice = self.soup_title.find_all('div', class_='row item-row py-1')

        title = []
        for line_item in self.line_slice:
            t_soup = BeautifulSoup(str(line_item), 'html.parser')
            t_soup2 = t_soup.find_all('a', href=True)
            for line_item2 in t_soup2:
                # anchors with no text
                if line_item2.text != '\n\n':
                    # does both the issue have or not have these special issues
                    # need a function just to do this alone. there will be other types that will need to be added.
                    if (self.issue.find('Annual') == -1 and line_item2.text.find('Annual') == -1) or (self.issue.find('Annual') > -1 and line_item2.text.find('Annual') > -1):
                        if (self.issue.find('2nd Printing') == -1 and line_item2.text.find('2nd Printing') == -1) or (self.issue.find('2nd Printing') > -1 and line_item2.text.find('2nd Printing') > -1) :
                            title.append(line_item2)

        t_soup3 = BeautifulSoup(str(title[0]), 'html.parser')

        # todo: make it were it can get all the appropriate comics variations.
        self.line_title = t_soup3.find('a')['href']


    def __search_issue(self):
        self.soup_issue = self.__soup_bowl(self.base + self.line_title, self.dest_folder, self.fissue, '_issue.html')
        self.issue_card = self.soup_issue.find(class_='issue-description')
        self.roles = self.issue_card.find_all(class_='creator-role')

    def __create_image(self):
        self.__grab_image(self.soup_issue, self.dest_folder + self.fissue)

    def __create_creator_list(self):
        # finding the roles and names for the comic
        self.creators = {}

        for role in self.roles:
            c_role = role.find('span')
            c_name = role.find(class_='creator')
            self.creators[c_role.text] = c_name.text
            # print(c_role.text + '' + c_name.text)

    def __create_issue_description(self):
        #find the description
        self.issue_card_copy = copy.copy(self.issue_card)
        for child in self.issue_card_copy.find_all('div'):
            child.decompose()
        str_descr = self.issue_card_copy.text
        pdescr = str.split(str_descr)
        self.issue_description = " ".join(pdescr)
        # print(fdescr)

    def __make_soup(self, url_, *Downloand_Info):
        """
            Copying network object denoted by the url_ to a local file.
            The file is then parsed by beautifulsoup (BS).
            The BS object object is reutrned.
        Args:
            all part of *Download_Info
            url_ (string): The url that will be retrieving the information from
            issue_ (string): The formatted issue name that will be apart of the file name
            level_ (string): The ending of the file name the function is saving to.

        Returns:
            beautifulsoup: soup object ready to be filtered.
        """
        if bool(Downloand_Info):
            file_location = ''
            for value in Downloand_Info:
                file_location += value

            local_filename, headers = urllib.request.urlretrieve(url_, file_location)
            page = open(local_filename, encoding='utf8')
            soup = BeautifulSoup(page, 'html.parser')
            page.close()
        else:
            response = requests.get(url_)
            soup = BeautifulSoup(response.text, 'html.parser')

        return soup

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
        self.Issue_Thumbnail = img_name + '.jpg'
        img.save(self.Issue_Thumbnail)

    def __cleanfolder(self, filepath):
        """
            Cleans out the contents of a giving folderpath.
        Args:
            filepath (string): full folderpath
        """
        for filename in os.listdir(filepath):
            os.unlink(filepath + filename)
            # print(filename)

    def show_image(self):
        img = Image.open(self.Issue_Thumbnail)
        img.show()