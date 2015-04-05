# -*- coding: utf-8 -*-

import abc

from walrus import Database
import elasticsearch

from pollicino.exceptions import StoreDataNotFound
from pollicino.response import ElasticsearchResponse


class Store(object):

    @staticmethod
    def from_config(config):
        storage = config.get('storage')
        if storage is None:
            raise KeyError('Specify a "storage" entry in your config')

        storage_instances = []
        for store in storage:
            storage_class = store['class']
            params = store.get('params')
            storage_instance = storage_class(**params)
            storage_instances.append(storage_instance)

        return storage_instances


class Backend(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def search(self, query):
        raise NotImplementedError

    @abc.abstractmethod
    def set(self, body):
        raise NotImplementedError


class Redis(Backend):
    def __init__(self, **params):
        db = Database(**params)
        self.ac = db.autocomplete()

    def search(self, query):
        search_result = self.ac.search(query)
        if not search_result:
            raise StoreDataNotFound()
        return search_result

    def set(self, body):
        full_address = body.get('full_address')
        self.ac.store(full_address, data=body)


class Elasticsearch(Backend):
    index = 'pollicino'
    doc_type = 'address'

    index_bootstrap = {
        "settings": {
            "index": {
                "analysis": {
                    "analyzer": {
                        "de_analyzer": {
                            "type": "custom",
                            "filter": [
                                "icu_normalizer",
                                "de_stop_filter",
                                "icu_folding",
                                "edge_ngram",
                            ],
                            "tokenizer": "icu_tokenizer"
                        },
                        "en_analyzer": {
                            "type": "custom",
                            "filter": [
                                "icu_normalizer",
                                "en_stop_filter",
                                "icu_folding",
                                "edge_ngram",
                            ],
                            "tokenizer": "icu_tokenizer"
                        },
                        "es_analyzer": {
                            "type": "custom",
                            "filter": [
                                "icu_normalizer",
                                "es_stop_filter",
                                "icu_folding",
                                "edge_ngram",
                            ],
                            "tokenizer": "icu_tokenizer"
                        },
                        "default": {
                            "type": "custom",
                            "filter": ["icu_normalizer", "icu_folding"],
                            "tokenizer": "icu_tokenizer"
                        }
                    },
                    "filter": {
                        "de_stop_filter": {
                            "type": "stop",
                            "stopwords": ["_german_"]
                        },
                        "en_stop_filter": {
                            "type": "stop",
                            "stopwords": ["_english_"]
                        },
                        "es_stop_filter": {
                            "type": "stop",
                            "stopwords": ["_spanish_"]
                        },
                        "edge_ngram": {
                            "type":"edgeNGram",
                            "min_gram":1,
                            "max_gram":15

                        }
                    }
                }
            }
        },
        "mappings": {
            "address": {
                "_all": {
                    "analyzer": "de_analyzer",
                },
                "properties": {
                    "location": {
                        "properties": {
                            "country": {
                                "type": "string",
                            },
                            "city": {
                                "type": "string",
                            },
                            "suburb": {
                                "type": "string",
                            },
                            "road": {
                                "type": "string",
                            },
                            "coordinates": {
                                "type": "geo_point",
                                "index": "not_analyzed"
                            }
                        }
                    }
                }
            }
        }
    }

    def __init__(self, **params):
        self.ttl = params.pop("ttl", "30d")
        self.backend = elasticsearch.Elasticsearch(**params)
        # TODO: it's not cheap to try to create the index (and mappings) for
        # every lookup, even if we ignore it

        self.backend.indices.create(
            index=self.index, ignore=400, body=self.index_bootstrap)

    # doc_type might be the key
    def set(self, body):
        # TTL harcoded to 30 days per google policy
        self.backend.index(
            index=self.index, doc_type=self.doc_type, body=body, ttl=self.ttl)

    def search(self, text):
        query = self.build_query(text)

        search_result = self.backend.search(
            index=self.index, doc_type=self.doc_type, body=query)

        if not search_result['hits']['hits']:
            raise StoreDataNotFound()

        return ElasticsearchResponse.serialize(search_result)

    def build_query(self, text):
        query = {
            "query": {
                "filtered": {
                    "query": {
                        "match": {
                            "_all": {
                                "query": text,
                                "operator": "and",
                            }
                        }
                    }
                }
            }
        }

        return query
