from django.urls import path
from .views import *
from Users.views import messages, new_message

app_name = 'blogapp'

urlpatterns = [
    path("", home, name='Home'),
    path('posts/', posts, name='Posts'),
    path('posts/list/', PostList.as_view(), name='PostsList'),
    path('post/<pk>', PostDetail.as_view(), name='PostDetail'),
    path('post/delete/<pk>', PostDelete.as_view(), name='PostDelete'),
    path('post_form/', postForm, name='PostForm'),
    path('post/edit/<post_id>/', editPost, name='EditPost'),

    path('inbox/', messages, name='Messages'),
    path('inbox/new_msg/', new_message, name='NewMessage'),
]