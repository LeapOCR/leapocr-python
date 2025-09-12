# ModelsOCRResultResponse


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**average_confidence** | **float** |  | [optional] 
**completed_at** | **str** |  | [optional] 
**credits_used** | **int** |  | [optional] 
**file_name** | **str** |  | [optional] 
**job_id** | **str** |  | [optional] 
**model** | **str** |  | [optional] 
**pages** | [**List[ModelsPageResponse]**](ModelsPageResponse.md) |  | [optional] 
**pagination** | [**ModelsPaginationResponse**](ModelsPaginationResponse.md) |  | [optional] 
**processed_pages** | **int** |  | [optional] 
**processing_time_seconds** | **float** |  | [optional] 
**result_format** | **str** |  | [optional] 
**status** | [**ModelsJobStatus**](ModelsJobStatus.md) |  | [optional] 
**total_pages** | **int** |  | [optional] 

## Example

```python
from openapi_client.models.models_ocr_result_response import ModelsOCRResultResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ModelsOCRResultResponse from a JSON string
models_ocr_result_response_instance = ModelsOCRResultResponse.from_json(json)
# print the JSON string representation of the object
print ModelsOCRResultResponse.to_json()

# convert the object into a dict
models_ocr_result_response_dict = models_ocr_result_response_instance.to_dict()
# create an instance of ModelsOCRResultResponse from a dict
models_ocr_result_response_from_dict = ModelsOCRResultResponse.from_dict(models_ocr_result_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


