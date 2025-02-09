# webscraping_ai.AccountApi

All URIs are relative to *https://api.webscraping.ai*

Method | HTTP request | Description
------------- | ------------- | -------------
[**account**](AccountApi.md#account) | **GET** /account | Information about your account calls quota


# **account**
> Account account()

Information about your account calls quota

Returns information about your account, including the remaining API credits quota, the next billing cycle start time, and the remaining concurrent requests. The response is in JSON format.

### Example

* Api Key Authentication (api_key):

```python
import webscraping_ai
from webscraping_ai.models.account import Account
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
    api_instance = webscraping_ai.AccountApi(api_client)

    try:
        # Information about your account calls quota
        api_response = api_instance.account()
        print("The response of AccountApi->account:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling AccountApi->account: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**Account**](Account.md)

### Authorization

[api_key](../README.md#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**403** | Wrong API key |  -  |
**200** | Success |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

