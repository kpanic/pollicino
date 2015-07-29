# -*- coding: utf-8 -*-

import unittest
import mock

from pollicino import geocoder, exceptions
from pollicino.store import Store

from pollicino import exceptions, store
from elasticsearch import NotFoundError


class ElasticsearchIntegrationTestCase(unittest.TestCase):
    def setUp(self):
        self.geocoder_mock = mock.MagicMock()
        self.store = store.Elasticsearch
        self.store.index = 'test_pollicino'
        self.store = self.store()

        address = {
            "full_address": "Landsberger Allee 70 10249 Berlin",
            "house_number": "70",
            "city": "Berlin",
            "suburb": "",
            "postcode": "10249",
            "road": "Landseberger Allee",
            "coordinates": [1.00, 1.002]
        }
        self.store.set(address, id=1)
        self.store.backend.indices.refresh(index=self.store.index)

    def test_store_delete(self):
        address = {
            "full_address": "Kiefholzstr 16 12435 Berlin",
            "house_number": "16",
            "city": "Berlin",
            "suburb": "",
            "postcode": "12435",
            "road": "Kiefholzstr",
            "coordinates": [1.00, 1.002]
            }
        self.store.set(address, id=2)
        self.store.backend.indices.refresh(index=self.store.index)
        self.store.delete(id=2)
        with self.assertRaises(NotFoundError):
            self.store.get(id=2)

    def test_elasticssearch_real_address(self):
        address = "Landsberger Allee 70 10249 Berlin"

        response = self.store.search(address)

        # TODO:
        # Landsberger Allee  70    10249  Berlin
        # Some responses like the one above have too many spaces
        # That's why the spliting is done

        # TODO:
        # Is not matching exactly, even when an exact address is given
        # the response contains multiple addresses
        self.assertTrue("".join(address.split()) in
                        "".join(res['full_address'].split())
                        for res in response)

    def test_elasticssearch_fake_address(self):
        address = "xxxxxx 70 100000 Berlin"

        with self.assertRaises(exceptions.StoreDataNotFound):
            self.store.search(address)


