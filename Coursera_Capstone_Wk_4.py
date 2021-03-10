#!/usr/bin/env python
# coding: utf-8

# A description of the problem and a discussion of the background. (15 marks)
# 
# The problem to be addressed is to compare two cities (Cleveland, Ohio and Columbus, Ohio) to see which is more preferable for opening a restaurant.  Not only will the restuaruant location be considered, but other venues around the restaurant will also be utilized for comparison. An area with more restaurants of one type may present too much competition, which can help to drive the business model on which type of restaurant to create.  Also, having other venues around the restaurant will indicate a higher probability of foot traffic and more potential business. 

# A description of the data and how it will be used to solve the problem. (15 marks)
# 
# First the state of Ohio will be broken down by Area code. After organizing the chart to have descending population, it was found that the two largest cities in Ohio (by population) are Cleveland and Columbus. 
# 
# The four main variables that were analyzed were that of the restaurants and total venues of each city (see below)
# 1. cle_dataframe_restaurant
# 2. cle_datatrame_venues
# 3. cbus_dataframe_restaurant
# 4. cbus_dataframe_venues
# 
# Each city was found using the geocoder where the latitude and longitude numbers were utilized. 
# 
# The API from foursquare was utilized having to have found the Client ID (), Client Secret, and Acess Token ().
# CLIENT_ID = 'ZRS2NV2A04VQZNFID0INKRS00YCZCTYVMVDFIR1L4FX5ZVIG' 
# CLIENT_SECRET = 'PRK2N423NAEOOKKKTL5EL4LLRJ2A4SJJYFJU2V55QT5WRMOQ' 
# ACCESS_TOKEN = 'K1HE3T2FSR4DHLLJYC1MNQMO2WE4JROAKLUSVO0MEZ0GJ5LP'
# 
# Requests were then made through the Foursquare server to look for restaurants and venues within each city center.  The results of the analysis were cleaned and process in the dataframe.
# 
# Each request was visualized using the folios chart with the red dot indicating the city center and the blue dots indicating the four square results.  
# 
# Lastly, an analysis of the two cities was done using the mean of the distance between venues and restuarants as well as a qualitative analysis to see the diversity of restaurants/venues within the city. 

# In[234]:


import pandas as pd
import numpy as np
import geocoder
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import folium

import requests # library to handle requests
import random # library for random number generation
get_ipython().system('pip install geopy')
from geopy.geocoders import Nominatim # module to convert an address into latitude and longitude values

# libraries for displaying images
from IPython.display import Image 
from IPython.core.display import HTML 
    
# tranforming json file into a pandas dataframe library
from pandas.io.json import json_normalize

get_ipython().system(' pip install folium==0.5.0')
import folium # plotting library

print('Folium installed')
print('Libraries imported.')


# Ohio cities information

# In[235]:


# 2. Scrape the Wikipedia page
url = 'https://en.wikipedia.org/wiki/List_of_Ohio_area_codes'
df = pd.read_html(url)
print(len(df))
print(type(df))


# In[236]:


df = df[0]
df


# In[339]:


df_ohio = df.drop(['Created'], axis = 1)
df_ohio


# In[300]:


import pandas as pd


# In[311]:


url_ohio_pop = 'https://en.wikipedia.org/wiki/List_of_cities_in_Ohio'
df_pop = pd.read_html(url_ohio_pop)
print(len(df_pop))
print(type(df_pop))


# In[314]:


df_pop1 = df_pop[0]
df_pop1


# In[338]:


df_pop2 = df_pop1.sort_values(by = ['Population'], ascending = False)
df_pop2


# In[321]:


print(df_pop2.loc[[58]])


# Columbus, Ohio Analysis

# In[238]:


address = 'Columbus, Ohio'

geolocator = Nominatim(user_agent="foursquare_agent")
location = geolocator.geocode(address)
latitude = location.latitude
longitude = location.longitude
print('The coordinates of Columbus, Ohio are {}, {}.'.format(latitude, longitude))


# In[239]:


