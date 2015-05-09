# -*- coding: utf-8 -*-

import six

from pollicino.exceptions import StoreDataNotFound
from geopy import Nominatim, GoogleV3

from pollicino.response import GeocoderResponse
from pollicino.store import Store


class OpenStreetMap(Nominatim):
    def geocode(self, query, **kwargs):
        kwargs['addressdetails'] = True
        kwargs['exactly_one'] = False
        responses = super(OpenStreetMap, self).geocode(query, **kwargs)
        if responses:
            geo_serializer = GeocoderResponse(provider='google')
            responses = [geo_serializer.serialize(response)
                         for response in responses]
        return responses


class Google(GoogleV3):
    def geocode(self, query, **kwargs):
        kwargs['exactly_one'] = False
        responses = super(Google, self).geocode(query, **kwargs)
        if responses:
            geo_serializer = GeocoderResponse(provider='google')
            responses = [geo_serializer.serialize(response)
                         for response in responses]
        return responses


class GeoContainer(object):

    @classmethod
    def from_config(cls, config):
        backends = config.get('backends')
        if backends is None:
            raise KeyError("Specify at least one geocoding backend in your config")
        backend_instances = []
        for backend_entry in backends:
            for _, backend in six.iteritems(backend_entry):
                backend_class = backend['class']
                params = backend.get('params', {})
                backend_instance = backend_class(**params)
                backend_instances.append(backend_instance)

        return cls(backend_instances)

    def __init__(self, backends):
        self.backends = backends

    def geocode(self, address):
        result = None
        for backend in self.backends:
            result = backend.geocode(address)
            if result is not None:
                break

        return result


class GeocoderClient(object):
    @classmethod
    def from_config(cls, config):

        storage = Store.from_config(config)
        geocoder = GeoContainer.from_config(config)

        store_client = cls(geocoder, storage)
        return store_client

    def __init__(self, geocoder, storage):
        self.geocoder = geocoder
        self.storage = storage

    def geocode(self, address):
        try:
            responses = []
            for store in self.storage:
                results = store.search(address)
                if results:
                    responses.extend(results)
        except StoreDataNotFound:
            print("Geocoding address: %s" % address)
            responses = self.geocoder.geocode(address)
            if not responses:
                raise ValueError("Address not found %s", address)
            for store in self.storage:
                store.bulk(responses)

        return responses
