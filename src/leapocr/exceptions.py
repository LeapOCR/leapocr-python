"""
LeapOCR Python SDK - Custom Exceptions

This module defines custom exception classes for the LeapOCR SDK.
"""

from typing import Any


class LeapOCRClientError(Exception):
    """Base exception for all LeapOCR client errors."""

    def __init__(
        self,
        message: str,
        error_type: str | None = None,
        status_code: int | None = None,
        response_body: dict[str, Any] | None = None,
    ):
        super().__init__(message)
        self.message = message
        self.error_type = error_type or "client_error"
        self.status_code = status_code
        self.response_body = response_body or {}

    def __str__(self) -> str:
        return f"LeapOCRClientError: {self.message}"

    def is_retryable(self) -> bool:
        """Whether this error can be retried."""
        return False


class LeapOCRServerError(LeapOCRClientError):
    """Exception for server-side errors (5xx status codes)."""

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        response_body: dict[str, Any] | None = None,
    ):
        super().__init__(message, "server_error", status_code, response_body)
        self.error_type = "server_error"

    def is_retryable(self) -> bool:
        """Server errors are generally retryable."""
        return True


class LeapOCRAuthenticationError(LeapOCRClientError):
    """Exception for authentication errors (401, 403 status codes)."""

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        response_body: dict[str, Any] | None = None,
    ):
        super().__init__(message, "authentication_error", status_code, response_body)
        self.error_type = "authentication_error"

    def is_retryable(self) -> bool:
        """Authentication errors are not retryable without fixing credentials."""
        return False


class LeapOCRValidationError(LeapOCRClientError):
    """Exception for validation errors (422 status code)."""

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        response_body: dict[str, Any] | None = None,
    ):
        super().__init__(message, "validation_error", status_code, response_body)
        self.error_type = "validation_error"

    def is_retryable(self) -> bool:
        """Validation errors are not retryable without fixing the request."""
        return False


class LeapOCRRateLimitError(LeapOCRClientError):
    """Exception for rate limit errors (429 status code)."""

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        response_body: dict[str, Any] | None = None,
    ):
        super().__init__(message, "rate_limit_error", status_code, response_body)
        self.error_type = "rate_limit_error"

    def is_retryable(self) -> bool:
        """Rate limit errors are retryable after delay."""
        return True


class LeapOCRTimeoutError(LeapOCRClientError):
    """Exception for timeout errors."""

    def __init__(self, message: str, timeout_seconds: float | None = None):
        super().__init__(message, "timeout_error")
        self.timeout_seconds = timeout_seconds
        self.error_type = "timeout_error"

    def is_retryable(self) -> bool:
        """Timeout errors are retryable."""
        return True


class LeapOCRNotFoundError(LeapOCRClientError):
    """Exception for resource not found errors (404 status code)."""

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        response_body: dict[str, Any] | None = None,
    ):
        super().__init__(message, "not_found_error", status_code, response_body)
        self.error_type = "not_found_error"

    def is_retryable(self) -> bool:
        """Not found errors are not retryable."""
        return False


class LeapOCRUploadError(LeapOCRClientError):
    """Exception for file upload errors."""

    def __init__(self, message: str, file_name: str | None = None):
        super().__init__(message, "upload_error")
        self.file_name = file_name
        self.error_type = "upload_error"

    def is_retryable(self) -> bool:
        """Upload errors may be retryable depending on the cause."""
        return True


class LeapOCRJobError(LeapOCRClientError):
    """Exception for job processing errors."""

    def __init__(
        self, message: str, job_id: str | None = None, job_status: str | None = None
    ):
        super().__init__(message, "job_error")
        self.job_id = job_id
        self.job_status = job_status
        self.error_type = "job_error"

    def is_retryable(self) -> bool:
        """Job errors are generally not retryable for the same job."""
        return False


class LeapOCRConfigurationError(LeapOCRClientError):
    """Exception for configuration errors."""

    def __init__(self, message: str, config_key: str | None = None):
        super().__init__(message, "configuration_error")
        self.config_key = config_key
        self.error_type = "configuration_error"

    def is_retryable(self) -> bool:
        """Configuration errors are not retryable without fixing the configuration."""
        return False


class LeapOCRExceptionMapper:
    """Maps generated API exceptions to custom exceptions."""

    @staticmethod
    def map_exception(error: Exception) -> LeapOCRClientError:
        """
        Map a generated API exception to a custom exception.

        Args:
            error: The original exception

        Returns:
            Mapped custom exception
        """
        # Try to get status code from ApiException
        status_code = getattr(error, "status", None)
        body = getattr(error, "body", {})

        if status_code:
            if status_code == 401:
                return LeapOCRAuthenticationError(
                    "Invalid API key or authentication failed",
                    status_code=status_code,
                    response_body=body,
                )
            elif status_code == 403:
                return LeapOCRAuthenticationError(
                    "Access forbidden - check API key permissions",
                    status_code=status_code,
                    response_body=body,
                )
            elif status_code == 404:
                return LeapOCRNotFoundError(
                    "Resource not found",
                    status_code=status_code,
                    response_body=body,
                )
            elif status_code == 422:
                return LeapOCRValidationError(
                    f"Validation error: {body}",
                    status_code=status_code,
                    response_body=body,
                )
            elif status_code == 429:
                return LeapOCRRateLimitError(
                    "Rate limit exceeded",
                    status_code=status_code,
                    response_body=body,
                )
            elif 500 <= status_code < 600:
                return LeapOCRServerError(
                    f"Server error: {body}",
                    status_code=status_code,
                    response_body=body,
                )

        # Default to generic client error
        return LeapOCRClientError(str(error))
