from django.db import connection
from .log import *
import json

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
            sql = 'select id, chapter, text, done, stats_args from texts where book_id=%s and user_id=%s order by id;'
            values = (book_id, user_id)
            c.execute(sql, values)
            res = dict_fetchall(c)
            return ('success', res)
    except Exception as exc:
        err_logger.exception(exc)
        return ('failure', [])


def db_batch_create_texts(book_id, user_id, chapter, texts_list):
    try:
        with connection.cursor() as c:
            for text in texts_list:
                sql = 'insert into texts (book_id, user_id, chapter, text, stats_raw, stats_args) values (%s, %s, %s, %s, %s, %s);'
                values = (book_id, user_id, chapter, text, json.dumps(''), json.dumps(''))
                c.execute(sql, values)
            return ('success', [])
    except Exception as exc:
        err_logger.exception(exc)
        return ('failure', [])

### TEXT FNs ##################################################################


def db_get_a_text_with_stats(text_id, user_id):
    try:
        with connection.cursor() as c:
            sql = 'select book_id from texts where id=%s and user_id=%s;'
            values = (text_id, user_id)
            c.execute(sql, values)
            book_id = c.fetchone()[0]

            sql = 'select id from texts where book_id=%s and user_id=%s order by id;'
            values = (book_id, user_id)
            c.execute(sql, values)
            text_ids = [row[0] for row in c.fetchall()]
            prev_text_id = None
            this_index = text_ids.index(text_id)
            next_text_id = None

            if this_index > 0:
                prev_text_id = text_ids[this_index-1]
            if this_index < len(text_ids)-1:
                next_text_id = text_ids[this_index+1]

            sql = 'select text, stats_args from texts where id=%s and user_id=%s;'
            values = (text_id, user_id)
            c.execute(sql, values)
            res = dict_fetchall(c)[0]
            return ('success', [{'text': res['text'], 'stats_args': res['stats_args'], 'prev_text_id': prev_text_id, 'next_text_id': next_text_id}])
    except Exception as exc:
        err_logger.exception(exc)
        return ('failure', [])


# def db_save_stats(text_id, user_id, stats_raw, stats_args):
#     try:
#         with connection.cursor() as c:
#             sql = 'update texts set stats_raw=%s, stats_args=%s, done=%s where id=%s and user_id=%s;'
#             values = (stats_raw, stats_args, 't', text_id, user_id)
#             c.execute(sql, values)
#             return ('success', [])
#     except Exception as exc:
#         err_logger.exception(exc)
#         return ('failure', [])


def db_save_stats_new(text_id, user_id, stats_raw, stats_args):
    try:
        with connection.cursor() as c:
            sql = 'update texts set stats_raw_str=%s, stats_args=%s, done=%s where id=%s and user_id=%s;'
            values = (stats_raw, stats_args, 't', text_id, user_id)
            c.execute(sql, values)
            return ('success', [])
    except Exception as exc:
        err_logger.exception(exc)
        return ('failure', [])


def db_del_texts_by_chapter(chapter_str, user_id):
    try:
        with connection.cursor() as c:
            sql = 'delete from texts where chapter=%s and user_id=%s;'
            values = (chapter_str, user_id)
            c.execute(sql, values)
            return ('success', [])
    except Exception as exc:
        err_logger.exception(exc)
        return ('failure', [])


def db_del_text_by_id(text_id, user_id):
    try:
        with connection.cursor() as c:
            sql = 'delete from texts where id=%s and user_id=%s;'
            values = (text_id, user_id)
            c.execute(sql, values)
            return ('success', [])
    except Exception as exc:
        err_logger.exception(exc)
        return ('failure', [])


### STATS FNs #################################################################

def db_return_all_text_stats(user_id):
    try:
        with connection.cursor() as c:
            sql = '''select stats_raw_str from texts where user_id=%s and done='t' order by id;'''
            values = (user_id,)
            c.execute(sql, values)
            res = c.fetchall()
            return ('success', res)
    except Exception as exc:
        err_logger.exception(exc)
        return ('failure', [])


### TEXT FNs ##################################################################

def db_get_options(user_id):
    try:
        with connection.cursor() as c:
            sql = 'select * from options where user_id=%s;'
            values = (user_id,)
            c.execute(sql, values)
            res = dict_fetchall(c)
            return ('success', res)
    except Exception as exc:
        err_logger.exception(exc)
        return ('failure', [])


def db_set_options(user_id, dark_mode):
    try:
        with connection.cursor() as c:
            sql = 'update options set dark_mode=%s where user_id=%s;'
            values = (dark_mode, user_id)
            c.execute(sql, values)
            return ('success', [])
    except Exception as exc:
        err_logger.exception(exc)
        return ('failure', [])


# def db_return_one_text_stats(user_id, text_id):
#     try:
#         with connection.cursor() as c:
#             sql = 'select stats_raw from texts where user_id=%s and id=%s order by id;'
#             values = (user_id, text_id)
#             c.execute(sql, values)
#             res = c.fetchall()
#             return ('success', res)
#     except Exception as exc:
#         err_logger.exception(exc)
#         return ('failure', [])
#
#
# def db_return_one_text_stats2(user_id, text_id):
#     try:
#         with connection.cursor() as c:
#             sql = 'select stats_raw_str from texts where user_id=%s and id=%s order by id;'
#             values = (user_id, text_id)
#             c.execute(sql, values)
#             res = c.fetchall()
#             return ('success', res)
#     except Exception as exc:
#         err_logger.exception(exc)
#         return ('failure', [])
#
#
# def db_return_all_text_ids():
#     try:
#         with connection.cursor() as c:
#             sql = 'select id from texts order by id;'
#             c.execute(sql)
#             res = c.fetchall()
#             return ('success', res)
#     except Exception as exc:
#         err_logger.exception(exc)
#         return ('failure', [])
