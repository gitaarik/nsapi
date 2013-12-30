from dateutil import parser
import xml.etree.ElementTree as ET
import requests


auth = (
    'gitaarik@gmail.com',
    'Kg7KENJ6BaLRbSrpHiDdc-m3tvo1NQbVc93ldNzffO2IQNQVIMMeVA'
)

def stations():

    response = requests.get(
        'http://webservices.ns.nl/ns-api-stations',
        auth=auth
    )

    stations_xml = ET.fromstring(response.content)
    stations = []

    for station_xml in stations_xml:
        stations.append({
            'name': station_xml.find('name').text,
            'code': station_xml.find('code').text,
            'country': station_xml.find('country').text,
            'lat': station_xml.find('lat').text,
            'long': station_xml.find('long').text,
            'alias': True if station_xml.find('alias').text == 'true' else False,
        })

    return stations

def station_departures(station):

    response = requests.get(
        'http://webservices.ns.nl/ns-api-avt?station={}'.format(station),
        auth=auth
    )

    departures_xml = ET.fromstring(response.content)
    departures = []

    for departure_xml in departures_xml:

        try:
            routetekst = departure_xml.find('RouteTekst').text
        except:
            routetekst = None

        departures.append({
            'ritnummer': departure_xml.find('RitNummer').text,
            'vertrektijd': departure_xml.find('VertrekTijd').text,
            'eindbestemming': departure_xml.find('EindBestemming').text,
            'treinsoort': departure_xml.find('TreinSoort').text,
            'routetekst': routetekst,
            'vervoerder': departure_xml.find('Vervoerder').text,
        })

    return departures
