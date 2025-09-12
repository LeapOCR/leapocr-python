# LeapOCR Python SDK

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Python SDK for the [LeapOCR API](https://www.leapocr.com/) - Process PDFs and extract structured data using AI.

## Project Status

**Version**: `0.1.0`

This SDK is currently in **beta** and is subject to change.

## Installation

```bash
pip install leapocr-python
```

For development:

```bash
uv sync
```

## Getting Started

### 1. Get Your API Key

To use the LeapOCR API, you'll need an API key. You can get one by signing up on the [LeapOCR website](https://www.leapocr.com/signup).

### 2. Quick Start

```python
import leapocr

# Initialize SDK with API key
client = leapocr.LeapOCRClient(api_key="pk_live_your_key_here")

# Process a file from URL
result = client.process_url(
    "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
    format="structured",
    tier="core"
)

print(f"Job ID: {result.job_id}")
print(f"Status: {result.status}")

# Wait for completion
final_result = client.wait_for_result(result.job_id)
print(f"Extracted data: {final_result.data}")
```

### Async Usage

```python
import asyncio
import leapocr

async def main():
    client = leapocr.LeapOCRClient(api_key="pk_live_your_key_here")
    
    # Process file asynchronously
    with open("document.pdf", "rb") as f:
        job = await client.upload_file_async(f)
        result = await client.wait_for_result_async(job.id)
        print(f"Extracted data: {result.data}")

asyncio.run(main())
```

## Features

- **Python-Native Interface**: Clean, idiomatic Python API with type hints
- **Full Async Support**: Async/await support for concurrent processing
- **Type-Safe**: Strong typing with Pydantic models and mypy support
- **Flexible Configuration**: Support for custom schemas, instructions, and processing tiers
- **Robust Error Handling**: Comprehensive error types with retry logic
- **File Upload Support**: Direct file upload with presigned URLs
- **Modern Tooling**: Built with UV for fast dependency management and builds

## Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/leapocr/leapocr-python.git
cd leapocr-python

# Install dependencies with UV
uv sync

# Install pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=leapocr

# Run specific test categories
uv run pytest -m "not integration"  # Unit tests only
uv run pytest -m integration        # Integration tests only
```

### Code Quality

```bash
# Format code
uv run black .

# Lint code
uv run ruff check .

# Type checking
uv run mypy .
```

### Building and Publishing

```bash
# Build package
uv build

# Publish to PyPI
uv publish
```

## API Reference

For a complete API reference, see the [documentation](https://docs.leapocr.com/).

## Error Handling

The SDK provides comprehensive error handling:

```python
from leapocr.exceptions import LeapOCRClientError, LeapOCRServerError

try:
    result = client.process_url("https://example.com/document.pdf")
except LeapOCRClientError as e:
    print(f"Client error: {e}")
except LeapOCRServerError as e:
    print(f"Server error: {e}")
    if e.is_retryable:
        # Implement retry logic
        pass
```

## Contributing

Contributions are welcome! Please see our [Contributing Guidelines](CONTRIBUTING.md) for more details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support and questions, please refer to the [API documentation](https://docs.leapocr.com) or open an issue.