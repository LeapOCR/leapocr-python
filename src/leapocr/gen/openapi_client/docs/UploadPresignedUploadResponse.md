# UploadPresignedUploadResponse


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**expires_at** | **datetime** |  | [optional] 
**job_id** | **str** |  | [optional] 
**upload_id** | **str** |  | [optional] 
**upload_url** | **str** |  | [optional] 

## Example

```python
from openapi_client.models.upload_presigned_upload_response import UploadPresignedUploadResponse

# TODO update the JSON string below
json = "{}"
# create an instance of UploadPresignedUploadResponse from a JSON string
upload_presigned_upload_response_instance = UploadPresignedUploadResponse.from_json(json)
# print the JSON string representation of the object
print UploadPresignedUploadResponse.to_json()

# convert the object into a dict
upload_presigned_upload_response_dict = upload_presigned_upload_response_instance.to_dict()
# create an instance of UploadPresignedUploadResponse from a dict
upload_presigned_upload_response_from_dict = UploadPresignedUploadResponse.from_dict(upload_presigned_upload_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


