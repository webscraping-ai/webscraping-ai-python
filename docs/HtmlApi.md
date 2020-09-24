# webscraping_ai.HTMLApi

All URIs are relative to *https://api.webscraping.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_html**](HTMLApi.md#get_html) | **GET** /html | Page HTML by URL
[**post_html**](HTMLApi.md#post_html) | **POST** /html | Page HTML by URL with POST request to the target page


# **get_html**
> str get_html(url, headers=headers, timeout=timeout, js=js, proxy=proxy)

Page HTML by URL

Returns just HTML on success, JSON on error

### Example

* Api Key Authentication (api_key):
```python
from __future__ import print_function
import time
import webscraping_ai
from webscraping_ai.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to https://api.webscraping.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = webscraping_ai.Configuration(
    host = "https://api.webscraping.ai"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: api_key
configuration = webscraping_ai.Configuration(
    host = "https://api.webscraping.ai",
    api_key = {
        'api_key': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['api_key'] = 'Bearer'

# Enter a context with an instance of the API client
with webscraping_ai.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = webscraping_ai.HTMLApi(api_client)
    url = 'https://example.com' # str | URL of the target page
headers = {'key': '{\"Cookie\":\"session=some_id\"}'} # dict(str, str) | HTTP headers to pass to the target page. Can be specified either via a nested query parameter (...&headers[One]=value1&headers=[Another]=value2) or as a JSON encoded object (...&headers={\"One\": \"value1\", \"Another\": \"value2\"}) (optional)
timeout = 5000 # int | Maximum processing time in ms. Increase it in case of timeout errors (5000 by default, maximum is 30000) (optional) (default to 5000)
js = True # bool | Execute on-page JavaScript using a headless browser (true by default), costs 2 requests (optional) (default to True)
proxy = 'datacenter' # str | Type of proxy, use residential proxies if your site restricts traffic from datacenters (datacenter by default) (optional) (default to 'datacenter')

    try:
        # Page HTML by URL
        api_response = api_instance.get_html(url, headers=headers, timeout=timeout, js=js, proxy=proxy)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling HTMLApi->get_html: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **url** | **str**| URL of the target page | 
 **headers** | [**dict(str, str)**](str.md)| HTTP headers to pass to the target page. Can be specified either via a nested query parameter (...&amp;headers[One]&#x3D;value1&amp;headers&#x3D;[Another]&#x3D;value2) or as a JSON encoded object (...&amp;headers&#x3D;{\&quot;One\&quot;: \&quot;value1\&quot;, \&quot;Another\&quot;: \&quot;value2\&quot;}) | [optional] 
 **timeout** | **int**| Maximum processing time in ms. Increase it in case of timeout errors (5000 by default, maximum is 30000) | [optional] [default to 5000]
 **js** | **bool**| Execute on-page JavaScript using a headless browser (true by default), costs 2 requests | [optional] [default to True]
 **proxy** | **str**| Type of proxy, use residential proxies if your site restricts traffic from datacenters (datacenter by default) | [optional] [default to &#39;datacenter&#39;]

### Return type

**str**

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, text/html

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**400** | Parameters validation error |  -  |
**402** | Billing issue, probably you&#39;ve ran out of credits |  -  |
**403** | Wrong API key |  -  |
**422** | Non-2xx and non-404 HTTP status code on the target page |  -  |
**429** | Too many concurrent requests |  -  |
**500** | Unexpected error, try again or contact support@webscraping.ai |  -  |
**504** | Timeout error, try increasing timeout parameter value |  -  |
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **post_html**
> str post_html(url, headers=headers, timeout=timeout, js=js, proxy=proxy, request_body=request_body)

Page HTML by URL with POST request to the target page

Returns just HTML on success, JSON on error. Request body will be passed to the target page.

### Example

* Api Key Authentication (api_key):
```python
from __future__ import print_function
import time
import webscraping_ai
from webscraping_ai.rest import ApiException
from pprint import pprint
# Defining the host is optional and defaults to https://api.webscraping.ai
# See configuration.py for a list of all supported configuration parameters.
configuration = webscraping_ai.Configuration(
    host = "https://api.webscraping.ai"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: api_key
configuration = webscraping_ai.Configuration(
    host = "https://api.webscraping.ai",
    api_key = {
        'api_key': 'YOUR_API_KEY'
    }
)
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['api_key'] = 'Bearer'

# Enter a context with an instance of the API client
with webscraping_ai.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = webscraping_ai.HTMLApi(api_client)
    url = 'https://httpbin.org/post' # str | URL of the target page
headers = {'key': '{\"Cookie\":\"session=some_id\"}'} # dict(str, str) | HTTP headers to pass to the target page. Can be specified either via a nested query parameter (...&headers[One]=value1&headers=[Another]=value2) or as a JSON encoded object (...&headers={\"One\": \"value1\", \"Another\": \"value2\"}) (optional)
timeout = 5000 # int | Maximum processing time in ms. Increase it in case of timeout errors (5000 by default, maximum is 30000) (optional) (default to 5000)
js = True # bool | Execute on-page JavaScript using a headless browser (true by default), costs 2 requests (optional) (default to True)
proxy = 'datacenter' # str | Type of proxy, use residential proxies if your site restricts traffic from datacenters (datacenter by default) (optional) (default to 'datacenter')
request_body = None # dict(str, object) | Request body to pass to the target page (optional)

    try:
        # Page HTML by URL with POST request to the target page
        api_response = api_instance.post_html(url, headers=headers, timeout=timeout, js=js, proxy=proxy, request_body=request_body)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling HTMLApi->post_html: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **url** | **str**| URL of the target page | 
 **headers** | [**dict(str, str)**](str.md)| HTTP headers to pass to the target page. Can be specified either via a nested query parameter (...&amp;headers[One]&#x3D;value1&amp;headers&#x3D;[Another]&#x3D;value2) or as a JSON encoded object (...&amp;headers&#x3D;{\&quot;One\&quot;: \&quot;value1\&quot;, \&quot;Another\&quot;: \&quot;value2\&quot;}) | [optional] 
 **timeout** | **int**| Maximum processing time in ms. Increase it in case of timeout errors (5000 by default, maximum is 30000) | [optional] [default to 5000]
 **js** | **bool**| Execute on-page JavaScript using a headless browser (true by default), costs 2 requests | [optional] [default to True]
 **proxy** | **str**| Type of proxy, use residential proxies if your site restricts traffic from datacenters (datacenter by default) | [optional] [default to &#39;datacenter&#39;]
 **request_body** | [**dict(str, object)**](object.md)| Request body to pass to the target page | [optional] 

### Return type

**str**

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, application/xml, text/plain
 - **Accept**: application/json, text/html

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**400** | Parameters validation error |  -  |
**402** | Billing issue, probably you&#39;ve ran out of credits |  -  |
**403** | Wrong API key |  -  |
**422** | Non-2xx and non-404 HTTP status code on the target page |  -  |
**429** | Too many concurrent requests |  -  |
**500** | Unexpected error, try again or contact support@webscraping.ai |  -  |
**504** | Timeout error, try increasing timeout parameter value |  -  |
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