CLIENT_ID = 'ZRS2NV2A04VQZNFID0INKRS00YCZCTYVMVDFIR1L4FX5ZVIG' # your Foursquare ID
CLIENT_SECRET = 'PRK2N423NAEOOKKKTL5EL4LLRJ2A4SJJYFJU2V55QT5WRMOQ' # your Foursquare Secret
ACCESS_TOKEN = 'K1HE3T2FSR4DHLLJYC1MNQMO2WE4JROAKLUSVO0MEZ0GJ5LP' # your FourSquare Access Token
VERSION = '20180604'
LIMIT = 30
print('Your credentails:')
print('CLIENT_ID: ' + CLIENT_ID)
print('CLIENT_SECRET:' + CLIENT_SECRET)


# In[240]:


search_query = 'Restaurant'
radius = 500
print(search_query + ' .... OK!')


# In[241]:


url = 'https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&ll={},{}&oauth_token={}&v={}&query={}&radius={}&limit={}'.format(CLIENT_ID, CLIENT_SECRET, latitude, longitude,ACCESS_TOKEN, VERSION, search_query, radius, LIMIT)
url


# In[242]:


results = requests.get(url).json()
results


# In[243]:


# assign relevant part of JSON to venues
venues = results['response']['venues']
dataframe = pd.json_normalize(venues)
dataframe.head()


# In[244]:


# keep only columns that include venue name, and anything that is associated with location
filtered_columns = ['name', 'categories'] + [col for col in dataframe.columns if col.startswith('location.')] + ['id']
dataframe_filtered = dataframe.loc[:, filtered_columns]

# function that extracts the category of the venue
def get_category_type(row):
    try:
        categories_list = row['categories']
    except:
        categories_list = row['venue.categories']
        
    if len(categories_list) == 0:
        return None
    else:
        return categories_list[0]['name']

# filter the category for each row
dataframe_filtered['categories'] = dataframe_filtered.apply(get_category_type, axis=1)

# clean column names by keeping only last term
dataframe_filtered.columns = [column.split('.')[-1] for column in dataframe_filtered.columns]

dataframe_filtered
cbus_dataframe_restaurant = dataframe_filtered
cbus_dataframe_restaurant


# In[245]:


venues_map = folium.Map(location=[latitude, longitude], zoom_start=15) # generate map centred around the Conrad Hotel

# add a red circle marker to represent the Conrad Hotel
folium.CircleMarker(
    [latitude, longitude],
    radius=10,
    color='red',
    popup='Conrad Hotel',
    fill = True,
    fill_color = 'red',
    fill_opacity = 0.6
).add_to(venues_map)

# add the restaurants as blue circle markers
for lat, lng, label in zip(cbus_dataframe_restaurant.lat, cbus_dataframe_restaurant.lng, cbus_dataframe_restaurant.categories):
    folium.CircleMarker(
        [lat, lng],
        radius=5,
        color='blue',
        popup=label,
        fill = True,
        fill_color='blue',
        fill_opacity=0.6
    ).add_to(venues_map)

# display map
venues_map


# Explore Columbus businesses

# In[246]:


url = 'https://api.foursquare.com/v2/venues/explore?client_id={}&client_secret={}&ll={},{}&v={}&radius={}&limit={}'.format(CLIENT_ID, CLIENT_SECRET, latitude, longitude, VERSION, radius, LIMIT)
url


# In[247]:


import requests


# In[248]:


results = requests.get(url).json()
'There are {} around Columbus, Ohio.'.format(len(results['response']['groups'][0]['items']))


# In[249]:


items = results['response']['groups'][0]['items']
items[0]


# In[250]:


dataframe = json_normalize(items) # flatten JSON

# filter columns
filtered_columns = ['venue.name', 'venue.categories'] + [col for col in dataframe.columns if col.startswith('venue.location.')] + ['venue.id']
dataframe_filtered = dataframe.loc[:, filtered_columns]

# filter the category for each row
dataframe_filtered['venue.categories'] = dataframe_filtered.apply(get_category_type, axis=1)

# clean columns
dataframe_filtered.columns = [col.split('.')[-1] for col in dataframe_filtered.columns]

cbus_dataframe_venues = dataframe_filtered
cbus_dataframe_venues.head(10)


# In[251]:


venues_map = folium.Map(location=[latitude, longitude], zoom_start=15) # generate map centred around Ecco


