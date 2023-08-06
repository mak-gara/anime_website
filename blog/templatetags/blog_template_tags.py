from django import template

register = template.Library()

@register.inclusion_tag('components/tiles.html')
def tiles(queryset, mode='direct'):
    context = {'big_cards_indexes': [],
               'queryset': queryset}
    if mode == 'direct':
        context['big_cards_indexes'] = list(range(0, len(queryset), 3))
    elif mode == 'reverso':
        context['big_cards_indexes'] = list(range(2, len(queryset), 3))
    return context