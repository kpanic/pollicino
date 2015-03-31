# -*- coding: utf-8 -*-

import unittest
import mock

from pollicino import geocoder, exceptions


class GeocoderClientTestCase(unittest.TestCase):
    def setUp(self):
        self.geocoder_mock = mock.MagicMock()
        self.store_mock = mock.MagicMock()
        self.store_mock().search.side_effect = [
            exceptions.StoreDataNotFound, mock.MagicMock()]

        self.config = {
            "backends": [
                {
                    "openstreetmap": {
                        "class": self.geocoder_mock,
                        "params": {"country_bias": 'XX'}
                    }
                }
            ],
            "storage": [{
                "class": self.store_mock,
                "params": {"host": 'localhost'},
                "ttl": "1"
            }]
        }

    def test_expect_geocoder_instance_with_minimal_config(self):
        geocoder_client = geocoder.GeocoderClient.from_config(self.config)
        self.assertTrue(geocoder_client)

    def test_expect_first_call_is_3rd_party_provider(self):
        geocoder_client = geocoder.GeocoderClient.from_config(self.config)
        geocoder_client.geocode('A sunny street')

        self.geocoder_mock().geocode.assert_called_once_with('A sunny street')

    def test_expect_second_call_is_cached(self):
        geocoder_client = geocoder.GeocoderClient.from_config(self.config)
        geocoder_client.geocode('A sunny street')
        geocoder_client.geocode('A sunny street')

        # geocoder call
        self.geocoder_mock().geocode.assert_called_once_with('A sunny street')

        # store hit
        self.store_mock().search.assert_called_with('A sunny street')


class GeocoderConfigTestCase(unittest.TestCase):
    def test_expect_empty_config_raise_an_exception(self):
        config = {}
        with self.assertRaises(KeyError):
            geocoder.GeocoderClient.from_config(config)

    def test_expect_config_without_cache_raise_and_exception(self):
        config = {
            "backends": [
                {
                    "openstreetmap": {
                        "class": mock.MagicMock(),
                        "params": {"country_bias": 'XX'}
                    }
                }
            ]
        }

        with self.assertRaises(KeyError):
            geocoder.GeocoderClient.from_config(config)

    def test_expect_config_without_backends_raise_and_exception(self):
        config = {
            "cache": mock.MagicMock()
        }

        with self.assertRaises(KeyError):
            geocoder.GeocoderClient.from_config(config)
