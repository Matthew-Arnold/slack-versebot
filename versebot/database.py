"""
VerseBot for reddit
By Matthieu Grieger
database.py
Copyright (c) 2015 Matthieu Grieger (MIT License)
"""

from regex import find_already_quoted_verses
import sqlite3
from config import DATABASE_PATH

_conn = None
cur = None


def connect(logger):
    """ Connect to SQLite database. """

    global _conn
    global cur
    try:
        _conn = sqlite3.connect(DATABASE_PATH)
        cur = _conn.cursor()
    except sqlite3.Error:
        logger.critical("Connection to database failed. Exiting...")
        exit(1)


def update_book_stats(new_books, is_edit_or_delete=False):
    """ Updates book_stats table with recently quoted books.
    Alternatively, this function is also used to remove book counts
    that were added by a comment that has been edited/deleted. """

    for book in new_books.items():
        if is_edit_or_delete:
            cur.execute("UPDATE book_stats SET t_count = t_count - %d WHERE book = '%s'" % (book[1], book[0]))
        else:
            cur.execute("UPDATE book_stats SET t_count = t_count + %d WHERE book = '%s'" % (book[1], book[0]))
    _conn.commit()


def update_subreddit_stats(new_subreddits, is_edit_or_delete=False):
    """ Updates subreddit_stats table with subreddits that have recently used VerseBot.
    Alternatively, this function is also used to remove subreddit counts that were
    added by a comment that has been edited/deleted. """

    for subreddit in new_subreddits.items():
        if is_edit_or_delete:
            cur.execute("UPDATE subreddit_stats SET t_count = t_count - %(num)s WHERE sub = '%(subreddit)s';"
                        % {"subreddit": subreddit[0], "num": subreddit[1]})
            cur.execute("DELETE FROM subreddit_stats WHERE t_count = 0;"
                        % {"subreddit": subreddit[0], "num": subreddit[1]})
        else:
            # I opted for this instead of upsert because it seemed simpler.
            cur.execute("UPDATE subreddit_stats SET t_count = t_count + %(num)s WHERE sub = '%(subreddit)s';"
                        % {"subreddit": subreddit[0], "num": subreddit[1]})
            cur.execute("INSERT INTO subreddit_stats (sub, t_count) SELECT '%(subreddit)s', %(num)s WHERE NOT EXISTS"
                        "(SELECT 1 FROM subreddit_stats WHERE sub = '%(subreddit)s');"
                        % {"subreddit": subreddit[0], "num": subreddit[1]})
    _conn.commit()


def update_translation_stats(translations, is_edit_or_delete=False):
    """ Updates translation_stats table with recently used translations. Alternatively,
    this function is also used to remove translation counts that were added by a comment that has been
    edited/deleted. """

    for translation in translations.items():
        trans = translation[0]
        count = translation[1]
        if is_edit_or_delete:
            cur.execute("UPDATE translation_stats SET t_count = t_count - %d WHERE trans = '%s'" % (count, trans))
        else:
            cur.execute("UPDATE translation_stats SET t_count = t_count + %d WHERE trans = '%s'" % (count, trans))
    _conn.commit()


def prepare_translation_list_update():
    """ Prepares the translation_stats table for a translation list update. The timestamp update trigger must be dropped
    so as to not mess up the actual timestamps. For all translations, available is set to false. The translations that
    are currently available will later be set to true. """

    cur.execute("UPDATE translation_stats SET available = 0;")
    _conn.commit()


def update_translation_list(translations):
    """ Updates translation_stats table with new translations that have been added. This query will also reset the
    available column for ALL translations to false, and then reset them to true individually if the translation exists
    in the local list of translations. This prevents users from trying to use translations within the database that are
    not officially supported anymore. """

    prepare_translation_list_update()
    for translation in translations:
        cur.execute(
            "UPDATE translation_stats SET available = 1 WHERE trans = '%s';" % translation.abbreviation)
        cur.execute(
            "INSERT INTO translation_stats (trans, name, lang, has_ot, has_nt, has_deut, available)"
            "SELECT '%(tran)s', '%(tname)s', '%(language)s', %(ot)s, %(nt)s, %(deut)s,"
            "1 WHERE NOT EXISTS (SELECT 1 FROM translation_stats WHERE trans = '%(tran)s');"
            % {"tran": translation.abbreviation, "tname": translation.name.replace("'", "''"),
               "language": translation.language, "ot": int(translation.has_ot),
               "nt": int(translation.has_nt), "deut": int(translation.has_deut)})
    _conn.commit()


def update_user_translation(username, ot_trans, nt_trans, deut_trans):
    """ Updates user_translation table with new custom default translations specified by the user. """

    cur.execute(
        "UPDATE user_translations"
        "SET ot_default = '%(ot)s', nt_default = '%(nt)s', deut_default = '%(deut)s', last_used = datetime('now')"
        "WHERE username = '%(name)s';"
        % {"name": username, "ot": ot_trans, "nt": nt_trans, "deut": deut_trans})
    cur.execute(
        "INSERT INTO user_translations (username, ot_default, nt_default, deut_default)"
        "SELECT '%(name)s', '%(ot)s', '%(nt)s', '%(deut)s'"
        "WHERE NOT EXISTS (SELECT 1 FROM user_translations WHERE username = '%(name)s');"
        % {"name": username, "ot": ot_trans, "nt": nt_trans, "deut": deut_trans})
    _conn.commit()


