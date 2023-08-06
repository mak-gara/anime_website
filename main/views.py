from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from django.db.models import Count, Q
from django.views import View
from django.views.generic import TemplateView, DetailView, ListView, CreateView
from django.contrib.contenttypes.models import ContentType

from common.util.utilities import get_client_ip

from .models import Anime, ImageSlider, CustomUser, Communication
from .forms import ReviewForm, NewUserForm, EditProfileForm, ContactForm
from .services import is_fan, remove_like, add_like


def get_views_count_for_period(period):
    current_datetime = timezone.now()
    return Count('views', filter=Q(views__request_date__gte=current_datetime + timedelta(days=-period)))


class HomepageView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Anime - Homepage'
        anime = Anime.objects.filter(draft=False)
        context['trends'] = anime.annotate(views_three_day=get_views_count_for_period(3)).order_by(
            '-views_three_day')[:6]
        context['popular'] = anime.annotate(views_count=Count('views')).order_by(
            '-views_count')[:6]
        context['recent'] = anime[:6]
        context['slides'] = ImageSlider.objects.all()

        return context


class AnimeDetailView(DetailView):
    model = Anime
    template_name = 'main/anime-details.html'
    slug_field = 'url'
    context_object_name = 'anime'

    def get_object(self, queryset=None):
        object = super().get_object()
        ip = get_client_ip(self.request)
        object.views.update_or_create(
            ip=ip, defaults={'request_date': timezone.now()})
        return object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['might_like'] = Anime.objects.filter(
            Q(genres__in=context['anime'].genres.all(), draft=False) & ~Q(title=context['anime'].title)).distinct()[:4]
        return context


class AddReview(LoginRequiredMixin, View):
    login_url = 'login'

    def post(self, request, slug):
        form = ReviewForm(request.POST)    
        anime = Anime.objects.get(url=slug)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.anime = anime
            form.save()
            messages.success(request, 'Comment added')
        else:
            messages.error(request, 'Form is not valid')
        return redirect(anime.get_absolute_url())


class AddLike(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, slug):
        obj = get_object_or_404(Anime, url=slug)
        if is_fan(obj, request.user):
            remove_like(obj, request.user)
        else:
            add_like(obj, request.user)
        return redirect(obj.get_absolute_url())


def register_request(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful')
            return redirect('/')
        messages.error(
            request, 'Unsuccessful registration. Invalid information.')
    if request.user.is_authenticated:
        messages.info(request, 'You are already registered')
        return redirect('/')
    return render(request, template_name='main/signup.html')


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('/')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    if request.user.is_authenticated:
        messages.info(request, 'You are already logined')
        return redirect('/')
    return render(request, template_name='main/login.html')


@login_required
def logout_request(request):
    logout(request)
    messages.info(request, 'You have successfully logged out.')
    return redirect('/')


@login_required
def delete_user(request):
    try:
        user = CustomUser.objects.get(username=request.user.username)
        user.delete()
        messages.success(request, 'The user is deleted')
        return redirect('homepage')
    except:
        messages.error(request, 'An error occurred while deleting a user')
        return redirect('profile')


class AnimeListView(ListView):
    model = Anime
    template_name = 'main/selection.html'
    paginate_by = 18
    context_object_name = 'anime'

    def get_queryset(self):
        if self.kwargs.get('slug'):
            slug = self.kwargs.get('slug')
            anime = Anime.objects.filter(draft=False)

            current_datetime = timezone.now()

            def get_views_count(period):
                return Count('views', filter=Q(views__request_date__gte=current_datetime + timedelta(days=-period)))

            match slug:
                case 'trends':
                    self.extra_context = {'title': 'Trending Now'}
                    qs = anime.annotate(views_three_day=get_views_count(
                        3)).order_by('-views_three_day')
                case 'popular':
                    self.extra_context = {'title': 'Popular Shows'}
                    qs = anime.annotate(views_count=Count(
                        'views')).order_by('-views_count')
                case 'recently_added':
                    self.extra_context = {'title': 'Recently Added Shows'}
                    qs = anime

            return qs


class SearchView(ListView):
    model = Anime
    template_name = 'main/selection.html'
    context_object_name = 'anime'

    def get_queryset(self):
        query = self.request.GET.get("query")
        self.extra_context = {'title': f'Search Query - {query}'}
        qs = Anime.objects.filter(
            Q(title__icontains=query) | Q(english_title__icontains=query) | Q(japanese_title__icontains=query))
        return qs


class ProfileView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        queryset = Anime.objects.filter(likes__user=request.user)
        return render(request, 'main/profile.html', context={'anime': queryset})

    def post(self, request):
        form = EditProfileForm(
            request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            # print(form.profile_pic)
            form.save()
            return redirect('profile')
        return redirect('/')


class CommunicationCreateView(SuccessMessageMixin, CreateView):
    model = Communication
    template_name = 'main/contacts.html'
    form_class = ContactForm
    success_url = '/'
    success_message = 'Your message was sent, thank you!'
