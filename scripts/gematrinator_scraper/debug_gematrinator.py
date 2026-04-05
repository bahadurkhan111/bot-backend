#!/usr/bin/env python3
"""
Debug script to inspect the actual HTML structure of Gematrinator pages
"""

import asyncio
from playwright.async_api import async_playwright


async def debug_page():
    """Fetch and display the actual page content."""
    async with async_playwright() as p:
        print("Launching browser...")
        browser = await p.chromium.launch(headless=False)  # Set to False to see the browser
        context = await browser.new_context()
        page = await context.new_page()
        
        # Test with number 7
        url = "https://gematrinator.com/number-properties?number=7"
        print(f"Loading: {url}")
        
        await page.goto(url, wait_until="domcontentloaded", timeout=60000)
        await asyncio.sleep(3)  # Wait for content
        
        # Get page title
        title = await page.title()
        print(f"\nPage Title: {title}")
        
        # Get all text content
        content = await page.content()
        
        # Save full HTML
        with open('debug_page_7.html', 'w', encoding='utf-8') as f:
            f.write(content)
        print("\n✓ Full HTML saved to: debug_page_7.html")
        
        # Try to find specific elements
        print("\n" + "="*60)
        print("SEARCHING FOR KEY ELEMENTS:")
        print("="*60)
        
        # Look for text containing "Prime"
        try:
            elements = await page.query_selector_all('*')
            print(f"\nTotal elements on page: {len(elements)}")
            
            # Get all text content
            all_text = await page.inner_text('body')
            print(f"\nPage text content (first 1000 chars):")
            print(all_text[:1000])
            
            # Search for specific keywords
            keywords = ['Prime', 'Fibonacci', 'Composite', 'Triangular', 'Divisor', 
                       'Octal', 'Binary', 'Hexadecimal']
            
            print("\n" + "="*60)
            print("KEYWORD SEARCH:")
            print("="*60)
            for keyword in keywords:
                if keyword in all_text:
                    print(f"✓ Found: {keyword}")
                    # Get context around the keyword
                    idx = all_text.find(keyword)
                    start = max(0, idx - 50)
                    end = min(len(all_text), idx + 100)
                    context = all_text[start:end].replace('\n', ' ')
                    print(f"  Context: ...{context}...")
                else:
                    print(f"✗ Not found: {keyword}")
            
        except Exception as e:
            print(f"Error during element search: {e}")
        
        # Keep browser open for manual inspection
        print("\n" + "="*60)
        print("Browser will stay open for 30 seconds for manual inspection...")
        print("="*60)
        await asyncio.sleep(30)
        
        await browser.close()
        print("\nDebug complete!")


if __name__ == "__main__":
    asyncio.run(debug_page())
