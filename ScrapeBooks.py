import requests
import re
import numpy as np
from StoreChars import DiscoveryCharDatabase
from TextPersonality import NLUPersonalityInterface


class BookTextInterface:
    """Gets text from book based on a book number"""
    def get_text(self, book_no: int) -> str:
        """ Get raw text from books """
        pass

    def get_char_names(self, book_text: str) -> np.array:
        """ Get character names from book """
        pass

    def get_char_text(book_text, char):
        """ Get all text from book about character """
        pass


class GutenburgBookText(BookTextInterface):
    def get_text(self, book_no):
        url = "https://www.gutenberg.org/files/%d/%d-0.txt" % (book_no, book_no)
        book = requests.get(url)
        book_text = book.content.decode('utf_8')
        book_text = self.remove_gutenburg_headers(book_text)
        book_text = self.remove_gutenberg_footer(book_text)
        # with open(file_name, "w") as file1:
        #     file1.write(book_text)
        return book_text

    # code from https://shravan-kuchkula.github.io/scrape_clean_normalize_gutenberg_text/#appendix
    def remove_gutenburg_headers(self, book_text):
        book_text = book_text.replace('\r', '')
        book_text = re.sub("\s+", ' ', book_text)
        start_match = re.search(r'\*{3}\s?START.+?\*{3}', book_text)
        end_match = re.search(r'\*{3}\s?END.+?\*{3}', book_text)
        try:
            book_text = book_text[start_match.span()[1]:end_match.span()[0]]
        except AttributeError:
            print('No match found')
        return book_text

    def remove_gutenberg_footer(self, book_text):
        if book_text.find('End of the Project Gutenberg') != -1:
            book_text = book_text[:book_text.find('End of the Project Gutenberg')]
        elif book_text.find('End of Project Gutenberg') != -1:
            book_text = book_text[:book_text.find('End of Project Gutenberg')]
        return book_text

    def get_char_names(self, book_text):
        char_list = re.findall('(?<![?.!”] )[A-Z][a-z]+ [A-Z][a-z]+', book_text)
        char_list = np.array(char_list)
        return np.unique(char_list)

    def get_char_sent(self, book_text, char):
        pattern = '[^.]* %s [^.]*[.]' % char
        sent_list = re.findall(pattern, book_text)
        return sent_list

if __name__ == "__main__":
    # gutenburg = GutenburgBookText()
    # text = gutenburg.get_text(12)
    # gutenburg.get_char_names(text)
    # print(gutenburg.get_char_sent(text, 'Alice'))
    # pride and prejudice book - 1342, study in scarlet - 244
    book_num = 244
    gutenburg = GutenburgBookText()
    nlu = NLUPersonalityInterface()
    ddb = DiscoveryCharDatabase("Collection 1")
    text = gutenburg.get_text(book_num)
    char_names = gutenburg.get_char_names(text)
    # print(char_names)
    # print(len(char_names))
    # print(gutenburg.get_char_sent(text, 'Jefferson Hope'))
    for name in char_names:
        print(name)
        first, last = name.split(" ")
        sent_list = gutenburg.get_char_sent(text, first)
        sent_list += gutenburg.get_char_sent(text, last)
        char_sents = ''.join(sent_list)
        if char_sents:
            char_personality = nlu.get_personality(char_sents)
            # ddb.add_char(name, char_personality)
            print(char_personality)
