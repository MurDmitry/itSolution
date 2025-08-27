from django.shortcuts import render
from .models import Quote, Source
import random


# Домашняя старница
def home_page(request):
    quotes = list(Quote.objects.all().select_related('source'))   # Данные из таблицы Quote и Source

    if not quotes:
        quote_text = "Цитаты не найдены"
        context = {'quote_text': quote_text}        
    else:
        # Взвешенный случайный выбор (использую random.choices с указанием весов)
        selected_quote = random.choices(quotes, weights=[quote.weight for quote in quotes], k=1)[0]

        context = {
            'quote_text': selected_quote.text,                 # Текст цитаты
            'quote_author': selected_quote.author,             # Автор цитаты
            'source_title': selected_quote.source.title,       # Откуда (фильм/книга/игра и так далее)
            'source_author': selected_quote.source.author,     # Автор произведения
            'source_year': selected_quote.source.year,         # Год  
            'likes': selected_quote.likes,                     # Количество лайков
            'dislikes': selected_quote.dislikes,               # Количество дизлайков
            'views_count': selected_quote.views_count          # Просмотры
        }
   
    return render(request, 'base/home.html', context)


# Страница с 10 (на данный момент со всеми. Пока нет фильтрации) самыми популярными цитатами
def the_best_quotes(request):
    quotes = Quote.objects.all()    # Данные из таблицы Quote
    context = {'quotes': quotes}
    return render(request, 'base/best_quotes.html', context)