from django.urls import path

from .views import PostListView, PostDetailView

app_name = 'blog'

urlpatterns = [
    path('post_details/<slug:slug>/', PostDetailView.as_view(), name='post_details'),
    path('', PostListView.as_view(), name='posts')
]
