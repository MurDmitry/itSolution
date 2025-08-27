from django.shortcuts import render
from .models import Quote, Source
import random


# Домашняя старница
def home_page(request):
    quotes = list(Quote.objects.all())   # Данные из таблицы Quote

    if not quotes:
        quote_text = "Цитаты не найдены"
    else:
        # Взвешенный случайный выбор (использую random.choices с указанием весов)
        selected_quote = random.choices(quotes, weights=[quote.weight for quote in quotes], k=1)[0]
        quote_text = selected_quote.text

    content = {'quote_text': quote_text}
    return render(request, 'base/home.html', content)


# Страница с 10 (на данный момент со всеми. Пока нет фильтрации) самыми популярными цитатами
def the_best_quotes(request):
    quotes = Quote.objects.all()    # Данные из таблицы Quote
    context = {'quotes': quotes}
    return render(request, 'base/best_quotes.html', context)