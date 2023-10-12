#!/usr/bin/env python
# coding: utf-8

# In[5]:


import pandas as pd
import json
import streamlit as st
inlaad = pd.read_json("https://opendata.rdw.nl/resource/vmju-ygcs.json?$Limit=168630")
df_ev_2022 = df = pd.DataFrame(inlaad)


# In[6]:


df_ev_2022


# In[7]:


df_ev_2022 = df_ev_2022.groupby('merk').filter(lambda x: len(x) >= 400)


# In[8]:


import plotly.express as px

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
fig.show()


# Vooral Tesla, Peugeot, Volkswagen en Kia zijn populaire merken onder de elektrische automobilist.

# In[8]:


df_ev_2022['catalogusprijs'].mean()


# De gemiddelde prijs van een elektrische auto is 52929 euro.

# In[29]:


import requests

# API endpoint URL with corrected query parameters
url = f'https://api.openchargemap.io/v3/poi/?output=json&countrycode=NL&maxresults=7909&compact=true&verbose=false&key=93b912b5-9d70-4b1f-960b-fb80a4c9c017'

# Make a GET request to retrieve charging station data
response = requests.get(url)

# Check for successful response
if response.status_code == 200:
    charging_stations = response.json()
    opencharge = pd.json_normalize(charging_stations)
    # Process the charging station data as needed
else:
    print(f"Error: {response.status_code}")
    print(response.text)  # Print the error message from the API if available


# In[35]:


opencharge.to_csv("opencharge.csv")


# In[36]:


opencharge.index


# In[37]:


opencharge['AddressInfo.Postcode'] = opencharge['AddressInfo.Postcode'].str.replace(' ', '')


# In[35]:


opencharge.drop(['AddressInfo.ContactEmail', 'DateLastConfirmed', 'MetadataValues', 'AddressInfo.ContactTelephone2', 'AddressInfo.AddressLine2', 'AddressInfo.AccessComments', 'GeneralComments','AddressInfo.ContactTelephone', 'UsageTypeID', 'AddressInfo.RelatedURL', 'OperatorsReference'], axis=1, inplace=True)


# In[76]:


opencharge.isna().sum().sort_values(ascending=True)


# In[44]:


opencharge.rename(columns={'AddressInfo.Longitude': 'Longitude', 'AddressInfo.Latitude': 'Latitude', 'AddressInfo.CountryID': 'CountryID'}, inplace=True)


# In[53]:


opencharge['AddressInfo.StateOrProvince'].isnull().sum()


# In[ ]:


opencharge['AddressInfo.Postcode'].isnull().sum()


# ## Kaart van de data uit opencharge
# 
# Hieronder wordt een kaart weergegeven met de locaties van de oplaadstations uit de opencharge dataset.

# In[35]:


# Import the necessary libraries
import folium

# Create a map object
m = folium.Map(location=[52.379189, 4.899431], zoom_start=10)

# Add markers for each charging station
for index, row in opencharge.iterrows():
    folium.Marker([row['AddressInfo.Latitude'], row['AddressInfo.Longitude']]).add_to(m)

# Display the map
m


# In[11]:


get_ipython().system('pip install sodapy')

from sodapy import Socrata

client = Socrata("opendata.rdw.nl", None)
results = client.get("w4rt-e856", limit=450000)
client2 = Socrata("opendata.rdw.nl", None)
results2 = client2.get("vsxf-rq7p", limit=16000000)


# In[15]:


df_results = pd.DataFrame(results)
df_results


# In[16]:


df_results_2 = pd.DataFrame(results2)
df_results_2


# In[18]:


df_results.to_csv("autosdata.csv")
df_results_2.to_csv("brandstoftypedata.csv")


# In[22]:


import pandas as pd

# Lees gegevens vanuit een CSV-bestand en plaats deze in een DataFrame
df_results_2 = pd.read_csv('brandstoftypedata.csv')
df_results = pd.read_csv('autosdata.csv')


# In[23]:


# Importeer de pandas-bibliotheek als dat nog niet is gedaan
import pandas as pd

# Voer de merge-operatie uit op basis van de kolom "kenteken"
merged_df = pd.merge(df_ev_2022, df_results_2, on='kenteken', how='inner')

# 'inner' betekent dat alleen de gemeenschappelijke rijen worden opgenomen
# Als je alle rijen uit beide DataFrames wilt behouden, zelfs als ze geen overeenkomstige kentekens hebben, gebruik dan 'outer' in plaats van 'inner'.

# Toon het samengevoegde DataFrame
merged_df


# In[24]:


merged_df['klasse_hybride_elektrisch_voertuig'].value_counts()


# Er zijn 266 hybride autos

# In[25]:


merged_df['brandstof_omschrijving'].value_counts()


# In[26]:


merged_df.isna().sum()


# In[27]:


#Hier ben ik een nieuwe dataset aan het maken met alleen nuttige inhoud
#De zuinigheidsclassificatie heb ik helaas niet meekunnen nemen

