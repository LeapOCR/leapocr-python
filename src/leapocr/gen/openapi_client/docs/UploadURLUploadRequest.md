# UploadURLUploadRequest


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**file_name** | **str** |  | [optional] 
**format** | **str** | Option 2: Direct specification (will create template on-the-fly) | [optional] 
**instructions** | **str** |  | [optional] 
**var_schema** | **Dict[str, object]** |  | [optional] 
**template_id** | **str** | Option 1: Use existing template | [optional] 
**tier** | **str** |  | [optional] 
**url** | **str** |  | 

## Example

```python
from openapi_client.models.upload_url_upload_request import UploadURLUploadRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UploadURLUploadRequest from a JSON string
upload_url_upload_request_instance = UploadURLUploadRequest.from_json(json)
# print the JSON string representation of the object
print UploadURLUploadRequest.to_json()

# convert the object into a dict
upload_url_upload_request_dict = upload_url_upload_request_instance.to_dict()
# create an instance of UploadURLUploadRequest from a dict
upload_url_upload_request_from_dict = UploadURLUploadRequest.from_dict(upload_url_upload_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


