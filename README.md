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
result = geocoder.geocode('Via dei recoaro')
print result

# Formatted for your convenience

{
    u'display_name': u'Via Recoaro, Cascina Edri, Broni, PV, LOM, 27049, Italia',
    u'importance': 0.4,
    u'place_id': u'65292550',
    u'lon': u'9.2735356',
    u'boundingbox': [u'45.0620131', u'45.0691679', u'9.2664604', u'9.2755081'],
    u'osm_type': u'way',
    u'licence': u'Data \xa9 OpenStreetMap contributors, ODbL 1.0. http://www.openstreetmap.org/copyright',
    u'osm_id': u'39148840',
    u'lat': u'45.0660006',
    u'type': u'unclassified',
    u'class': u'highway',
    u'address':
    {
        u'country': u'Italia',
        u'county': u'PV',
        u'suburb': u'Cascina Edri',
        u'state': u'LOM',
        u'postcode': u'27049',
        u'country_code': u'it',
        u'village': u'Broni',
        u'road': u'Via Recoaro'
    }
}
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
* Unify responses
* Code organization
* Deal with geocoding typos
* ...etc
