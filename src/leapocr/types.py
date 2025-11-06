"""
LeapOCR Python SDK - Types and Enums

This module defines custom types and enums used throughout the SDK.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any


class ProcessFormat(str, Enum):
    """Processing format options."""

    STRUCTURED = "structured"
    TEXT = "text"
    TABLES = "tables"
    FORMS = "forms"


class ProcessTier(str, Enum):
    """Processing tier options."""

    CORE = "core"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"


class UploadMethod(str, Enum):
    """File upload methods."""

    PRESIGNED = "presigned"
    DIRECT = "direct"


class JobStatus(str, Enum):
    """Job status values."""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class Job:
    """Represents a processing job."""

    id: str
    status: JobStatus | str
    created_at: datetime | None = None

    def __post_init__(self):
        if isinstance(self.status, str):
            try:
                self.status = JobStatus(self.status.lower())
            except ValueError:
                pass  # Keep as string if not a valid enum value


@dataclass
class JobStatusInfo:
    """Detailed job status information."""

    job_id: str
    status: JobStatus | str
    progress: float | None = None
    error_message: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    def __post_init__(self):
        if isinstance(self.status, str):
            try:
                self.status = JobStatus(self.status.lower())
            except ValueError:
                pass  # Keep as string if not a valid enum value


@dataclass
class JobResult:
    """Represents the result of a completed job."""

    job_id: str
    status: JobStatus | str
    data: dict[str, Any] | None = None
    pages: list[dict[str, Any]] | None = None
    credits_used: int | None = None
    processing_time: float | None = None
    error_message: str | None = None
    created_at: datetime | None = None
    completed_at: datetime | None = None

    def __post_init__(self):
        if isinstance(self.status, str):
            try:
                self.status = JobStatus(self.status.lower())
            except ValueError:
                pass  # Keep as string if not a valid enum value


@dataclass
class FileUploadResult:
    """Represents the result of a file upload operation."""

    job_id: str
    upload_url: str
    headers: dict[str, str]
    status: str = "uploaded"
    file_name: str | None = None
    file_size: int | None = None
    content_type: str | None = None


@dataclass
class ClientConfig:
    """Configuration for the LeapOCR client."""

    api_key: str
    base_url: str = "https://api.leapocr.com"
    timeout: float = 30.0
    max_retries: int = 3
    user_agent: str | None = None
    verify_ssl: bool = True
    proxy: dict[str, str] | None = None

    def __post_init__(self):
        self.base_url = self.base_url.rstrip("/")
        if not self.user_agent:
            import leapocr

            self.user_agent = f"leapocr-python/{leapocr.__version__}"


@dataclass
class RetryConfig:
    """Configuration for retry behavior."""

    max_retries: int = 3
    base_delay: float = 1.0
    max_delay: float = 60.0
    exponential_base: float = 2.0
    jitter: bool = True
    retryable_status_codes: set = {429, 500, 502, 503, 504}


@dataclass
class UploadOptions:
    """Options for file upload."""

    format: ProcessFormat | str = ProcessFormat.STRUCTURED
    tier: ProcessTier | str = ProcessTier.CORE
    project_id: str | None = None
    schema_id: str | None = None
    instruction_id: str | None = None
    category_id: str | None = None
    webhook_url: str | None = None
    method: UploadMethod = UploadMethod.PRESIGNED

    def __post_init__(self):
        if isinstance(self.format, str):
            try:
                self.format = ProcessFormat(self.format.lower())
            except ValueError:
                pass  # Keep as string if not a valid enum value

        if isinstance(self.tier, str):
            try:
                self.tier = ProcessTier(self.tier.lower())
            except ValueError:
                pass  # Keep as string if not a valid enum value


@dataclass
class ProcessOptions:
    """Options for document processing."""

    format: ProcessFormat | str = ProcessFormat.STRUCTURED
    tier: ProcessTier | str = ProcessTier.CORE
    project_id: str | None = None
    schema_id: str | None = None
    instruction_id: str | None = None
    category_id: str | None = None
    webhook_url: str | None = None
    timeout: float | None = None
    poll_interval: float = 2.0

    def __post_init__(self):
        if isinstance(self.format, str):
            try:
                self.format = ProcessFormat(self.format.lower())
            except ValueError:
                pass  # Keep as string if not a valid enum value

        if isinstance(self.tier, str):
            try:
                self.tier = ProcessTier(self.tier.lower())
            except ValueError:
                pass  # Keep as string if not a valid enum value


@dataclass
class PageResult:
    """Represents extraction results for a single page."""

    page_number: int
    data: dict[str, Any] | None = None
    text: str | None = None
    tables: list[dict[str, Any]] | None = None
    confidence: float | None = None
    processing_time: float | None = None


@dataclass
class AnalyticsData:
    """Represents analytics data."""

    total_jobs: int
    completed_jobs: int
    failed_jobs: int
    total_credits_used: int
    average_processing_time: float
    success_rate: float
    jobs_by_status: dict[str, int]
    credits_by_project: dict[str, int]
    timeline_data: list[dict[str, Any]]


@dataclass
class CreditUsage:
    """Represents credit usage information."""

    available: int
    used: int
    total: int
    reset_date: datetime | None = None
    usage_history: list[dict[str, Any]] = None


# Type aliases for better readability
JobID = str
ProjectID = str
SchemaID = str
InstructionID = str
CategoryID = str
WebhookURL = str
APIKey = str
TimeoutSeconds = float
RetryCount = int
