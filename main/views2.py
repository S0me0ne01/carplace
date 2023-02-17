from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User, UserManager
from django.contrib.auth.forms import UserCreationForm

from .models import *
from .forms import *

import time
import datetime
import requests

from django.contrib.auth import authenticate, login
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import HttpResponseRedirect, HttpRequest, HttpResponseForbidden, HttpResponse, HttpResponseNotFound, Http404
from django.urls import reverse

from django.core.paginator import Paginator
from django.core.mail import send_mail


def homepage(request, language):
    kw = {'language' : language}
    language_check('main:homepage', kw)
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

    context = {'p_categories' : p_categories, 's_categories' : s_categories, 'products' : products, 'services' : services}
    return render(request, 'homepage.html', context)


def all(request, language, kind):
    kw = {'language' : language, 'kind' : kind}
    language_check('main:all', kw)
    p_categories = ProductCategory.objects.all()
    s_categories = ServiceCategory.objects.all()

    if kind == 'products':
        objects = Product.objects.order_by('-published')
    elif kind == 'services':
        objects = Service.objects.order_by('-published')
    elif kind == 'p_categories' or kind == 's_categories':
        pass
    else:
        return HttpResponseNotFound()

    paginator = Paginator(objects, 6)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)

    context = {'p_categories' : p_categories, 's_categories' : s_categories, 'kind' : kind, 'objects' : page.object_list, 'page' : page}
    return render(request, 'all.html', context)


def detail(request, language, kind, object_id):
    kw = {'language' : language, 'kind' : kind, 'object_id' : object_id}
    language_check('main:detail', kw)
    p_categories = ProductCategory.objects.all()
    s_categories = ServiceCategory.objects.all()

    if kind == 'service':
        object = get_object_or_404(Service, id = object_id)
    else:
        object = get_object_or_404(Product, id = object_id)

    context = {'p_categories' : p_categories, 's_categories' : s_categories, 'object' : object}
    return render(request, 'detail.html', context)


def add(request, language, kind):
    if True:
        kw = {'language' : language, 'kind' : kind}
        language_check('main:add', kw)
        p_categories = ProductCategory.objects.all()
        s_categories = ServiceCategory.objects.all()

        if kind == 'products':
            form_type = ProductForm
        elif kind == 'services':
            form_type = ServiceForm
        elif kind == 'p_categories':
            form_type = ProductCategoryForm
        elif kind == 's_categories':
            form_type = ServiceCategoryForm
        else:
            context = {'p_categories' : p_categories, 's_categories' : s_categories}
            return render(request, 'add_choose.html', context)

        if request.method == "POST":
            f = form_type(request.POST, request.FILES)
            if f.is_valid():
                f = f.save(commit = False)
                f.save()
                return HttpResponseRedirect(reverse('main:all', args = (kind,)))
            else:
                context = {'p_categories' : p_categories, 's_categories' : s_categories, 'kind' : kind, 'form' : f}
                return render(request, 'add.html', context)
        else:
            f = form_type()
            context = {'p_categories' : p_categories, 's_categories' : s_categories, 'kind' : kind, 'form' : f}
            return render(request, 'add.html', context)
    else:
        return HttpResponseNotFound()


def edit(request, language, kind, object_id):
    if request.user.is_staff:
        kw = {'language' : language, 'kind' : kind, 'object_id' : object_id}
        language_check('main:edit', kw)
        p_categories = ProductCategory.objects.all()
        s_categories = ServiceCategory.objects.all()

        if kind == 'products':
            form_type = 'ProductForm'
            object = get_object_or_404(Product, id = object_id)

        elif kind == 'services':
            form_type = 'ServiceForm'
            object = get_object_or_404(Service, id = object_id)

        elif kind == 'p_categories':
            form_type = 'ProductCategoryForm'
            object = get_object_or_404(ProductCategory, id = object_id)

        elif kind == 's_categories':
            form_type = 'ServiceCategoryForm'
            object = get_object_or_404(ServiceCategoryForm, id = object_id)

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
                context = {'p_categories' : p_categories, 's_categories' : s_categories, 'kind' : kind, 'form' : f}
                return render(request, 'edit.html', context)
        else:
            f = form_type(instance = object)
            context = {'p_categories' : p_categories, 's_categories' : s_categories, 'kind' : kind, 'form' : f}
            return render(request, 'edit.html', context)
    else:
        return HttpResponseNotFound()


def delete(request, language, kind, object_id):
    if request.user.is_staff:
        kw = {'language' : language, 'kind' : kind, 'object_id' : object_id}
        language_check('main:delete', kw)

        if kind == 'products':
            object = get_object_or_404(Product, id = object_id)
            rdir = HttpResponseRedirect(reverse('main:all', args = (kind,)))

        elif kind == 'services':
            object = get_object_or_404(Service, id = object_id)
            rdir = HttpResponseRedirect(reverse('main:all', args = (kind,)))

        elif kind == 'p_categories':
            object = get_object_or_404(ProductCategory, id = object_id)
            rdir = HttpResponseRedirect(reverse('main:categories', args = ()))

        elif kind == 's_categories':
            object = get_object_or_404(ServiceCategory, id = object_id)
            rdir = HttpResponseRedirect(reverse('main:categories', args = ()))

        else:
            return HttpResponseNotFound()

        if object.image:
            object.image.delete()
        object.delete()

        return rdir
    else:
        return HttpResponseNotFound()


