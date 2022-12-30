from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import *
from .log import *
import json


def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'main/index.html')


def my_library(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user_id = request.user.account.id
    result = db_return_users_books(user_id)[1]
    return render(request, 'main/my_library.html', {'data': result})


def type_no_txt(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'main/type_no_txt.html')


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
        if row['chapter'] != chapter:
            k += 1
            chapter = row['chapter']
            texts.append({chapter: []})
        text = row['text']
        if len(text) > 45:
            text = text[:45] + '...'
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
    text = data['text'].replace('\n\n', '\n')
    texts_list = []
    while text:
        # line_break_pos = text.find('\n', 1000)
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

def type(request, text_id):
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
    }})


def return_stats_ajax(request, text_id):
    if not request.user.is_authenticated:
        return redirect('login')
    user_id = request.user.account.id
    stats = json.loads(request.body)
    # stats = json.dumps(json.loads(request.body))
    # print(stats['stats'], stats['args'])
    result = db_save_stats(text_id, user_id, json.dumps(stats['stats']), json.dumps(stats['args']))
    if result[0] == 'success':
        # if True:
        return HttpResponse(json.dumps({'result': 'success'}),  # pyright: ignore
                            content_type='application/json; charset=utf-8')
    else:
        return HttpResponse(json.dumps({'result': 'failure'}),  # pyright: ignore
                            content_type='application/json; charset=utf-8')
