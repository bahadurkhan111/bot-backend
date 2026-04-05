# -*- coding: utf-8 -*-
"""
SECTION 3: FEATURE ENGINEERING CLASS
Applies 35 calculators to create enhanced features
"""

class FeatureEngineering:
    """Feature engineering class that applies mathematical calculators"""
    
    def __init__(self, dataframe):
        """Initialize with pandas DataFrame"""
        self.df = dataframe.copy()
        self.calc = MathCalculators()
    
    def apply_all_calculators(self):
        """Apply all mathematical calculators as features to dataset"""
        try:
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
            
            if len(numeric_cols) < 2:
                return self.df
            
            # Statistical features
            print("Adding statistical features...")
            self.df['row_variance'] = self.df[numeric_cols].apply(
                lambda row: self.calc.calculate_variance(row.values), axis=1
            )
            self.df['row_std'] = self.df[numeric_cols].apply(
                lambda row: self.calc.standard_deviation(row.values), axis=1
            )
            self.df['row_mean'] = self.df[numeric_cols].apply(
                lambda row: self.calc.mean(row.values), axis=1
            )
            
            # Logarithmic features
            print("Adding logarithmic features...")
            for col in numeric_cols[:3]:
                self.df[f'{col}_log'] = self.df[col].apply(
                    lambda x: self.calc.natural_log(abs(x) + 1)
                )
                self.df[f'{col}_log10'] = self.df[col].apply(
                    lambda x: self.calc.logarithm(abs(x) + 1, 10)
                )
            
            # Square root features
            print("Adding square root features...")
            for col in numeric_cols[:3]:
                self.df[f'{col}_sqrt'] = self.df[col].apply(
                    lambda x: self.calc.square_root(abs(x))
                )
            
            # Exponential features
            print("Adding exponential features...")
            for col in numeric_cols[:2]:
                self.df[f'{col}_exp'] = self.df[col].apply(
                    lambda x: self.calc.exponent(abs(x) + 1, 0.5)
                )
            
            # Trigonometric features
            print("Adding trigonometric features...")
            for col in numeric_cols[:2]:
                normalized = (self.df[col] - self.df[col].min()) / (self.df[col].max() - self.df[col].min() + 1e-10)
                angle = normalized * 360
                self.df[f'{col}_sin'] = angle.apply(lambda x: self.calc.sine(x))
                self.df[f'{col}_cos'] = angle.apply(lambda x: self.calc.cosine(x))
            
            # Pairwise features
            if len(numeric_cols) >= 2:
                print("Adding pairwise features...")
                col1, col2 = numeric_cols[0], numeric_cols[1]
                
                self.df[f'{col1}_{col2}_pct_change'] = self.df.apply(
                    lambda row: self.calc.percentage_change(
                        row[col1] if row[col1] != 0 else 0.001, 
                        row[col2]
                    ), axis=1
                )
                
                self.df[f'{col1}_{col2}_ratio'] = self.df.apply(
                    lambda row: row[col1] / (row[col2] + 1e-10), axis=1
                )
                
                self.df[f'{col1}_{col2}_gcd'] = self.df.apply(
                    lambda row: self.calc.gcd(abs(row[col1]), abs(row[col2])), axis=1
                )
                
                self.df[f'{col1}_{col2}_lcm'] = self.df.apply(
                    lambda row: self.calc.lcm(abs(row[col1]), abs(row[col2])), axis=1
                )
                
                self.df[f'{col1}_{col2}_pythag'] = self.df.apply(
                    lambda row: self.calc.pythagorean(abs(row[col1]), abs(row[col2])), axis=1
                )
            
            # Polynomial features
            print("Adding polynomial features...")
            for col in numeric_cols[:2]:
                self.df[f'{col}_squared'] = self.df[col] ** 2
                self.df[f'{col}_cubed'] = self.df[col] ** 3
            
            # Clean up inf and nan values
            self.df.replace([np.inf, -np.inf], 0, inplace=True)
            self.df.fillna(0, inplace=True)
            
            print(f"Feature engineering complete! Added {len(self.df.columns) - len(numeric_cols)} new features")
            return self.df
            
        except Exception as e:
            print(f"Error in feature engineering: {e}")
            return self.df
    
    def get_feature_names(self):
        """Get list of all feature names"""
        return self.df.columns.tolist()
    
    def get_numeric_features(self):
        """Get list of numeric feature names"""
        return self.df.select_dtypes(include=[np.number]).columns.tolist()

print("✓ FeatureEngineering class defined")
