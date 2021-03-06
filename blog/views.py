from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from .forms import CommentForm, TagForm, PostForm
from .models import Post, Tag


class PostCreateView(LoginRequiredMixin, CreateView):
    """Create a post."""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_create.html'


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


# class PostDetailView(LoginRequiredMixin, TemplateView):
#     """Dispaling a specific post."""
#     # model = Post
#     template_name = 'blog/post_detail.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         post = get_object_or_404(Post, slug=context['slug'])
#         context['post'] = post
#         comments = post.comments.all()
#         context['comments'] = comments
#         context['comment_form'] = CommentForm()
#         return context


class PostDetailView(LoginRequiredMixin, View):
    """Dispaling a specific post."""
    def get(self, request, slug):
        obj = get_object_or_404(Post, slug__iexact=slug)
        comments = obj.comments.all()
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
        comments = obj.comments.all()
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = obj
            new_comment.user = request.user
            new_comment.save()
            comment_form = CommentForm()
        return render(request, 'blog/post_detail.html', context={
            'post': obj,
            'comments': comments,
            'comment_form': comment_form,
        })


class PostUpdateView(LoginRequiredMixin, UpdateView):
    """Update a post."""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_update.html'


# class PostDeleteView(LoginRequiredMixin, View):
#     """Deleting a post directly from the database."""
#     def get(self, request, pk):
#         return render(request, 'blog/post_delete.html', context={
#             'pk': pk,
#         })
#
#     def post(self, request, pk):
#         with connection.cursor() as cursor:
#             cursor.execute(
#                 dedent('''\
#                     delete from blog_post_tags
#                     where post_id=%s;'''),
#                 [ pk ]
#             )
#             cursor.execute(
#                 dedent('''\
#                     delete from blog_post
#                     where id=%s;'''),
#                 [ pk ]
#             )
#         return HttpResponseRedirect(reverse('post_list_url'))


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
        print(f"slug: {self.kwargs.get('slug')}")
        tag = Tag.objects.get(title=self.kwargs.get('slug'))
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
