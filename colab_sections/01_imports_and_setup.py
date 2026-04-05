# -*- coding: utf-8 -*-
"""
SECTION 1: IMPORTS AND SETUP
Imports and basic configuration
"""

import pandas as pd
import math
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from sklearn.metrics import r2_score
import xgboost as xgb
from sklearn import linear_model
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import warnings
import random
import secrets
from fractions import Fraction
from typing import Union, Tuple, Optional, List
warnings.filterwarnings("ignore")

print("✓ All libraries imported successfully")
