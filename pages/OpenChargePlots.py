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

st.write("Er missen datapunten voor de provinciekolom. Deze is opgevuld door een dictionary op te vullen met de postcodewaardes voor elk provincie.")
postcode_province_mapping = {
    # Noord-Holland
    **{code: 'Noord-Holland' for code in range(1000, 1300)},
    **{code: 'Noord-Holland' for code in range(1380, 1385)},
    **{code: 'Noord-Holland' for code in range(1398, 1426)},
    **{code: 'Noord-Holland' for code in range(1430, 2160)},

    # Flevoland
    **{code: 'Flevoland' for code in range(1300, 1380)},
    **{code: 'Flevoland' for code in range(3890, 3900)},

    # Utrecht
    **{code: 'Utrecht' for code in range(1390, 1394)},
    **{code: 'Utrecht' for code in range(1396, 1426)},
    **{code: 'Utrecht' for code in range(1426, 1430)},
    **{code: 'Utrecht' for code in range(3382, 3465)},
    **{code: 'Utrecht' for code in range(3467, 3770)},
    **{code: 'Utrecht' for code in range(3795, 3837)},
    **{code: 'Utrecht' for code in range(3837, 3890)},
    **{code: 'Utrecht' for code in range(3926, 4000)},
    **{code: 'Utrecht' for code in range(4120, 4130)},
    **{code: 'Utrecht' for code in range(4130, 4147)},
    **{code: 'Utrecht' for code in range(4163, 4170)},
    **{code: 'Utrecht' for code in range(4170, 4200)},
    **{code: 'Utrecht' for code in range(4200, 4210)},
    **{code: 'Utrecht' for code in range(4211, 4213)},
    **{code: 'Utrecht' for code in range(4230, 4240)},
    **{code: 'Utrecht' for code in range(4240, 4250)},
    **{code: 'Utrecht' for code in range(4250, 4300)},
    **{code: 'Utrecht' for code in range(3925, 4000)},
    **{code: 'Utrecht' for code in range(8100, 8160)},
    **{code: 'Utrecht' for code in range(8196, 8200)},

    # Zuid-Holland
    **{code: 'Zuid-Holland' for code in range(1428, 1430)},
    **{code: 'Zuid-Holland' for code in range(2159, 2165)},
    **{code: 'Zuid-Holland' for code in range(3465, 3467)},
    **{code: 'Zuid-Holland' for code in range(4200, 4210)},
    **{code: 'Zuid-Holland' for code in range(4213, 4220)},
    **{code: 'Zuid-Holland' for code in range(4220, 4230)},
    **{code: 'Zuid-Holland' for code in range(4240, 4250)},
    **{code: 'Zuid-Holland' for code in range(4250, 4300)},
    **{code: 'Zuid-Holland' for code in range(4310, 4600)},
    **{code: 'Zuid-Holland' for code in range(4600, 4672)},
    **{code: 'Zuid-Holland' for code in range(4680, 4700)},
    **{code: 'Zuid-Holland' for code in range(6030, 6500)},
    **{code: 'Zuid-Holland' for code in range(8160, 8196)},
    **{code: 'Zuid-Holland' for code in range(8260, 8300)},
    **{code: 'Zuid-Holland' for code in range(8323, 8355)},
    **{code: 'Zuid-Holland' for code in range(8355, 8380)},

    # Gelderland
    **{code: 'Gelderland' for code in range(3770, 3795)},
    **{code: 'Gelderland' for code in range(3925, 4000)},
    **{code: 'Gelderland' for code in range(4120, 4130)},
    **{code: 'Gelderland' for code in range(4120, 4130)},
    **{code: 'Gelderland' for code in range(4147, 4170)},
    **{code: 'Gelderland' for code in range(4170, 4200)},
    **{code: 'Gelderland' for code in range(4211, 4213)},
    **{code: 'Gelderland' for code in range(4214, 4220)},
    **{code: 'Gelderland' for code in range(4230, 4240)},
    **{code: 'Gelderland' for code in range(4242, 4250)},
    **{code: 'Gelderland' for code in range(5300, 5340)},
    **{code: 'Gelderland' for code in range(5740, 5766)},
    **{code: 'Gelderland' for code in range(8196, 8200)},
    **{code: 'Gelderland' for code in range(8388, 9300)},

    # Noord-Brabant
    **{code: 'Noord-Brabant' for code in range(4250, 4300)},
    **{code: 'Noord-Brabant' for code in range(4680, 4700)},
    **{code: 'Noord-Brabant' for code in range(4700, 5300)},
    **{code: 'Noord-Brabant' for code in range(5340, 5766)},
    **{code: 'Noord-Brabant' for code in range(5820, 5850)},
    **{code: 'Noord-Brabant' for code in range(6020, 6030)},

    # Limburg
    **{code: 'Limburg' for code in range(5766, 5820)},
    **{code: 'Limburg' for code in range(5850, 6020)},
    **{code: 'Limburg' for code in range(6030, 6500)},
    **{code: 'Limburg' for code in range(6584, 6600)},

    # Zeeland
    **{code: 'Zeeland' for code in range(4600, 4672)},
    **{code: 'Zeeland' for code in range(4672, 4680)},

    # Overijssel
    **{code: 'Overijssel' for code in range(7400, 7440)},
    **{code: 'Overijssel' for code in range(7440, 7740)},
    **{code: 'Overijssel' for code in range(7800, 7950)},
    **{code: 'Overijssel' for code in range(7950, 7956)},
    **{code: 'Overijssel' for code in range(7956, 8000)},
    **{code: 'Overijssel' for code in range(8000, 8055)},
    **{code: 'Overijssel' for code in range(8055, 8070)},
    **{code: 'Overijssel' for code in range(8100, 8160)},
    **{code: 'Overijssel' for code in range(8160, 8196)},
    **{code: 'Overijssel' for code in range(8200, 8260)},
    **{code: 'Overijssel' for code in range(8260, 8300)},
    **{code: 'Overijssel' for code in range(8323, 8355)},
    **{code: 'Overijssel' for code in range(8355, 8380)},

    # Drenthe
    **{code: 'Drenthe' for code in range(7740, 7767)},
    **{code: 'Drenthe' for code in range(7950, 7956)},
    **{code: 'Drenthe' for code in range(8380, 8388)},
    **{code: 'Drenthe' for code in range(8388, 9300)},
    **{code: 'Drenthe' for code in range(9300, 9350)},
    **{code: 'Drenthe' for code in range(9400, 9480)},
    **{code: 'Drenthe' for code in range(9480, 9500)},
    **{code: 'Drenthe' for code in range(9500, 9510)},
    **{code: 'Drenthe' for code in range(9510, 9540)},
    **{code: 'Drenthe' for code in range(9540, 9565)},
    **{code: 'Drenthe' for code in range(9565, 9570)},
    **{code: 'Drenthe' for code in range(9565, 9570)},
    **{code: 'Drenthe' for code in range(9570, 9580)},
    **{code: 'Drenthe' for code in range(9580, 9654)},

    # Groningen
    **{code: 'Groningen' for code in range(9350, 9400)},
    **{code: 'Groningen' for code in range(9479, 9480)},

    # For other codes not mentioned, you can specify a default value (e.g., 'Unknown')
}
st.write("Door met behulp van een regex expressie op kolom postcode zijn de lege provincie kolom waardes opgevuld aan de hand van de eerder vermelde dictionary.")

