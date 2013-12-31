from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.http import Http404
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

        stations = {}

        for station in api.stations():
            stations[station['name']] = station['code']

        return Response(stations, headers={
            'Access-Control-Allow-Origin': '*',
            #'X-Frame-Options': 'ALLOW-FROM *'
        })

class StationDepartures(APIView):

    def get(self, request, station_code):

        headers = {
            'Access-Control-Allow-Origin': '*',
            #'X-Frame-Options': 'ALLOW-FROM *'
        }

        try:
            departures = api.station_departures(station_code)
        except api.StationNotSupported:
            return Response(
                { 'error': 'not-found' },
                status=404,
                headers=headers
            )
        else:
            return Response(departures, headers=headers)
