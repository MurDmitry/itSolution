from django.shortcuts import render, redirect
from .models import Quote, Source
import random
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt


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


@login_required
@csrf_exempt    # Декоратор, отключающий CSRF защиту для этого view (обычно для API endpoints)
@require_POST   # Декоратор, разрешающий только POST запросы к этому view
def like_quote(request, quote_id):
    try:
        quote = Quote.objects.get(id=quote_id)
        quote.toggle_like(request.user)         # Метод (из model.py) переключения лайка для текущего пользователя
        quote.save()
        return JsonResponse({                   # JSON ответ с результатом операции
            'success': True,
            'likes': quote.likes,               # Количество лайков после изменения
            'dislikes': quote.dislikes
        })
    except Quote.DoesNotExist:
        return JsonResponse({'success': False})


@login_required
@csrf_exempt
@require_POST
def dislike_quote(request, quote_id):
    try:
        quote = Quote.objects.get(id=quote_id)
        quote.toggle_dislike(request.user)        # Метод (из model.py) переключения дизлайка для текущего пользователя
        quote.save()
        return JsonResponse({
            'success': True,
            'likes': quote.likes,
            'dislikes': quote.dislikes
        })
    except Quote.DoesNotExist:
        return JsonResponse({'success': False})


# Домашняя старница (требует авторизации)
@login_required(login_url='login')
def home_page(request):
    quotes = list(Quote.objects.all().select_related('source'))

    if not quotes:
        quote_text = "Цитаты не найдены"
        context = {'quote_text': quote_text}
    else:
        selected_quote = random.choices(
            quotes, weights=[quote.weight for quote in quotes], k=1)[0]
        
        # Проверка: если человек (в этой сессии) уже смотрел => просмотр не засчитываю
        session_key = f'quote_viewed_{selected_quote.id}'
        if not request.session.get(session_key, False):
            # Увеличиваю счетчик просмотров только если цитата еще не просмотрена в этой сессии
            selected_quote.views_count += 1
            selected_quote.save()
            request.session[session_key] = True
        
        # Проверяю, поставил ли пользователь лайк или дизлайк этой цитате
        user_liked = request.user in selected_quote.liked_by.all()
        user_disliked = request.user in selected_quote.disliked_by.all()

        context = {
            'quote_id': selected_quote.id,                  # id цитаты
            'quote_text': selected_quote.text,
            'quote_author': selected_quote.author,
            'source_title': selected_quote.source.title,
            'source_author': selected_quote.source.author,
            'source_year': selected_quote.source.year,
            'likes': selected_quote.likes,                  # Общее количество лайков
            'dislikes': selected_quote.dislikes,            # Общее количество дизлайков
            'views_count': selected_quote.views_count,      # Количество просмотров
            'user_liked': user_liked,                       # Лайкнул ли текущий пользователь
            'user_disliked': user_disliked                  # Дизлайкнул ли текущий пользователь
        }
    return render(request, 'base/home.html', context)


# Страница с 10 самыми популярными цитатами
@login_required(login_url='login')
def the_best_quotes(request):
    # 10 цитат, отсортированных по лайкам и весу
    quotes = Quote.objects.all().order_by('-likes', '-weight')[:10]
    
    # Данные для таблицы
    ranked_quotes = []
    for i, quote in enumerate(quotes, 1):
        # Текст цитаты с автором и источником
        author_display = quote.author if quote.author else quote.source.author
        formatted_text = f'«{quote.text}» - {author_display}, {quote.source.title}'
        
        ranked_quotes.append({
            'position': i,
            'formatted_text': formatted_text,
            'likes': quote.likes
        })

    context = {'ranked_quotes': ranked_quotes}
    return render(request, 'base/best_quotes.html', context)


# Добавить цитату
def add_quote(request):
    return render(request, 'base/add_quote.html')