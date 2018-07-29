import asyncio

from django.test import Client
from aiohttp.client import ClientResponse
from asynctest import TestCase, patch, mock

from .views import update_artists_data


class MoviesListTest(TestCase):

    async def artists_json_response(*args):
        return {'name': 'artist_name'}
    
    async def test_update_artists_data(self):
        artists_data = {}
        response = mock.Mock()
        response.json = self.artists_json_response
        with patch("aiohttp.client.ClientSession._request", return_value=response) as patched:
            await update_artists_data(['http://example.com'], artists_data)
        assert artists_data == {'http://example.com': 'artist_name'}

    async def film_json_response(*args, **kwargs):
        return [
            {
                'name': 'Film example name',
                'people': ['http://example.com/people/ba924631-068e-4436-b6de-f3283fa848f0']
            },
            {
                'name': 'Film example name2',
                'people': ['http://example.com/people/']  
            }
        ]

    def test_get_movie_list(self):
        client = Client()
        artist_response, film_response = mock.Mock(), mock.Mock()
        artist_response.json = self.artists_json_response
        film_response.json = self.film_json_response
        with mock.patch("aiohttp.client.ClientSession._request",
                        side_effect=[film_response, artist_response]) as patched:
            response = client.get('/movies/')
            assert response.context['movies'] == [
                {
                    'name': 'Film example name',
                    'people': ['http://example.com/people/ba924631-068e-4436-b6de-f3283fa848f0'],
                    'people_data': ['artist_name']
                },
                {
                    'name': 'Film example name2',
                    'people': ['http://example.com/people/'],
                    'people_data': []
                }
            ]
