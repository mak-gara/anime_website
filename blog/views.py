from django import forms
from django.views.generic import ListView, DetailView

from .models import Post

class PostListView(ListView):
    model = Post
    template_name = 'blog/post-list.html'
    context_object_name = 'posts'
    paginate_by = 6
    queryset = Post.objects.filter(draft=False)

class PostDetailView(DetailView):
    model = Post
    slug_field = 'url'
    template_name = 'blog/post-details.html'
    context_object_name = 'post'

