from django import forms
from .models import Comment


# Указываем класс формы
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # Мы будем работать со всеми полями
        fields = ['message', 'user', 'lesson']

        # При этом поля user и lesson отображать на странице мы не будем
        widgets = {'user': forms.HiddenInput(), 'lesson': forms.HiddenInput()}
