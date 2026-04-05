#!/usr/bin/env python3
"""
Installation and usage instructions for Gematrinator Number Scraper
"""

# INSTALLATION INSTRUCTIONS
"""
1. Install required packages:
   pip install playwright pandas openpyxl

2. Install Playwright browsers:
   playwright install chromium

3. Run the scraper:
   python scripts/gematrinator_number_scraper.py
"""

# USAGE EXAMPLES
"""
Basic usage (scrape numbers 1-31):
    python scripts/gematrinator_number_scraper.py

Custom range in Python code:
    from scripts.gematrinator_number_scraper import GematrinatorScraper
    import asyncio
    
    async def custom_scrape():
        scraper = GematrinatorScraper(start_number=1, end_number=50)
        await scraper.scrape_all_numbers()
        scraper.export_to_excel("custom_output.xlsx")
    
    asyncio.run(custom_scrape())
"""

# OUTPUT FORMAT
"""
The Excel file will contain columns for:
- number: The number being analyzed (1-31)
- url: Source URL
- scrape_timestamp: When data was collected

Number Sequences:
- prime_position
- composite_position
- fibonacci_position
- triangular_position
- square_position
- cube_position
- tetrahedral_position
- square_pyramidal_position
- star_position
- pentagonal_position

Divisors:
- divisors_count
- divisors_list
- divisors_sum
- divisors_composite_position

Conversions:
- conversion_octal
- conversion_duodecimal
- conversion_hexadecimal
- conversion_binary

Additional Properties:
- natural_logarithm
- is_prime
- next_indicator
- roman_numeral
"""
