# -*- coding: utf-8 -*-

from pollicino import geocoder, store


CONFIG = {
    # List of backends to fallback to
    # There might be a list of multiple backends
    # Use google fallback for the moment, since it has most of the times
    # housenumbers, while OpenStreetMap, might lack them
    "backends": [
        {
            "google": {
                "class": geocoder.Google,
            }
        }
    ],
    # Other storage could be plugged in, additionally to store.Elasticsearch
    "storage": [
        {
            "class": store.Elasticsearch,
            "params": {"host": "localhost"},
            "ttl": "30d"
        }
    ]
}
