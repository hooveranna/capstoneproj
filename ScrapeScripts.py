import sys

import numpy as np
import re
import nltk
from urllib.parse import quote

from bs4 import BeautifulSoup, NavigableString
import requests
from ibm_cloud_sdk_core import ApiException

from StoreChars import DiscoveryCharDatabase
from TextPersonality import NLUPersonalityInterface


class ScrapeScriptsInterface:
    @staticmethod
    def get_text(script_info: dict) -> dict:
        """ Get raw text from books """
        pass

    @staticmethod
    def get_char_names(script_info: dict) -> np.array:
        """ Get character names from book """
        pass

    @staticmethod
    def get_char_text(script_info: dict, char: str):
        """ Get all text from book about character """
        pass

    @staticmethod
    def get_title(script_info: dict) -> str:
        """ returns the title of a book given a certain text """
        pass


class IMSDBScrapeScripts(ScrapeScriptsInterface):
    BASE_URL = 'http://www.imsdb.com'
    SCRIPTS_DIR = 'scripts'

    @staticmethod
    def get_text(script_info: dict) -> dict:
        relative_link = script_info["relative_link"]
        tail = relative_link.split('/')[-1]
        print('fetching %s' % tail)
        script_front_url = IMSDBScrapeScripts.BASE_URL + quote(relative_link)
        front_page_response = requests.get(script_front_url)
        front_soup = BeautifulSoup(front_page_response.text, "html.parser")

        try:
            script_link = front_soup.find_all('p', align="center")[0].a['href']
        except IndexError:
            print('%s has no script :(' % tail)
            return None

        if script_link.endswith('.html'):
            title = script_link.split('/')[-1].split(' Script')[0]
            script_url = IMSDBScrapeScripts.BASE_URL + script_link
            script_soup = BeautifulSoup(requests.get(script_url).text, "html.parser")
            script_text = script_soup.find_all('td', {'class': "scrtext"})[0]  #.get_text()
            script_text = IMSDBScrapeScripts.clean_script(script_text)
            return {"script_soup": script_text}
        else:
            print('%s is a pdf :(' % tail)
            return None

    @staticmethod
    def get_char_names(script_info: dict) -> np.array:
        #get initial values
        text = script_info["script_soup"]
        bolds = text.find_all('b')
        char = []
        remove = []

        #append likely names to char
        for bold in bolds:
            string = re.sub(r'\r\n', '', bold.text)
            string = re.sub(r'\s+', ' ', string)
            string = re.sub('[0-9]', '', string)
            string = string.strip()
            if string != ' ' and string != '' and string != 'Writers' and string != 'Genres' and not '.' in string and not '?' in string and not '(' in string and not ')' in string and not '#' in string and not '-' in string and not ':' in string and not '/' in string and not '!' in string:
                strArray = string.split()
                if len(strArray) < 3:
                    char.append(string)

        #Remove duplicates
        char_names = np.unique(char)
        for i in range(char_names.shape[0]):
            for j in range(i+1,char_names.shape[0]):
                if char_names[i] in char_names[j]:
                    remove.append(j)
        char_names = np.delete(char_names, remove)

        #nltk labeling (not working)
        #for name in char_names:
        #    for chunk in nltk.chunk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(name))):
        #        if hasattr(chunk,'label'):
        #            print(chunk[0][0], chunk.label())

        return char_names

    @staticmethod
    def get_char_text(script_info: dict, char: str):
        text = script_info["script_soup"]
        bolds = text.find_all('b')
        char_text = []
        for bold in bolds:
            if char == bold.get_text(strip=True):
                char_str = bold.next_sibling
                if isinstance(char_str, NavigableString):
                    char_str = char_str.strip()
                    char_str = re.sub(r'\r\n', '', char_str)
                    char_str = re.sub(r'\s+', ' ', char_str)
                    char_text.append(char_str)

        return char_text

    @staticmethod
    def get_title(script_info: dict):
        relative_link = script_info["relative_link"]
        tail = relative_link.split('/')[-1]

        return tail.replace(" Script.html", "")

    @staticmethod
    def clean_script(script_text):
        # remove empty tags from soup obj
        for x in script_text.find_all():
            # fetching text from tag and remove whitespaces
            if len(x.get_text(strip=True)) == 0:
                # Remove empty tag
                x.extract()

        tables = script_text.find_all('table')
        for table in tables:
            table.extract()
        scripts = script_text.find_all('script')
        for script in scripts:
            script.extract()
        divs = script_text.find_all('div')
        for div in divs:
            div.extract()
        return script_text
    #     text = text.replace('Back to IMSDb', '')
    #     text = text.replace('''<b><!--
    # </b>if (window!= top)
    # top.location.href=location.href
    # <b>// -->
    # </b>
    # ''', '')
    #     text = text.replace('''          Scanned by http://freemoviescripts.com
    #           Formatting by http://simplyscripts.home.att.net
    # ''', '')
    #     return text.replace(r'\r', '')


