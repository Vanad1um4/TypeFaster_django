from django.views.generic import RedirectView
from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('my_library/', views.my_library, name='my_library'),
    path('type_no_txt/', views.type_no_txt, name='type_no_txt'),

    path('add_book/', views.add_book_ajax),
    path('rename_book/', views.rename_book_ajax),
    path('delete_book/', views.delete_book_ajax),

    path('get_texts/', views.get_texts_ajax),
    path('add_text/', views.add_text_ajax),

    path('', RedirectView.as_view(url='home/')),
]