def get_user_translation(username, bible_section):
    """ Retrieves the default translation for the user in a certain section of the Bible. """

    if bible_section == "Old Testament":
        section = "ot_default"
    elif bible_section == "New Testament":
        section = "nt_default"
    else:
        section = "deut_default"
    cur.execute("SELECT %s FROM user_translations WHERE username = '%s';" % (section, str(username)))
    try:
        translation = cur.fetchone()[0]
    except TypeError:
        translation = None
    cur.execute("UPDATE user_translations SET last_used = datetime('now') WHERE username = '%s'" % str(username))
    _conn.commit()
    return translation


def clean_user_translations():
    """ Removes user translation entries that haven't been used for 90 days or more to save on database space. """

    cur.execute("DELETE FROM user_translations WHERE last_used < datetime('now', '-90 days');")
    _conn.commit()


def update_subreddit_translation(subreddit, ot_trans, nt_trans, deut_trans):
    """ Updates subreddit_translation table with new custom default translations specified by a
    moderator of a subreddit. """

    cur.execute(
        "UPDATE subreddit_translations"
        "SET ot_default = '%(ot)s', nt_default = '%(nt)s', deut_default = '%(deut)s', created = datetime('now')'"
        "WHERE sub = '%(subreddit)s';"
        % {"subreddit": subreddit.lower(), "ot": ot_trans, "nt": nt_trans, "deut": deut_trans})
    cur.execute(
        "INSERT INTO subreddit_translations (sub, ot_default, nt_default, deut_default)"
        "SELECT '%(subreddit)s', '%(ot)s', '%(nt)s', '%(deut)s'"
        "WHERE NOT EXISTS (SELECT 1 FROM subreddit_translations WHERE sub = '%(subreddit)s');"
        % {"subreddit": subreddit.lower(), "ot": ot_trans, "nt": nt_trans, "deut": deut_trans})
    _conn.commit()


def get_subreddit_translation(subreddit, bible_section):
    """ Retrieves the default translation for the subreddit in a certain section of the Bible. """

    if bible_section == "Old Testament":
        section = "ot_default"
    elif bible_section == "New Testament":
        section = "nt_default"
    else:
        section = "deut_default"
    cur.execute("SELECT %s FROM subreddit_translations WHERE sub = '%s';" % (section, subreddit.lower()))
    try:
        trans = cur.fetchone()[0]
        return trans
    except TypeError:
        return None


def is_valid_translation(translation, testament):
    """ Checks the translations table for the supplied translation, and determines whether it is valid
    for the book that the user wants to quote. If the translation is not valid (either it is not available,
    or it doesn't contain the book), the translation will either default to the subreddit default
    or the global default. """

    if testament == "Old Testament":
        testament = "has_ot"
    elif testament == "New Testament":
        testament = "has_nt"
    else:
        testament = "has_deut"
    cur.execute("SELECT %s, available FROM translation_stats WHERE trans = '%s';" % (testament, translation))
    try:
        in_testament, is_available = cur.fetchone()
        if in_testament and is_available:
            return True
        else:
            return False
    except sqlite3.Error:
        return False


def increment_comment_count():
    """ Increments the comment count entry whenever a new comment has been made. """

    cur.execute("UPDATE comment_count SET t_count = t_count + 1;")
    _conn.commit()


def decrement_comment_count():
    """ Decrements the comment count entry whenever a comment is deleted. """

    cur.execute("UPDATE comment_count SET t_count = t_count - 1;")
    _conn.commit()


def update_db_stats(verse_list):
    """ Iterates through all verses in verse_list and adds them to dicts
    to pass to the database update functions. """

    books = dict()
    translations = dict()
    subreddits = dict()

    for verse in verse_list:
        book = verse.book
        translation = verse.translation
        subreddit = verse.subreddit

        if book in books:
            books[book] += 1
        else:
            books[book] = 1

        if translation in translations:
            translations[translation] += 1
        else:
            translations[translation] = 1

        if subreddit in subreddits:
            subreddits[subreddit] += 1
        else:
            subreddits[subreddit] = 1

    update_book_stats(books)
    update_translation_stats(translations)
    update_subreddit_stats(subreddits)


def remove_invalid_statistics(message, subreddit):
    """ Performs necessary database operations to fix invalid statistics after a user has requested a comment
    to be edited or deleted. """

    invalid_verses = find_already_quoted_verses(message)
    invalid_books = dict()
    invalid_trans = dict()
    invalid_sub = dict()

    for verse in invalid_verses:
        book = verse[0].rstrip()
        translation = verse[1]
        if book in invalid_books:
            invalid_books[book] += 1
        else:
            invalid_books[book] = 1

        if translation in invalid_trans:
            invalid_trans[translation] += 1
        else:
            invalid_trans[translation] = 1

        if subreddit in invalid_sub:
            invalid_sub[subreddit] += 1
        else:
            invalid_sub[subreddit] = 1

    update_book_stats(invalid_books, is_edit_or_delete=True)
    update_translation_stats(invalid_trans, is_edit_or_delete=True)
    update_subreddit_stats(invalid_sub, is_edit_or_delete=True)
