import folium
import geopy
from geopy import distance
import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
from streamlit_folium import folium_static
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="mappy")

st.markdown("# Map Service")

data = {'lat' : [23.3455, 23.5456, 23.231424,23.9455, 24.5456, 24.231424], 'lon' : [78.2425,78.2435,78.344747,78.1425,78.935,78.344447]}
sos = {'lat' : [23.3455] , 'lon' : [78.2127]}

if st.checkbox("Enter Location") :
    add = st.text_input("Enter Address")
    location = geolocator.geocode(add)
    sos = {'lat' : [location.latitude] , 'lon' : [location.longitude]}

if st.checkbox("Drop Location") : 
    data = {'lat' : [23.5456,23.231424], 'lon' : [78.2425,78.344447]}

data = pd.DataFrame(data)
sos  = pd.DataFrame(sos)

m = folium.Map(location=[sos.iloc[0]['lat'],sos.iloc[0]['lon']], tiles="OpenStreetMap", zoom_start=7)



for i in range(len(data)):
    folium.Marker(
          location=[data.iloc[i]['lat'], data.iloc[i]['lon']],
          popup= "Services",
          icon= folium.Icon(color= "green")
       ).add_to(m)

for i in range(len(sos)):
    folium.Marker(
          location=[sos.iloc[i]['lat'], sos.iloc[i]['lon']],
          popup= "SOS",
          icon= folium.Icon(color= "red")
       ).add_to(m)
    
    
def short_dist(sosloc):
    l = []
    c = []
    for i in range(len(data)):
        d = distance.distance((data.iloc[i]['lat'], data.iloc[i]['lon']), sosloc)
        l.append(d)
        c.append((data.iloc[i]['lat'], data.iloc[i]['lon']))
        print(d)
    return (min(l), c[l.index(min(l))])
    
dist , coord = short_dist((sos.iloc[0]['lat'], sos.iloc[0]['lon']))
st.write(dist)
st.write(coord)
folium.PolyLine([coord, (sos.iloc[0]['lat'], sos.iloc[0]['lon'])]).add_to(m)
folium_static(m)

