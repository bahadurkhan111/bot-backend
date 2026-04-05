#!/usr/bin/env python3
"""
Quick access script for Gematrinator scraper

Usage:
    python run_gematrinator_scraper.py [start] [end]
    
Examples:
    python run_gematrinator_scraper.py           # Scrape 1-31
    python run_gematrinator_scraper.py 1 50      # Scrape 1-50
    python run_gematrinator_scraper.py 10 20     # Scrape 10-20
"""

import asyncio
import sys
from scripts.gematrinator_scraper import GematrinatorScraper


async def main():
    # Parse command line arguments
    if len(sys.argv) == 1:
        start, end = 1, 31
    elif len(sys.argv) == 3:
        start = int(sys.argv[1])
        end = int(sys.argv[2])
    else:
        print(__doc__)
        sys.exit(1)
    
    # Run scraper
    scraper = GematrinatorScraper(start_number=start, end_number=end)
    await scraper.scrape_all_numbers()
    scraper.print_summary()
    
    # Export to data folder
    filename = f"data/gematrinator_output/gematrinator_{start}_to_{end}.xlsx"
    scraper.export_to_excel(filename)
    
    print(f"\n✅ Scraping complete! File saved to: {filename}")


if __name__ == "__main__":
    asyncio.run(main())
