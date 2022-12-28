from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import *
from .log import *
import json


def home(request):
    if request.user.is_authenticated:
        return render(request, 'main/index.html')
        # return redirect('home')
    return redirect('login')


def my_library(request):
    user_id = request.user.account.id
    result = db_return_users_books(user_id)[1]
    return render(request, 'main/my_library.html', {'data': result})


def type_no_txt(request):
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
    # print(user_id, data)
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
    # print(user_id, data)
    result = db_get_texts(data['book_id'], user_id)
    texts = []
    chapter = ''
    k = -1
    for row in result[1]:
        print(row)
        if row['chapter'] != chapter:
            k += 1
            chapter = row['chapter']
            texts.append({chapter: []})
        text = row['text']
        if len(text) > 33:
            text = text[:33] + '...'
        texts[k][chapter].append({'text_id': row['id'], 'text_preview': text, 'done': row['done']})

        # if row['chapter'] not in chapters:
        #     chapters.append(row['chapter'])
        #     k += 1
        #     texts[k] = []
        # texts[k].append({'text_id': row['id'], 'text_preview': row['text'][:33] + '...', 'done': row['done']})

    # print(texts)
    # print(chapters)

    if result[0] == 'success':
        # if True:
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
    # print(user_id, data)
    text = data['text'].replace('\n\n', '\n')
    texts_list = []
    while text:
        line_break_pos = text.find('\n', 100)
        if line_break_pos != -1:
            texts_list.append(text[:line_break_pos])
            text = text[line_break_pos+1:]
        if line_break_pos == -1:
            texts_list.append(text)
            text = ''
    # print(texts_list)
    # for text in texts_list:
    #     print(text)
    result = db_batch_create_texts(data['book_id'], user_id, data['chapter'], texts_list)
    if result[0] == 'success':
        # if True:
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

    result = db_get_a_text_with_stats(text_id, user_id)
    print(result)

    if result[0] == 'success':
        text = result[1][0]['text']
        stats = result[1][0]['stats']
        if stats:
            stats = json.loads(stats)
            complete = True
            cpm = stats['cpm']
            wpm = stats['wpm']
            acc = stats['acc']
            chars = stats['chars']
            words = stats['words']
            errors = stats['errors']
            time = stats['time']

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
        'id': text_id
    }})


def return_stats(request, text_id):
    if not request.user.is_authenticated:
        return redirect('login')
    # data = json.loads(request.body)
    # print(json.dumps(data))
    user_id = request.user.account.id
    stats = json.dumps(json.loads(request.body))
    result = db_save_stats(text_id, user_id, stats)
    # profile = request.user.profile
    # text = Text.objects.get(id=text_id)
    # try:
    #     stats = TextStats.objects.get(text__id=text.id, user__id=profile.id)
    # except Exception as e:
    #     print(e)
    #     stats = TextStats(text=text, user=profile)
    # stats.complete = data['complete']
    # stats.stats_string = data['stats']
    # stats.cpm = data['cpm']
    # stats.wpm = data['wpm']
    # stats.acc = data['acc']
    # stats.chars = data['chars']
    # stats.words = data['words']
    # stats.errors = data['errors']
    # stats.time = data['time']
    #
    # stats.save()
    return HttpResponse(json.dumps({'result': 'success'}),  # pyright: ignore
                        content_type='application/json; charset=utf-8')
    return HttpResponse(json.dumps({'result': 'failure'}),  # pyright: ignore
                        content_type='application/json; charset=utf-8')
