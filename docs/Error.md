# Error


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**message** | **str** | Error description | [optional] 
**status_code** | **int** | Target page response HTTP status code (403, 500, etc) | [optional] 
**status_message** | **str** | Target page response HTTP status message | [optional] 
**body** | **str** | Target page response body | [optional] 

## Example

```python
from webscraping_ai.models.error import Error

# TODO update the JSON string below
json = "{}"
# create an instance of Error from a JSON string
error_instance = Error.from_json(json)
# print the JSON string representation of the object
print(Error.to_json())

# convert the object into a dict
error_dict = error_instance.to_dict()
# create an instance of Error from a dict
error_from_dict = Error.from_dict(error_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


