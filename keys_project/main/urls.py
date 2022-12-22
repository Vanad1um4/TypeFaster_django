from django.views.generic import RedirectView
from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('my_library/', views.my_library, name='my_library'),
    path('type_no_txt/', views.type_no_txt, name='type_no_txt'),
    path('add_book/', views.add_book, name='add_book'),

    path('', RedirectView.as_view(url='home/')),
]
