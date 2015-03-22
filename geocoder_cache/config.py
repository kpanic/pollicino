# -*- coding: utf-8 -*-

from redis_cache import SimpleCache
import geopy

from geocoder_cache import geocoder

cache = SimpleCache()

# Sudan
COUNTRY = 'SD'

CONFIG = {
    # List of backends to fallback to
    "backends": [
        {
            "openstreetmap": {
                "class": geocoder.NominatimWrapper,
                "params": {"country_bias": COUNTRY}
            }
        },
        {
            "google": {
                "class": geopy.GoogleV3,
            }
        }
    ],
    "cache": cache
}
