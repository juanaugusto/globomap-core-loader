import json
import unittest
from loader.globomap import GloboMapClient, GloboMapException
from mock import patch, MagicMock
from tests.util import open_json, as_json


class TestGloboMapCllient(unittest.TestCase):

    def setUp(self):
        self.globomap_client = GloboMapClient('http://localhost:8080')

    @classmethod
    def tearDownClass(cls):
        patch.stopall()

    def test_create_element(self):
        requests_mock = self._mock_request({"key": "globomap_key"}, 201)

        payload = open_json('tests/json/globomap/create_vip.json')
        self.assertIsNotNone(self.globomap_client.update_element_state('CREATE', 'collections', 'vip', payload))
        self._assert_request_called(
            requests_mock,
            'POST',
            'http://localhost:8080/collections/vip/',
            payload
        )

    def test_create_element_expect_exception(self):
        with self.assertRaises(GloboMapException):
            requests_mock = self._mock_request({"id": 1}, 500)
            payload = {'name': 'vip.test.com'}
            self.globomap_client.create('collections', 'vip', payload)

            self._assert_request_called(
                requests_mock,
                'POST',
                'http://localhost:8080/collections/vip/',
                payload
            )

    def test_update_element(self):
        payload = open_json('tests/json/globomap/update_vip.json')
        requests_mock = self._mock_request(as_json(payload), 200)

        self.assertIsNotNone(self.globomap_client.update_element_state('UPDATE', 'collections', 'vip', payload))
        self._assert_request_called(
            requests_mock,
            'PUT',
            'http://localhost:8080/collections/vip/globomap_vip.test.com',
            payload
        )

    def test_update_element_expect_exception(self):
        with self.assertRaises(GloboMapException):
            requests_mock = self._mock_request({"id": 1}, 500)
            payload = open_json('tests/json/globomap/update_vip.json')
            self.globomap_client.update_element_state('UPDATE', 'collections', 'vip',  payload)

            self._assert_request_called(
                requests_mock,
                'UPDATE',
                'http://localhost:8080/collections/vip/globomap_vip.test.com',
                payload
            )

    def test_patch_element(self):
        payload = open_json('tests/json/globomap/update_vip.json')
        requests_mock = self._mock_request(as_json(payload), 200)

        self.assertIsNotNone(self.globomap_client.update_element_state('PATCH', 'collections', 'vip', payload))
        self._assert_request_called(
            requests_mock,
            'PATCH',
            'http://localhost:8080/collections/vip/globomap_vip.test.com',
            payload
        )

    def test_patch_element_expect_exception(self):
        with self.assertRaises(GloboMapException):
            requests_mock = self._mock_request({"id": 1}, 500)
            payload = open_json('tests/json/globomap/update_vip.json')
            self.globomap_client.update_element_state('UPDATE', 'collections', 'vip', payload)

            self._assert_request_called(
                requests_mock,
                'PATCH',
                'http://localhost:8080/collections/vip/globomap_vip.test.com',
                payload
            )

    def test_delete_element(self):
        requests_mock = self._mock_request(None, 200)
        payload = open_json('tests/json/globomap/delete_vip.json')

        self.assertIsNone(self.globomap_client.update_element_state('DELETE', 'collections', 'vip', payload))
        self._assert_request_called(
            requests_mock,
            'DELETE',
            'http://localhost:8080/collections/vip/globomap_vip.test.com',
            None
        )

    def test_delete_element_expect_exception(self):
        with self.assertRaises(GloboMapException):
            requests_mock = self._mock_request(None, 500)
            payload = open_json('tests/json/globomap/delete_vip.json')
            self.globomap_client.update_element_state('DELETE', 'collections', 'vip', payload)

            self._assert_request_called(
                requests_mock,
                'DELETE',
                'http://localhost:8080/collections/vip/globomap_vip.test.com',
                None
            )

    def _assert_request_called(self, requests_mock, method, url, payload):
        requests_mock.request.assert_called_once_with(method, url, data=json.dumps(payload))

    def _mock_request(self, content, status=200):
        requests_mock = patch('loader.globomap.requests').start()
        response_mock = MagicMock(status_code=status, content=as_json(content))
        requests_mock.request.return_value = response_mock
        return requests_mock
