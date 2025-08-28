from django.shortcuts import render, redirect
from .models import Quote, Source
import random
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm


# Авторизация (вход в аккаунт)
def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            # Проверка на наличие пользователя
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Такого пользователя не существует")

        # Проверка пароля и логина
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Если все хорошо, то авторизируем пользователя
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Неверные логин или пароль")

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


# Выход из аккаунта
def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = UserCreationForm()
    context = {'form': form}

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Ошибка при регистрации')
    return render(request, 'base/login_register.html', context)


# Домашняя старница (требует авторизации)
@login_required(login_url='login')
def home_page(request):
    quotes = list(Quote.objects.all().select_related(
        'source'))   # Данные из таблицы Quote и Source

    if not quotes:
        quote_text = "Цитаты не найдены"
        context = {'quote_text': quote_text}
    else:
        # Взвешенный случайный выбор (использую random.choices с указанием весов)
        selected_quote = random.choices(
            quotes, weights=[quote.weight for quote in quotes], k=1)[0]

        context = {
            'quote_text': selected_quote.text,                 # Текст цитаты
            'quote_author': selected_quote.author,             # Автор цитаты
            # Откуда (фильм/книга/игра и так далее)
            'source_title': selected_quote.source.title,
            'source_author': selected_quote.source.author,     # Автор произведения
            'source_year': selected_quote.source.year,         # Год
            'likes': selected_quote.likes,                     # Количество лайков
            'dislikes': selected_quote.dislikes,               # Количество дизлайков
            'views_count': selected_quote.views_count          # Просмотры
        }

    return render(request, 'base/home.html', context)


# Страница с 10 (на данный момент со всеми. Пока нет фильтрации) самыми популярными цитатами
@login_required(login_url='login')
def the_best_quotes(request):
    quotes = Quote.objects.all()    # Данные из таблицы Quote
    context = {'quotes': quotes}
    return render(request, 'base/best_quotes.html', context)
