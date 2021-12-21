#!/usr/bin/python3
# -*- coding: utf-8 -*-


import streamlit as st
import plotly.express as px
from PIL import Image
import pandas as pd


@st.cache
def load_data_co2():
    url = 'owid-co2-data.csv'
    return pd.read_csv(url)


@st.cache
def load_data_climate():
    url = 'Climate-data.csv'
    return pd.read_csv(url)

@st.cache
def load_net_zero():
    url = 'net-zero-target-set.csv'
    return pd.read_csv(url)

@st.cache
def load_temperature():
    url = 'temperature-anomaly.csv'
    return pd.read_csv(url)


st.set_page_config(layout="wide")

df_co2 = load_data_co2()

st.title('Global Warming and CO2 Emission')
st.markdown(
"""
As the extreme weather is sufferred world-wide, the importance of environment protection and net-zero achievement is highlighted by more and more countries.
By the end of 2021, 137 countries have committed to carbon neutrality which is tracked by [Energy and Climate Intelligence Unit](https://eciu.net/netzerotracker). 
Most of the target year of the commitments are centered around 2050. 
""")

st.header('Global Warming')
col1, space1, col2 = st.columns([9,1,9])

with col1:
    st.markdown("""
    A global temperature rise of 1$\degree$C seems to be a small case. However, in a geological context, a global-scale warming of 1$\degree$C in less
    than 150 years is an unusually large temperature change in a short span of time. It is also important to recognize the warming is not uniform globally. Land
    surface temperatures rise more than ocean temperatures. From the map shown on the right, the global average temperatures over land have risen about twice as 
    much as that over ocean. Compared to the 1951 - 1980 average, temperatures over land increased by around 1.3$\degree$C. An incredible news about global 
    warming occurred on December 14, 2021 that [WMO](https://public.wmo.int/en/media/press-release/wmo-recognizes-new-arctic-temperature-record-of-38%E2%81%B0c#:~:text=WMO%20recognizes%20new%20Arctic%20temperature%20record%20of%2038%E2%81%B0C%20%7C%20World%20Meteorological%20Organization) recognized new Arctic temperature record of 38$\degree$C.
    """)

with col2:
    fig1 = Image.open('berkeley-temp-anomaly-map.png')
    st.image(fig1, caption='Local temperatures in 2019 relative to average temperature in 1951-1980')

st.header('Global Temperature Trend')
st.markdown("""
    Over the last few decades, global temperature has risen sharply from 1990 - 2019. Generally, from 1850 to 2019, the average amount of temperature rise is about 
    1.1$\degree$C.
    """)
col3, space2, col4 = st.columns([9,1,9])

with col3:
    df_temp = load_temperature().query("Entity == 'Global'")
    fig2 = px.line(df_temp, x="Year", y=df_temp.columns[3:6],\
                title='Global Average Temperature Anomaly<br><sup>Global average land-sea temperature anomaly relative to the 1961-1990 average temperature</sup>')
    fig2.update_yaxes(title ='Degree Celsius')
    fig2.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.01
    ))
    st.plotly_chart(fig2, use_container_width=True)
    

st.header('CO2 Per Capita')
col5, space3, col6 = st.columns([9,1,9])
with col5:
    fig4 = px.choropleth(df_co2[df_co2['year'] == 2020], locations="iso_code",
                        color="co2_per_capita",
                        hover_name="country",
                        range_color=(0, 25),
                        color_continuous_scale=px.colors.sequential.Reds,
                        title= 'CO2 Emission World Map in 2020')
    st.plotly_chart(fig4, use_container_width=True)

with col6:
    default_countries = ['United States', 'United Kingdom', 'EU-27', 'China']
    countries = df_co2['country'].unique()
    options = st.multiselect('Country or Distinct', countries, default_countries)
    df3 = df_co2.query('country == @options')
    fig5 = px.line(df3, "year", "co2_per_capita", color="country")
    st.plotly_chart(fig5, use_container_width=True)


st.header('Countries with Net-Zero Emission Targets')
df_emission = load_net_zero()
fig7 = px.choropleth(df_emission, locations="Code",
                        color="Is there a net-zero target?",
                        hover_name="Entity"
                    )
st.plotly_chart(fig7, use_container_width=True)


st.header('Reference')
st.markdown("""
    [Our World in Data - CO2 Emission](https://ourworldindata.org/co2-emissions#licence)

    [Energy & Climate Intelligence Unit](https://eciu.net/netzerotracker)

    [United Nations - The 17 Goals](https://sdgs.un.org/goals)
    """)
