# -*- coding: utf-8 -*-

from redis_cache import SimpleCache
import geopy

cache = SimpleCache()

CONFIG = {
    # List of backends to fallback to
    "backends": [geopy.Nominatim, geopy.GoogleV3, ],
    "cache": cache
}
