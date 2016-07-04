"""
VerseBot for Reddit
By Matthieu Grieger
Continued By Team VerseBot
webparser.py
Copyright (c) 2015 Matthieu Grieger (MIT License)
Portions copyright (c) 2016 Matt Arnold (MIT License)
"""

import re
import requests
from urllib.request import urlopen
from warnings import filterwarnings

from bs4 import BeautifulSoup

from translation import Translation

filterwarnings("ignore", category=DeprecationWarning)


class WebParser:
    """ WebParser class for BibleGateway parsing methods. """

    def __init__(self):
        """ Initializes translations attribute and checks if there are any new
        translations to add to the database. """

        self.translations = find_supported_translations()
        self.translations.sort(key=lambda t: len(t.abbreviation), reverse=True)


def get_web_contents(verse):
    """ Determines which web service to use based on the input
    translation, then calls the appropriate function to grab the contents
    of the verse.

    :param verse: The verse to grab the contents for
    """

    if verse.translation == "JPS":
        return get_bible_hub_verse(verse)
    else:
        return get_bible_gateway_verse(verse)


def find_supported_translations():
    """ Retrieves a list of supported translations from BibleGateway's
    translation page. """

    url = "https://www.biblegateway.com/versions/"
    translations = list()

    page = urlopen(url)
    soup = BeautifulSoup(page.read(), "html.parser")

    t_has_ot = True
    t_has_nt = True
    t_has_deut = False

    trans = soup.findAll("tr", {"class": "language-row"})
    for t in trans:
        if not t.find("a").has_attr("title"):
            t_text = t.find("td", {"class": "translation-name"}).get_text()
            t_name = t_text[:t_text.rfind("(") - 1]
            t_abbreviation = t_text[t_text.rfind("(") + 1:t_text.rfind(")")]
            t_language = t["data-language"]
            if t.find("span", {"class": "testament"}):
                section = t.find("span", {"class": "testament"}).get_text()
                if section == "OT":
                    t_has_ot = True
                    t_has_nt = False
                    t_has_deut = False
                elif section == "NT":
                    t_has_ot = False
                    t_has_nt = True
                    t_has_deut = False
                elif section == "with Apocrypha":
                    t_has_ot = True
                    t_has_nt = True
                    t_has_deut = True
            new_trans = Translation(t_name, t_abbreviation, t_language,
                                    t_has_ot, t_has_nt, t_has_deut)
            translations.append(new_trans)

    # Add local translations to supported translations list
    translations.append(Translation("JPS Tanakh", "JPS", "en",
                                    True, False, False))

    return translations


def get_bible_gateway_verse(verse):
    """ Retrieves the text for a user-supplied verse selection that
    can be found on BibleGateway.

    :param verse: The verse to grab the contents for
    """

    if verse.verse is not None:
        url = ("https://www.biblegateway.com/passage/"
               "?search=%s+%s:%s&version=%s"
               % (verse.book.replace(" ", "%20"), verse.chapter,
                  verse.verse, verse.translation))
    else:
        url = ("https://www.biblegateway.com/passage/?search=%s+%s&version=%s"
               % (verse.book.replace(" ", "%20"), verse.chapter,
                  verse.translation))

    page = urlopen(url)
    soup = BeautifulSoup(page.read(), "html.parser")

    verses = soup.findAll("span", {"class": "text"})

    if not verses:
        return None, None, None

    trans_title = soup.find("span",
                            {"class": "passage-display-version"}).get_text()
    permalink = ("https://www.biblegateway.com/passage/"
                 "?search=%s+%s&version=%s"
                 % (verse.book, verse.chapter, verse.translation))

    contents = ""
    numbers = re.compile(r"(\d+)")
    for v in verses:
        if v.find("span", {"class": "indent-1-breaks"}) is not None:
            v.find("span", {"class": "indent-1-breaks"}).decompose()
        if v.parent.name != "h3" and v.parent.name != "h4":
            if "<span class=\"chapternum\">" in str(v):
                text = v.get_text().replace(str(verse.chapter), "1") + " "
            elif v.get_text().replace(" ", "") == "Back":
                text = ""
            else:
                text = v.get_text() + " "
            text = numbers.sub(r"[**\1**]", text, 1)
        else:
            text = "\n\n>**" + v.get_text() + "**  \n"

        contents += re.sub(r"\[\w\]", "", text)

    return contents, trans_title, permalink


def get_bible_hub_verse(verse):
    """ Retrieves the text for a user-supplied verse selection that can be
    found on Bible Hub.
    :param verse: The verse to grab the contents for"""

    url = ("http://biblehub.com/%s/%s/%d.htm"
           % (verse.translation.lower(), verse.book.lower().replace(" ", "_"),
              verse.chapter))

    page = urlopen(url)
    soup = BeautifulSoup(page.read(), "html.parser")

    verses = soup.find("div", {"class": "chap"})

    if len(verses) < 1:
        return None, None, None

    for cur_verse in verses.findAll("b"):
        cur_verse.decompose()
    text = verses.get_text()

    trans_title = soup.find("div", {"class": "vheading"}).get_text()

    verse_list = text.splitlines()

    contents = ""
    for i, val in enumerate(verse_list):
        verse_num = i + 1
        if verse.start_verse == 0:
            contents += ("[**%d**] %s " % (verse_num, val))
        else:
            if (verse_num >= verse.start_verse and
                    (verse.end_verse == 0 or verse_num <= verse.end_verse)):
                contents += ("[**%d**] %s " % (verse_num, val))

    return contents, trans_title, url


def search_bible_gateway(search_terms, version='ESV'):
    url = 'https://www.biblegateway.com/quicksearch/'
    params = {'quicksearch': search_terms.replace(' ', '+'), 'version': version}

    r = requests.get(url, params=params)
    soup = BeautifulSoup(r.text, 'html.parser')
    search_results = soup.find_all('article', class_='row bible-item')

    if len(search_results) == 0:
        return None

    reference = search_results[0].div.a.string

    return str(reference)
