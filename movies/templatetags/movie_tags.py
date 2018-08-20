from django import template

register = template.Library()


@register.simple_tag
def get_artist_data(artists, artist_url, attr, default=''):
    if artist_url in artists:
        return artists[artist_url].get(attr, default)
    return 'NA'
