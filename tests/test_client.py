"""
Unit tests for the LeapOCR Python SDK client.
"""

import pytest
import os
from unittest.mock import Mock, patch, MagicMock
import io
from pathlib import Path

from leapocr import LeapOCRClient
from leapocr.client import LeapOCRClient
from leapocr.exceptions import (
    LeapOCRClientError,
    LeapOCRAuthenticationError,
    LeapOCRValidationError,
    LeapOCRRateLimitError,
    LeapOCRTimeoutError,
    LeapOCRNotFoundError,
)
from leapocr.types import ProcessFormat, ProcessTier, Job, JobStatus, JobResult
from leapocr.services.ocr import OCRService


class TestLeapOCRClient:
    """Test cases for LeapOCRClient."""
    
    def test_init_with_api_key(self):
        """Test client initialization with API key."""
        client = LeapOCRClient(api_key="test_key")
        assert client.api_key == "test_key"
        assert client.base_url == "https://api.leapocr.com"
        assert client.timeout == 30.0
        assert client.max_retries == 3
    
    def test_init_without_api_key(self):
        """Test client initialization fails without API key."""
        with pytest.raises(LeapOCRClientError, match="API key is required"):
            LeapOCRClient(api_key="")
    
    def test_init_with_custom_config(self):
        """Test client initialization with custom configuration."""
        client = LeapOCRClient(
            api_key="test_key",
            base_url="https://custom.api.com",
            timeout=60.0,
            max_retries=5,
            user_agent="custom-agent",
        )
        assert client.base_url == "https://custom.api.com"
        assert client.timeout == 60.0
        assert client.max_retries == 5
        assert client.user_agent == "custom-agent"
    
    def test_context_manager(self):
        """Test client as context manager."""
        with LeapOCRClient(api_key="test_key") as client:
            assert client.api_key == "test_key"
        
        # Client should be closed after exiting context
        assert hasattr(client, '_http_client')
    
    @patch('leapocr.client.LeapOCRGenClient')
    def test_process_url_success(self, mock_gen_client):
        """Test successful URL processing."""
        # Mock the generated client response
        mock_response = Mock()
        mock_response.data = Mock()
        mock_response.data.job_id = "test_job_id"
        mock_response.data.status = "pending"
        mock_gen_client.return_value.upload_from_url_with_http_info.return_value = mock_response
        
        client = LeapOCRClient(api_key="test_key")
        
        result = client.process_url(
            url="https://example.com/doc.pdf",
            format=ProcessFormat.STRUCTURED,
            tier=ProcessTier.CORE,
        )
        
        assert isinstance(result, Job)
        assert result.id == "test_job_id"
        assert result.status == "pending"
    
    @patch('leapocr.client.LeapOCRGenClient')
    def test_process_url_with_string_format(self, mock_gen_client):
        """Test URL processing with string format."""
        mock_response = Mock()
        mock_response.data = Mock()
        mock_response.data.job_id = "test_job_id"
        mock_response.data.status = "pending"
        mock_gen_client.return_value.upload_from_url_with_http_info.return_value = mock_response
        
        client = LeapOCRClient(api_key="test_key")
        
        result = client.process_url(
            url="https://example.com/doc.pdf",
            format="structured",  # String instead of enum
            tier="core",          # String instead of enum
        )
        
        assert isinstance(result, Job)
        assert result.id == "test_job_id"
    
    @patch('leapocr.client.LeapOCRGenClient')
    def test_process_url_api_error(self, mock_gen_client):
        """Test URL processing with API error."""
        from leapocr.gen.openapi_client.exceptions import ApiException
        
        # Mock API exception
        mock_gen_client.return_value.upload_from_url_with_http_info.side_effect = ApiException(
            status=401,
            reason="Unauthorized"
        )
        
        client = LeapOCRClient(api_key="test_key")
        
        with pytest.raises(LeapOCRAuthenticationError):
            client.process_url(url="https://example.com/doc.pdf")
    
    def test_handle_api_error_401(self):
        """Test error handling for 401 status code."""
        from leapocr.gen.openapi_client.exceptions import ApiException
        
        client = LeapOCRClient(api_key="test_key")
        error = ApiException(status=401, reason="Unauthorized")
        
        with pytest.raises(LeapOCRAuthenticationError):
            client._handle_api_error(error)
    
    def test_handle_api_error_404(self):
        """Test error handling for 404 status code."""
        from leapocr.gen.openapi_client.exceptions import ApiException
        
        client = LeapOCRClient(api_key="test_key")
        error = ApiException(status=404, reason="Not Found")
        
        with pytest.raises(LeapOCRNotFoundError):
            client._handle_api_error(error)
    
    def test_handle_api_error_422(self):
        """Test error handling for 422 status code."""
        from leapocr.gen.openapi_client.exceptions import ApiException
        
        client = LeapOCRClient(api_key="test_key")
        error = ApiException(status=422, reason="Validation Error", body={"detail": "Invalid input"})
        
        with pytest.raises(LeapOCRValidationError):
            client._handle_api_error(error)
    
    def test_handle_api_error_429(self):
        """Test error handling for 429 status code."""
        from leapocr.gen.openapi_client.exceptions import ApiException
        
        client = LeapOCRClient(api_key="test_key")
        error = ApiException(status=429, reason="Rate Limit Exceeded")
        
        with pytest.raises(LeapOCRRateLimitError):
            client._handle_api_error(error)
    
    def test_handle_api_error_500(self):
        """Test error handling for 500 status code."""
        from leapocr.gen.openapi_client.exceptions import ApiException
        
        client = LeapOCRClient(api_key="test_key")
        error = ApiException(status=500, reason="Internal Server Error")
        
        with pytest.raises(LeapOCRClientError) as exc_info:
            client._handle_api_error(error)
        
        assert exc_info.value.is_retryable()
    
    @patch('leapocr.client.LeapOCRGenClient')
    def test_upload_file_success(self, mock_gen_client):
        """Test successful file upload."""
        # Mock presigned upload response
        mock_presigned_response = Mock()
        mock_presigned_response.data = Mock()
        mock_presigned_response.data.job_id = "upload_job_id"
        mock_presigned_response.data.upload_url = "https://upload.url.com"
        mock_presigned_response.data.headers = {"Content-Type": "application/pdf"}
        
        mock_gen_client.return_value.presigned_upload_with_http_info.return_value = mock_presigned_response
        
        # Mock HTTP client
        mock_upload_response = Mock()
        mock_upload_response.raise_for_status.return_value = None
        
        client = LeapOCRClient(api_key="test_key")
        client._http_client = Mock()
        client._http_client.put.return_value = mock_upload_response
        
        # Test with file-like object
        file_content = io.BytesIO(b"fake pdf content")
        result = client.upload_file(file=file_content)
        
        assert result.job_id == "upload_job_id"
        assert result.upload_url == "https://upload.url.com"
        assert result.headers == {"Content-Type": "application/pdf"}
    
    @patch('leapocr.client.LeapOCRGenClient')
    def test_get_job_status_success(self, mock_gen_client):
        """Test successful job status retrieval."""
        mock_response = Mock()
        mock_response.data = Mock()
        mock_response.data.job_id = "test_job_id"
        mock_response.data.status = "processing"
        mock_response.data.progress = 50.0
        mock_gen_client.return_value.get_job_status_with_http_info.return_value = mock_response
        
        client = LeapOCRClient(api_key="test_key")
        status = client.get_job_status("test_job_id")
        
        assert status.job_id == "test_job_id"
        assert status.status == "processing"
        assert status.progress == 50.0
    
    @patch('leapocr.client.LeapOCRGenClient')
    def test_get_job_result_success(self, mock_gen_client):
        """Test successful job result retrieval."""
        mock_response = Mock()
        mock_response.data = Mock()
        mock_response.data.job_id = "test_job_id"
        mock_response.data.status = "completed"
        mock_response.data.data = {"extracted_text": "Sample text"}
        mock_response.data.credits_used = 10
        mock_gen_client.return_value.get_job_result_with_http_info.return_value = mock_response
        
        client = LeapOCRClient(api_key="test_key")
        result = client.get_job_result("test_job_id")
        
        assert result.job_id == "test_job_id"
        assert result.status == "completed"
        assert result.data == {"extracted_text": "Sample text"}
        assert result.credits_used == 10
    
    @patch('leapocr.client.LeapOCRClient.get_job_status')
    @patch('leapocr.client.LeapOCRClient.get_job_result')
    def test_wait_for_result_success(self, mock_get_result, mock_get_status):
        """Test successful waiting for job result."""
        from datetime import datetime
        
        # Mock status updates
        mock_get_status.side_effect = [
            Mock(status="processing", progress=25.0),
            Mock(status="processing", progress=75.0),
            Mock(status="completed", progress=100.0),
        ]
        
        # Mock final result
        mock_result = Mock()
        mock_result.job_id = "test_job_id"
        mock_result.status = "completed"
        mock_result.data = {"result": "success"}
        mock_get_result.return_value = mock_result
        
        client = LeapOCRClient(api_key="test_key")
        result = client.wait_for_result("test_job_id", timeout=10, poll_interval=0.1)
        
        assert result.status == "completed"
        assert result.data == {"result": "success"}
        assert mock_get_status.call_count == 3
    
    @patch('leapocr.client.LeapOCRClient.get_job_status')
    def test_wait_for_result_timeout(self, mock_get_status):
        """Test timeout when waiting for job result."""
        # Mock status that never completes
        mock_get_status.return_value = Mock(status="processing", progress=50.0)
        
        client = LeapOCRClient(api_key="test_key")
        
        with pytest.raises(LeapOCRTimeoutError):
            client.wait_for_result("test_job_id", timeout=0.5, poll_interval=0.1)


