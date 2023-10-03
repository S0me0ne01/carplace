from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User, UserManager
from django.contrib.auth.forms import UserCreationForm

from .models import *
from .forms import *

import time
import datetime
import requests
import telegram

from django.contrib.auth import authenticate, login
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import HttpResponseRedirect, HttpRequest, HttpResponseForbidden, HttpResponse, HttpResponseNotFound, Http404
from django.urls import reverse

from django.template import RequestContext

from django.core.paginator import Paginator
from django.core.mail import send_mail


def homepage(request):
    p_categories = ProductCategory.objects.all()
    s_categories = ServiceCategory.objects.all()

    products = Product.objects.order_by('-views')[:6]
    services = Service.objects.order_by('-views')[:6]

    adress = request.META.get('HTTP_X_FORWARDED_FOR')
    if adress:
        adress = adress.split(',')[-1].strip()
    else:
        adress = request.META.get('REMOTE_ADDR')

    try:
        ip = Ip.objects.get(adress = adress, year = str(datetime.datetime.now().year), month = str(datetime.datetime.now().month))
    except Ip.DoesNotExist:
        Ip.objects.create(adress = adress, year = str(datetime.datetime.now().year), month = str(datetime.datetime.now().month))

    language = request.COOKIES.get('language')
    if not language:
        language = 'ru'

    context = {'language' : language, 'p_categories' : p_categories, 's_categories' : s_categories, 'products' : products, 'services' : services}
    response = render(request, 'homepage.html', context)
    response.set_cookie('language', language)
    return response


def all(request, kind):
    p_categories = ProductCategory.objects.all()
    s_categories = ServiceCategory.objects.all()

    language = request.COOKIES.get('language')
    if not language:
        language = 'ru'

    if kind == 'products':
        objects = Product.objects.order_by('-published')
    elif kind == 'services':
        objects = Service.objects.order_by('-published')
    elif kind == 'p_categories' or kind == 's_categories':
        template = 'all.html'
        context = {'language' : language, 'p_categories' : p_categories, 's_categories' : s_categories, 'kind' : kind}
    else:
        context = {'language' : language, 'p_categories' : p_categories, 's_categories' : s_categories}
        template = 'all_choose.html'

    if kind == 'products' or kind == 'services':
        paginator = Paginator(objects, 6)
        if 'page' in request.GET:
            page_num = request.GET['page']
        else:
            page_num = 1
        page = paginator.get_page(page_num)
        context = {'language' : language, 'p_categories' : p_categories, 's_categories' : s_categories, 'kind' : kind, 'objects' : page.object_list, 'page' : page}
        template = 'all.html'


    response = render(request, template, context)
    response.set_cookie('language', language)
    return response


def by_category(request, kind, category_id):
    p_categories = ProductCategory.objects.all()
    s_categories = ServiceCategory.objects.all()

    language = request.COOKIES.get('language')
    if not language:
        language = 'ru'

    if kind == 'products':
        category = get_object_or_404(ProductCategory, id = category_id)
        objects = Product.objects.filter(category = category)
    elif kind == 'services':
        category = get_object_or_404(ServiceCategory, id = category_id)
        objects = Service.objects.filter(category = category)
    else:
        return HttpResponseNotFound()

    paginator = Paginator(objects, 6)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)

    context = {'language' : language, 'p_categories' : p_categories, 's_categories' : s_categories, 'category' : category, 'kind' : kind, 'objects' : page.object_list, 'page' : page}
    response = render(request, 'by_category.html', context)
    response.set_cookie('language', language)
    return response



def detail(request, kind, object_id):
    p_categories = ProductCategory.objects.all()
    s_categories = ServiceCategory.objects.all()

    language = request.COOKIES.get('language')
    if not language:
        language = 'ru'

    if kind == 'services':
        object = get_object_or_404(Service, id = object_id)
    else:
        object = get_object_or_404(Product, id = object_id)

    context = {'language' : language, 'p_categories' : p_categories, 's_categories' : s_categories, 'object' : object, 'kind' : kind}
    response = render(request, 'detail.html', context)
    response.set_cookie('language', language)
    return response


def add(request, kind):
    if request.user.is_staff:
        p_categories = ProductCategory.objects.all()
        s_categories = ServiceCategory.objects.all()

        language = request.COOKIES.get('language')
        if not language:
            language = 'ru'

        if kind == 'products':
            form_type = ProductForm
        elif kind == 'services':
            form_type = ServiceForm
        elif kind == 'p_categories':
            form_type = ProductCategoryForm
        elif kind == 's_categories':
            form_type = ServiceCategoryForm
        else:
            context = {'language' : language, 'p_categories' : p_categories, 's_categories' : s_categories}
            response = render(request, 'add_choose.html', context)
            response.set_cookie('language', language)
            return response

        if request.method == "POST":
            f = form_type(request.POST, request.FILES)
            if f.is_valid():
                f = f.save(commit = False)
                f.save()
                return HttpResponseRedirect(reverse('main:all', args = (kind,)))
            else:
                context = {'language' : language, 'p_categories' : p_categories, 's_categories' : s_categories, 'kind' : kind, 'form' : f}
                response = render(request, 'add.html', context)
                response.set_cookie('language', language)
                return response
        else:
            f = form_type()
            context = {'language' : language, 'p_categories' : p_categories, 's_categories' : s_categories, 'kind' : kind, 'form' : f}
            response = render(request, 'add.html', context)
            response.set_cookie('language', language)
            return response
    else:
        return HttpResponseNotFound()


