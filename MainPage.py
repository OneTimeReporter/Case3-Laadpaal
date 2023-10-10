#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import pandas as pd
import requests
from PIL import Image
from io import BytesIO

#Header Image aanroepen
response = requests.get("https://media.nhnieuws.nl/images/371192.799931d.jpg?width=1600&ratio=3:1&quality=70")
laadpaalheader = Image.open(BytesIO(response.content))

st.title("Case 3 - Gender Inequality Analyse")
st.subheader("Team 1: Ryan Stevens, Luuk Koppen, Timo Jansen, Tarik Kiliç")
st.image(laadpaalheader, caption="Vanaf 2030 wil de gemeente Amsterdam alle benzine- en dieselauto's weren binnen de ring A10")


st.write('''
Vanaf 2030 mogen nieuwe auto's in Nederland alleen volledig elektrisch zijn. 
''')