if __name__ == "__main__":
    ddb = DiscoveryCharDatabase("Collection 2")
    nlu = NLUPersonalityInterface()
    # print(ddb.reset_db("Collection 2"))
    # response = requests.get('https://imsdb.com/all-scripts.html')
    # html = response.text
    #
    # soup = BeautifulSoup(html, "html.parser")
    # paragraphs = soup.find_all('p')

    scrape_scripts = {"/Movie%20Scripts/Twilight%20Script.html", "/Movie%20Scripts/Toy%20Story%20Script.html", "/Movie%20Scripts/Princess%20Bride,%20The%20Script.html", "/Movie%20Scripts/Psycho%20Script.html", "/Movie%20Scripts/Coraline%20Script.html", "/Movie%20Scripts/Addams%20Family,%20The%20Script.html", "/Movie%20Scripts/Taxi%20Driver%20Script.html", "/Movie%20Scripts/Wolf%20of%20Wall%20Street,%20The%20Script.html", "/Movie%20Scripts/Saw%20Script.html", "/Movie%20Scripts/Mission%20Impossible%20Script.html", "/Movie%20Scripts/Pirates%20of%20the%20Caribbean%20Script.html", "/Movie%20Scripts/Life%20of%20Pi%20Script.html", "/Movie%20Scripts/Ocean's%20Eleven%20Script.html", "/Movie%20Scripts/Despicable%20Me%202%20Script.html", "/Movie%20Scripts/Terminator%20Script.html", "/Movie%20Scripts/Zootopia%20Script.html", "/Movie%20Scripts/Shrek%20Script.html", "/Movie%20Scripts/How%20to%20Train%20Your%20Dragon%20Script.html", "/Movie%20Scripts/Coco%20Script.html", "/Movie%20Scripts/Happy%20Feet%20Script.html", "/Movie%20Scripts/Kung%20Fu%20Panda%20Script.html", "/Movie%20Scripts/Frozen%20(Disney)%20Script.html", "/Movie%20Scripts/Blade%20Runner%20Script.html", "/Movie%20Scripts/Lord%20of%20the%20Rings:%20Fellowship%20of%20the%20Ring,%20The%20Script.html", "/Movie%20Scripts/X-Men%20Origins:%20Wolverine%20Script.html", "/Movie%20Scripts/Wonder%20Woman%20Script.html", "/Movie%20Scripts/Thor%20Script.html", "/Movie%20Scripts/Citizen%20Kane%20Script.html", "/Movie%20Scripts/Titanic%20Script", "/Movie%20Scripts/La%20La%20Land%20Script.html", "/Movie%20Scripts/Jurassic%20Park%20Script.html", "/Movie%20Scripts/Star%20Wars:%20A%20New%20Hope%20Script.html", "/Movie%20Scripts/Legally%20Blonde%20Script.html", "/Movie%20Scripts/Star%20Trek%20Script.html", "/Movie%20Scripts/Spider-Man%20Script.html", "/Movie%20Scripts/Black%20Panther%20Script.html", "/Movie%20Scripts/Avengers,%20The%20(2012)%20Script.html", "/Movie%20Scripts/Avatar%20Script.html", "/Movie%20Scripts/Interstellar%20Script.html", "/Movie%20Scripts/Men%20in%20Black%203%20Script.html", "/Movie%20Scripts/Dark%20Knight%20Rises,%20The%20Script.html", "/Movie%20Scripts/American%20Psycho%20Script.html", "/Movie%20Scripts/V%20for%20Vendetta%20Script.html", }

    # for p in paragraphs:
    with open('all_chars.txt', 'w') as fp:
        for script in scrape_scripts:
            # relative_link = p.a['href']
            relative_link = script.replace("%20", " ")
            # print(relative_link)
            # title, script = get_script(relative_link)
            test_script_info = {"relative_link": relative_link}
            test_text = IMSDBScrapeScripts.get_text(test_script_info)
            if not test_text:
                continue
            # print(test_text["script_soup"].get_text())
            test_title = IMSDBScrapeScripts.get_title(test_script_info)
            # print(test_title)
            test_names = IMSDBScrapeScripts.get_char_names(test_text)
            for name in test_names:
                test_char_text = IMSDBScrapeScripts.get_char_text(test_text, name)
                # print(test_char_text)
                if len(test_char_text) > 10:
                    char_sents = ''.join(test_char_text)
                    if char_sents:
                        print(name)
                        # fp.write(name +" from " + test_title + "\n")
                        try:
                            char_personality = nlu.get_personality(char_sents)
                            full_dict = dict(char_personality[0])
                            full_dict.update(char_personality[1])
                            full_dict["title"] = test_title
                            full_dict["sentences"] = test_char_text
                            full_dict["char_name"] = name
                            print(full_dict)
                            # ddb.add_char(name, full_dict)
                        except ApiException:
                            print("IBM Api Exception:", sys.exc_info()[1])

    #
    #     with open(os.path.join(SCRIPTS_DIR, title.strip('.html') + '.txt'), 'w', encoding='utf-8') as outfile:
    #         outfile.write(script)
    # test_script_info = {"relative_link": "/Movie Scripts/Frozen (Disney) Script.html"}
    # test_text = IMSDBScrapeScripts.get_text(test_script_info)
    # print(test_text["script_soup"].get_text())
    # test_title = IMSDBScrapeScripts.get_title(test_script_info)
    # print(test_title)
    # print(IMSDBScrapeScripts.get_char_text(test_text, "ANNA"))
