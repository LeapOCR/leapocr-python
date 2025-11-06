"""
Integration tests for the LeapOCR Python SDK.

These tests require a live API and valid API key.
Set the LEAPOCR_API_KEY environment variable to run these tests.
"""

import os

import pytest

from leapocr import LeapOCRClient, ProcessFormat, ProcessTier
from leapocr.exceptions import LeapOCRClientError

# Skip integration tests if no API key is provided
pytestmark = pytest.mark.skipif(
    not os.getenv("LEAPOCR_API_KEY"),
    reason="LEAPOCR_API_KEY environment variable is required for integration tests",
)


class TestLeapOCRClientIntegration:
    """Integration tests for LeapOCRClient."""

    @pytest.fixture
    def client(self):
        """Create a real client for integration testing."""
        api_key = os.getenv("LEAPOCR_API_KEY")
        return LeapOCRClient(api_key=api_key)

    def test_client_initialization(self, client):
        """Test client initialization with real API key."""
        assert client.api_key.startswith("pk_")
        assert client.base_url == "https://api.leapocr.com"
        assert client.timeout == 30.0

    @pytest.mark.slow
    def test_process_url_integration(self, client):
        """Test real URL processing."""
        url = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"

        try:
            job = client.process_url(
                url=url,
                format=ProcessFormat.TEXT,
                tier=ProcessTier.CORE,
            )

            assert job.id is not None
            assert len(job.id) > 0
            assert job.status in ["pending", "processing"]

        except LeapOCRClientError as e:
            pytest.fail(f"URL processing failed: {e}")

    @pytest.mark.slow
    def test_get_job_status_integration(self, client):
        """Test getting job status."""
        # First submit a job
        url = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
        job = client.process_url(url=url, format=ProcessFormat.TEXT)

        # Then check its status
        try:
            status = client.get_job_status(job.id)
            assert status.job_id == job.id
            assert status.status is not None

        except LeapOCRClientError as e:
            pytest.fail(f"Getting job status failed: {e}")

    @pytest.mark.slow
    def test_wait_for_result_integration(self, client):
        """Test waiting for job completion."""
        url = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"

        try:
            # Submit job
            job = client.process_url(url=url, format=ProcessFormat.TEXT)

            # Wait for result (with reasonable timeout)
            result = client.wait_for_result(job.id, timeout=60)

            assert result.job_id == job.id
            assert result.status in ["completed", "failed"]

            if result.status == "completed":
                assert result.data is not None
                assert result.credits_used is not None
                assert result.credits_used > 0

        except LeapOCRClientError as e:
            pytest.fail(f"Waiting for result failed: {e}")

    @pytest.mark.slow
    def test_upload_file_integration(self, client):
        """Test file upload integration."""
        # Create a minimal PDF content (real PDF would be better)
        pdf_content = (
            b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n"
        )

        try:
            upload_result = client.upload_file(
                file=io.BytesIO(pdf_content),
                format=ProcessFormat.TEXT,
                tier=ProcessTier.CORE,
            )

            assert upload_result.job_id is not None
            assert len(upload_result.job_id) > 0
            assert upload_result.upload_url is not None

        except LeapOCRClientError as e:
            pytest.fail(f"File upload failed: {e}")

    @pytest.mark.slow
    def test_authentication_error(self):
        """Test authentication error with invalid API key."""
        invalid_client = LeapOCRClient(api_key="pk_invalid_key_12345")

        with pytest.raises(LeapOCRClientError) as exc_info:
            invalid_client.process_url(
                url="https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
            )

        # Should be authentication-related error
        assert (
            "authentication" in str(exc_info.value).lower()
            or "unauthorized" in str(exc_info.value).lower()
        )


