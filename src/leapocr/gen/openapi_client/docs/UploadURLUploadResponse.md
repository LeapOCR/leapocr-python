# UploadURLUploadResponse


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**created_at** | **datetime** |  | [optional] 
**job_id** | **str** |  | [optional] 
**source_url** | **str** |  | [optional] 
**status** | **str** |  | [optional] 

## Example

```python
from openapi_client.models.upload_url_upload_response import UploadURLUploadResponse

# TODO update the JSON string below
json = "{}"
# create an instance of UploadURLUploadResponse from a JSON string
upload_url_upload_response_instance = UploadURLUploadResponse.from_json(json)
# print the JSON string representation of the object
print UploadURLUploadResponse.to_json()

# convert the object into a dict
upload_url_upload_response_dict = upload_url_upload_response_instance.to_dict()
# create an instance of UploadURLUploadResponse from a dict
upload_url_upload_response_from_dict = UploadURLUploadResponse.from_dict(upload_url_upload_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


