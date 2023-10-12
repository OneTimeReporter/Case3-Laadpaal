import pandas as pd
import json
import streamlit as st
import plotly.express as px
import requests
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
from sodapy import Socrata
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import re

inlaad = pd.read_json("https://opendata.rdw.nl/resource/vmju-ygcs.json?$Limit=168630")
df_ev_2022 = df = pd.DataFrame(inlaad)
st.write(df_ev_2022)

df_ev_2022 = df_ev_2022.groupby('merk').filter(lambda x: len(x) >= 400)

# Aannamen dat de kolom 'Merk' in de DataFrame 'df' zit
merken = df_ev_2022['merk']

# Bereken de count van elke merkwaarde
merk_counts = merken.value_counts()

# Maak een DataFrame van de gesorteerde merk counts
sorted_merk_counts = merk_counts.sort_values(ascending=False).reset_index()
sorted_merk_counts.columns = ['Merk', 'Aantal']

# Maak een histogram met Plotly Express
fig = px.bar(sorted_merk_counts, x='Merk', y='Aantal',
             title='Histogram van Automerken',
             labels={'Aantal': 'Aantal', 'Merk': 'Automerk'},
             width=800, height=600)

# Zorg ervoor dat de x-as labels leesbaar zijn
fig.update_xaxes(tickangle=90, tickmode='array', tickvals=sorted_merk_counts['Merk'])

# Toon het histogram
st.plotly_chart(fig, use_container_width=True)
st.divider()
st.write("Vooral Tesla, Peugeot, Volkswagen en Kia zijn populaire merken onder de elektrische automobilist.")

st.code("df_ev_2022['catalogusprijs'].mean()")
df_ev_2022['catalogusprijs'].mean()
st.write("De gemiddelde prijs van een elektrische auto is 52929 euro.")
st.divider()

inladen = pd.read_csv('pages/opencharge.csv')
opencharge = pd.DataFrame(inladen)

st.write(opencharge.index)
st.write("Data wordt opgeschoont, onnodige kolommen worden gedropt, en kolommen worden hernoemt voor makkelijkere leesbaarheid en bruikbaarheid.")
st.code(''' 
opencharge['AddressInfo.Postcode'] = opencharge['AddressInfo.Postcode'].str.replace(' ', '')
opencharge.drop(['AddressInfo.ContactEmail', 'DateLastConfirmed', 'MetadataValues', 'AddressInfo.ContactTelephone2', 'AddressInfo.AddressLine2', 'AddressInfo.AccessComments', 'GeneralComments','AddressInfo.ContactTelephone', 'UsageTypeID', 'AddressInfo.RelatedURL', 'OperatorsReference'], axis=1, inplace=True)
opencharge.rename(columns={'AddressInfo.Longitude': 'Longitude', 'AddressInfo.Latitude': 'Latitude', 'AddressInfo.CountryID': 'CountryID'}, inplace=True)
''')
opencharge['AddressInfo.Postcode'] = opencharge['AddressInfo.Postcode'].str.replace(' ', '')
opencharge.rename(columns={'AddressInfo.Longitude': 'Longitude', 'AddressInfo.Latitude': 'Latitude', 'AddressInfo.CountryID': 'CountryID'}, inplace=True)

st.header("Kaart van de data uit opencharge")

st.write("Hieronder wordt een kaart weergegeven met de locaties van de oplaadstations uit de opencharge dataset.")

# Create a map object
m = folium.Map(location=[52.379189, 4.899431], zoom_start=10)

# Add markers for each charging station
for index, row in opencharge.iterrows():
    folium.Marker([row['Latitude'], row['Longitude']]).add_to(m)

# Display the map
st.map = st_folium(m, width=1000)

#df_results = pd.DataFrame(results)
#st.write(df_results)
#df_results_2 = pd.DataFrame(results2)
#st.write(df_results_2)

# Voer de merge-operatie uit op basis van de kolom "kenteken"
st.write("De initiele dataset wordt gejoint met brandstoftype data behaalt van de website van de rdw.")

st.code('''
merged_df = pd.merge(df_ev_2022, df_results_2, on='kenteken', how='inner')
''')
brandstofinladen = pd.read_csv("pages/brandstoftypedata.csv")
df_results_2 = pd.DataFrame(brandstofinladen)
merged_df = pd.merge(df_ev_2022, df_results_2, on='kenteken', how='inner')

