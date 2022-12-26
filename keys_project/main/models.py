from django.db import connection
from .log import *

err_logger = get_err_logger(f'{__name__}', True)


def dict_fetchall(cursor):
    """Returns all rows from a cursor as a dict"""
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

# TABLE ACCOUNTS
# id,

# TABLE BOOKS
# id, book_name, users_id,


def db_return_users_books(user_id):
    try:
        with connection.cursor() as c:
            sql = '''
                select id, name
                from books
                where users_id=%s
                ;'''
            values = (user_id,)
            c.execute(sql, values)
            res = c.fetchall()
            return ('success', res)
    except Exception as exc:
        err_logger.exception(exc)
        return ('failure', [])


def db_create_book(book_name, user_id):
    try:
        with connection.cursor() as c:
            sql = 'insert into books (name, users_id) values (%s, %s);'
            values = (book_name, user_id,)
            c.execute(sql, values)
            return ('success', [])
    except Exception as exc:
        err_logger.exception(exc)
        return ('failure', [])


def db_delete_book(book_id, user_id):
    try:
        with connection.cursor() as c:
            sql = 'delete from books where id=%s and users_id=%s;'
            values = (book_id, user_id,)
            c.execute(sql, values)
            return ('success', [])
    except Exception as exc:
        err_logger.exception(exc)
        return ('failure', [])


# TABLE TEXTS
# id, text, stats, books_id, chapter_str_long, chapter_str_short, done_bool,