class TestOCRService:
    """Test cases for OCRService."""
    
    def test_service_init(self):
        """Test OCR service initialization."""
        client = Mock(spec=LeapOCRClient)
        service = OCRService(client)
        assert service.client == client
    
    @patch('leapocr.services.ocr.OCRService._process_url')
    def test_process_document_url(self, mock_process_url):
        """Test processing document from URL."""
        mock_job = Mock(spec=Job)
        mock_process_url.return_value = mock_job
        
        client = Mock(spec=LeapOCRClient)
        service = OCRService(client)
        
        result = service.process_document("https://example.com/doc.pdf")
        
        mock_process_url.assert_called_once()
        assert result == mock_job
    
    @patch('leapocr.services.ocr.OCRService._process_file')
    def test_process_document_file_path(self, mock_process_file):
        """Test processing document from file path."""
        mock_job = Mock(spec=Job)
        mock_process_file.return_value = mock_job
        
        client = Mock(spec=LeapOCRClient)
        service = OCRService(client)
        
        result = service.process_document("/path/to/document.pdf")
        
        mock_process_file.assert_called_once()
        assert result == mock_job
    
    @patch('leapocr.services.ocr.OCRService._process_file')
    def test_process_document_file_like_object(self, mock_process_file):
        """Test processing document from file-like object."""
        mock_job = Mock(spec=Job)
        mock_process_file.return_value = mock_job
        
        client = Mock(spec=LeapOCRClient)
        service = OCRService(client)
        
        file_obj = io.BytesIO(b"fake content")
        result = service.process_document(file_obj)
        
        mock_process_file.assert_called_once()
        assert result == mock_job
    
    def test_extract_text_success(self):
        """Test successful text extraction."""
        mock_result = Mock()
        mock_result.data = {"text": "Sample extracted text"}
        
        client = Mock(spec=LeapOCRClient)
        service = OCRService(client)
        
        with patch.object(service, 'process_document', return_value=mock_result):
            text = service.extract_text("https://example.com/doc.pdf")
            assert text == "Sample extracted text"
    
    def test_extract_text_failure(self):
        """Test text extraction failure."""
        mock_result = Mock()
        mock_result.data = None
        
        client = Mock(spec=LeapOCRClient)
        service = OCRService(client)
        
        with patch.object(service, 'process_document', return_value=mock_result):
            with pytest.raises(LeapOCRClientError):
                service.extract_text("https://example.com/doc.pdf")
    
    def test_extract_structured_data_success(self):
        """Test successful structured data extraction."""
        expected_data = {"invoice_number": "INV-001", "amount": 100.0}
        mock_result = Mock()
        mock_result.data = expected_data
        
        client = Mock(spec=LeapOCRClient)
        service = OCRService(client)
        
        with patch.object(service, 'process_document', return_value=mock_result):
            data = service.extract_structured_data("https://example.com/doc.pdf")
            assert data == expected_data
    
    def test_validate_job_result(self):
        """Test job result validation."""
        from leapocr.types import JobResult
        
        # Valid completed result
        valid_result = JobResult(
            job_id="test_job",
            status="completed",
            data={"extracted": True},
        )
        
        client = Mock(spec=LeapOCRClient)
        service = OCRService(client)
        
        assert service.validate_job_result(valid_result) is True
        
        # Invalid result - not completed
        invalid_result = JobResult(
            job_id="test_job",
            status="processing",
            data={"extracted": True},
        )
        assert service.validate_job_result(invalid_result) is False
        
        # Invalid result - has error
        error_result = JobResult(
            job_id="test_job",
            status="completed",
            error_message="Processing failed",
        )
        assert service.validate_job_result(error_result) is False


