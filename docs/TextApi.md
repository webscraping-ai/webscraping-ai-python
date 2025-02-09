# webscraping_ai.TextApi

All URIs are relative to *https://api.webscraping.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_text**](TextApi.md#get_text) | **GET** /text | Page text by URL


# **get_text**
> str get_text(url, text_format=text_format, return_links=return_links, headers=headers, timeout=timeout, js=js, js_timeout=js_timeout, wait_for=wait_for, proxy=proxy, country=country, custom_proxy=custom_proxy, device=device, error_on_404=error_on_404, error_on_redirect=error_on_redirect, js_script=js_script)

Page text by URL

Returns the visible text content of a webpage specified by the URL. Can be used to feed data to LLM models. The response can be in plain text, JSON, or XML format based on the text_format parameter. Proxies and Chromium JavaScript rendering are used for page retrieval and processing. Returns JSON on error.

### Example

* Api Key Authentication (api_key):

```python
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
configuration.api_key['api_key'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['api_key'] = 'Bearer'

# Enter a context with an instance of the API client
with webscraping_ai.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = webscraping_ai.TextApi(api_client)
    url = 'https://example.com' # str | URL of the target page.
    text_format = plain # str | Format of the text response (plain by default). \"plain\" will return only the page body text. \"json\" and \"xml\" will return a json/xml with \"title\", \"description\" and \"content\" keys. (optional) (default to plain)
    return_links = False # bool | [Works only with text_format=json] Return links from the page body text (false by default). Useful for building web crawlers. (optional) (default to False)
    headers = {'key': '{\"Cookie\":\"session=some_id\"}'} # Dict[str, str] | HTTP headers to pass to the target page. Can be specified either via a nested query parameter (...&headers[One]=value1&headers=[Another]=value2) or as a JSON encoded object (...&headers={\"One\": \"value1\", \"Another\": \"value2\"}). (optional)
    timeout = 10000 # int | Maximum web page retrieval time in ms. Increase it in case of timeout errors (10000 by default, maximum is 30000). (optional) (default to 10000)
    js = True # bool | Execute on-page JavaScript using a headless browser (true by default). (optional) (default to True)
    js_timeout = 2000 # int | Maximum JavaScript rendering time in ms. Increase it in case if you see a loading indicator instead of data on the target page. (optional) (default to 2000)
    wait_for = 'wait_for_example' # str | CSS selector to wait for before returning the page content. Useful for pages with dynamic content loading. Overrides js_timeout. (optional)
    proxy = datacenter # str | Type of proxy, use residential proxies if your site restricts traffic from datacenters (datacenter by default). Note that residential proxy requests are more expensive than datacenter, see the pricing page for details. (optional) (default to datacenter)
    country = us # str | Country of the proxy to use (US by default). (optional) (default to us)
    custom_proxy = 'custom_proxy_example' # str | Your own proxy URL to use instead of our built-in proxy pool in \"http://user:password@host:port\" format (<a target=\"_blank\" href=\"https://webscraping.ai/proxies/smartproxy\">Smartproxy</a> for example). (optional)
    device = desktop # str | Type of device emulation. (optional) (default to desktop)
    error_on_404 = False # bool | Return error on 404 HTTP status on the target page (false by default). (optional) (default to False)
    error_on_redirect = False # bool | Return error on redirect on the target page (false by default). (optional) (default to False)
    js_script = 'document.querySelector(\'button\').click();' # str | Custom JavaScript code to execute on the target page. (optional)

    try:
        # Page text by URL
        api_response = api_instance.get_text(url, text_format=text_format, return_links=return_links, headers=headers, timeout=timeout, js=js, js_timeout=js_timeout, wait_for=wait_for, proxy=proxy, country=country, custom_proxy=custom_proxy, device=device, error_on_404=error_on_404, error_on_redirect=error_on_redirect, js_script=js_script)
        print("The response of TextApi->get_text:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling TextApi->get_text: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **url** | **str**| URL of the target page. | 
 **text_format** | **str**| Format of the text response (plain by default). \&quot;plain\&quot; will return only the page body text. \&quot;json\&quot; and \&quot;xml\&quot; will return a json/xml with \&quot;title\&quot;, \&quot;description\&quot; and \&quot;content\&quot; keys. | [optional] [default to plain]
 **return_links** | **bool**| [Works only with text_format&#x3D;json] Return links from the page body text (false by default). Useful for building web crawlers. | [optional] [default to False]
 **headers** | [**Dict[str, str]**](str.md)| HTTP headers to pass to the target page. Can be specified either via a nested query parameter (...&amp;headers[One]&#x3D;value1&amp;headers&#x3D;[Another]&#x3D;value2) or as a JSON encoded object (...&amp;headers&#x3D;{\&quot;One\&quot;: \&quot;value1\&quot;, \&quot;Another\&quot;: \&quot;value2\&quot;}). | [optional] 
 **timeout** | **int**| Maximum web page retrieval time in ms. Increase it in case of timeout errors (10000 by default, maximum is 30000). | [optional] [default to 10000]
 **js** | **bool**| Execute on-page JavaScript using a headless browser (true by default). | [optional] [default to True]
 **js_timeout** | **int**| Maximum JavaScript rendering time in ms. Increase it in case if you see a loading indicator instead of data on the target page. | [optional] [default to 2000]
 **wait_for** | **str**| CSS selector to wait for before returning the page content. Useful for pages with dynamic content loading. Overrides js_timeout. | [optional] 
 **proxy** | **str**| Type of proxy, use residential proxies if your site restricts traffic from datacenters (datacenter by default). Note that residential proxy requests are more expensive than datacenter, see the pricing page for details. | [optional] [default to datacenter]
 **country** | **str**| Country of the proxy to use (US by default). | [optional] [default to us]
 **custom_proxy** | **str**| Your own proxy URL to use instead of our built-in proxy pool in \&quot;http://user:password@host:port\&quot; format (&lt;a target&#x3D;\&quot;_blank\&quot; href&#x3D;\&quot;https://webscraping.ai/proxies/smartproxy\&quot;&gt;Smartproxy&lt;/a&gt; for example). | [optional] 
 **device** | **str**| Type of device emulation. | [optional] [default to desktop]
 **error_on_404** | **bool**| Return error on 404 HTTP status on the target page (false by default). | [optional] [default to False]
 **error_on_redirect** | **bool**| Return error on redirect on the target page (false by default). | [optional] [default to False]
 **js_script** | **str**| Custom JavaScript code to execute on the target page. | [optional] 

### Return type

**str**

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, text/html, text/xml

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**400** | Parameters validation error |  -  |
**402** | Billing issue, probably you&#39;ve ran out of credits |  -  |
**403** | Wrong API key |  -  |
**429** | Too many concurrent requests |  -  |
**500** | Non-2xx and non-404 HTTP status code on the target page or unexpected error, try again or contact support@webscraping.ai |  -  |
**504** | Timeout error, try increasing timeout parameter value |  -  |
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

