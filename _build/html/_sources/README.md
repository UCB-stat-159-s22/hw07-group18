# Reproductibility Research for Metro Interstate Traffic

[![Binder](https://mybinder.org/badge_logo.svg)]()

**Note:** This repository is public so that Binder can find it. The data is available at: https://archive.ics.uci.edu/ml/datasets/Metro+Interstate+Traffic+Volume. This repository is a class project to for reproducibility, as a homework assignment for the [Spring 2022 installment of UC Berkeley's Stat 159/259 course, _Reproducible and Collaborative Data Science_](https://ucb-stat-159-s22.github.io).

## Goals

In this project we explore th traffic data for Minneapolis-St Paul and try to explore relationships between temperature, weather conditions, date and time information on Mineeapolis interstate traffic and predict traffic volume given these weather conditions. All the data required to run the project is in the data folder. The saved plots and graphs are in the figures directory and the models are saved in the models directory. We have provided a set of tests to check basic accuracy which can be run with the makefile commands provided below

## Data Information

Abstract: Hourly Minneapolis-St Paul, MN traffic volume for westbound I-94. Includes weather and holiday features from 2012-2018.

1. holiday Categorical US National holidays plus regional holiday, Minnesota State Fair
2. temp Numeric Average temp in kelvin
3. rain_1h Numeric Amount in mm of rain that occurred in the hour
4. snow_1h Numeric Amount in mm of snow that occurred in the hour
5. clouds_all Numeric Percentage of cloud cover
6. weather_main Categorical Short textual description of the current weather
7. weather_description Categorical Longer textual description of the current weather
8. date_time DateTime Hour of the data collected in local CST time
9. traffic_volume Numeric Hourly I-94 ATR 301 reported westbound traffic volume

## Running Instructions

You can run the main notebook with the binder link given or clone the repository to run it localy. We have also provided a list of makefile instructions for easier execution

### Makefile Commands

