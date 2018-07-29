import re
import asyncio

from django.shortcuts import render
from aiohttp import ClientSession

from .utils import memoize


API_ENDPOINT = 'https://ghibliapi.herokuapp.com/{}{}'
MOVIES_ENDPOINT = API_ENDPOINT.format('films', '')
PEOPLE_PATTERN = re.compile('people/[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89aAbB][a-f0-9]{3}-[a-f0-9]{12}')


async def update_artists_data(artists_urls, artists_data):
    """Update artists_data with key as artist's url and key as artist's name."""

    async with ClientSession() as session:
        for artist_url in artists_urls:
            if artist_url not in artists_data:
                # do not request data for same persons
                async with session.get(artist_url) as response:
                    json_data = await response.json()
                    artists_data[artist_url] = json_data['name']

async def get_movies_data():
    async with ClientSession() as session:
        async with session.get(MOVIES_ENDPOINT) as response:
            return await response.json()


@memoize
def movies_list(request):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    # fetch top 20 movies
    all_movies = loop.run_until_complete(get_movies_data())

    # prepare list of all people links
    all_people_urls = []
    for movie in all_movies:
        for artist in movie['people']:
            if PEOPLE_PATTERN.search(artist):
                all_people_urls.append(artist)
    
    # fetch all peoples data
    artists_data = {}
    loop.run_until_complete(update_artists_data(all_people_urls, artists_data))

    # replace people url with data
    for movie in all_movies:
        movie['people_data'] = []
        for people in movie['people']:
            if people in artists_data:
                movie['people_data'].append(artists_data[people])

    response = render(request, 'index.html', {'movies': all_movies})
    response['Cache-Control'] = 'max-age=60'
    return response
