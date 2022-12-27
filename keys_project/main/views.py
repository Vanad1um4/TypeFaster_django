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
    return render(request, 'main/index.html')


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
    print(user_id, data)
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

    print(texts)
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
    print(user_id, data)
    result = db_create_text(data['book_id'], user_id, data['chapter'], data['text'], '')
    if result[0] == 'success':
        # if True:
        return HttpResponse(json.dumps({'result': 'success'}),  # pyright: ignore
                            content_type='application/json; charset=utf-8')
    else:
        return HttpResponse(json.dumps({'result': 'failure'}),  # pyright: ignore
                            content_type='application/json; charset=utf-8')
