from django.contrib.auth.views import PasswordChangeView
from django.urls import path, include

from .views import HomepageView, AnimeDetailView, AddReview, AddLike, SearchView, register_request, login_request, \
    delete_user, logout_request, AnimeListView, ProfileView, CommunicationCreateView

app_name = 'main'

urlpatterns = [
    path('contacts/', CommunicationCreateView.as_view(), name='contacts'),
    path('profile/delete/', delete_user, name='delete_user'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('search/', SearchView.as_view(), name='search'),
    path('selection/<slug:slug>/', AnimeListView.as_view(), name='selection'),
    path('change_password/',
         PasswordChangeView.as_view(template_name='main/change-password.html', success_url='/'),
         name='change_password'),
    path('logout/', logout_request, name='logout'),
    path('login/', login_request, name='login'),
    path('register/', register_request, name='register'),
    path('add_like/<slug:slug>/', AddLike.as_view(), name='add_like'),
    path('add_review/<slug:slug>', AddReview.as_view(), name='add_review'),
    path('anime_detail/<slug:slug>/', AnimeDetailView.as_view(), name='anime_detail'),
    path('', HomepageView.as_view(), name='homepage'),
]
