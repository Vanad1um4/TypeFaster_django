from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import *
from .log import *
import json
import time
import sys


def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'main/index.html')


def my_library(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user_id = request.user.account.id
    result = db_return_users_books(user_id)[1]

    options_dict = get_options(user_id)
    return render(request, 'main/my_library.html', {'data': result, 'options': options_dict})


def type_no_txt(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user_id = request.user.account.id
    options_dict = get_options(user_id)
    return render(request, 'main/type_no_txt.html', {'options': options_dict})


### BOOK FNs ##################################################################

def add_book_ajax(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user_id = request.user.account.id
    data = json.loads(request.body)
    # print(user_id, data)
    result = db_create_book(data['book_name'], user_id)
    if result[0] == 'success':
        return HttpResponse(json.dumps({'result': 'success'}),  # pyright: ignore
                            content_type='application/json; charset=utf-8')
    else:
        return HttpResponse(json.dumps({'result': 'failure'}),  # pyright: ignore
                            content_type='application/json; charset=utf-8')


def rename_book_ajax(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user_id = request.user.account.id
    data = json.loads(request.body)
    # print(user_id, data)
    result = db_rename_book(data['book_name'], data['book_id'], user_id)
    if result[0] == 'success':
        return HttpResponse(json.dumps({'result': 'success'}),  # pyright: ignore
                            content_type='application/json; charset=utf-8')
    else:
        return HttpResponse(json.dumps({'result': 'failure'}),  # pyright: ignore
                            content_type='application/json; charset=utf-8')


def delete_book_ajax(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user_id = request.user.account.id
    data = json.loads(request.body)
    result = db_delete_book(data['book_id'], user_id)
    if result[0] == 'success':
        return HttpResponse(json.dumps({'result': 'success'}),  # pyright: ignore
                            content_type='application/json; charset=utf-8')
    else:
        return HttpResponse(json.dumps({'result': 'failure'}),  # pyright: ignore
                            content_type='application/json; charset=utf-8')

### BOOK FNs ##################################################################


def get_texts_ajax(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user_id = request.user.account.id
    data = json.loads(request.body)
    result = db_get_texts(data['book_id'], user_id)
    texts = []
    chapter = ''
    k = -1
    for row in result[1]:
        # print(row)
        if row['chapter'] != chapter:
            k += 1
            chapter = row['chapter']
            texts.append({chapter: []})
        text = row['text']
        if len(text) > 35:
            text = text[:35] + '...'
        stats_args = json.loads(row['stats_args'])
        # print(stats_args)
        cpm = 0
        wpm = 0
        acc = 0.00
        chars = 0
        words = 0
        time = 0
        errors = 0

        if stats_args:
            cpm = stats_args['cpm']
            wpm = stats_args['wpm']
            acc = stats_args['acc']
            chars = stats_args['chars']
            words = stats_args['words']
            time = stats_args['time']
            errors = stats_args['errors']
        texts[k][chapter].append({'text_id': row['id'], 'text_preview': text, 'done': row['done'],
                                  'cpm': cpm, 'wpm': wpm, 'acc': acc, 'chars': chars, 'words': words, 'time': time, 'errors': errors})

    if result[0] == 'success':
        return HttpResponse(json.dumps({'result': 'success', 'data': {'texts': texts}}),  # pyright: ignore
                            content_type='application/json; charset=utf-8')
    else:
        return HttpResponse(json.dumps({'result': 'failure'}),  # pyright: ignore
                            content_type='application/json; charset=utf-8')


def add_text_ajax(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user_id = request.user.account.id
    data = json.loads(request.body)

    text = data['text']
    while '\n\n' in text:
        text = text.replace('\n\n', '\n')
    while '  ' in text:
        text = text.replace('  ', ' ')
    while '…' in text:
        text = text.replace('…', '...')

    texts_list = []
    while text:
        line_break_pos = text.find('\n', 1000)
        if line_break_pos != -1:
            texts_list.append(text[:line_break_pos])
            text = text[line_break_pos+1:]
        if line_break_pos == -1:
            texts_list.append(text)
            text = ''
    result = db_batch_create_texts(data['book_id'], user_id, data['chapter'], texts_list)
    if result[0] == 'success':
        return HttpResponse(json.dumps({'result': 'success'}),  # pyright: ignore
                            content_type='application/json; charset=utf-8')
    else:
        return HttpResponse(json.dumps({'result': 'failure'}),  # pyright: ignore
                            content_type='application/json; charset=utf-8')


def delete_texts_by_chapter_ajax(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user_id = request.user.account.id
    data = json.loads(request.body)
    # print(data)
    result = db_del_texts_by_chapter(data['chapter_name'], user_id)
    if result[0] == 'success':
        # if True:
        return HttpResponse(json.dumps({'result': 'success'}),  # pyright: ignore
                            content_type='application/json; charset=utf-8')
    else:
        return HttpResponse(json.dumps({'result': 'failure'}),  # pyright: ignore
                            content_type='application/json; charset=utf-8')


def delete_text_by_id_ajax(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user_id = request.user.account.id
    data = json.loads(request.body)
    # print(data)
    result = db_del_text_by_id(data['text_id'], user_id)
    if result[0] == 'success':
        return HttpResponse(json.dumps({'result': 'success'}),  # pyright: ignore
                            content_type='application/json; charset=utf-8')
    else:
        return HttpResponse(json.dumps({'result': 'failure'}),  # pyright: ignore
                            content_type='application/json; charset=utf-8')


### TYPE FNs ##################################################################

def type_text(request, text_id):
    if not request.user.is_authenticated:
        return redirect('login')
    user_id = request.user.account.id

    complete = False
    cpm = 0
    wpm = 0
    acc = 0.00
    chars = 0
    words = 0
    errors = 0
    time = 0
    text = ''
    prev = 0
    next = 0

    result = db_get_a_text_with_stats(text_id, user_id)
    # print(result)

    if result[0] == 'success':
        text = result[1][0]['text']
        stats = json.loads(result[1][0]['stats_args'])
        prev = result[1][0]['prev_text_id']
        next = result[1][0]['next_text_id']
        # print(stats)
        # print(bool(stats))
        # try:
        if stats:
            complete = True
            cpm = stats['cpm']
            wpm = stats['wpm']
            acc = stats['acc']
            chars = stats['chars']
            words = stats['words']
            errors = stats['errors']
            time = stats['time']
        # except:
        #     pass

    options_dict = get_options(user_id)
    return render(request, 'main/type.html', {'data': {
        'complete': complete,
        'cpm': cpm,
        'wpm': wpm,
        'acc': acc,
        'chars': chars,
        'words': words,
        'errors': errors,
        'time': time,
        'text': text,
        'id': text_id,
        'prev': prev,
        'next': next,
    }, 'options': options_dict})


def return_stats_ajax(request, text_id):
    if not request.user.is_authenticated:
        return redirect('login')
    user_id = request.user.account.id
    stats = json.loads(request.body)
    # stats = json.dumps(json.loads(request.body))
    # print(stats['stats'], stats['args'])
    # result_old = db_save_stats(text_id, user_id, json.dumps(stats['stats']), json.dumps(stats['args']))

    first_time = stats['stats']['0']['time']
    result_list = []
    for i, letter in enumerate(stats['stats']):
        if i > 0:
            result_list.append([stats['stats'][letter]['txt'],
                                stats['stats'][letter]['time']-first_time,
                                stats['stats'][letter]['error']])
        else:
            result_list.append([stats['stats'][letter]['txt'],
                                first_time,
                                stats['stats'][letter]['error']])

    result_new = db_save_stats_new(text_id, user_id, json.dumps(result_list), json.dumps(stats['args']))

    if result_new[0] == 'success':
        # if True:
        return HttpResponse(json.dumps({'result': 'success'}),  # pyright: ignore
                            content_type='application/json; charset=utf-8')
    else:
        return HttpResponse(json.dumps({'result': 'failure'}),  # pyright: ignore
                            content_type='application/json; charset=utf-8')


### STATS FNs #################################################################

def my_stats(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user_id = request.user.account.id
    result = db_return_all_text_stats(user_id)[1]
    letters_dict = {}
    words_dict = {}
    words_sum = 0
    bl = '.,!?"«»“”…'
    for text_str in result:
        text_list = json.loads(text_str[0])
        word = ''
        word_errors = 0
        for letter in text_list:
            # print(letter)
            if letter[0].lower() in letters_dict.keys() and letter[0] != ' ':
                letters_dict[letter[0].lower()]['amt'] += 1
                if letter[2] > 0:
                    letters_dict[letter[0].lower()]['err'] += 1
            elif letter[0] != ' ':
                letters_dict[letter[0].lower()] = {}
                letters_dict[letter[0].lower()]['amt'] = 1
                letters_dict[letter[0].lower()]['err'] = 0

            if letter[0] == ' ' or letter[0] == '⏎':
                if word in words_dict.keys():
                    words_dict[word]['amt'] += 1
                    if word_errors > 0:
                        words_dict[word]['err'] += 1
                    words_sum += 1
                else:
                    words_dict[word] = {}
                    words_dict[word]['amt'] = 1
                    words_dict[word]['err'] = 0
                word = ''
                word_errors = 0
            elif letter[0] in bl:
                pass
            else:
                word += letter[0].lower()
                if letter[2] > 0:
                    word_errors += 1

    # print(letters_dict)
    # for i, k in letters_dict.items():
    #     print(i, k)
    # data_sorted = sorted(letters_dict.items(), key=lambda x: x[1]['amt'], reverse=True)
    # print(data_sorted)

    # print(words_dict)
    words_sorted = sorted(words_dict.items(), key=lambda x: x[1]['amt'], reverse=True)
    # print(words_sorted)
    words_with_error_rate = {}
    limit = words_sum / 2000
    for i in words_sorted:
        if i[1]['amt'] > limit:
            i[1]['error_rate'] = round(i[1]['err'] / i[1]['amt'] * 1000) / 10
            # print(i)
            # words_with_error_rate[i[0]] = {}
            words_with_error_rate[i[0]] = i[1]
    # print(words_sum)

    words_with_error_rate_sorted = sorted(words_with_error_rate.items(), key=lambda x: x[1]['error_rate'], reverse=True)

    for i in words_with_error_rate_sorted:
        print(i)

    # letters_dict = {'l': {'amt': 11179, 'err': 604}, 'o': {'amt': 18931, 'err': 2178}, 'n': {'amt': 16652, 'err': 1138}, 'p': {'amt': 4563, 'err': 334}, 'e': {'amt': 30679, 'err': 1930}, 'h': {'amt': 15607, 'err': 1054}, 't': {'amt': 22775, 'err': 1637}, 'x': {'amt': 440, 'err': 41}, 's': {'amt': 15319, 'err': 1186}, 'c': {'amt': 6388, 'err': 564}, 'u': {'amt': 6788, 'err': 654}, 'i': {'amt': 17023, 'err': 1735}, 'a': {'amt': 20091, 'err': 1581}, 'd': {'amt': 11908, 'err': 958}, 'b': {'amt': 3577, 'err': 464}, 'k': {'amt': 3170, 'err': 515}, 'g': {'amt': 5516, 'err': 601}, 'y': {'amt': 4263, 'err': 347}, ',': {'amt': 3413, 'err': 515}, 'j': {'amt': 519, 'err': 76}, 'm': {'amt': 6199, 'err': 545}, 'w': {'amt': 5537, 'err': 440}, 'f': {'amt': 4685, 'err': 633}, 'r': {'amt': 13318, 'err': 1560}, '.': {'amt': 5125, 'err': 421}, '⏎': {'amt': 1757, 'err': 120}, '’': {
    #     'amt': 1935, 'err': 211}, 'v': {'amt': 2162, 'err': 363}, ';': {'amt': 38, 'err': 8}, '–': {'amt': 1, 'err': 0}, '*': {'amt': 105, 'err': 11}, '-': {'amt': 445, 'err': 93}, 'q': {'amt': 180, 'err': 27}, ':': {'amt': 33, 'err': 2}, 'z': {'amt': 215, 'err': 22}, '?': {'amt': 521, 'err': 49}, '“': {'amt': 1730, 'err': 151}, '”': {'amt': 1718, 'err': 336}, '!': {'amt': 31, 'err': 1}, 'é': {'amt': 2, 'err': 1}, '…': {'amt': 62, 'err': 11}, '2': {'amt': 18, 'err': 2}, '1': {'amt': 18, 'err': 3}, '6': {'amt': 9, 'err': 1}, '8': {'amt': 5, 'err': 0}, '‘': {'amt': 10, 'err': 1}, '0': {'amt': 17, 'err': 6}, '3': {'amt': 9, 'err': 3}, '/': {'amt': 1, 'err': 0}, '5': {'amt': 9, 'err': 3}, '4': {'amt': 4, 'err': 1}, '7': {'amt': 3, 'err': 2}, '&': {'amt': 3, 'err': 2}, '#': {'amt': 3, 'err': 2}, '[': {'amt': 2, 'err': 0}, ']': {'amt': 2, 'err': 0}, '9': {'amt': 2, 'err': 0}}

    letters_list = []
    for i in letters_dict:
        # print(i, letters_dict[i])
        # print(i[0], i[1]['amt'])
        letters_list.append([i, letters_dict[i]['amt'], letters_dict[i]['err']])
    # print(letters_list)

    max_freq = 0
    max_err = 0

    for i in letters_list:
        if i[1] > max_freq:
            max_freq = i[1]
        if i[2] > max_err:
            max_err = i[2]

    # print(max_freq, max_err)
    freq_mult_factor = max_freq / 255
    err_mult_factor = max_err / 255
    # print(multiplication_factor)
    data_freq_normalized = []
    for i in letters_list:
        data_freq_normalized.append([i[0], round(i[1] / freq_mult_factor), round(i[2] / err_mult_factor)])
    # print(data_freq_normalized)

    data = []
    data.append(data_freq_normalized)
    return render(request, 'main/stats.html', {'data': data})


### STATS FNs #################################################################

def get_options(user_id):
    options_res = db_get_options(user_id)
    options_dict = {'dark_mode': False}
    if options_res[0] == 'success':
        options_dict = options_res[1][0]
    return options_dict


def set_options_ajax(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user_id = request.user.account.id
    options = json.loads(request.body)
    dark_mode = options['dark_mode']
    result = db_set_options(user_id, dark_mode)
    if result[0] == 'success':
        return HttpResponse(status=204)
    else:
        return HttpResponse(status=500)

### TEST FNs ##################################################################

# def test_ajax(request, text_id):
#     if not request.user.is_authenticated:
#         return redirect('login')
#     user_id = request.user.account.id
#     # data = json.loads(request.body)
#     # print(data)
#     print(text_id)
#     result_db = db_return_one_text_stats(user_id, text_id)
#     result = json.loads(result_db[1][0][0])
#     # print(result['0'])
#     result_list = []
#     first_time = result['0']['time']
#     print(first_time)
#     for i in result:
#         # print([result[i]['txt'], result[i]['time']-first_time, result[i]['error']])
#         result_list.append([result[i]['txt'], result[i]['time']-first_time, result[i]['error']])
#     print(result_list)
#     result_str = json.dumps(result_list)
#     # print(type(result_str))
#
#     result_db = db_save_stats_new(text_id, user_id, result_str)
#     # result = ('success',)
#     return HttpResponse(json.dumps({'result': 'success'}),  # pyright: ignore
#                         content_type='application/json; charset=utf-8')

# convert old stats dict to new stats list
# def test2_ajax(request):
#     user_id = request.user.account.id
#     ids = db_return_all_text_ids()
#     # print(ids[1])
#     print(len(ids[1]))
#     for j, id in enumerate(ids[1]):
#         text_id = id[0]
#         # print(text_id)
#         result_db = db_return_one_text_stats(user_id, text_id)
#         result = json.loads(result_db[1][0][0])
#         result_list = []
#         first_time = result['0']['time']
#         for i in result:
#             result_list.append([result[i]['txt'], result[i]['time']-first_time, result[i]['error']])
#         result_str = json.dumps(result_list)
#         result_db = db_save_stats_new(text_id, user_id, result_str)
#         print(f'{j} of {len(ids[1])} (text id {text_id}) is done')
#
#     # result_db = db_return_one_text_stats(user_id, text_id)
#     #
#     # # result_db = db_return_one_text_stats2(user_id, text_id)
#     # print(sys.getsizeof(result_db[1][0][0]))
#     # result = json.loads(result_db[1][0][0])
#     # print(sys.getsizeof(result))
#     # print('Done')
#     return HttpResponse(json.dumps({'result': 'success'}),  # pyright: ignore
#                         content_type='application/json; charset=utf-8')


# @time_count
# def time_count(func, *args, **kwargs):
#     def wrapper(*args, **kwargs):
#         start = time.time()
#         func(*args, **kwargs)
#         end = time.time()
#         print(end - start)
#     return wrapper
