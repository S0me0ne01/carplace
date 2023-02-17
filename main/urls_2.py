from django.contrib import admin
from django.urls import path

from .views import *

from django.contrib.auth.views import LoginView, LogoutView

app_name = 'main'

urlpatterns = [
    #Authentication
    path('<str:language>/login/', user_login, name = 'login'),
    path('login/', user_login, kwargs={'language': None}, name = 'login'),
    path('logout/', LogoutView.as_view(next_page='main:homepage', template_name = "logged_out.html"), name = 'logout'),
    #Homepage
    path('<str:language>/', homepage, name = 'homepage'),
    path('', homepage, kwargs={'language': None}, name = 'homepage'),
    #All
    path('<str:language>/all/<str:kind>/', all, name = 'all'),
    path('<str:language>/all/', all, kwargs={'kind': None}, name = 'all'),
    path('all/', all, kwargs={'language' : None, 'kind': None}, name = 'all'),
    #Detail
    path('<str:language>/detail/<str:kind>/<str:object_id>/', detail, name = 'detail'),
    path('detail/<str:kind>/<str:object_id>/', detail, kwargs={'language': None}, name = 'detail'),
    #Add|Edit|Delete
    path('<str:language>/add/<str:kind>/', add, name = 'add'),
    path('add/<str:kind>/', add, kwargs={'language': None}, name = 'add'),
    path('<str:language>/add/', add, kwargs={'kind': None}, name = 'add'),
    path('add/', add, kwargs={'language' : None, 'kind': None}, name = 'add'),
    path('<str:language>/edit/<str:kind>/<str:object_id>/', edit, name = 'edit'),
    path('edit/<str:kind>/<str:object_id>/', edit, kwargs={'language' : None, 'kind': None}, name = 'edit'),
    path('<str:language>/delete/<str:kind>/<str:object_id>/', delete, name = 'delete'),
    path('delete/<str:kind>/<str:object_id>/', delete, kwargs={'language': None}, name = 'delete'),
    #Basket
    path('<str:language>/basket/<str:action>/<str:product_id>/<int:quantity>/', basket_add, name = 'basket_add'),
    path('basket/<str:action>/<str:product_id>/<int:quantity>/', basket_add, kwargs={'language': None}, name = 'basket_add'),
    path('<str:language>/basket/<str:action>/<str:product_id>/<int:quantity>/', basket_add, name = 'basket_add'),
    path('basket/<str:action>/<str:product_id>/<int:quantity>/', basket_add, kwargs={'language': None}, name = 'basket_add'),
    path('<str:language>/basket/<str:action>/<str:product_id>/', basket_add, kwargs={'quantity': 1}, name = 'basket_add'),
    path('basket/<str:action>/<str:product_id>/', basket_add, kwargs={'language' : None, 'quantity': 1}, name = 'basket_add'),
    path('<str:language>/basket/erase/', basket_erase, name = 'basket_erase'),
    path('basket/erase/', basket_erase, kwargs={'language': None}, name = 'basket_erase'),
    path('<str:language>/basket/', basket, name = 'basket'),
    path('basket/', basket, kwargs={'language': None}, name = 'basket'),
    #Moderation
    path('<str:language>/moderation/', moderation, name = 'moderation'),
    path('moderation/', moderation, kwargs={'language': None}, name = 'moderation'),
    #Search
    path('<str:language>/search/<str:text>/', search_result, name = 'search_result'),
    path('search/<str:text>/', search_result, kwargs={'language': None}, name = 'search_result'),
    path('<str:language>/search/', search_input, name = 'search_input'),
    path('search/', search_input, kwargs={'language': None}, name = 'search_input'),
]
