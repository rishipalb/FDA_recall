import streamlit as st
import pandas as pd
import numpy as np

st.markdown("# Search Product Recalls 🎉")
st.sidebar.markdown("# Search Options 🎉")

st.write('Results of custom search')
df = pd.read_excel('data/recalls.xlsx')
df["Date"] = pd.to_datetime(df["Date"])
df["Date"] = df["Date"].dt.strftime("%Y-%m-%d") #MMM DD, YYYY
#st.write(df)

product = st.sidebar.multiselect(
 'What are your favorite product type?', df['Product-Types'].unique())

brand = st.sidebar.multiselect('What are your favorite brand?', df['Brand-Names'].unique())

# Filter dataframe
new_df = df[(df['Product-Types'].isin(product)) & (df['Brand-Names'].isin(brand))]

# write dataframe to screen
st.write(new_df)

#text_1 = st.sidebar.text_input('Search keywords', 'Dole')
#new_df1 = df[(df['Product-Types'].isin(text_1)) & (df['Brand-Names'].isin(text_1))]
#st.write('Text input results:', new_df1)

text_1 = st.sidebar.text_input('Search keywords', 'Dole')
new_df1 = df[(df['Product-Types'].str.contains(text_1, case=False, na=False)) & (df['Brand-Names'].str.contains(text_1, case=False, na=False))]
st.write('Text input results:', new_df1)
