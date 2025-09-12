# openapi_client.UploadApi

All URIs are relative to *http://localhost:8080/api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**presigned_upload_0**](UploadApi.md#presigned_upload_0) | **POST** /ocr/uploads/presigned | Presigned upload
[**upload_from_url_0**](UploadApi.md#upload_from_url_0) | **POST** /ocr/uploads/url | Public URL upload


# **presigned_upload_0**
> UploadPresignedUploadResponse presigned_upload_0(upload_initiate_upload_request)

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
    api_instance = openapi_client.UploadApi(api_client)
    upload_initiate_upload_request = openapi_client.UploadInitiateUploadRequest() # UploadInitiateUploadRequest | Upload initiation request

    try:
        # Presigned upload
        api_response = api_instance.presigned_upload_0(upload_initiate_upload_request)
        print("The response of UploadApi->presigned_upload_0:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UploadApi->presigned_upload_0: %s\n" % e)
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

# **upload_from_url_0**
> UploadURLUploadResponse upload_from_url_0(upload_url_upload_request)

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
    api_instance = openapi_client.UploadApi(api_client)
    upload_url_upload_request = openapi_client.UploadURLUploadRequest() # UploadURLUploadRequest | URL upload request

    try:
        # Public URL upload
        api_response = api_instance.upload_from_url_0(upload_url_upload_request)
        print("The response of UploadApi->upload_from_url_0:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling UploadApi->upload_from_url_0: %s\n" % e)
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

