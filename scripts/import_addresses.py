#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
from os.path import dirname, realpath

from pollicino.store import Store
from pollicino.config import CONFIG

store = Store.from_config(CONFIG)

pwd = dirname(realpath(__file__))

data_path = '%s/../data/excerpt_berlin_streets.csv' % pwd


def filter_out_incomplete_data(addresses):
    address_components = []

    for address in addresses:
        if address[0] and not (str.isalpha(address[5]) or
                               str.isalpha(address[6])):
            components = map(lambda component: component.strip(), address)
            address_components.append(components)

    return address_components


def store_addresses(address_components):
    for component in address_components:
        address = {}
        address.update({
            "full_address": ' '.join(component[0:4]),
            "house_number": component[1],
            "city": component[4],
            "suburb": component[3],
            "postcode": component[2],
            "road": component[0],
            "coordinates": [component[5], component[6]]
        })
        # Use just the first storage for the moment
        store[0].set(address)

with open(data_path) as fd:
    reader = csv.reader(fd, delimiter=';')

    # skip the header
    reader.next()

    address_components = filter_out_incomplete_data(reader)

    print("Total number of addresses to import %s" % len(address_components))
    print("Importing...")

    store_addresses(address_components)

    print("Import done.")
