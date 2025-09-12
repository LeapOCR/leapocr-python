# openapi_client.SDKApi

All URIs are relative to *http://localhost:8080/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_job_result_0**](SDKApi.md#get_job_result_0) | **GET** /ocr/result/{job_id} | Get OCR job result
[**get_job_status_0**](SDKApi.md#get_job_status_0) | **GET** /ocr/status/{job_id} | Get OCR job status
[**presigned_upload_1**](SDKApi.md#presigned_upload_1) | **POST** /ocr/uploads/presigned | Presigned upload
[**upload_from_url_1**](SDKApi.md#upload_from_url_1) | **POST** /ocr/uploads/url | Public URL upload


# **get_job_result_0**
> ModelsOCRResultResponse get_job_result_0(job_id, page=page, limit=limit)

Get OCR job result

Retrieve OCR processing results for a completed job with extracted text and structured data. Returns job status if processing is still in progress. Supports pagination

### Example

```python
import time
import os
import openapi_client
from openapi_client.models.models_ocr_result_response import ModelsOCRResultResponse
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8080/api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost:8080/api/v1"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.SDKApi(api_client)
    job_id = 'job_id_example' # str | OCR job ID
    page = 1 # int | Page number for result pagination (optional) (default to 1)
    limit = 100 # int | Number of items per page (optional) (default to 100)

    try:
        # Get OCR job result
        api_response = api_instance.get_job_result_0(job_id, page=page, limit=limit)
        print("The response of SDKApi->get_job_result_0:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SDKApi->get_job_result_0: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **job_id** | **str**| OCR job ID | 
 **page** | **int**| Page number for result pagination | [optional] [default to 1]
 **limit** | **int**| Number of items per page | [optional] [default to 100]

### Return type

[**ModelsOCRResultResponse**](ModelsOCRResultResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OCR processing completed, results available |  -  |
**202** | OCR processing in progress, status returned |  -  |
**400** | Bad request - invalid job ID or parameters |  -  |
**401** | Unauthorized - authentication required |  -  |
**403** | Forbidden - job belongs to different user |  -  |
**404** | Not found - job does not exist |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_job_status_0**
> StatusResponse get_job_status_0(job_id)

Get OCR job status

Retrieve current processing status and progress information for an OCR job. Shows completion status, progress percentage, and any error details

### Example

```python
import time
import os
import openapi_client
from openapi_client.models.status_response import StatusResponse
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8080/api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost:8080/api/v1"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.SDKApi(api_client)
    job_id = 'job_id_example' # str | OCR job ID

    try:
        # Get OCR job status
        api_response = api_instance.get_job_status_0(job_id)
        print("The response of SDKApi->get_job_status_0:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SDKApi->get_job_status_0: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **job_id** | **str**| OCR job ID | 

### Return type

[**StatusResponse**](StatusResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Job status retrieved successfully |  -  |
**400** | Bad request - invalid job ID format |  -  |
**401** | Unauthorized - authentication required |  -  |
**403** | Forbidden - job belongs to different user |  -  |
**404** | Not found - job does not exist |  -  |
**500** | Internal server error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **presigned_upload_1**
> UploadPresignedUploadResponse presigned_upload_1(upload_initiate_upload_request)

Presigned upload

Create a job and generate a presigned URL for direct file upload to R2. Supported format: PDF (.pdf) only. **Output Types:** - `structured`: Structured data extraction. Requires one of: category_id (with schema & instructions) - `markdown`: Page-by-page OCR. All configuration fields are optional - `per_page_structured`: Per-page structured extraction (future or hybrid mode) **Note:** Only one of category_id, schema, or instruction can be provided per request

### Example

```python
import time
import os
import openapi_client
from openapi_client.models.upload_initiate_upload_request import UploadInitiateUploadRequest
from openapi_client.models.upload_presigned_upload_response import UploadPresignedUploadResponse
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8080/api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost:8080/api/v1"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.SDKApi(api_client)
    upload_initiate_upload_request = openapi_client.UploadInitiateUploadRequest() # UploadInitiateUploadRequest | Upload initiation request

    try:
        # Presigned upload
        api_response = api_instance.presigned_upload_1(upload_initiate_upload_request)
        print("The response of SDKApi->presigned_upload_1:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SDKApi->presigned_upload_1: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **upload_initiate_upload_request** | [**UploadInitiateUploadRequest**](UploadInitiateUploadRequest.md)| Upload initiation request | 

### Return type

[**UploadPresignedUploadResponse**](UploadPresignedUploadResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**400** | Bad Request |  -  |
**401** | Unauthorized |  -  |
**402** | Insufficient credits |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **upload_from_url_1**
> UploadURLUploadResponse upload_from_url_1(upload_url_upload_request)

Public URL upload

Create a job and start processing from a public URL. Supported format: PDF (.pdf) only. **Output Types:** - `structured`: Structured data extraction. Requires one of: category_id (with schema & instructions) - `markdown`: Page-by-page OCR. All configuration fields are optional - `per_page_structured`: Per-page structured extraction (future or hybrid mode) **Note:** Only one of category_id, schema, or instruction can be provided per request

### Example

```python
import time
import os
import openapi_client
from openapi_client.models.upload_url_upload_request import UploadURLUploadRequest
from openapi_client.models.upload_url_upload_response import UploadURLUploadResponse
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost:8080/api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost:8080/api/v1"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.SDKApi(api_client)
    upload_url_upload_request = openapi_client.UploadURLUploadRequest() # UploadURLUploadRequest | URL upload request

    try:
        # Public URL upload
        api_response = api_instance.upload_from_url_1(upload_url_upload_request)
        print("The response of SDKApi->upload_from_url_1:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SDKApi->upload_from_url_1: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **upload_url_upload_request** | [**UploadURLUploadRequest**](UploadURLUploadRequest.md)| URL upload request | 

### Return type

[**UploadURLUploadResponse**](UploadURLUploadResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**400** | Bad Request |  -  |
**401** | Unauthorized |  -  |
**402** | Insufficient credits |  -  |
**500** | Internal Server Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

