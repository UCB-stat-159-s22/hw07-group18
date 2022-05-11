#!/usr/bin/env python
# coding: utf-8

# # Metro Interstate Traffic Volume Report

# ## Introduction

# Metro interstate traffic volume is the hourly traffic volume of metropolitan interstate. For this specific dataset, we are studying the hourly Minneapolis-St Paul, MN traffic volume for westbound I-94 from 2012-10-02 to 2018-9-30. We explore th traffic data for Minneapolis-St Paul and try to explore relationships between temperature, weather conditions, date and time information on Mineeapolis interstate traffic and predict traffic volume given these weather conditions. We therefore build a linear model that examines how the above variables are correlated to traffic volume.

# ## Data Information

# Abstract: Hourly Minneapolis-St Paul, MN traffic volume for westbound I-94. Includes weather and holiday features from 2012-2018.
# 
# 1. holiday Categorical US National holidays plus regional holiday, Minnesota State Fair
# 2. temp Numeric Average temp in kelvin
# 3. rain_1h Numeric Amount in mm of rain that occurred in the hour
# 4. snow_1h Numeric Amount in mm of snow that occurred in the hour
# 5. clouds_all Numeric Percentage of cloud cover
# 6. weather_main Categorical Short textual description of the current weather
# 7. weather_description Categorical Longer textual description of the current weather
# 8. date_time DateTime Hour of the data collected in local CST time
# 9. traffic_volume Numeric Hourly I-94 ATR 301 reported westbound traffic volume

# ## Data Preprocessing

# Before doing EDA or further data anlysis, it is important to explore and perform data cleaning to check for any irregularities in the dataset and to see if any additional columns are needed. Our original data contains 9 columns and 48,204 rows. Specifically, the explanatory variables are holiday, temperature, amount of rain per hour, amount of snow per hour, coverage of clounds, type of weather, description of weather, and date time. The last column is the response variable traffic_volume.
# 
# Upon observing the original data frame, we think it is helpful to extract new columns froms the `date_time` variable to better aid the analysis process. Thus, the `date`, `month`, and `hour` variables are created because these might be important factors that correlates to the traffic volume change.
# 
# Weekday vs weekend affects traffic volume because each day of week may have different patterns. Therefore, categorical variable `weekday` is added to our dataset, another variable `is_weekend` is added with weekdays encoded as False and weekends encoded as True.
# 
# We observe that there is one outlier for the `rain_1h` which has a value of over 8000. We drop the irregular observation because it is clearly a mistake. On the other hand, for most observations, the amount of rain is 0 since there is no rain for most of the times. To better train our data, we transform the numerical variable of `rain_1h` to catagorical variables `rain_level` describing the level of rain.
# 
# ![rain](figures/rain_1h.png)
# 
# Similary, `snow_1h` is divided into 3 categories as the new column `snow_level`, with no snow, small snow, and big snow. 
# 
# The `temperature` variable in the original data uses the unit of kelvin. To better interpret the variable, we transform the unit to celsius. There are also outliers for the temperature which is also clearly mistakes, so we remove them.
# 
# ![temp](figures/temp.png)
# 
# For the `holiday` variable, there are many of them in the original dataset, which includes christmas, new year's day, etc, but only holiday vs non-holiday should be useful. Therefore, this column is transformed into True or False.
# 

# ## Explanatory Data Analysis

