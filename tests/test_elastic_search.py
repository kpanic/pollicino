# -*- coding: utf-8 -*-

import unittest

from pollicino import exceptions
from pollicino import store

from elasticsearch import NotFoundError


class ElasticsearchIntegrationTestCase(unittest.TestCase):
    def setUp(self):
        storage = store.Elasticsearch
        storage.index = 'pollicino_test'
        self.storage = storage()

        self.address = {
            "full_address": "Landsberger Allee 70 10249 Berlin",
            "house_number": "70",
            "city": "Berlin",
            "suburb": "",
            "postcode": "10249",
            "road": "Landseberger Allee",
            "coordinates": [1.00, 1.002]
        }

        self.storage.set(self.address, id=1)
        self.storage.backend.indices.refresh(index=self.storage.index)

    def test_storage_delete(self):
        address = {
            "full_address": "Kiefholzstr 16 12435 Berlin",
            "house_number": "16",
            "city": "Berlin",
            "suburb": "",
            "postcode": "12435",
            "road": "Kiefholzstr",
            "coordinates": [1.00, 1.002]
        }

        self.storage.set(address, id=2)
        self.storage.backend.indices.refresh(index=self.storage.index)
        self.storage.delete(id=2)
        with self.assertRaises(NotFoundError):
            self.storage.get(id=2)

    def test_storage_with_a_real_address(self):
        address = "Landsberger Allee 70 10249 Berlin"

        response = self.storage.search(address)

        self.assertEqual(response[0], self.address)

    @unittest.skip("Fails on travis, passed locally, skip for now")
    def test_storage_partial_complete(self):
        address = "Lands"

        response = self.storage.search(address)

        self.assertEqual(response[0], self.address)

    def test_storage_with_unexisting_address(self):
        address = "xxxxxx 70 100000 Berlin"

        with self.assertRaises(exceptions.StoreDataNotFound):
            self.storage.search(address)
