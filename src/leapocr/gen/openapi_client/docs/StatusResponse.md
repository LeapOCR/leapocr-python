# StatusResponse


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**category** | **str** | Document category name example: Financial Reports | [optional] 
**confidence_score** | **float** | Average confidence score of OCR results (null if job not completed) example: 94.8 | [optional] 
**created_at** | **str** | When the job was created example: 2024-01-15T10:30:00Z | [optional] 
**error_message** | **str** | Error message if job failed example: Failed to process page 5 | [optional] 
**file_name** | **str** | The name of the file being processed example: quarterly_financial_report_q4.pdf | [optional] 
**id** | **str** | The unique identifier of the job example: 123e4567-e89b-12d3-a456-426614174000 | [optional] 
**processed_pages** | **int** | Number of pages processed so far example: 24 | [optional] 
**processing_time** | **int** | Total processing time in seconds example: 156 | [optional] 
**progress_percentage** | **float** | Percentage of pages processed example: 100 | [optional] 
**result_format** | **str** | The result format type of the job example: structured | [optional] 
**status** | **str** | The current status of the job example: completed | [optional] 
**total_pages** | **int** | Total number of pages in the document example: 24 | [optional] 

## Example

```python
from openapi_client.models.status_response import StatusResponse

# TODO update the JSON string below
json = "{}"
# create an instance of StatusResponse from a JSON string
status_response_instance = StatusResponse.from_json(json)
# print the JSON string representation of the object
print StatusResponse.to_json()

# convert the object into a dict
status_response_dict = status_response_instance.to_dict()
# create an instance of StatusResponse from a dict
status_response_from_dict = StatusResponse.from_dict(status_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


