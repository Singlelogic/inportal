from django.urls import path

from .views import (
    CommentDeleteView, CommentUpdateView,
    PostCreateView, PostDeleteView, PostDetailView, PostListView, PostUpdateView,
    TagCreateView, TagListView, TagDetailView, TagDelete, TagUpdateView,
    TagDeleteInPost,
)


urlpatterns = [
    path('', PostListView.as_view(), name='post_list_url'),
    path('post/create/', PostCreateView.as_view(), name='post_create_url'),
    path('post/<slug>/', PostDetailView.as_view(), name='post_detail_url'),
    path('post/<slug>/update/', PostUpdateView.as_view(), name='post_update_url'),
    path('post/<slug>/delete/', PostDeleteView.as_view(), name='post_delete_url'),
    path('tags/', TagListView.as_view(), name='tag_list_url'),
    path('tag/create/', TagCreateView.as_view(), name='tag_create_url'),
    path('tag/<slug>/', TagDetailView.as_view(), name='tag_detail_url'),
    path('tag/<slug>/update/', TagUpdateView.as_view(), name='tag_update_url'),
    path('tag/<slug>/delete/', TagDelete.as_view(), name='tag_delete_url'),
    path('post/<post_id>/<tag_id>/', TagDeleteInPost.as_view(), name='tag_delete_in_post'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment_update_url'),
    path('comment/<int:pk>/delete', CommentDeleteView.as_view(), name='comment_delete_url'),
]
