from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


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
    author = models.CharField(max_length=100, null=True, blank=True, verbose_name="Автор/Режиссер")
    year = models.IntegerField(null=True, blank=True, verbose_name="Год выпуска")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Quote(models.Model):
    """
    Модель Цитаты:
    1. id: Идентификатор. Автоинкрементное поле. Создается автоматически. PK
    2. text: Текст цитаты. Обязательное поле (Not null)
    3. source: Источник. FK (Source). Обязательное поле (Not null)
    4. weight: Вес цитаты. Значение по умолчанию = 1
    5. views_count: Количество просмотров. Значение по умолчанию = 0
    6. likes: Количество лайков . Значение по умолчанию = 0
    7. dislikes: Количество дизлайков. Значение по умолчанию = 0
    """

    text = models.TextField(verbose_name="Текст цитаты")
    source = models.ForeignKey(
        Source,
        on_delete=models.CASCADE,
        related_name='quotes',
        verbose_name="Источник"
    )
    weight = models.PositiveIntegerField(
        default=1,
        verbose_name="Вес цитаты",
        help_text="Чем выше вес, тем больше шанс показа цитаты",
        validators=[
            MinValueValidator(1),   # Минимальное значение = 1
            MaxValueValidator(100)  # Максимальное значение = 100
        ]
    )
    views_count = models.PositiveIntegerField(default=0, verbose_name="Количество просмотров")
    likes = models.PositiveIntegerField(default=0, verbose_name="Лайки")
    dislikes = models.PositiveIntegerField(default=0, verbose_name="Дизлайки")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
