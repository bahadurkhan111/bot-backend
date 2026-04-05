#!/usr/bin/env python3
"""
Test script for Gematrinator scraper - tests with a single number first
"""

import asyncio
import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.gematrinator_number_scraper import GematrinatorScraper


async def test_single_number():
    """Test scraping a single number."""
    print("Testing scraper with number 7...")
    print("="*60)
    
    scraper = GematrinatorScraper(start_number=7, end_number=7)
    
    try:
        results = await scraper.scrape_all_numbers()
        
        print("\nTest Results:")
        print("="*60)
        
        if results:
            data = results[0]
            print(f"\nNumber: {data.get('number')}")
            print(f"URL: {data.get('url')}")
            print(f"\nExtracted Properties:")
            
            for key, value in sorted(data.items()):
                if key not in ['number', 'url', 'scrape_timestamp', 'error']:
                    if value is not None:
                        print(f"  {key}: {value}")
            
            # Try exporting
            print("\n" + "="*60)
            print("Testing Excel export...")
            filename = scraper.export_to_excel("test_gematrinator_output.xlsx")
            print(f"✓ Test export successful: {filename}")
            
            return True
        else:
            print("❌ No results returned")
            return False
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_multiple_numbers():
    """Test scraping multiple numbers (1-5)."""
    print("\n\nTesting scraper with numbers 1-5...")
    print("="*60)
    
    scraper = GematrinatorScraper(start_number=1, end_number=5)
    
    try:
        results = await scraper.scrape_all_numbers()
        scraper.print_summary()
        
        if len(results) == 5:
            print("\n✓ Successfully scraped all 5 numbers")
            return True
        else:
            print(f"\n❌ Expected 5 results, got {len(results)}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run all tests."""
    print("GEMATRINATOR SCRAPER - TEST SUITE")
    print("="*60)
    print()
    
    # Test 1: Single number
    test1_passed = await test_single_number()
    
    # Test 2: Multiple numbers
    test2_passed = await test_multiple_numbers()
    
    # Summary
    print("\n\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Test 1 (Single Number):   {'✓ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"Test 2 (Multiple Numbers): {'✓ PASSED' if test2_passed else '❌ FAILED'}")
    
    if test1_passed and test2_passed:
        print("\n🎉 All tests passed! Scraper is ready to use.")
        print("\nRun the full scraper with:")
        print("  python scripts/gematrinator_number_scraper.py")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")


if __name__ == "__main__":
    asyncio.run(main())
