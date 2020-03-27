# coding: utf-8

"""
    WebScraping.AI

    A client for https://webscraping.ai API. It provides Chrome JS rendering, rotating proxies and HTML parsing for web scraping.  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from webscraping_ai.api_client import ApiClient
from webscraping_ai.exceptions import (
    ApiTypeError,
    ApiValueError
)


class HtmlApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def get_page(self, url, **kwargs):  # noqa: E501
        """Get page HTML by URL (renders JS in Chrome and uses rotating proxies)  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_page(url, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str url: URL of the page to get (required)
        :param str selector: CSS selector to get a part of the page (null by default, returns whole page HTML)
        :param bool outer_html: Return outer HTML of the selected element (false by default, returns inner HTML)
        :param str proxy: Proxy country code, for geotargeting (US by default)
        :param bool disable_js: Disable JS execution (false by default)
        :param bool inline_css: Inline included CSS files to make page viewable on other domains (false by default)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: ScrappedPage
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.get_page_with_http_info(url, **kwargs)  # noqa: E501

    def get_page_with_http_info(self, url, **kwargs):  # noqa: E501
        """Get page HTML by URL (renders JS in Chrome and uses rotating proxies)  # noqa: E501

        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_page_with_http_info(url, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str url: URL of the page to get (required)
        :param str selector: CSS selector to get a part of the page (null by default, returns whole page HTML)
        :param bool outer_html: Return outer HTML of the selected element (false by default, returns inner HTML)
        :param str proxy: Proxy country code, for geotargeting (US by default)
        :param bool disable_js: Disable JS execution (false by default)
        :param bool inline_css: Inline included CSS files to make page viewable on other domains (false by default)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: tuple(ScrappedPage, status_code(int), headers(HTTPHeaderDict))
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = ['url', 'selector', 'outer_html', 'proxy', 'disable_js', 'inline_css']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_page" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'url' is set
        if self.api_client.client_side_validation and ('url' not in local_var_params or  # noqa: E501
                                                        local_var_params['url'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `url` when calling `get_page`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []
        if 'url' in local_var_params and local_var_params['url'] is not None:  # noqa: E501
            query_params.append(('url', local_var_params['url']))  # noqa: E501
        if 'selector' in local_var_params and local_var_params['selector'] is not None:  # noqa: E501
            query_params.append(('selector', local_var_params['selector']))  # noqa: E501
        if 'outer_html' in local_var_params and local_var_params['outer_html'] is not None:  # noqa: E501
            query_params.append(('outer_html', local_var_params['outer_html']))  # noqa: E501
        if 'proxy' in local_var_params and local_var_params['proxy'] is not None:  # noqa: E501
            query_params.append(('proxy', local_var_params['proxy']))  # noqa: E501
        if 'disable_js' in local_var_params and local_var_params['disable_js'] is not None:  # noqa: E501
            query_params.append(('disable_js', local_var_params['disable_js']))  # noqa: E501
        if 'inline_css' in local_var_params and local_var_params['inline_css'] is not None:  # noqa: E501
            query_params.append(('inline_css', local_var_params['inline_css']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # Authentication setting
        auth_settings = ['api_key']  # noqa: E501

        return self.api_client.call_api(
            '/', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='ScrappedPage',  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)
