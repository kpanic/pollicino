# -*- coding: utf-8 -*-


class ElasticsearchResponse(object):
    @staticmethod
    def serialize(response):
        hits = response['hits']['hits']

        docs = [hit['_source'] for hit in hits]
        return docs


class GoogleAddress(object):

    mappings = {
        "street_number": ["housenumber"],
        "locality": ["city"],
        "country": ["country"],
        "route": ["road"],
        "sublocality_level_2": ["neighbourhood"],
        "administrative_area_level_2": ["suburb"],
        "administrative_area_level_1": ["state", "county"],
        "postal_code": ["postcode"]
    }

    def _init_attributes(self):
        for address_component in self.address_components:
            address_type = address_component['types'].pop(0)
            mapped_address_types = self.mappings.get(
                address_type, address_type)
            for mapped_address_type in mapped_address_types:
                setattr(
                    self, mapped_address_type, address_component['long_name'])
            if mapped_address_type == 'country':
                setattr(self, 'country_code', address_component['short_name'])

    def __init__(self, response):
        self.address_components = response.raw['address_components']
        self._init_attributes()

    def __getattr__(self, key):
        # Google returns different structures based on a geocoding query,
        # return None if the mapping is not found
        if not hasattr(self, key):
            return None


class NominatimAddress(object):
    def __init__(self, response):
        self.address = response.raw['address']

    def __getattr__(self, key):
        return self.address.get(key)


class GeocoderResponse(object):

    providers = ['openstreetmap', 'google']

    def __init__(self, provider=None):
        if provider not in self.providers:
            raise ValueError('Specify a geocoding from: $s', self.providers)
        self.AddressProvider = (NominatimAddress if provider == 'openstreetmap'
                                else GoogleAddress)

    def serialize(self, response):
        address = self.AddressProvider(response)

        doc = {
            "city": address.city,
            "country": address.country,
            "country_code": address.country_code,
            "county": address.county,
            "neighbourhood": address.neighbourhood,
            "postcode": address.postcode,
            "road": address.road,
            "state": address.state,
            "suburb": address.suburb,
            "house_number": address.housenumber,
            "full_address": response.address,
            "coordinates": [response.longitude, response.latitude]}

        return doc
