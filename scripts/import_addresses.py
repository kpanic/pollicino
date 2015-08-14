#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import dirname, realpath
import json

from pollicino.store import Store
from pollicino.config import CONFIG

store = Store.from_config(CONFIG)

pwd = dirname(realpath(__file__))

data_path = '%s/../data/excerpt_berlin_streets.json' % pwd


def prepare_addresses(address_components):
    for component in address_components:
        component = json.loads(component)
        tags = component.get('tags')
        if tags is not None:
            # If it has not street and coordinates are not float, skip
            if not all([tags.get('addr:street'), tags.get('addr:city')]):
                continue

            address = {}

            try:
                lon = float(component['lon'])
                lat = float(component['lat'])
            except KeyError:
                centroid = component.get('centroid')
                lon = float(centroid['lon'])
                lat = float(centroid['lat'])

            full_address = ' '.join([
                tags.get('addr:street', ''),
                tags.get('addr:housenumber', ''),
                tags.get('addr:suburb', ''),
                tags.get('addr:postcode', ''),
                tags.get('addr:city', ''),
                ])

            address.update({
                "full_address": full_address,
                "house_number": tags.get('addr:housenumber', ''),
                "city": tags.get('addr:city', ''),
                "suburb": tags.get('addr:suburb', ''),
                "postcode": tags.get('addr:postcode', ''),
                "road": tags.get('addr:street', ''),
                "coordinates": [lon, lat]
            })
            yield address


with open(data_path) as fd:

    addresses = prepare_addresses(fd)

    print("Bulk indexing...")
    store.bulk(addresses)
    print("Import done.")
