# -*- coding: utf-8 -*-
"""
SECTION 5: PREPARE TRAINING DATA
Split data into features (X) and target (y)
"""

# Split data for training and testing
X = df[['Ordinal','Reduction','Reverse','Reverse Reduction','Latin','Reverse Sumerian', 'Satanic', 'Reverse Satanic',
        'BibleStudy', 'Trigonal', 'Fibonacci', 'Reverse Primes', 'Reverse Trigonal', 'Chaldean']]
y = df['Sumerian']

print(f"\nTraining with {len(X.columns)} features")
print("\n✓ Data prepared for training")
