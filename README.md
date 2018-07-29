# asyncio-sample-app
A sample app to test asyncio by hitting a rest service and writing test for it

## Description
The app exposes a url /movies/ which lists out top movies data using Ghibli's Api (https://ghibliapi.herokuapp.com/).
This app hits the film API and fetches top movies results. It then also hits the people api and populates the film data with people's name.

## Tech
The interesting part is the use of asyncio to achieve the work. Async http calls use aiohttp(https://github.com/aio-libs/aiohttp).
Tests uses asynctest (https://github.com/Martiusweb/asynctest/). 
A `Memoize` decorater caches the api call for 1 minute. Also `Cache-Control` has been set with max-age for 1 minute.

## Next interesting todos
- Pagination for results
- Handling of Etag and last modified headers
