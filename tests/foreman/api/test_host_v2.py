"""Unit tests for the ``hosts`` paths.

Each ``TestCase`` subclass tests a single URL. A full list of URLs to be tested
can be found here: http://theforeman.org/api/apidoc/v2/hosts

"""
from fauxfactory import FauxFactory
from robottelo.api import client
from robottelo.common.decorators import skip_if_bz_bug_open
from robottelo.common.helpers import get_server_url, get_server_credentials
from robottelo import entities
from unittest import TestCase
from urlparse import urljoin
# (too many public methods) pylint: disable=R0904


class HostsTestCase(TestCase):
    """Tests for path ``api/v2/hosts``."""
    def setUp(self):  # pylint: disable=C0103
        """Set ``self.path``."""
        self.path = urljoin(get_server_url(), 'api/v2/hosts')

    def test_get(self):
        """@Test: GET ``api/v2/hosts``.

        @Feature: Host
        @Assert: HTTP 200 is returned with an ``application/json``
        content-type, and response contains valid categories of data.

        """
        response = client.get(
            self.path,
            auth=get_server_credentials(),
            verify=False
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('application/json', response.headers['content-type'])

        # Are the correct categories of data returned?
        categories = response.json().keys()
        for category in (
                u'total', u'subtotal', u'page', u'per_page', u'search',
                u'sort', u'results'):
            self.assertIn(category, categories)

    def test_get_search(self):
        """@Test: GET ``api/v2/hosts`` and specify the ``search`` parameter.

        @Feature: Host
        @Assert: HTTP 200 is returned, along with ``search`` term.

        """
        query = FauxFactory.generate_string(
            'utf8',
            FauxFactory.generate_integer(1, 100)
        )
        response = client.get(
            self.path,
            auth=get_server_credentials(),
            params={'search': query},
            verify=False,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['search'], query)

    def test_get_per_page(self):
        """@Test: GET ``api/v2/hosts`` and specify the ``per_page`` parameter.

        @Feature: Host
        @Assert: HTTP 200 is returned, along with per ``per_page`` value.

        """
        per_page = FauxFactory.generate_integer(1, 1000)
        response = client.get(
            self.path,
            auth=get_server_credentials(),
            params={'per_page': per_page},
            verify=False,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['per_page'], per_page)

    def test_get_unauthorized(self):
        """@Test: GET ``api/v2/hosts`` and do not provide credentials.

        @Feature: Host
        @Assert: HTTP 401 is returned

        """
        response = client.get(self.path, verify=False)
        self.assertEqual(response.status_code, 401)

    @skip_if_bz_bug_open('1113272')
    def test_post(self):
        """@Test: POST ``api/v2/hosts``.

        @Feature: Host
        @Assert: HTTP 201 is returned

        """
        response = client.post(
            self.path,
            entities.Host().attributes('api'),
            auth=get_server_credentials(),
            verify=False,
        )
        status_code = 201
        self.assertEqual(
            status_code,
            response.status_code,
            'Desired HTTP {0}, got HTTP {1}. {2}'.format(
                status_code,
                response.status_code,
                response.json().get('error', 'No error received.')
            )
        )

    def test_post_unauthorized(self):
        """@Test: POST ``api/v2/hosts`` and do not provide credentials.

        @Feature: Host
        @Assert: HTTP 401 is returned

        """
        response = client.post(self.path, verify=False)
        self.assertEqual(response.status_code, 401)