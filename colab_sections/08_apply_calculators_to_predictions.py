# -*- coding: utf-8 -*-
"""
SECTION 8: APPLY 35 CALCULATORS TO EACH MODEL PREDICTION
Show all 35 mathematical operations for each of the 4 models
"""

print("\n\n" + "="*100)
print("35 CALCULATORS APPLIED TO EACH MODEL / 35 CALCULADORAS APLICADAS A CADA MODELO")
print("="*100)

# Organize predictions
RandomForestPrediction = RandomForestModel
XGBPrediction = XGBModelResult
LinearRegressionPrediction = LinearRegressionModel
LassoPrediction = Lasso_model

models_data = {
    'Random Forest': RandomForestPrediction,
    'XGB': XGBPrediction,
    'Linear Regression': LinearRegressionPrediction,
    'Lasso': LassoPrediction
}

print("\n" + "="*100)
print("MODEL PREDICTIONS / PREDICCIONES DE LOS MODELOS")
print("="*100)
for model_name, prediction in models_data.items():
    print(f"{model_name:20s}: {prediction:.6f}")

# Apply 35 calculators to each model prediction
calc = MathCalculators()

for model_name, prediction_value in models_data.items():
    print("\n\n" + "="*100)
    print(f"CALCULATORS FOR {model_name.upper()} MODEL / CALCULADORAS PARA MODELO {model_name.upper()}")
    print(f"Prediction / Predicción: {prediction_value:.6f}")
    print("="*100)
    
    print("\n" + "-"*100)
    print("1. NATURAL LOGARITHM (ln) / LOGARITMO NATURAL (ln)")
    print("-" * 100)
    ln_result = calc.natural_log(abs(prediction_value) + 1)
    print(f"   Formula: ln(x)")
    print(f"   Result / Resultado: ln({prediction_value:.6f}) = {ln_result:.6f}")
    
    print("\n" + "-"*100)
    print("2. LOGARITHM BASE-10 / LOGARITMO BASE-10")
    print("-" * 100)
    log10_result = calc.logarithm(abs(prediction_value) + 1, 10)
    print(f"   Formula: log₁₀(x)")
    print(f"   Result / Resultado: log₁₀({prediction_value:.6f}) = {log10_result:.6f}")
    
    print("\n" + "-"*100)
    print("3. LOGARITHM BASE-2 / LOGARITMO BASE-2")
    print("-" * 100)
    log2_result = calc.logarithm(abs(prediction_value) + 1, 2)
    print(f"   Formula: log₂(x)")
    print(f"   Result / Resultado: log₂({prediction_value:.6f}) = {log2_result:.6f}")
    
    print("\n" + "-"*100)
    print("4. SQUARE ROOT / RAÍZ CUADRADA")
    print("-" * 100)
    sqrt_result = calc.square_root(abs(prediction_value))
    print(f"   Formula: √x")
    print(f"   Result / Resultado: √{prediction_value:.6f} = {sqrt_result:.6f}")
    
    print("\n" + "-"*100)
    print("5. SQUARED / CUADRADO")
    print("-" * 100)
    squared_result = calc.exponent(prediction_value, 2)
    print(f"   Formula: x²")
    print(f"   Result / Resultado: ({prediction_value:.6f})² = {squared_result:.6f}")
    
    print("\n" + "-"*100)
    print("6. CUBED / CUBO")
    print("-" * 100)
    cubed_result = calc.exponent(prediction_value, 3)
    print(f"   Formula: x³")
    print(f"   Result / Resultado: ({prediction_value:.6f})³ = {cubed_result:.6f}")
    
    print("\n" + "-"*100)
    print("7. FACTORIAL / FACTORIAL")
    print("-" * 100)
    n = min(abs(int(prediction_value)), 10)
    factorial_result = calc.factorial(n)
    print(f"   Formula: n!")
    print(f"   Result / Resultado: {n}! = {factorial_result:.0f}")
    
    print("\n" + "-"*100)
    print("8. EXPONENTIAL (e^x) / EXPONENCIAL (e^x)")
    print("-" * 100)
    exp_input = min(prediction_value / 100, 10)
    exp_result = calc.antilog(exp_input, math.e)
    print(f"   Formula: e^x")
    print(f"   Result / Resultado: e^{exp_input:.6f} = {exp_result:.6f}")
    
    print("\n" + "-"*100)
    print("9. SINE (normalized) / SENO (normalizado)")
    print("-" * 100)
    angle = (prediction_value % 360)
    sine_result = calc.sine(angle)
    print(f"   Formula: sin(α)")
    print(f"   Result / Resultado: sin({angle:.2f}°) = {sine_result:.6f}")
    
    print("\n" + "-"*100)
    print("10. COSINE (normalized) / COSENO (normalizado)")
    print("-" * 100)
    cosine_result = calc.cosine(angle)
    print(f"   Formula: cos(α)")
    print(f"   Result / Resultado: cos({angle:.2f}°) = {cosine_result:.6f}")
    
    print("\n" + "-"*100)
    print("11. TANGENT (normalized) / TANGENTE (normalizado)")
    print("-" * 100)
    tangent_result = calc.tangent(angle)
    print(f"   Formula: tan(α)")
    print(f"   Result / Resultado: tan({angle:.2f}°) = {tangent_result:.6f}")
    
    print("\n" + "-"*100)
    print("12. ABSOLUTE VALUE / VALOR ABSOLUTO")
    print("-" * 100)
    abs_result = abs(prediction_value)
    print(f"   Formula: |x|")
    print(f"   Result / Resultado: |{prediction_value:.6f}| = {abs_result:.6f}")
    
    print("\n" + "-"*100)
    print("13. RECIPROCAL / RECÍPROCO")
    print("-" * 100)
    reciprocal_result = 1 / (prediction_value + 1e-10)
    print(f"   Formula: 1/x")
    print(f"   Result / Resultado: 1/{prediction_value:.6f} = {reciprocal_result:.6f}")
    
    print("\n" + "-"*100)
    print("14. PERCENTAGE OF 100 / PORCENTAJE DE 100")
    print("-" * 100)
    pct_result = calc.percentage(prediction_value, 100)
    print(f"   Formula: x% of 100")
    print(f"   Result / Resultado: {prediction_value:.6f}% de 100 = {pct_result:.6f}")
    
    print("\n" + "-"*100)
    print("15. ADDITION WITH 100 / SUMA CON 100")
    print("-" * 100)
    add_result = calc.add(prediction_value, 100)
    print(f"   Formula: x + 100")
    print(f"   Result / Resultado: {prediction_value:.6f} + 100 = {add_result:.6f}")
    
    print("\n" + "-"*100)
    print("16. SUBTRACTION FROM 1000 / RESTA DE 1000")
    print("-" * 100)
    sub_result = calc.subtract(1000, prediction_value)
    print(f"   Formula: 1000 - x")
    print(f"   Result / Resultado: 1000 - {prediction_value:.6f} = {sub_result:.6f}")
    
    print("\n" + "-"*100)
    print("17. MULTIPLICATION BY 2 / MULTIPLICACIÓN POR 2")
    print("-" * 100)
    mult_result = calc.multiply(prediction_value, 2)
    print(f"   Formula: x × 2")
    print(f"   Result / Resultado: {prediction_value:.6f} × 2 = {mult_result:.6f}")
    
    print("\n" + "-"*100)
    print("18. DIVISION BY 2 / DIVISIÓN POR 2")
    print("-" * 100)
    div_quotient, div_remainder = calc.divide(prediction_value, 2)
    print(f"   Formula: x ÷ 2")
    print(f"   Result / Resultado: {prediction_value:.6f} ÷ 2 = {div_quotient:.0f} remainder / residuo {div_remainder:.6f}")
    
    print("\n" + "-"*100)
    print("19. MODULO 10 / MÓDULO 10")
    print("-" * 100)
    mod_result = prediction_value % 10
    print(f"   Formula: x mod 10")
    print(f"   Result / Resultado: {prediction_value:.6f} mod 10 = {mod_result:.6f}")
    
    print("\n" + "-"*100)
    print("20. FLOOR / PISO")
    print("-" * 100)
    floor_result = math.floor(prediction_value)
    print(f"   Formula: ⌊x⌋")
    print(f"   Result / Resultado: ⌊{prediction_value:.6f}⌋ = {floor_result}")
    
    print("\n" + "-"*100)
    print("21. CEILING / TECHO")
    print("-" * 100)
    ceil_result = math.ceil(prediction_value)
    print(f"   Formula: ⌈x⌉")
    print(f"   Result / Resultado: ⌈{prediction_value:.6f}⌉ = {ceil_result}")
    
    print("\n" + "-"*100)
    print("22. ROUND / REDONDEO")
    print("-" * 100)
    round_result = round(prediction_value)
    print(f"   Formula: round(x)")
    print(f"   Result / Resultado: round({prediction_value:.6f}) = {round_result}")
    
    print("\n" + "-"*100)
    print("23. CUBE ROOT / RAÍZ CÚBICA")
    print("-" * 100)
    cbrt_result = calc.exponent(abs(prediction_value), 1/3)
    print(f"   Formula: ∛x")
    print(f"   Result / Resultado: ∛{prediction_value:.6f} = {cbrt_result:.6f}")
    
    print("\n" + "-"*100)
    print("24. POWER OF 1.5 / POTENCIA DE 1.5")
    print("-" * 100)
    pow_result = calc.exponent(abs(prediction_value), 1.5)
    print(f"   Formula: x^1.5")
    print(f"   Result / Resultado: ({prediction_value:.6f})^1.5 = {pow_result:.6f}")
    
    print("\n" + "-"*100)
    print("25. PERCENTAGE INCREASE FROM 100 / INCREMENTO PORCENTUAL DESDE 100")
    print("-" * 100)
    pct_inc_result = calc.percentage_increase(100, prediction_value)
    print(f"   Formula: % increase from 100")
    print(f"   Result / Resultado: {pct_inc_result:.6f}%")
    
    print("\n" + "-"*100)
    print("26. GCD WITH 100 / MCD CON 100")
    print("-" * 100)
    gcd_result = calc.gcd(abs(prediction_value), 100)
    print(f"   Formula: gcd(x, 100)")
    print(f"   Result / Resultado: gcd({abs(prediction_value):.0f}, 100) = {gcd_result:.0f}")
    
    print("\n" + "-"*100)
    print("27. LCM WITH 10 / MCM CON 10")
    print("-" * 100)
    lcm_result = calc.lcm(abs(prediction_value), 10)
    print(f"   Formula: lcm(x, 10)")
    print(f"   Result / Resultado: lcm({abs(prediction_value):.0f}, 10) = {lcm_result:.0f}")
    
    print("\n" + "-"*100)
    print("28. EXPONENTIAL GROWTH (5% for 1 year) / CRECIMIENTO EXPONENCIAL (5% por 1 año)")
    print("-" * 100)
    exp_growth_result = calc.exponential_growth(prediction_value, 0.05, 1)
    print(f"   Formula: x(1 + 0.05)^1")
    print(f"   Result / Resultado: {exp_growth_result:.6f}")
    
    print("\n" + "-"*100)
    print("29. PYTHAGOREAN WITH 3 / PITÁGORAS CON 3")
    print("-" * 100)
    pythag_result = calc.pythagorean(abs(prediction_value), 3)
    print(f"   Formula: √(x² + 3²)")
    print(f"   Result / Resultado: {pythag_result:.6f}")
    
    print("\n" + "-"*100)
    print("30. INVERSE SINE (normalized) / SENO INVERSO (normalizado)")
    print("-" * 100)
    asin_input = (prediction_value % 2) / 2
    if abs(asin_input) <= 1:
        asin_result = calc.arcsine(asin_input)
        print(f"   Formula: arcsin(x)")
        print(f"   Result / Resultado: arcsin({asin_input:.6f}) = {asin_result:.6f}°")
    else:
        print(f"   Value out of range / Valor fuera de rango")
    
    print("\n" + "-"*100)
    print("31. INVERSE COSINE (normalized) / COSENO INVERSO (normalizado)")
    print("-" * 100)
    acos_input = (prediction_value % 2) / 2
    if abs(acos_input) <= 1:
        acos_result = calc.arccosine(acos_input)
        print(f"   Formula: arccos(x)")
        print(f"   Result / Resultado: arccos({acos_input:.6f}) = {acos_result:.6f}°")
    else:
        print(f"   Value out of range / Valor fuera de rango")
    
    print("\n" + "-"*100)
    print("32. INVERSE TANGENT / TANGENTE INVERSA")
    print("-" * 100)
    atan_result = calc.arctangent(prediction_value / 100)
    print(f"   Formula: arctan(x)")
    print(f"   Result / Resultado: arctan({prediction_value/100:.6f}) = {atan_result:.6f}°")
    
    print("\n" + "-"*100)
    print("33. ANTILOG BASE-10 (scaled) / ANTILOGARITMO BASE-10 (escalado)")
    print("-" * 100)
    antilog_input = prediction_value / 100
    antilog_result = calc.antilog(antilog_input, 10)
    print(f"   Formula: 10^x")
    print(f"   Result / Resultado: 10^{antilog_input:.6f} = {antilog_result:.6f}")
    
    print("\n" + "-"*100)
    print("34. FRACTION REPRESENTATION (as /100) / REPRESENTACIÓN FRACCIONARIA (como /100)")
    print("-" * 100)
    frac_num = int(abs(prediction_value))
    frac_den = 100
    gcd_frac = calc.gcd(frac_num, frac_den)
    simplified_num = frac_num // int(gcd_frac)
    simplified_den = frac_den // int(gcd_frac)
    print(f"   Formula: Simplify x/100 / Simplificar x/100")
    print(f"   Result / Resultado: {frac_num}/{frac_den} = {simplified_num}/{simplified_den}")
    
    print("\n" + "-"*100)
    print("35. PERCENTAGE OF NEXT HUNDRED / PORCENTAJE AL PRÓXIMO CENTENAR")
    print("-" * 100)
    next_hundred = math.ceil(prediction_value / 100) * 100
    pct_to_hundred = ((next_hundred - prediction_value) / next_hundred) * 100 if next_hundred != 0 else 0
    print(f"   Formula: Distance to next 100 / Distancia al próximo 100")
    print(f"   Result / Resultado: {pct_to_hundred:.6f}% to {next_hundred}")

print("\n\n" + "="*100)
print("ALL 35 CALCULATORS APPLIED TO ALL 4 MODELS")
print("TODAS LAS 35 CALCULADORAS APLICADAS A LOS 4 MODELOS")
print("="*100 + "\n")