# 'inner' betekent dat alleen de gemeenschappelijke rijen worden opgenomen
# Als je alle rijen uit beide DataFrames wilt behouden, zelfs als ze geen overeenkomstige kentekens hebben, gebruik dan 'outer' in plaats van 'inner'.

st.write("Toon het samengevoegde DataFrame")
#st.write(merged_df)
st.write("Toon het aantal hybride auto's")
st.write(merged_df['klasse_hybride_elektrisch_voertuig'].value_counts())
st.write("Er zijn 266 hybride autos")
st.write("Toont de waardes in brandstof omschrijving, en de aantal nan waardes in de dataframe")
st.write(merged_df['brandstof_omschrijving'].value_counts())
st.write(merged_df.isna().sum())

#Hier ben ik een nieuwe dataset aan het maken met alleen nuttige inhoud
#De zuinigheidsclassificatie heb ik helaas niet meekunnen nemen

merged_clean = merged_df[['merk', 'handelsbenaming', 'voertuigsoort', 'inrichting', 'massa_rijklaar', 'catalogusprijs', 'lengte', 'breedte', 'klasse_hybride_elektrisch_voertuig', 'brandstof_omschrijving']]
#st.write(merged_clean)

# Annamen dat merged_clean je DataFrame is
# Vervang null-waarden in de kolom klasse_hybride_elektrisch_voertuig door 'Geen hybride'
merged_clean['klasse_hybride_elektrisch_voertuig'].fillna('Geen hybride', inplace=True)

st.write(merged_clean.isna().sum())

missing_uitvoering_rows = merged_clean[merged_clean['catalogusprijs'].isnull()]

# Toon de rijen met ontbrekende waarden in de kolom 'uitvoering'
st.write(missing_uitvoering_rows)

#tesla model 3 48836
#eqv is 85670
#model y is 56001
#model x is 130499
#2008 is 40946
#ix m60 is 144830
# ilter de rijen met de opgegeven voorwaarden
filtered_rows = merged_clean.loc[(merged_clean['handelsbenaming'] == 'IX M60') & (merged_clean['inrichting'] == 'stationwagen')]

# Toon de rijen die aan beide voorwaarden voldoen
gemiddelde_catalogusprijs = filtered_rows['catalogusprijs'].mean()

merged_clean.at[67755, 'catalogusprijs'] = 144830
merged_clean.at[95138, 'catalogusprijs'] = 40946
merged_clean.at[99228, 'catalogusprijs'] = 85670
merged_clean.at[101810, 'catalogusprijs'] = 48836
merged_clean.at[121665, 'catalogusprijs'] = 56001
merged_clean.at[141444, 'catalogusprijs'] = 130499
st.write(merged_clean.isna().sum())

missing_lengte_rows = merged_clean[merged_clean['lengte'].isnull()]

# Toon de rijen met ontbrekende waarden in de kolom 'uitvoering'
st.write(missing_lengte_rows)

# Groepeer de gegevens op basis van 'handelsbenaming' en 'voertuigsoort', en vul de ontbrekende waarden in 'lengte' op
merged_clean['lengte'] = merged_clean.groupby(['handelsbenaming', 'voertuigsoort'])['lengte'].transform(lambda x: x.fillna(x.mean()))
merged_clean['breedte'] = merged_clean.groupby(['handelsbenaming', 'voertuigsoort'])['breedte'].transform(lambda x: x.fillna(x.mean()))
st.write(merged_clean.isna().sum())

missing_lengte2_rows = merged_clean[merged_clean['lengte'].isnull()]

# Toon de rijen met ontbrekende waarden in de kolom 'uitvoering'
st.write(missing_lengte2_rows)

cleaned_df = merged_clean.dropna()
#cleaned_df

# Calculate the z-scores for catalogusprijs
z_scores = np.abs((cleaned_df['catalogusprijs'] - cleaned_df['catalogusprijs'].mean()) / cleaned_df['catalogusprijs'].std())
# Identify the outliers
outliers = cleaned_df[z_scores > 3]
# Remove the outliers
cleaned_df = cleaned_df[z_scores <= 3]
# Show the updated DataFrame
#cleaned_df


