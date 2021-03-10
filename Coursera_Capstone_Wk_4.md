A description of the problem and a discussion of the background. (15 marks)

The problem to be addressed is to compare two cities (Cleveland, Ohio and Columbus, Ohio) to see which is more preferable for opening a restaurant.  Not only will the restuaruant location be considered, but other venues around the restaurant will also be utilized for comparison. An area with more restaurants of one type may present too much competition, which can help to drive the business model on which type of restaurant to create.  Also, having other venues around the restaurant will indicate a higher probability of foot traffic and more potential business. 

A description of the data and how it will be used to solve the problem. (15 marks)

First the state of Ohio will be broken down by Area code. After organizing the chart to have descending population, it was found that the two largest cities in Ohio (by population) are Cleveland and Columbus. 

The four main variables that were analyzed were that of the restaurants and total venues of each city (see below)
1. cle_dataframe_restaurant
2. cle_datatrame_venues
3. cbus_dataframe_restaurant
4. cbus_dataframe_venues

Each city was found using the geocoder where the latitude and longitude numbers were utilized. 

The API from foursquare was utilized having to have found the Client ID (), Client Secret, and Acess Token ().
CLIENT_ID = 'ZRS2NV2A04VQZNFID0INKRS00YCZCTYVMVDFIR1L4FX5ZVIG' 
CLIENT_SECRET = 'PRK2N423NAEOOKKKTL5EL4LLRJ2A4SJJYFJU2V55QT5WRMOQ' 
ACCESS_TOKEN = 'K1HE3T2FSR4DHLLJYC1MNQMO2WE4JROAKLUSVO0MEZ0GJ5LP'

Requests were then made through the Foursquare server to look for restaurants and venues within each city center.  The results of the analysis were cleaned and process in the dataframe.

Each request was visualized using the folios chart with the red dot indicating the city center and the blue dots indicating the four square results.  

Lastly, an analysis of the two cities was done using the mean of the distance between venues and restuarants as well as a qualitative analysis to see the diversity of restaurants/venues within the city. 


```python
import pandas as pd
import numpy as np
import geocoder
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import folium

import requests # library to handle requests
import random # library for random number generation
!pip install geopy
from geopy.geocoders import Nominatim # module to convert an address into latitude and longitude values

# libraries for displaying images
from IPython.display import Image 
from IPython.core.display import HTML 
    
# tranforming json file into a pandas dataframe library
from pandas.io.json import json_normalize

! pip install folium==0.5.0
import folium # plotting library

print('Folium installed')
print('Libraries imported.')
```

    Requirement already satisfied: geopy in c:\users\hengo\anaconda3\lib\site-packages (2.1.0)
    Requirement already satisfied: geographiclib<2,>=1.49 in c:\users\hengo\anaconda3\lib\site-packages (from geopy) (1.50)
    Requirement already satisfied: folium==0.5.0 in c:\users\hengo\anaconda3\lib\site-packages (0.5.0)
    Requirement already satisfied: six in c:\users\hengo\anaconda3\lib\site-packages (from folium==0.5.0) (1.15.0)
    Requirement already satisfied: branca in c:\users\hengo\anaconda3\lib\site-packages (from folium==0.5.0) (0.4.2)
    Requirement already satisfied: jinja2 in c:\users\hengo\anaconda3\lib\site-packages (from folium==0.5.0) (2.11.2)
    Requirement already satisfied: requests in c:\users\hengo\anaconda3\lib\site-packages (from folium==0.5.0) (2.25.1)
    Requirement already satisfied: MarkupSafe>=0.23 in c:\users\hengo\anaconda3\lib\site-packages (from jinja2->folium==0.5.0) (1.1.1)
    Requirement already satisfied: certifi>=2017.4.17 in c:\users\hengo\anaconda3\lib\site-packages (from requests->folium==0.5.0) (2020.12.5)
    Requirement already satisfied: urllib3<1.27,>=1.21.1 in c:\users\hengo\anaconda3\lib\site-packages (from requests->folium==0.5.0) (1.26.2)
    Requirement already satisfied: idna<3,>=2.5 in c:\users\hengo\anaconda3\lib\site-packages (from requests->folium==0.5.0) (2.10)
    Requirement already satisfied: chardet<5,>=3.0.2 in c:\users\hengo\anaconda3\lib\site-packages (from requests->folium==0.5.0) (4.0.0)
    Folium installed
    Libraries imported.
    

Ohio cities information


```python
# 2. Scrape the Wikipedia page
url = 'https://en.wikipedia.org/wiki/List_of_Ohio_area_codes'
df = pd.read_html(url)
print(len(df))
print(type(df))
```

    3
    <class 'list'>
    


