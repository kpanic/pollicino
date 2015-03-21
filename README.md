## Geocoder Cache

## Multiple geocoders, spiced up with persistent cache

* Free software: LGPL3 license

**WARNING**

**Work in Progress**, use at your own risk ;)

## Do-not-usage (yet ;))

```python
from geocoder_cache import config

from geocoder_cache.geocoder import GeocoderClient

geocoder = GeocoderClient.from_config(config.CONFIG)

# Get from the cache or geocode the address
# Tuti Bridge, Sudan. Find out a place that is in OSM but not on Google Maps or
# the reverse to double check the fallback
result = geocoder.geocode('Tuti bridge')
print result['display_name']

Tuti Bridge, Al Mogran, Mogran, الخرطوم, al-Khartum, 11114, السودان - Sudan
```

## Requirements

* Install redis-server with your favorite package manager to cache geocoded
  responses

Example on Debian based distributions:

```
sudo apt-get install redis-server
```

## TODO

* Tests :)
* Timeouts
* Code organization
* Deal with geocoding typos
* ...etc
