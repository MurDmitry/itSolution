from django.shortcuts import render

# Тестовые цитаты для 10 лучших 
quotes = [
    {'id': 1, 'quote': 'Цитата 1', 'rating': 7},
    {'id': 2, 'quote': 'Цитата 2', 'rating': 2},
    {'id': 3, 'quote': 'Цитата 3', 'rating': 10},
    {'id': 4, 'quote': 'Цитата 4', 'rating': 8},
]

# Домашняя старница
def home_page(request):
    return render(request, 'base/home.html')

# Страница с 10 самыми популярными цитатами
def the_best_quotes(request):
    context = {'quotes': quotes}
    return render(request, 'base/best_quotes.html', context)