merged_clean = merged_df[['merk', 'handelsbenaming', 'voertuigsoort', 'inrichting', 'massa_rijklaar', 'catalogusprijs', 'lengte', 'breedte', 'klasse_hybride_elektrisch_voertuig', 'brandstof_omschrijving']]
merged_clean


# In[28]:


import pandas as pd

# Annamen dat merged_clean je DataFrame is
# Vervang null-waarden in de kolom klasse_hybride_elektrisch_voertuig door 'Geen hybride'
merged_clean['klasse_hybride_elektrisch_voertuig'].fillna('Geen hybride', inplace=True)


# In[29]:


merged_clean.isna().sum()


# In[30]:


missing_uitvoering_rows = merged_clean[merged_clean['catalogusprijs'].isnull()]

# Toon de rijen met ontbrekende waarden in de kolom 'uitvoering'
missing_uitvoering_rows


# In[32]:


#tesla model 3 48836
#eqv is 85670
#model y is 56001
#model x is 130499
#2008 is 40946
#ix m60 is 144830
# Filter de rijen met de opgegeven voorwaarden
filtered_rows = merged_clean.loc[(merged_clean['handelsbenaming'] == 'IX M60') & (merged_clean['inrichting'] == 'stationwagen')]

# Toon de rijen die aan beide voorwaarden voldoen
gemiddelde_catalogusprijs = filtered_rows['catalogusprijs'].mean()

merged_clean.at[67755, 'catalogusprijs'] = 144830
merged_clean.at[95138, 'catalogusprijs'] = 40946
merged_clean.at[99228, 'catalogusprijs'] = 85670
merged_clean.at[101810, 'catalogusprijs'] = 48836
merged_clean.at[121665, 'catalogusprijs'] = 56001
merged_clean.at[141444, 'catalogusprijs'] = 130499
merged_clean.isna().sum()


# In[33]:


missing_lengte_rows = merged_clean[merged_clean['lengte'].isnull()]

# Toon de rijen met ontbrekende waarden in de kolom 'uitvoering'
missing_lengte_rows


# In[34]:


# Groepeer de gegevens op basis van 'handelsbenaming' en 'voertuigsoort', en vul de ontbrekende waarden in 'lengte' op
merged_clean['lengte'] = merged_clean.groupby(['handelsbenaming', 'voertuigsoort'])['lengte'].transform(lambda x: x.fillna(x.mean()))
merged_clean['breedte'] = merged_clean.groupby(['handelsbenaming', 'voertuigsoort'])['breedte'].transform(lambda x: x.fillna(x.mean()))
merged_clean.isna().sum()


# In[21]:


missing_lengte2_rows = merged_clean[merged_clean['lengte'].isnull()]

# Toon de rijen met ontbrekende waarden in de kolom 'uitvoering'
missing_lengte2_rows


# In[37]:


cleaned_df = merged_clean.dropna()
cleaned_df


# In[124]:


import numpy as np

# Calculate the z-scores for catalogusprijs
z_scores = np.abs((cleaned_df['catalogusprijs'] - cleaned_df['catalogusprijs'].mean()) / cleaned_df['catalogusprijs'].std())

# Identify the outliers
outliers = cleaned_df[z_scores > 3]

# Remove the outliers
cleaned_df = cleaned_df[z_scores <= 3]

# Show the updated DataFrame
cleaned_df


# In[151]:


import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Maak een scatter plot om de relatie tussen massa_rijklaar en catalogusprijs te verkennen
plt.figure(figsize=(10, 6))
sns.scatterplot(x='massa_rijklaar', y='catalogusprijs', hue='inrichting', alpha=0.5, data=cleaned_df)
plt.plot([cleaned_df['massa_rijklaar'].min(), cleaned_df['massa_rijklaar'].max()], [cleaned_df['catalogusprijs'].mean(), cleaned_df['catalogusprijs'].mean()], color='red', linestyle='--')

# Fit a linear regression line to the scatter plot
sns.regplot(x='massa_rijklaar', y='catalogusprijs', data=cleaned_df, scatter=False, color='blue')

plt.xlabel('Massa Rijklaar')
plt.ylabel('Catalogusprijs')
plt.title("Relatie tussen Massa Rijklaar en Catalogusprijs van elektrische auto's")
plt.show()


# In[ ]:





# In[ ]:





# In[90]:


import plotly.express as px

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

fig.show()


# In[55]:


for value in opencharge["UsageCost"]:
    print(value)


# In[43]:


import re
import numpy as np

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
for value in opencharge["UsageCost"]:
    print(value)


# In[56]:


opencharge["UsageCost"].unique()


# In[42]:


df_ev_2022['massa_rijklaar'].mean()


# De gemiddelde massa van een elektrische auto is 1903 kg.

# In[114]:


import plotly.express as px

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
fig.show()


# In[115]:


import plotly.express as px

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
fig.show()