def basket(request, language):
    if request.user.is_authenticated:
        kw = {'language' : language}
        language_check('main:basket', kw)
        p_categories = ProductCategory.objects.all()
        s_categories = ServiceCategory.objects.all()
        baskets = Basket.objects.filter(client = request.user.client).order_by('-date')


        total_price = 0
        for basket in baskets:
            total_price += basket.product.price

        context = {'p_categories' : p_categories, 's_categories' : s_categories, 'baskets' : baskets, 'total_price' : total_price}
        return render(request, 'basket.html', context)
    else:
        return HttpResponseRedirect(reverse('main:login', args = ()))


def basket_add(request, language, action, product_id, quantity):
    if request.user.is_authenticated:
        kw = {'language' : language, 'action' : action, 'product_id' : product_id, 'quantity' : quantity}
        language_check('main:basket_add', kw)

        if action == 'add':
            try:
                product = get_object_or_404(Product, id = product_id)
                basket = Basket.objects.get(client = request.user.client, product = product)
            except Basket.DoesNotExist:
                basket = Basket.objects.create(client = request.user.client, product = product, quantity = quantity)
            return HttpResponseRedirect(request.meta['HTTP_REFERRER'])
        elif action == 'remove':
            try:
                product = get_object_or_404(Product, id = product_id)
                basket = Basket.objects.get(client = request.user.client, product = product)
                basket.delete()
            except Basket.DoesNotExist:
                pass
            return HttpResponseRedirect(request.meta['HTTP_REFERRER'])
        else:
            return HttpResponseNotFound()
    else:
        return HttpResponseRedirect(reverse('main:login', args = ()))


def basket_erase(request, language):
    if request.user.is_authenticated:
        kw = {'language' : language}
        language_check('main:basket_erase', kw)

        baskets = Basket.objects.filter(client = request.user.client)
        for basket in baskets:
            basket.delete()
        return HttpResponseRedirect(reverse('main:basket', args = ()))
    else:
        return HttpResponseRedirect(reverse('main:login', args = ()))


def message_seller(request, language):
    if request.user.is_authenticated:
        if request.user.client.phone != Null:
            kw = {'language' : language}
            language_check('main:message_seller', kw)

            baskets = Basket.objects.filter(client = request.user.client)
        else:
            return HttpResponseRedirect(reverse('main:login', args = ()))
    else:
        return HttpResponseRedirect(reverse('main:login', args = ()))


def phone(request, language):
    kw = {'language' : language}
    language_check('main:phone', kw)
    p_categories = ProductCategory.objects.all()
    s_categories = ServiceCategory.objects.all()

    if request.user.is_authenticated:
        if request.user.client.phone != Null:
            phone = request.user.client.phone
        else:
            phone = Null
        if request.method == "POST":
            pf = PhoneForm(request.POST, instance = phone)
            if pf.is_valid():
                pf = pf.save(commit = False)
                pf.save()
                return HttpResponseRedirect(request.meta['HTTP_REFERRER'])
            else:
                context = {'p_categories' : p_categories, 's_categories' : s_categories, 'form' : pf}
                return render(request, 'phone.html', context)
        else:
            pf = PhoneForm(instance = phone)
            context = {'p_categories' : p_categories, 's_categories' : s_categories, 'form' : pf}
            return render(request, 'phone.html', context)
    else:
        return HttpResponseRedirect(reverse('main:login', args = ()))


def moderation(request, language):
    if request.user.is_staff:
        kw = {'language' : language}
        language_check('main:moderation', kw)
        p_categories = ProductCategory.objects.all()
        s_categories = ServiceCategory.objects.all()
        ips = Ip.objects.order_by('-year', '-month')

        context = {'p_categories' : p_categories, 's_categories' : s_categories, 'ips' : ips}
        return render(request, 'moderation.html', context)
    else:
        return HttpResponseNotFound()


def search_input(request, language):
    kw = {'language' : language}
    language_check('main:search_input', kw)
    p_categories = ProductCategory.objects.all()
    s_categories = ServiceCategory.objects.all()

    if request.method == "POST":
        sf = SearchForm(request.POST)
        if sf.is_valid():
            sf = sf.save(commit = False)
            return HttpResponseRedirect(reverse('main:search_result', args = (sf.text,)))
        else:
            context = {'p_categories' : p_categories, 's_categories' : s_categories, 'form' : sf}
            return render(request, 'search_input.html', context)
    else:
        sf = SearchForm()
        context = {'p_categories' : p_categories, 's_categories' : s_categories, 'form': sf}
        return render(request, 'search_input.html', context)


def search_result(request, language, text):
    kw = {'language' : language}
    language_check('main:search_result', kw)
    p_categories = ProductCategory.objects.all()
    s_categories = ServiceCategory.objects.all()

    products = Product.objects.filter(name__icontains = text)
    services = Service.objects.filter(name__icontains = text)

    paginator = Paginator(products, 6)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)

    context = {'p_categories' : p_categories, 's_categories' : s_categories, 'products' : page.object_list, 'services' : services, 'page' : page}
    return render(request, 'search_result.html', context)


def language_check(redirect_to, kw):
    if kw['language'] != 'ru' and kw['language'] != 'kz' and kw['language'] != None:
        return HttpResponseNotFound()
    if kw['language'] == None:
        kw['language'] = 'ru'

        return HttpResponseRedirect(reverse(redirect_to, kwargs = kw))



def user_login(request, language):
    kw = {'language' : language}
    language_check('main:login', kw)
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
            lf = LoginForm()
            context = {'form' : lf}
            return render(request, 'login.html', context)
