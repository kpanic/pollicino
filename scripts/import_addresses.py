#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import sys
from os.path import dirname, realpath

from pollicino.store import Store
from pollicino.config import CONFIG

store = Store.from_config(CONFIG)

pwd = dirname(realpath(__file__))

data_path = '%s/../data/excerpt_berlin_streets.csv' % pwd

csv.field_size_limit(sys.maxsize)


def prepare_addresses(address_components):
    for component in address_components:
        # If it has not street and coordinates are not float, skip
        if not all([component['street'], component['city']]):
            continue

        address = {}
        try:
            lon = float(component['lon'].strip())
            lat = float(component['lat'].strip())
        except ValueError:
            # Corrupted data, it's not a float, skip
            continue
        full_address = ' '.join([
            component['street'],
            component['housenumber'],
            component['suburb'],
            component['postcode'],
            component['city'],
            ])

        address.update({
            "full_address": full_address,
            "house_number": component['housenumber'],
            "city": component['city'],
            "suburb": component['suburb'],
            "postcode": component['postcode'],
            "road": component['street'],
            "coordinates": [lon, lat]
        })
        yield address


with open(data_path) as fd:
    reader = csv.DictReader(fd, delimiter=';')

    addresses = prepare_addresses(reader)

    print("Bulk indexing...")
    store[0].bulk(addresses)
    print("Import done.")
