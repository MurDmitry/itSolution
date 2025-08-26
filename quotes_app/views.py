from django.shortcuts import render
from django.http import HttpResponse

# Домашняя старница
def home_page(request):
    return HttpResponse("<h1>Домашняя страница</h1>")

# Страница с 10 самыми популярными цитатами
def the_best_quotes(request):
    return HttpResponse("<h1>Топ 10 цитат</h1>")