def edit(request, kind, object_id):
    language = request.COOKIES.get('language')
    if not language:
        language = 'ru'

    if request.user.is_staff:
        p_categories = ProductCategory.objects.all()
        s_categories = ServiceCategory.objects.all()

        if kind == 'products':
            form_type = ProductForm
            object = get_object_or_404(Product, id = object_id)

        elif kind == 'services':
            form_type = ServiceForm
            object = get_object_or_404(Service, id = object_id)

        elif kind == 'p_categories':
            form_type = ProductCategoryForm
            object = get_object_or_404(ProductCategory, id = object_id)

        elif kind == 's_categories':
            form_type = ServiceCategoryForm
            object = get_object_or_404(ServiceCategory, id = object_id)

        else:
            return HttpResponseNotFound()

        if request.method == "POST":
            f = form_type(request.POST, request.FILES, instance = object)
            if f.is_valid():
                f = f.save(commit = False)
                f.save()
                if kind == 'products' or kind == 'services':
                    return HttpResponseRedirect(reverse('main:detail', args = (kind, object_id,)))
                else:
                    return HttpResponseRedirect(reverse('main:all', args = (kind,)))
            else:
                context = {'language' : language, 'p_categories' : p_categories, 's_categories' : s_categories, 'object_id' : object_id, 'kind' : kind, 'form' : f}
                response = render(request, 'add.html', context)
                response.set_cookie('language', language)
                return response
        else:
            f = form_type(instance = object)
            context = {'language' : language, 'p_categories' : p_categories, 's_categories' : s_categories, 'object_id' : object_id, 'kind' : kind, 'form' : f}
            response = render(request, 'add.html', context)
            response.set_cookie('language', language)
            return response
    else:
        return HttpResponseNotFound()


def delete(request, kind, object_id):
    language = request.COOKIES.get('language')
    if not language:
        language = 'ru'

    if request.user.is_staff:
        if kind == 'products':
            object = get_object_or_404(Product, id = object_id)

        elif kind == 'services':
            object = get_object_or_404(Service, id = object_id)

        elif kind == 'p_categories':
            object = get_object_or_404(ProductCategory, id = object_id)
            if object.image:
                object.image.delete()

        elif kind == 's_categories':
            object = get_object_or_404(ServiceCategory, id = object_id)
            if object.image:
                object.image.delete()
        else:
            return HttpResponseNotFound()

        if kind == 'products' or kind == 'services' or kind == 'p_categories' or kind == 's_categories':
            object.delete()

        return HttpResponseRedirect(reverse('main:all', args = (kind,)))
    else:
        return HttpResponseNotFound()


def moderation(request):
    language = request.COOKIES.get('language')
    if not language:
        language = 'ru'

    if request.user.is_staff:
        p_categories = ProductCategory.objects.all()
        s_categories = ServiceCategory.objects.all()
        views = Ip.objects.filter(year = str(datetime.datetime.now().year), month = str(datetime.datetime.now().month)).count()

        context = {'language' : language, 'p_categories' : p_categories, 's_categories' : s_categories, 'views' : views}
        response = render(request, 'moderation.html', context)
        response.set_cookie('language', language)
        return response
    else:
        return HttpResponseNotFound()


def search_input(request):
    language = request.COOKIES.get('language')
    if not language:
        language = 'ru'

    p_categories = ProductCategory.objects.all()
    s_categories = ServiceCategory.objects.all()

    if request.method == "POST":
        sf = SearchForm(request.POST)
        if sf.is_valid():
            sf = sf.save(commit = False)
            return HttpResponseRedirect(reverse('main:search_result', args = (sf.text,)))
        else:
            context = {'language' : language, 'p_categories' : p_categories, 's_categories' : s_categories, 'form' : sf}
            response = render(request, 'search_input.html', context)
            response.set_cookie('language', language)
            return response
    else:
        sf = SearchForm()
        context = {'language' : language, 'p_categories' : p_categories, 's_categories' : s_categories, 'form': sf}
        response = render(request, 'search_input.html', context)
        response.set_cookie('language', language)
        return response


def search_result(request, text):
    language = request.COOKIES.get('language')
    if not language:
        language = 'ru'

    p_categories = ProductCategory.objects.all()
    s_categories = ServiceCategory.objects.all()

    products = Product.objects.filter(name__icontains = text)
    services = Service.objects.filter(name__icontains = text)

    context = {'language' : language, 'p_categories' : p_categories, 's_categories' : s_categories, 'products' : products, 'services' : services}
    response = render(request, 'search_result.html', context)
    response.set_cookie('language', language)
    return response


def language_change(request, new_language):
    response = redirect(request.META['HTTP_REFERER'])
    if new_language == 'kz' or new_language == 'ru':
        response.set_cookie('language', new_language)

    return response


def user_login(request):
    language = request.COOKIES.get('language')
    if not language:
        language = 'ru'

    if request.method == 'POST':
        lf = LoginForm(request.POST)
        if lf.is_valid():
            cd = lf.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('main:homepage', args = ()))
                else:
                    return HttpResponse('Ошибка аккаунта')
            else:
                return HttpResponse('Некорректные данные')
        else:
            context = {'language' : language, 'form' : lf}
            response = render(request, 'login.html', context)
            response.set_cookie('language', language)
            return response
    else:
        lf = LoginForm()
        context = {'language' : language, 'form' : lf}
        response = render(request, 'login.html', context)
        response.set_cookie('language', language)
        return response