# add Ecco as a red circle mark
folium.CircleMarker(
    [latitude, longitude],
    radius=10,
    popup='Ecco',
    fill=True,
    color='red',
    fill_color='red',
    fill_opacity=0.6
    ).add_to(venues_map)
# add popular spots to the map as blue circle markers
for lat, lng, label in zip(cbus_dataframe_venues.lat, cbus_dataframe_venues.lng, cbus_dataframe_venues.categories):
    folium.CircleMarker(
        [lat, lng],
        radius=5,
        popup=label,
        fill=True,
        color='blue',
        fill_color='blue',
        fill_opacity=0.6
        ).add_to(venues_map)

# display map
venues_map


# Trending Venues Columbus, Ohio

# In[252]:


# define URL
url = 'https://api.foursquare.com/v2/venues/trending?client_id={}&client_secret={}&ll={},{}&v={}'.format(CLIENT_ID, CLIENT_SECRET, latitude, longitude, VERSION)

# send GET request and get trending venues
results = requests.get(url).json()
results


# In[253]:


if len(results['response']['venues']) == 0:
    trending_venues_df = 'No trending venues are available at the moment!'
    
else:
    trending_venues = results['response']['venues']
    trending_venues_df = json_normalize(trending_venues)

    # filter columns
    columns_filtered = ['name', 'categories'] + ['location.distance', 'location.city', 'location.postalCode', 'location.state', 'location.country', 'location.lat', 'location.lng']
    trending_venues_df = trending_venues_df.loc[:, columns_filtered]

    # filter the category for each row
    trending_venues_df['categories'] = trending_venues_df.apply(get_category_type, axis=1)


# In[254]:


# display trending venues
trending_venues_df


# CLEVELAND,  OHIO Analysis

# In[255]:


address = 'Cleveland, Ohio'

geolocator = Nominatim(user_agent="foursquare_agent")
location = geolocator.geocode(address1)
latitude = location.latitude
longitude = location.longitude
print('The coordinates of Cleveland, Ohio are {}, {}.'.format(latitude1, longitude1))


# In[256]:


search_query = 'Restaurant'
radius = 500
print(search_query + ' .... OK!')


# In[257]:


url = 'https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&ll={},{}&oauth_token={}&v={}&query={}&radius={}&limit={}'.format(CLIENT_ID, CLIENT_SECRET, latitude, longitude,ACCESS_TOKEN, VERSION, search_query, radius, LIMIT)
url


# In[258]:


results = requests.get(url).json()
results


# In[259]:


# assign relevant part of JSON to venues
venues = results['response']['venues']
dataframecle = pd.json_normalize(venues)
dataframecle.head()


# In[260]:


# keep only columns that include venue name, and anything that is associated with location
filtered_columns = ['name', 'categories'] + [col for col in dataframecle.columns if col.startswith('location.')] + ['id']
dataframe_filtered = dataframecle.loc[:, filtered_columns]

# function that extracts the category of the venue
def get_category_type(row):
    try:
        categories_list = row['categories']
    except:
        categories_list = row['venue.categories']
        
    if len(categories_list) == 0:
        return None
    else:
        return categories_list[0]['name']

# filter the category for each row
dataframe_filtered['categories'] = dataframe_filtered.apply(get_category_type, axis=1)

# clean column names by keeping only last term
dataframe_filtered.columns = [column.split('.')[-1] for column in dataframe_filtered.columns]

cle_dataframe_restaurant = dataframe_filtered
cle_dataframe_restaurant.head()


# In[261]:


venues_map = folium.Map(location=[latitude, longitude], zoom_start=15) # generate map centred around the Cleveland, Ohio

# add a red circle marker to represent the Conrad Hotel
folium.CircleMarker(
    [latitude, longitude],
    radius=10,
    color='red',
    popup='Conrad Hotel',
    fill = True,
    fill_color = 'red',
    fill_opacity = 0.6
).add_to(venues_map)

# add the restaurants as blue circle markers
for lat, lng, label in zip(cle_dataframe_restaurant.lat, cle_dataframe_restaurant.lng, cle_dataframe_restaurant.categories):
    folium.CircleMarker(
        [lat, lng],
        radius=5,
        color='blue',
        popup=label,
        fill = True,
        fill_color='blue',
        fill_opacity=0.6
    ).add_to(venues_map)

