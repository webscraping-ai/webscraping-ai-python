# webscraping_ai.HtmlApi

All URIs are relative to *https://webscraping.ai/api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_page**](HtmlApi.md#get_page) | **GET** / | Get page HTML by URL (renders JS in Chrome and uses rotating proxies)


# **get_page**
> ScrappedPage get_page(url, selector=selector, outer_html=outer_html, proxy=proxy, disable_js=disable_js, inline_css=inline_css)

Get page HTML by URL (renders JS in Chrome and uses rotating proxies)

### Example

* Api Key Authentication (api_key):
```python
from __future__ import print_function
import time
import webscraping_ai
from webscraping_ai.rest import ApiException
from pprint import pprint
configuration = webscraping_ai.Configuration()
# Configure API key authorization: api_key
configuration.api_key['api_key'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['api_key'] = 'Bearer'

# Defining host is optional and default to https://webscraping.ai/api
configuration.host = "https://webscraping.ai/api"
# Enter a context with an instance of the API client
with webscraping_ai.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = webscraping_ai.HtmlApi(api_client)
    url = 'https://example.com' # str | URL of the page to get
selector = 'html' # str | CSS selector to get a part of the page (null by default, returns whole page HTML) (optional)
outer_html = false # bool | Return outer HTML of the selected element (false by default, returns inner HTML) (optional)
proxy = 'US' # str | Proxy country code, for geotargeting (US by default) (optional)
disable_js = false # bool | Disable JS execution (false by default) (optional)
inline_css = false # bool | Inline included CSS files to make page viewable on other domains (false by default) (optional)

    try:
        # Get page HTML by URL (renders JS in Chrome and uses rotating proxies)
        api_response = api_instance.get_page(url, selector=selector, outer_html=outer_html, proxy=proxy, disable_js=disable_js, inline_css=inline_css)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling HtmlApi->get_page: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **url** | **str**| URL of the page to get | 
 **selector** | **str**| CSS selector to get a part of the page (null by default, returns whole page HTML) | [optional] 
 **outer_html** | **bool**| Return outer HTML of the selected element (false by default, returns inner HTML) | [optional] 
 **proxy** | **str**| Proxy country code, for geotargeting (US by default) | [optional] 
 **disable_js** | **bool**| Disable JS execution (false by default) | [optional] 
 **inline_css** | **bool**| Inline included CSS files to make page viewable on other domains (false by default) | [optional] 

### Return type

[**ScrappedPage**](ScrappedPage.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Success |  -  |
**405** | Invalid input |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

