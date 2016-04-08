# -*- coding: utf-8 -*-

import abc

import elasticsearch
from elasticsearch.helpers import bulk as es_bulk

from pollicino.exceptions import StoreDataNotFound
from pollicino.response import ElasticsearchResponse


class Store(object):

    @staticmethod
    def from_config(config):
        storage = config.get('storage')
        if storage is None:
            raise KeyError('Specify a "storage" entry in your config')

        storage_class = storage['class']
        params = storage.get('params')
        storage_instance = storage_class(**params)

        return storage_instance


class Backend(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def search(self, query):
        raise NotImplementedError

    @abc.abstractmethod
    def set(self, body):
        raise NotImplementedError


class Redis(Backend):
    get_namespace = 'pollicino:address:{}'.format

    def search(self, query):
        pass

    def set(self, key, value):
        pass


class Elasticsearch(Backend):
    index = 'pollicino'
    doc_type = 'address'

    index_bootstrap = {
        "settings": {
            "index": {
                "analysis": {
                    "analyzer": {
                        "autocomplete_analyzer": {
                            "type": "custom",
                            "filter": [
                                "icu_normalizer",
                                "icu_folding",
                                "edge_ngram",
                            ],
                            "tokenizer": "icu_tokenizer"
                        }
                    },
                    "filter": {
                        "edge_ngram": {
                            "type": "edgeNGram",
                            "min_gram": 1,
                            "max_gram": 15

                        }
                    }
                }
            }
        },
        "mappings": {
            "address": {
                "dynamic": "strict",
                "_ttl": {"enabled": True},
                "_all": {
                    "analyzer": "autocomplete_analyzer"
                },
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
                    "postcode": {
                        "type": "string",
                        "index": "not_analyzed",
                    },
                    "house_number": {
                        "type": "string",
                        "index": "not_analyzed",
                    },
                    "coordinates": {
                        "type": "geo_point",
                    },
                    "full_address": {
                        "type": "string",
                    }
                }
            }
        }
    }

    def __init__(self, **params):
        self.backend = elasticsearch.Elasticsearch(**params)
        # TODO: it's not cheap to try to create the index (and mappings) for
        # every lookup, even if we ignore it

        self.backend.indices.create(
            index=self.index, ignore=400, body=self.index_bootstrap)

    def set(self, body, **extra_params):
        ttl = body.pop('ttl', None)
        if ttl is not None:
            body['_ttl'] = self.ttl

        self.backend.index(index=self.index, doc_type=self.doc_type, body=body,
                           **extra_params)

    def _prepare_bulk(self, docs):
        actions = {}
        for doc in docs:
            actions = {'_op_type': 'index',
                       '_index': 'pollicino',
                       '_type': 'address',
                       '_source': doc}
            ttl = doc.pop('ttl', None)
            if ttl is not None:
                actions['_ttl'] = ttl
            yield actions

    def bulk(self, body):
        bulk_actions = self._prepare_bulk(body)
        es_bulk(self.backend, bulk_actions,
                request_timeout=60, chunk_size=1000)

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

    def delete(self, id):
        self.backend.delete(index=self.index, doc_type=self.doc_type, id=id)

    def get(self, id):
        return self.backend.get(
            index=self.index, doc_type=self.doc_type, id=id)
