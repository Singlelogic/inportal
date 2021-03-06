from django.urls import path

from .views import (
    PostCreateView, PostDeleteView, PostDetailView, PostListView, PostUpdateView,
    TagCreateView, TagListView, TagDetailView, TagDelete, TagUpdateView,
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
    path('tag/<slug>/delete/', TagDelete.as_view(), name='tag_delete_url')
]
