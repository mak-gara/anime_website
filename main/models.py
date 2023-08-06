import os.path

from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from django.urls import reverse_lazy

from django.utils.crypto import get_random_string


def generate_slug():
    return get_random_string(26)


def get_anime_img_upload_path(instance, filename):
    print(instance.url)
    return 'anime/' + os.path.join(instance.url, filename)


class Anime(models.Model):
    title = models.CharField(max_length=70, unique=True)
    english_title = models.CharField(max_length=70, blank=True, null=True)
    japanese_title = models.CharField(max_length=70)
    description = models.TextField()
    date_aired = models.CharField(max_length=50)
    age_rating = models.PositiveSmallIntegerField(default=16,
                                                  validators=[MaxValueValidator(18, message='Maximum age rating 18+')])
    duration = models.CharField(max_length=25)
    episodes = models.PositiveSmallIntegerField(
        default=1, validators=[MinValueValidator(1)])

    type = models.ForeignKey(
        'Category', related_name='anime_by_type', on_delete=models.SET_NULL, null=True)
    source = models.ForeignKey(
        'Category', related_name='anime_by_source', on_delete=models.SET_NULL, null=True)
    studios = models.ManyToManyField(
        'Category', related_name='anime_by_studio')
    licensors = models.ManyToManyField(
        'Category', related_name='anime_by_licensor')
    producers = models.ManyToManyField(
        'Category', related_name='anime_by_producer')
    genres = models.ManyToManyField('Category', related_name='anime_by_genre')
    themes = models.ManyToManyField('Category', related_name='anime_by_theme')

    poster = models.ImageField(
        upload_to=get_anime_img_upload_path, help_text='230x325px', blank=True)
    comment_img = models.ImageField(
        upload_to=get_anime_img_upload_path, help_text='90x130px', blank=True)
    top_views_img = models.ImageField(
        upload_to=get_anime_img_upload_path, help_text='350x190px', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reviews = GenericRelation('Review')
    views = models.ManyToManyField('Ip', related_name='views', blank=True)
    likes = GenericRelation('Like')
    url = models.SlugField(unique=True, default=generate_slug)
    draft = models.BooleanField(default=False)

    
    def get_absolute_url(self):
        return reverse_lazy('main:anime_detail', kwargs={'slug': self.url})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Anime'
        ordering = ('-created_at',)


class Category(models.Model):
    title = models.CharField(max_length=70, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Categories'


# dynamic file path, model "AnimeFrame", field "frame"
def get_upload_path(instance, filename):
    return 'frames/' + os.path.join(instance.anime.slug, filename)


class Review(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    anime = models.ForeignKey(
        Anime, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField(max_length=300)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.anime.title

    class Meta:
        ordering = ('-created_at',)


class ImageSlider(models.Model):
    anime = models.OneToOneField(Anime, on_delete=models.CASCADE)
    quote = models.CharField(max_length=70)
    image = models.ImageField(upload_to='slider', help_text='1172x564px')

    def __str__(self):
        return self.anime.title

    class Meta:
        verbose_name = 'Slide'


class Like(models.Model):
    user = models.ForeignKey(
        'CustomUser', related_name='likes', on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f'User:{self.user.username}, ContentType:{self.content_type}'


class Ip(models.Model):
    ip = models.CharField('IP', max_length=45)
    request_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.ip

    class Meta:
        verbose_name = 'IP'
        verbose_name_plural = 'IP addresses'


class CustomUser(AbstractUser):
    profile_pic = models.ImageField(upload_to='profile', blank=True)

    class Meta(AbstractUser.Meta):
        pass

    def __str__(self):
        return self.username


class Communication(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Message'
        ordering = ('sent_at',)

    def __str__(self):
        return self.name
