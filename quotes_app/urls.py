from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_page, name="home"),                           # Домашняя страница
    path('top_quotes', views.the_best_quotes, name="the_best_quotes") # Топ 10 цитат по лайкам
]