from django.contrib import admin
from django.urls import path, include

#Для обработки выгруженных файлов
from django.conf import settings
from django.conf.urls.static import static

app_name = 'carplace'

urlpatterns = [
    path('', include('main.urls')),
]


if settings.DEBUG: #Этот путь нужен только если сайт работает в отладочном режиме
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
