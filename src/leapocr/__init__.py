"""
LeapOCR Python SDK

A modern, type-safe Python SDK for the LeapOCR API.
"""

__version__ = "0.1.0"
__author__ = "LeapOCR"
__email__ = "support@leapocr.com"
__license__ = "MIT"

# Import main classes and types for public API
from .client import LeapOCRClient
from .exceptions import (
    LeapOCRClientError,
    LeapOCRServerError,
    LeapOCRAuthenticationError,
    LeapOCRValidationError,
    LeapOCRRateLimitError,
    LeapOCRTimeoutError,
    LeapOCRNotFoundError,
    LeapOCRUploadError,
    LeapOCRJobError,
    LeapOCRConfigurationError,
)
from .types import (
    ProcessFormat,
    ProcessTier,
    UploadMethod,
    JobStatus,
    Job,
    JobStatusInfo,
    JobResult,
    FileUploadResult,
    ClientConfig,
    RetryConfig,
    UploadOptions,
    ProcessOptions,
    PageResult,
    AnalyticsData,
    CreditUsage,
)

# Export public API
__all__ = [
    # Main client
    "LeapOCRClient",
    
    # Exceptions
    "LeapOCRClientError",
    "LeapOCRServerError",
    "LeapOCRAuthenticationError",
    "LeapOCRValidationError",
    "LeapOCRRateLimitError",
    "LeapOCRTimeoutError",
    "LeapOCRNotFoundError",
    "LeapOCRUploadError",
    "LeapOCRJobError",
    "LeapOCRConfigurationError",
    
    # Types and enums
    "ProcessFormat",
    "ProcessTier",
    "UploadMethod",
    "JobStatus",
    "Job",
    "JobStatusInfo",
    "JobResult",
    "FileUploadResult",
    "ClientConfig",
    "RetryConfig",
    "UploadOptions",
    "ProcessOptions",
    "PageResult",
    "AnalyticsData",
    "CreditUsage",
]

# Convenience function for quick client creation
def create_client(
    api_key: str,
    base_url: str = "https://api.leapocr.com",
    **kwargs
) -> LeapOCRClient:
    """
    Create a LeapOCR client with common configuration.
    
    Args:
        api_key: Your LeapOCR API key
        base_url: Base URL for the API (default: https://api.leapocr.com)
        **kwargs: Additional client configuration options
        
    Returns:
        Configured LeapOCRClient instance
    """
    return LeapOCRClient(api_key=api_key, base_url=base_url, **kwargs)


# Version checking utility
def check_version(minimum_version: str) -> bool:
    """
    Check if the current SDK version meets the minimum requirement.
    
    Args:
        minimum_version: Minimum version required (e.g., "0.1.0")
        
    Returns:
        True if current version meets or exceeds minimum, False otherwise
    """
    from packaging.version import parse
    
    try:
        current = parse(__version__)
        minimum = parse(minimum_version)
        return current >= minimum
    except Exception:
        # If version parsing fails, assume compatible
        return True


# Utility function to validate API key format
def validate_api_key(api_key: str) -> bool:
    """
    Validate the format of an API key.
    
    Args:
        api_key: The API key to validate
        
    Returns:
        True if the API key format appears valid, False otherwise
    """
    if not api_key:
        return False
    
    # Basic format validation
    # LeapOCR API keys typically start with "pk_live_" or "pk_test_"
    return api_key.startswith(("pk_live_", "pk_test_")) and len(api_key) >= 40