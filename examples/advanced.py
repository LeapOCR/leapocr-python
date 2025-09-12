"""
Advanced usage example for the LeapOCR Python SDK.

This example demonstrates advanced features:
1. Batch processing multiple documents
2. Using custom schemas and instructions
3. Error handling and retries
4. Using the high-level OCR service
"""

import os
import asyncio
from pathlib import Path
from leapocr import (
    LeapOCRClient,
    OCRService,
    ProcessFormat,
    ProcessTier,
    ProcessOptions,
    LeapOCRClientError,
    LeapOCRTimeoutError,
    LeapOCRRateLimitError,
)


def advanced_sync_example():
    """Advanced synchronous processing example."""
    api_key = os.getenv("LEAPOCR_API_KEY")
    if not api_key:
        print("Please set your LEAPOCR_API_KEY environment variable")
        return
    
    client = LeapOCRClient(api_key=api_key)
    ocr_service = OCRService(client)
    
    try:
        # Example 1: Batch processing with custom options
        print("🚀 Batch processing multiple documents...")
        
        # Sample URLs (replace with your actual documents)
        document_urls = [
            "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
            "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
        ]
        
        # Custom processing options
        options = ProcessOptions(
            format=ProcessFormat.STRUCTURED,
            tier=ProcessTier.PREMIUM,
            timeout=120,
            poll_interval=1.0,
        )
        
        # Process batch
        results = ocr_service.batch_process(
            sources=document_urls,
            options=options,
            max_concurrent=2,
            wait_for_all=True,
            timeout=90,
        )
        
        print(f"✅ Batch processing completed for {len(results)} documents")
        
        for i, result in enumerate(results):
            if hasattr(result, 'status'):
                print(f"   Document {i+1}: {result.status}")
                if hasattr(result, 'credits_used'):
                    print(f"      Credits used: {result.credits_used}")
        
        print()
        
        # Example 2: Processing with custom schema and instruction
        print("🎯 Processing with custom configuration...")
        
        advanced_options = ProcessOptions(
            format=ProcessFormat.STRUCTURED,
            tier=ProcessTier.PREMIUM,
            project_id="your-project-id",  # Replace with actual project ID
            schema_id="your-schema-id",    # Replace with actual schema ID
            instruction_id="your-instruction-id",  # Replace with actual instruction ID
            category_id="invoice",        # Replace with actual category ID
            webhook_url="https://your-webhook-url.com/ocr-webhook",
        )
        
        # Process single document with advanced options
        try:
            result = ocr_service.process_document(
                source="https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
                options=advanced_options,
                wait_for_result=True,
                timeout=120,
            )
            
            print(f"✅ Advanced processing completed!")
            print(f"   Status: {result.status}")
            
            if result.data:
                print(f"   Structured data extracted with custom schema")
                
        except LeapOCRTimeoutError:
            print("⏰ Processing timed out, but job may still complete")
        except LeapOCRClientError as e:
            print(f"⚠️  Processing error: {e}")
        
        print()
        
        # Example 3: Error handling and retry logic
        print("🔄 Demonstrating error handling...")
        
        def process_with_retry(source, max_retries=3):
            for attempt in range(max_retries):
                try:
                    result = ocr_service.process_document(
                        source=source,
                        options=ProcessOptions(format=ProcessFormat.TEXT),
                        wait_for_result=True,
                        timeout=30,
                    )
                    return result
                except LeapOCRRateLimitError:
                    if attempt < max_retries - 1:
                        wait_time = 2 ** attempt  # Exponential backoff
                        print(f"   Rate limited, waiting {wait_time}s before retry...")
                        import time
                        time.sleep(wait_time)
                        continue
                    else:
                        raise
                except (LeapOCRTimeoutError, LeapOCRClientError) as e:
                    print(f"   Error on attempt {attempt + 1}: {e}")
                    if attempt < max_retries - 1:
                        continue
                    else:
                        raise
        
        try:
            result = process_with_retry(
                "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
            )
            print(f"✅ Retry successful! Status: {result.status}")
        except Exception as e:
            print(f"❌ All retry attempts failed: {e}")
        
        print()
        
        # Example 4: Using convenience methods
        print("📝 Using convenience methods...")
        
        try:
            # Extract text directly
            text = ocr_service.extract_text(
                "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
                timeout=60,
            )
            print(f"✅ Text extracted ({len(text)} characters)")
            
            # Extract structured data
            structured_data = ocr_service.extract_structured_data(
                "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
                timeout=60,
            )
            print(f"✅ Structured data extracted: {len(structured_data)} fields")
            
        except Exception as e:
            print(f"❌ Convenience method error: {e}")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    finally:
        client.close()


