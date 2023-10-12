import pandas as pd
import plotly.express as px
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np

st.title("Laadpaal dataverkenning")
inladen = pd.read_csv('pages/laadpaaldata.csv')
laadpaalDf = pd.Dataframe(inladen)
laadpaalDf['Efficiency'] = laadpaalDf['ChargeTime'] / laadpaalDf['ConnectedTime'] * 100
laadpaalDf = laadpaalDf[laadpaalDf['ChargeTime'] >= 0]

st.text("We beginnen met het inladen van de dataset door het aan te roepen van 'laadpaaldata.csv'. ")
st.text("De kolom 'Efficiency' wordt aangemaakt door 'Chargetime' te delen met 'ConnectedTime'. ")

laadpaalDf.dtypes

laadpaalDf.describe()

laadpaalDf.loc[laadpaalDf['Efficiency'] > 100, 'Efficiency'] = 100

laadpaalDf

laadpaalDf['Started'] = pd.to_datetime(laadpaalDf['Started'], errors='coerce', format='%Y-%m-%d %H:%M:%S')

plt.hist(laadpaalDf['ChargeTime'], bins=10, range=(0, 10), color='skyblue', edgecolor='black')
plt.xlabel('Laadtijd (Uren)')
plt.ylabel('Waarnemingen')
plt.title('Verdeling van Laadtijd')

plt.show()

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

plt.show()

# Sort the data by ConnectedTime
sorted_data = laadpaalDf.sort_values('ConnectedTime')

# Calculate the trend line using linear regression
coefficients = np.polyfit(sorted_data['ConnectedTime'], sorted_data['Efficiency'], 1)
trend_line = np.poly1d(coefficients)

# Plot the scatter plot with smaller datapoints
plt.scatter(laadpaalDf['MaxPower'], laadpaalDf['TotalEnergy'], c=laadpaalDf['ConnectedTime'], cmap='cool', alpha=0.5, s=10)
plt.xlabel('ConnectedTime')
plt.ylabel('Efficiency')
plt.title('Scatter Plot of MaxPower vs Efficiency')
plt.colorbar(label='ConnectedTime')

# Plot the trend line
plt.plot(sorted_data['ConnectedTime'], trend_line(sorted_data['TotalEnergy']), color='red')

plt.ylim(0)  # Set the Y axis lower limit to 0

plt.show()

