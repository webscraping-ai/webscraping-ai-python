# coding: utf-8

"""
    WebScraping.AI

    A client for https://webscraping.ai API. It provides a web scaping automation API with Chrome JS rendering, rotating proxies and builtin HTML parsing.  # noqa: E501

    The version of the OpenAPI document: 2.0.1
    Contact: support@webscraping.ai
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import re  # noqa: F401

# python 2 and python 3 compatibility library
import six

from webscraping_ai.api_client import ApiClient
from webscraping_ai.exceptions import (  # noqa: F401
    ApiTypeError,
    ApiValueError
)


class HTMLApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def get_html(self, url, **kwargs):  # noqa: E501
        """Page HTML by URL  # noqa: E501

        Returns just HTML on success, JSON on error  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_html(url, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str url: URL of the target page (required)
        :param dict(str, str) headers: HTTP headers to pass to the target page. Can be specified either via a nested query parameter (...&headers[One]=value1&headers=[Another]=value2) or as a JSON encoded object (...&headers={\"One\": \"value1\", \"Another\": \"value2\"})
        :param int timeout: Maximum processing time in ms. Increase it in case of timeout errors (5000 by default, maximum is 30000)
        :param bool js: Execute on-page JavaScript using a headless browser (true by default), costs 2 requests
        :param str proxy: Type of proxy, use residential proxies if your site restricts traffic from datacenters (datacenter by default)
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.get_html_with_http_info(url, **kwargs)  # noqa: E501

    def get_html_with_http_info(self, url, **kwargs):  # noqa: E501
        """Page HTML by URL  # noqa: E501

        Returns just HTML on success, JSON on error  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.get_html_with_http_info(url, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str url: URL of the target page (required)
        :param dict(str, str) headers: HTTP headers to pass to the target page. Can be specified either via a nested query parameter (...&headers[One]=value1&headers=[Another]=value2) or as a JSON encoded object (...&headers={\"One\": \"value1\", \"Another\": \"value2\"})
        :param int timeout: Maximum processing time in ms. Increase it in case of timeout errors (5000 by default, maximum is 30000)
        :param bool js: Execute on-page JavaScript using a headless browser (true by default), costs 2 requests
        :param str proxy: Type of proxy, use residential proxies if your site restricts traffic from datacenters (datacenter by default)
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = [
            'url',
            'headers',
            'timeout',
            'js',
            'proxy'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout'
            ]
        )

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method get_html" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'url' is set
        if self.api_client.client_side_validation and ('url' not in local_var_params or  # noqa: E501
                                                        local_var_params['url'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `url` when calling `get_html`")  # noqa: E501

        if self.api_client.client_side_validation and 'timeout' in local_var_params and local_var_params['timeout'] > 30000:  # noqa: E501
            raise ApiValueError("Invalid value for parameter `timeout` when calling `get_html`, must be a value less than or equal to `30000`")  # noqa: E501
        if self.api_client.client_side_validation and 'timeout' in local_var_params and local_var_params['timeout'] < 1:  # noqa: E501
            raise ApiValueError("Invalid value for parameter `timeout` when calling `get_html`, must be a value greater than or equal to `1`")  # noqa: E501
        collection_formats = {}

        path_params = {}

        query_params = []
        if 'url' in local_var_params and local_var_params['url'] is not None:  # noqa: E501
            query_params.append(('url', local_var_params['url']))  # noqa: E501
        if 'headers' in local_var_params and local_var_params['headers'] is not None:  # noqa: E501
            query_params.append(('headers', local_var_params['headers']))  # noqa: E501
        if 'timeout' in local_var_params and local_var_params['timeout'] is not None:  # noqa: E501
            query_params.append(('timeout', local_var_params['timeout']))  # noqa: E501
        if 'js' in local_var_params and local_var_params['js'] is not None:  # noqa: E501
            query_params.append(('js', local_var_params['js']))  # noqa: E501
        if 'proxy' in local_var_params and local_var_params['proxy'] is not None:  # noqa: E501
            query_params.append(('proxy', local_var_params['proxy']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'text/html'])  # noqa: E501

        # Authentication setting
        auth_settings = ['api_key']  # noqa: E501

        return self.api_client.call_api(
            '/html', 'GET',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)

    def post_html(self, url, **kwargs):  # noqa: E501
        """Page HTML by URL with POST request to the target page  # noqa: E501

        Returns just HTML on success, JSON on error. Request body will be passed to the target page.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.post_html(url, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str url: URL of the target page (required)
        :param dict(str, str) headers: HTTP headers to pass to the target page. Can be specified either via a nested query parameter (...&headers[One]=value1&headers=[Another]=value2) or as a JSON encoded object (...&headers={\"One\": \"value1\", \"Another\": \"value2\"})
        :param int timeout: Maximum processing time in ms. Increase it in case of timeout errors (5000 by default, maximum is 30000)
        :param bool js: Execute on-page JavaScript using a headless browser (true by default), costs 2 requests
        :param str proxy: Type of proxy, use residential proxies if your site restricts traffic from datacenters (datacenter by default)
        :param dict(str, object) request_body: Request body to pass to the target page
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True
        return self.post_html_with_http_info(url, **kwargs)  # noqa: E501

    def post_html_with_http_info(self, url, **kwargs):  # noqa: E501
        """Page HTML by URL with POST request to the target page  # noqa: E501

        Returns just HTML on success, JSON on error. Request body will be passed to the target page.  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.post_html_with_http_info(url, async_req=True)
        >>> result = thread.get()

        :param async_req bool: execute request asynchronously
        :param str url: URL of the target page (required)
        :param dict(str, str) headers: HTTP headers to pass to the target page. Can be specified either via a nested query parameter (...&headers[One]=value1&headers=[Another]=value2) or as a JSON encoded object (...&headers={\"One\": \"value1\", \"Another\": \"value2\"})
        :param int timeout: Maximum processing time in ms. Increase it in case of timeout errors (5000 by default, maximum is 30000)
        :param bool js: Execute on-page JavaScript using a headless browser (true by default), costs 2 requests
        :param str proxy: Type of proxy, use residential proxies if your site restricts traffic from datacenters (datacenter by default)
        :param dict(str, object) request_body: Request body to pass to the target page
        :param _return_http_data_only: response data without head status code
                                       and headers
        :param _preload_content: if False, the urllib3.HTTPResponse object will
                                 be returned without reading/decoding response
                                 data. Default is True.
        :param _request_timeout: timeout setting for this request. If one
                                 number provided, it will be total request
                                 timeout. It can also be a pair (tuple) of
                                 (connection, read) timeouts.
        :return: None
                 If the method is called asynchronously,
                 returns the request thread.
        """

        local_var_params = locals()

        all_params = [
            'url',
            'headers',
            'timeout',
            'js',
            'proxy',
            'request_body'
        ]
        all_params.extend(
            [
                'async_req',
                '_return_http_data_only',
                '_preload_content',
                '_request_timeout'
            ]
        )

        for key, val in six.iteritems(local_var_params['kwargs']):
            if key not in all_params:
                raise ApiTypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method post_html" % key
                )
            local_var_params[key] = val
        del local_var_params['kwargs']
        # verify the required parameter 'url' is set
        if self.api_client.client_side_validation and ('url' not in local_var_params or  # noqa: E501
                                                        local_var_params['url'] is None):  # noqa: E501
            raise ApiValueError("Missing the required parameter `url` when calling `post_html`")  # noqa: E501

        if self.api_client.client_side_validation and 'timeout' in local_var_params and local_var_params['timeout'] > 30000:  # noqa: E501
            raise ApiValueError("Invalid value for parameter `timeout` when calling `post_html`, must be a value less than or equal to `30000`")  # noqa: E501
        if self.api_client.client_side_validation and 'timeout' in local_var_params and local_var_params['timeout'] < 1:  # noqa: E501
            raise ApiValueError("Invalid value for parameter `timeout` when calling `post_html`, must be a value greater than or equal to `1`")  # noqa: E501
        collection_formats = {}

        path_params = {}

        query_params = []
        if 'url' in local_var_params and local_var_params['url'] is not None:  # noqa: E501
            query_params.append(('url', local_var_params['url']))  # noqa: E501
        if 'headers' in local_var_params and local_var_params['headers'] is not None:  # noqa: E501
            query_params.append(('headers', local_var_params['headers']))  # noqa: E501
        if 'timeout' in local_var_params and local_var_params['timeout'] is not None:  # noqa: E501
            query_params.append(('timeout', local_var_params['timeout']))  # noqa: E501
        if 'js' in local_var_params and local_var_params['js'] is not None:  # noqa: E501
            query_params.append(('js', local_var_params['js']))  # noqa: E501
        if 'proxy' in local_var_params and local_var_params['proxy'] is not None:  # noqa: E501
            query_params.append(('proxy', local_var_params['proxy']))  # noqa: E501

        header_params = {}

        form_params = []
        local_var_files = {}

        body_params = None
        if 'request_body' in local_var_params:
            body_params = local_var_params['request_body']
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json', 'text/html'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['application/json', 'application/x-www-form-urlencoded', 'application/xml', 'text/plain'])  # noqa: E501

        # Authentication setting
        auth_settings = ['api_key']  # noqa: E501

        return self.api_client.call_api(
            '/html', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type=None,  # noqa: E501
            auth_settings=auth_settings,
            async_req=local_var_params.get('async_req'),
            _return_http_data_only=local_var_params.get('_return_http_data_only'),  # noqa: E501
            _preload_content=local_var_params.get('_preload_content', True),
            _request_timeout=local_var_params.get('_request_timeout'),
            collection_formats=collection_formats)