class TestExceptions:
    """Test cases for custom exceptions."""
    
    def test_base_exception_properties(self):
        """Test base exception properties."""
        exc = LeapOCRClientError("Test error", status_code=400)
        assert exc.message == "Test error"
        assert exc.status_code == 400
        assert exc.is_retryable() is False
    
    def test_server_exception_retryable(self):
        """Test server exception is retryable."""
        exc = LeapOCRClientError("Server error", error_type="server_error")
        assert exc.is_retryable() is True
    
    def test_authentication_exception_not_retryable(self):
        """Test authentication exception is not retryable."""
        exc = LeapOCRAuthenticationError("Auth failed")
        assert exc.is_retryable() is False
    
    def test_validation_exception_not_retryable(self):
        """Test validation exception is not retryable."""
        exc = LeapOCRValidationError("Validation failed")
        assert exc.is_retryable() is False
    
    def test_rate_limit_exception_retryable(self):
        """Test rate limit exception is retryable."""
        exc = LeapOCRRateLimitError("Rate limited")
        assert exc.is_retryable() is True
    
    def test_timeout_exception_retryable(self):
        """Test timeout exception is retryable."""
        exc = LeapOCRTimeoutError("Timeout")
        assert exc.is_retryable() is True


class TestTypes:
    """Test cases for types and enums."""
    
    def test_process_format_enum(self):
        """Test ProcessFormat enum values."""
        assert ProcessFormat.STRUCTURED == "structured"
        assert ProcessFormat.TEXT == "text"
        assert ProcessFormat.TABLES == "tables"
        assert ProcessFormat.FORMS == "forms"
    
    def test_process_tier_enum(self):
        """Test ProcessTier enum values."""
        assert ProcessTier.CORE == "core"
        assert ProcessTier.PREMIUM == "premium"
        assert ProcessTier.ENTERPRISE == "enterprise"
    
    def test_job_status_enum(self):
        """Test JobStatus enum values."""
        assert JobStatus.PENDING == "pending"
        assert JobStatus.PROCESSING == "processing"
        assert JobStatus.COMPLETED == "completed"
        assert JobStatus.FAILED == "failed"
        assert JobStatus.CANCELLED == "cancelled"
    
    def test_job_dataclass(self):
        """Test Job dataclass."""
        job = Job(id="test_job", status="pending")
        assert job.id == "test_job"
        assert job.status == "pending"
        assert job.created_at is None
    
    def test_job_status_conversion(self):
        """Test Job status string to enum conversion."""
        job = Job(id="test_job", status="PENDING")
        assert job.status == JobStatus.PENDING
        
        # Test invalid status remains as string
        job_invalid = Job(id="test_job", status="invalid_status")
        assert job_invalid.status == "invalid_status"
    
    def test_job_result_dataclass(self):
        """Test JobResult dataclass."""
        result = JobResult(
            job_id="test_job",
            status="completed",
            data={"extracted": True},
            credits_used=10,
        )
        assert result.job_id == "test_job"
        assert result.status == "completed"
        assert result.data == {"extracted": True}
        assert result.credits_used == 10