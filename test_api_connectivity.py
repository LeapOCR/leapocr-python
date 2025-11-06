#!/usr/bin/env python3
"""
Simple test to check if the LeapOCR API is accessible.
"""

import os
import httpx


def test_api_connectivity():
    """Test basic API connectivity."""

    api_key = os.getenv("LEAPOCR_API_KEY")
    if not api_key:
        print("❌ LEAPOCR_API_KEY not set")
        return False

    base_url = "http://localhost:8080"

    try:
        # Test basic connectivity
        print(f"🔍 Testing connectivity to {base_url}...")

        with httpx.Client(timeout=10.0) as client:
            # Test health endpoint or swagger
            response = client.get(f"{base_url}/api/v1/swagger.json")

            if response.status_code == 200:
                print("✅ API is accessible!")
                print(f"   Status: {response.status_code}")
                print(f"   Response size: {len(response.text)} bytes")
                return True
            else:
                print(f"❌ API returned status: {response.status_code}")
                return False

    except Exception as e:
        print(f"❌ Failed to connect to API: {e}")
        return False


if __name__ == "__main__":
    success = test_api_connectivity()
    if success:
        print("\n🎉 API connectivity test passed!")
    else:
        print("\n💥 API connectivity test failed!")
        print("   Make sure the OCR API is running on localhost:8080")