async def advanced_async_example():
    """Advanced asynchronous processing example."""
    api_key = os.getenv("LEAPOCR_API_KEY")
    if not api_key:
        print("Please set your LEAPOCR_API_KEY environment variable")
        return
    
    async with LeapOCRClient(api_key=api_key) as client:
        ocr_service = OCRService(client)
        
        try:
            # Example: Async batch processing
            print("🚀 Async batch processing...")
            
            document_urls = [
                "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
                "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
                "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
            ]
            
            # Process all documents concurrently
            results = await ocr_service.batch_process_async(
                sources=document_urls,
                options=ProcessOptions(format=ProcessFormat.TEXT),
                max_concurrent=3,
                wait_for_all=True,
                timeout=60,
            )
            
            print(f"✅ Async batch processing completed for {len(results)} documents")
            
            successful = sum(1 for r in results if hasattr(r, 'status') and r.status == 'completed')
            print(f"   Successfully processed: {successful}/{len(results)}")
            
            # Example: Async document processing with streaming-style monitoring
            print("\n📊 Real-time job monitoring...")
            
            async def process_with_monitoring(source):
                job = await ocr_service.process_document_async(
                    source=source,
                    options=ProcessOptions(format=ProcessFormat.STRUCTURED),
                    wait_for_result=False,
                )
                
                # Monitor job status
                while True:
                    status = client.get_job_status(job.id)
                    print(f"   Job {job.id}: {status.status} ({status.progress or 0}%)")
                    
                    if status.status in ['completed', 'failed', 'cancelled']:
                        break
                    
                    await asyncio.sleep(2)  # Poll every 2 seconds
                
                return await client.get_job_result(job.id)
            
            result = await process_with_monitoring(
                "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
            )
            
            print(f"✅ Monitored processing completed: {result.status}")
            
        except Exception as e:
            print(f"❌ Async processing error: {e}")


def configuration_example():
    """Example showing different client configurations."""
    print("⚙️  Client configuration examples...")
    
    # Basic configuration
    api_key = os.getenv("LEAPOCR_API_KEY")
    if not api_key:
        print("Please set your LEAPOCR_API_KEY environment variable")
        return
    
    # Different client configurations
    configs = [
        {
            "name": "Production Client",
            "config": {"base_url": "https://api.leapocr.com", "timeout": 30.0}
        },
        {
            "name": "Development Client", 
            "config": {"base_url": "http://localhost:8080", "timeout": 60.0}
        },
        {
            "name": "High-Performance Client",
            "config": {"timeout": 120.0, "max_retries": 5}
        }
    ]
    
    for config_info in configs:
        try:
            print(f"\n🔧 Testing {config_info['name']}...")
            client = LeapOCRClient(api_key=api_key, **config_info['config'])
            
            # Test basic connectivity (commented out to avoid actual API calls)
            # status = client.get_job_status("test-job-id")
            print(f"   ✅ {config_info['name']} configured successfully")
            
            client.close()
            
        except Exception as e:
            print(f"   ❌ {config_info['name']} failed: {e}")


if __name__ == "__main__":
    print("🚀 LeapOCR Python SDK - Advanced Example")
    print("=" * 50)
    
    # Configuration examples
    print("\n📋 Configuration Examples:")
    configuration_example()
    
    # Advanced synchronous examples
    print("\n📋 Advanced Synchronous Examples:")
    advanced_sync_example()
    
    # Advanced asynchronous examples
    print("\n📋 Advanced Asynchronous Examples:")
    asyncio.run(advanced_async_example())
    
    print("\n✨ Advanced examples completed!")