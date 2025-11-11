"""Example: Using templates for document processing.

This example demonstrates how to use pre-configured templates
by their slug instead of defining schema and instructions inline.
"""

import asyncio
import os

from leapocr import LeapOCR, ProcessOptions


async def main():
    """Process documents using a template."""
    api_key = os.getenv("LEAPOCR_API_KEY")
    if not api_key:
        raise ValueError("LEAPOCR_API_KEY environment variable not set")

    async with LeapOCR(api_key) as client:
        # Example 1: Use a template by slug
        print("Processing with invoice template...")
        result = await client.ocr.process_and_wait(
            "https://example.com/invoice.pdf",
            options=ProcessOptions(
                template_slug="invoice-extraction",  # Reference existing template
            ),
        )

        print(f"✓ Processed using template: {result.template_name}")
        print(f"  Job ID: {result.job_id}")
        print(f"  Pages processed: {result.processed_pages}")
        print(f"  Credits used: {result.credits_used}")
        print(f"  Result format: {result.result_format}")
        print()

        # Example 2: Process multiple files with the same template
        print("Batch processing with template...")
        files = [
            "https://example.com/invoice1.pdf",
            "https://example.com/invoice2.pdf",
            "https://example.com/invoice3.pdf",
        ]

        tasks = [
            client.ocr.process_and_wait(
                url, options=ProcessOptions(template_slug="invoice-extraction")
            )
            for url in files
        ]

        results = await asyncio.gather(*tasks)

        print(f"✓ Processed {len(results)} documents")
        total_credits = sum(r.credits_used for r in results)
        print(f"  Total credits: {total_credits}")
        print()

        # Example 3: Use different templates for different document types
        print("Processing different document types...")

        contracts_result = await client.ocr.process_and_wait(
            "contract.pdf",
            options=ProcessOptions(template_slug="contract-analysis"),
        )

        receipts_result = await client.ocr.process_and_wait(
            "receipt.pdf",
            options=ProcessOptions(template_slug="receipt-extraction"),
        )

        print(f"✓ Contract processed with: {contracts_result.template_name}")
        print(f"✓ Receipt processed with: {receipts_result.template_name}")


if __name__ == "__main__":
    asyncio.run(main())
