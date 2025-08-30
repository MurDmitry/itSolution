from django import forms
from .models import Quote, Source


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