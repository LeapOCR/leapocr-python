# ModelsOCRStatusResponse


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**completed_at** | **str** |  | [optional] 
**error_message** | **str** |  | [optional] 
**job_id** | **str** |  | [optional] 
**processed_pages** | **int** |  | [optional] 
**progress_percentage** | **float** |  | [optional] 
**result_format** | **str** |  | [optional] 
**status** | **str** |  | [optional] 
**total_pages** | **int** |  | [optional] 

## Example

```python
from openapi_client.models.models_ocr_status_response import ModelsOCRStatusResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ModelsOCRStatusResponse from a JSON string
models_ocr_status_response_instance = ModelsOCRStatusResponse.from_json(json)
# print the JSON string representation of the object
print ModelsOCRStatusResponse.to_json()

# convert the object into a dict
models_ocr_status_response_dict = models_ocr_status_response_instance.to_dict()
# create an instance of ModelsOCRStatusResponse from a dict
models_ocr_status_response_from_dict = ModelsOCRStatusResponse.from_dict(models_ocr_status_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


