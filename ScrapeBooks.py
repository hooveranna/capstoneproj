import requests
import re
import numpy as np


class BookTextInterface:
    """Gets text from book based on a book number"""
    def get_text(self, book_no: int) -> str:
        pass


class GutenburgBookText(BookTextInterface):
    def get_text(self, book_no, file_name):
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
        book_text = book_text.replace('\n', ' ')
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

def get_char_names(book_text):
    char_list = re.findall('[A-Z][a-z]* [A-Z][a-z]*', book_text)
    char_list = np.array(char_list)
    return np.unique(char_list)


def get_char_sent(book_text, char):
    pattern = '[^.]* %s [^.]*[.]' % char
    sent_list = re.findall(pattern, book_text)
    return sent_list





if __name__ == "__main__":
    gutenburg = GutenburgBookText()
    text = gutenburg.get_gutenberg_text(12, "booktext.txt")
    get_char_names(text)
    print(get_char_sent(text, 'Alice'))

