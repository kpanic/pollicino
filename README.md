## Pollicino

## Street search, spiced up with multiple storage and geocoders

### Find Pollicino by following breadcrumbs in the woods!

* Free software: LGPL3 license

**Description**

The aim of this project is to be able to use multiple geocoding
backends (OpenStreetMap, Google maps and so on) and execute search in a storage
(elasticsearch, redis, etc)

There might be different storage backends support in the future other than the
aforementioned.

**WARNING**

**Work in Progress**

## Do-not-use (yet ;)) (really)

```python
from pollicino import config

from pollicino.geocoder import GeocoderClient

geocoder = GeocoderClient.from_config(config.CONFIG)

result = geocoder.geocode('Via Recoaro 1, Broni')
print result

# Formatted for your convenience

{'city': u'Broni',
 'coordinates': [9.2732744, 45.0688205],
 'country': u'Italy',
 'country_code': u'IT',
 'county': u'Lombardia',
 'full_address': u'Via dei Recoaro, 1, 27043 Broni PV, Italy',
 'house_number': u'1',
 'neighbourhood': None,
 'postcode': u'27043',
 'road': u'Via dei Recoaro',
 'state': u'Lombardia',
 'suburb': u'Pavia'}
```

# Warming up the Elasticsearch storage from an OpenStreetMap data excerpt

Execute: `./scripts/import_addresses.py`
You should have in the `pollicino` index an excerpt of the streets of
**Berlin**.
Try to search for `Landsberg`, it should match `Landsberg*` from Elasticsearch,
otherwise fallback to Google Maps

**NOTE**
Per **Google Maps Terms of Use**, the data can be cached for 30 days maximum, this
is specified in the configuration of `Pollicino`

## Requirements

* Install elasticsearch with your favorite package manager: 

Example on Debian based distributions 
(after adding the elasticsearch repository):

```
sudo apt-get install elasticsearch
```

* Install the ICU Analisys plugin for Elasticsearch

```
sudo bin/plugin install elasticsearch/elasticsearch-analysis-icu/2.5.0
```

And restart Elasticsearch

**NOTE**
on Debian based distributions the `plugin` command is located in:

`/usr/share/elasticsearch/bin/plugin`

## TODO

* Tests :)
* Check how the response coming from google changes to handle corner cases
* Localize the analyzers based on configuration (Currently the `de_analyzer` is
  hardcoded)
* Add the OpenStreetMap importer script
* Timeouts
* Unify responses
* Code organization
* ...etc
