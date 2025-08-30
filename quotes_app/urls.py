from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home_page, name="home"),                               # Домашняя страница (home.html)
    path('best_quotes/', views.the_best_quotes, name="the_best_quotes"),  # Топ 10 цитат по лайкам (best_quotes.html)
    path('login/', views.loginPage, name="login"),                        # Вход
    path('logout/', views.logoutUser, name="logout"),                     # Выход
    path('register/', views.registerPage, name="register"),               # Регистрация
    path('like/<int:quote_id>/', views.like_quote, name="like_quote"),
    path('dislike/<int:quote_id>/', views.dislike_quote, name="dislike_quote"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)