# Maak een scatter plot om de relatie tussen massa_rijklaar en catalogusprijs te verkennen
plt.figure(figsize=(10, 6))
sns.scatterplot(x='massa_rijklaar', y='catalogusprijs', hue='inrichting', alpha=0.5, data=cleaned_df)
plt.plot([cleaned_df['massa_rijklaar'].min(), cleaned_df['massa_rijklaar'].max()], [cleaned_df['catalogusprijs'].mean(), cleaned_df['catalogusprijs'].mean()], color='red', linestyle='--')

# Fit a linear regression line to the scatter plot
sns.regplot(x='massa_rijklaar', y='catalogusprijs', data=cleaned_df, scatter=False, color='blue')

plt.xlabel('Massa Rijklaar')
plt.ylabel('Catalogusprijs')
plt.title("Relatie tussen Massa Rijklaar en Catalogusprijs van elektrische auto's")
st.pyplot()

st.divider()

# Maak een histogram met Plotly en toon de exacte count op de bars
fig = px.histogram(cleaned_df, x='klasse_hybride_elektrisch_voertuig', 
                   title='Histogram van Klasse Hybride Elektrisch Voertuig',
                   labels={'klasse_hybride_elektrisch_voertuig': 'Klasse Hybride Elektrisch Voertuig', 'count': 'Aantal Voertuigen'})

# Voeg tekstlabels toe aan de bars met de exacte count
fig.update_traces(texttemplate='%{y}', textposition='outside')

# Stel de hoogte van de plot in
fig.update_layout(height=600)

# Pas de kleuren van de blokken aan
fig.update_traces(marker_color=['#1f77b4', '#ff7f0e'])

st.plotly_chart(fig)

st.divider()

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
opencharge["UsageCost"] = opencharge["UsageCost"].apply(clean_usage_cost)

opencharge["UsageCost"] = opencharge["UsageCost"].astype(float)

#De merken grouperen met de gemiddelde massa rijklaar van ieder merk.
df_merk_mass = df_ev_2022.groupby('merk')['massa_rijklaar'].mean().reset_index()

#Het gemiddelde van alle merken toevoegen.
new_data = {'merk': ['GEMIDDELD'], 'massa_rijklaar': df_ev_2022['massa_rijklaar'].mean()}
new_df = pd.DataFrame(new_data)
df_merk_mass = pd.concat([df_merk_mass, new_df], ignore_index=True)

#De gegevens sorteren van groot naar klein op basis van de massa rijklaar.
df_merk_mass = df_merk_mass.sort_values(by='massa_rijklaar', ascending=False)

#plotten
fig = px.bar(df_merk_mass, x='merk', y='massa_rijklaar',
             title='Histogram van de gemiddelde massa van een elektrische auto per automerken',
             labels={'merk': 'Automerk', 'massa_rijklaar': 'Gemiddelde massa per automerk'}, color='merk', color_discrete_sequence=['blue'])


#Het gemiddelde van alle merken kleuren.
fig.update_traces(marker_color='red', selector=dict(name='GEMIDDELD'))
st.plotly_chart(fig)
st.divider()

#De merken grouperen met de gemiddelde catalogusprijs van ieder merk.
df_merk_mass = df_ev_2022.groupby('merk')['catalogusprijs'].mean().reset_index()

#Het gemiddelde van alle merken toevoegen.
new_data = {'merk': ['GEMIDDELD'], 'catalogusprijs': df_ev_2022['catalogusprijs'].mean()}
new_df = pd.DataFrame(new_data)
df_merk_mass = pd.concat([df_merk_mass, new_df], ignore_index=True)

#De gegevens sorteren van groot naar klein op basis van de massa rijklaar.
df_merk_mass = df_merk_mass.sort_values(by='catalogusprijs', ascending=False)

#plotten
fig = px.bar(df_merk_mass, x='merk', y='catalogusprijs',
             title='Histogram van de gemiddelde catalogusprijs van een elektrische auto per automerken',
             labels={'merk': 'Automerk', 'catalogusprijs': 'Gemiddelde catalogusprijs per automerk'}, color='merk', color_discrete_sequence=['blue'])


#Het gemiddelde van alle merken kleuren.
fig.update_traces(marker_color='red', selector=dict(name='GEMIDDELD'))
st.plotly_chart(fig)