class TestOCRServiceIntegration:
    """Integration tests for OCRService."""

    @pytest.fixture
    def service(self):
        """Create a real OCR service for integration testing."""
        api_key = os.getenv("LEAPOCR_API_KEY")
        client = LeapOCRClient(api_key=api_key)
        from leapocr.services.ocr import OCRService

        return OCRService(client)

    @pytest.mark.slow
    def test_extract_text_integration(self, service):
        """Test text extraction integration."""
        url = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"

        try:
            text = service.extract_text(url, timeout=60)
            assert isinstance(text, str)
            assert len(text) > 0

        except LeapOCRClientError as e:
            pytest.fail(f"Text extraction failed: {e}")

    @pytest.mark.slow
    def test_extract_structured_data_integration(self, service):
        """Test structured data extraction integration."""
        url = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"

        try:
            data = service.extract_structured_data(url, timeout=60)
            assert isinstance(data, dict)

        except LeapOCRClientError as e:
            pytest.fail(f"Structured data extraction failed: {e}")

    @pytest.mark.slow
    def test_batch_processing_integration(self, service):
        """Test batch processing integration."""
        urls = [
            "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
            "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
        ]

        try:
            # Process without waiting for results
            results = service.batch_process(
                sources=urls,
                max_concurrent=1,  # Keep it simple for integration tests
                wait_for_all=False,
                timeout=30,
            )

            assert len(results) == len(urls)
            for result in results:
                assert hasattr(result, "id")
                assert hasattr(result, "status")

        except LeapOCRClientError as e:
            pytest.fail(f"Batch processing failed: {e}")


class TestAsyncIntegration:
    """Async integration tests."""

    @pytest.fixture
    def async_client(self):
        """Create a real async client for integration testing."""
        api_key = os.getenv("LEAPOCR_API_KEY")
        return LeapOCRClient(api_key=api_key)

    @pytest.mark.slow
    @pytest.mark.asyncio
    async def test_async_process_url_integration(self, async_client):
        """Test async URL processing integration."""
        url = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"

        try:
            job = await async_client.process_url_async(
                url=url,
                format=ProcessFormat.TEXT,
                tier=ProcessTier.CORE,
            )

            assert job.id is not None
            assert len(job.id) > 0
            assert job.status in ["pending", "processing"]

        except LeapOCRClientError as e:
            pytest.fail(f"Async URL processing failed: {e}")

    @pytest.mark.slow
    @pytest.mark.asyncio
    async def test_async_wait_for_result_integration(self, async_client):
        """Test async waiting for job completion."""
        url = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"

        try:
            # Submit job async
            job = await async_client.process_url_async(
                url=url, format=ProcessFormat.TEXT
            )

            # Wait for result async
            result = await async_client.wait_for_result_async(job.id, timeout=60)

            assert result.job_id == job.id
            assert result.status in ["completed", "failed"]

        except LeapOCRClientError as e:
            pytest.fail(f"Async waiting for result failed: {e}")

    @pytest.mark.slow
    @pytest.mark.asyncio
    async def test_async_context_manager(self):
        """Test async context manager."""
        api_key = os.getenv("LEAPOCR_API_KEY")

        async with LeapOCRClient(api_key=api_key) as client:
            assert client.api_key.startswith("pk_")

            # Test a simple operation
            url = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
            job = await client.process_url_async(url=url, format=ProcessFormat.TEXT)
            assert job.id is not None


# Performance tests (marked as slow)
class TestPerformance:
    """Performance tests for the SDK."""

    @pytest.mark.slow
    def test_concurrent_requests(self):
        """Test handling of concurrent requests."""
        api_key = os.getenv("LEAPOCR_API_KEY")
        client = LeapOCRClient(api_key=api_key)

        url = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"

        try:
            # Submit multiple jobs concurrently
            import threading

            results = []
            errors = []

            def submit_job():
                try:
                    job = client.process_url(url=url, format=ProcessFormat.TEXT)
                    results.append(job)
                except Exception as e:
                    errors.append(e)

            # Start multiple threads
            threads = []
            for _ in range(3):
                thread = threading.Thread(target=submit_job)
                threads.append(thread)
                thread.start()

            # Wait for all threads to complete
            for thread in threads:
                thread.join()

            # Check results
            assert len(errors) == 0, f"Errors occurred: {errors}"
            assert len(results) == 3

            for result in results:
                assert result.id is not None
                assert len(result.id) > 0

        except LeapOCRClientError as e:
            pytest.fail(f"Concurrent requests test failed: {e}")


if __name__ == "__main__":
    # Run integration tests manually if needed
    print("Integration tests require LEAPOCR_API_KEY environment variable")
    print("Run with: pytest tests/test_integration.py -v")
