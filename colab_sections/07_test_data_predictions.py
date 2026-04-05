# -*- coding: utf-8 -*-
"""
SECTION 7: TEST DATA AND MODEL PREDICTIONS
Create test data and get predictions from all 4 models
"""

# Create test data
input_var = {}
input_var['Ordinal'] = 6.5
input_var['Reduction'] = -115
input_var['Reverse'] = -105
input_var['Reverse Reduction'] = -218
input_var['Latin'] = 180
input_var['Reverse Sumerian'] = 116
input_var['Satanic'] = 92
input_var['Reverse Satanic'] = 1801
input_var['BibleStudy'] = .531
input_var['Trigonal'] = .612
input_var['Fibonacci'] = 365
input_var['Reverse Primes'] = .605
input_var['Reverse Trigonal'] = -142
input_var['Chaldean'] = 120

TestData = pd.DataFrame({'x': input_var}).transpose()
print("Test Data:")
print(TestData)

# Get predictions from all 4 models
print("\n" + "="*80)
print("MODEL PREDICTIONS")
print("="*80)

RandomForestModel = modelReload.predict(TestData)[0]
print(f"Random Forest Prediction: {RandomForestModel:.6f}")

XGBModelResult = XGBModelReload.predict(TestData)[0]
print(f"XGB Prediction: {XGBModelResult:.6f}")

LinearRegressionModel = LinearRegressionModelReload.predict(TestData)[0]
print(f"Linear Regression Prediction: {LinearRegressionModel:.6f}")

Lasso_model = Lasso_modelReload.predict(TestData)[0]
print(f"Lasso Prediction: {Lasso_model:.6f}")

# Calculate logarithms safely (handle negative/zero values)
print("\n" + "="*80)
print("LOGARITHMIC TRANSFORMATIONS")
print("="*80)

# Random Forest
print(f"\nRandom Forest ({RandomForestModel:.6f}):")
print(f"  Log2:  {math.log2(abs(RandomForestModel) + 1e-10):.6f}")
print(f"  Ln:    {math.log(abs(RandomForestModel) + 1e-10):.6f}")
print(f"  Log10: {math.log10(abs(RandomForestModel) + 1e-10):.6f}")

# XGB
print(f"\nXGB ({XGBModelResult:.6f}):")
print(f"  Log2:  {math.log2(abs(XGBModelResult) + 1e-10):.6f}")
print(f"  Ln:    {math.log(abs(XGBModelResult) + 1e-10):.6f}")
print(f"  Log10: {math.log10(abs(XGBModelResult) + 1e-10):.6f}")

# Linear Regression
print(f"\nLinear Regression ({LinearRegressionModel:.6f}):")
print(f"  Log2:  {math.log2(abs(LinearRegressionModel) + 1e-10):.6f}")
print(f"  Ln:    {math.log(abs(LinearRegressionModel) + 1e-10):.6f}")
print(f"  Log10: {math.log10(abs(LinearRegressionModel) + 1e-10):.6f}")

# Lasso
print(f"\nLasso ({Lasso_model:.6f}):")
print(f"  Log2:  {math.log2(abs(Lasso_model) + 1e-10):.6f}")
print(f"  Ln:    {math.log(abs(Lasso_model) + 1e-10):.6f}")
print(f"  Log10: {math.log10(abs(Lasso_model) + 1e-10):.6f}")

print("\n✓ All predictions generated successfully")
