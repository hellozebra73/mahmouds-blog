from django.urls import path
from . import views


urlpatterns = [
    path('', views.posts, name='posts'),
    path('posts', views.posts, name='posts'),
    path('create', views.create, name='create'),
    path('create/<int:id>', views.create, name='create'),
    path('submit', views.submitPost, name='submit'),
    path('deletePost', views.deletePost, name='delete'),
]


