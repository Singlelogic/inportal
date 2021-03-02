from django.urls import path

from .views import (
    PostCreate, PostDelete, PostDetail, posts_list, PostUpdate,
    TagCreate, TagDelete, TagDetail, tags_list, TagUpdate,
)


urlpatterns = [
    path('', posts_list, name='posts_list_url'),
    path('post/create/', PostCreate.as_view(), name='post_create_url'),
    path('post/<slug>/', PostDetail.as_view(), name='post_detail_url'),
    path('post/<slug>/update/', PostUpdate.as_view(), name='post_update_url'),
    path('post/<slug>/delete/', PostDelete.as_view(), name='post_delete_url'),
    path('tags/', tags_list, name='tags_list_url'),
    path('tag/create/', TagCreate.as_view(), name='tag_create_url'),
    path('tag/<slug>/', TagDetail.as_view(), name='tag_detail_url'),
    path('tag/<slug>/update/', TagUpdate.as_view(), name='tag_update_url'),
    path('tag/<slug>/delete/', TagDelete.as_view(), name='tag_delete_url')
]
