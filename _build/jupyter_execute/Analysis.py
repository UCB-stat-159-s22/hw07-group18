#!/usr/bin/env python
# coding: utf-8

# # Metro Interstate Traffic Volume Analysis Notebook

# ## Data Importation

# In[1]:


# Libraries
import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
import os
from traffic_tools import utils


# In[2]:


traffic = pd.read_csv('data/Metro_Interstate_Traffic_Volume.csv')
traffic


# ## Introduction
# Before doing EDA or further data anlysis, it is important to explore and perform data cleaning to check for any irregularities in the dataset and to see if any additional columns are needed. Our original data contains 9 columns and 48,204 rows. Specifically, the explanatory variables are holiday, temperature, amount of rain per hour, amount of snow per hour, coverage of clounds, type of weather, description of weather, and date time. The last column is the response variable traffic_volume.

# In[3]:


traffic.head()


# In[4]:


traffic.shape


# In[5]:


traffic.dtypes


# ## Data Preprocessing

# Upon observing the original data frame, we think it is helpful to extract new columns froms the `date_time` variable to better aid the analysis process. Thus, the `date`, `month`, and `hour` variables are created because these might be important factors that correlates to the traffic volume change.

# In[6]:


# create new variables
traffic['date_time'] = pd.to_datetime(traffic.date_time)
traffic['date'] = traffic.date_time.dt.date
traffic['hour'] = traffic.date_time.dt.hour
traffic['month'] = traffic.date_time.dt.month


# Weekday vs weekend affects traffic volume because each day of week may have different patterns. Therefore, categorical variable `weekday` is added to our dataset, another variable `is_weekend` is added with weekdays encoded as False and weekends encoded as True.

# In[7]:


traffic['weekday'] = traffic.date_time.dt.weekday

traffic['is_weekend'] = traffic['weekday'].map(utils.encode_weekend)


# We observe that there is one outlier for the `rain_1h`. We drop the irregular observation because it is clearly a mistake. For most observations, the amount of rain is 0 since there is no rain for most of the times. To better train our data, we transform the numerical variable of `rain_1h` to catagorical variables `rain_level` describing the level of rain.

# In[10]:


sns.boxplot('rain_1h', data = traffic)
plt.savefig('figures/rain_1h.png')


# In[11]:


traffic = traffic.loc[traffic.rain_1h<8000]


# In[12]:


traffic['rain_level'] = traffic['rain_1h'].map(utils.encode_rain_level)


# Similary, `snow_1h` is divided into 3 categories as the new column `snow_level`, with no snow, small snow, and big snow. 

# In[13]:


traffic['snow_level'] = traffic['snow_1h'].map(utils.encode_snow_level)


# The `temperature` variable in the original data uses the unit of kelvin. To better interpret the variable, we transform the unit to celsius. There are also outliers for the temperature which is also clearly mistakes, so we remove them.

# In[14]:


traffic['temp'] = traffic['temp'] - 273.15


# In[15]:


sns.boxplot('temp', data = traffic)
plt.savefig('figures/temp.png')


# In[16]:


traffic = traffic.loc[traffic.temp >= -50]


# For the `holiday` variable, there are many of them, but only holiday vs non-holiday should be useful. Therefore, this column is transformed into True or False.

# In[17]:


traffic['holiday'] = traffic['holiday'].map(utils.encode_holiday)


# ## Finalized Dataset

# Upon finishing the data preprocessing and cleaning, the final dataset has 48193 rows and 16 columns.

# In[18]:


traffic.head()


# In[19]:


traffic.shape


# ## Explanatory Data Analysis

# Before building any models or perforing any analysis, we need to perform data visualizations to see how the variables relate to each other.

# In[20]:


plt.hist(traffic.traffic_volume, bins = 30)
plt.title('Distribution of traffic volume')
plt.ylabel('count')
plt.xlabel('traffic volume');
plt.savefig('figures/traffic_volume_hist.png')


# Significant less traffic volume over weekends (5:Saturday, 6:Sunday)

# In[21]:


sns.boxplot(y='traffic_volume', x='weekday', data = traffic)
plt.savefig('figures/weekday_box.png')


# In[22]:


sns.boxplot(y='traffic_volume', x='is_weekend', data = traffic)
plt.savefig('figures/is_weekend_box.png')


# Not much difference for traffic volume across different months

# In[26]:


sns.boxplot(y='traffic_volume', x='month', data = traffic)
plt.savefig('figures/month_box.png')


# In[24]:


sns.boxplot(y='traffic_volume', x='snow_level', data = traffic)
plt.savefig('figures/snow_level_box.png')


# In[25]:


sns.boxplot(y='traffic_volume', x='rain_level', data = traffic)
plt.savefig('figures/rain_level_box.png')


# Then, we also examines the correlation between numerical variables to traffic volume through the correlation matrix. Collinearity is also assesed with this heat map. There is a slight positive correlation between `temp` and `traffic_volume`. There is almost no correlation between `clouds_all` and `traffic_volume`. These accord with what we see in the previous graphs. There is also a slight negative correlation between `temp` and `clouds_all`. This makes sense because the weather tend to be cooler when there is a high coverage of clouds. Both `snow_1h` and `rain_1h` have really weak correlation on traffic_volume. 

# In[30]:


df = pd.DataFrame(traffic,columns=['traffic_volume','clouds_all','temp', 'snow_1h', 'rain_1h'])

corrMatrix = df.corr()
sns.heatmap(corrMatrix, annot=True)
plt.show()
plt.savefig('figures/corr_matrix')


# ## Research Question
# 
# Does different environmental variables (such as snow, rain, cloud, temperature, holiday, and weekend) impacts the level of traffic overall?

# ## Analysis and Interpretation of the Data
# 

# In[25]:


traffic


# ## Farther EDA

# In[26]:


ols_traffic_model = traffic.copy()
ols_traffic_model['holiday'] = [0 if i == False else 1 for i in traffic['holiday']]
ols_traffic_model.drop(['weather_main', 'weather_description', 'date_time', 'date', 'weekday', 'rain_level', 'snow_level', 'month', 'hour'], axis=1, inplace=True)
ols_traffic_model['is_weekend'] = [0 if i == False else 1 for i in traffic['is_weekend']]
ols_traffic_model.columns = ['Holiday', 'Temperature (C)', 'Rain Level', 'Snow Level', 'Cloud Level', 'Traffic Volume', 'Weekend']

ols_traffic_model


# ## Difference-in-Difference Using Fit_OLS_Model

# In[27]:


def fit_OLS_model(df, target_variable, explanatory_variables, intercept = False):
    """
    Fits an OLS model from data.
    
    Inputs:
        df: pandas DataFrame
        target_variable: string, name of the target variable
        explanatory_variables: list of strings, names of the explanatory variables
        intercept: bool, if True add intercept term
    Outputs:
        fitted_model: model containing OLS regression results
    """
    
    target = df[target_variable]
    inputs = df[explanatory_variables]
    if intercept:
        inputs = sm.add_constant(inputs)
    
    fitted_model = sm.OLS(target, inputs).fit()
    return(fitted_model)


# In[28]:


linear_model = fit_OLS_model(ols_traffic_model, 'Traffic Volume', ['Holiday', 'Temperature (C)', 'Rain Level', 'Snow Level', 'Cloud Level', 'Weekend'], intercept=True)
print(linear_model.summary())


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
