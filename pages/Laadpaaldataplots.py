import pandas as pd
import plotly.express as px
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

st.set_option('deprecation.showPyplotGlobalUse', False)

st.title("Laadpaal dataverkenning")
inladen = pd.read_csv('pages/laadpaaldata.csv')
laadpaalDf = pd.DataFrame(inladen)
laadpaalDf['Efficiency'] = laadpaalDf['ChargeTime'] / laadpaalDf['ConnectedTime'] * 100
laadpaalDf = laadpaalDf[laadpaalDf['ChargeTime'] >= 0]
laadpaalDf.loc[laadpaalDf['Efficiency'] > 100, 'Efficiency'] = 100
laadpaalDf['Started'] = pd.to_datetime(laadpaalDf['Started'], errors='coerce', format='%Y-%m-%d %H:%M:%S')
laadpaalDf['Ended'] = pd.to_datetime(laadpaalDf['Ended'], errors='coerce', format='%Y-%m-%d %H:%M:%S')

st.write("We beginnen met het inladen van de dataset door het aan te roepen van 'laadpaaldata.csv'. ")
st.write("De kolom 'Efficiency' wordt aangemaakt door 'Chargetime' te delen met 'ConnectedTime'. ")

st.header("Dataset Dtypes")
st.write("De datatypes en algemene informatie van de dataset.")
st.write(laadpaalDf.dtypes)
st.divider()
st.header("Dataset Describe")
st.write("De tijdskolommen zijn in uren, en de eenheid van energie gebruikt is kWh.")
st.write(laadpaalDf.describe())
st.divider() 
st.header("Overzicht dataset")
st.write(laadpaalDf)
st.divider()

plt.hist(laadpaalDf['ChargeTime'], bins=10, range=(0, 10), color='skyblue', edgecolor='black', label = "Charge Time", alpha = 0.5)
plt.hist(laadpaalDf['ConnectedTime'], bins=10, range=(0, 10), color='orange', edgecolor='black', label = "Connected Time", alpha = 0.5)
plt.xlabel('Tijd (Uren)')
plt.ylabel('Waarnemingen')
plt.legend(loc='upper right')
plt.title('Verdeling van Laadtijd en Aansluitingstijd')

st.write("Een histogram dat de verdeling van de laadtijden en aansluitingstijden in de dataset laat zien. Er is duidelijk te zien dat de meeste mensen een laadpaal laden voor een tijd tussen de 0 en 4 uur.")
st.write("Er is te zien dat de Connectedtime niet dezelfde grote piek heeft tussen 0-4 uur dan de Chargetime, dit laat ons zien dat er veel gevallen zijn waar auto's nog aangesloten zitten nadat ze al volledig opgeladen zijn.")
st.pyplot()
st.divider()
# Calculate the z-score for the ConnectedTime column
z_scores = (laadpaalDf['ConnectedTime'] - laadpaalDf['ConnectedTime'].mean()) / laadpaalDf['ConnectedTime'].std()
# Define a threshold for outliers (e.g., z-score > 3)
outlier_threshold = 3
# Drop rows where the z-score exceeds the threshold
laadpaalDf = laadpaalDf[z_scores <= outlier_threshold]

# Drop rows where the Efficiency column is equal to 0
laadpaalDf = laadpaalDf[laadpaalDf['Efficiency'] != 0]


# Sort the data by ConnectedTime
sorted_data = laadpaalDf.sort_values('ConnectedTime')

# Calculate the trend line using linear regression
coefficients = np.polyfit(sorted_data['ConnectedTime'], sorted_data['Efficiency'], 1)
trend_line = np.poly1d(coefficients)

# Plot the scatter plot with smaller datapoints
plt.scatter(laadpaalDf['ConnectedTime'], laadpaalDf['Efficiency'], c=laadpaalDf['ConnectedTime'], cmap='cool', alpha=0.5, s=10)
plt.xlabel('ConnectedTime')
plt.ylabel('Efficiency')
plt.title('Scatter Plot of ConnectedTime vs Efficiency')
plt.colorbar(label='ConnectedTime')

# Plot the trend line
plt.plot(sorted_data['ConnectedTime'], trend_line(sorted_data['ConnectedTime']), color='red')

plt.ylim(0)  # Set the Y axis lower limit to 0
st.write("Een scatterplot tussen de aansluitingstijd en efficiency, de stijlheid van de negatieve lineare trendlijn laat zien dat des te langer een auto aan het opladen is, de verhouding tussen aansluitingstijd en oplaadtijd verslechterd.")
st.write("Dit laat zien dat auto's vaak langer opladen dan nodig is. De efficiency van de laadpalen zou verbeterd kunnen worden door een systeem te implementeren waar laadpalen beschikbaar worden zodra een aangesloten auto opgeladen is.")
st.pyplot()
