import os

from django.db import models
from django.urls import reverse_lazy
from django.utils.crypto import get_random_string


def generate_slug():
    return get_random_string(26)

def get_upload_path(instance, filename):
    return 'blog/' + os.path.join(instance.url, filename)


class Post(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    preview = models.ImageField(upload_to=get_upload_path)
    content_img = models.ImageField('Content image', upload_to=get_upload_path, blank=True)
    visible_date = models.DateField()
    tags = models.ManyToManyField('Tag')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    url = models.SlugField(unique=True, default=generate_slug)
    draft = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created_at',)

    def get_absolute_url(self):
        return reverse_lazy('blog:post_details', kwargs={'slug': self.url})

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=30)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.title

