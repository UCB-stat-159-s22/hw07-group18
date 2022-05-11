import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def encode_weekend(x):
    if x == 5 or x == 6:
        return True
    else:
        return False

def encode_rain_level(x):
    if x < 0.5:
        return 'No rain'
    elif x < 2:
        return 'Weak rain'
    elif x < 6:
        return 'Moderate Rain'
    elif x < 10:
        return 'Heavy Rain'
    else:
        return 'Extreme Rain'

def encode_snow_level(x):
    if x == 0:
        return 'No snow'
    elif x < 0.25:
        return 'Small snow'
    else:
        return 'Big snow'

def encode_holiday(x):
    if x == 'None':
        return False
    else:
        return True