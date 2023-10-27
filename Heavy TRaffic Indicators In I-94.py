#!/usr/bin/env python
# coding: utf-8

# ## Heavy Traffic Indicators on I-94
# 

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


i_94 = pd.read_csv("Metro_Interstate_Traffic_Volume.csv")


# In[3]:


i_94.head().sort_values("date_time", ascending = True)


# In[4]:


i_94.info()


# In[5]:


i_94["traffic_volume"].value_counts()


# ## Analyze traffic volume 

# In[6]:


i_94["traffic_volume"].plot.hist()


# In[7]:


i_94["traffic_volume"].describe()


# Between 2012-10-02 09:00:00 and 2018-09-30 23:00:00, the hourly traffic volume varied from 0 to 7,280 cars, with an average of 3,260 cars.
# 
# About 25% of the time, there were only 1,193 cars or fewer passing the station each hour — this probably occurs during the night, or when a road is under construction. However, about 25% of the time, the traffic volume was four times as much (4,933 cars or more).
# 
# This observation gives our analysis an interesting direction: comparing daytime data with nighttime data.

# ## Traffic Volume: Day vs. Night

# We'll start by dividing the dataset into two parts:
# 
# Daytime data: hours from 7 AM to 7 PM (12 hours)
# Nighttime data: hours from 7 PM to 7 AM (12 hours)
# While this is not a perfect criterion for distinguishing between nighttime and daytime, it's a good starting point.

# In[8]:


i_94["date_time"] = pd.to_datetime(i_94["date_time"])
day = i_94.copy()[(i_94["date_time"].dt.hour >= 7) & (i_94["date_time"].dt.hour < 19)]
night = i_94.copy()[(i_94["date_time"].dt.hour >= 19) | (i_94["date_time"].dt.hour < 7)]


# In[9]:


night


# ## Traffic Volume: Day vs. Night (II)

# In[10]:


plt.figure(figsize=(11,3.5))

plt.subplot(1, 2, 1)
plt.hist(day['traffic_volume'])
plt.title('Traffic Volume: Day')
plt.xlim(-100,7500)
plt.ylim(0,8000)
plt.ylabel('Frequency')
plt.xlabel('Traffic Volume')

plt.subplot(1,2,2)
plt.hist(night['traffic_volume'])
plt.title('Traffic Volume: Day')
plt.xlim(-100,6500)
plt.ylim(0,7500)
plt.ylabel('Frequency')
plt.xlabel('Traffic Volume')

plt.show()


# ## Statics

# In[11]:


day['traffic_volume'].describe()


# In[12]:


night['traffic_volume'].describe()


# The histogram that shows the distribution of traffic volume during the day is left skewed. This means that most of the traffic volume values are high — there are 4,252 or more cars passing the station each hour 75% of the time (because 25% of values are less than 4,252).
# 
# The histogram displaying the nighttime data is right skewed. This means that most of the traffic volume values are low — 75% of the time, the number of cars that passed the station each hour was less than 2,819.
# 
# Although there are still measurements of over 5,000 cars per hour, the traffic at night is generally light. Our goal is to find indicators of heavy traffic, so we'll only focus on the daytime data moving forward.

# ## Time Indicators

# In[13]:


day['month'] = day['date_time'].dt.month
by_month = day.groupby('month').mean()
by_month["traffic_volume"].plot.line()


# In[16]:


by_month


# The traffic looks less heavy during cold months (November–February) and more intense during warm months (March–October), with one interesting exception: July. Is there anything special about July? Is traffic significantly less heavy in July each year?
# 
# To answer the last question, let's see how the 

# In[14]:


day['year'] = day['date_time'].dt.year
by_year = day.groupby('year').mean()
by_year["traffic_volume"].plot.line()


# In[44]:


plt.figure(figsize=(11,18))
number = [2,3,4,5,6]
years = [2012,2013,2014,2015,2016,2017,2018]

for i,year in zip(number,years):
    plt.subplot(3,2,i)
    day_year = day[day['year'] == year].groupby('month').mean()
    day_year['traffic_volume'].plot.line()
    plt.title("Year" + str(year))
    plt.xticks([3,6,9,12])
    
    



# As we can see, every year in June to July, volume of traffic is decress, it can cause of ice melt, and it like the seasonal

# ## Time indicators (II)
# 

# In[48]:


day['dayofweek'] = day['date_time'].dt.dayofweek
by_dayofweek = day.groupby('dayofweek').mean()
by_dayofweek['traffic_volume'].plot.line()


# Traffic volume is significantly heavier on business days (Monday – Friday). Except for Monday, we only see values over 5,000 during business days. Traffic is lighter on weekends, with values below 4,000 cars.

# ## Time indicator

# In[52]:


day['hour'] = day['date_time'].dt.hour
bussiness_days = day.copy()[day['dayofweek'] <= 4]
weekend = day.copy()[day['dayofweek'] >= 5 ]
by_hour_business = bussiness_days.groupby('hour').mean()
by_hour_weekend = weekend.groupby('hour').mean()


# In[55]:


by_hour_business["traffic_volume"].plot.line()
by_hour_weekend["traffic_volume"].plot.line()


# Conclusion: The traffic is usually heavier during warm months (March–October) compared to cold months (November–February).
# The traffic is usually heavier on business days compared to weekends.
# On business days, the rush hours are around 7 and 16.

# In[59]:


day.corr()["traffic_volume"]


# In[62]:


day.plot.scatter('traffic_volume', 'temp')
plt.ylim([200,350])


# In[67]:


weather = day.groupby("weather_main").mean()
weather["traffic_volume"].plot.barh()


# In[68]:


day


# In[70]:


weather = day.groupby("weather_description").mean()
weather["traffic_volume"].plot.barh(figsize = (5,10))


# 
# It looks like there are three weather types where traffic volume exceeds 5,000:
# 
# Shower snow
# Light rain and snow
# Proximity thunderstorm with drizzle
# It's not clear why these weather types have the highest average traffic values — this is bad weather, but not that bad. Perhaps more people take their cars out of the garage when the weather is bad instead of riding a bike or walking.

# Conclusion
# In this project, we tried to find a few indicators of heavy traffic on the I-94 Interstate highway. We managed to find two types of indicators:
# 
# Time indicators
# The traffic is usually heavier during warm months (March–October) compared to cold months (November–February).
# The traffic is usually heavier on business days compared to the weekends.
# On business days, the rush hours are around 7 and 16.
# Weather indicators
# Shower snow
# Light rain and snow
# Proximity thunderstorm with drizzle

# In[ ]:




