import pytest
from TextPersonality import NLUPersonalityInterface
from ScrapeBooks import GutenburgBookText

#test case persoanlity
def test_personality_vaild1():
    nlu = NLUPersonalityInterface()
    this_dict =nlu.get_personality(
       'But the black kitten had been finished with earlier in the afternoon, and so, while Alice was sitting curled up in a corner of the great arm-chair, half talking to herself and half asleep, the kitten had been having a grand game of romps with the ball of worsted Alice had been trying to wind up, and had been rolling it up and down till it had all come undone again; and there it was, spread over the hearth-rug, all knots and tangles, with the kitten running after its own tail in the middle.')
    assert this_dict, "dict should not be null"

def test_persoanlity_vaild2():
    nlu = NLUPersonalityInterface()
    this_dict =nlu.get_personality(
       'Those summer nights seem long ago, And so is the girl you used to call. ')
    assert this_dict, "dict should not be null"

def test_length_too_short():
    with pytest.raises(Exception):
        nlu = NLUPersonalityInterface()
        assert nlu.get_personality('happy')
        # should raise an ApiException

def test_length_zero():
    with pytest.raises(Exception):
        nlu = NLUPersonalityInterface()
        assert nlu.get_personality()

#test case scrape book
def test_get_text_valid1():
    gutenburg = GutenburgBookText()
    book_num = 19
    assert gutenburg.get_text(book_num), "the book should not be null"

def test_get_text_valid2():
    gutenburg = GutenburgBookText()
    book_num = 1234
    assert gutenburg.get_text(book_num), "the book should not be null"

# def test_scrape_not_valid():
#     with pytest.raises(Exception):
#         gutenburg = GutenburgBookText()
#         book_num = -1
#         assert gutenburg.get_text(book_num)

def test_get_char_names_valid():
    gutenburg = GutenburgBookText()
    book_num = 244
    book_text = gutenburg.get_text(book_num)
    assert gutenburg.get_char_names(book_text).size != 0, "the name list should not be null"

