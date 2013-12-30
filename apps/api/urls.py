from django.conf.urls import patterns, url
from . import views


urlpatterns = patterns('',
    url(r'^stations/', views.Stations.as_view()),
    url(r'^stationnames/', views.StationNames.as_view()),
    url(r'^departures/(?P<station_code>\w+)/', views.StationDepartures.as_view())
)
