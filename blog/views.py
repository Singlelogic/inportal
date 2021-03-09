from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from .forms import CommentForm, TagForm, PostForm
from .models import Comment, Post, Tag


class PostCreateView(LoginRequiredMixin, CreateView):
    """Create a post."""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_create.html'

    def form_valid(self, form):
        """Adding an author to a post."""
        post = form.instance
        post.user = self.request.user
        return super().form_valid(form)


class PostListView(LoginRequiredMixin, ListView):
    """List of posts."""
    paginate_by = 3

    def get_queryset(self):
        """Getting posts by title and body, if a search was requested."""
        search_query = self.request.GET.get('search', '')
        if search_query:
            posts = Post.objects.filter(Q(title__icontains=search_query) |
                                        Q(body__icontains=search_query))
        else:
            posts = Post.objects.all()
        return posts


class PostDetailView(LoginRequiredMixin, View):
    """Dispaling a specific post."""
    def get(self, request, slug):
        obj = get_object_or_404(Post, slug__iexact=slug)
        comments = obj.comments.all()
        comment_form = CommentForm()
        tags = obj.tags.all()
        return render(request, 'blog/post_detail.html', context={
            'post': obj,
            'admin_object': obj,
            'detail': True,
            'comments': comments,
            'comment_form': comment_form,
            'tags': tags,
        })

    def post(self, request, slug):
        obj = get_object_or_404(Post, slug__iexact=slug)
        comments = obj.comments.all()
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = obj
            new_comment.user = request.user
            new_comment.save()
            comment_form = CommentForm()
            tags = obj.tags.all()
        return render(request, 'blog/post_detail.html', context={
            'post': obj,
            'admin_object': obj,
            'detail': True,
            'comments': comments,
            'comment_form': comment_form,
            'tags': tags,
        })


class PostUpdateView(LoginRequiredMixin, UpdateView):
    """Update a post."""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_update.html'


class PostDeleteView(LoginRequiredMixin, DeleteView):
    """Delete a post."""
    model = Post
    template_name = 'blog/post_delete.html'
    success_url = reverse_lazy('post_list_url')


class TagCreateView(LoginRequiredMixin, CreateView):
    """Create a tag."""
    model = Tag
    form_class = TagForm
    template_name = 'blog/tag_create.html'
    success_url = reverse_lazy('post_list_url')
    raise_exception = True


class TagListView(LoginRequiredMixin, ListView):
    """List of tags."""
    model = Tag


class TagDetailView(LoginRequiredMixin, ListView):
    """Output of posts of a specific tag."""
    template_name = 'blog/post_list.html'
    paginate_by = 3

    def get_queryset(self):
        """Selecting posts by tag."""
        tag = Tag.objects.get(slug=self.kwargs.get('slug'))
        return tag.posts.all()


class TagUpdateView(LoginRequiredMixin, UpdateView):
    """Update a tag"""
    model = Tag
    form_class = TagForm
    template_name = 'blog/tag_update.html'
    raise_exception = True


class TagDelete(LoginRequiredMixin, DeleteView):
    """Delete a tag."""
    model = Tag
    template_name = 'blog/tag_delete.html'
    success_url = reverse_lazy('tag_list_url')
    raise_exception = True


class TagDeleteInPost(LoginRequiredMixin, View):
    """Delete a tag in a post."""
    def get(self, request, post_id, tag_id):
        post = get_object_or_404(Post, id=post_id)
        tag = get_object_or_404(Tag, id=tag_id)
        return render(request, 'blog/tag_delete_in_post.html', context={
            'post': post,
            'tag': tag,
        })

    def post(self, request, post_id, tag_id):
        post = get_object_or_404(Post, id=post_id)
        tag = get_object_or_404(Tag, id=tag_id)
        post.tags.remove(tag)
        return HttpResponseRedirect(reverse('post_detail_url',
                                            kwargs={'slug': post.slug}))


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    """Update a comment."""
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_update.html'
    raise_exception = True
    success_url = reverse_lazy('post_list_url')

    def get_success_url(self):
        """Getting the url of the post in which this comment belongs."""
        comment = Comment.objects.get(pk=self.kwargs['pk'])
        success_url = reverse('post_detail_url', kwargs={'slug': comment.post.slug})
        return success_url


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    """Delete a comment."""
    model = Comment
    template_name = 'blog/comment_delete.html'
    raise_exception = True

    def get_success_url(self):
        """Getting the url of the post in which this comment belongs."""
        comment = Comment.objects.get(pk=self.kwargs['pk'])
        return comment.get_post_url()
