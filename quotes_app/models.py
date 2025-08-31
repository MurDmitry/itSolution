from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User


class Source(models.Model):
    """
    Модель Источники:
    1. id: Идентификатор. Автоинкрементное поле. Создается автоматически. PK
    2. source_type: Тип источника. Выбор из списка. Обязательное поле (Not null). По умолчанию "Другое"
    3. title: Название источника. Обязательное поле (Not null)
    4. author: Автор / режиссёр. Поле может быть пустым
    5. year: Год выпуска. Поле может быть пустым
    """

    # Типы источника
    SOURCE_TYPES = [
        ('movie', 'Фильм'),
        ('book', 'Книга'),
        ('series', 'Сериал'),
        ('game', 'Игра'),
        ('other', 'Другое'),
    ]
    source_type = models.CharField(
        max_length=20,
        choices=SOURCE_TYPES,
        default='other',
        verbose_name="Тип источника"
    )
    title = models.CharField(max_length=200, verbose_name="Название источника")
    author = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="Автор/Режиссер")
    year = models.IntegerField(
        null=True, blank=True, verbose_name="Год выпуска")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.author and self.year:                             # Указан автор и год
            return f"{self.title} ({self.author}, {self.year})"
        elif self.author:                                         # Указан только автор
            return f"{self.title} ({self.author})"
        elif self.year:                                           # Указан только год
            return f"{self.title} ({self.year})"
        else:                                                     # Без автора и года
            return self.title


class Quote(models.Model):
    """
    Модель Цитаты:
    1. id: Идентификатор. Автоинкрементное поле. Создается автоматически. PK
    2. text: Текст цитаты. Обязательное поле (Not null)
    3. author: Автор цитаты. Необязательное поле
    4. source: Источник. FK (Source). Обязательное поле (Not null)
    5. weight: Вес цитаты. Значение по умолчанию = 1
    6. views_count: Количество просмотров. Значение по умолчанию = 0
    7. likes: Количество лайков . Значение по умолчанию = 0
    8. dislikes: Количество дизлайков. Значение по умолчанию = 0
    """

    text = models.TextField(verbose_name="Текст цитаты")
    source = models.ForeignKey(
        Source,
        on_delete=models.CASCADE,
        related_name='quotes',
        verbose_name="Источник"
    )
    author = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="Автор цитаты")
    weight = models.PositiveIntegerField(
        default=1,
        verbose_name="Вес цитаты",
        help_text="Чем выше вес, тем больше шанс показа цитаты",
        validators=[
            MinValueValidator(1),   # Минимальное значение = 1
            MaxValueValidator(100)  # Максимальное значение = 100
        ]
    )
    views_count = models.PositiveIntegerField(
        default=0, verbose_name="Количество просмотров")
    likes = models.PositiveIntegerField(default=0, verbose_name="Лайки")
    dislikes = models.PositiveIntegerField(default=0, verbose_name="Дизлайки")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Связь с пользователем для хранения лайков и дизлайков
    liked_by = models.ManyToManyField(User, related_name='liked_quotes', blank=True)
    disliked_by = models.ManyToManyField(User, related_name='disliked_quotes', blank=True)

    def toggle_like(self, user):
        """Добавить или убрать лайк для цитаты для пользователя"""
        if user in self.liked_by.all():             # Проверка: есть ли пользователь в списке лайнувших
            self.liked_by.remove(user)              # Если да (т.е. лайкнул до этого) - убираю лайк
            self.likes = self.liked_by.count()      # Синхронизация с количеством
        else:
            self.liked_by.add(user)                 # Иначе ставлю лайк
            self.likes = self.liked_by.count()      # Синхронизация с количеством
            if user in self.disliked_by.all():      # Если он дизлайнул, то теперь к лайкам +1, а к дизлайкам -1 
                self.disliked_by.remove(user)
                self.dislikes = self.disliked_by.count()

    def toggle_dislike(self, user):
        """Добавить или убрать дизлайк для цитаты для пользователя"""
        if user in self.disliked_by.all():
            self.disliked_by.remove(user)
            self.dislikes = self.disliked_by.count()
        else:
            self.disliked_by.add(user)
            self.dislikes = self.disliked_by.count()
            if user in self.liked_by.all():
                self.liked_by.remove(user)
                self.likes = self.liked_by.count()
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        likes_count = self.liked_by.count()
        dislikes_count = self.disliked_by.count()
        
        updated = False
        if self.likes != likes_count:
            self.likes = likes_count
            updated = True
        if self.dislikes != dislikes_count:
            self.dislikes = dislikes_count
            updated = True
        
        if updated:
            super().save(update_fields=['likes', 'dislikes'])

    def __str__(self):
        # Начало цитаты и источник
        return f"{self.text[:50]}... ({self.source.title})"
