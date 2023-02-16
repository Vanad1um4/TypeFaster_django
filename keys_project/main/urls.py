from django.views.generic import RedirectView
from django.urls import path
from . import views

urlpatterns = [
    # path('home/', views.home, name='home'),
    path('my_library/', views.my_library, name='my_library'),
    path('type/', views.type_no_txt, name='type_no_txt'),

    path('add_book/', views.add_book_ajax),
    path('rename_book/', views.rename_book_ajax),
    path('delete_book/', views.delete_book_ajax),

    path('get_texts/', views.get_texts_ajax),
    path('add_text/', views.add_text_ajax),
    path('delete_texts_by_chapter/', views.delete_texts_by_chapter_ajax),
    path('delete_text_by_id/', views.delete_text_by_id_ajax),

    path('type/<int:text_id>/', views.type_text),
    path('type/<int:text_id>/return_stats/', views.return_stats_ajax),

    path('stats/', views.my_stats, name='stats'),

    path('set_options/', views.set_options_ajax),
    # path('test/<int:text_id>/', views.test_ajax),
    # path('test2/', views.test2_ajax),

    path('', RedirectView.as_view(url='my_library/')),
]