# display map
venues_map


# In[262]:


url = 'https://api.foursquare.com/v2/venues/explore?client_id={}&client_secret={}&ll={},{}&v={}&radius={}&limit={}'.format(CLIENT_ID, CLIENT_SECRET, latitude, longitude, VERSION, radius, LIMIT)
url


# In[263]:


import requests


# In[264]:


results = requests.get(url).json()
'There are {} around Cleveland, Ohio.'.format(len(results['response']['groups'][0]['items']))


# In[265]:


items = results['response']['groups'][0]['items']
items[0]


# In[266]:


dataframe = json_normalize(items) # flatten JSON

# filter columns
filtered_columns = ['venue.name', 'venue.categories'] + [col for col in dataframe.columns if col.startswith('venue.location.')] + ['venue.id']
dataframe_filtered = dataframe.loc[:, filtered_columns]

# filter the category for each row
dataframe_filtered['venue.categories'] = dataframe_filtered.apply(get_category_type, axis=1)

# clean columns
dataframe_filtered.columns = [col.split('.')[-1] for col in dataframe_filtered.columns]

cle_dataframe_venues = dataframe_filtered
cle_dataframe_venues.head()


# In[267]:


venues_map = folium.Map(location=[latitude, longitude], zoom_start=15) # generate map centred around Ecco


# add Ecco as a red circle mark
folium.CircleMarker(
    [latitude, longitude],
    radius=10,
    popup='Ecco',
    fill=True,
    color='red',
    fill_color='red',
    fill_opacity=0.6
    ).add_to(venues_map)
# add popular spots to the map as blue circle markers
for lat, lng, label in zip(cle_dataframe_venues.lat, cle_dataframe_venues.lng, cle_dataframe_venues.categories):
    folium.CircleMarker(
        [lat, lng],
        radius=5,
        popup=label,
        fill=True,
        color='blue',
        fill_color='blue',
        fill_opacity=0.6
        ).add_to(venues_map)

# display map
venues_map


# In[268]:


# define URL
url = 'https://api.foursquare.com/v2/venues/trending?client_id={}&client_secret={}&ll={},{}&v={}'.format(CLIENT_ID, CLIENT_SECRET, latitude, longitude, VERSION)

# send GET request and get trending venues
results = requests.get(url).json()
results


# In[269]:


if len(results['response']['venues']) == 0:
    trending_venues_df = 'No trending venues are available at the moment!'
    
else:
    trending_venues = results['response']['venues']
    trending_venues_df = json_normalize(trending_venues)

    # filter columns
    columns_filtered = ['name', 'categories'] + ['location.distance', 'location.city', 'location.postalCode', 'location.state', 'location.country', 'location.lat', 'location.lng']
    trending_venues_df = trending_venues_df.loc[:, columns_filtered]

    # filter the category for each row
    trending_venues_df['categories'] = trending_venues_df.apply(get_category_type, axis=1)


# In[270]:


# display trending venues
trending_venues_df


# Compare the two cities

# In[278]:


cle_dataframe_venues['categories'] = cle_dataframe_venues['categories'].astype(str)


# In[279]:


cle_dataframe_restaurant['categories'] = cle_dataframe_restaurant['categories'].astype(str)


# In[280]:


cbus_dataframe_venues['categories'] = cbus_dataframe_venues['categories'].astype(str)


# In[281]:


cbus_dataframe_restaurant['categories'] = cbus_dataframe_restaurant['categories'].astype(str)


# In[282]:


cle_dataframe_restaurant['distance'].mean()


# In[283]:


cbus_dataframe_restaurant['distance'].mean()


# In[284]:


cle_dataframe_venues['distance'].mean()


# In[286]:


cbus_dataframe_venues['distance'].mean()


# In[287]:


countclerest = cle_dataframe_restaurant['categories'].value_counts()
print(countclerest)


# In[289]:


countcbusrest = cbus_dataframe_restaurant['categories'].value_counts()
print(countcbusrest)


# In[290]:


countcleven = cle_dataframe_venues['categories'].value_counts()
print(countcleven)


# In[291]:


countcbusven = cbus_dataframe_venues['categories'].value_counts()
print(countcbusven)


# In[ ]:




