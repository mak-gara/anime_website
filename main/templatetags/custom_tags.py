from django import template

from ..models import Anime, Review
from ..services import is_fan
from ..views import get_views_count_for_period

register = template.Library()


@register.inclusion_tag('components/like-button.html')
def like_button(obj, user):
    return {'state': is_fan(obj, user), 'anime_slug': obj.url}


@register.inclusion_tag('components/sidebar.html')
def sidebar():
    items = Anime.objects.filter(draft=False)

    # getting 4 anime with new comments
    anime = []
    for comment in Review.objects.all():
        if (comment.anime.draft == False) and (comment.anime not in anime):
            anime.append(comment.anime)
        if len(anime) == 4:
            break
    new_comments = anime

    return {
        'top_day': items.annotate(views_day=get_views_count_for_period(1)).order_by('-views_day')[:5],
        'top_week': items.annotate(views_week=get_views_count_for_period(7)).order_by('-views_week')[:5],
        'top_month': items.annotate(views_month=get_views_count_for_period(30)).order_by('-views_month')[:5],
        'top_year': items.annotate(views_year=get_views_count_for_period(365)).order_by('-views_year')[:5],
        'new_comments': new_comments
    }


@register.inclusion_tag('components/anime-card.html')
def anime_card(item):
    return {'item': item}


@register.inclusion_tag('components/pagination.html')
def pagination(page_obj):
    return {'page_obj': page_obj}

@register.filter
def queryset_to_string(queryset):
    titles = [item.title for item in queryset[:2]]
    return ', '.join(titles)
