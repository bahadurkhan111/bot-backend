"""
Importer for Gematrinator Number Properties

Loads scraped data from Excel files into the NumberProperty model.
"""

import pandas as pd
from datetime import datetime
from pathlib import Path
from django.utils import timezone
from .models import NumberProperty


class NumberPropertyImporter:
    """Import number properties from Gematrinator Excel data."""
    
    def __init__(self, excel_path: str):
        """
        Initialize importer.
        
        Args:
            excel_path: Path to the Gematrinator Excel file
        """
        self.excel_path = Path(excel_path)
        if not self.excel_path.exists():
            raise FileNotFoundError(f"Excel file not found: {excel_path}")
        
        self.df = None
        self.imported_count = 0
        self.skipped_count = 0
        self.errors = []
    
    def load_excel(self):
        """Load the Excel file into a DataFrame."""
        print(f"Loading Excel file: {self.excel_path}")
        self.df = pd.read_excel(self.excel_path)
        print(f"Loaded {len(self.df)} rows, {len(self.df.columns)} columns")
        return self.df
    
    def import_all(self, force_update: bool = False):
        """
        Import all number properties from Excel to database.
        
        Args:
            force_update: If True, update existing records. If False, skip existing.
            
        Returns:
            Dictionary with import statistics
        """
        if self.df is None:
            self.load_excel()
        
        print(f"\nImporting {len(self.df)} number properties...")
        
        for idx, row in self.df.iterrows():
            try:
                self._import_row(row, force_update)
            except Exception as e:
                error_msg = f"Error importing row {idx} (number {row.get('number', 'unknown')}): {e}"
                self.errors.append(error_msg)
                print(f"  ❌ {error_msg}")
        
        stats = {
            'total_rows': len(self.df),
            'imported': self.imported_count,
            'skipped': self.skipped_count,
            'errors': len(self.errors),
            'error_messages': self.errors
        }
        
        print(f"\n{'='*60}")
        print(f"Import complete!")
        print(f"  Imported: {stats['imported']}")
        print(f"  Skipped:  {stats['skipped']}")
        print(f"  Errors:   {stats['errors']}")
        print(f"{'='*60}")
        
        return stats
    
    def _import_row(self, row, force_update: bool = False):
        """
        Import a single row from the DataFrame.
        
        Args:
            row: pandas Series representing one row
            force_update: Whether to update existing records
        """
        number = int(row['number'])
        
        # Check if already exists
        if NumberProperty.objects.filter(number=number).exists() and not force_update:
            self.skipped_count += 1
            print(f"  ⏭️  Skipped number {number} (already exists)")
            return
        
        # Calculate condensed number (numerological reduction)
        condensed = NumberProperty.calculate_condensed_number(number)
        
        # Parse scraped_at timestamp
        scraped_at = None
        if pd.notna(row.get('scrape_timestamp')):
            try:
                scraped_at = pd.to_datetime(row['scrape_timestamp'])
            except:
                scraped_at = timezone.now()
        
        # Prepare data
        data = {
            'number': number,
            'condensed_number': condensed,
            
            # Sequence membership (boolean)
            'is_prime': bool(row.get('is_prime', False)),
            'is_composite': bool(row.get('composite_is_sequence', False)),
            'is_fibonacci': bool(row.get('fibonacci_is_sequence', False)),
            'is_triangular': bool(row.get('triangular_is_sequence', False)),
            'is_square': bool(row.get('square_is_sequence', False)),
            'is_cube': bool(row.get('cube_is_sequence', False)),
            'is_tetrahedral': bool(row.get('tetrahedral_is_sequence', False)),
            'is_square_pyramidal': bool(row.get('square_pyramidal_is_sequence', False)),
            'is_star': bool(row.get('star_is_sequence', False)),
            'is_pentagonal': bool(row.get('pentagonal_is_sequence', False)),
            
            # Sequence positions
            'prime_position': self._parse_int(row.get('prime_position')),
            'composite_position': self._parse_int(row.get('composite_position')),
            'fibonacci_position': self._parse_int(row.get('fibonacci_position')),
            'triangular_position': self._parse_int(row.get('triangular_position')),
            'square_position': self._parse_int(row.get('square_position')),
            'cube_position': self._parse_int(row.get('cube_position')),
            'tetrahedral_position': self._parse_int(row.get('tetrahedral_position')),
            'square_pyramidal_position': self._parse_int(row.get('square_pyramidal_position')),
            'star_position': self._parse_int(row.get('star_position')),
            'pentagonal_position': self._parse_int(row.get('pentagonal_position')),
            
            # Nth values
            'prime_nth_value': self._parse_int(row.get('prime_nth_value')),
            'composite_nth_value': self._parse_int(row.get('composite_nth_value')),
            'fibonacci_nth_value': self._parse_int(row.get('fibonacci_nth_value')),
            'triangular_nth_value': self._parse_int(row.get('triangular_nth_value')),
            'square_nth_value': self._parse_int(row.get('square_nth_value')),
            'cube_nth_value': self._parse_int(row.get('cube_nth_value')),
            'tetrahedral_nth_value': self._parse_int(row.get('tetrahedral_nth_value')),
            'square_pyramidal_nth_value': self._parse_int(row.get('square_pyramidal_nth_value')),
            'star_nth_value': self._parse_int(row.get('star_nth_value')),
            'pentagonal_nth_value': self._parse_int(row.get('pentagonal_nth_value')),
            
            # Divisors
            'divisors_count': self._parse_int(row.get('divisors_count')),
            'divisors_sum': self._parse_int(row.get('divisors_sum')),
            'divisors_list': self._parse_list(row.get('divisors_list')),
            
            # Conversions
            'conversion_binary': str(row.get('conversion_binary', '')),
            'conversion_octal': str(row.get('conversion_octal', '')),
            'conversion_duodecimal': str(row.get('conversion_duodecimal', '')),
            'conversion_hexadecimal': str(row.get('conversion_hexadecimal', '')),
            'roman_numeral': str(row.get('roman_numeral', '')),
            
            # Mathematical
            'natural_logarithm': self._parse_float(row.get('natural_logarithm')),
            
            # Metadata
            'source_url': str(row.get('url', '')),
            'scraped_at': scraped_at,
            'properties_json': self._row_to_clean_dict(row),
        }
        
        # Create or update
        obj, created = NumberProperty.objects.update_or_create(
            number=number,
            defaults=data
        )
        
        self.imported_count += 1
        action = "✓ Created" if created else "↻ Updated"
        print(f"  {action} number {number} (condensed: {condensed})")
    
    @staticmethod
    def _parse_int(value):
        """Parse integer, return None if NaN or invalid."""
        if pd.isna(value):
            return None
        try:
            return int(value)
        except (ValueError, TypeError):
            return None
    
    @staticmethod
    def _parse_float(value):
        """Parse float, return None if NaN or invalid."""
        if pd.isna(value):
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None
    
    @staticmethod
    def _parse_list(value):
        """Parse list from string, return None if invalid."""
        if pd.isna(value):
            return None
        if isinstance(value, list):
            return value
        if isinstance(value, str):
            # Try to parse as comma-separated values
            try:
                return [int(x.strip()) for x in value.split(',')]
            except:
                return None
        return None
    
    @staticmethod
    def _row_to_clean_dict(row):
        """
        Convert pandas Series to dict, replacing NaN with None.
        This ensures JSON compatibility for PostgreSQL JSONField.
        """
        data = row.to_dict()
        clean_data = {}
        for key, value in data.items():
            if pd.isna(value):
                clean_data[key] = None
            else:
                clean_data[key] = value
        return clean_data


def import_from_file(file_path: str, force_update: bool = False):
    """
    Convenience function to import from a file.
    
    Args:
        file_path: Path to Excel file
        force_update: Whether to update existing records
        
    Returns:
        Import statistics dictionary
    """
    importer = NumberPropertyImporter(file_path)
    return importer.import_all(force_update=force_update)
