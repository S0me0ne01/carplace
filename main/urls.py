from django.contrib import admin
from django.urls import path

from .views import *

from django.contrib.auth.views import LoginView, LogoutView

app_name = 'main'

urlpatterns = [
    #Authentication
    path('login/', user_login, name = 'login'),
    path('logout/', LogoutView.as_view(next_page='main:homepage', template_name = "logged_out.html"), name = 'logout'),
    #Homepage
    path('', homepage, name = 'homepage'),
    #All
    path('all/<str:kind>/', all, name = 'all'),
    path('all/', all, kwargs={'kind': None}, name = 'all'),
    #by_category
    path('category/<str:kind>/<str:category_id>/', by_category, name = 'by_category'),
    #Detail
    path('detail/<str:kind>/<str:object_id>/', detail, name = 'detail'),
    #Add|Edit|Delete
    path('add/<str:kind>/', add, name = 'add'),
    path('add/', add, kwargs={'kind': None}, name = 'add'),
    path('edit/<str:kind>/<str:object_id>/', edit, name = 'edit'),
    path('delete/<str:kind>/<str:object_id>/', delete, name = 'delete'),
    #Language
    path('language/change/<str:new_language>/', language_change, name = 'language_change'),
    #Moderation
    path('moderation/', moderation, name = 'moderation'),
    #Search
    path('search/<str:text>/', search_result, name = 'search_result'),
    path('search/', search_input, name = 'search_input'),
]
