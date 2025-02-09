# webscraping_ai.SelectedHTMLApi

All URIs are relative to *https://api.webscraping.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_selected**](SelectedHTMLApi.md#get_selected) | **GET** /selected | HTML of a selected page area by URL and CSS selector
[**get_selected_multiple**](SelectedHTMLApi.md#get_selected_multiple) | **GET** /selected-multiple | HTML of multiple page areas by URL and CSS selectors


# **get_selected**
> str get_selected(url, selector=selector, headers=headers, timeout=timeout, js=js, js_timeout=js_timeout, wait_for=wait_for, proxy=proxy, country=country, custom_proxy=custom_proxy, device=device, error_on_404=error_on_404, error_on_redirect=error_on_redirect, js_script=js_script, format=format)

HTML of a selected page area by URL and CSS selector

Returns HTML of a selected page area by URL and CSS selector. Useful if you don't want to do the HTML parsing on your side.

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
    api_instance = webscraping_ai.SelectedHTMLApi(api_client)
    url = 'https://example.com' # str | URL of the target page.
    selector = 'h1' # str | CSS selector (null by default, returns whole page HTML) (optional)
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
    format = json # str | Format of the response (text by default). \"json\" will return a JSON object with the response, \"text\" will return a plain text/HTML response. (optional) (default to json)

    try:
        # HTML of a selected page area by URL and CSS selector
        api_response = api_instance.get_selected(url, selector=selector, headers=headers, timeout=timeout, js=js, js_timeout=js_timeout, wait_for=wait_for, proxy=proxy, country=country, custom_proxy=custom_proxy, device=device, error_on_404=error_on_404, error_on_redirect=error_on_redirect, js_script=js_script, format=format)
        print("The response of SelectedHTMLApi->get_selected:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SelectedHTMLApi->get_selected: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **url** | **str**| URL of the target page. | 
 **selector** | **str**| CSS selector (null by default, returns whole page HTML) | [optional] 
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
 **format** | **str**| Format of the response (text by default). \&quot;json\&quot; will return a JSON object with the response, \&quot;text\&quot; will return a plain text/HTML response. | [optional] [default to json]

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
**429** | Too many concurrent requests |  -  |
**500** | Non-2xx and non-404 HTTP status code on the target page or unexpected error, try again or contact support@webscraping.ai |  -  |
**504** | Timeout error, try increasing timeout parameter value |  -  |
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_selected_multiple**
> List[str] get_selected_multiple(url, selectors=selectors, headers=headers, timeout=timeout, js=js, js_timeout=js_timeout, wait_for=wait_for, proxy=proxy, country=country, custom_proxy=custom_proxy, device=device, error_on_404=error_on_404, error_on_redirect=error_on_redirect, js_script=js_script)

HTML of multiple page areas by URL and CSS selectors

Returns HTML of multiple page areas by URL and CSS selectors. Useful if you don't want to do the HTML parsing on your side.

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
    api_instance = webscraping_ai.SelectedHTMLApi(api_client)
    url = 'https://example.com' # str | URL of the target page.
    selectors = ['[\"h1\"]'] # List[str] | Multiple CSS selectors (null by default, returns whole page HTML) (optional)
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
        # HTML of multiple page areas by URL and CSS selectors
        api_response = api_instance.get_selected_multiple(url, selectors=selectors, headers=headers, timeout=timeout, js=js, js_timeout=js_timeout, wait_for=wait_for, proxy=proxy, country=country, custom_proxy=custom_proxy, device=device, error_on_404=error_on_404, error_on_redirect=error_on_redirect, js_script=js_script)
        print("The response of SelectedHTMLApi->get_selected_multiple:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SelectedHTMLApi->get_selected_multiple: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **url** | **str**| URL of the target page. | 
 **selectors** | [**List[str]**](str.md)| Multiple CSS selectors (null by default, returns whole page HTML) | [optional] 
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

**List[str]**

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

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

