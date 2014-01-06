import re
from datetime import timedelta
from dateutil.parser import parse
import xml.etree.ElementTree as ET
import requests


auth = (
    'gitaarik@gmail.com',
    'Kg7KENJ6BaLRbSrpHiDdc-m3tvo1NQbVc93ldNzffO2IQNQVIMMeVA'
)

class StationNotSupported(Exception):
    pass


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

    simple_fields = {
        'number': 'RitNummer',
        'destination': 'EindBestemming',
        'train_type': 'TreinSoort',
        'route_text': 'RouteTekst',
        'carrier': 'Vervoerder',
        'travel_hint': 'ReisTip',
    }

    def get_xml():
        return requests.get(
            'http://webservices.ns.nl/ns-api-avt?station={}'.format(station),
            auth=auth
        ).content

    def get_departures():

        departures = []
        departures_xml = ET.fromstring(get_xml())

        if departures_xml.tag == 'error':
            raise StationNotSupported();

        for departure_xml in departures_xml:

            departure = {}
            set_simple_fields(departure, departure_xml)
            set_platform(departure, departure_xml)
            set_remarks(departure, departure_xml)
            set_departure_time_including_delay(departure, departure_xml)

            departures.append(departure)

        return departures

    def set_simple_fields(departure, departure_xml):

        for json_name, xml_name in simple_fields.items():

            element = departure_xml.find(xml_name)

            if element is None:
                value = None
            else:
                value = element.text

            departure[json_name] = value

    def set_platform(departure, departure_xml):

        platform_el = departure_xml.find('VertrekSpoor')

        if platform_el is None:
            platform = None
            platform_changed = None
        else:
            platform = platform_el.text
            platform_changed = (
                True if platform_el.attrib['wijziging'] == 'true'
                else False
            )

        departure['platform'] = platform
        departure['platform_changed'] = platform_changed

    def set_remarks(departure, departure_xml):

        remarks_el = departure_xml.find('Opmerkingen')
        remarks = []

        if remarks_el is not None:
            for remark in remarks_el.getchildren():
                remark.append(remark.text.strip())

        departure['remarks'] = remarks

    def set_departure_time_including_delay(departure, departure_xml):

        departure_time = departure_xml.find('VertrekTijd').text

        try:
            departure_delay = int(re.sub('[^0-9]', '',
                departure_xml.find('VertrekVertraging').text))
        except Exception:
            departure_delay = 0

        try:
            departure_time = parse(departure_time)
        except Exception:
            departure_time_including_delay = None
        else:
            departure_time_including_delay = (
                departure_time + timedelta(minutes=departure_delay)
            )

        departure['departure_time'] = departure_time
        departure['departure_delay'] = departure_delay
        departure['departure_time_including_delay'] = departure_time_including_delay

    return get_departures()
