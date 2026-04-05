"""
Management command to import number properties from Gematrinator Excel file.
"""

from django.core.management.base import BaseCommand
from pathlib import Path
from apps.number_properties.importer import NumberPropertyImporter


class Command(BaseCommand):
    help = 'Import number properties from Gematrinator Excel file into database'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--source',
            type=str,
            default='data/gematrinator_output/',
            help='Path to Excel file or directory containing Gematrinator data'
        )
        parser.add_argument(
            '--file',
            type=str,
            help='Specific Excel filename (if source is a directory)'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force update existing records'
        )
    
    def handle(self, *args, **options):
        source = options['source']
        specific_file = options.get('file')
        force_update = options['force']
        
        # Determine the Excel file path
        source_path = Path(source)
        
        if specific_file:
            excel_file = source_path / specific_file
        elif source_path.is_file() and source_path.suffix == '.xlsx':
            excel_file = source_path
        elif source_path.is_dir():
            # Find the most recent Gematrinator Excel file
            excel_files = list(source_path.glob('gematrinator_numbers_*.xlsx'))
            if not excel_files:
                self.stdout.write(
                    self.style.ERROR(
                        f'No Gematrinator Excel files found in {source_path}'
                    )
                )
                return
            excel_file = max(excel_files, key=lambda p: p.stat().st_mtime)
            self.stdout.write(
                self.style.SUCCESS(f'Found most recent file: {excel_file.name}')
            )
        else:
            self.stdout.write(
                self.style.ERROR(f'Invalid source path: {source}')
            )
            return
        
        if not excel_file.exists():
            self.stdout.write(
                self.style.ERROR(f'File not found: {excel_file}')
            )
            return
        
        self.stdout.write(f'\nImporting from: {excel_file}')
        self.stdout.write(f'Force update: {force_update}\n')
        
        # Import
        try:
            importer = NumberPropertyImporter(str(excel_file))
            stats = importer.import_all(force_update=force_update)
            
            # Display results
            self.stdout.write('\n' + '='*60)
            self.stdout.write(self.style.SUCCESS('✓ Import completed successfully!'))
            self.stdout.write(f'  Total rows:  {stats["total_rows"]}')
            self.stdout.write(
                self.style.SUCCESS(f'  Imported:    {stats["imported"]}')
            )
            
            if stats['skipped'] > 0:
                self.stdout.write(
                    self.style.WARNING(f'  Skipped:     {stats["skipped"]}')
                )
            
            if stats['errors'] > 0:
                self.stdout.write(
                    self.style.ERROR(f'  Errors:      {stats["errors"]}')
                )
                self.stdout.write('\nError messages:')
                for error in stats['error_messages']:
                    self.stdout.write(self.style.ERROR(f'  - {error}'))
            
            self.stdout.write('='*60 + '\n')
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'\n❌ Import failed: {e}')
            )
            raise
