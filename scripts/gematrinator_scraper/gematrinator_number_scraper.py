#!/usr/bin/env python3
"""
Gematrinator Number Properties Scraper

Extracts all number properties from Gematrinator.com for numbers 1-31
and exports to Excel.

Requirements:
- playwright
- pandas
- openpyxl
"""

import asyncio
import re
from typing import Dict, List, Optional, Any
from datetime import datetime
from playwright.async_api import async_playwright, Page
import pandas as pd


class GematrinatorScraper:
    """Scraper for Gematrinator.com number properties."""
    
    BASE_URL = "https://gematrinator.com/number-properties?number={}"
    
    def __init__(self, start_number: int = 1, end_number: int = 31):
        """Initialize scraper with number range."""
        self.start_number = start_number
        self.end_number = end_number
        self.results: List[Dict[str, Any]] = []
    
    async def scrape_all_numbers(self) -> List[Dict[str, Any]]:
        """Scrape all numbers in the specified range."""
        async with async_playwright() as p:
            # Launch browser (headless mode)
            print("[INIT] Launching browser...")
            browser = await p.chromium.launch(headless=True)
            print("[INIT] Creating browser context...")
            context = await browser.new_context(
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            )
            page = await context.new_page()
            print("[INIT] Browser ready")
            
            print(f"\n[START] Scraping numbers {self.start_number} to {self.end_number}")
            print(f"[START] Total numbers to scrape: {self.end_number - self.start_number + 1}")
            
            for number in range(self.start_number, self.end_number + 1):
                print(f"\n[{number}/{self.end_number}] Starting scrape for number {number}...")
                data = await self.scrape_number(page, number)
                self.results.append(data)
                
                if 'error' in data:
                    print(f"[{number}/{self.end_number}] ⚠️  Error: {data['error']}")
                else:
                    print(f"[{number}/{self.end_number}] ✓ Successfully scraped")
                
                # Small delay to be respectful to the server
                await asyncio.sleep(1)
            
            print("\n[CLEANUP] Closing browser...")
            await browser.close()
            print("[CLEANUP] Browser closed")
        
        return self.results
    
    async def scrape_number(self, page: Page, number: int) -> Dict[str, Any]:
        """Scrape all properties for a single number."""
        url = self.BASE_URL.format(number)
        
        try:
            print(f"  → Loading URL: {url}")
            await page.goto(url, wait_until="domcontentloaded", timeout=60000)
            print(f"  → Page loaded, waiting for JavaScript content...")
            # Wait for the HTMLSpot div to be populated (it's empty initially)
            try:
                await page.wait_for_selector('#HTMLSpot table', timeout=10000)
                print(f"  → Content loaded successfully")
            except:
                print(f"  → Warning: Timeout waiting for content, proceeding anyway")
            
            # Additional wait to ensure all content is rendered
            await asyncio.sleep(3)
            print(f"  → Extracting data...")
            
            # Initialize data dictionary
            data = {
                'number': number,
                'url': url,
                'scrape_timestamp': datetime.now().isoformat()
            }
            
            # Extract all sections
            print(f"  → Extracting sequences...")
            data.update(await self.extract_number_sequences(page))
            print(f"  → Extracting divisors...")
            data.update(await self.extract_divisors(page))
            print(f"  → Extracting conversions...")
            data.update(await self.extract_conversions(page))
            print(f"  → Extracting additional properties...")
            data.update(await self.extract_additional_properties(page))
            
            print(f"  → Data extraction complete")
            return data
            
        except Exception as e:
            print(f"  ✗ ERROR scraping number {number}: {e}")
            import traceback
            print(f"  ✗ Traceback: {traceback.format_exc()[:200]}...")
            return {
                'number': number,
                'url': url,
                'error': str(e),
                'scrape_timestamp': datetime.now().isoformat()
            }
    
    async def extract_number_sequences(self, page: Page) -> Dict[str, Any]:
        """Extract all mathematical sequence information."""
        sequences = {}
        print(f"    • Parsing number sequences...")
        
        sequence_types = [
            'Prime',
            'Composite',
            'Fibonacci',
            'Triangular',
            'Square',
            'Cube',
            'Tetrahedral',
            'Square Pyramidal',
            'Star',
            'Pentagonal'
        ]
        
        try:
            content = await page.content()
            
            # Check if number IS a special sequence (e.g., "4th Prime!")
            for seq_type in sequence_types:
                key = seq_type.lower().replace(' ', '_')
                
                # Pattern 1: Number IS this sequence type (e.g., "<a>4</a>th Prime!")
                # Looking for: <a href...>NUMBER</a></b>th Prime!</td>
                is_sequence_pattern = rf'<a[^>]*>(\d+)</a></b>(?:st|nd|rd|th).*?{seq_type}!'
                is_match = re.search(is_sequence_pattern, content, re.IGNORECASE | re.DOTALL)
                if is_match:
                    sequences[f'{key}_is_sequence'] = is_match.group(1)
                    sequences[f'{key}_position'] = is_match.group(1)
                    print(f"      ✓ IS {seq_type} #{is_match.group(1)}")
                else:
                    sequences[f'{key}_is_sequence'] = None
            
            # Extract the "Nth..." table - what each sequence's Nth value is
            # Looking for: <td class="RelativeClass"> Prime #: &nbsp;</td><td class="RelativeNum"><b...><a...>17</a>
            for seq_type in sequence_types:
                key = seq_type.lower().replace(' ', '_')
                
                # Find the Nth value of each sequence
                pattern = rf'<td class="RelativeClass">\s*{seq_type}\s*#:\s*&nbsp;</td><td class="RelativeNum"><b[^>]*><a[^>]*>(\d+)</a>'
                match = re.search(pattern, content, re.IGNORECASE)
                
                if match:
                    sequences[f'{key}_nth_value'] = match.group(1)
                    if f'{key}_position' not in sequences or sequences[f'{key}_position'] is None:
                        sequences[f'{key}_position'] = None
                    print(f"      ✓ {seq_type} #N = {match.group(1)}")
                else:
                    sequences[f'{key}_nth_value'] = None
                    if f'{key}_position' not in sequences:
                        sequences[f'{key}_position'] = None
                
        except Exception as e:
            print(f"  Warning: Could not extract sequences: {e}")
            import traceback
            traceback.print_exc()
        
        return sequences
    
    async def extract_divisors(self, page: Page) -> Dict[str, Any]:
        """Extract divisor information."""
        divisors_data = {}
        print(f"    • Parsing divisors...")
        
        try:
            content = await page.content()
            
            # Extract divisor count
            count_match = re.search(r'Count:\s*(\d+)', content)
            divisors_data['divisors_count'] = count_match.group(1) if count_match else None
            if count_match:
                print(f"      ✓ Divisors count: {count_match.group(1)}")
            
            # Extract divisor list
            # Look for pattern like "List: 1, 2, 3, 4, 6, 12"
            list_match = re.search(r'List:\s*([\d,\s]+)', content)
            if list_match:
                divisor_list = list_match.group(1).strip()
                divisors_data['divisors_list'] = divisor_list
            else:
                divisors_data['divisors_list'] = None
            
            # Extract divisor sum
            sum_match = re.search(r'Sum:\s*(\d+)', content)
            divisors_data['divisors_sum'] = sum_match.group(1) if sum_match else None
            
            # Extract composite number position in divisors section
            comp_match = re.search(r'Composite #\s*(\d+)', content)
            divisors_data['divisors_composite_position'] = comp_match.group(1) if comp_match else None
            
        except Exception as e:
            print(f"  Warning: Could not extract divisors: {e}")
            divisors_data['divisors_count'] = None
            divisors_data['divisors_list'] = None
            divisors_data['divisors_sum'] = None
        
        return divisors_data
    
    async def extract_conversions(self, page: Page) -> Dict[str, Any]:
        """Extract base conversion information."""
        conversions = {}
        print(f"    • Parsing conversions...")
        
        conversion_types = [
            ('Octal', 'octal'),
            ('Duodecimal', 'duodecimal'),
            ('Hexadecimal', 'hexadecimal'),
            ('Binary', 'binary')
        ]
        
        try:
            content = await page.content()
            
            for display_name, key in conversion_types:
                # Pattern to match conversion table rows
                # <td>7</td><td>Octal</td><td>7</td>
                # <td>-</td><td>Binary</td><td>111</td>
                pattern = rf'<td[^>]*>.*?</td><td[^>]*>{display_name}</td><td[^>]*><b[^>]*><a[^>]*>(\d+)</a>'
                match = re.search(pattern, content, re.IGNORECASE)
                
                if match:
                    conversions[f'conversion_{key}'] = match.group(1)
                    print(f"      ✓ {display_name}: {match.group(1)}")
                else:
                    conversions[f'conversion_{key}'] = None
            
        except Exception as e:
            print(f"  Warning: Could not extract conversions: {e}")
            for _, key in conversion_types:
                conversions[f'conversion_{key}'] = None
        
        return conversions
    
    async def extract_additional_properties(self, page: Page) -> Dict[str, Any]:
        """Extract additional properties like ln, prime status, etc."""
        properties = {}
        print(f"    • Parsing additional properties...")
        
        try:
            content = await page.content()
            
            # Check if number IS a prime (appears as "Xth Prime!")
            is_prime_pattern = r'<a[^>]*>(\d+)</a></b>(?:st|nd|rd|th).*?Prime!'
            is_prime_match = re.search(is_prime_pattern, content, re.IGNORECASE | re.DOTALL)
            properties['is_prime'] = bool(is_prime_match)
            if is_prime_match:
                properties['prime_position'] = is_prime_match.group(1)
                print(f"      ✓ IS Prime (position {is_prime_match.group(1)})")
            else:
                properties['prime_position'] = None
            
            # Extract natural logarithm (if present)
            ln_match = re.search(r'ln[:\s]+([\d.]+)', content, re.IGNORECASE)
            properties['natural_logarithm'] = ln_match.group(1) if ln_match else None
            if ln_match:
                print(f"      ✓ Natural log: {ln_match.group(1)}")
            
            # Extract Roman numeral (if present) - avoid matching single 'i' from other places
            roman_match = re.search(r'Roman[:\s]*([IVXLCDM]{2,})', content, re.IGNORECASE)
            properties['roman_numeral'] = roman_match.group(1) if roman_match else None
            if roman_match:
                print(f"      ✓ Roman: {roman_match.group(1)}")
            
        except Exception as e:
            print(f"  Warning: Could not extract additional properties: {e}")
            properties['natural_logarithm'] = None
            properties['is_prime'] = False
            properties['prime_position'] = None
        
        return properties
    
    def export_to_excel(self, filename: str = None) -> str:
        """Export scraped data to Excel file."""
        if not self.results:
            raise ValueError("No data to export. Run scrape_all_numbers() first.")
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"gematrinator_numbers_{timestamp}.xlsx"
        
        print(f"\n[EXPORT] Converting {len(self.results)} records to DataFrame...")
        # Convert to DataFrame
        df = pd.DataFrame(self.results)
        
        # Reorder columns to put number first
        cols = ['number'] + [col for col in df.columns if col != 'number']
        df = df[cols]
        
        print(f"[EXPORT] Writing to Excel file: {filename}...")
        # Export to Excel
        df.to_excel(filename, index=False, engine='openpyxl')
        
        print(f"[EXPORT] ✓ Data exported to: {filename}")
        print(f"[EXPORT] Total rows: {len(df)}")
        print(f"[EXPORT] Total columns: {len(df.columns)}")
        
        return filename
    
    def print_summary(self):
        """Print a summary of scraped data."""
        if not self.results:
            print("No data scraped yet.")
            return
        
        print(f"\n{'='*60}")
        print(f"SCRAPING SUMMARY")
        print(f"{'='*60}")
        print(f"Total numbers scraped: {len(self.results)}")
        print(f"Range: {self.start_number} to {self.end_number}")
        
        # Count errors
        errors = sum(1 for r in self.results if 'error' in r)
        print(f"Errors encountered: {errors}")
        
        if errors == 0:
            print("\n✓ All numbers scraped successfully!")
        
        # Show sample data
        if self.results:
            print(f"\nSample data (first number):")
            first = self.results[0]
            for key, value in list(first.items())[:10]:
                print(f"  {key}: {value}")
            print("  ...")


async def main():
    """Main execution function."""
    print("="*60)
    print("GEMATRINATOR NUMBER PROPERTIES SCRAPER")
    print("="*60)
    print()
    
    # Create scraper instance
    scraper = GematrinatorScraper(start_number=1, end_number=31)
    
    # Scrape all numbers
    print("Starting web scraping...")
    results = await scraper.scrape_all_numbers()
    
    # Print summary
    scraper.print_summary()
    
    # Export to Excel
    print("\nExporting to Excel...")
    filename = scraper.export_to_excel()
    
    print(f"\n{'='*60}")
    print("SCRAPING COMPLETE!")
    print(f"{'='*60}")
    print(f"Output file: {filename}")
    print()


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
