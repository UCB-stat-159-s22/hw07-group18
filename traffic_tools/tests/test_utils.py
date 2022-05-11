from traffic_tools import utils
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def test1():
    assert encode_weekend(5) == True
    assert encode_weekend(6) == True
    assert encode_weekend(7) == False
    
def test2():
    assert encode_rain_level(0.4) == 'No rain'
    assert encode_rain_level(1) == 'Weak rain'
    assert encode_rain_level(4) == 'Moderate Rain'
    assert encode_rain_level(7) == 'Heavy Rain'
    assert encode_rain_level(11) == 'Extreme Rain'

def test3():
    assert encode_snow_level(0) == 'No snow'
    assert encode_snow_level(0.24) == 'Small snow'
    assert encode_snow_level(5) == 'Big snow'

def test4():
    assert encode_holiday('None') == False
    assert encode_holiday('None12') == True
