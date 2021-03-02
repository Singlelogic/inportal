from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from .forms import CommentForm, TagForm, PostForm
from .models import Comment, Post, Tag
from .mixins import (
    OblectCreateMixin, ObjectUpdateMixin, ObjectDeleteMixin
)
from .utils import paginator


class PostDetail(View):

    def get(self, request, slug):
        obj = get_object_or_404(Post, slug__iexact=slug)
        comments = obj.comments.filter(active=True)
        comment_form = CommentForm()
        return render(request, 'blog/post_detail.html', context={
            'post': obj,
            'admin_object': obj,
            'detail': True,
            'comments': comments,
            'comment_form': comment_form,
        })

    def post(self, request, slug):
        obj = get_object_or_404(Post, slug__iexact=slug)
        comments = obj.comments.filter(active=True)
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = obj
            # Save the comment to the database
            new_comment.save()
            comment_form = CommentForm()

        return render(request, 'blog/post_detail.html', context={
            'post': obj,
            'comments': comments,
            'comment_form': comment_form,
        })


class PostCreate(LoginRequiredMixin, OblectCreateMixin, View):
    model_form = PostForm
    template = 'blog/post_create.html'
    raise_exception = True


class PostUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Post
    model_form = PostForm
    template = 'blog/post_update_form.html'
    raise_exception = True


class PostDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Post
    template = 'blog/post_delete_form.html'
    redirect_url = 'posts_list_url'
    raise_exception = True


def posts_list(request):
    search_query = request.GET.get('search', '')
    if search_query:
        posts = Post.objects.filter(Q(title__icontains=search_query) |
                                    Q(body__icontains=search_query))
    else:
        posts = Post.objects.all()

    page, is_paginated = paginator(request, posts)
    return render(request, 'blog/index.html', context={
        'page_object': page,
        'is_paginated': is_paginated
    })


class TagDetail(View):
    def get(self, request, slug):
        obj = get_object_or_404(Tag, slug__iexact=slug)
        posts = obj.posts.all()
        page, is_paginated = paginator(request, posts)
        return render(request, 'blog/index.html', context={
            'detail': True,
            'admin_object': obj,
            'page_object': page,
            'is_paginated': is_paginated,
            'title': obj.title,
        })


class TagCreate(LoginRequiredMixin, OblectCreateMixin, View):
    model_form = TagForm
    template = 'blog/tag_create.html'
    raise_exception = True


class TagUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Tag
    model_form = TagForm
    template = 'blog/tag_update_form.html'
    raise_exception = True


class TagDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Tag
    template = 'blog/tag_delete_form.html'
    redirect_url = 'tags_list_url'
    raise_exception = True


def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'blog/tags_list.html', context={'tags': tags})