st.code('''
# Test the mapping
postcode = 1315  # Replace with a specific postal code to test
province = postcode_province_mapping.get(postcode, 'Unknown')
print(f"Postal Code {postcode} belongs to {province}")

# Remove non-numeric values from postcode
df.postcode = df['postcode'].str.replace(r'[A-Za-z]', '')
df.postcode

# Drop rijen met lege strings in de kolom 'postcode'
df = df.dropna(subset=['postcode'])
df = df[df['postcode'].astype(str).str.strip() != '']

# Overschrijf de waarden in de kolom 'province' in de DataFrame df met behulp van de mapping
df['province'] = df['postcode'].astype(int).map(postcode_province_mapping)
''',language="Python")

# Test the mapping
postcode = 1315  # Replace with a specific postal code to test
province = postcode_province_mapping.get(postcode, 'Unknown')
print(f"Postal Code {postcode} belongs to {province}")

# Remove non-numeric values from postcode
df.postcode = df['postcode'].str.replace(r'[A-Za-z]', '')
df.postcode

# Drop rijen met lege strings in de kolom 'postcode'
df = df.dropna(subset=['postcode'])
df = df[df['postcode'].astype(str).str.strip() != '']

# Overschrijf de waarden in de kolom 'province' in de DataFrame df met behulp van de mapping
df['province'] = df['postcode'].astype(int).map(postcode_province_mapping)

# Toon de DataFrame om te controleren of de waarden zijn overschreven
st.write("Zoals te zien is, is de provincie kolom nu opgevuld.")
st.write(df.isna().sum())
st.divider()

# Download de dataset van postcodes naar provincies van de CBS-website
url = "https://www.cbs.nl/-/media/_excel/2021/47/postcode-huisnummer2021.xlsx"
postcode_data = pd.read_excel(url, dtype={'postcode': str})

# Voorbeeld van een postcode
postcode = '1234AB'

# Haal de provincie op voor de gegeven postcode
provincie = postcode_data.loc[postcode_data['postcode'] == postcode.replace(' ','').upper(), 'provincie'].values[0]

print(f"Provincie voor postcode {postcode}: {provincie}")


unieke_waarden = df['Province'].unique()
unieke_waarden


df.UsageCost.isna().sum()

df.UsageCost = df.UsageCost.round(2)

# Fill up the Nan values with the Median and exclude 0
df.UsageCost = df.UsageCost.replace(0, np.nan)
median = df.UsageCost.median()
df.UsageCost = df.UsageCost.interpolate()
df.UsageCost

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

