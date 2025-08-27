from django.shortcuts import render
from .models import Quote, Source


# Домашняя старница
def home_page(request):
    return render(request, 'base/home.html')

# Страница с 10 самыми популярными цитатами
def the_best_quotes(request):
    quotes = Quote.objects.all()    # Данные из таблицы Quote
    context = {'quotes': quotes}
    return render(request, 'base/best_quotes.html', context)