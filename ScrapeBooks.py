import requests
import re
import numpy as np
import nltk
from StoreChars import DiscoveryCharDatabase
from TextPersonality import NLUPersonalityInterface
from bs4 import BeautifulSoup


class BookTextInterface:
    """Gets text from book based on a book number"""
    def get_text(self, book_no: int) -> str:
        """ Get raw text from books """
        pass

    def get_char_names(self, book_text: str) -> np.array:
        """ Get character names from book """
        pass

    def get_char_text(self, book_text, char):
        """ Get all text from book about character """
        pass

    def get_title(self, book_no: int):
        """ returns the title of a book given a certain text """
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

    def get_char_names(self,book_text):
        twos = []
        threes = []
        for sent in nltk.sent_tokenize(book_text):
            for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
                if hasattr(chunk, 'label') and chunk.label() == "PERSON":
                    if len(chunk) == 2 and chunk[0][0] != 'Mr.'and chunk[0][0] != 'Mrs.'and chunk[0][0] != 'Ms.'and chunk[0][0] != 'Dr.'and chunk[0][0] != 'Mister'and chunk[0][0] != 'Lady'and chunk[0][0] != 'Miss'and chunk[0][0] != 'Poor'and chunk[0][0] != 'Did'and chunk[0][0] != 'Captain'and chunk[0][0] != 'Colonel'and chunk[0][0] != 'Could'and chunk[0][0] != 'Mount'and chunk[0][0] != 'Madame'and chunk[0][0] != 'Doctor'and chunk[0][0] != 'Sir'and chunk[0][0] != 'Brother'and chunk[0][0] != 'Sister'and chunk[0][0] != 'Does'and chunk[0][0] != 'Part'and chunk[0][0] != 'Good'and chunk[1][0] and chunk[0][0] != 'Young' and chunk[0][0] != 'Old'!= 'Town' and chunk[1][0] != 'City' and chunk[1][0] != 'Park' and chunk[1][0] != 'Place' and chunk[0][0] != 'Street' and chunk[1][0] != 'Street' and chunk[1][0] != 'Bridge' and chunk[1][0] != 'Station' and chunk[1][0] != 'Road'and chunk[1][0] != 'Lake'and chunk[1][0] != 'Pond'and chunk[1][0] != 'Sea' and chunk[1][0] != 'Terrace'and chunk[1][0] != 'House'and chunk[1][0] != 'Lodge'and chunk[1][0] != 'Woods'and chunk[1][0] != 'Mount'and chunk[1][0] != 'Dale'and chunk[1][0] != 'Gardens'and chunk[1][0] != 'Court'and len(chunk[1][0]) > 2:
                        twos.append(chunk[0][0] + " " + chunk[1][0])
                    elif len(chunk) == 3 and chunk[0][0] != 'Did'and chunk[0][0] != 'Could'and chunk[2][0] != 'City'and len(chunk[1][0]) > 2:
                        threes.append(chunk[0][0] + " " + chunk[1][0] + " " + chunk[2][0])

        twos = np.unique(np.array(twos))
        threes = np.unique(np.array(threes))
        remove = []
        for i in range(twos.shape[0]):
            for j in range(threes.shape[0]):
                if twos[i] in threes[j]:
                    remove.append(j)

        return np.append(twos, np.delete(threes,remove))

    def get_title(self, book_no):
        url = 'http://www.gutenberg.org/files/%d/%d-h/%d-h.htm' % (book_no, book_no, book_no)
        source = requests.get(url).text
        soup = BeautifulSoup(source, 'html.parser')
        h1_tag = soup.find('h1').getText()
        title = re.sub(r'[^\w\s]', '', h1_tag)
        title = title.replace('\r', '')
        title = re.sub("\s+", ' ', title)
        return title.title()

    def get_char_text(self, book_text, char):
        pattern = '[^.]* %s [^.]*[.]' % char
        sent_list = re.findall(pattern, book_text)
        return sent_list


if __name__ == "__main__":
    # gutenburg = GutenburgBookText()
    # text = gutenburg.get_text(12)
    # gutenburg.get_char_names(text)
    # print(gutenburg.get_char_sent(text, 'Alice'))
    # pride and prejudice book - 1342, study in scarlet - 244, the odyssey - 1727
    book_num = 1727
    gutenburg = GutenburgBookText()
    nlu = NLUPersonalityInterface()
    ddb = DiscoveryCharDatabase("Collection 1")
    text = gutenburg.get_text(book_num)
    book_title = gutenburg.get_title(book_num)
    char_names = gutenburg.get_char_names(text)
    # print(char_names)
    # print(len(char_names))
    # print(gutenburg.get_char_text(text, 'Jefferson Hope'))
    for name in char_names:
        name = name.title()
        print(name)
        names = name.split(" ")
        first = names[0];
        last = names[len(names) - 1]
        sent_list = gutenburg.get_char_text(text, first)
        sent_list += gutenburg.get_char_text(text, last)
        char_sents = ''.join(sent_list)
        if char_sents:
            char_personality = nlu.get_personality(char_sents)
            full_dict = dict(char_personality[0])
            full_dict.update(char_personality[1])
            full_dict["title"] = book_title
            full_dict["sentences"] = sent_list
            # ddb.add_char(name, full_dict)
            print(full_dict)