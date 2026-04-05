# Gematrinator Number Properties Scraper

Web scraper para extraer propiedades numéricas de Gematrinator.com (números 1-31) y exportar a Excel.

## 📁 Estructura del Proyecto

```
scripts/gematrinator_scraper/
├── gematrinator_number_scraper.py  # Scraper principal
├── test_gematrinator_scraper.py    # Tests de validación
├── debug_gematrinator.py            # Script de depuración
├── requirements.txt                 # Dependencias Python
├── README.py                        # Documentación adicional
└── README.md                        # Este archivo

data/gematrinator_output/
└── gematrinator_numbers_*.xlsx     # Archivos Excel generados
```

## 🚀 Instalación

```bash
# Instalar dependencias
pip install -r scripts/gematrinator_scraper/requirements.txt

# Instalar navegadores de Playwright
playwright install chromium
```

## 📊 Uso

### Ejecutar el scraper completo (números 1-31)
```bash
python scripts/gematrinator_scraper/gematrinator_number_scraper.py
```

### Ejecutar tests
```bash
python scripts/gematrinator_scraper/test_gematrinator_scraper.py
```

### Uso programático
```python
import asyncio
from scripts.gematrinator_scraper.gematrinator_number_scraper import GematrinatorScraper

async def scrape_custom_range():
    scraper = GematrinatorScraper(start_number=1, end_number=50)
    results = await scraper.scrape_all_numbers()
    scraper.export_to_excel("mi_output.xlsx")

asyncio.run(scrape_custom_range())
```

## 📈 Datos Extraídos (44 columnas)

### Secuencias Numéricas
- **IS Sequence**: Indica si el número ES parte de una secuencia específica
  - `prime_is_sequence`, `fibonacci_is_sequence`, `triangular_is_sequence`, etc.
  
- **Nth Values**: Valor N-ésimo de cada secuencia
  - `prime_nth_value`: El N-ésimo número primo
  - `fibonacci_nth_value`: El N-ésimo número de Fibonacci
  - `triangular_nth_value`, `square_nth_value`, `cube_nth_value`, etc.

### Conversiones de Base
- `conversion_octal`: Representación octal
- `conversion_duodecimal`: Representación duodecimal
- `conversion_hexadecimal`: Representación hexadecimal
- `conversion_binary`: Representación binaria

### Propiedades Adicionales
- `is_prime`: Booleano indicando si es primo
- `prime_position`: Posición en la secuencia de primos (si aplica)
- `natural_logarithm`: Logaritmo natural
- `roman_numeral`: Representación en números romanos

### Divisores (cuando aplica)
- `divisors_count`: Cantidad de divisores
- `divisors_list`: Lista de divisores
- `divisors_sum`: Suma de divisores

## ✨ Características

- ✅ Logs detallados en cada paso del proceso
- ✅ Espera inteligente para contenido JavaScript dinámico
- ✅ Extracción completa de todas las propiedades numéricas
- ✅ Exportación automática a Excel con pandas
- ✅ Manejo de errores robusto
- ✅ Tests automatizados incluidos
- ✅ Configurable para cualquier rango de números

## 🔧 Requisitos

- Python 3.11+
- playwright >= 1.40.0
- pandas >= 2.0.0
- openpyxl >= 3.1.0

## 📝 Ejemplo de Salida

```
[INIT] Launching browser...
[INIT] Browser ready
[START] Scraping numbers 1 to 31
[1/31] Starting scrape for number 1...
  → Loading URL: https://gematrinator.com/number-properties?number=1
  → Content loaded successfully
  → Extracting sequences...
    • Parsing number sequences...
      ✓ Prime #N = 2
      ✓ Fibonacci #N = 1
  → Extracting conversions...
    ✓ Binary: 1
  ✓ Successfully scraped
...
[EXPORT] ✓ Data exported to: gematrinator_numbers_20260111_192724.xlsx
```

## 📞 Soporte

Para más información sobre el uso y personalización del scraper, consulta los comentarios en el código fuente o ejecuta el script de debug para inspeccionar páginas específicas.
