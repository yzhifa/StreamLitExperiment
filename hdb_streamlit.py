import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import altair as alt

# 1 sqm = 10.7 sqft
sqm_sqft = 10.7

fileLoc = r"C:\Users\ZF\Documents\Streamlit Project"

csv_name = "resale-flat-prices-based-on-registration-date-from-jan-2017-onwards.csv"

df = pd.read_csv(csv_name)
df["_year"] = df["month"].apply(lambda x: x[:4])
df["_month"] = df["month"].apply(lambda x: x[-2:])
df["_psf"] = df['resale_price']/(df["floor_area_sqm"]*sqm_sqft)

# Dimension 1 -- Select town
dim_towns = sorted(np.unique(df["town"]))

# Sidebar
with st.sidebar:
    st.header("Sidebar here")
    selected_town = st.selectbox("Select a town", dim_towns)

# Filter 1
filter_town = df["town"] == selected_town

# New dataframe based on selected town
df2 = df[filter_town].copy()

# Dimensions 2 -- based on selected town
dim_storeyRange = sorted(np.unique(df2["storey_range"]))
dim_flatType = sorted(np.unique(df2["flat_type"]))
dim_floorArea = sorted(np.unique(df2["floor_area_sqm"]))
# dim_flatType = sorted(np.unique(df2["flat_type"]))

# Sidebar
with st.sidebar:
    st.header("Sidebar here")
    selected_storeyRange = st.selectbox("Select storey range", dim_storeyRange)
    selected_flatType = st.selectbox("Select a flat type", dim_flatType)
    # selected_floorArea = st.selectbox("Select a floor area (sqm)", dim_floorArea)

filter = (df2["storey_range"] == selected_storeyRange) & \
        (df2["flat_type"] == selected_flatType)

# Outputs

# Title
st.header("HDB Resale Prices from 2017")

tab_a, tab0, tab1 = st.tabs(["Quick Stats", "Trends", "Details"])

with tab_a:
    st.write("Slicers cannot be applied in this tab")

    st.header("Prices by Town")
    st.bar_chart(df.groupby(by=["_year", "town"])["resale_price"].mean().unstack(level=0))

    st.header("Transactions by Town")
    st.bar_chart(df.groupby(by=["_year", "town"])["resale_price"].count().unstack(level=0))

with tab0:
    st.write("Slicers cannot be applied in this tab")
    
    st.header("Resale Price Trend")
    st.line_chart(df.groupby(by="_year")["resale_price"].mean())

    st.header("PSF Trend")
    st.line_chart(df.groupby(by="_year")["_psf"].mean())

    st.header("Count of Transactions")
    st.line_chart(df.groupby(by="_year")["_psf"].count())


with tab1:

    st.title("Trends for " + selected_town + f" ({selected_flatType}, {selected_storeyRange} Storey")

    # Price trends
    st.header("Price Trends")
    st.line_chart(df2[filter].groupby(by="_year")["resale_price"].mean())
    
    st.header("PSF Trends")
    st.line_chart(df2[filter].groupby(by="_year")["_psf"].mean())
    
    st.header("Transaction Trends")
    st.line_chart(df2[filter].groupby(by="_year")["_psf"].count())
    

    # Misc
    st.header("Price by Storey Range")
    df3 = df2.groupby(by=["_year", "storey_range"])["resale_price"].mean()\
            .unstack(level=1)

    st.bar_chart(df3)


