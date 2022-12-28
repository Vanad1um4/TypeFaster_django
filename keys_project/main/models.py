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
# id, book_name, user_id,


### BOOK FNs ##################################################################

def db_return_users_books(user_id):
    try:
        with connection.cursor() as c:
            sql = 'select id, name from books where user_id=%s order by id;'
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
            sql = 'insert into books (name, user_id) values (%s, %s);'
            values = (book_name, user_id,)
            c.execute(sql, values)
            return ('success', [])
    except Exception as exc:
        err_logger.exception(exc)
        return ('failure', [])


def db_rename_book(book_name, book_id, user_id):
    try:
        with connection.cursor() as c:
            sql = 'update books set name=%s where id=%s and user_id=%s;'
            values = (book_name, book_id, user_id,)
            c.execute(sql, values)
            return ('success', [])
    except Exception as exc:
        err_logger.exception(exc)
        return ('failure', [])


def db_delete_book(book_id, user_id):
    try:
        with connection.cursor() as c:
            sql = 'delete from texts where book_id=%s and user_id=%s;'
            values = (book_id, user_id,)
            c.execute(sql, values)
            sql = 'delete from books where id=%s and user_id=%s;'
            values = (book_id, user_id,)
            c.execute(sql, values)
            return ('success', [])
    except Exception as exc:
        err_logger.exception(exc)
        return ('failure', [])


### TEXT FNs ##################################################################

# TABLE TEXTS
# id, book_id, user_id, chapter_str, text, stats, done_bool

def db_get_texts(book_id, user_id):
    try:
        with connection.cursor() as c:
            sql = 'select * from texts where book_id=%s and user_id=%s order by id;'
            values = (book_id, user_id)
            c.execute(sql, values)
            res = dict_fetchall(c)
            return ('success', res)
    except Exception as exc:
        err_logger.exception(exc)
        return ('failure', [])


def db_create_text(book_id, user_id, chapter, text, stats):
    try:
        with connection.cursor() as c:
            sql = 'insert into texts (book_id, user_id, chapter, text, stats) values (%s, %s, %s, %s, %s);'
            values = (book_id, user_id, chapter, text, stats)
            c.execute(sql, values)
            return ('success', [])
    except Exception as exc:
        err_logger.exception(exc)
        return ('failure', [])


def db_batch_create_texts(book_id, user_id, chapter, texts_list):
    try:
        with connection.cursor() as c:
            for text in texts_list:
                sql = 'insert into texts (book_id, user_id, chapter, text, stats) values (%s, %s, %s, %s, %s);'
                values = (book_id, user_id, chapter, text, '')
                c.execute(sql, values)
            return ('success', [])
    except Exception as exc:
        err_logger.exception(exc)
        return ('failure', [])

### TEXT FNs ##################################################################


def db_get_a_text_with_stats(text_id, user_id):
    try:
        with connection.cursor() as c:
            sql = 'select text, stats from texts where id=%s and user_id=%s;'
            values = (text_id, user_id)
            c.execute(sql, values)
            res = dict_fetchall(c)
            return ('success', res)
    except Exception as exc:
        err_logger.exception(exc)
        return ('failure', [])


def db_save_stats(text_id, user_id, stats):
    try:
        with connection.cursor() as c:
            sql = 'update texts set stats=%s, done=%s where id=%s and user_id=%s;'
            values = (stats, 't', text_id, user_id)
            c.execute(sql, values)
            return ('success', [])
    except Exception as exc:
        err_logger.exception(exc)
        return ('failure', [])
