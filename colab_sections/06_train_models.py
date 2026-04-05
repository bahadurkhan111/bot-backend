# -*- coding: utf-8 -*-
"""
SECTION 6: TRAIN ALL 4 ML MODELS
Random Forest, XGB, Linear Regression, Lasso
"""

# Random Forest Regressor
print("\n" + "="*80)
print("TRAINING RANDOM FOREST")
print("="*80)
model_regression = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10)
model_regression.fit(X, y)
y_pred = model_regression.predict(X)
predict = model_regression.predict(X)
rf_score = r2_score(y, predict)
print(f"Random Forest R² Score: {rf_score:.6f}")
joblib.dump(model_regression,'RandomForestRegressorModel.pkl')
modelReload=joblib.load('RandomForestRegressorModel.pkl')

# XGB
print("\n" + "="*80)
print("TRAINING XGB")
print("="*80)
xgb_model = xgb.XGBRegressor(objective="reg:squarederror", random_state=42, n_estimators=100, max_depth=6)
xgb_model.fit(X, y)
y_pred1 = xgb_model.predict(X)
xgb_score = r2_score(y, y_pred1)
print(f"XGB R² Score: {xgb_score:.6f}")
joblib.dump(xgb_model,'XGBModel.pkl')
XGBModelReload=joblib.load('XGBModel.pkl')

# Linear Regression
print("\n" + "="*80)
print("TRAINING LINEAR REGRESSION")
print("="*80)
LinearRegression = LinearRegression()
LinearRegression.fit(X, y)
predict2 = LinearRegression.predict(X)
lr_score = r2_score(y, predict2)
print(f"Linear Regression R² Score: {lr_score:.6f}")
joblib.dump(LinearRegression,'LinearRegression.pkl')
LinearRegressionModelReload=joblib.load('LinearRegression.pkl')

# Lasso Model
print("\n" + "="*80)
print("TRAINING LASSO")
print("="*80)
Lasso_model = linear_model.Lasso(alpha=0.1, max_iter=10000)
Lasso_model.fit(X, y)
lasso_prediction = Lasso_model.predict(X)
lasso_score = r2_score(y, lasso_prediction)
print(f"Lasso R² Score: {lasso_score:.6f}")
joblib.dump(Lasso_model,'Lasso_model.pkl')
Lasso_modelReload=joblib.load('Lasso_model.pkl')

# Model Comparison
print("\n" + "="*80)
print("MODEL COMPARISON")
print("="*80)
print(f"Random Forest R² Score:     {rf_score:.6f}")
print(f"XGB R² Score:                {xgb_score:.6f}")
print(f"Linear Regression R² Score:  {lr_score:.6f}")
print(f"Lasso R² Score:              {lasso_score:.6f}")
print("="*80 + "\n")

print("\n✓ All 4 models trained successfully")
