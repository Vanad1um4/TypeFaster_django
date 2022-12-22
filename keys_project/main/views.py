from django.shortcuts import render, redirect


def home(request):
    if request.user.is_authenticated:
        return render(request, 'main/index.html')
        # return redirect('home')
    return redirect('login')


def my_library(request):
    return render(request, 'main/my_library.html')


def type_no_txt(request):
    return render(request, 'main/index.html')


def add_book(request):
    return render(request, 'main/index.html')

# def my_library(request):
#     return render(request, 'main/index.html')
