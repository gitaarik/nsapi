import xml.etree.ElementTree as ET
import requests


def stations():

    response = requests.get(
        'http://webservices.ns.nl/ns-api-stations',
        auth=(
            'gitaarik@gmail.com',
            'Kg7KENJ6BaLRbSrpHiDdc-m3tvo1NQbVc93ldNzffO2IQNQVIMMeVA'
        )
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
