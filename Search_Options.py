import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt

st.markdown("# Search Product Recalls 🎉")
st.markdown("This app is designed to provide an easy-to-use user interface for checking the recent recalls enforced by the Food and Drug Administration (FDA). It also provides a visual analysis of the FDA’s recall history, presents trends and shows the most common recall reasons.")


st.markdown('## Search Options')
df = pd.read_excel('data/recalls.xlsx')
df["Date"] = df["Date"].astype('datetime64[ns]')
df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d") # MMM DD, YYYY
#st.write(df)

#Sidebars
st.sidebar.markdown('# Options')
today = dt.date.today()
start_date = st.sidebar.date_input("**Select a start date**",
    dt.date(2017, 1, 1))
end_date = st.sidebar.date_input("**Select an end date**",
    today)
st.sidebar.markdown("**Exclude terminated recalls?**")
st.sidebar.write("Select this option to remove recalls that were resolved or are no longer active.")
rem_terminated = st.sidebar.checkbox('Yes')

# CSS to inject contained in a string
hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """

# Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)

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

tab1, tab2 = st.tabs(['Keyword Search', 'Multi Search'])


with tab1:
    
    text_1 = st.text_input('**Search keywords**', '')
    st.info("**Example:** whole foods")
    if text_1 != '':
        new_df1 = df2[(df2['Product-Types'].str.contains(text_1, case=False, na=False)) | (df2['Brand-Names'].str.contains(text_1, case=False, na=False)) | (df2['Company-Name'].str.contains(text_1, case=False, na=False))| (df2['Product-Description'].str.contains(text_1, case=False, na=False)) | (df2['Recall-Reason-Description'].str.contains(text_1, case=False, na=False))].sort_values(by=['Date'], ascending=False)
        new_df1 = new_df1.sort_values(['Date'], ascending=[False])
        #st.markdown("# **Results of custom search** 🎉")
        #st.write('**Text input results:**', new_df1)
        if not new_df1.empty:
            # write dataframe to screen
            st.markdown("**Results of custom search** 🎉")
            st.table(new_df1)
        else:
            st.write("**Recall history:** Could not find a match.")

with tab2:
    df3 = df2.sort_values(['Brand-Names'], ascending=[True])
    product = st.multiselect('**What are your favorite product types?**', df3['Product-Types'].sort_values().unique())
    brand_df = df3[(df3['Product-Types'].isin(product))].sort_values(by=['Brand-Names'], ascending=True)
    brand = st.multiselect('**What are your favorite brand?**', brand_df['Brand-Names'].unique())

    # Filter dataframe
    new_df = brand_df[(brand_df['Brand-Names'].isin(brand))].sort_values(by=['Date'], ascending=False)
    if not new_df.empty:
        # write dataframe to screen
        st.markdown("Results of custom search 🎉")
        st.table(new_df)



st.info("**Disclaimer:** This is app is for experimental and educational purpose only. The dataset may not be current and therefore would result in inaccurate and outdate information. The developer does not take any responsibility in the event of potential harm caused by the inadvertent use of this app.")
