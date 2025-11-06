"""
Basic usage example for the LeapOCR Python SDK.

This example demonstrates the most common use cases:
1. Processing a document from URL
2. Uploading and processing a local file
3. Waiting for results
"""

import asyncio
import os

from leapocr import LeapOCRClient, ProcessFormat, ProcessTier


def main():
    # Get API key from environment variable
    api_key = os.getenv("LEAPOCR_API_KEY")
    if not api_key:
        print("Please set your LEAPOCR_API_KEY environment variable")
        return

    # Initialize the client with localhost
    client = LeapOCRClient(api_key=api_key, base_url="http://localhost:8080")

    try:
        # Example 1: Process a document from URL
        print("📄 Processing document from URL...")
        url = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"

        job = client.process_url(
            url=url,
            format=ProcessFormat.STRUCTURED,
            tier=ProcessTier.CORE,
        )

        print(f"✅ Job submitted: {job.id}")
        print(f"   Status: {job.status}")

        # Wait for the result
        print("⏳ Waiting for processing to complete...")
        result = client.wait_for_result(job.id, timeout=60)

        print("✅ Processing completed!")
        print(f"   Final status: {result.status}")
        print(f"   Credits used: {result.credits_used}")
        print(f"   Processing time: {result.processing_time}s")

        if result.data:
            print(f"   Extracted data: {result.data}")

        print()

        # Example 2: Process a local file
        print("📁 Processing local file...")

        # Create a sample file path (you would replace this with an actual file)
        sample_file = "sample_document.pdf"

        if os.path.exists(sample_file):
            upload_result = client.upload_file(
                file=sample_file,
                format=ProcessFormat.TEXT,
                tier=ProcessTier.CORE,
            )

            print(f"✅ File uploaded: {upload_result.job_id}")

            # Wait for result
            file_result = client.wait_for_result(upload_result.job_id, timeout=60)

            print("✅ File processing completed!")
            print(f"   Status: {file_result.status}")

            if file_result.data and "text" in file_result.data:
                print(f"   Extracted text: {file_result.data['text'][:200]}...")
        else:
            print(
                f"⚠️  Sample file {sample_file} not found, skipping file upload example"
            )

        print()

        # Example 3: Check job status
        print("📊 Checking job status...")
        status = client.get_job_status(job.id)
        print(f"   Job ID: {status.job_id}")
        print(f"   Status: {status.status}")
        print(f"   Progress: {status.progress}%")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        # Clean up
        client.close()


async def async_example():
    """Async version of the basic example."""
    # Get API key from environment variable
    api_key = os.getenv("LEAPOCR_API_KEY")
    if not api_key:
        print("Please set your LEAPOCR_API_KEY environment variable")
        return

    # Initialize the client with async context manager
    async with LeapOCRClient(api_key=api_key) as client:
        try:
            # Example: Process document from URL asynchronously
            print("📄 Processing document from URL (async)...")
            url = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"

            job = await client.process_url_async(
                url=url,
                format=ProcessFormat.STRUCTURED,
                tier=ProcessTier.CORE,
            )

            print(f"✅ Job submitted: {job.id}")

            # Wait for the result asynchronously
            print("⏳ Waiting for processing to complete...")
            result = await client.wait_for_result_async(job.id, timeout=60)

            print("✅ Processing completed!")
            print(f"   Final status: {result.status}")
            print(f"   Credits used: {result.credits_used}")

            if result.data:
                print(f"   Extracted data: {result.data}")

        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    print("🚀 LeapOCR Python SDK - Basic Example")
    print("=" * 50)

    # Run synchronous example
    print("\n📋 Synchronous Example:")
    main()

    # Run asynchronous example
    print("\n📋 Asynchronous Example:")
    asyncio.run(async_example())

    print("\n✨ Examples completed!")
