from traffic_tools import utils
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def test1():
    assert utils.encode_weekend(5) == True
    assert utils.encode_weekend(6) == True
    assert utils.encode_weekend(7) == False
    
def test2():
    assert utils.encode_rain_level(0.4) == 'No rain'
    assert utils.encode_rain_level(1) == 'Weak rain'
    assert utils.encode_rain_level(4) == 'Moderate Rain'
    assert utils.encode_rain_level(7) == 'Heavy Rain'
    assert utils.encode_rain_level(11) == 'Extreme Rain'

def test3():
    assert utils.encode_snow_level(0) == 'No snow'
    assert utils.encode_snow_level(0.24) == 'Small snow'
    assert utils.encode_snow_level(5) == 'Big snow'

def test4():
    assert utils.encode_holiday('None') == False
    assert utils.encode_holiday('None12') == True
