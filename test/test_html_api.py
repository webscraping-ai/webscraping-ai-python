# coding: utf-8

"""
    WebScraping.AI

    This is a sample server Petstore server. For this sample, you can use the api key `special-key` to test the authorization filters.  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest

import webscraping_ai
from webscraping_ai.api.html_api import HtmlApi  # noqa: E501
from webscraping_ai.rest import ApiException


class TestHtmlApi(unittest.TestCase):
    """HtmlApi unit test stubs"""

    def setUp(self):
        self.api = webscraping_ai.api.html_api.HtmlApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_get_page(self):
        """Test case for get_page

        Get page HTML by URL  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
