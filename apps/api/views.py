from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.views import APIView
from rest_framework.response import Response
from . import api


class Stations(APIView):

    @method_decorator(cache_page(60 * 60 * 24)) # cache one day
    def get(self, request):

        all_stations = api.stations()
        stations = {}

        for station in all_stations:
            if not station['alias']:
                del(station['alias'])
                stations[station['code']] = station

        return Response(stations, headers={
            'Access-Control-Allow-Origin': '*',
            #'X-Frame-Options': 'ALLOW-FROM *'
        })


class StationNames(APIView):

    def get(self, request):

        all_stations = api.stations()
        stations = {}

        for station in all_stations:
            stations[station['name']] = station['code']

        return Response(stations, headers={
            'Access-Control-Allow-Origin': '*',
            #'X-Frame-Options': 'ALLOW-FROM *'
        })
