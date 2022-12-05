import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt

st.markdown("# Search Product Recalls 🎉")


st.markdown('## Search Options')
df = pd.read_excel('data/recalls.xlsx')
df["Date"] = df["Date"].astype('datetime64[ns]')
df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d") # MMM DD, YYYY
#st.write(df)

#Sidebars
st.sidebar.markdown('# Options')
today = dt.date.today()
start_date = st.sidebar.date_input("Select a start date",
    dt.date(2017, 1, 1))
end_date = st.sidebar.date_input("Select an end date",
    today)
st.sidebar.markdown("Exclude terminated recalls?")
rem_terminated = st.sidebar.checkbox('Yes')

#Set dates
df2 = df.query('Date > @start_date and Date < @end_date')
df2_sort = df2.sort_values(['Date'], ascending=[False])
#st.write(df2_sort)

#Apply terminated search conditions
if rem_terminated:
    df2 = df2[(~df2['Terminated Recall'].str.contains('Terminated', case=False, na=False))]
    #st.write(df2)
else: 
#df2 = df.query('Date > @selected_date and Date < @end_date')
    df2 = df2.sort_values(['Date'], ascending=[False])
    #st.write(test_sort2)

#Check to verify the terminated sidebar
#st.write(df2)

tab1, tab2 = st.tabs(['Multi Search', 'Keyword Search'])

with tab1:
    df3 = df2.sort_values(['Brand-Names'], ascending=[True])
    product = st.multiselect(
    '**What are your favorite product type?**', df2['Product-Types'].unique())

    brand = st.multiselect('**What are your favorite brand?**', df3['Brand-Names'].unique())

    # Filter dataframe
    new_df = df2[(df2['Product-Types'].isin(product)) & (df2['Brand-Names'].isin(brand))].sort_values(by=['Date'], ascending=False)
    if not new_df.empty:
        # write dataframe to screen
        st.markdown("Results of custom search 🎉")
        st.write(new_df)

#text_1 = st.sidebar.text_input('Search keywords', 'Dole')
#new_df1 = df[(df['Product-Types'].isin(text_1)) & (df['Brand-Names'].isin(text_1))]
#st.write('Text input results:', new_df1)
with tab2:
    st.markdown("Results of custom search 🎉")
    text_1 = st.text_input('**Search keywords**', '')
    if text_1 != '':
        new_df1 = df2[(df2['Product-Types'].str.contains(text_1, case=False, na=False)) | (df2['Brand-Names'].str.contains(text_1, case=False, na=False)) | (df2['Recall-Reason-Description'].str.contains(text_1, case=False, na=False))].sort_values(by=['Date'], ascending=False)
        st.markdown("# **Results of custom search** 🎉")
        st.write('**Text input results:**', new_df1)

st.write("**Example:** whole foods")

st.write("**Disclaimer:** This is app is for experimental and educational purpose only. The dataset may not be current and therefore would result in inaccurate and outdate information. The developer does not take any responsibility in the event of potential harm caused by the inadvertent use of this app.")
