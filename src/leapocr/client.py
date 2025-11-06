"""
LeapOCR Python SDK - Main Client

This module provides the main LeapOCRClient class that wraps the generated
OpenAPI client to provide a clean, pythonic interface.
"""

import asyncio
import io
from pathlib import Path

import httpx

from .exceptions import (
    LeapOCRAuthenticationError,
    LeapOCRClientError,
    LeapOCRNotFoundError,
    LeapOCRRateLimitError,
    LeapOCRServerError,
    LeapOCRTimeoutError,
    LeapOCRValidationError,
)
from .gen.openapi_client import Configuration, LeapOCRGenClient
from .gen.openapi_client.exceptions import ApiException
from .types import (
    FileUploadResult,
    Job,
    JobResult,
    JobStatus,
    ProcessFormat,
    ProcessTier,
)


class LeapOCRClient:
    """Main LeapOCR client providing a clean, pythonic interface."""

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.leapocr.com",
        timeout: float = 30.0,
        max_retries: int = 3,
        user_agent: str | None = None,
    ):
        """
        Initialize the LeapOCR client.

        Args:
            api_key: Your LeapOCR API key
            base_url: Base URL for the API (default: https://api.leapocr.com)
            timeout: Request timeout in seconds (default: 30.0)
            max_retries: Maximum number of retry attempts (default: 3)
            user_agent: Custom user agent string

        Raises:
            LeapOCRClientError: If API key is not provided
        """
        if not api_key:
            raise LeapOCRClientError("API key is required")

        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.user_agent = user_agent or "leapocr-python/0.1.0"

        # Configure the generated client
        self._config = Configuration(
            host=self.base_url,
            api_key={"Bearer": self.api_key},
            api_key_prefix={"Bearer": "Bearer"},
        )

        # Create sync and async HTTP clients
        self._http_client = httpx.Client(
            timeout=timeout,
            headers={
                "User-Agent": self.user_agent,
                "Authorization": f"Bearer {self.api_key}",
            },
        )

        self._async_http_client = httpx.AsyncClient(
            timeout=timeout,
            headers={
                "User-Agent": self.user_agent,
                "Authorization": f"Bearer {self.api_key}",
            },
        )

        # Initialize the generated client
        self._gen_client = LeapOCRGenClient(configuration=self._config)

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close_async()

    def close(self):
        """Close the HTTP client."""
        if hasattr(self, "_http_client"):
            self._http_client.close()

    async def close_async(self):
        """Close the async HTTP client."""
        if hasattr(self, "_async_http_client"):
            await self._async_http_client.aclose()

    def _handle_api_error(self, error: ApiException) -> None:
        """Convert generated API exceptions to custom exceptions."""
        status_code = getattr(error, "status", None)

        if status_code == 401:
            raise LeapOCRAuthenticationError("Invalid API key or authentication failed")
        elif status_code == 403:
            raise LeapOCRAuthenticationError(
                "Access forbidden - check API key permissions"
            )
        elif status_code == 404:
            raise LeapOCRNotFoundError("Resource not found")
        elif status_code == 422:
            raise LeapOCRValidationError(f"Validation error: {error.body}")
        elif status_code == 429:
            raise LeapOCRRateLimitError("Rate limit exceeded")
        elif status_code and 500 <= status_code < 600:
            raise LeapOCRServerError(f"Server error: {error.body}")
        else:
            raise LeapOCRClientError(f"API error: {error}")

    # OCR Processing Methods
    def process_url(
        self,
        url: str,
        format: ProcessFormat | str = ProcessFormat.STRUCTURED,
        tier: ProcessTier | str = ProcessTier.CORE,
        project_id: str | None = None,
        schema_id: str | None = None,
        instruction_id: str | None = None,
        category_id: str | None = None,
        webhook_url: str | None = None,
    ) -> Job:
        """
        Process a document from URL.

        Args:
            url: URL of the document to process
            format: Processing format (structured, text, etc.)
            tier: Processing tier (core, premium, etc.)
            project_id: Project ID to associate with the job
            schema_id: Custom schema ID for structured extraction
            instruction_id: Custom instruction ID
            category_id: Document category ID
            webhook_url: Webhook URL for job completion notification

        Returns:
            Job object with job ID and status

        Raises:
            LeapOCRClientError: If the request fails
        """
        try:
            # Convert enum values to strings
            format_str = (
                format.value if isinstance(format, ProcessFormat) else str(format)
            )
            tier_str = tier.value if isinstance(tier, ProcessTier) else str(tier)

            from .gen.openapi_client.models.upload_url_upload_request import (
                UploadURLUploadRequest,
            )

            request = UploadURLUploadRequest(
                url=url,
                format=format_str,
                tier=tier_str,
                project_id=project_id,
                schema_id=schema_id,
                instruction_id=instruction_id,
                category_id=category_id,
                webhook_url=webhook_url,
            )

            response = self._gen_client.upload_from_url_with_http_info(request)
            result_data = response.data

            return Job(
                id=result_data.job_id,
                status=result_data.status or "pending",
                created_at=getattr(result_data, "created_at", None),
            )

        except ApiException as e:
            self._handle_api_error(e)
        except Exception as e:
            raise LeapOCRClientError(f"Unexpected error processing URL: {e}")

    async def process_url_async(
        self,
        url: str,
        format: ProcessFormat | str = ProcessFormat.STRUCTURED,
        tier: ProcessTier | str = ProcessTier.CORE,
        project_id: str | None = None,
        schema_id: str | None = None,
        instruction_id: str | None = None,
        category_id: str | None = None,
        webhook_url: str | None = None,
    ) -> Job:
        """
        Process a document from URL asynchronously.

        Args:
            url: URL of the document to process
            format: Processing format (structured, text, etc.)
            tier: Processing tier (core, premium, etc.)
            project_id: Project ID to associate with the job
            schema_id: Custom schema ID for structured extraction
            instruction_id: Custom instruction ID
            category_id: Document category ID
            webhook_url: Webhook URL for job completion notification

        Returns:
            Job object with job ID and status

        Raises:
            LeapOCRClientError: If the request fails
        """
        try:
            format_str = (
                format.value if isinstance(format, ProcessFormat) else str(format)
            )
            tier_str = tier.value if isinstance(tier, ProcessTier) else str(tier)

            from .gen.openapi_client.models.upload_url_upload_request import (
                UploadURLUploadRequest,
            )

            request = UploadURLUploadRequest(
                url=url,
                format=format_str,
                tier=tier_str,
                project_id=project_id,
                schema_id=schema_id,
                instruction_id=instruction_id,
                category_id=category_id,
                webhook_url=webhook_url,
            )

            # Note: The generated client doesn't have async methods, so we'll use sync for now
            # In a real implementation, we'd need to add async support to the generated client
            response = self._gen_client.upload_from_url_with_http_info(request)
            result_data = response.data

            return Job(
                id=result_data.job_id,
                status=result_data.status or "pending",
                created_at=getattr(result_data, "created_at", None),
            )

        except ApiException as e:
            self._handle_api_error(e)
        except Exception as e:
            raise LeapOCRClientError(f"Unexpected error processing URL async: {e}")

    def upload_file(
        self,
        file: str | Path | io.IOBase,
        format: ProcessFormat | str = ProcessFormat.STRUCTURED,
        tier: ProcessTier | str = ProcessTier.CORE,
        project_id: str | None = None,
        schema_id: str | None = None,
        instruction_id: str | None = None,
        category_id: str | None = None,
        webhook_url: str | None = None,
    ) -> FileUploadResult:
        """
        Upload a file for processing.

        Args:
            file: File path or file-like object to upload
            format: Processing format (structured, text, etc.)
            tier: Processing tier (core, premium, etc.)
            project_id: Project ID to associate with the job
            schema_id: Custom schema ID for structured extraction
            instruction_id: Custom instruction ID
            category_id: Document category ID
            webhook_url: Webhook URL for job completion notification

        Returns:
            FileUploadResult with upload details

        Raises:
            LeapOCRClientError: If the upload fails
        """
        try:
            # Get presigned upload URL
            from .gen.openapi_client.models.upload_initiate_upload_request import (
                UploadInitiateUploadRequest,
            )

            initiate_request = UploadInitiateUploadRequest(
                format=format.value
                if isinstance(format, ProcessFormat)
                else str(format),
                tier=tier.value if isinstance(tier, ProcessTier) else str(tier),
                project_id=project_id,
                schema_id=schema_id,
                instruction_id=instruction_id,
                category_id=category_id,
                webhook_url=webhook_url,
            )

            initiate_response = self._gen_client.presigned_upload_with_http_info(
                initiate_request
            )
            presigned_data = initiate_response.data

            # Read file content
            if isinstance(file, (str, Path)):
                with open(file, "rb") as f:
                    file_content = f.read()
            else:
                file_content = file.read()

            # Upload file to presigned URL
            upload_response = self._http_client.put(
                presigned_data.upload_url,
                content=file_content,
                headers=presigned_data.headers,
            )

            upload_response.raise_for_status()

            return FileUploadResult(
                job_id=presigned_data.job_id,
                upload_url=presigned_data.upload_url,
                headers=presigned_data.headers or {},
                status="uploaded",
            )

        except ApiException as e:
            self._handle_api_error(e)
        except Exception as e:
            raise LeapOCRClientError(f"Unexpected error uploading file: {e}")

    def get_job_status(self, job_id: str) -> JobStatus:
        """
        Get the status of a processing job.

        Args:
            job_id: ID of the job to check

        Returns:
            JobStatus object with current status

        Raises:
            LeapOCRClientError: If the request fails
        """
        try:
            response = self._gen_client.get_job_status_with_http_info(job_id)
            status_data = response.data

            return JobStatus(
                job_id=status_data.job_id,
                status=status_data.status,
                progress=getattr(status_data, "progress", None),
                error_message=getattr(status_data, "error_message", None),
                created_at=getattr(status_data, "created_at", None),
                updated_at=getattr(status_data, "updated_at", None),
            )

        except ApiException as e:
            self._handle_api_error(e)
        except Exception as e:
            raise LeapOCRClientError(f"Unexpected error getting job status: {e}")

    def get_job_result(self, job_id: str) -> JobResult:
        """
        Get the result of a completed job.

        Args:
            job_id: ID of the job to get results for

        Returns:
            JobResult object with processing results

        Raises:
            LeapOCRClientError: If the request fails
        """
        try:
            response = self._gen_client.get_job_result_with_http_info(job_id)
            result_data = response.data

            return JobResult(
                job_id=result_data.job_id,
                status=result_data.status,
                data=getattr(result_data, "data", None),
                pages=getattr(result_data, "pages", None),
                credits_used=getattr(result_data, "credits_used", None),
                processing_time=getattr(result_data, "processing_time", None),
                error_message=getattr(result_data, "error_message", None),
                created_at=getattr(result_data, "created_at", None),
                completed_at=getattr(result_data, "completed_at", None),
            )

        except ApiException as e:
            self._handle_api_error(e)
        except Exception as e:
            raise LeapOCRClientError(f"Unexpected error getting job result: {e}")

    def wait_for_result(
        self,
        job_id: str,
        timeout: float | None = None,
        poll_interval: float = 2.0,
    ) -> JobResult:
        """
        Wait for a job to complete and return the result.

        Args:
            job_id: ID of the job to wait for
            timeout: Maximum time to wait in seconds (None for no timeout)
            poll_interval: Time between status checks in seconds

        Returns:
            JobResult object with processing results

        Raises:
            LeapOCRTimeoutError: If the job doesn't complete within timeout
            LeapOCRClientError: If the job fails or request fails
        """
        import time

        start_time = time.time()

        while True:
            status = self.get_job_status(job_id)

            if status.status in ["completed", "failed", "cancelled"]:
                return self.get_job_result(job_id)

            # Check timeout
            if timeout and (time.time() - start_time) > timeout:
                raise LeapOCRTimeoutError(
                    f"Job {job_id} did not complete within {timeout} seconds"
                )

            # Wait before polling again
            time.sleep(poll_interval)

    async def wait_for_result_async(
        self,
        job_id: str,
        timeout: float | None = None,
        poll_interval: float = 2.0,
    ) -> JobResult:
        """
        Wait for a job to complete and return the result (async version).

        Args:
            job_id: ID of the job to wait for
            timeout: Maximum time to wait in seconds (None for no timeout)
            poll_interval: Time between status checks in seconds

        Returns:
            JobResult object with processing results

        Raises:
            LeapOCRTimeoutError: If the job doesn't complete within timeout
            LeapOCRClientError: If the job fails or request fails
        """

        start_time = asyncio.get_event_loop().time()

        while True:
            status = self.get_job_status(job_id)

            if status.status in ["completed", "failed", "cancelled"]:
                return self.get_job_result(job_id)

            # Check timeout
            if timeout and (asyncio.get_event_loop().time() - start_time) > timeout:
                raise LeapOCRTimeoutError(
                    f"Job {job_id} did not complete within {timeout} seconds"
                )

            # Wait before polling again
            await asyncio.sleep(poll_interval)
