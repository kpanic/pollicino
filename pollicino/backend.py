# -*- coding: utf-8 -*-

from geopy import Nominatim, GoogleV3

from pollicino.response import GeocoderResponse


class OpenStreetMap(Nominatim):
    def geocode(self, query, **kwargs):
        kwargs['addressdetails'] = True
        kwargs['exactly_one'] = False
        responses = super(OpenStreetMap, self).geocode(query, **kwargs)
        if responses:
            geo_serializer = GeocoderResponse(provider='openstreetmap')
            responses = [geo_serializer.serialize(response)
                         for response in responses]
        return responses


class Google(GoogleV3):

    def __init__(self, *args, **kwargs):
        self.index_ttl = kwargs.pop('ttl')
        super(Google, self).__init__(*args, **kwargs)

    def geocode(self, query, **kwargs):
        geocoded_data = []
        kwargs['exactly_one'] = False

        responses = super(Google, self).geocode(query, **kwargs)
        if responses:
            geo_serializer = GeocoderResponse(provider='google')
            for response in responses:
                serialized_address = geo_serializer.serialize(response)
                serialized_address['ttl'] = self.index_ttl
                geocoded_data.append(serialized_address)

        return geocoded_data
