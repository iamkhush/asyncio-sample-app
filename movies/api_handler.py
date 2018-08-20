import re
import asyncio

from aiohttp import ClientSession

API_ENDPOINT = 'https://ghibliapi.herokuapp.com/{}{}'
MOVIES_ENDPOINT = API_ENDPOINT.format('films', '')
ARTIST_PATTERN = re.compile('people/[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89aAbB][a-f0-9]{3}-[a-f0-9]{12}')


async def get_artist_data(session, artist_url, all_artists_data):
    async with session.get(artist_url) as response:
        return await response.json()


async def get_all_artists_data(all_movies):
    all_artists_data = {}
    async with ClientSession() as session:
        for movie_data in all_movies:
            for artist_url in movie_data['people']:
                if ARTIST_PATTERN.search(artist_url) and artist_url not in all_artists_data:
                    all_artists_data[artist_url] = await get_artist_data(
                        session, artist_url, all_artists_data)
    return all_artists_data


async def get_all_movies_and_artists():
    async with ClientSession() as session:
        async with session.get(MOVIES_ENDPOINT) as response:
            all_movies = await response.json()
            all_artists = await get_all_artists_data(all_movies)
            return all_movies, all_artists