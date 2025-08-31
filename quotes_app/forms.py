from django import forms
from .models import Quote, Source
from django.core.exceptions import ValidationError


# Форма Цитата (Указываю какие поля)
class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = ['text', 'author', 'weight', 'source']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Введите текст цитаты',
                'rows': 4
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Автор цитаты'
            }),
            'weight': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 100
            }),
            'source': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'text': 'Текст цитаты*',
            'author': 'Автор цитаты',
            'weight': 'Вес цитаты (1-100)*',
            'source': 'Источник*',
        }

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get('text')
        source = cleaned_data.get('source')

        if not text or not source:
            # Если обязательные поля не заполнены - нет смысла дальше проверять
            return cleaned_data

        # Проверка на дубликат цитаты у того же источника
        duplicate = Quote.objects.filter(text=text.strip(), source=source)
        if self.instance.pk:
            duplicate = duplicate.exclude(pk=self.instance.pk)
        if duplicate.exists():
            raise ValidationError('Такая цитата уже существует для данного источника.')

        # Проверка на максимум 3 цитаты у источника
        count_quotes = Quote.objects.filter(source=source).count()
        if not self.instance.pk and count_quotes >= 3:
            raise ValidationError('Нельзя добавлять более 3 цитат для одного источника.')

        return cleaned_data

    

# Форма Источник (указываю какие поля)
class SourceForm(forms.ModelForm):
    class Meta:
        model = Source
        fields = ['source_type', 'title', 'author', 'year']
        widgets = {
            'source_type': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название источника'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Автор/Режиссер'}),
            'year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Год выпуска'}),
        }
        labels = {
            'source_type': 'Тип источника',
            'title': 'Название*',
            'author': 'Автор/Режиссер',
            'year': 'Год выпуска',
        }