# Before building any models, we need to perform data visualizations to see how the variables relate to each other.  We first visualize the distribution of the response variable traffic_volume to check for distribution. As shown in figure, the distributions are not normal, with many spikes.
# 
# ![traffic_volume](figures/traffic_volume_hist.png)
# 
# Then, we perform exploratory data analysis for the explanatory variables to visualize high-level data characteristics. We use box plots because they are useful to see the correlation between each subgroup of categorical to the traffic volume. 
# 
# We observe that there is significant less traffic volume over weekends (5 = Saturday and 6 = Sunday). 
# 
# ![weekday](figures/weekday_box.png)
# 
# Thus, we compare the difference in traffic volume for only weekday vs weekend. Weekday shows significant more traffic volume than weekend. This makes sense because people commute a lot more during weekdays to go to work.
# 
# ![is_weekend](figures/is_weekend_box.png)
# 
# There are no apparent difference in traffic volume across months.
# 
# ![month](figures/month_box.png)
# 
# Box plots for snow_level and rain_level are also examined. For snow, people's tend to travel more during big snow days, which is not very reasonable in this case. 
# 
# ![snow](figures/snow_level_box.png)
# 
# For rain levels, it is reasonable that people might choose to walk so traffic volume is not the greatest. However, as rain level starts to increase, traffic volume gradually decreases since people are not willing to travel in rainy days. 
# 
# ![rain](figures/rain_level_box.png)
# 
# Then, we also examines the correlation between numerical variables to traffic volume through the correlation matrix. Collinearity is also assesed with this heat map. There is a slight positive correlation between `temp` and `traffic_volume`. There is almost no correlation between `clouds_all` and `traffic_volume`. These accord with what we see in the previous graphs. There is also a slight negative correlation between `temp` and `clouds_all`. This makes sense because the weather tend to be cooler when there is a high coverage of clouds. Both `snow_1h` and `rain_1h` have really weak correlation on traffic_volume. 
# 
# ![heat_map](figures/corr_matrix.png)
# 
# 

# ## Research Question
# 
# Does off-days within the year, such as the weekend and holidays decrease the level of traffic?

# ### Fit OLS Model

# ![fit_OLS_model](figures/fit_OLS_model.png)

# ## Analysis and Interpretation of the Model
# 
# According to our Fit OLS Regression Model that we have built based on our variables, we tried to find a correlation between the level of Traffic and off-days in a year. 
# 
# Using OLS, we can find the equivalent value of the difference-in-difference estimate of the treatment variables (weekend and holidays). That is, we can find the correlation between our target variable (Traffic Level) and environmental variables, and calculate the difference between these means. 
# 
# The reason we use OLS is to easily include our confounders as well as calculating errors.
# 
# To do this, we can estimate the unknown parameters in $y = \beta_0 + \beta_1 T + \beta_2 I + \beta_3 X_1+ \beta_4 X_2 + \beta_5 X_3 + \beta_6 X_4$ where $X_i$ is the $i^{th}$ confounder in our dataset.
# 
# In this case, each $\beta$ represents our target variable of Level of Traffic. The $T$ and $I$ represents our the off-days during the year for regular employees and employers.  
# 
# 
# According to the summary of our model, we were able to find that there is overall negative correlation between the level of traffic and our treatment variables. For some of the unexpected discoveries we had, the most unexpected finding wasthe statistic significance on the snow level. Initially, we assumed that high level of snow would decrease the amount of traffic, but the result we discovered was very different from our expectation. The p-value for this factor came out to be 0.684, which was higher than 0.05. This also signifies that the snow does not have strong correlation on traffic level. For other coefficients on our variables, they were reasonably expected at the beginning of our hypothesis test as we expected that higher rain and snow would decrease the level of traffic. We expected a negative correlation because due to the danger of driving under restraint atmospheric conditions from snow and rain (which could hinder vision and increase chance of accident by less surface friction on the road), we expected less people to drive on those days. Similarly, we expected negative correlation between the traffic level and other variables, such as weekend and holiday, as less people would be driving to commute to work or they would more likely to stay at home. Other surprising foundings we had were correlation between cloud level/Temperature and traffic level as the coefficients were positive, but exceptionally smaller compared to other variables that had positive coefficients. This demonstrates that there are some correlation between these factors, but weaker correlation compared to holiday, rain, snow, and weekend variables. 

# ## Conclusion
# 
# Given the interpretation between overall environmental factors and the traffic level, we are confident to say there are overall positive correlation between the combined environmental factors on the level of traffic overall, which can be found from the positive constant coefficient. There were some unexpected discoveries made  on the relationship between the level of traffic and snowiness of the weather, we found strongest correlation between the holiday/weekend (treatment variable) and our Level of Traffic (target variable). Overall, the p-values for target variables were statistically significant, except the level of snow, ultimately supporting our hypothesis that both off-days throughout the year decreases the level of traffic. 
