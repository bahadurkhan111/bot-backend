"""
Gematrinator Web Scraper
Extrae las fórmulas y propiedades numéricas de gematrinator.com
Requiere: pip install playwright
Luego ejecutar: playwright install chromium
"""

from playwright.sync_api import sync_playwright
import json
import time

def scrape_number_properties(number, save_to_file=True):
    """
    Extrae todas las propiedades de un número desde gematrinator.com
    
    Args:
        number: El número a analizar
        save_to_file: Si True, guarda los resultados en JSON
    
    Returns:
        dict: Diccionario con todas las propiedades del número
    """
    
    url = f"https://www.gematrinator.com/calculator/properties/index.php?num={number}"
    
    with sync_playwright() as p:
        # Lanzar navegador (headless=False para ver qué hace)
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        print(f"Accediendo a: {url}")
        page.goto(url, wait_until="networkidle")
        
        # Esperar a que la página cargue completamente
        time.sleep(2)
        
        properties = {
            "number": number,
            "factorization": {},
            "sequences": {},
            "divisors": {},
            "special_properties": []
        }
        
        try:
            # Extraer factorización
            factorization_elem = page.locator("text=/Prime Factorization/").locator("..").locator("td").nth(1)
            if factorization_elem.count() > 0:
                properties["factorization"]["text"] = factorization_elem.inner_text()
            
            # Extraer divisores
            divisors_elem = page.locator("text=/Divisors/").locator("..").locator("td").nth(1)
            if divisors_elem.count() > 0:
                properties["divisors"]["list"] = divisors_elem.inner_text()
            
            # Extraer suma de divisores
            sum_divisors_elem = page.locator("text=/Sum of Divisors/").locator("..").locator("td").nth(1)
            if sum_divisors_elem.count() > 0:
                properties["divisors"]["sum"] = sum_divisors_elem.inner_text()
            
            # Extraer todas las filas de la tabla
            rows = page.locator("table tr").all()
            
            for row in rows:
                cells = row.locator("td").all()
                if len(cells) >= 2:
                    label = cells[0].inner_text().strip()
                    value = cells[1].inner_text().strip()
                    
                    # Buscar patrones de secuencias
                    if "Prime" in label:
                        properties["sequences"]["prime"] = value
                    elif "Composite" in label:
                        properties["sequences"]["composite"] = value
                    elif "Fibonacci" in label:
                        properties["sequences"]["fibonacci"] = value
                    elif "Triangular" in label:
                        properties["sequences"]["triangular"] = value
                    elif "Square" in label and "Pyramidal" not in label:
                        properties["sequences"]["square"] = value
                    elif "Cube" in label:
                        properties["sequences"]["cube"] = value
                    elif "Tetrahedral" in label:
                        properties["sequences"]["tetrahedral"] = value
                    elif "Square Pyramidal" in label:
                        properties["sequences"]["square_pyramidal"] = value
                    elif "Star" in label:
                        properties["sequences"]["star"] = value
                    elif "Pentagonal" in label:
                        properties["sequences"]["pentagonal"] = value
                    
                    # Propiedades especiales
                    if "Perfect" in label or "Abundant" in label or "Deficient" in label:
                        properties["special_properties"].append({label: value})
            
            print(f"\n✅ Datos extraídos para el número {number}")
            print(json.dumps(properties, indent=2, ensure_ascii=False))
            
            # Guardar a archivo JSON
            if save_to_file:
                filename = f"gematrinator_{number}.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(properties, f, indent=2, ensure_ascii=False)
                print(f"\n💾 Guardado en: {filename}")
            
        except Exception as e:
            print(f"❌ Error extrayendo datos: {e}")
        
        finally:
            browser.close()
        
        return properties


def scrape_multiple_numbers(numbers_list, delay=3):
    """
    Extrae propiedades de múltiples números
    
    Args:
        numbers_list: Lista de números a analizar
        delay: Segundos de espera entre cada solicitud (para no sobrecargar el servidor)
    """
    all_results = {}
    
    for num in numbers_list:
        print(f"\n{'='*60}")
        print(f"Procesando número: {num}")
        print('='*60)
        
        result = scrape_number_properties(num)
        all_results[num] = result
        
        if num != numbers_list[-1]:  # No esperar después del último
            print(f"\n⏳ Esperando {delay} segundos antes del siguiente...")
            time.sleep(delay)
    
    # Guardar todos los resultados en un archivo consolidado
    with open("gematrinator_all_results.json", 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    
    print(f"\n\n🎉 Proceso completado. Todos los resultados guardados en: gematrinator_all_results.json")
    return all_results


if __name__ == "__main__":
    # Ejemplo de uso: extrae propiedades de un solo número
    print("🔍 Gematrinator Scraper - Extracción de Propiedades Numéricas\n")
    
    # Opción 1: Un solo número
    # scrape_number_properties(144)
    
    # Opción 2: Múltiples números (los que ya probaste)
    test_numbers = [6, 28, 55, 144]
    scrape_multiple_numbers(test_numbers, delay=3)
    
    # Opción 3: Rango de números (cuidado con no hacer muchas solicitudes)
    # numbers = list(range(1, 101))  # Del 1 al 100
    # scrape_multiple_numbers(numbers, delay=2)
