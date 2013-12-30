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

    simple_fields = {
        'ritnummer': 'RitNummer',
        'vertrektijd': 'VertrekTijd',
        'vertrekvertraging': 'VertrekVertraging',
        'vertrekvertragingtekst': 'VertrekVertragingTekst',
        'eindbestemming': 'EindBestemming',
        'treinsoort': 'TreinSoort',
        'routetekst': 'RouteTekst',
        'vervoerder': 'Vervoerder',
        'reistip': 'ReisTip',
    }

    def get_xml():
        return requests.get(
            'http://webservices.ns.nl/ns-api-avt?station={}'.format(station),
            auth=auth
        ).content

    def get_departures():

        departures = []

        for departure_xml in ET.fromstring(get_xml()):

            departure = {}
            set_simple_fields(departure, departure_xml)
            set_vertrekspoor(departure, departure_xml)
            set_opmerkingen(departure, departure_xml)

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

    def set_vertrekspoor(departure, departure_xml):

        vertrekspoor_el = departure_xml.find('VertrekSpoor')

        if vertrekspoor_el is None:
            vertrekspoor = None
            vertrekspoor_gewijzigd = None
        else:
            vertrekspoor = vertrekspoor_el.text
            vertrekspoor_gewijzigd = (
                True if vertrekspoor_el.attrib['wijziging'] == 'true'
                else False
            )

        departure['vertrekspoor'] = vertrekspoor
        departure['vertrekspoor_gewijzigd'] = vertrekspoor_gewijzigd

    def set_opmerkingen(departure, departure_xml):

        opmerkingen_el = departure_xml.find('Opmerkingen')
        opmerkingen = []

        if opmerkingen_el is not None:
            for opmerking in opmerkingen_el.getchildren():
                opmerkingen.append(opmerking.text.strip())

        departure['opmerkingen'] = opmerkingen

    return get_departures()
