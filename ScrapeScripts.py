import numpy as np
import re
import spacy
import nltk
from urllib.parse import quote

from bs4 import BeautifulSoup, NavigableString
import requests


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
    def get_char_names(text: BeautifulSoup) -> np.array:
        #get initial values
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
            if bold.get_text(strip=True) == char:
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
    response = requests.get('https://imsdb.com/scripts/10-Things-I-Hate-About-You.html')
    html = response.text
    
    soup = BeautifulSoup(html, "html.parser")
    names = IMSDBScrapeScripts.get_char_names(soup)
    print(names)
    # paragraphs = soup.find_all('p')
    #
    # for p in paragraphs:
    #     relative_link = p.a['href']
    #     print(relative_link)
    #     title, script = get_script(relative_link)
    #     if not script:
    #         continue
    #
    #     with open(os.path.join(SCRIPTS_DIR, title.strip('.html') + '.txt'), 'w', encoding='utf-8') as outfile:
    #         outfile.write(script)
    test_script_info = {"relative_link": "/Movie Scripts/10 Things I Hate About You Script.html"}
    # test_text = IMSDBScrapeScripts.get_text(test_script_info)
    # print(test_text["script_soup"].get_text())
    # test_title = IMSDBScrapeScripts.get_title(test_script_info)
    # print(test_title)
    # print(IMSDBScrapeScripts.get_char_text(test_text, "BIANCA"))
