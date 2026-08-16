from django.urls import path
from .views import (
    PostListView, PostDetailView, PostCreateView,
    CategoryCreateView, PostDeleteView
)

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/create/', PostCreateView.as_view(), name='post_create'),
    path('category/create/', CategoryCreateView.as_view(), name='category_create'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
]
