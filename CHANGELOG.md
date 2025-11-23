## [0.0.4] - 2025-01-23

### Breaking Changes
- **Updated result endpoint structure** - `PageResult.text` field replaced with `PageResult.result`
- **Removed fields** - `processing_time_seconds` and `PageMetadata` removed from API responses
- The `result` field now contains either:
  - `str` - for markdown format (plain text)
  - `dict` - for structured formats (parsed JSON object)

### Changed
- **API Response Structure**:
  - `PageResult.text` → `PageResult.result` (supports both string and dict types)
  - Removed `PageResult.metadata`, `processed_at` fields
  - Removed `JobResult.processing_time_seconds` field
  - Result endpoint now returns `result` instead of `text` for each page

- **Updated Models**:
  - Regenerated SDK from latest OpenAPI specification
  - `ModelsPageResponse` now has `result: Optional[Any]` field
  - `ModelsOCRResultResponse` includes updated field set

### Documentation
- Updated README with comprehensive `result` field documentation
- Added result type table showing `dict` vs `str` for each format
- Updated all examples to use `page.result` instead of `page.text`
- Added examples showing proper handling of both string and dict result types
- Removed references to deprecated fields in all examples

### Migration Guide
```python
# Before (v0.0.3)
for page in result.pages:
    text = page.text
    processing_time = page.metadata.processing_ms

total_time = result.processing_time_seconds

# After (v0.0.4)
for page in result.pages:
    # Handle both string (markdown) and dict (structured)
    if isinstance(page.result, str):
        text = page.result  # Markdown text
    else:
        data = page.result  # Structured data dict

# processing_time_seconds and metadata fields removed
```

## [0.0.3] - 2025-11-11

- chore: update CHANGELOG.md for v0.0.2 (c936efc)
- Update LICENSE and README to reflect Apache 2.0 license (5f5a20b)
- Enhance project metadata and add logo assets (9e442ef)
- Update dependencies and logo URL in project configuration (29096ea)
- Update version to 0.0.3 across project files (6847878)

## [0.0.2] - ${DATE}

- gen (1040bb7)
- Add template usage and job management examples in documentation (1c08c01)
- deleting unused stuff (9f4fc82)
- Release version 0.0.2 with significant updates (fc7e835)
- Update project configuration and documentation (4075175)
- fixing readme (f3f9e28)
- Update Python version requirements in README and pyproject.toml (029f12c)
- Update CI workflow to include 'dev' extra dependencies (49d402d)

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.0.2] - 2025-11-11

### Breaking Changes
- **Removed `process_and_wait()` method** - Use two-step pattern: `process_file()`/`process_url()` → `wait_until_done()`
- API now matches Go/JS SDKs for consistency across all language implementations

### Added
- **New OCR Models**:
  - `Model.ENGLISH_PRO_V1` - High-accuracy English document processing (2 credits/page)
  - `Model.PRO_V1` - Premium multilingual document processing (2 credits/page)
- **Custom Model Support** - `ProcessOptions.model` now accepts custom model strings for organization-specific models
- **`wait_until_done()` method** - Explicit job waiting with poll options, matching Go/JS SDK patterns
- New example: `examples/advanced/model_selection.py` demonstrating all models and custom model usage

### Changed
- **Two-step processing pattern** (BREAKING):
  - Old: `result = await client.ocr.process_and_wait("doc.pdf")`
  - New: `job = await client.ocr.process_file("doc.pdf")` → `result = await client.ocr.wait_until_done(job.job_id)`
- Updated all documentation and examples to use two-step pattern
- Modernized type hints: `Optional[X]` → `X | None`, `Union[X, Y]` → `X | Y`
- Enhanced README with model comparison table and custom model examples
- Improved batch processing examples showing submit-all → wait-all pattern

### Fixed
- Type annotation compatibility with Python 3.9+ using `from __future__ import annotations`

### Migration Guide
Users upgrading from v0.0.1 must update code:
```python
# Before (v0.0.1)
result = await client.ocr.process_and_wait(
    "document.pdf",
    options=ProcessOptions(format=Format.STRUCTURED)
)

# After (v0.0.2)
job = await client.ocr.process_file(
    "document.pdf",
    options=ProcessOptions(format=Format.STRUCTURED)
)
result = await client.ocr.wait_until_done(job.job_id)
```

**Benefits of new pattern**:
- Explicit control over job submission vs. waiting
- Better concurrent batch processing
- API parity with Go/JS SDKs
- Flexibility to check status or delete jobs between steps

## [0.0.1] - 2025-11-08

### Added
- Initial release of LeapOCR Python SDK
- Async-first client with httpx
- Support for file and URL processing
- Multiple output formats (Structured, Markdown, Per-Page Structured)
- Custom schema support for structured data extraction
- Built-in retry logic with exponential backoff
- Progress tracking with callbacks
- Comprehensive error handling hierarchy
- Type-safe API with full mypy support
- Direct multipart file uploads
- Concurrent batch processing support
- 93 unit tests and 13 integration tests
- Complete documentation and examples

### Core Features
- `LeapOCR` main client with async context manager
- `OCRService` for document processing operations
- `ProcessOptions` for configurable processing
- `PollOptions` for custom polling behavior
- `ClientConfig` for client configuration

### Error Classes
- `LeapOCRError` - Base error class
- `AuthenticationError` - Authentication failures
- `RateLimitError` - Rate limit exceeded
- `ValidationError` - Input validation errors
- `FileError` - File-related errors
- `JobError` - Job processing errors
- `JobFailedError` - Job processing failures
- `JobTimeoutError` - Job timeout errors
- `NetworkError` - Network connectivity issues
- `APIError` - API error responses
- `InsufficientCreditsError` - Insufficient credits

### Examples
- Basic file processing
- URL processing with manual polling
- Concurrent batch processing
- Schema-based extraction
- Custom configuration
- Error handling strategies
- Timeout handling

[Unreleased]: https://github.com/leapocr/leapocr-python/compare/v0.0.4...HEAD
[0.0.4]: https://github.com/leapocr/leapocr-python/compare/v0.0.3...v0.0.4
[0.0.3]: https://github.com/leapocr/leapocr-python/compare/v0.0.2...v0.0.3
[0.0.2]: https://github.com/leapocr/leapocr-python/compare/v0.0.1...v0.0.2
[0.0.1]: https://github.com/leapocr/leapocr-python/releases/tag/v0.0.1
