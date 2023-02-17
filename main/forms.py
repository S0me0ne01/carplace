from django import forms
from .models import *

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.core import validators
from django.core.validators import FileExtensionValidator


class ProductCategoryForm(forms.ModelForm):
	name = forms.CharField(label = 'Название на русском')
	name_kz = forms.CharField(label = 'Название на казахском')

	class Meta:
		model = ProductCategory
		fields = ('name', 'name_kz',)


class ServiceCategoryForm(forms.ModelForm):
	name = forms.CharField(label = 'Название на русском')
	name_kz = forms.CharField(label = 'Название на казахском')

	class Meta:
		model = ServiceCategory
		fields = ('name', 'name_kz',)


class ProductForm(forms.ModelForm):
	category = forms.ModelChoiceField(queryset = ProductCategory.objects.all(), label = "Категория", empty_label = None, error_messages={'required': 'Выберите категорию'}, widget=forms.widgets.Select(attrs={'size': 8}))
	name = forms.CharField(label = 'Название на русском')
	name_kz = forms.CharField(label = 'Название на казахском')
	description = forms.CharField(label = 'Описание на русском', widget=forms.widgets.Textarea())
	description_kz = forms.CharField(label = 'Описание на казахском', widget=forms.widgets.Textarea())
	image = forms.ImageField(label = 'Изображение', validators=[FileExtensionValidator(allowed_extensions=('png', 'jpg', 'jpeg'))], error_messages={'invalid_extension' : 'Этот формат не поддерживается', 'required' : ''}, required = True)
	price = forms.IntegerField(label = 'Цена')
	in_stock = forms.BooleanField(label = 'Есть в наличии')

	class Meta:
		model = Product
		fields = ('category', 'name', 'name_kz', 'description', 'description_kz', 'image', 'price', 'in_stock',)


class ServiceForm(forms.ModelForm):
	category = forms.ModelChoiceField(queryset = ServiceCategory.objects.all(), label = "Категория", empty_label = None, error_messages={'required': 'Выберите категорию'}, widget=forms.widgets.Select(attrs={'size': 8}))
	name = forms.CharField(label = 'Название на русском')
	name_kz = forms.CharField(label = 'Название на казахском')
	description = forms.CharField(label = 'Описание', widget=forms.widgets.Textarea())
	description_kz = forms.CharField(label = 'Описание на казахском', widget=forms.widgets.Textarea())
	image = forms.ImageField(label = 'Изображение', validators=[FileExtensionValidator(allowed_extensions=('png', 'jpg', 'jpeg'))], error_messages={'invalid_extension' : 'Этот формат не поддерживается', 'required' : ''}, required = True)
	price = forms.IntegerField(label = 'Цена')
	duration = forms.IntegerField(label = 'Время выполнения (мин)')

	class Meta:
		model = Service
		fields = ('category', 'name', 'name_kz', 'description', 'description_kz', 'image', 'price', 'duration',)


class PhoneForm(forms.ModelForm):
	phone = forms.CharField(label = '')

	class Meta:
		model = Phone
		fields = ('phone',)


class SearchForm(forms.ModelForm):
	text = forms.CharField(label = '')

	class Meta:
		model = Search
		fields = ('text',)


class LoginForm(forms.Form):
	username = forms.CharField(label = 'Ваш никнейм')
	password = forms.CharField(label = 'Ваш пароль', widget=forms.PasswordInput)
