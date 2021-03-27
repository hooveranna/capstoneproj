import numpy as np
import os
from urllib.parse import quote

from bs4 import BeautifulSoup
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
    def get_char_names(script_info: dict) -> np.array:
        pass

    @staticmethod
    def get_char_text(script_info: dict, char: str):
        text = script_info["script_soup"]
        print(text)

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
    # response = requests.get('https://imsdb.com/all-scripts.html')
    # html = response.text
    #
    # soup = BeautifulSoup(html, "html.parser")
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
    test_text = IMSDBScrapeScripts.get_text(test_script_info)
    # print(IMSDBScrapeScripts.clean_script(test_text["script_soup"].get_text()))
    # test_title = IMSDBScrapeScripts.get_title(test_script_info)
    # print(test_title)
    IMSDBScrapeScripts.get_char_text(test_text, "JANE")
