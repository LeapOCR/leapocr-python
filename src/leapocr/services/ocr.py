"""
LeapOCR Python SDK - OCR Service

This module provides high-level OCR processing services.
"""

import asyncio
import io
from pathlib import Path
from typing import Any

from ..client import LeapOCRClient
from ..exceptions import LeapOCRClientError
from ..types import (
    Job,
    JobResult,
    JobStatus,
    PageResult,
    ProcessFormat,
    ProcessOptions,
)


class OCRService:
    """High-level service for OCR processing operations."""

    def __init__(self, client: LeapOCRClient):
        """
        Initialize the OCR service.

        Args:
            client: LeapOCR client instance
        """
        self.client = client

    def process_document(
        self,
        source: str | Path | io.IOBase,
        options: ProcessOptions | None = None,
        wait_for_result: bool = False,
        timeout: float | None = None,
    ) -> Job | JobResult:
        """
        Process a document from any source (URL or file).

        Args:
            source: Document URL, file path, or file-like object
            options: Processing options
            wait_for_result: Whether to wait for processing to complete
            timeout: Maximum time to wait for completion

        Returns:
            Job if wait_for_result=False, JobResult if wait_for_result=True

        Raises:
            LeapOCRClientError: If processing fails
        """
        if options is None:
            options = ProcessOptions()

        # Determine source type and process accordingly
        if isinstance(source, (str, Path)):
            # Check if it's a URL or file path
            source_str = str(source)
            if source_str.startswith(("http://", "https://")):
                return self._process_url(source_str, options, wait_for_result, timeout)
            else:
                return self._process_file(source, options, wait_for_result, timeout)
        else:
            # File-like object
            return self._process_file(source, options, wait_for_result, timeout)

    async def process_document_async(
        self,
        source: str | Path | io.IOBase,
        options: ProcessOptions | None = None,
        wait_for_result: bool = False,
        timeout: float | None = None,
    ) -> Job | JobResult:
        """
        Process a document asynchronously.

        Args:
            source: Document URL, file path, or file-like object
            options: Processing options
            wait_for_result: Whether to wait for processing to complete
            timeout: Maximum time to wait for completion

        Returns:
            Job if wait_for_result=False, JobResult if wait_for_result=True

        Raises:
            LeapOCRClientError: If processing fails
        """
        if options is None:
            options = ProcessOptions()

        # Determine source type and process accordingly
        if isinstance(source, (str, Path)):
            source_str = str(source)
            if source_str.startswith(("http://", "https://")):
                return await self._process_url_async(
                    source_str, options, wait_for_result, timeout
                )
            else:
                return await self._process_file_async(
                    source, options, wait_for_result, timeout
                )
        else:
            # File-like object
            return await self._process_file_async(
                source, options, wait_for_result, timeout
            )

    def _process_url(
        self,
        url: str,
        options: ProcessOptions,
        wait_for_result: bool,
        timeout: float | None,
    ) -> Job | JobResult:
        """Process a document from URL."""
        job = self.client.process_url(
            url=url,
            format=options.format,
            tier=options.tier,
            project_id=options.project_id,
            schema_id=options.schema_id,
            instruction_id=options.instruction_id,
            category_id=options.category_id,
            webhook_url=options.webhook_url,
        )

        if wait_for_result:
            return self.client.wait_for_result(
                job.id,
                timeout=timeout or options.timeout,
                poll_interval=options.poll_interval,
            )
        else:
            return job

    async def _process_url_async(
        self,
        url: str,
        options: ProcessOptions,
        wait_for_result: bool,
        timeout: float | None,
    ) -> Job | JobResult:
        """Process a document from URL asynchronously."""
        job = await self.client.process_url_async(
            url=url,
            format=options.format,
            tier=options.tier,
            project_id=options.project_id,
            schema_id=options.schema_id,
            instruction_id=options.instruction_id,
            category_id=options.category_id,
            webhook_url=options.webhook_url,
        )

        if wait_for_result:
            return await self.client.wait_for_result_async(
                job.id,
                timeout=timeout or options.timeout,
                poll_interval=options.poll_interval,
            )
        else:
            return job

    def _process_file(
        self,
        file: str | Path | io.IOBase,
        options: ProcessOptions,
        wait_for_result: bool,
        timeout: float | None,
    ) -> Job | JobResult:
        """Process a file upload."""
        upload_result = self.client.upload_file(
            file=file,
            format=options.format,
            tier=options.tier,
            project_id=options.project_id,
            schema_id=options.schema_id,
            instruction_id=options.instruction_id,
            category_id=options.category_id,
            webhook_url=options.webhook_url,
        )

        if wait_for_result:
            return self.client.wait_for_result(
                upload_result.job_id,
                timeout=timeout or options.timeout,
                poll_interval=options.poll_interval,
            )
        else:
            # Convert upload result to job for consistency
            return Job(
                id=upload_result.job_id,
                status=JobStatus.PENDING,
            )

    async def _process_file_async(
        self,
        file: str | Path | io.IOBase,
        options: ProcessOptions,
        wait_for_result: bool,
        timeout: float | None,
    ) -> Job | JobResult:
        """Process a file upload asynchronously."""
        # Note: upload_file is sync for now, would need async implementation
        upload_result = self.client.upload_file(
            file=file,
            format=options.format,
            tier=options.tier,
            project_id=options.project_id,
            schema_id=options.schema_id,
            instruction_id=options.instruction_id,
            category_id=options.category_id,
            webhook_url=options.webhook_url,
        )

        if wait_for_result:
            return await self.client.wait_for_result_async(
                upload_result.job_id,
                timeout=timeout or options.timeout,
                poll_interval=options.poll_interval,
            )
        else:
            # Convert upload result to job for consistency
            return Job(
                id=upload_result.job_id,
                status=JobStatus.PENDING,
            )

    def batch_process(
        self,
        sources: list[str | Path | io.IOBase],
        options: ProcessOptions | None = None,
        max_concurrent: int = 3,
        wait_for_all: bool = False,
        timeout: float | None = None,
    ) -> list[Job | JobResult]:
        """
        Process multiple documents concurrently.

        Args:
            sources: List of document sources (URLs, file paths, or file-like objects)
            options: Processing options
            max_concurrent: Maximum number of concurrent processing jobs
            wait_for_all: Whether to wait for all jobs to complete
            timeout: Maximum time to wait for each job

        Returns:
            List of Job or JobResult objects
        """
        if options is None:
            options = ProcessOptions()

        results = []

        # Process documents in batches to avoid overwhelming the API
        for i in range(0, len(sources), max_concurrent):
            batch = sources[i : i + max_concurrent]

            # Process batch concurrently
            batch_jobs = []
            for source in batch:
                job = self.process_document(source, options, wait_for_result=False)
                batch_jobs.append(job)

            if wait_for_all:
                # Wait for all jobs in batch to complete
                batch_results = []
                for job in batch_jobs:
                    result = self.client.wait_for_result(
                        job.id,
                        timeout=timeout or options.timeout,
                        poll_interval=options.poll_interval,
                    )
                    batch_results.append(result)
                results.extend(batch_results)
            else:
                results.extend(batch_jobs)

        return results

    async def batch_process_async(
        self,
        sources: list[str | Path | io.IOBase],
        options: ProcessOptions | None = None,
        max_concurrent: int = 3,
        wait_for_all: bool = False,
        timeout: float | None = None,
    ) -> list[Job | JobResult]:
        """
        Process multiple documents concurrently (async version).

        Args:
            sources: List of document sources (URLs, file paths, or file-like objects)
            options: Processing options
            max_concurrent: Maximum number of concurrent processing jobs
            wait_for_all: Whether to wait for all jobs to complete
            timeout: Maximum time to wait for each job

        Returns:
            List of Job or JobResult objects
        """
        if options is None:
            options = ProcessOptions()

        results = []

        # Process documents concurrently with semaphore
        semaphore = asyncio.Semaphore(max_concurrent)

        async def process_single(source: str | Path | io.IOBase) -> Job | JobResult:
            async with semaphore:
                return await self.process_document_async(
                    source, options, wait_for_result=wait_for_all, timeout=timeout
                )

        # Create tasks for all sources
        tasks = [process_single(source) for source in sources]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Handle any exceptions
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                # Convert exceptions to job results with error info
                results[i] = JobResult(
                    job_id=f"error_{i}",
                    status=JobStatus.FAILED,
                    error_message=str(result),
                )

        return results

    def extract_text(
        self,
        source: str | Path | io.IOBase,
        timeout: float | None = None,
    ) -> str:
        """
        Extract text from a document (convenience method).

        Args:
            source: Document URL, file path, or file-like object
            timeout: Maximum time to wait for completion

        Returns:
            Extracted text as string

        Raises:
            LeapOCRClientError: If extraction fails
        """
        options = ProcessOptions(format=ProcessFormat.TEXT)
        result = self.process_document(
            source, options, wait_for_result=True, timeout=timeout
        )

        if isinstance(result, JobResult) and result.data:
            return result.data.get("text", "")
        else:
            raise LeapOCRClientError("Failed to extract text from document")

    def extract_structured_data(
        self,
        source: str | Path | io.IOBase,
        schema_id: str | None = None,
        timeout: float | None = None,
    ) -> dict[str, Any]:
        """
        Extract structured data from a document (convenience method).

        Args:
            source: Document URL, file path, or file-like object
            schema_id: Custom schema ID for structured extraction
            timeout: Maximum time to wait for completion

        Returns:
            Structured data as dictionary

        Raises:
            LeapOCRClientError: If extraction fails
        """
        options = ProcessOptions(
            format=ProcessFormat.STRUCTURED,
            schema_id=schema_id,
        )
        result = self.process_document(
            source, options, wait_for_result=True, timeout=timeout
        )

        if isinstance(result, JobResult) and result.data:
            return result.data
        else:
            raise LeapOCRClientError("Failed to extract structured data from document")

    def get_page_results(self, job_result: JobResult) -> list[PageResult]:
        """
        Extract page-level results from a job result.

        Args:
            job_result: Job result containing page data

        Returns:
            List of PageResult objects
        """
        if not job_result.pages:
            return []

        page_results = []
        for page_data in job_result.pages:
            page_result = PageResult(
                page_number=page_data.get("page_number", 0),
                data=page_data.get("data"),
                text=page_data.get("text"),
                tables=page_data.get("tables", []),
                confidence=page_data.get("confidence"),
                processing_time=page_data.get("processing_time"),
            )
            page_results.append(page_result)

        return page_results

    def validate_job_result(self, job_result: JobResult) -> bool:
        """
        Validate that a job result is complete and valid.

        Args:
            job_result: Job result to validate

        Returns:
            True if valid, False otherwise
        """
        if job_result.status != JobStatus.COMPLETED:
            return False

        if job_result.error_message:
            return False

        if not job_result.data and not job_result.pages:
            return False

        return True
