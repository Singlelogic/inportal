from django import forms
from django.core.exceptions import ValidationError

from .models import Comment, Post, Tag
from .utils import is_ru


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['title']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_title(self):
        new_title = self.cleaned_data['title'].lower()
        en_new_slug = is_ru(new_title)

        if new_title == 'create':
            raise ValidationError("Тэг не может быть - 'Create'")
        elif Tag.objects.filter(title__iexact=new_title).count():
            raise ValidationError("Тэг '{}' уже существует".format(new_title))
        elif Tag.objects.filter(slug__iexact=en_new_slug).count():
            raise ValidationError("Тэг '{}' уже существует, попробуйте найти его в латинице".format(new_title))
        return new_title


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'image_preview', 'tags', 'body']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'})
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }
