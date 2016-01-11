"""
VerseBot for reddit
By Matthieu Grieger
tests.py
Copyright (c) 2015 Matthieu Grieger (MIT License)
"""

import logging
import os
import sys
import unittest

import books
import database
import regex
import verse
import webparser

sys.path.append(os.path.join('..', 'versebot'))


class TestBookRetrieval(unittest.TestCase):
    """ Tests book retrieval and parsing functions. """
    
    def test_book_standardization(self):
        """ Tests book conversion to standardized book names. """

        self.assertTrue(books.get_book("1 Jn") == "1 John")
        self.assertTrue(books.get_book("ti") == "Titus")
        self.assertTrue(books.get_book("thisisntabook") is None)
    
    def test_book_number_retrieval(self):
        """ Tests book number retrieval. """

        self.assertTrue(books.get_book_number("Genesis") == 1)
        self.assertTrue(books.get_book_number("Bel and the Dragon") == 82)
        self.assertTrue(books.get_book_number("thisisntabook") is None)
        
        
class TestBibleGatewayParsing(unittest.TestCase):
    """ Tests parsing of BibleGateway webpages. """
    
    def test_supported_translation_retrieval(self):
        """ Tests retrieval of supported translations. """

        parser = webparser.WebParser()
        self.assertTrue(len(parser.translations) != 0)
        
    def test_bible_gateway_text_retrieval(self):
        """ Tests the retrieval of BibleGateway verse contents. """

        parser = webparser
        database.connect(logging.getLogger("versebot"))
        v = verse.Verse("Genesis", "1", "esv", "mgrieger",
                        "VerseBot", verse="1")
        self.assertTrue("In the beginning, God created "
                        "the heavens and the earth." in
                        parser.get_bible_gateway_verse(v)[0])
        

class TestRegex(unittest.TestCase):
    """ Tests regular expressions. """
    
    def test_verse_regex(self):
        self.assertTrue(regex.find_verses(
            "Testing testing! [genesis 5:3-5 (nrsv)]") is not None)
        self.assertTrue(regex.find_verses("[genesis (nrsv)") is None)


if __name__ == "__main__":
    unittest.main()