```python
df = df[0]
df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Code</th>
      <th>Created</th>
      <th>Region</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>216</td>
      <td>1947</td>
      <td>Cleveland (October 1947)</td>
    </tr>
    <tr>
      <th>1</th>
      <td>220</td>
      <td>2015</td>
      <td>Central and southeastern Ohio except Columbus,...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>234</td>
      <td>2000</td>
      <td>Akron, Canton, Youngstown, and Warren, overlay...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>326</td>
      <td>2020</td>
      <td>Southwestern part of Ohio including Dayton, Sp...</td>
    </tr>
    <tr>
      <th>4</th>
      <td>330</td>
      <td>1996</td>
      <td>Akron, Canton, Youngstown, and Warren, overlay...</td>
    </tr>
    <tr>
      <th>5</th>
      <td>380</td>
      <td>2016</td>
      <td>Columbus, overlay with 614 (February 27, 2016)</td>
    </tr>
    <tr>
      <th>6</th>
      <td>419</td>
      <td>1947</td>
      <td>Northwest and north central Ohio including Tol...</td>
    </tr>
    <tr>
      <th>7</th>
      <td>440</td>
      <td>1997</td>
      <td>Part of Northeast Ohio including parts of Clev...</td>
    </tr>
    <tr>
      <th>8</th>
      <td>513</td>
      <td>1947</td>
      <td>Southwest Ohio including Cincinnati (October 1...</td>
    </tr>
    <tr>
      <th>9</th>
      <td>567</td>
      <td>2002</td>
      <td>Northwest and north central Ohio including Tol...</td>
    </tr>
    <tr>
      <th>10</th>
      <td>614</td>
      <td>1947</td>
      <td>Columbus, overlay with 380 (October 1947)</td>
    </tr>
    <tr>
      <th>11</th>
      <td>740</td>
      <td>1997</td>
      <td>Central and southeastern Ohio except Columbus,...</td>
    </tr>
    <tr>
      <th>12</th>
      <td>937</td>
      <td>1996</td>
      <td>Southwestern part of Ohio including Dayton, Sp...</td>
    </tr>
  </tbody>
</table>
</div>




```python
df_ohio = df.drop(['Created'], axis = 1)
df_ohio
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Code</th>
      <th>Region</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>216</td>
      <td>Cleveland (October 1947)</td>
    </tr>
    <tr>
      <th>1</th>
      <td>220</td>
      <td>Central and southeastern Ohio except Columbus,...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>234</td>
      <td>Akron, Canton, Youngstown, and Warren, overlay...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>326</td>
      <td>Southwestern part of Ohio including Dayton, Sp...</td>
    </tr>
    <tr>
      <th>4</th>
      <td>330</td>
      <td>Akron, Canton, Youngstown, and Warren, overlay...</td>
    </tr>
    <tr>
      <th>5</th>
      <td>380</td>
      <td>Columbus, overlay with 614 (February 27, 2016)</td>
    </tr>
    <tr>
      <th>6</th>
      <td>419</td>
      <td>Northwest and north central Ohio including Tol...</td>
    </tr>
    <tr>
      <th>7</th>
      <td>440</td>
      <td>Part of Northeast Ohio including parts of Clev...</td>
    </tr>
    <tr>
      <th>8</th>
      <td>513</td>
      <td>Southwest Ohio including Cincinnati (October 1...</td>
    </tr>
    <tr>
      <th>9</th>
      <td>567</td>
      <td>Northwest and north central Ohio including Tol...</td>
    </tr>
    <tr>
      <th>10</th>
      <td>614</td>
      <td>Columbus, overlay with 380 (October 1947)</td>
    </tr>
    <tr>
      <th>11</th>
      <td>740</td>
      <td>Central and southeastern Ohio except Columbus,...</td>
    </tr>
    <tr>
      <th>12</th>
      <td>937</td>
      <td>Southwestern part of Ohio including Dayton, Sp...</td>
    </tr>
  </tbody>
</table>
</div>




```python
import pandas as pd
```


```python
url_ohio_pop = 'https://en.wikipedia.org/wiki/List_of_cities_in_Ohio'
df_pop = pd.read_html(url_ohio_pop)
print(len(df_pop))
print(type(df_pop))
```

    3
    <class 'list'>
    


```python
df_pop1 = df_pop[0]
df_pop1
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>City</th>
      <th>Population</th>
      <th>County</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Akron</td>
      <td>198090</td>
      <td>Summit</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Alliance</td>
      <td>21616</td>
      <td>Mahoning</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Alliance</td>
      <td>21616</td>
      <td>Stark</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Amherst</td>
      <td>12021</td>
      <td>Lorain</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Ashland</td>
      <td>20423</td>
      <td>Ashland</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>271</th>
      <td>Worthington</td>
      <td>13575</td>
      <td>Franklin</td>
    </tr>
    <tr>
      <th>272</th>
      <td>Wyoming</td>
      <td>8428</td>
      <td>Hamilton</td>
    </tr>
    <tr>
      <th>273</th>
      <td>Xenia</td>
      <td>25719</td>
      <td>Greene</td>
    </tr>
    <tr>
      <th>274</th>
      <td>Youngstown</td>
      <td>64782</td>
      <td>Mahoning</td>
    </tr>
    <tr>
      <th>275</th>
      <td>Zanesville</td>
      <td>25487</td>
      <td>Muskingum</td>
    </tr>
  </tbody>
</table>
<p>276 rows × 3 columns</p>
</div>




```python
df_pop2 = df_pop1.sort_values(by = ['Population'], ascending = False)
df_pop2
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>City</th>
      <th>Population</th>
      <th>County</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>58</th>
      <td>Columbus</td>
      <td>892672</td>
      <td>Franklin</td>
    </tr>
    <tr>
      <th>56</th>
      <td>Columbus</td>
      <td>892672</td>
      <td>Delaware</td>
    </tr>
    <tr>
      <th>57</th>
      <td>Columbus</td>
      <td>892672</td>
      <td>Fairfield</td>
    </tr>
    <tr>
      <th>51</th>
      <td>Cleveland</td>
      <td>383793</td>
      <td>Cuyahoga</td>
    </tr>
    <tr>
      <th>47</th>
      <td>Cincinnati</td>
      <td>302605</td>
      <td>Hamilton</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>173</th>
      <td>Northwood</td>
      <td>5265</td>
      <td>Wood</td>
    </tr>
    <tr>
      <th>206</th>
      <td>Saint Clairsville</td>
      <td>5184</td>
      <td>Belmont</td>
    </tr>
    <tr>
      <th>44</th>
      <td>Chardon</td>
      <td>5148</td>
      <td>Geauga</td>
    </tr>
    <tr>
      <th>235</th>
      <td>Toronto</td>
      <td>5091</td>
      <td>Jefferson</td>
    </tr>
    <tr>
      <th>158</th>
      <td>Munroe Falls</td>
      <td>5012</td>
      <td>Summit</td>
    </tr>
  </tbody>
</table>
<p>276 rows × 3 columns</p>
</div>




```python
print(df_pop2.loc[[58]])
```

    58    892672
    Name: Population, dtype: int64
    

Columbus, Ohio Analysis


```python
address = 'Columbus, Ohio'

geolocator = Nominatim(user_agent="foursquare_agent")
location = geolocator.geocode(address)
latitude = location.latitude
longitude = location.longitude
print('The coordinates of Columbus, Ohio are {}, {}.'.format(latitude, longitude))
```

    The coordinates of Columbus, Ohio are 39.9622601, -83.0007065.
    


```python
CLIENT_ID = 'ZRS2NV2A04VQZNFID0INKRS00YCZCTYVMVDFIR1L4FX5ZVIG' # your Foursquare ID
CLIENT_SECRET = 'PRK2N423NAEOOKKKTL5EL4LLRJ2A4SJJYFJU2V55QT5WRMOQ' # your Foursquare Secret
ACCESS_TOKEN = 'K1HE3T2FSR4DHLLJYC1MNQMO2WE4JROAKLUSVO0MEZ0GJ5LP' # your FourSquare Access Token
VERSION = '20180604'
LIMIT = 30
print('Your credentails:')
print('CLIENT_ID: ' + CLIENT_ID)
print('CLIENT_SECRET:' + CLIENT_SECRET)
```

    Your credentails:
    CLIENT_ID: ZRS2NV2A04VQZNFID0INKRS00YCZCTYVMVDFIR1L4FX5ZVIG
    CLIENT_SECRET:PRK2N423NAEOOKKKTL5EL4LLRJ2A4SJJYFJU2V55QT5WRMOQ
    


```python
search_query = 'Restaurant'
radius = 500
print(search_query + ' .... OK!')
```

    Restaurant .... OK!
    


```python
url = 'https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&ll={},{}&oauth_token={}&v={}&query={}&radius={}&limit={}'.format(CLIENT_ID, CLIENT_SECRET, latitude, longitude,ACCESS_TOKEN, VERSION, search_query, radius, LIMIT)
url
```




    'https://api.foursquare.com/v2/venues/search?client_id=ZRS2NV2A04VQZNFID0INKRS00YCZCTYVMVDFIR1L4FX5ZVIG&client_secret=PRK2N423NAEOOKKKTL5EL4LLRJ2A4SJJYFJU2V55QT5WRMOQ&ll=39.9622601,-83.0007065&oauth_token=K1HE3T2FSR4DHLLJYC1MNQMO2WE4JROAKLUSVO0MEZ0GJ5LP&v=20180604&query=Restaurant&radius=500&limit=30'




```python
results = requests.get(url).json()
results
```




    {'meta': {'code': 200, 'requestId': '60490824d799930a420e523d'},
     'notifications': [{'type': 'notificationTray', 'item': {'unreadCount': 0}}],
     'response': {'venues': [{'id': '4b491017f964a5203f6426e3',
        'name': 'The Plaza Restaurant',
        'location': {'address': '75 E State St',
         'crossStreet': 'at Sheraton Columbus at Capitol Square',
         'lat': 39.960256204327145,
         'lng': -82.99771696409734,
         'labeledLatLngs': [{'label': 'display',
           'lat': 39.960256204327145,
           'lng': -82.99771696409734},
          {'label': 'entrance', 'lat': 39.960167, 'lng': -82.997941}],
         'distance': 338,
         'postalCode': '43215',
         'cc': 'US',
         'city': 'Columbus',
         'state': 'OH',
         'country': 'United States',
         'formattedAddress': ['75 E State St (at Sheraton Columbus at Capitol Square)',
          'Columbus, OH 43215']},
        'categories': [{'id': '4bf58dd8d48988d14e941735',
          'name': 'American Restaurant',
          'pluralName': 'American Restaurants',
          'shortName': 'American',
          'icon': {'prefix': 'https://ss3.4sqi.net/img/categories_v2/food/default_',
           'suffix': '.png'},
          'primary': True}],
        'referralId': 'v-1615398948',
        'hasPerk': False},
       {'id': '4f32757319836c91c7d9d5fb',
        'name': 'Michael Phillips Restaurant Group',
        'location': {'address': '20 N High St',
         'lat': 39.96281051635742,
         'lng': -83.00054931640625,
         'labeledLatLngs': [{'label': 'display',
           'lat': 39.96281051635742,
           'lng': -83.00054931640625}],
         'distance': 62,
         'postalCode': '43215',
         'cc': 'US',
         'city': 'Columbus',
         'state': 'OH',
         'country': 'United States',
         'formattedAddress': ['20 N High St', 'Columbus, OH 43215']},
        'categories': [{'id': '4d4b7105d754a06374d81259',
          'name': 'Food',
          'pluralName': 'Food',
          'shortName': 'Food',
          'icon': {'prefix': 'https://ss3.4sqi.net/img/categories_v2/food/default_',
           'suffix': '.png'},
          'primary': True}],
        'referralId': 'v-1615398948',
        'hasPerk': False},
       {'id': '4b7afb59f964a520f3492fe3',
        'name': 'Juice Bar Health Food Restaurant',
        'location': {'address': '41 S High St',
         'lat': 39.96121299460664,
         'lng': -82.99999752840088,
         'labeledLatLngs': [{'label': 'display',
           'lat': 39.96121299460664,
           'lng': -82.99999752840088}],
         'distance': 131,
         'postalCode': '43215',
         'cc': 'US',
         'city': 'Columbus',
         'state': 'OH',
         'country': 'United States',
         'formattedAddress': ['41 S High St', 'Columbus, OH 43215']},
        'categories': [{'id': '4bf58dd8d48988d112941735',
          'name': 'Juice Bar',
          'pluralName': 'Juice Bars',
          'shortName': 'Juice Bar',
          'icon': {'prefix': 'https://ss3.4sqi.net/img/categories_v2/food/juicebar_',
           'suffix': '.png'},
          'primary': True}],
        'referralId': 'v-1615398948',
        'hasPerk': False},
       {'id': '5b0476fa69e77b002c5b0f4f',
        'name': 'Veritas Restaurant',
        'location': {'address': '11 West Gay St',
         'lat': 39.9634792381194,
         'lng': -83.00140857696533,
         'labeledLatLngs': [{'label': 'display',
           'lat': 39.9634792381194,
           'lng': -83.00140857696533}],
         'distance': 148,
         'cc': 'US',
         'city': 'Columbus',
         'state': 'OH',
         'country': 'United States',
         'formattedAddress': ['11 West Gay St', 'Columbus, OH']},
        'categories': [{'id': '4bf58dd8d48988d157941735',
          'name': 'New American Restaurant',
          'pluralName': 'New American Restaurants',
          'shortName': 'New American',
          'icon': {'prefix': 'https://ss3.4sqi.net/img/categories_v2/food/newamerican_',
           'suffix': '.png'},
          'primary': True}],
        'referralId': 'v-1615398948',
        'hasPerk': False},
       {'id': '4f32749519836c91c7d98299',
        'name': 'Annas Restaurant',
        'location': {'address': '65 E Gay St',
         'lat': 39.963468,
         'lng': -82.998604,
         'labeledLatLngs': [{'label': 'display',
           'lat': 39.963468,
           'lng': -82.998604}],
         'distance': 224,
         'postalCode': '43215',
         'cc': 'US',
         'city': 'Columbus',
         'state': 'OH',
         'country': 'United States',
         'formattedAddress': ['65 E Gay St', 'Columbus, OH 43215']},
        'categories': [{'id': '4d4b7105d754a06374d81259',
          'name': 'Food',
          'pluralName': 'Food',
          'shortName': 'Food',
          'icon': {'prefix': 'https://ss3.4sqi.net/img/categories_v2/food/default_',
           'suffix': '.png'},
          'primary': True}],
        'referralId': 'v-1615398948',
        'hasPerk': False},
       {'id': '4b107f18f964a520bb7123e3',
        'name': 'Due Amici Restaurant',
        'location': {'address': '67 E Gay St',
         'crossStreet': 'Third Street',
         'lat': 39.96375935453356,
         'lng': -82.99882086606961,
         'labeledLatLngs': [{'label': 'display',
           'lat': 39.96375935453356,
           'lng': -82.99882086606961},
          {'label': 'entrance', 'lat': 39.963468, 'lng': -82.998906}],
         'distance': 231,
         'postalCode': '43215',
         'cc': 'US',
         'city': 'Columbus',
         'state': 'OH',
         'country': 'United States',
         'formattedAddress': ['67 E Gay St (Third Street)', 'Columbus, OH 43215']},
        'categories': [{'id': '4bf58dd8d48988d110941735',
          'name': 'Italian Restaurant',
          'pluralName': 'Italian Restaurants',
          'shortName': 'Italian',
          'icon': {'prefix': 'https://ss3.4sqi.net/img/categories_v2/food/italian_',
           'suffix': '.png'},
          'primary': True}],
        'delivery': {'id': '1318752',
         'url': 'https://www.grubhub.com/restaurant/due-amici-67-east-gay-street-columbus/1318752?affiliate=1131&utm_source=foursquare-affiliate-network&utm_medium=affiliate&utm_campaign=1131&utm_content=1318752',
         'provider': {'name': 'grubhub',
          'icon': {'prefix': 'https://fastly.4sqi.net/img/general/cap/',
           'sizes': [40, 50],
           'name': '/delivery_provider_grubhub_20180129.png'}}},
        'referralId': 'v-1615398948',
        'hasPerk': False},
       {'id': '5fc3b1ed06486b3bd918120a',
        'name': '4Th & State Downtown Restaurant',
        'location': {'address': '152 E State St',
         'lat': 39.960778,
         'lng': -82.996052,
         'labeledLatLngs': [{'label': 'display',
           'lat': 39.960778,
           'lng': -82.996052}],
         'distance': 430,
         'postalCode': '43215',
         'cc': 'US',
         'city': 'Columbus',
         'state': 'OH',
         'country': 'United States',
         'formattedAddress': ['152 E State St', 'Columbus, OH 43215']},
        'categories': [{'id': '4bf58dd8d48988d1d3941735',
          'name': 'Vegetarian / Vegan Restaurant',
          'pluralName': 'Vegetarian / Vegan Restaurants',
          'shortName': 'Vegetarian / Vegan',
          'icon': {'prefix': 'https://ss3.4sqi.net/img/categories_v2/food/vegetarian_',
           'suffix': '.png'},
          'primary': True}],
        'referralId': 'v-1615398948',
        'hasPerk': False},
       {'id': '4b914a74f964a52072b033e3',
        'name': 'Amici Restaurant',
        'location': {'lat': 39.966381,
         'lng': -83.001805,
         'labeledLatLngs': [{'label': 'display',
           'lat': 39.966381,
           'lng': -83.001805}],
         'distance': 468,
         'postalCode': '43215',
         'cc': 'US',
         'city': 'Columbus',
         'state': 'OH',
         'country': 'United States',
         'formattedAddress': ['Columbus, OH 43215']},
        'categories': [],
        'referralId': 'v-1615398948',
        'hasPerk': False},
       {'id': '4e2ad2b0fa76bbf847d21070',
        'name': 'Courtyard Marriott Restaurant',
        'location': {'lat': 39.966060147509396,
         'lng': -83.00281350495078,
         'labeledLatLngs': [{'label': 'display',
           'lat': 39.966060147509396,
           'lng': -83.00281350495078}],
         'distance': 459,
         'cc': 'US',
         'state': 'Ohio',
         'country': 'United States',
         'formattedAddress': ['Ohio']},
        'categories': [{'id': '4bf58dd8d48988d143941735',
          'name': 'Breakfast Spot',
          'pluralName': 'Breakfast Spots',
          'shortName': 'Breakfast',
          'icon': {'prefix': 'https://ss3.4sqi.net/img/categories_v2/food/breakfast_',
           'suffix': '.png'},
          'primary': True}],
        'referralId': 'v-1615398948',
        'hasPerk': False},
       {'id': '4f324b0c19836c91c7c96cbc',
        'name': 'Moon Star Chinese Restaurant',
        'location': {'address': '205 S High St',
         'lat': 39.95780944824219,
         'lng': -83.0000228881836,
         'labeledLatLngs': [{'label': 'display',
           'lat': 39.95780944824219,
           'lng': -83.0000228881836}],
         'distance': 498,
         'postalCode': '43215',
         'cc': 'US',
         'city': 'Columbus',
         'state': 'OH',
         'country': 'United States',
         'formattedAddress': ['205 S High St', 'Columbus, OH 43215']},
        'categories': [{'id': '4bf58dd8d48988d145941735',
          'name': 'Chinese Restaurant',
          'pluralName': 'Chinese Restaurants',
          'shortName': 'Chinese',
          'icon': {'prefix': 'https://ss3.4sqi.net/img/categories_v2/food/asian_',
           'suffix': '.png'},
          'primary': True}],
        'referralId': 'v-1615398948',
        'hasPerk': False},
       {'id': '52c88b3211d236d01459477e',
        'name': 'Greyhound Restaurant',
        'location': {'lat': 39.95857,
         'lng': -82.996598,
         'labeledLatLngs': [{'label': 'display',
           'lat': 39.95857,
           'lng': -82.996598}],
         'distance': 540,
         'cc': 'US',
         'city': 'Columbus',
         'state': 'OH',
         'country': 'United States',
         'formattedAddress': ['Columbus, OH']},
        'categories': [{'id': '4bf58dd8d48988d120951735',
          'name': 'Food Court',
          'pluralName': 'Food Courts',
          'shortName': 'Food Court',
          'icon': {'prefix': 'https://ss3.4sqi.net/img/categories_v2/shops/food_foodcourt_',
           'suffix': '.png'},
          'primary': True}],
        'referralId': 'v-1615398948',
        'hasPerk': False},
       {'id': '4b140226f964a520a39b23e3',
        'name': "Danny's Deli",
        'location': {'address': '37 W Broad St',
         'crossStreet': 'at S Front St',
         'lat': 39.96159119128514,
         'lng': -83.00223642069196,
         'labeledLatLngs': [{'label': 'display',
           'lat': 39.96159119128514,
           'lng': -83.00223642069196},
          {'label': 'entrance', 'lat': 39.961923, 'lng': -83.001742}],
         'distance': 150,
         'postalCode': '43215',
         'cc': 'US',
         'city': 'Columbus',
         'state': 'OH',
         'country': 'United States',
         'formattedAddress': ['37 W Broad St (at S Front St)',
          'Columbus, OH 43215']},
        'categories': [{'id': '4bf58dd8d48988d1c5941735',
          'name': 'Sandwich Place',
          'pluralName': 'Sandwich Places',
          'shortName': 'Sandwiches',
          'icon': {'prefix': 'https://ss3.4sqi.net/img/categories_v2/food/deli_',
           'suffix': '.png'},
          'primary': True}],
        'delivery': {'id': '2542345',
         'url': 'https://www.grubhub.com/restaurant/danny-delicious-37-west-broad-street-columbus/2542345?affiliate=1131&utm_source=foursquare-affiliate-network&utm_medium=affiliate&utm_campaign=1131&utm_content=2542345',
         'provider': {'name': 'grubhub',
          'icon': {'prefix': 'https://fastly.4sqi.net/img/general/cap/',
           'sizes': [40, 50],
           'name': '/delivery_provider_grubhub_20180129.png'}}},
        'referralId': 'v-1615398948',
        'hasPerk': False},
       {'id': '4b0b04b2f964a5209e2b23e3',
        'name': 'Elevator Brewery & Draught Haus',
        'location': {'address': '161 N High St',
         'lat': 39.965774930501674,
         'lng': -83.00175811472143,
         'labeledLatLngs': [{'label': 'display',
           'lat': 39.965774930501674,
           'lng': -83.00175811472143},
          {'label': 'entrance', 'lat': 39.965676, 'lng': -83.001462}],
         'distance': 401,
         'postalCode': '43215',
         'cc': 'US',
         'city': 'Columbus',
         'state': 'OH',
         'country': 'United States',
         'formattedAddress': ['161 N High St', 'Columbus, OH 43215']},
        'categories': [{'id': '50327c8591d4c4b30a586d5d',
          'name': 'Brewery',
          'pluralName': 'Breweries',
          'shortName': 'Brewery',
          'icon': {'prefix': 'https://ss3.4sqi.net/img/categories_v2/food/brewery_',
           'suffix': '.png'},
          'primary': True}],
        'referralId': 'v-1615398948',
        'hasPerk': False},
       {'id': '4bf7185d8d30d13a2f67fe17',
        'name': 'Elevator Brewery Brewquarters',
        'location': {'address': '165 N 4th St',
         'crossStreet': 'Spring',
         'lat': 39.96625385031577,
         'lng': -82.99736526144949,
         'labeledLatLngs': [{'label': 'display',
           'lat': 39.96625385031577,
           'lng': -82.99736526144949},
          {'label': 'entrance', 'lat': 39.966272, 'lng': -82.997084}],
         'distance': 528,
         'postalCode': '43215',
         'cc': 'US',
         'city': 'Columbus',
         'state': 'OH',
         'country': 'United States',
         'formattedAddress': ['165 N 4th St (Spring)', 'Columbus, OH 43215']},
        'categories': [{'id': '50327c8591d4c4b30a586d5d',
          'name': 'Brewery',
          'pluralName': 'Breweries',
          'shortName': 'Brewery',
          'icon': {'prefix': 'https://ss3.4sqi.net/img/categories_v2/food/brewery_',
           'suffix': '.png'},
          'primary': True}],
        'referralId': 'v-1615398948',
        'hasPerk': False}]}}




```python
# assign relevant part of JSON to venues
venues = results['response']['venues']
dataframe = pd.json_normalize(venues)
dataframe.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>name</th>
      <th>categories</th>
      <th>referralId</th>
      <th>hasPerk</th>
      <th>location.address</th>
      <th>location.crossStreet</th>
      <th>location.lat</th>
      <th>location.lng</th>
      <th>location.labeledLatLngs</th>
      <th>...</th>
      <th>location.city</th>
      <th>location.state</th>
      <th>location.country</th>
      <th>location.formattedAddress</th>
      <th>delivery.id</th>
      <th>delivery.url</th>
      <th>delivery.provider.name</th>
      <th>delivery.provider.icon.prefix</th>
      <th>delivery.provider.icon.sizes</th>
      <th>delivery.provider.icon.name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>4b491017f964a5203f6426e3</td>
      <td>The Plaza Restaurant</td>
      <td>[{'id': '4bf58dd8d48988d14e941735', 'name': 'A...</td>
      <td>v-1615398948</td>
      <td>False</td>
      <td>75 E State St</td>
      <td>at Sheraton Columbus at Capitol Square</td>
      <td>39.960256</td>
      <td>-82.997717</td>
      <td>[{'label': 'display', 'lat': 39.96025620432714...</td>
      <td>...</td>
      <td>Columbus</td>
      <td>OH</td>
      <td>United States</td>
      <td>[75 E State St (at Sheraton Columbus at Capito...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1</th>
      <td>4f32757319836c91c7d9d5fb</td>
      <td>Michael Phillips Restaurant Group</td>
      <td>[{'id': '4d4b7105d754a06374d81259', 'name': 'F...</td>
      <td>v-1615398948</td>
      <td>False</td>
      <td>20 N High St</td>
      <td>NaN</td>
      <td>39.962811</td>
      <td>-83.000549</td>
      <td>[{'label': 'display', 'lat': 39.96281051635742...</td>
      <td>...</td>
      <td>Columbus</td>
      <td>OH</td>
      <td>United States</td>
      <td>[20 N High St, Columbus, OH 43215]</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2</th>
      <td>4b7afb59f964a520f3492fe3</td>
      <td>Juice Bar Health Food Restaurant</td>
      <td>[{'id': '4bf58dd8d48988d112941735', 'name': 'J...</td>
      <td>v-1615398948</td>
      <td>False</td>
      <td>41 S High St</td>
      <td>NaN</td>
      <td>39.961213</td>
      <td>-82.999998</td>
      <td>[{'label': 'display', 'lat': 39.96121299460664...</td>
      <td>...</td>
      <td>Columbus</td>
      <td>OH</td>
      <td>United States</td>
      <td>[41 S High St, Columbus, OH 43215]</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3</th>
      <td>5b0476fa69e77b002c5b0f4f</td>
      <td>Veritas Restaurant</td>
      <td>[{'id': '4bf58dd8d48988d157941735', 'name': 'N...</td>
      <td>v-1615398948</td>
      <td>False</td>
      <td>11 West Gay St</td>
      <td>NaN</td>
      <td>39.963479</td>
      <td>-83.001409</td>
      <td>[{'label': 'display', 'lat': 39.9634792381194,...</td>
      <td>...</td>
      <td>Columbus</td>
      <td>OH</td>
      <td>United States</td>
      <td>[11 West Gay St, Columbus, OH]</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>4</th>
      <td>4f32749519836c91c7d98299</td>
      <td>Annas Restaurant</td>
      <td>[{'id': '4d4b7105d754a06374d81259', 'name': 'F...</td>
      <td>v-1615398948</td>
      <td>False</td>
      <td>65 E Gay St</td>
      <td>NaN</td>
      <td>39.963468</td>
      <td>-82.998604</td>
      <td>[{'label': 'display', 'lat': 39.963468, 'lng':...</td>
      <td>...</td>
      <td>Columbus</td>
      <td>OH</td>
      <td>United States</td>
      <td>[65 E Gay St, Columbus, OH 43215]</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 23 columns</p>
</div>




```python
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
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>name</th>
      <th>categories</th>
      <th>address</th>
      <th>crossStreet</th>
      <th>lat</th>
      <th>lng</th>
      <th>labeledLatLngs</th>
      <th>distance</th>
      <th>postalCode</th>
      <th>cc</th>
      <th>city</th>
      <th>state</th>
      <th>country</th>
      <th>formattedAddress</th>
      <th>id</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>The Plaza Restaurant</td>
      <td>American Restaurant</td>
      <td>75 E State St</td>
      <td>at Sheraton Columbus at Capitol Square</td>
      <td>39.960256</td>
      <td>-82.997717</td>
      <td>[{'label': 'display', 'lat': 39.96025620432714...</td>
      <td>338</td>
      <td>43215</td>
      <td>US</td>
      <td>Columbus</td>
      <td>OH</td>
      <td>United States</td>
      <td>[75 E State St (at Sheraton Columbus at Capito...</td>
      <td>4b491017f964a5203f6426e3</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Michael Phillips Restaurant Group</td>
      <td>Food</td>
      <td>20 N High St</td>
      <td>NaN</td>
      <td>39.962811</td>
      <td>-83.000549</td>
      <td>[{'label': 'display', 'lat': 39.96281051635742...</td>
      <td>62</td>
      <td>43215</td>
      <td>US</td>
      <td>Columbus</td>
      <td>OH</td>
      <td>United States</td>
      <td>[20 N High St, Columbus, OH 43215]</td>
      <td>4f32757319836c91c7d9d5fb</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Juice Bar Health Food Restaurant</td>
      <td>Juice Bar</td>
      <td>41 S High St</td>
      <td>NaN</td>
      <td>39.961213</td>
      <td>-82.999998</td>
      <td>[{'label': 'display', 'lat': 39.96121299460664...</td>
      <td>131</td>
      <td>43215</td>
      <td>US</td>
      <td>Columbus</td>
      <td>OH</td>
      <td>United States</td>
      <td>[41 S High St, Columbus, OH 43215]</td>
      <td>4b7afb59f964a520f3492fe3</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Veritas Restaurant</td>
      <td>New American Restaurant</td>
      <td>11 West Gay St</td>
      <td>NaN</td>
      <td>39.963479</td>
      <td>-83.001409</td>
      <td>[{'label': 'display', 'lat': 39.9634792381194,...</td>
      <td>148</td>
      <td>NaN</td>
      <td>US</td>
      <td>Columbus</td>
      <td>OH</td>
      <td>United States</td>
      <td>[11 West Gay St, Columbus, OH]</td>
      <td>5b0476fa69e77b002c5b0f4f</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Annas Restaurant</td>
      <td>Food</td>
      <td>65 E Gay St</td>
      <td>NaN</td>
      <td>39.963468</td>
      <td>-82.998604</td>
      <td>[{'label': 'display', 'lat': 39.963468, 'lng':...</td>
      <td>224</td>
      <td>43215</td>
      <td>US</td>
      <td>Columbus</td>
      <td>OH</td>
      <td>United States</td>
      <td>[65 E Gay St, Columbus, OH 43215]</td>
      <td>4f32749519836c91c7d98299</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Due Amici Restaurant</td>
      <td>Italian Restaurant</td>
      <td>67 E Gay St</td>
      <td>Third Street</td>
      <td>39.963759</td>
      <td>-82.998821</td>
      <td>[{'label': 'display', 'lat': 39.96375935453356...</td>
      <td>231</td>
      <td>43215</td>
      <td>US</td>
      <td>Columbus</td>
      <td>OH</td>
      <td>United States</td>
      <td>[67 E Gay St (Third Street), Columbus, OH 43215]</td>
      <td>4b107f18f964a520bb7123e3</td>
    </tr>
    <tr>
      <th>6</th>
      <td>4Th &amp; State Downtown Restaurant</td>
      <td>Vegetarian / Vegan Restaurant</td>
      <td>152 E State St</td>
      <td>NaN</td>
      <td>39.960778</td>
      <td>-82.996052</td>
      <td>[{'label': 'display', 'lat': 39.960778, 'lng':...</td>
      <td>430</td>
      <td>43215</td>
      <td>US</td>
      <td>Columbus</td>
      <td>OH</td>
      <td>United States</td>
      <td>[152 E State St, Columbus, OH 43215]</td>
      <td>5fc3b1ed06486b3bd918120a</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Amici Restaurant</td>
      <td>None</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>39.966381</td>
      <td>-83.001805</td>
      <td>[{'label': 'display', 'lat': 39.966381, 'lng':...</td>
      <td>468</td>
      <td>43215</td>
      <td>US</td>
      <td>Columbus</td>
      <td>OH</td>
      <td>United States</td>
      <td>[Columbus, OH 43215]</td>
      <td>4b914a74f964a52072b033e3</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Courtyard Marriott Restaurant</td>
      <td>Breakfast Spot</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>39.966060</td>
      <td>-83.002814</td>
      <td>[{'label': 'display', 'lat': 39.96606014750939...</td>
      <td>459</td>
      <td>NaN</td>
      <td>US</td>
      <td>NaN</td>
      <td>Ohio</td>
      <td>United States</td>
      <td>[Ohio]</td>
      <td>4e2ad2b0fa76bbf847d21070</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Moon Star Chinese Restaurant</td>
      <td>Chinese Restaurant</td>
      <td>205 S High St</td>
      <td>NaN</td>
      <td>39.957809</td>
      <td>-83.000023</td>
      <td>[{'label': 'display', 'lat': 39.95780944824219...</td>
      <td>498</td>
      <td>43215</td>
      <td>US</td>
      <td>Columbus</td>
      <td>OH</td>
      <td>United States</td>
      <td>[205 S High St, Columbus, OH 43215]</td>
      <td>4f324b0c19836c91c7c96cbc</td>
    </tr>
    <tr>
      <th>10</th>
      <td>Greyhound Restaurant</td>
      <td>Food Court</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>39.958570</td>
      <td>-82.996598</td>
      <td>[{'label': 'display', 'lat': 39.95857, 'lng': ...</td>
      <td>540</td>
      <td>NaN</td>
      <td>US</td>
      <td>Columbus</td>
      <td>OH</td>
      <td>United States</td>
      <td>[Columbus, OH]</td>
      <td>52c88b3211d236d01459477e</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Danny's Deli</td>
      <td>Sandwich Place</td>
      <td>37 W Broad St</td>
      <td>at S Front St</td>
      <td>39.961591</td>
      <td>-83.002236</td>
      <td>[{'label': 'display', 'lat': 39.96159119128514...</td>
      <td>150</td>
      <td>43215</td>
      <td>US</td>
      <td>Columbus</td>
      <td>OH</td>
      <td>United States</td>
      <td>[37 W Broad St (at S Front St), Columbus, OH 4...</td>
      <td>4b140226f964a520a39b23e3</td>
    </tr>
    <tr>
      <th>12</th>
      <td>Elevator Brewery &amp; Draught Haus</td>
      <td>Brewery</td>
      <td>161 N High St</td>
      <td>NaN</td>
      <td>39.965775</td>
      <td>-83.001758</td>
      <td>[{'label': 'display', 'lat': 39.96577493050167...</td>
      <td>401</td>
      <td>43215</td>
      <td>US</td>
      <td>Columbus</td>
      <td>OH</td>
      <td>United States</td>
      <td>[161 N High St, Columbus, OH 43215]</td>
      <td>4b0b04b2f964a5209e2b23e3</td>
    </tr>
    <tr>
      <th>13</th>
      <td>Elevator Brewery Brewquarters</td>
      <td>Brewery</td>
      <td>165 N 4th St</td>
      <td>Spring</td>
      <td>39.966254</td>
      <td>-82.997365</td>
      <td>[{'label': 'display', 'lat': 39.96625385031577...</td>
      <td>528</td>
      <td>43215</td>
      <td>US</td>
      <td>Columbus</td>
      <td>OH</td>
      <td>United States</td>
      <td>[165 N 4th St (Spring), Columbus, OH 43215]</td>
      <td>4bf7185d8d30d13a2f67fe17</td>
    </tr>
  </tbody>
</table>
</div>




```python
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
```




<div style="width:100%;"><div style="position:relative;width:100%;height:0;padding-bottom:60%;"><span style="color:#565656">Make this Notebook Trusted to load map: File -> Trust Notebook</span><iframe src="about:blank" style="position:absolute;width:100%;height:100%;left:0;top:0;border:none !important;" data-html=%3C%21DOCTYPE%20html%3E%0A%3Chead%3E%20%20%20%20%0A%20%20%20%20%3Cmeta%20http-equiv%3D%22content-type%22%20content%3D%22text/html%3B%20charset%3DUTF-8%22%20/%3E%0A%20%20%20%20%3Cscript%3EL_PREFER_CANVAS%20%3D%20false%3B%20L_NO_TOUCH%20%3D%20false%3B%20L_DISABLE_3D%20%3D%20false%3B%3C/script%3E%0A%20%20%20%20%3Cscript%20src%3D%22https%3A//cdn.jsdelivr.net/npm/leaflet%401.2.0/dist/leaflet.js%22%3E%3C/script%3E%0A%20%20%20%20%3Cscript%20src%3D%22https%3A//ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js%22%3E%3C/script%3E%0A%20%20%20%20%3Cscript%20src%3D%22https%3A//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js%22%3E%3C/script%3E%0A%20%20%20%20%3Cscript%20src%3D%22https%3A//cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.js%22%3E%3C/script%3E%0A%20%20%20%20%3Clink%20rel%3D%22stylesheet%22%20href%3D%22https%3A//cdn.jsdelivr.net/npm/leaflet%401.2.0/dist/leaflet.css%22/%3E%0A%20%20%20%20%3Clink%20rel%3D%22stylesheet%22%20href%3D%22https%3A//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css%22/%3E%0A%20%20%20%20%3Clink%20rel%3D%22stylesheet%22%20href%3D%22https%3A//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap-theme.min.css%22/%3E%0A%20%20%20%20%3Clink%20rel%3D%22stylesheet%22%20href%3D%22https%3A//maxcdn.bootstrapcdn.com/font-awesome/4.6.3/css/font-awesome.min.css%22/%3E%0A%20%20%20%20%3Clink%20rel%3D%22stylesheet%22%20href%3D%22https%3A//cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.css%22/%3E%0A%20%20%20%20%3Clink%20rel%3D%22stylesheet%22%20href%3D%22https%3A//rawgit.com/python-visualization/folium/master/folium/templates/leaflet.awesome.rotate.css%22/%3E%0A%20%20%20%20%3Cstyle%3Ehtml%2C%20body%20%7Bwidth%3A%20100%25%3Bheight%3A%20100%25%3Bmargin%3A%200%3Bpadding%3A%200%3B%7D%3C/style%3E%0A%20%20%20%20%3Cstyle%3E%23map%20%7Bposition%3Aabsolute%3Btop%3A0%3Bbottom%3A0%3Bright%3A0%3Bleft%3A0%3B%7D%3C/style%3E%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%3Cstyle%3E%20%23map_1640012c66dc40ae8882f73f2a542d87%20%7B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20position%20%3A%20relative%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20width%20%3A%20100.0%25%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20height%3A%20100.0%25%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20left%3A%200.0%25%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20top%3A%200.0%25%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%3C/style%3E%0A%20%20%20%20%20%20%20%20%0A%3C/head%3E%0A%3Cbody%3E%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%3Cdiv%20class%3D%22folium-map%22%20id%3D%22map_1640012c66dc40ae8882f73f2a542d87%22%20%3E%3C/div%3E%0A%20%20%20%20%20%20%20%20%0A%3C/body%3E%0A%3Cscript%3E%20%20%20%20%0A%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20bounds%20%3D%20null%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20map_1640012c66dc40ae8882f73f2a542d87%20%3D%20L.map%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%27map_1640012c66dc40ae8882f73f2a542d87%27%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7Bcenter%3A%20%5B39.9622601%2C-83.0007065%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20zoom%3A%2015%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20maxBounds%3A%20bounds%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20layers%3A%20%5B%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20worldCopyJump%3A%20false%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20crs%3A%20L.CRS.EPSG3857%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7D%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20tile_layer_6445160710744c9599592af1ecd6c408%20%3D%20L.tileLayer%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%27https%3A//%7Bs%7D.tile.openstreetmap.org/%7Bz%7D/%7Bx%7D/%7By%7D.png%27%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22attribution%22%3A%20null%2C%0A%20%20%22detectRetina%22%3A%20false%2C%0A%20%20%22maxZoom%22%3A%2018%2C%0A%20%20%22minZoom%22%3A%201%2C%0A%20%20%22noWrap%22%3A%20false%2C%0A%20%20%22subdomains%22%3A%20%22abc%22%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_1640012c66dc40ae8882f73f2a542d87%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_a3359ccc445a412db57ab6b18b94d6fd%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.9622601%2C-83.0007065%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22red%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22red%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%2010%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_1640012c66dc40ae8882f73f2a542d87%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_1cf2ec479caa4ae193d3d89deb0cb70c%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_4f513f659a11415e8c42585f49a5582d%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_4f513f659a11415e8c42585f49a5582d%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EConrad%20Hotel%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_1cf2ec479caa4ae193d3d89deb0cb70c.setContent%28html_4f513f659a11415e8c42585f49a5582d%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_a3359ccc445a412db57ab6b18b94d6fd.bindPopup%28popup_1cf2ec479caa4ae193d3d89deb0cb70c%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_946962121c814a63a3ea4cb02dad1ec6%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.960256204327145%2C-82.99771696409734%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_1640012c66dc40ae8882f73f2a542d87%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_a521d7f69c8349adb843828b7e8f1684%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_bfe9019d0e5e48ef99dbe00aafa77edb%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_bfe9019d0e5e48ef99dbe00aafa77edb%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EAmerican%20Restaurant%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_a521d7f69c8349adb843828b7e8f1684.setContent%28html_bfe9019d0e5e48ef99dbe00aafa77edb%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_946962121c814a63a3ea4cb02dad1ec6.bindPopup%28popup_a521d7f69c8349adb843828b7e8f1684%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_8809e6115c8a45b496eb62027d2545b2%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.96281051635742%2C-83.00054931640625%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_1640012c66dc40ae8882f73f2a542d87%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_89b3da9e22d540b38ba7fb0eaf10e0b3%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_d1725e08a1894ef893a1ff429bf8459a%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_d1725e08a1894ef893a1ff429bf8459a%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EFood%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_89b3da9e22d540b38ba7fb0eaf10e0b3.setContent%28html_d1725e08a1894ef893a1ff429bf8459a%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_8809e6115c8a45b496eb62027d2545b2.bindPopup%28popup_89b3da9e22d540b38ba7fb0eaf10e0b3%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_0c39ff933e19435bb110a120e1945a0a%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.96121299460664%2C-82.99999752840088%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_1640012c66dc40ae8882f73f2a542d87%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_d9583389ec95417087091db7d42adf54%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_6caa6994a16c43d9939ce78010701654%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_6caa6994a16c43d9939ce78010701654%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EJuice%20Bar%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_d9583389ec95417087091db7d42adf54.setContent%28html_6caa6994a16c43d9939ce78010701654%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_0c39ff933e19435bb110a120e1945a0a.bindPopup%28popup_d9583389ec95417087091db7d42adf54%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_ceb3896082f34ab892e997b47a23c6f9%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.9634792381194%2C-83.00140857696533%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_1640012c66dc40ae8882f73f2a542d87%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_f501148a820e49ae8f5e4cf515b20204%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_7abc986a7bb3422ea5c2b4ce5a8b2635%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_7abc986a7bb3422ea5c2b4ce5a8b2635%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ENew%20American%20Restaurant%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_f501148a820e49ae8f5e4cf515b20204.setContent%28html_7abc986a7bb3422ea5c2b4ce5a8b2635%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_ceb3896082f34ab892e997b47a23c6f9.bindPopup%28popup_f501148a820e49ae8f5e4cf515b20204%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_f661cfbfc6304992b8ec2dc207213f2c%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.963468%2C-82.998604%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_1640012c66dc40ae8882f73f2a542d87%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_8a940d698c0044ec914d1912f0e751e4%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_33f2000ffa8349d2ad5f467b86f841dd%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_33f2000ffa8349d2ad5f467b86f841dd%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EFood%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_8a940d698c0044ec914d1912f0e751e4.setContent%28html_33f2000ffa8349d2ad5f467b86f841dd%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_f661cfbfc6304992b8ec2dc207213f2c.bindPopup%28popup_8a940d698c0044ec914d1912f0e751e4%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_fff26fd8be1f4f669e1a34575f72f3a8%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.96375935453356%2C-82.99882086606961%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_1640012c66dc40ae8882f73f2a542d87%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_0131257e5d2b44da812a2678ffda10e5%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_277a81f36b1f42ba8e172f24855c9b30%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_277a81f36b1f42ba8e172f24855c9b30%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EItalian%20Restaurant%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_0131257e5d2b44da812a2678ffda10e5.setContent%28html_277a81f36b1f42ba8e172f24855c9b30%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_fff26fd8be1f4f669e1a34575f72f3a8.bindPopup%28popup_0131257e5d2b44da812a2678ffda10e5%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_8feaa1ee8af748aca6a2031591177389%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.960778%2C-82.996052%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_1640012c66dc40ae8882f73f2a542d87%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_8e35fffc362f417682794e005e92eb0b%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_d6653de207ab473481796cae7a4c5e4b%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_d6653de207ab473481796cae7a4c5e4b%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EVegetarian%20/%20Vegan%20Restaurant%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_8e35fffc362f417682794e005e92eb0b.setContent%28html_d6653de207ab473481796cae7a4c5e4b%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_8feaa1ee8af748aca6a2031591177389.bindPopup%28popup_8e35fffc362f417682794e005e92eb0b%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_eae8bba0f1ba44f8a461acc71992fba5%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.966381%2C-83.001805%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_1640012c66dc40ae8882f73f2a542d87%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_c695dd56a37a4a4fa7bf9a84beb08142%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.966060147509396%2C-83.00281350495078%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_1640012c66dc40ae8882f73f2a542d87%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_97aec0c150274b8db7803676d867ab2d%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_04f48ac228c544ff8bf54285e2708a2d%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_04f48ac228c544ff8bf54285e2708a2d%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EBreakfast%20Spot%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_97aec0c150274b8db7803676d867ab2d.setContent%28html_04f48ac228c544ff8bf54285e2708a2d%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_c695dd56a37a4a4fa7bf9a84beb08142.bindPopup%28popup_97aec0c150274b8db7803676d867ab2d%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_998d9b59537545c9bda7c258c288eb8c%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.95780944824219%2C-83.0000228881836%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_1640012c66dc40ae8882f73f2a542d87%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_d94c2341414748928016064835ecda9e%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_496968a454a74959be1652d9a3386ce9%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_496968a454a74959be1652d9a3386ce9%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EChinese%20Restaurant%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_d94c2341414748928016064835ecda9e.setContent%28html_496968a454a74959be1652d9a3386ce9%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_998d9b59537545c9bda7c258c288eb8c.bindPopup%28popup_d94c2341414748928016064835ecda9e%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_19e2a1317d3a4d6d8f4e0ed4ba476c38%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.95857%2C-82.996598%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_1640012c66dc40ae8882f73f2a542d87%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_9175d2b8a3fe4984945bcf1539333fbe%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_40ea66c7350f496c8cef696c586a0308%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_40ea66c7350f496c8cef696c586a0308%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EFood%20Court%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_9175d2b8a3fe4984945bcf1539333fbe.setContent%28html_40ea66c7350f496c8cef696c586a0308%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_19e2a1317d3a4d6d8f4e0ed4ba476c38.bindPopup%28popup_9175d2b8a3fe4984945bcf1539333fbe%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_4b793e2714ac4b189e5919b49a4c19d2%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.96159119128514%2C-83.00223642069196%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_1640012c66dc40ae8882f73f2a542d87%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_248624deadec4e8cbd923e0a9934593b%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_54834da06e5e4cdc93befb6c2aa8bd7f%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_54834da06e5e4cdc93befb6c2aa8bd7f%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ESandwich%20Place%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_248624deadec4e8cbd923e0a9934593b.setContent%28html_54834da06e5e4cdc93befb6c2aa8bd7f%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_4b793e2714ac4b189e5919b49a4c19d2.bindPopup%28popup_248624deadec4e8cbd923e0a9934593b%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_aa6324642b514e178ca77105870d738d%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.965774930501674%2C-83.00175811472143%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_1640012c66dc40ae8882f73f2a542d87%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_ef961eccbdbe4c548fd51eae1be833f6%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_8277b37028584f71879326a189530992%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_8277b37028584f71879326a189530992%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EBrewery%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_ef961eccbdbe4c548fd51eae1be833f6.setContent%28html_8277b37028584f71879326a189530992%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_aa6324642b514e178ca77105870d738d.bindPopup%28popup_ef961eccbdbe4c548fd51eae1be833f6%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_decfaca3d9a84eb280cb9aec149d4f0c%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.96625385031577%2C-82.99736526144949%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_1640012c66dc40ae8882f73f2a542d87%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_a1717097cc834edfa54d90140518e716%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_25d4211f25614184bc926ab81dd3bc7f%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_25d4211f25614184bc926ab81dd3bc7f%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EBrewery%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_a1717097cc834edfa54d90140518e716.setContent%28html_25d4211f25614184bc926ab81dd3bc7f%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_decfaca3d9a84eb280cb9aec149d4f0c.bindPopup%28popup_a1717097cc834edfa54d90140518e716%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%3C/script%3E onload="this.contentDocument.open();this.contentDocument.write(    decodeURIComponent(this.getAttribute('data-html')));this.contentDocument.close();" allowfullscreen webkitallowfullscreen mozallowfullscreen></iframe></div></div>



Explore Columbus businesses


```python
url = 'https://api.foursquare.com/v2/venues/explore?client_id={}&client_secret={}&ll={},{}&v={}&radius={}&limit={}'.format(CLIENT_ID, CLIENT_SECRET, latitude, longitude, VERSION, radius, LIMIT)
url
```




    'https://api.foursquare.com/v2/venues/explore?client_id=ZRS2NV2A04VQZNFID0INKRS00YCZCTYVMVDFIR1L4FX5ZVIG&client_secret=PRK2N423NAEOOKKKTL5EL4LLRJ2A4SJJYFJU2V55QT5WRMOQ&ll=39.9622601,-83.0007065&v=20180604&radius=500&limit=30'




```python
import requests
```


```python
results = requests.get(url).json()
'There are {} around Columbus, Ohio.'.format(len(results['response']['groups'][0]['items']))
```




    'There are 30 around Columbus, Ohio.'




```python
items = results['response']['groups'][0]['items']
items[0]
```




    {'reasons': {'count': 0,
      'items': [{'summary': 'This spot is popular',
        'type': 'general',
        'reasonName': 'globalInteractionReason'}]},
     'venue': {'id': '4b0aafe2f964a520642623e3',
      'name': 'Café Brioso',
      'location': {'address': '14 E Gay St',
       'crossStreet': 'at N. High Street',
       'lat': 39.96363995001144,
       'lng': -83.00056843562001,
       'labeledLatLngs': [{'label': 'display',
         'lat': 39.96363995001144,
         'lng': -83.00056843562001},
        {'label': 'entrance', 'lat': 39.963755, 'lng': -83.00065}],
       'distance': 154,
       'postalCode': '43215',
       'cc': 'US',
       'city': 'Columbus',
       'state': 'OH',
       'country': 'United States',
       'formattedAddress': ['14 E Gay St (at N. High Street)',
        'Columbus, OH 43215',
        'United States']},
      'categories': [{'id': '4bf58dd8d48988d1e0931735',
        'name': 'Coffee Shop',
        'pluralName': 'Coffee Shops',
        'shortName': 'Coffee Shop',
        'icon': {'prefix': 'https://ss3.4sqi.net/img/categories_v2/food/coffeeshop_',
         'suffix': '.png'},
        'primary': True}],
      'photos': {'count': 0, 'groups': []},
      'venuePage': {'id': '32833229'}},
     'referralId': 'e-0-4b0aafe2f964a520642623e3-0'}




```python
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
```

    <ipython-input-250-289ff5f6b758>:1: FutureWarning: pandas.io.json.json_normalize is deprecated, use pandas.json_normalize instead
      dataframe = json_normalize(items) # flatten JSON
    




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>name</th>
      <th>categories</th>
      <th>address</th>
      <th>crossStreet</th>
      <th>lat</th>
      <th>lng</th>
      <th>labeledLatLngs</th>
      <th>distance</th>
      <th>postalCode</th>
      <th>cc</th>
      <th>city</th>
      <th>state</th>
      <th>country</th>
      <th>formattedAddress</th>
      <th>neighborhood</th>
      <th>id</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Café Brioso</td>
      <td>Coffee Shop</td>
      <td>14 E Gay St</td>
      <td>at N. High Street</td>
      <td>39.963640</td>
      <td>-83.000568</td>
      <td>[{'label': 'display', 'lat': 39.96363995001144...</td>
      <td>154</td>
      <td>43215</td>
      <td>US</td>
      <td>Columbus</td>
      <td>OH</td>
      <td>United States</td>
      <td>[14 E Gay St (at N. High Street), Columbus, OH...</td>
      <td>NaN</td>
      <td>4b0aafe2f964a520642623e3</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Si Señor!</td>
      <td>Latin American Restaurant</td>
      <td>72 E Lynn St</td>
      <td>Pearl Alley</td>
      <td>39.963314</td>
      <td>-82.998769</td>
      <td>[{'label': 'display', 'lat': 39.96331434826980...</td>
      <td>202</td>
      <td>43215</td>
      <td>US</td>
      <td>Columbus</td>
      <td>OH</td>
      <td>United States</td>
      <td>[72 E Lynn St (Pearl Alley), Columbus, OH 4321...</td>
      <td>NaN</td>
      <td>4ba0f7cff964a520e78a37e3</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Ohio Theatre</td>
      <td>Theater</td>
      <td>39 E State St</td>
      <td>NaN</td>
      <td>39.960281</td>
      <td>-82.999090</td>
      <td>[{'label': 'display', 'lat': 39.9602811061592,...</td>
      <td>259</td>
      <td>43215</td>
      <td>US</td>
      <td>Columbus</td>
      <td>OH</td>
      <td>United States</td>
      <td>[39 E State St, Columbus, OH 43215, United Sta...</td>
      <td>NaN</td>
      <td>4b195041f964a52010db23e3</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Moonlight Market</td>
      <td>Arts &amp; Crafts Store</td>
      <td>NaN</td>
      <td>Gay St.</td>
      <td>39.963803</td>
      <td>-82.999985</td>
      <td>[{'label': 'display', 'lat': 39.96380258156589...</td>
      <td>182</td>
      <td>NaN</td>
      <td>US</td>
      <td>Columbus</td>
      <td>OH</td>
      <td>United States</td>
      <td>[Gay St., Columbus, OH, United States]</td>
      <td>NaN</td>
      <td>5169d89f498e469204f04814</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Hotel LeVeque, Autograph Collection</td>
      <td>Hotel</td>
      <td>50 W Broad St</td>
      <td>Broad and Front</td>
      <td>39.962299</td>
      <td>-83.002059</td>
      <td>[{'label': 'display', 'lat': 39.96229935639491...</td>
      <td>115</td>
      <td>43215</td>
      <td>US</td>
      <td>Columbus</td>
      <td>OH</td>
      <td>United States</td>
      <td>[50 W Broad St (Broad and Front), Columbus, OH...</td>
      <td>NaN</td>
      <td>58c96261735a4d6c4d5595a3</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Ohio Statehouse</td>
      <td>Capitol Building</td>
      <td>1 Capitol Sq</td>
      <td>N High St</td>
      <td>39.961317</td>
      <td>-82.998999</td>
      <td>[{'label': 'display', 'lat': 39.9613173177356,...</td>
      <td>179</td>
      <td>43215</td>
      <td>US</td>
      <td>Columbus</td>
      <td>OH</td>
      <td>United States</td>
      <td>[1 Capitol Sq (N High St), Columbus, OH 43215,...</td>
      <td>NaN</td>
      <td>4b2d024ff964a5203dcc24e3</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Palace Theatre</td>
      <td>Theater</td>
      <td>34 W Broad St</td>
      <td>NaN</td>
      <td>39.962515</td>
      <td>-83.002334</td>
      <td>[{'label': 'display', 'lat': 39.96251516633823...</td>
      <td>141</td>
      <td>43215</td>
      <td>US</td>
      <td>Columbus</td>
      <td>OH</td>
      <td>United States</td>
      <td>[34 W Broad St, Columbus, OH 43215, United Sta...</td>
      <td>NaN</td>
      <td>4b058649f964a520bb5a22e3</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Buckeye Bourbon House</td>
      <td>Whisky Bar</td>
      <td>36 East Gay Street</td>
      <td>NaN</td>
      <td>39.963721</td>
      <td>-82.999950</td>
      <td>[{'label': 'display', 'lat': 39.96372147121163...</td>
      <td>175</td>
      <td>43215</td>
      <td>US</td>
      <td>Columbus</td>
      <td>OH</td>
      <td>United States</td>
      <td>[36 East Gay Street, Columbus, OH 43215, Unite...</td>
      <td>NaN</td>
      <td>589ba47051d19e538db89ad3</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Due Amici Restaurant</td>
      <td>Italian Restaurant</td>
      <td>67 E Gay St</td>
      <td>Third Street</td>
      <td>39.963759</td>
      <td>-82.998821</td>
      <td>[{'label': 'display', 'lat': 39.96375935453356...</td>
      <td>231</td>
      <td>43215</td>
      <td>US</td>
      <td>Columbus</td>
      <td>OH</td>
      <td>United States</td>
      <td>[67 E Gay St (Third Street), Columbus, OH 4321...</td>
      <td>NaN</td>
      <td>4b107f18f964a520bb7123e3</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Tip Top Kitchen &amp; Cocktails</td>
      <td>American Restaurant</td>
      <td>73 E Gay St</td>
      <td>at Third St</td>
      <td>39.963772</td>
      <td>-82.998777</td>
      <td>[{'label': 'display', 'lat': 39.96377178554681...</td>
      <td>235</td>
      <td>43215</td>
      <td>US</td>
      <td>Columbus</td>
      <td>OH</td>
      <td>United States</td>
      <td>[73 E Gay St (at Third St), Columbus, OH 43215...</td>
      <td>NaN</td>
      <td>4b058649f964a520c35a22e3</td>
    </tr>
  </tbody>
</table>
</div>




```python
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
```




<div style="width:100%;"><div style="position:relative;width:100%;height:0;padding-bottom:60%;"><span style="color:#565656">Make this Notebook Trusted to load map: File -> Trust Notebook</span><iframe src="about:blank" style="position:absolute;width:100%;height:100%;left:0;top:0;border:none !important;" data-html=%3C%21DOCTYPE%20html%3E%0A%3Chead%3E%20%20%20%20%0A%20%20%20%20%3Cmeta%20http-equiv%3D%22content-type%22%20content%3D%22text/html%3B%20charset%3DUTF-8%22%20/%3E%0A%20%20%20%20%3Cscript%3EL_PREFER_CANVAS%20%3D%20false%3B%20L_NO_TOUCH%20%3D%20false%3B%20L_DISABLE_3D%20%3D%20false%3B%3C/script%3E%0A%20%20%20%20%3Cscript%20src%3D%22https%3A//cdn.jsdelivr.net/npm/leaflet%401.2.0/dist/leaflet.js%22%3E%3C/script%3E%0A%20%20%20%20%3Cscript%20src%3D%22https%3A//ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js%22%3E%3C/script%3E%0A%20%20%20%20%3Cscript%20src%3D%22https%3A//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js%22%3E%3C/script%3E%0A%20%20%20%20%3Cscript%20src%3D%22https%3A//cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.js%22%3E%3C/script%3E%0A%20%20%20%20%3Clink%20rel%3D%22stylesheet%22%20href%3D%22https%3A//cdn.jsdelivr.net/npm/leaflet%401.2.0/dist/leaflet.css%22/%3E%0A%20%20%20%20%3Clink%20rel%3D%22stylesheet%22%20href%3D%22https%3A//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css%22/%3E%0A%20%20%20%20%3Clink%20rel%3D%22stylesheet%22%20href%3D%22https%3A//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap-theme.min.css%22/%3E%0A%20%20%20%20%3Clink%20rel%3D%22stylesheet%22%20href%3D%22https%3A//maxcdn.bootstrapcdn.com/font-awesome/4.6.3/css/font-awesome.min.css%22/%3E%0A%20%20%20%20%3Clink%20rel%3D%22stylesheet%22%20href%3D%22https%3A//cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.css%22/%3E%0A%20%20%20%20%3Clink%20rel%3D%22stylesheet%22%20href%3D%22https%3A//rawgit.com/python-visualization/folium/master/folium/templates/leaflet.awesome.rotate.css%22/%3E%0A%20%20%20%20%3Cstyle%3Ehtml%2C%20body%20%7Bwidth%3A%20100%25%3Bheight%3A%20100%25%3Bmargin%3A%200%3Bpadding%3A%200%3B%7D%3C/style%3E%0A%20%20%20%20%3Cstyle%3E%23map%20%7Bposition%3Aabsolute%3Btop%3A0%3Bbottom%3A0%3Bright%3A0%3Bleft%3A0%3B%7D%3C/style%3E%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%3Cstyle%3E%20%23map_6a01172b62ac4bd69b89122b37c60ab2%20%7B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20position%20%3A%20relative%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20width%20%3A%20100.0%25%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20height%3A%20100.0%25%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20left%3A%200.0%25%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20top%3A%200.0%25%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%3C/style%3E%0A%20%20%20%20%20%20%20%20%0A%3C/head%3E%0A%3Cbody%3E%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%3Cdiv%20class%3D%22folium-map%22%20id%3D%22map_6a01172b62ac4bd69b89122b37c60ab2%22%20%3E%3C/div%3E%0A%20%20%20%20%20%20%20%20%0A%3C/body%3E%0A%3Cscript%3E%20%20%20%20%0A%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20bounds%20%3D%20null%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20map_6a01172b62ac4bd69b89122b37c60ab2%20%3D%20L.map%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%27map_6a01172b62ac4bd69b89122b37c60ab2%27%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7Bcenter%3A%20%5B39.9622601%2C-83.0007065%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20zoom%3A%2015%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20maxBounds%3A%20bounds%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20layers%3A%20%5B%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20worldCopyJump%3A%20false%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20crs%3A%20L.CRS.EPSG3857%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7D%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20tile_layer_86d4039174d64834bcf3b79e1cbdb457%20%3D%20L.tileLayer%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%27https%3A//%7Bs%7D.tile.openstreetmap.org/%7Bz%7D/%7Bx%7D/%7By%7D.png%27%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22attribution%22%3A%20null%2C%0A%20%20%22detectRetina%22%3A%20false%2C%0A%20%20%22maxZoom%22%3A%2018%2C%0A%20%20%22minZoom%22%3A%201%2C%0A%20%20%22noWrap%22%3A%20false%2C%0A%20%20%22subdomains%22%3A%20%22abc%22%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_6a01172b62ac4bd69b89122b37c60ab2%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_9f2d9b8f301f4a9f821fe93e9209128c%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.9622601%2C-83.0007065%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22red%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22red%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%2010%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_6a01172b62ac4bd69b89122b37c60ab2%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_bccf7880b7d64448b6093ca9746d1052%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_7f4e568dd5ff4d8181e72c8e09481299%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_7f4e568dd5ff4d8181e72c8e09481299%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EEcco%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_bccf7880b7d64448b6093ca9746d1052.setContent%28html_7f4e568dd5ff4d8181e72c8e09481299%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_9f2d9b8f301f4a9f821fe93e9209128c.bindPopup%28popup_bccf7880b7d64448b6093ca9746d1052%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_bcafe8a78b7f45de93313ccfb8bb0d5a%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.96363995001144%2C-83.00056843562001%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_6a01172b62ac4bd69b89122b37c60ab2%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_26f4b08aeeed43f4b47a5d25df6bfa7a%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_dfbdc12956a8472e81dd502b715dc4ef%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_dfbdc12956a8472e81dd502b715dc4ef%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ECoffee%20Shop%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_26f4b08aeeed43f4b47a5d25df6bfa7a.setContent%28html_dfbdc12956a8472e81dd502b715dc4ef%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_bcafe8a78b7f45de93313ccfb8bb0d5a.bindPopup%28popup_26f4b08aeeed43f4b47a5d25df6bfa7a%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_7abbaa356dd740e3b7dd2ef292b80932%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.963314348269805%2C-82.99876887694457%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_6a01172b62ac4bd69b89122b37c60ab2%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_7668081c1fd9481b837ab2f0089132e1%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_920ccb46d7494667bdf535e07244a9d1%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_920ccb46d7494667bdf535e07244a9d1%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ELatin%20American%20Restaurant%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_7668081c1fd9481b837ab2f0089132e1.setContent%28html_920ccb46d7494667bdf535e07244a9d1%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_7abbaa356dd740e3b7dd2ef292b80932.bindPopup%28popup_7668081c1fd9481b837ab2f0089132e1%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_9855430e17e746f794e1b3e5a2119b78%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.9602811061592%2C-82.99909047530281%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_6a01172b62ac4bd69b89122b37c60ab2%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_dde0564c13024df68beccb7bb6101471%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_74f86e7d0a4e456fbd8e0e18f1823558%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_74f86e7d0a4e456fbd8e0e18f1823558%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ETheater%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_dde0564c13024df68beccb7bb6101471.setContent%28html_74f86e7d0a4e456fbd8e0e18f1823558%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_9855430e17e746f794e1b3e5a2119b78.bindPopup%28popup_dde0564c13024df68beccb7bb6101471%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_00ec02704ce74e6191a6b255067de06f%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.96380258156589%2C-82.99998522990438%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_6a01172b62ac4bd69b89122b37c60ab2%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_8802fea6c5c343e18134fc2612d59ce4%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_45807e985b7a48cda8b8c9630bd83cca%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_45807e985b7a48cda8b8c9630bd83cca%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EArts%20%26%20Crafts%20Store%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_8802fea6c5c343e18134fc2612d59ce4.setContent%28html_45807e985b7a48cda8b8c9630bd83cca%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_00ec02704ce74e6191a6b255067de06f.bindPopup%28popup_8802fea6c5c343e18134fc2612d59ce4%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_fe29d7dab4374786b601065a46bc00d9%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.96229935639491%2C-83.00205926410854%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_6a01172b62ac4bd69b89122b37c60ab2%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_eb6a76c5df6a496098f78ec8250b7541%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_bb8ba77d72554598b63498ea4f8690af%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_bb8ba77d72554598b63498ea4f8690af%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EHotel%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_eb6a76c5df6a496098f78ec8250b7541.setContent%28html_bb8ba77d72554598b63498ea4f8690af%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_fe29d7dab4374786b601065a46bc00d9.bindPopup%28popup_eb6a76c5df6a496098f78ec8250b7541%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_f7fa7ec126954f68b4eb1dba1165d4ca%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.9613173177356%2C-82.99899871587945%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_6a01172b62ac4bd69b89122b37c60ab2%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_9eadd588a9744f94b7dd6501527154a7%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_5b2a470669ca4b90bc1e36dee0ea1dc2%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_5b2a470669ca4b90bc1e36dee0ea1dc2%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ECapitol%20Building%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_9eadd588a9744f94b7dd6501527154a7.setContent%28html_5b2a470669ca4b90bc1e36dee0ea1dc2%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_f7fa7ec126954f68b4eb1dba1165d4ca.bindPopup%28popup_9eadd588a9744f94b7dd6501527154a7%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_3cb84b339a904c1d85d8d5c261d91601%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.96251516633823%2C-83.002333726136%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_6a01172b62ac4bd69b89122b37c60ab2%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_246b2956493d46a1aa3aec0f20bbaa06%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_25bc514df15e4d02a77edd772020c455%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_25bc514df15e4d02a77edd772020c455%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ETheater%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_246b2956493d46a1aa3aec0f20bbaa06.setContent%28html_25bc514df15e4d02a77edd772020c455%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_3cb84b339a904c1d85d8d5c261d91601.bindPopup%28popup_246b2956493d46a1aa3aec0f20bbaa06%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_38012c44a50f429e82689649d0ae88e9%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.96372147121163%2C-82.99994989570284%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_6a01172b62ac4bd69b89122b37c60ab2%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_9cdad17aa40c4b4088ce1a36ab35279c%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_a301728fcad9425badec316a9b62ce76%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_a301728fcad9425badec316a9b62ce76%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EWhisky%20Bar%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_9cdad17aa40c4b4088ce1a36ab35279c.setContent%28html_a301728fcad9425badec316a9b62ce76%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_38012c44a50f429e82689649d0ae88e9.bindPopup%28popup_9cdad17aa40c4b4088ce1a36ab35279c%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_3a16148ebace48f3b588d39766932d25%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.96375935453356%2C-82.99882086606961%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_6a01172b62ac4bd69b89122b37c60ab2%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_701429c9e06d4b3bb94237f76b91b270%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_c55f4d2ca80f431f88aacf52e20fb71a%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_c55f4d2ca80f431f88aacf52e20fb71a%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EItalian%20Restaurant%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_701429c9e06d4b3bb94237f76b91b270.setContent%28html_c55f4d2ca80f431f88aacf52e20fb71a%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_3a16148ebace48f3b588d39766932d25.bindPopup%28popup_701429c9e06d4b3bb94237f76b91b270%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_6a709c0711164b56833712ae20968ec5%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.96377178554681%2C-82.99877666617621%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_6a01172b62ac4bd69b89122b37c60ab2%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_d65e89e6ac8a4e359273fae9fac77dba%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_3fd83cc4d01642d0ac800b3964f57c3b%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_3fd83cc4d01642d0ac800b3964f57c3b%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EAmerican%20Restaurant%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_d65e89e6ac8a4e359273fae9fac77dba.setContent%28html_3fd83cc4d01642d0ac800b3964f57c3b%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_6a709c0711164b56833712ae20968ec5.bindPopup%28popup_d65e89e6ac8a4e359273fae9fac77dba%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_7729e07db35e40d0a1f115ca25ff6607%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.96278391%2C-82.99819044%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_6a01172b62ac4bd69b89122b37c60ab2%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_fca1fc136b914e048e7e217749a0fdee%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_31ee07c82fae4ceeab0ba975488d2eed%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_31ee07c82fae4ceeab0ba975488d2eed%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ECoffee%20Shop%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_fca1fc136b914e048e7e217749a0fdee.setContent%28html_31ee07c82fae4ceeab0ba975488d2eed%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_7729e07db35e40d0a1f115ca25ff6607.bindPopup%28popup_fca1fc136b914e048e7e217749a0fdee%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_55ae23494c2e48ce813f189a13027c0a%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.9635158%2C-82.9983604%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_6a01172b62ac4bd69b89122b37c60ab2%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_d7728603dda54668b5ba735e16718a96%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_ea3b5c28aae14b19ac43d6a68f6d375b%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_ea3b5c28aae14b19ac43d6a68f6d375b%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ESteakhouse%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_d7728603dda54668b5ba735e16718a96.setContent%28html_ea3b5c28aae14b19ac43d6a68f6d375b%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_55ae23494c2e48ce813f189a13027c0a.bindPopup%28popup_d7728603dda54668b5ba735e16718a96%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_71ae763e5cd24d99bc01ee1ccee1a8f2%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.964417%2C-83.002748%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_6a01172b62ac4bd69b89122b37c60ab2%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_09e3142c61f647c18086150155d226ba%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_bd35577cf9a941a19f842665e26df3a1%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_bd35577cf9a941a19f842665e26df3a1%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ECaf%C3%A9%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_09e3142c61f647c18086150155d226ba.setContent%28html_bd35577cf9a941a19f842665e26df3a1%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_71ae763e5cd24d99bc01ee1ccee1a8f2.bindPopup%28popup_09e3142c61f647c18086150155d226ba%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_1bcaf2dcbbdb45d5855da1d04aa312e6%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.96518471739724%2C-83.0011438550397%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_6a01172b62ac4bd69b89122b37c60ab2%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_23930001dda64f80846084599fae8cb6%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_000eb271bd40498dbf63e704ebcd6503%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_000eb271bd40498dbf63e704ebcd6503%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EDeli%20/%20Bodega%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_23930001dda64f80846084599fae8cb6.setContent%28html_000eb271bd40498dbf63e704ebcd6503%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_1bcaf2dcbbdb45d5855da1d04aa312e6.bindPopup%28popup_23930001dda64f80846084599fae8cb6%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_586357d9557e449abae160b9b8ad20b4%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.96211355847053%2C-83.00227492711895%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_6a01172b62ac4bd69b89122b37c60ab2%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_3a9f5e9bf53a4421bd04e0f36a8c1731%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_c94ace74bab24356bdfc514ba68bba40%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_c94ace74bab24356bdfc514ba68bba40%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EHotel%20Bar%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_3a9f5e9bf53a4421bd04e0f36a8c1731.setContent%28html_c94ace74bab24356bdfc514ba68bba40%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_586357d9557e449abae160b9b8ad20b4.bindPopup%28popup_3a9f5e9bf53a4421bd04e0f36a8c1731%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_eacd1b311d0d41febd5dd1a0a6c207d2%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.962941001949794%2C-82.9969388920307%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_6a01172b62ac4bd69b89122b37c60ab2%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_98fabade4af448a0bce3140b475a72ec%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_41e79870cd264897ada33035bc2cfa88%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_41e79870cd264897ada33035bc2cfa88%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EGym%20/%20Fitness%20Center%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_98fabade4af448a0bce3140b475a72ec.setContent%28html_41e79870cd264897ada33035bc2cfa88%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_eacd1b311d0d41febd5dd1a0a6c207d2.bindPopup%28popup_98fabade4af448a0bce3140b475a72ec%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_9c2953544ef24a118544649214fbaa50%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.9593775616348%2C-82.99986327217285%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_6a01172b62ac4bd69b89122b37c60ab2%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_79554e6b5240470ca9461cc2370a864f%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_19ef518dcb3642e6814f95c184247f8d%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_19ef518dcb3642e6814f95c184247f8d%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ETaco%20Place%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_79554e6b5240470ca9461cc2370a864f.setContent%28html_19ef518dcb3642e6814f95c184247f8d%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_9c2953544ef24a118544649214fbaa50.bindPopup%28popup_79554e6b5240470ca9461cc2370a864f%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_35579416c20e46cfbca5c4bd83a981b3%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.963051632495116%2C-82.99986362457275%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_6a01172b62ac4bd69b89122b37c60ab2%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_13657fb52eca4ccd9fe6c2c561b9a508%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_2401a7c848564ce18d28cdbdbad2c397%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_2401a7c848564ce18d28cdbdbad2c397%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EFarmers%20Market%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_13657fb52eca4ccd9fe6c2c561b9a508.setContent%28html_2401a7c848564ce18d28cdbdbad2c397%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_35579416c20e46cfbca5c4bd83a981b3.bindPopup%28popup_13657fb52eca4ccd9fe6c2c561b9a508%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_51c6259bb6414f3c9b9c15eb495e2141%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.96120607529633%2C-83.00034060155167%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_6a01172b62ac4bd69b89122b37c60ab2%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_eee2f7e607cd46769f3360a6a1350cc6%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_4b925e48a36a4216aa9d8a99557c23f5%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_4b925e48a36a4216aa9d8a99557c23f5%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ECoffee%20Shop%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_eee2f7e607cd46769f3360a6a1350cc6.setContent%28html_4b925e48a36a4216aa9d8a99557c23f5%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_51c6259bb6414f3c9b9c15eb495e2141.bindPopup%28popup_eee2f7e607cd46769f3360a6a1350cc6%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_5e6e4b19096a4ae29a3ff36c9406bcfe%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.963303%2C-83.000334%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_6a01172b62ac4bd69b89122b37c60ab2%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_7e6256dd3e2a4a36b1577b3dcb48d34b%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_40343286ce994babbbe20cc536da64b6%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_40343286ce994babbbe20cc536da64b6%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ELeather%20Goods%20Store%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_7e6256dd3e2a4a36b1577b3dcb48d34b.setContent%28html_40343286ce994babbbe20cc536da64b6%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_5e6e4b19096a4ae29a3ff36c9406bcfe.bindPopup%28popup_7e6256dd3e2a4a36b1577b3dcb48d34b%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_b202f57a335b409eb3e69ecf917d1458%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.965406473207494%2C-82.9980016224784%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_6a01172b62ac4bd69b89122b37c60ab2%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_143dbf25c0b8406da887c885264a025e%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_f4b1c1f0004a4572953c75ba8929ea2d%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_f4b1c1f0004a4572953c75ba8929ea2d%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ERecord%20Shop%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_143dbf25c0b8406da887c885264a025e.setContent%28html_f4b1c1f0004a4572953c75ba8929ea2d%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_b202f57a335b409eb3e69ecf917d1458.bindPopup%28popup_143dbf25c0b8406da887c885264a025e%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_39c9bd01ca6148cdbcdac22c81548c3b%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.96361633561406%2C-82.9999144039499%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_6a01172b62ac4bd69b89122b37c60ab2%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_ca064a8514cc413d8b39af71b751f2b6%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_6f183d82416a4e63a6f34133871ecc44%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_6f183d82416a4e63a6f34133871ecc44%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EIrish%20Pub%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_ca064a8514cc413d8b39af71b751f2b6.setContent%28html_6f183d82416a4e63a6f34133871ecc44%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_39c9bd01ca6148cdbcdac22c81548c3b.bindPopup%28popup_ca064a8514cc413d8b39af71b751f2b6%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_6fa952ea314d422fb7812e5f6985d963%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.960222116585264%2C-82.99792241026108%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_6a01172b62ac4bd69b89122b37c60ab2%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_9c5dfdfcafd6416b9269630583a97a3f%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_bb77f3921c4841888bcbd9f698499c15%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_bb77f3921c4841888bcbd9f698499c15%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ESalad%20Place%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_9c5dfdfcafd6416b9269630583a97a3f.setContent%28html_bb77f3921c4841888bcbd9f698499c15%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_6fa952ea314d422fb7812e5f6985d963.bindPopup%28popup_9c5dfdfcafd6416b9269630583a97a3f%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_2eecdf1fea054577b295ac834dc7870e%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.9634740888355%2C-82.99814923417732%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_6a01172b62ac4bd69b89122b37c60ab2%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_aeb04e06ab7a49ab9e29fdc7b8bd50e3%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_52035523886b4d7cb7565cded8304058%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_52035523886b4d7cb7565cded8304058%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EHotel%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_aeb04e06ab7a49ab9e29fdc7b8bd50e3.setContent%28html_52035523886b4d7cb7565cded8304058%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_2eecdf1fea054577b295ac834dc7870e.bindPopup%28popup_aeb04e06ab7a49ab9e29fdc7b8bd50e3%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_eba8d9aa5c744138802c8c14863fac03%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.96346037653453%2C-83.00077710161985%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_6a01172b62ac4bd69b89122b37c60ab2%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_985bb3ef71304e28be4287cc298696c2%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_3334e5cd203e4602b4b93408129b0e94%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_3334e5cd203e4602b4b93408129b0e94%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EAsian%20Restaurant%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_985bb3ef71304e28be4287cc298696c2.setContent%28html_3334e5cd203e4602b4b93408129b0e94%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_eba8d9aa5c744138802c8c14863fac03.bindPopup%28popup_985bb3ef71304e28be4287cc298696c2%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_f9e61296093d4cb2879e5cbc2efa1e44%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.958941688041364%2C-83.00027518029934%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_6a01172b62ac4bd69b89122b37c60ab2%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_886363a7dded4620a69f72defcdaf8c0%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_a78ec49d4d6b4a42abbcc9a9e61ba9a9%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_a78ec49d4d6b4a42abbcc9a9e61ba9a9%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EArt%20Gallery%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_886363a7dded4620a69f72defcdaf8c0.setContent%28html_a78ec49d4d6b4a42abbcc9a9e61ba9a9%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_f9e61296093d4cb2879e5cbc2efa1e44.bindPopup%28popup_886363a7dded4620a69f72defcdaf8c0%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_e6ed1d5944a04bcb8f2e3820c666f9db%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.96383399686143%2C-82.99861029918011%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_6a01172b62ac4bd69b89122b37c60ab2%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_76571d95ceda4422b48ab8e491d89a8e%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_38a7773d7b1c43069cbeaf2a136c59a1%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_38a7773d7b1c43069cbeaf2a136c59a1%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ECuban%20Restaurant%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_76571d95ceda4422b48ab8e491d89a8e.setContent%28html_38a7773d7b1c43069cbeaf2a136c59a1%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_e6ed1d5944a04bcb8f2e3820c666f9db.bindPopup%28popup_76571d95ceda4422b48ab8e491d89a8e%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_b824db1a950a4bddb9f392de21df23d5%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.963240945185525%2C-83.00080324360862%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_6a01172b62ac4bd69b89122b37c60ab2%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_57a594990a974a8a86c1637d8d8e7fcf%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_e6ea4c69170d46eebfc3dc92d6c43a7c%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_e6ea4c69170d46eebfc3dc92d6c43a7c%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EPizza%20Place%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_57a594990a974a8a86c1637d8d8e7fcf.setContent%28html_e6ea4c69170d46eebfc3dc92d6c43a7c%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_b824db1a950a4bddb9f392de21df23d5.bindPopup%28popup_57a594990a974a8a86c1637d8d8e7fcf%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_fa7df8c7a4954c97b7ceba81aa685bba%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.963530852999355%2C-82.99638762164376%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_6a01172b62ac4bd69b89122b37c60ab2%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_158fe9c03b8b471883363861f1770a38%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_d358d62634794e6098f23c6cbd474043%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_d358d62634794e6098f23c6cbd474043%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EEvent%20Space%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_158fe9c03b8b471883363861f1770a38.setContent%28html_d358d62634794e6098f23c6cbd474043%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_fa7df8c7a4954c97b7ceba81aa685bba.bindPopup%28popup_158fe9c03b8b471883363861f1770a38%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_760d92bb7e9e438f8f01be50f02f9ca6%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B39.95867466388746%2C-82.99840770788457%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_6a01172b62ac4bd69b89122b37c60ab2%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_8f24f9ed63d441fdbbd7925fdf457b3a%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_b8e8f22909b14999b74a7f32dceb4ffa%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_b8e8f22909b14999b74a7f32dceb4ffa%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ECaf%C3%A9%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_8f24f9ed63d441fdbbd7925fdf457b3a.setContent%28html_b8e8f22909b14999b74a7f32dceb4ffa%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_760d92bb7e9e438f8f01be50f02f9ca6.bindPopup%28popup_8f24f9ed63d441fdbbd7925fdf457b3a%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%3C/script%3E onload="this.contentDocument.open();this.contentDocument.write(    decodeURIComponent(this.getAttribute('data-html')));this.contentDocument.close();" allowfullscreen webkitallowfullscreen mozallowfullscreen></iframe></div></div>



Trending Venues Columbus, Ohio


```python
# define URL
url = 'https://api.foursquare.com/v2/venues/trending?client_id={}&client_secret={}&ll={},{}&v={}'.format(CLIENT_ID, CLIENT_SECRET, latitude, longitude, VERSION)

# send GET request and get trending venues
results = requests.get(url).json()
results
```




    {'meta': {'code': 200, 'requestId': '6049082797d24e3f5ef5165d'},
     'response': {'venues': []}}




```python
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
```


```python
# display trending venues
trending_venues_df
```




    'No trending venues are available at the moment!'



CLEVELAND,  OHIO Analysis


```python
address = 'Cleveland, Ohio'

geolocator = Nominatim(user_agent="foursquare_agent")
location = geolocator.geocode(address1)
latitude = location.latitude
longitude = location.longitude
print('The coordinates of Cleveland, Ohio are {}, {}.'.format(latitude1, longitude1))
```

    The coordinates of Cleveland, Ohio are 39.9622601, -83.0007065.
    


```python
search_query = 'Restaurant'
radius = 500
print(search_query + ' .... OK!')
```

    Restaurant .... OK!
    


```python
url = 'https://api.foursquare.com/v2/venues/search?client_id={}&client_secret={}&ll={},{}&oauth_token={}&v={}&query={}&radius={}&limit={}'.format(CLIENT_ID, CLIENT_SECRET, latitude, longitude,ACCESS_TOKEN, VERSION, search_query, radius, LIMIT)
url
```




    'https://api.foursquare.com/v2/venues/search?client_id=ZRS2NV2A04VQZNFID0INKRS00YCZCTYVMVDFIR1L4FX5ZVIG&client_secret=PRK2N423NAEOOKKKTL5EL4LLRJ2A4SJJYFJU2V55QT5WRMOQ&ll=41.5051613,-81.6934446&oauth_token=K1HE3T2FSR4DHLLJYC1MNQMO2WE4JROAKLUSVO0MEZ0GJ5LP&v=20180604&query=Restaurant&radius=500&limit=30'




```python
results = requests.get(url).json()
results
```




    {'meta': {'code': 200, 'requestId': '6049082768265d5191e4c544'},
     'notifications': [{'type': 'notificationTray', 'item': {'unreadCount': 0}}],
     'response': {'venues': [{'id': '5748cb02498e1c0c6cfa6584',
        'name': 'The Burnham Restaurant',
        'location': {'address': 'Hilton Cleveland Downtown',
         'lat': 41.50299558347314,
         'lng': -81.69587648445662,
         'labeledLatLngs': [{'label': 'display',
           'lat': 41.50299558347314,
           'lng': -81.69587648445662}],
         'distance': 315,
         'postalCode': '44114',
         'cc': 'US',
         'city': 'Cleveland',
         'state': 'OH',
         'country': 'United States',
         'formattedAddress': ['Hilton Cleveland Downtown', 'Cleveland, OH 44114']},
        'categories': [{'id': '4bf58dd8d48988d157941735',
          'name': 'New American Restaurant',
          'pluralName': 'New American Restaurants',
          'shortName': 'New American',
          'icon': {'prefix': 'https://ss3.4sqi.net/img/categories_v2/food/newamerican_',
           'suffix': '.png'},
          'primary': True}],
        'referralId': 'v-1615398951',
        'hasPerk': False},
       {'id': '4f32385b19836c91c7c1fbc6',
        'name': 'Mannys Cozy Corner Restaurant',
        'location': {'address': '815 Superior Ave E',
         'lat': 41.50242233276367,
         'lng': -81.68932342529297,
         'labeledLatLngs': [{'label': 'display',
           'lat': 41.50242233276367,
           'lng': -81.68932342529297}],
         'distance': 459,
         'postalCode': '44114',
         'cc': 'US',
         'city': 'Cleveland',
         'state': 'OH',
         'country': 'United States',
         'formattedAddress': ['815 Superior Ave E', 'Cleveland, OH 44114']},
        'categories': [{'id': '4d4b7105d754a06374d81259',
          'name': 'Food',
          'pluralName': 'Food',
          'shortName': 'Food',
          'icon': {'prefix': 'https://ss3.4sqi.net/img/categories_v2/food/default_',
           'suffix': '.png'},
          'primary': True}],
        'referralId': 'v-1615398951',
        'hasPerk': False},
       {'id': '4f32572d19836c91c7ce2420',
        'name': 'A Better Place Restaurant',
        'location': {'address': '815 Superior Ave E',
         'lat': 41.50242233276367,
         'lng': -81.68932342529297,
         'labeledLatLngs': [{'label': 'display',
           'lat': 41.50242233276367,
           'lng': -81.68932342529297}],
         'distance': 459,
         'postalCode': '44114',
         'cc': 'US',
         'city': 'Cleveland',
         'state': 'OH',
         'country': 'United States',
         'formattedAddress': ['815 Superior Ave E', 'Cleveland, OH 44114']},
        'categories': [{'id': '4d4b7105d754a06374d81259',
          'name': 'Food',
          'pluralName': 'Food',
          'shortName': 'Food',
          'icon': {'prefix': 'https://ss3.4sqi.net/img/categories_v2/food/default_',
           'suffix': '.png'},
          'primary': True}],
        'referralId': 'v-1615398951',
        'hasPerk': False},
       {'id': '4f32291619836c91c7bc1f1c',
        'name': "Sergio's Italian Restaurant",
        'location': {'address': '526 Superior Ave E',
         'lat': 41.50080871582031,
         'lng': -81.6903305053711,
         'labeledLatLngs': [{'label': 'entrance',
           'lat': 41.500864,
           'lng': -81.690865},
          {'label': 'display',
           'lat': 41.50080871582031,
           'lng': -81.6903305053711}],
         'distance': 549,
         'postalCode': '44114',
         'cc': 'US',
         'city': 'Cleveland',
         'state': 'OH',
         'country': 'United States',
         'formattedAddress': ['526 Superior Ave E', 'Cleveland, OH 44114']},
        'categories': [{'id': '4bf58dd8d48988d110941735',
          'name': 'Italian Restaurant',
          'pluralName': 'Italian Restaurants',
          'shortName': 'Italian',
          'icon': {'prefix': 'https://ss3.4sqi.net/img/categories_v2/food/italian_',
           'suffix': '.png'},
          'primary': True}],
        'referralId': 'v-1615398951',
        'hasPerk': False},
       {'id': '4ad4bff2f964a520c2e920e3',
        'name': '1890 Restaurant & Lounge',
        'location': {'address': '420 Superior Ave E',
         'crossStreet': 'in Hyatt Regency Cleveland at The Arcade',
         'lat': 41.50063425179471,
         'lng': -81.6909366958338,
         'labeledLatLngs': [{'label': 'display',
           'lat': 41.50063425179471,
           'lng': -81.6909366958338}],
         'distance': 545,
         'postalCode': '44114',
         'cc': 'US',
         'city': 'Cleveland',
         'state': 'OH',
         'country': 'United States',
         'formattedAddress': ['420 Superior Ave E (in Hyatt Regency Cleveland at The Arcade)',
          'Cleveland, OH 44114']},
        'categories': [{'id': '4bf58dd8d48988d14e941735',
          'name': 'American Restaurant',
          'pluralName': 'American Restaurants',
          'shortName': 'American',
          'icon': {'prefix': 'https://ss3.4sqi.net/img/categories_v2/food/default_',
           'suffix': '.png'},
          'primary': True}],
        'venuePage': {'id': '47791445'},
        'referralId': 'v-1615398951',
        'hasPerk': False},
       {'id': '4f32b8c419836c91c7f33e96',
        'name': 'Sinergy Restaurant and Lounge',
        'location': {'address': '1213 W 6th St',
         'lat': 41.50114059448242,
         'lng': -81.69924926757812,
         'labeledLatLngs': [{'label': 'display',
           'lat': 41.50114059448242,
           'lng': -81.69924926757812}],
         'distance': 659,
         'postalCode': '44113',
         'cc': 'US',
         'city': 'Cleveland',
         'state': 'OH',
         'country': 'United States',
         'formattedAddress': ['1213 W 6th St', 'Cleveland, OH 44113']},
        'categories': [{'id': '4bf58dd8d48988d116941735',
          'name': 'Bar',
          'pluralName': 'Bars',
          'shortName': 'Bar',
          'icon': {'prefix': 'https://ss3.4sqi.net/img/categories_v2/nightlife/pub_',
           'suffix': '.png'},
          'primary': True}],
        'referralId': 'v-1615398951',
        'hasPerk': False},
       {'id': '4c335c2c16adc9287f78c39c',
        'name': "Addy's",
        'location': {'address': '99 W Saint Clair Ave',
         'lat': 41.5011825028896,
         'lng': -81.69548826892535,
         'labeledLatLngs': [{'label': 'display',
           'lat': 41.5011825028896,
           'lng': -81.69548826892535}],
         'distance': 474,
         'postalCode': '44113',
         'cc': 'US',
         'city': 'Cleveland',
         'state': 'OH',
         'country': 'United States',
         'formattedAddress': ['99 W Saint Clair Ave', 'Cleveland, OH 44113']},
        'categories': [{'id': '4bf58dd8d48988d14e941735',
          'name': 'American Restaurant',
          'pluralName': 'American Restaurants',
          'shortName': 'American',
          'icon': {'prefix': 'https://ss3.4sqi.net/img/categories_v2/food/default_',
           'suffix': '.png'},
          'primary': True}],
        'delivery': {'id': '1791840',
         'url': 'https://www.grubhub.com/restaurant/addys-restaurants-99-west-saint-clair-avenue-cleveland/1791840?affiliate=1131&utm_source=foursquare-affiliate-network&utm_medium=affiliate&utm_campaign=1131&utm_content=1791840',
         'provider': {'name': 'grubhub',
          'icon': {'prefix': 'https://fastly.4sqi.net/img/general/cap/',
           'sizes': [40, 50],
           'name': '/delivery_provider_grubhub_20180129.png'}}},
        'referralId': 'v-1615398951',
        'hasPerk': False},
       {'id': '4bd70960637ba593ba1ef970',
        'name': 'Sportsman',
        'location': {'address': '101 Saint Clair Ave NE',
         'lat': 41.50192642211914,
         'lng': -81.69501495361328,
         'labeledLatLngs': [{'label': 'display',
           'lat': 41.50192642211914,
           'lng': -81.69501495361328}],
         'distance': 383,
         'postalCode': '44114',
         'cc': 'US',
         'city': 'Cleveland',
         'state': 'OH',
         'country': 'United States',
         'formattedAddress': ['101 Saint Clair Ave NE', 'Cleveland, OH 44114']},
        'categories': [{'id': '4bf58dd8d48988d146941735',
          'name': 'Deli / Bodega',
          'pluralName': 'Delis / Bodegas',
          'shortName': 'Deli / Bodega',
          'icon': {'prefix': 'https://ss3.4sqi.net/img/categories_v2/food/deli_',
           'suffix': '.png'},
          'primary': True}],
        'referralId': 'v-1615398951',
        'hasPerk': False}]}}




```python
# assign relevant part of JSON to venues
venues = results['response']['venues']
dataframecle = pd.json_normalize(venues)
dataframecle.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>name</th>
      <th>categories</th>
      <th>referralId</th>
      <th>hasPerk</th>
      <th>location.address</th>
      <th>location.lat</th>
      <th>location.lng</th>
      <th>location.labeledLatLngs</th>
      <th>location.distance</th>
      <th>...</th>
      <th>location.country</th>
      <th>location.formattedAddress</th>
      <th>location.crossStreet</th>
      <th>venuePage.id</th>
      <th>delivery.id</th>
      <th>delivery.url</th>
      <th>delivery.provider.name</th>
      <th>delivery.provider.icon.prefix</th>
      <th>delivery.provider.icon.sizes</th>
      <th>delivery.provider.icon.name</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>5748cb02498e1c0c6cfa6584</td>
      <td>The Burnham Restaurant</td>
      <td>[{'id': '4bf58dd8d48988d157941735', 'name': 'N...</td>
      <td>v-1615398951</td>
      <td>False</td>
      <td>Hilton Cleveland Downtown</td>
      <td>41.502996</td>
      <td>-81.695876</td>
      <td>[{'label': 'display', 'lat': 41.50299558347314...</td>
      <td>315</td>
      <td>...</td>
      <td>United States</td>
      <td>[Hilton Cleveland Downtown, Cleveland, OH 44114]</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1</th>
      <td>4f32385b19836c91c7c1fbc6</td>
      <td>Mannys Cozy Corner Restaurant</td>
      <td>[{'id': '4d4b7105d754a06374d81259', 'name': 'F...</td>
      <td>v-1615398951</td>
      <td>False</td>
      <td>815 Superior Ave E</td>
      <td>41.502422</td>
      <td>-81.689323</td>
      <td>[{'label': 'display', 'lat': 41.50242233276367...</td>
      <td>459</td>
      <td>...</td>
      <td>United States</td>
      <td>[815 Superior Ave E, Cleveland, OH 44114]</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2</th>
      <td>4f32572d19836c91c7ce2420</td>
      <td>A Better Place Restaurant</td>
      <td>[{'id': '4d4b7105d754a06374d81259', 'name': 'F...</td>
      <td>v-1615398951</td>
      <td>False</td>
      <td>815 Superior Ave E</td>
      <td>41.502422</td>
      <td>-81.689323</td>
      <td>[{'label': 'display', 'lat': 41.50242233276367...</td>
      <td>459</td>
      <td>...</td>
      <td>United States</td>
      <td>[815 Superior Ave E, Cleveland, OH 44114]</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4f32291619836c91c7bc1f1c</td>
      <td>Sergio's Italian Restaurant</td>
      <td>[{'id': '4bf58dd8d48988d110941735', 'name': 'I...</td>
      <td>v-1615398951</td>
      <td>False</td>
      <td>526 Superior Ave E</td>
      <td>41.500809</td>
      <td>-81.690331</td>
      <td>[{'label': 'entrance', 'lat': 41.500864, 'lng'...</td>
      <td>549</td>
      <td>...</td>
      <td>United States</td>
      <td>[526 Superior Ave E, Cleveland, OH 44114]</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>4</th>
      <td>4ad4bff2f964a520c2e920e3</td>
      <td>1890 Restaurant &amp; Lounge</td>
      <td>[{'id': '4bf58dd8d48988d14e941735', 'name': 'A...</td>
      <td>v-1615398951</td>
      <td>False</td>
      <td>420 Superior Ave E</td>
      <td>41.500634</td>
      <td>-81.690937</td>
      <td>[{'label': 'display', 'lat': 41.50063425179471...</td>
      <td>545</td>
      <td>...</td>
      <td>United States</td>
      <td>[420 Superior Ave E (in Hyatt Regency Clevelan...</td>
      <td>in Hyatt Regency Cleveland at The Arcade</td>
      <td>47791445</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 24 columns</p>
</div>




```python
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
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>name</th>
      <th>categories</th>
      <th>address</th>
      <th>lat</th>
      <th>lng</th>
      <th>labeledLatLngs</th>
      <th>distance</th>
      <th>postalCode</th>
      <th>cc</th>
      <th>city</th>
      <th>state</th>
      <th>country</th>
      <th>formattedAddress</th>
      <th>crossStreet</th>
      <th>id</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>The Burnham Restaurant</td>
      <td>New American Restaurant</td>
      <td>Hilton Cleveland Downtown</td>
      <td>41.502996</td>
      <td>-81.695876</td>
      <td>[{'label': 'display', 'lat': 41.50299558347314...</td>
      <td>315</td>
      <td>44114</td>
      <td>US</td>
      <td>Cleveland</td>
      <td>OH</td>
      <td>United States</td>
      <td>[Hilton Cleveland Downtown, Cleveland, OH 44114]</td>
      <td>NaN</td>
      <td>5748cb02498e1c0c6cfa6584</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Mannys Cozy Corner Restaurant</td>
      <td>Food</td>
      <td>815 Superior Ave E</td>
      <td>41.502422</td>
      <td>-81.689323</td>
      <td>[{'label': 'display', 'lat': 41.50242233276367...</td>
      <td>459</td>
      <td>44114</td>
      <td>US</td>
      <td>Cleveland</td>
      <td>OH</td>
      <td>United States</td>
      <td>[815 Superior Ave E, Cleveland, OH 44114]</td>
      <td>NaN</td>
      <td>4f32385b19836c91c7c1fbc6</td>
    </tr>
    <tr>
      <th>2</th>
      <td>A Better Place Restaurant</td>
      <td>Food</td>
      <td>815 Superior Ave E</td>
      <td>41.502422</td>
      <td>-81.689323</td>
      <td>[{'label': 'display', 'lat': 41.50242233276367...</td>
      <td>459</td>
      <td>44114</td>
      <td>US</td>
      <td>Cleveland</td>
      <td>OH</td>
      <td>United States</td>
      <td>[815 Superior Ave E, Cleveland, OH 44114]</td>
      <td>NaN</td>
      <td>4f32572d19836c91c7ce2420</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Sergio's Italian Restaurant</td>
      <td>Italian Restaurant</td>
      <td>526 Superior Ave E</td>
      <td>41.500809</td>
      <td>-81.690331</td>
      <td>[{'label': 'entrance', 'lat': 41.500864, 'lng'...</td>
      <td>549</td>
      <td>44114</td>
      <td>US</td>
      <td>Cleveland</td>
      <td>OH</td>
      <td>United States</td>
      <td>[526 Superior Ave E, Cleveland, OH 44114]</td>
      <td>NaN</td>
      <td>4f32291619836c91c7bc1f1c</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1890 Restaurant &amp; Lounge</td>
      <td>American Restaurant</td>
      <td>420 Superior Ave E</td>
      <td>41.500634</td>
      <td>-81.690937</td>
      <td>[{'label': 'display', 'lat': 41.50063425179471...</td>
      <td>545</td>
      <td>44114</td>
      <td>US</td>
      <td>Cleveland</td>
      <td>OH</td>
      <td>United States</td>
      <td>[420 Superior Ave E (in Hyatt Regency Clevelan...</td>
      <td>in Hyatt Regency Cleveland at The Arcade</td>
      <td>4ad4bff2f964a520c2e920e3</td>
    </tr>
  </tbody>
</table>
</div>




```python
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
```




<div style="width:100%;"><div style="position:relative;width:100%;height:0;padding-bottom:60%;"><span style="color:#565656">Make this Notebook Trusted to load map: File -> Trust Notebook</span><iframe src="about:blank" style="position:absolute;width:100%;height:100%;left:0;top:0;border:none !important;" data-html=%3C%21DOCTYPE%20html%3E%0A%3Chead%3E%20%20%20%20%0A%20%20%20%20%3Cmeta%20http-equiv%3D%22content-type%22%20content%3D%22text/html%3B%20charset%3DUTF-8%22%20/%3E%0A%20%20%20%20%3Cscript%3EL_PREFER_CANVAS%20%3D%20false%3B%20L_NO_TOUCH%20%3D%20false%3B%20L_DISABLE_3D%20%3D%20false%3B%3C/script%3E%0A%20%20%20%20%3Cscript%20src%3D%22https%3A//cdn.jsdelivr.net/npm/leaflet%401.2.0/dist/leaflet.js%22%3E%3C/script%3E%0A%20%20%20%20%3Cscript%20src%3D%22https%3A//ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js%22%3E%3C/script%3E%0A%20%20%20%20%3Cscript%20src%3D%22https%3A//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js%22%3E%3C/script%3E%0A%20%20%20%20%3Cscript%20src%3D%22https%3A//cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.js%22%3E%3C/script%3E%0A%20%20%20%20%3Clink%20rel%3D%22stylesheet%22%20href%3D%22https%3A//cdn.jsdelivr.net/npm/leaflet%401.2.0/dist/leaflet.css%22/%3E%0A%20%20%20%20%3Clink%20rel%3D%22stylesheet%22%20href%3D%22https%3A//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css%22/%3E%0A%20%20%20%20%3Clink%20rel%3D%22stylesheet%22%20href%3D%22https%3A//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap-theme.min.css%22/%3E%0A%20%20%20%20%3Clink%20rel%3D%22stylesheet%22%20href%3D%22https%3A//maxcdn.bootstrapcdn.com/font-awesome/4.6.3/css/font-awesome.min.css%22/%3E%0A%20%20%20%20%3Clink%20rel%3D%22stylesheet%22%20href%3D%22https%3A//cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.css%22/%3E%0A%20%20%20%20%3Clink%20rel%3D%22stylesheet%22%20href%3D%22https%3A//rawgit.com/python-visualization/folium/master/folium/templates/leaflet.awesome.rotate.css%22/%3E%0A%20%20%20%20%3Cstyle%3Ehtml%2C%20body%20%7Bwidth%3A%20100%25%3Bheight%3A%20100%25%3Bmargin%3A%200%3Bpadding%3A%200%3B%7D%3C/style%3E%0A%20%20%20%20%3Cstyle%3E%23map%20%7Bposition%3Aabsolute%3Btop%3A0%3Bbottom%3A0%3Bright%3A0%3Bleft%3A0%3B%7D%3C/style%3E%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%3Cstyle%3E%20%23map_d1cf053ce0704e23919d043768e391e1%20%7B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20position%20%3A%20relative%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20width%20%3A%20100.0%25%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20height%3A%20100.0%25%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20left%3A%200.0%25%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20top%3A%200.0%25%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%3C/style%3E%0A%20%20%20%20%20%20%20%20%0A%3C/head%3E%0A%3Cbody%3E%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%3Cdiv%20class%3D%22folium-map%22%20id%3D%22map_d1cf053ce0704e23919d043768e391e1%22%20%3E%3C/div%3E%0A%20%20%20%20%20%20%20%20%0A%3C/body%3E%0A%3Cscript%3E%20%20%20%20%0A%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20bounds%20%3D%20null%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20map_d1cf053ce0704e23919d043768e391e1%20%3D%20L.map%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%27map_d1cf053ce0704e23919d043768e391e1%27%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7Bcenter%3A%20%5B41.5051613%2C-81.6934446%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20zoom%3A%2015%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20maxBounds%3A%20bounds%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20layers%3A%20%5B%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20worldCopyJump%3A%20false%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20crs%3A%20L.CRS.EPSG3857%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7D%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20tile_layer_d7997e4f778546a0ae6965e417c16b13%20%3D%20L.tileLayer%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%27https%3A//%7Bs%7D.tile.openstreetmap.org/%7Bz%7D/%7Bx%7D/%7By%7D.png%27%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22attribution%22%3A%20null%2C%0A%20%20%22detectRetina%22%3A%20false%2C%0A%20%20%22maxZoom%22%3A%2018%2C%0A%20%20%22minZoom%22%3A%201%2C%0A%20%20%22noWrap%22%3A%20false%2C%0A%20%20%22subdomains%22%3A%20%22abc%22%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_d1cf053ce0704e23919d043768e391e1%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_8ec693f2808f4064a85c383064202da5%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B41.5051613%2C-81.6934446%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22red%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22red%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%2010%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_d1cf053ce0704e23919d043768e391e1%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_408adc74ab994931a15c1e3848570415%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_19c8f7ef727f4750a109e989b4fbee4e%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_19c8f7ef727f4750a109e989b4fbee4e%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EConrad%20Hotel%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_408adc74ab994931a15c1e3848570415.setContent%28html_19c8f7ef727f4750a109e989b4fbee4e%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_8ec693f2808f4064a85c383064202da5.bindPopup%28popup_408adc74ab994931a15c1e3848570415%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_0c75161809a445ce96a632fc7ff5d658%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B41.50299558347314%2C-81.69587648445662%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_d1cf053ce0704e23919d043768e391e1%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_e3a262b223994b7d81a4d760eb296878%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_bf14739202274399a13aa076a592aacb%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_bf14739202274399a13aa076a592aacb%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ENew%20American%20Restaurant%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_e3a262b223994b7d81a4d760eb296878.setContent%28html_bf14739202274399a13aa076a592aacb%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_0c75161809a445ce96a632fc7ff5d658.bindPopup%28popup_e3a262b223994b7d81a4d760eb296878%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_b2931ce52b5d419f99db973121c3adf0%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B41.50242233276367%2C-81.68932342529297%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_d1cf053ce0704e23919d043768e391e1%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_1bb74446d0f24c718b99c880d6ede2ff%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_cfbc941ce41e4fbb9ede5920843c80eb%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_cfbc941ce41e4fbb9ede5920843c80eb%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EFood%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_1bb74446d0f24c718b99c880d6ede2ff.setContent%28html_cfbc941ce41e4fbb9ede5920843c80eb%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_b2931ce52b5d419f99db973121c3adf0.bindPopup%28popup_1bb74446d0f24c718b99c880d6ede2ff%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_d66ca9da156941f8b98620a8f829c5ea%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B41.50242233276367%2C-81.68932342529297%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_d1cf053ce0704e23919d043768e391e1%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_27378f951b84481a9b16174ae00dae8f%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_1f6359e3450142d9b683ede4c13f659e%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_1f6359e3450142d9b683ede4c13f659e%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EFood%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_27378f951b84481a9b16174ae00dae8f.setContent%28html_1f6359e3450142d9b683ede4c13f659e%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_d66ca9da156941f8b98620a8f829c5ea.bindPopup%28popup_27378f951b84481a9b16174ae00dae8f%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_76964e0cfc5a4e5aad4c2b7d016a7b6f%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B41.50080871582031%2C-81.6903305053711%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_d1cf053ce0704e23919d043768e391e1%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_062b279aa5214219909ba4fefb52b8e0%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_2f1973cba7ee4c728e773bf815b232a3%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_2f1973cba7ee4c728e773bf815b232a3%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EItalian%20Restaurant%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_062b279aa5214219909ba4fefb52b8e0.setContent%28html_2f1973cba7ee4c728e773bf815b232a3%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_76964e0cfc5a4e5aad4c2b7d016a7b6f.bindPopup%28popup_062b279aa5214219909ba4fefb52b8e0%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_2cb8efeee0964bf28a93ef8b7459ca61%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B41.50063425179471%2C-81.6909366958338%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_d1cf053ce0704e23919d043768e391e1%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_dc55451a9ffe43c8b1ac8bd777906b81%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_f43680e3455d433b8a210d6af4616eba%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_f43680e3455d433b8a210d6af4616eba%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EAmerican%20Restaurant%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_dc55451a9ffe43c8b1ac8bd777906b81.setContent%28html_f43680e3455d433b8a210d6af4616eba%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_2cb8efeee0964bf28a93ef8b7459ca61.bindPopup%28popup_dc55451a9ffe43c8b1ac8bd777906b81%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_aaab93af0bb043d5828678486518357d%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B41.50114059448242%2C-81.69924926757812%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_d1cf053ce0704e23919d043768e391e1%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_8717d915028049f8b0d38d9e9123b489%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_f4e1d6c5cda94d559d187e83d8fa1e6b%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_f4e1d6c5cda94d559d187e83d8fa1e6b%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EBar%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_8717d915028049f8b0d38d9e9123b489.setContent%28html_f4e1d6c5cda94d559d187e83d8fa1e6b%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_aaab93af0bb043d5828678486518357d.bindPopup%28popup_8717d915028049f8b0d38d9e9123b489%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_32b351db8d154ab4ba3cedd8382177fc%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B41.5011825028896%2C-81.69548826892535%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_d1cf053ce0704e23919d043768e391e1%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_1f246011c143474eae66283d106c1f36%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_80f0b1647ebd4eafa6d81638db8410b7%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_80f0b1647ebd4eafa6d81638db8410b7%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EAmerican%20Restaurant%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_1f246011c143474eae66283d106c1f36.setContent%28html_80f0b1647ebd4eafa6d81638db8410b7%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_32b351db8d154ab4ba3cedd8382177fc.bindPopup%28popup_1f246011c143474eae66283d106c1f36%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_bfc80ca64bda4457baa7e99350e8c867%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B41.50192642211914%2C-81.69501495361328%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_d1cf053ce0704e23919d043768e391e1%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_8186a7e37cd443288d1eb4e6b9b10261%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_871acb6ec6754018bec5dbfcede3671f%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_871acb6ec6754018bec5dbfcede3671f%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EDeli%20/%20Bodega%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_8186a7e37cd443288d1eb4e6b9b10261.setContent%28html_871acb6ec6754018bec5dbfcede3671f%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_bfc80ca64bda4457baa7e99350e8c867.bindPopup%28popup_8186a7e37cd443288d1eb4e6b9b10261%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%3C/script%3E onload="this.contentDocument.open();this.contentDocument.write(    decodeURIComponent(this.getAttribute('data-html')));this.contentDocument.close();" allowfullscreen webkitallowfullscreen mozallowfullscreen></iframe></div></div>




```python
url = 'https://api.foursquare.com/v2/venues/explore?client_id={}&client_secret={}&ll={},{}&v={}&radius={}&limit={}'.format(CLIENT_ID, CLIENT_SECRET, latitude, longitude, VERSION, radius, LIMIT)
url
```




    'https://api.foursquare.com/v2/venues/explore?client_id=ZRS2NV2A04VQZNFID0INKRS00YCZCTYVMVDFIR1L4FX5ZVIG&client_secret=PRK2N423NAEOOKKKTL5EL4LLRJ2A4SJJYFJU2V55QT5WRMOQ&ll=41.5051613,-81.6934446&v=20180604&radius=500&limit=30'




```python
import requests
```


```python
results = requests.get(url).json()
'There are {} around Cleveland, Ohio.'.format(len(results['response']['groups'][0]['items']))
```




    'There are 30 around Cleveland, Ohio.'




```python
items = results['response']['groups'][0]['items']
items[0]
```




    {'reasons': {'count': 0,
      'items': [{'summary': 'This spot is popular',
        'type': 'general',
        'reasonName': 'globalInteractionReason'}]},
     'venue': {'id': '5346a9d0498e296984404d80',
      'name': 'Urban Farmer',
      'location': {'address': '1325 E 6th St',
       'crossStreet': 'at Saint Clair Ave NE',
       'lat': 41.50325156560989,
       'lng': -81.69166061424355,
       'labeledLatLngs': [{'label': 'display',
         'lat': 41.50325156560989,
         'lng': -81.69166061424355}],
       'distance': 259,
       'postalCode': '44114',
       'cc': 'US',
       'city': 'Cleveland',
       'state': 'OH',
       'country': 'United States',
       'formattedAddress': ['1325 E 6th St (at Saint Clair Ave NE)',
        'Cleveland, OH 44114',
        'United States']},
      'categories': [{'id': '4bf58dd8d48988d1cc941735',
        'name': 'Steakhouse',
        'pluralName': 'Steakhouses',
        'shortName': 'Steakhouse',
        'icon': {'prefix': 'https://ss3.4sqi.net/img/categories_v2/food/steakhouse_',
         'suffix': '.png'},
        'primary': True}],
      'delivery': {'id': '1053646',
       'url': 'https://www.grubhub.com/restaurant/urban-farmer-1325-e-6th-st-cleveland/1053646?affiliate=1131&utm_source=foursquare-affiliate-network&utm_medium=affiliate&utm_campaign=1131&utm_content=1053646',
       'provider': {'name': 'grubhub',
        'icon': {'prefix': 'https://fastly.4sqi.net/img/general/cap/',
         'sizes': [40, 50],
         'name': '/delivery_provider_grubhub_20180129.png'}}},
      'photos': {'count': 0, 'groups': []},
      'venuePage': {'id': '83995899'}},
     'referralId': 'e-0-5346a9d0498e296984404d80-0'}




```python
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
```

    <ipython-input-266-f430039d5843>:1: FutureWarning: pandas.io.json.json_normalize is deprecated, use pandas.json_normalize instead
      dataframe = json_normalize(items) # flatten JSON
    




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>name</th>
      <th>categories</th>
      <th>address</th>
      <th>crossStreet</th>
      <th>lat</th>
      <th>lng</th>
      <th>labeledLatLngs</th>
      <th>distance</th>
      <th>postalCode</th>
      <th>cc</th>
      <th>city</th>
      <th>state</th>
      <th>country</th>
      <th>formattedAddress</th>
      <th>neighborhood</th>
      <th>id</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Urban Farmer</td>
      <td>Steakhouse</td>
      <td>1325 E 6th St</td>
      <td>at Saint Clair Ave NE</td>
      <td>41.503252</td>
      <td>-81.691661</td>
      <td>[{'label': 'display', 'lat': 41.50325156560989...</td>
      <td>259</td>
      <td>44114</td>
      <td>US</td>
      <td>Cleveland</td>
      <td>OH</td>
      <td>United States</td>
      <td>[1325 E 6th St (at Saint Clair Ave NE), Clevel...</td>
      <td>NaN</td>
      <td>5346a9d0498e296984404d80</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Mall B</td>
      <td>Park</td>
      <td>Saint Clair Avenue</td>
      <td>btw E &amp; W Mall Drives</td>
      <td>41.502984</td>
      <td>-81.694149</td>
      <td>[{'label': 'display', 'lat': 41.502984, 'lng':...</td>
      <td>249</td>
      <td>44114</td>
      <td>US</td>
      <td>Cleveland</td>
      <td>OH</td>
      <td>United States</td>
      <td>[Saint Clair Avenue (btw E &amp; W Mall Drives), C...</td>
      <td>NaN</td>
      <td>4c746740d8948cfa5d0a65da</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Free Stamp by Claes Oldenburg &amp; Coosje van Bru...</td>
      <td>Public Art</td>
      <td>Willard Park</td>
      <td>NaN</td>
      <td>41.505412</td>
      <td>-81.692501</td>
      <td>[{'label': 'display', 'lat': 41.50541168268271...</td>
      <td>83</td>
      <td>44114</td>
      <td>US</td>
      <td>Cleveland</td>
      <td>OH</td>
      <td>United States</td>
      <td>[Willard Park, Cleveland, OH 44114, United Sta...</td>
      <td>NaN</td>
      <td>4c1c3d73b9f876b05fb57b46</td>
    </tr>
    <tr>
      <th>3</th>
      <td>The Westin Cleveland Downtown</td>
      <td>Hotel</td>
      <td>777 Saint Clair Ave NE</td>
      <td>at E 6th St</td>
      <td>41.503725</td>
      <td>-81.691413</td>
      <td>[{'label': 'display', 'lat': 41.5037247, 'lng'...</td>
      <td>232</td>
      <td>44114</td>
      <td>US</td>
      <td>Cleveland</td>
      <td>OH</td>
      <td>United States</td>
      <td>[777 Saint Clair Ave NE (at E 6th St), Clevela...</td>
      <td>NaN</td>
      <td>5124f21e80551995afc1e135</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Willard Park</td>
      <td>Park</td>
      <td>E 9th St &amp; Lakeside Ave E</td>
      <td>NaN</td>
      <td>41.505621</td>
      <td>-81.692276</td>
      <td>[{'label': 'display', 'lat': 41.50562058588829...</td>
      <td>110</td>
      <td>44114</td>
      <td>US</td>
      <td>Cleveland</td>
      <td>OH</td>
      <td>United States</td>
      <td>[E 9th St &amp; Lakeside Ave E, Cleveland, OH 4411...</td>
      <td>NaN</td>
      <td>4bdeffb1e75c0f47ad8cc903</td>
    </tr>
  </tbody>
</table>
</div>




```python
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
```




<div style="width:100%;"><div style="position:relative;width:100%;height:0;padding-bottom:60%;"><span style="color:#565656">Make this Notebook Trusted to load map: File -> Trust Notebook</span><iframe src="about:blank" style="position:absolute;width:100%;height:100%;left:0;top:0;border:none !important;" data-html=%3C%21DOCTYPE%20html%3E%0A%3Chead%3E%20%20%20%20%0A%20%20%20%20%3Cmeta%20http-equiv%3D%22content-type%22%20content%3D%22text/html%3B%20charset%3DUTF-8%22%20/%3E%0A%20%20%20%20%3Cscript%3EL_PREFER_CANVAS%20%3D%20false%3B%20L_NO_TOUCH%20%3D%20false%3B%20L_DISABLE_3D%20%3D%20false%3B%3C/script%3E%0A%20%20%20%20%3Cscript%20src%3D%22https%3A//cdn.jsdelivr.net/npm/leaflet%401.2.0/dist/leaflet.js%22%3E%3C/script%3E%0A%20%20%20%20%3Cscript%20src%3D%22https%3A//ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js%22%3E%3C/script%3E%0A%20%20%20%20%3Cscript%20src%3D%22https%3A//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js%22%3E%3C/script%3E%0A%20%20%20%20%3Cscript%20src%3D%22https%3A//cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.js%22%3E%3C/script%3E%0A%20%20%20%20%3Clink%20rel%3D%22stylesheet%22%20href%3D%22https%3A//cdn.jsdelivr.net/npm/leaflet%401.2.0/dist/leaflet.css%22/%3E%0A%20%20%20%20%3Clink%20rel%3D%22stylesheet%22%20href%3D%22https%3A//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css%22/%3E%0A%20%20%20%20%3Clink%20rel%3D%22stylesheet%22%20href%3D%22https%3A//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap-theme.min.css%22/%3E%0A%20%20%20%20%3Clink%20rel%3D%22stylesheet%22%20href%3D%22https%3A//maxcdn.bootstrapcdn.com/font-awesome/4.6.3/css/font-awesome.min.css%22/%3E%0A%20%20%20%20%3Clink%20rel%3D%22stylesheet%22%20href%3D%22https%3A//cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.css%22/%3E%0A%20%20%20%20%3Clink%20rel%3D%22stylesheet%22%20href%3D%22https%3A//rawgit.com/python-visualization/folium/master/folium/templates/leaflet.awesome.rotate.css%22/%3E%0A%20%20%20%20%3Cstyle%3Ehtml%2C%20body%20%7Bwidth%3A%20100%25%3Bheight%3A%20100%25%3Bmargin%3A%200%3Bpadding%3A%200%3B%7D%3C/style%3E%0A%20%20%20%20%3Cstyle%3E%23map%20%7Bposition%3Aabsolute%3Btop%3A0%3Bbottom%3A0%3Bright%3A0%3Bleft%3A0%3B%7D%3C/style%3E%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%3Cstyle%3E%20%23map_77a710de7f9d4e47af82867901aec818%20%7B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20position%20%3A%20relative%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20width%20%3A%20100.0%25%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20height%3A%20100.0%25%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20left%3A%200.0%25%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20top%3A%200.0%25%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%3C/style%3E%0A%20%20%20%20%20%20%20%20%0A%3C/head%3E%0A%3Cbody%3E%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%3Cdiv%20class%3D%22folium-map%22%20id%3D%22map_77a710de7f9d4e47af82867901aec818%22%20%3E%3C/div%3E%0A%20%20%20%20%20%20%20%20%0A%3C/body%3E%0A%3Cscript%3E%20%20%20%20%0A%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20bounds%20%3D%20null%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20map_77a710de7f9d4e47af82867901aec818%20%3D%20L.map%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%27map_77a710de7f9d4e47af82867901aec818%27%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7Bcenter%3A%20%5B41.5051613%2C-81.6934446%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20zoom%3A%2015%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20maxBounds%3A%20bounds%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20layers%3A%20%5B%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20worldCopyJump%3A%20false%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20crs%3A%20L.CRS.EPSG3857%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7D%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20tile_layer_4756cda806244953b1571d67e2b01f33%20%3D%20L.tileLayer%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%27https%3A//%7Bs%7D.tile.openstreetmap.org/%7Bz%7D/%7Bx%7D/%7By%7D.png%27%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22attribution%22%3A%20null%2C%0A%20%20%22detectRetina%22%3A%20false%2C%0A%20%20%22maxZoom%22%3A%2018%2C%0A%20%20%22minZoom%22%3A%201%2C%0A%20%20%22noWrap%22%3A%20false%2C%0A%20%20%22subdomains%22%3A%20%22abc%22%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_77a710de7f9d4e47af82867901aec818%29%3B%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_c820d08d90284e51b83e2b3a273945c0%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B41.5051613%2C-81.6934446%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22red%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22red%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%2010%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_77a710de7f9d4e47af82867901aec818%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_73ca0c0d92bc4bc4b096f809dbe17249%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_734eb92fde5b41469908bbedcc2d5ae2%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_734eb92fde5b41469908bbedcc2d5ae2%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EEcco%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_73ca0c0d92bc4bc4b096f809dbe17249.setContent%28html_734eb92fde5b41469908bbedcc2d5ae2%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_c820d08d90284e51b83e2b3a273945c0.bindPopup%28popup_73ca0c0d92bc4bc4b096f809dbe17249%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_8a0abba8b4b947b4b08e5feccb09bf30%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B41.50325156560989%2C-81.69166061424355%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_77a710de7f9d4e47af82867901aec818%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_01510b730cea450e96b3d7162970d1c5%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_93c8857c9fc9409ba6d59ec8850b9dc8%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_93c8857c9fc9409ba6d59ec8850b9dc8%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ESteakhouse%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_01510b730cea450e96b3d7162970d1c5.setContent%28html_93c8857c9fc9409ba6d59ec8850b9dc8%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_8a0abba8b4b947b4b08e5feccb09bf30.bindPopup%28popup_01510b730cea450e96b3d7162970d1c5%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_604592ce951d41e4aa7b4ba54d71eb5c%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B41.502984%2C-81.694149%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_77a710de7f9d4e47af82867901aec818%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_91741c93683e416384104c3ee47b10cd%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_df6dbdc60fb941c09074ebc7e188d768%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_df6dbdc60fb941c09074ebc7e188d768%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EPark%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_91741c93683e416384104c3ee47b10cd.setContent%28html_df6dbdc60fb941c09074ebc7e188d768%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_604592ce951d41e4aa7b4ba54d71eb5c.bindPopup%28popup_91741c93683e416384104c3ee47b10cd%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_5aca49b9ddd04db098298b7a7a87f7fd%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B41.50541168268271%2C-81.6925013065338%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_77a710de7f9d4e47af82867901aec818%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_1334ca62d8374b61aaa4d7a6f1d22164%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_beccbb0b80354e8b8be26c072e23e2b3%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_beccbb0b80354e8b8be26c072e23e2b3%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EPublic%20Art%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_1334ca62d8374b61aaa4d7a6f1d22164.setContent%28html_beccbb0b80354e8b8be26c072e23e2b3%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_5aca49b9ddd04db098298b7a7a87f7fd.bindPopup%28popup_1334ca62d8374b61aaa4d7a6f1d22164%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_76071ef2e8644c4f8ef5c314a24956e6%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B41.5037247%2C-81.6914126%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_77a710de7f9d4e47af82867901aec818%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_ae623f4927004461a1866ae9254a1e65%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_c378e48f57cd4ffdadd4cf3f4b9088e9%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_c378e48f57cd4ffdadd4cf3f4b9088e9%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EHotel%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_ae623f4927004461a1866ae9254a1e65.setContent%28html_c378e48f57cd4ffdadd4cf3f4b9088e9%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_76071ef2e8644c4f8ef5c314a24956e6.bindPopup%28popup_ae623f4927004461a1866ae9254a1e65%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_49a229816d2b46caa5fffee1fac1d806%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B41.505620585888295%2C-81.69227600097656%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_77a710de7f9d4e47af82867901aec818%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_90d6854e7aac469baba3c4dfa730c366%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_561474aada1c49c2bebb1873b3e6b88a%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_561474aada1c49c2bebb1873b3e6b88a%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EPark%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_90d6854e7aac469baba3c4dfa730c366.setContent%28html_561474aada1c49c2bebb1873b3e6b88a%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_49a229816d2b46caa5fffee1fac1d806.bindPopup%28popup_90d6854e7aac469baba3c4dfa730c366%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_30c195cd37d3499a98169874c2d55781%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B41.5027085%2C-81.6960105%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_77a710de7f9d4e47af82867901aec818%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_24d61b4d877f4b599a487615b859fc0c%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_ec265a47b8d14465b126a2efb6985dad%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_ec265a47b8d14465b126a2efb6985dad%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EHotel%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_24d61b4d877f4b599a487615b859fc0c.setContent%28html_ec265a47b8d14465b126a2efb6985dad%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_30c195cd37d3499a98169874c2d55781.bindPopup%28popup_24d61b4d877f4b599a487615b859fc0c%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_125d6de347c345dcae95db111c118652%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B41.50360945077006%2C-81.69288436682916%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_77a710de7f9d4e47af82867901aec818%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_a6f1ae401f9445afa878f8f7fce15e13%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_2330aed08610474d855aff0471abaab4%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_2330aed08610474d855aff0471abaab4%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EAuditorium%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_a6f1ae401f9445afa878f8f7fce15e13.setContent%28html_2330aed08610474d855aff0471abaab4%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_125d6de347c345dcae95db111c118652.bindPopup%28popup_a6f1ae401f9445afa878f8f7fce15e13%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_58781347b5044a18a4418e7984c34f12%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B41.50452821360203%2C-81.68970254426124%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_77a710de7f9d4e47af82867901aec818%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_7b522c44720843028fb37c4d54dc3d65%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_286ab3a99e784939b02443656500750a%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_286ab3a99e784939b02443656500750a%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EGym%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_7b522c44720843028fb37c4d54dc3d65.setContent%28html_286ab3a99e784939b02443656500750a%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_58781347b5044a18a4418e7984c34f12.bindPopup%28popup_7b522c44720843028fb37c4d54dc3d65%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_c57dffaed82e479ba898db1c98b1e250%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B41.50743239118702%2C-81.69666945934296%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_77a710de7f9d4e47af82867901aec818%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_2c4d0c6185bb46aebe4608f20b2f27ae%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_112c55b2bfd84d8b9ee97b6487259f4c%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_112c55b2bfd84d8b9ee97b6487259f4c%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EScience%20Museum%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_2c4d0c6185bb46aebe4608f20b2f27ae.setContent%28html_112c55b2bfd84d8b9ee97b6487259f4c%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_c57dffaed82e479ba898db1c98b1e250.bindPopup%28popup_2c4d0c6185bb46aebe4608f20b2f27ae%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_c50fa5ea158a4d04a67b308e61d8d1bc%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B41.50836425030443%2C-81.69499080157769%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_77a710de7f9d4e47af82867901aec818%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_9333a785574844358e6f70365b8c08f6%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_03cdb613c9054c439af635b628c3af39%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_03cdb613c9054c439af635b628c3af39%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EMuseum%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_9333a785574844358e6f70365b8c08f6.setContent%28html_03cdb613c9054c439af635b628c3af39%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_c50fa5ea158a4d04a67b308e61d8d1bc.bindPopup%28popup_9333a785574844358e6f70365b8c08f6%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_15799146c9304ed4ad201569bf25600b%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B41.50735405475603%2C-81.69609144330025%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_77a710de7f9d4e47af82867901aec818%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_15bba8423c87485488286a20aae456e7%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_33c6754d947948db9890affc185345ad%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_33c6754d947948db9890affc185345ad%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EMovie%20Theater%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_15bba8423c87485488286a20aae456e7.setContent%28html_33c6754d947948db9890affc185345ad%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_15799146c9304ed4ad201569bf25600b.bindPopup%28popup_15bba8423c87485488286a20aae456e7%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_8b3a3e10fe5746ee84f198c83542cbc3%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B41.50340778674893%2C-81.69137582988586%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_77a710de7f9d4e47af82867901aec818%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_bc62f1e8ee2949adadf4dba49fb18554%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_7685aed2242947fb9998e419fbb46acf%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_7685aed2242947fb9998e419fbb46acf%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ECoffee%20Shop%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_bc62f1e8ee2949adadf4dba49fb18554.setContent%28html_7685aed2242947fb9998e419fbb46acf%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_8b3a3e10fe5746ee84f198c83542cbc3.bindPopup%28popup_bc62f1e8ee2949adadf4dba49fb18554%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_5c99b70214524a1e88d5e187d608541f%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B41.503816316752705%2C-81.6900358047267%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_77a710de7f9d4e47af82867901aec818%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_86c8c7e8290f43f19fe11d00eefc5837%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_b7215cf6e8fe4e81b474061cd21f7dd2%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_b7215cf6e8fe4e81b474061cd21f7dd2%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ECaf%C3%A9%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_86c8c7e8290f43f19fe11d00eefc5837.setContent%28html_b7215cf6e8fe4e81b474061cd21f7dd2%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_5c99b70214524a1e88d5e187d608541f.bindPopup%28popup_86c8c7e8290f43f19fe11d00eefc5837%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_276d872af5de4fdcb269c3a02013906a%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B41.50457606312036%2C-81.68998003005981%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_77a710de7f9d4e47af82867901aec818%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_bc0cf4d88f5d40df8f70e018cb7703ba%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_55b864aafdd64727b3f9dfbd11f790f1%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_55b864aafdd64727b3f9dfbd11f790f1%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EWings%20Joint%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_bc0cf4d88f5d40df8f70e018cb7703ba.setContent%28html_55b864aafdd64727b3f9dfbd11f790f1%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_276d872af5de4fdcb269c3a02013906a.bindPopup%28popup_bc0cf4d88f5d40df8f70e018cb7703ba%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_a21b7615a3a24f1d8af6ee6ca4e8d5e7%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B41.50317715847862%2C-81.69552429616404%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_77a710de7f9d4e47af82867901aec818%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_4404881ed3b645f684e2dae0577f5bcb%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_69f3f67472ca4a3a9d3763d4d749ff43%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_69f3f67472ca4a3a9d3763d4d749ff43%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EHotel%20Bar%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_4404881ed3b645f684e2dae0577f5bcb.setContent%28html_69f3f67472ca4a3a9d3763d4d749ff43%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_a21b7615a3a24f1d8af6ee6ca4e8d5e7.bindPopup%28popup_4404881ed3b645f684e2dae0577f5bcb%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_c49a9e9d84774f1599ba6f146e754338%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B41.503621792841045%2C-81.68975915092742%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_77a710de7f9d4e47af82867901aec818%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_c244cd7333744bd68021063c25e97efb%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_6b2eb8bd405343e481a793953989ca1b%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_6b2eb8bd405343e481a793953989ca1b%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ECaf%C3%A9%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_c244cd7333744bd68021063c25e97efb.setContent%28html_6b2eb8bd405343e481a793953989ca1b%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_c49a9e9d84774f1599ba6f146e754338.bindPopup%28popup_c244cd7333744bd68021063c25e97efb%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_9f9618c883df4224b6d7ce552ee5e9c7%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B41.50167943298645%2C-81.6929680109024%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_77a710de7f9d4e47af82867901aec818%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_83d5f80165ec42aca1477c216b2edbf4%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_93c4ecdd51384f65aa9a32fde3c63acd%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_93c4ecdd51384f65aa9a32fde3c63acd%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EFountain%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_83d5f80165ec42aca1477c216b2edbf4.setContent%28html_93c4ecdd51384f65aa9a32fde3c63acd%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_9f9618c883df4224b6d7ce552ee5e9c7.bindPopup%28popup_83d5f80165ec42aca1477c216b2edbf4%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_078b5f59f0d44063a2ca859151846cf6%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B41.502343650248775%2C-81.69178413606394%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_77a710de7f9d4e47af82867901aec818%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_80581406fc2c411f864da12c02aa61bb%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_524e3595caa747e08e0da6bd56ae6a04%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_524e3595caa747e08e0da6bd56ae6a04%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EHotel%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_80581406fc2c411f864da12c02aa61bb.setContent%28html_524e3595caa747e08e0da6bd56ae6a04%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_078b5f59f0d44063a2ca859151846cf6.bindPopup%28popup_80581406fc2c411f864da12c02aa61bb%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_9e01e1d8554d4075b6a880e1c0bfd9fa%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B41.505602258166746%2C-81.6985509807194%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_77a710de7f9d4e47af82867901aec818%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_0471675052c6418498e71acd1e0afaa3%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_e3f9af7be3374f23958a431dcc1b9ebd%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_e3f9af7be3374f23958a431dcc1b9ebd%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ESouvenir%20Shop%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_0471675052c6418498e71acd1e0afaa3.setContent%28html_e3f9af7be3374f23958a431dcc1b9ebd%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_9e01e1d8554d4075b6a880e1c0bfd9fa.bindPopup%28popup_0471675052c6418498e71acd1e0afaa3%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_37f4917b115d4a638212c31e26b19ada%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B41.501384%2C-81.6946462%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_77a710de7f9d4e47af82867901aec818%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_492a654b9e6c4b62969056b9b0255c83%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_bf04184081c24c679cb0b192fe3e1321%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_bf04184081c24c679cb0b192fe3e1321%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EHotel%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_492a654b9e6c4b62969056b9b0255c83.setContent%28html_bf04184081c24c679cb0b192fe3e1321%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_37f4917b115d4a638212c31e26b19ada.bindPopup%28popup_492a654b9e6c4b62969056b9b0255c83%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_c4952d88b0964fa793172c5862accd88%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B41.5048136%2C-81.6917545%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_77a710de7f9d4e47af82867901aec818%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_63183106ae70480e9578c46441235aaa%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_e608f08f65704718b17568da72c09bef%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_e608f08f65704718b17568da72c09bef%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ECredit%20Union%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_63183106ae70480e9578c46441235aaa.setContent%28html_e608f08f65704718b17568da72c09bef%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_c4952d88b0964fa793172c5862accd88.bindPopup%28popup_63183106ae70480e9578c46441235aaa%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_56bf5f68685b472aa4e29ecc71bf6f7f%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B41.50299693039093%2C-81.69597528352189%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_77a710de7f9d4e47af82867901aec818%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_b52945676c144e96bf7d986c312c2726%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_64ce7d2a1bab4a828b06d8ef27c1f859%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_64ce7d2a1bab4a828b06d8ef27c1f859%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EHotel%20Bar%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_b52945676c144e96bf7d986c312c2726.setContent%28html_64ce7d2a1bab4a828b06d8ef27c1f859%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_56bf5f68685b472aa4e29ecc71bf6f7f.bindPopup%28popup_b52945676c144e96bf7d986c312c2726%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_a71abb9d52d7442783d41a55a84c5a54%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B41.50190040101537%2C-81.69028043746948%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_77a710de7f9d4e47af82867901aec818%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_f2df4ca77ed3487fb9ee5f8f6565f27b%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_2efcb0e3ab7248508e8efaf9b68472b9%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_2efcb0e3ab7248508e8efaf9b68472b9%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EMuseum%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_f2df4ca77ed3487fb9ee5f8f6565f27b.setContent%28html_2efcb0e3ab7248508e8efaf9b68472b9%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_a71abb9d52d7442783d41a55a84c5a54.bindPopup%28popup_f2df4ca77ed3487fb9ee5f8f6565f27b%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_3d1cc004a45b4151815692535c6c5820%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B41.50334830782703%2C-81.68946512706903%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_77a710de7f9d4e47af82867901aec818%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_ffc4abd549044ec0b469bc3d0a5c00ff%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_61dd09ff049c41c49e4c29c0801015d0%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_61dd09ff049c41c49e4c29c0801015d0%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EPharmacy%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_ffc4abd549044ec0b469bc3d0a5c00ff.setContent%28html_61dd09ff049c41c49e4c29c0801015d0%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_3d1cc004a45b4151815692535c6c5820.bindPopup%28popup_ffc4abd549044ec0b469bc3d0a5c00ff%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_d29593189c194e2cb7bc5e4a93391a4e%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B41.50693826749729%2C-81.6898512840271%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_77a710de7f9d4e47af82867901aec818%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_74a6427cdc454a2aaa60b7af87d67d53%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_5318c9d4410a4883816cb9787edd457f%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_5318c9d4410a4883816cb9787edd457f%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ECoffee%20Shop%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_74a6427cdc454a2aaa60b7af87d67d53.setContent%28html_5318c9d4410a4883816cb9787edd457f%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_d29593189c194e2cb7bc5e4a93391a4e.bindPopup%28popup_74a6427cdc454a2aaa60b7af87d67d53%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_82b9b76a7b344ca7bd20131cbc8e35bc%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B41.501051316149486%2C-81.69118532385892%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_77a710de7f9d4e47af82867901aec818%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_d585bd6f9fcb47ada9b4ec2bff371e53%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_743a75c83b0444cfaf2039c23abe7517%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_743a75c83b0444cfaf2039c23abe7517%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EPark%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_d585bd6f9fcb47ada9b4ec2bff371e53.setContent%28html_743a75c83b0444cfaf2039c23abe7517%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_82b9b76a7b344ca7bd20131cbc8e35bc.bindPopup%28popup_d585bd6f9fcb47ada9b4ec2bff371e53%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_90c4d8530d124304bef16affbc03dbb1%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B41.502803775583736%2C-81.6889684802062%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_77a710de7f9d4e47af82867901aec818%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_d3d87c8f727d43b796cad6b0ce0c8af3%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_5bb77c57298d474bac9fcd759d2b6efd%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_5bb77c57298d474bac9fcd759d2b6efd%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3ESandwich%20Place%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_d3d87c8f727d43b796cad6b0ce0c8af3.setContent%28html_5bb77c57298d474bac9fcd759d2b6efd%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_90c4d8530d124304bef16affbc03dbb1.bindPopup%28popup_d3d87c8f727d43b796cad6b0ce0c8af3%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_12c3357fdd064b6a9457714e6f4ae0e2%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B41.50513047%2C-81.69024825%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_77a710de7f9d4e47af82867901aec818%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_29a3637ce4a541c7bbe4af713cc801ed%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_ed4e7e39571949bd92f9bedec4215625%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_ed4e7e39571949bd92f9bedec4215625%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EMobile%20Phone%20Shop%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_29a3637ce4a541c7bbe4af713cc801ed.setContent%28html_ed4e7e39571949bd92f9bedec4215625%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_12c3357fdd064b6a9457714e6f4ae0e2.bindPopup%28popup_29a3637ce4a541c7bbe4af713cc801ed%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_a00ff4c120ee46f6aaccb90db68073bf%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B41.50696416294396%2C-81.69008750128341%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_77a710de7f9d4e47af82867901aec818%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_ba71b320fa27423abba55f35e49d9bdf%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_1e5c23f0a2f143409094383113021e9a%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_1e5c23f0a2f143409094383113021e9a%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EHotel%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_ba71b320fa27423abba55f35e49d9bdf.setContent%28html_1e5c23f0a2f143409094383113021e9a%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_a00ff4c120ee46f6aaccb90db68073bf.bindPopup%28popup_ba71b320fa27423abba55f35e49d9bdf%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20circle_marker_3c7b9e1afbc54a06a212306dfa1ae20d%20%3D%20L.circleMarker%28%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%5B41.5040671%2C-81.6905365%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%22bubblingMouseEvents%22%3A%20true%2C%0A%20%20%22color%22%3A%20%22blue%22%2C%0A%20%20%22dashArray%22%3A%20null%2C%0A%20%20%22dashOffset%22%3A%20null%2C%0A%20%20%22fill%22%3A%20true%2C%0A%20%20%22fillColor%22%3A%20%22blue%22%2C%0A%20%20%22fillOpacity%22%3A%200.6%2C%0A%20%20%22fillRule%22%3A%20%22evenodd%22%2C%0A%20%20%22lineCap%22%3A%20%22round%22%2C%0A%20%20%22lineJoin%22%3A%20%22round%22%2C%0A%20%20%22opacity%22%3A%201.0%2C%0A%20%20%22radius%22%3A%205%2C%0A%20%20%22stroke%22%3A%20true%2C%0A%20%20%22weight%22%3A%203%0A%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%29.addTo%28map_77a710de7f9d4e47af82867901aec818%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20var%20popup_1859edf862fd45cf950b7594a96f2807%20%3D%20L.popup%28%7BmaxWidth%3A%20%27300%27%7D%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20var%20html_cc0560b54d3a4fd4b215546099ecbff0%20%3D%20%24%28%27%3Cdiv%20id%3D%22html_cc0560b54d3a4fd4b215546099ecbff0%22%20style%3D%22width%3A%20100.0%25%3B%20height%3A%20100.0%25%3B%22%3EBank%3C/div%3E%27%29%5B0%5D%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20popup_1859edf862fd45cf950b7594a96f2807.setContent%28html_cc0560b54d3a4fd4b215546099ecbff0%29%3B%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20circle_marker_3c7b9e1afbc54a06a212306dfa1ae20d.bindPopup%28popup_1859edf862fd45cf950b7594a96f2807%29%3B%0A%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%0A%3C/script%3E onload="this.contentDocument.open();this.contentDocument.write(    decodeURIComponent(this.getAttribute('data-html')));this.contentDocument.close();" allowfullscreen webkitallowfullscreen mozallowfullscreen></iframe></div></div>




```python
# define URL
url = 'https://api.foursquare.com/v2/venues/trending?client_id={}&client_secret={}&ll={},{}&v={}'.format(CLIENT_ID, CLIENT_SECRET, latitude, longitude, VERSION)

# send GET request and get trending venues
results = requests.get(url).json()
results
```




    {'meta': {'code': 200, 'requestId': '60490829ccb5ce3c7581bd0c'},
     'response': {'venues': []}}




```python
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
```


```python
# display trending venues
trending_venues_df
```




    'No trending venues are available at the moment!'



Compare the two cities


```python
cle_dataframe_venues['categories'] = cle_dataframe_venues['categories'].astype(str)
```


```python
cle_dataframe_restaurant['categories'] = cle_dataframe_restaurant['categories'].astype(str)
```


```python
cbus_dataframe_venues['categories'] = cbus_dataframe_venues['categories'].astype(str)
```


```python
cbus_dataframe_restaurant['categories'] = cbus_dataframe_restaurant['categories'].astype(str)
```


```python
cle_dataframe_restaurant['distance'].mean()
```




    480.375




```python
cbus_dataframe_restaurant['distance'].mean()
```




    329.14285714285717




```python
cle_dataframe_venues['distance'].mean()
```




    314.76666666666665




```python
cbus_dataframe_venues['distance'].mean()
```




    232.56666666666666




```python
countclerest = cle_dataframe_restaurant['categories'].value_counts()
print(countclerest)
```

    Food                       2
    American Restaurant        2
    New American Restaurant    1
    Bar                        1
    Deli / Bodega              1
    Italian Restaurant         1
    Name: categories, dtype: int64
    


```python
countcbusrest = cbus_dataframe_restaurant['categories'].value_counts()
print(countcbusrest)
```

    Brewery                          2
    Food                             2
    Vegetarian / Vegan Restaurant    1
    Chinese Restaurant               1
    Juice Bar                        1
    Italian Restaurant               1
    Breakfast Spot                   1
    New American Restaurant          1
    Sandwich Place                   1
    American Restaurant              1
    None                             1
    Food Court                       1
    Name: categories, dtype: int64
    


```python
countcleven = cle_dataframe_venues['categories'].value_counts()
print(countcleven)
```

    Hotel                5
    Park                 3
    Hotel Bar            2
    Coffee Shop          2
    Café                 2
    Museum               2
    Pharmacy             1
    Bank                 1
    Auditorium           1
    Mobile Phone Shop    1
    Steakhouse           1
    Gym                  1
    Science Museum       1
    Fountain             1
    Wings Joint          1
    Public Art           1
    Credit Union         1
    Movie Theater        1
    Sandwich Place       1
    Souvenir Shop        1
    Name: categories, dtype: int64
    


```python
countcbusven = cbus_dataframe_venues['categories'].value_counts()
print(countcbusven)
```

    Coffee Shop                  3
    Hotel                        2
    Café                         2
    Theater                      2
    Art Gallery                  1
    Whisky Bar                   1
    Asian Restaurant             1
    American Restaurant          1
    Arts & Crafts Store          1
    Salad Place                  1
    Italian Restaurant           1
    Taco Place                   1
    Gym / Fitness Center         1
    Deli / Bodega                1
    Record Shop                  1
    Leather Goods Store          1
    Hotel Bar                    1
    Pizza Place                  1
    Steakhouse                   1
    Irish Pub                    1
    Capitol Building             1
    Event Space                  1
    Latin American Restaurant    1
    Farmers Market               1
    Cuban Restaurant             1
    Name: categories, dtype: int64
    


```python

```
