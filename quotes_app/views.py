from django.shortcuts import render

# Домашняя старница
def home_page(request):
    return render(request, 'home.html')

# Страница с 10 самыми популярными цитатами
def the_best_quotes(request):
    return render(request, 'best_quotes.html')