import pandas as pd
import re
import numpy as np
import streamlit as st
import folium
from folium.plugins import HeatMap


st.title("Laadpalen op een kaart")

# Read the CSV file
inlaad = pd.read_csv('pages/opencharge.csv')
df = pd.DataFrame(inlaad)

st.header("Data opschonen")
st.write("Tijdens het initiele dataverkenning, hebben wij ontdenkt dat er veel behoefte is aan data cleaning in deze dataset.")
st.write("Na overleg was besloten dat de kolom 'UsageCost' meegenomen zal worden in onze plot.")
st.write("Er missen wel veel datapunten")
st.write(df.UsageCost.isna().sum())
st.write("Er zat absoluut geen structuur in de formatting voor waardes binnen deze kolom. Met behulp van string replacement en regular expressions is de data opgeschoont voor gebruik.")
st.write("De nul waardes worden vervangen met de median waardes.")
st.code('''
def clean_usage_cost(value):
    if isinstance(value, str):
        # Replace commas with dots
        value = value.replace(',', '.')

        # Check if the value is "free" (case-insensitive)
        if value.lower() == 'free':
            value = 0
        else:
            # Remove non-numeric characters and convert to float
            value = re.sub(r'[^0-9.]', '', value)
            try:
                value = float(value)
            except ValueError:
                value = np.nan

        return value
    else:
        # Handle other data types as NaN
        return np.nan

# Apply the custom function to the "UsageCost" column
df["UsageCost"] = df["UsageCost"].apply(clean_usage_cost)

# Fill up the Nan values with the Median and exclude 0
df.UsageCost = df.UsageCost.replace(0, np.nan)
median = df.UsageCost.median()
df.UsageCost = df.UsageCost.interpolate()
df.UsageCost       

''',language="Python")

# Define a custom function to clean the "UsageCost" column
def clean_usage_cost(value):
    if isinstance(value, str):
        # Replace commas with dots
        value = value.replace(',', '.')

        # Check if the value is "free" (case-insensitive)
        if value.lower() == 'free':
            value = 0
        else:
            # Remove non-numeric characters and convert to float
            value = re.sub(r'[^0-9.]', '', value)
            try:
                value = float(value)
            except ValueError:
                value = np.nan

        return value
    else:
        # Handle other data types as NaN
        return np.nan

# Apply the custom function to the "UsageCost" column
df["UsageCost"] = df["UsageCost"].apply(clean_usage_cost)



st.write(df['UsageCost'].dtype)
st.write(df)
st.write(df.isna().sum())

st.write("Aantal kolommen worden hernoemt om leesbaarheid en bruikbaarheid te verbeteren")

st.code('''
df.rename(columns={"AddressInfo.Town": "Town"}, inplace=True)
df.rename(columns={"AddressInfo.StateOrProvince": "Province"}, inplace=True)
df.rename(columns={"AddressInfo.Postcode": "postcode"}, inplace=True))
''',language="Python")
st.divider()
df.rename(columns={"AddressInfo.Town": "Town"}, inplace=True)
df.rename(columns={"AddressInfo.StateOrProvince": "Province"}, inplace=True)
df.rename(columns={"AddressInfo.Postcode": "postcode"}, inplace=True)


st.divider()
st.header("Laadpalen heatmap over heel Nederland")
st.write("Met behulp van Folium, hebben wij een heatmap geplot van de laadpaaldichtheid over heel Nederland")
st.write("Zoals te zien is, zitten de meeste laadpalen in de Randstad.")
st.write("Als Nederland voor 2030 volledig elektrisch wilt zijn, zullen er meer laadpalen moeten geinstalleerd worden in de lichter gekleurde gebieden om de minder gepopuleerde delen van Nederland te servicen.")

# Create a map
map_df = folium.Map(location=[52.3702, 4.8952], zoom_start=8)

# Create a list of coordinates from the DataFrame
coordinates = df[['AddressInfo.Latitude', 'AddressInfo.Longitude']].values

# Create a HeatMap layer
heatmap_layer = HeatMap(coordinates, radius=15)

# Add the HeatMap layer to the map
heatmap_layer.add_to(map_df)

# Display the map
st.write(map_df)

