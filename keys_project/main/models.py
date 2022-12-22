from django.db import connection
# from datetime import date, datetime
from .log import *

# debug_logger = get_debug_logger(f'{__name__} (debug)')
# info_logger = get_info_logger(f'{__name__} (info)', print=True)
# crit_logger = get_crit_logger(f'{__name__} (crit)')
#
# debug_logger.debug(f'something')
# info_logger.info(f'something')
# crit_logger.critical(f'something')


def dict_fetchall(cursor):
    """Returns all rows from a cursor as a dict"""
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

# TABLE ACCOUNTS
# id,

# TABLE BOOKS
# id, book_name, users_id,

# TABLE TEXTS
# id, text, stats, books_id, chapter_str_long, chapter_str_short, done_bool,
