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


def add_book_ajax(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user_id = request.user.account.id
    data = json.loads(request.body)
    # print(user_id, data)
    result = db_create_book(data['book_name'], user_id)
    if result[0] == 'success':
        # if True:
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
        # if True:
        return HttpResponse(json.dumps({'result': 'success'}),  # pyright: ignore
                            content_type='application/json; charset=utf-8')
    else:
        return HttpResponse(json.dumps({'result': 'failure'}),  # pyright: ignore
                            content_type='application/json; charset=utf-8')
