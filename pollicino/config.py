# -*- coding: utf-8 -*-

from pollicino import backend, store


CONFIG = {
    # List of backends to fallback to
    # There might be a list of multiple backends
    # Use google fallback for the moment, since it has most of the times
    # housenumbers, while OpenStreetMap, might lack them
    "backends": [
        {
            "google": {
                "class": backend.Google,
                "params": {"ttl": "30d"}
            }
        }
    ],
    "storage": {
        "class": store.Elasticsearch,
        "params": {"host": "localhost"}
    }
}
