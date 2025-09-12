# ResponseErrorResponse


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**code** | [**ResponseErrorCode**](ResponseErrorCode.md) |  | [optional] 
**details** | **object** |  | [optional] 
**error** | [**ResponseErrorMessage**](ResponseErrorMessage.md) |  | [optional] 

## Example

```python
from openapi_client.models.response_error_response import ResponseErrorResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ResponseErrorResponse from a JSON string
response_error_response_instance = ResponseErrorResponse.from_json(json)
# print the JSON string representation of the object
print ResponseErrorResponse.to_json()

# convert the object into a dict
response_error_response_dict = response_error_response_instance.to_dict()
# create an instance of ResponseErrorResponse from a dict
response_error_response_from_dict = ResponseErrorResponse.from_dict(response_error_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


