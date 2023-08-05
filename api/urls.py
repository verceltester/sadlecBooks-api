
from django.contrib import admin
from django.urls import path
from api import views

from django.conf import settings
from restapi import settings
from django.conf.urls.static import static


app_name = 'api'

urlpatterns = [
    # path('', views.book),
       
     
    
    path('api/book/<int:bookid>/<int:chapid>/<int:sub1id>/<int:sub2id>/', views.Subhead2Text),
    path('api/book/<int:bookid>/<int:chapid>/<int:sub1id>/', views.Subhead1Text),
    path('api/book/<int:bookid>/<int:chapid>/', views.ChapterText),
    path('api/book/<int:bookid>/toc/', views.booktoc, name="book-toc"),
    path('api/book/<int:bookid>/', views.bookdetails, name="book-detail"),
    path('api/book/', views.book, name="book-list"),
    path('', views.home, name="home"),
   
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)