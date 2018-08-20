import asyncio

from django.shortcuts import render

from .utils import memoize
from .api_handler import get_all_movies_and_artists

@memoize
def get_movies_list(request):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    all_movies_data, artists_data = loop.run_until_complete(get_all_movies_and_artists())

    response = render(request, 'index.html', {'movies': all_movies_data, 'artists': artists_data})
    response['Cache-Control'] = 'max-age=60'
    return response
