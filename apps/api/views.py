from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.views import APIView
from rest_framework.response import Response
from . import api


access_control_headers = {
    'Access-Control-Allow-Origin': '*',
    #'X-Frame-Options': 'ALLOW-FROM *'
}


class Stations(APIView):

    @method_decorator(cache_page(60 * 60 * 24)) # cache one day
    def get(self, request):

        all_stations = api.stations()
        stations = {}

        for station in all_stations:
            if not station['alias']:
                del(station['alias'])
                stations[station['code']] = station

        return Response(stations, headers=access_control_headers)


class StationNames(APIView):

    @method_decorator(cache_page(60 * 60 * 24)) # cache one day
    def get(self, request):

        stations = {}

        for station in api.stations():
            stations[station['name']] = station['code']

        return Response(stations, headers=access_control_headers)

class StationDepartures(APIView):

    @method_decorator(cache_page(60)) # cache 1 minute
    def get(self, request, station_code):

        try:
            departures = api.station_departures(station_code)
        except api.StationNotSupported:
            return Response(
                { 'error': 'not-found' },
                status=404,
                headers=access_control_headers
            )
        else:
            return Response(departures, headers=access_control_headers)
