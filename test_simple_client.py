#!/usr/bin/env python3
"""
Simplified LeapOCR test that directly uses httpx to test the API endpoints.
"""

import os
import json
import httpx
from typing import Dict, Any, Optional

class SimpleLeapOCRClient:
    """A simplified client that directly uses httpx for testing."""
    
    def __init__(self, api_key: str, base_url: str = "http://localhost:8080"):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.client = httpx.Client(
            timeout=30.0,
            headers={
                'X-API-Key': api_key,
                'User-Agent': 'leapocr-python-test/0.1.0'
            }
        )
    
    def process_url(self, url: str, format: str = "structured", tier: str = "core") -> Dict[str, Any]:
        """Process a document from URL."""
        endpoint = f"{self.base_url}/api/v1/ocr/uploads/url"
        
        payload = {
            "url": url,
            "format": format,
            "tier": tier
        }
        
        response = self.client.post(endpoint, json=payload)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"API request failed: {response.status_code} - {response.text}")
    
    def get_job_status(self, job_id: str) -> Dict[str, Any]:
        """Get job status."""
        endpoint = f"{self.base_url}/api/v1/ocr/status/{job_id}"
        
        response = self.client.get(endpoint)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"API request failed: {response.status_code} - {response.text}")
    
    def get_job_result(self, job_id: str) -> Dict[str, Any]:
        """Get job result."""
        endpoint = f"{self.base_url}/api/v1/ocr/result/{job_id}"
        
        response = self.client.get(endpoint)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"API request failed: {response.status_code} - {response.text}")

def test_basic_functionality():
    """Test basic LeapOCR functionality."""
    
    api_key = os.getenv("LEAPOCR_API_KEY")
    if not api_key:
        print("❌ LEAPOCR_API_KEY not set")
        return False
    
    print("🚀 Testing basic LeapOCR functionality...")
    
    client = SimpleLeapOCRClient(api_key=api_key)
    
    try:
        # Test 1: Process a URL
        print("\n📄 Testing URL processing...")
        url = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
        
        job = client.process_url(url=url, format="structured", tier="core")
        print(f"✅ Job submitted: {job.get('job_id')}")
        print(f"   Status: {job.get('status')}")
        
        job_id = job.get('job_id')
        
        # Test 2: Check job status
        print("\n⏳ Checking job status...")
        status = client.get_job_status(job_id)
        print(f"✅ Job status: {status.get('status')}")
        print(f"   Progress: {status.get('progress', 'N/A')}")
        
        # Test 3: Wait for processing to complete
        print("\n⏳ Waiting for processing to complete...")
        import time
        
        max_wait = 60  # Maximum wait time in seconds
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            try:
                result = client.get_job_result(job_id)
                status = result.get('status')
                
                if status == 'completed':
                    print(f"✅ Job completed!")
                    print(f"   Status: {status}")
                    print(f"   Credits used: {result.get('credits_used', 'N/A')}")
                    
                    if result.get('data'):
                        print(f"   Extracted data preview: {str(result.get('data'))[:200]}...")
                    break
                elif status == 'failed':
                    print(f"❌ Job failed!")
                    print(f"   Status: {status}")
                    break
                else:
                    print(f"⏳ Job status: {status} (progress: {result.get('progress_percentage', 0)}%)")
                    time.sleep(5)
                    
            except Exception as e:
                if "202" in str(e):
                    print("⏳ Job still processing...")
                    time.sleep(5)
                else:
                    raise e
        
        if time.time() - start_time >= max_wait:
            print("⏰ Timeout reached, job may still be processing")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    
    finally:
        client.client.close()

if __name__ == "__main__":
    success = test_basic_functionality()
    if success:
        print("\n🎉 All tests passed!")
    else:
        print("\n💥 Tests failed!")