# UploadInitiateUploadRequest


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**content_type** | **str** |  | 
**file_name** | **str** |  | 
**file_size** | **int** |  | [optional] 
**format** | **str** | Option 2: Direct specification (will create template on-the-fly) | [optional] 
**instructions** | **str** |  | [optional] 
**var_schema** | **Dict[str, object]** |  | [optional] 
**template_id** | **str** | Option 1: Use existing template | [optional] 
**tier** | **str** |  | [optional] 

## Example

```python
from openapi_client.models.upload_initiate_upload_request import UploadInitiateUploadRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UploadInitiateUploadRequest from a JSON string
upload_initiate_upload_request_instance = UploadInitiateUploadRequest.from_json(json)
# print the JSON string representation of the object
print UploadInitiateUploadRequest.to_json()

# convert the object into a dict
upload_initiate_upload_request_dict = upload_initiate_upload_request_instance.to_dict()
# create an instance of UploadInitiateUploadRequest from a dict
upload_initiate_upload_request_from_dict = UploadInitiateUploadRequest.from_dict(upload_initiate_upload_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


