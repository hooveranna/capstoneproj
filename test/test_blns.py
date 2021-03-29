import pytest
from TextPersonality import NLUPersonalityInterface
from ScrapeBooks import GutenburgBookText
import logging

def test_blns1():
    with pytest.raises(Exception):
        nlu = NLUPersonalityInterface()
        this_dict = nlu.get_personality('False')
        assert this_dict

def test_blns1():
    with pytest.raises(Exception):
        nlu = NLUPersonalityInterface()
        this_dict = nlu.get_personality('FALSE')
        assert this_dict


# def test_blns2():
#     with pytest.raises(Exception):
#         nlu = NLUPersonalityInterface()
#         logging.basicConfig()
#         log = logging.getLogger("LOG")
#         with open('test/blns.txt', 'r') as f:
#             for line in f:
#                 if not line.startswith("#"):
#                     this_dict =nlu.get_personality(line)
#                     log.warning(line)
#                     print(line)
#                     assert this_dict