# -*- coding: utf-8 -*-

import unittest
import mock

from redis_cache.rediscache import CacheMissException

from geocoder_cache import geocoder


class ConfigTestCase(unittest.TestCase):
    def setUp(self):
        self.nominatim_mock = mock.MagicMock()
        self.google_mock = mock.MagicMock()
        self.cache_mock = mock.MagicMock()
        self.cache_mock.get_json.side_effect = [
            CacheMissException, mock.MagicMock()]

        self.config = {
            "backends": [
                {
                    "openstreetmap": {
                        "class": self.nominatim_mock,
                        "params": {"country_bias": 'XX'}
                    }
                },
                {
                    "google": {
                        "class": self.google_mock,
                    }
                }
            ],
            "cache": self.cache_mock
        }

    def test_expect_geocoder_instance_with_minimal_config(self):
        geocoder_client = geocoder.GeocoderClient.from_config(self.config)
        self.assertTrue(geocoder_client)

    def test_expect_first_call_is_3rd_party_provider(self):
        geocoder_client = geocoder.GeocoderClient.from_config(self.config)
        geocoder_client.geocode('A sunny street')

        self.nominatim_mock().geocode.assert_called_once_with('a sunny street')
        self.assertFalse(self.google_mock().geocode.call_count)

    def test_expect_second_call_is_cached(self):
        geocoder_client = geocoder.GeocoderClient.from_config(self.config)
        geocoder_client.geocode('A sunny street')
        geocoder_client.geocode('A sunny street')

        # geocoder call
        self.nominatim_mock().geocode.assert_called_once_with('a sunny street')

        # cache hit
        self.cache_mock.get_json.assert_called_with('a sunny street')
        self.assertFalse(self.google_mock().geocode.call_count)


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
