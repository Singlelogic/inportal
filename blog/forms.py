from django import forms
from django.core.exceptions import ValidationError

from .models import Comment, Post, Tag


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['title']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()

        if new_slug == 'create':
            raise ValidationError('Slug may not be "Create"')
        if Tag.objects.filter(slug__iexact=new_slug).count():
            raise ValidationError('We have "{}" slug already'.format(new_slug))
        return new_slug


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
