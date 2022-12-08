import streamlit as st
import pandas as pd
import altair as alt
import datetime as dt
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
from dateutil.relativedelta import relativedelta # to add days or years

st.markdown("# FDA Product Recall 🎈")
st.markdown("FDA recalls in this app that is available @ https://www.fda.gov/media/145551/download. Source: https://www.fda.gov/about-fda/open-government-fda-data-sets/recalls-data-sets. Note: The recall list is only Firm-issued recall dataset.")

st.sidebar.markdown("# Recent Recall Status 🎈")

def main_page():
    st.markdown("# Main page 🎈")
    st.sidebar.markdown("# Main page 🎈")

def page2():
    st.markdown("# Page 2 ❄️")
    st.sidebar.markdown("# Recall Search ❄️")

def page2():
    st.markdown("# Page 3 ❄️")
    st.sidebar.markdown("# Page 3 ❄️")




#today_date = dt.date.today()
#today_date = st.sidebar.date_input('Today:', today)
## Range selector
cols1,_ = st.columns((1,2)) # To make it narrower
format = 'MMM DD, YYYY'  # format output # strftime("%Y-%m-%d")
start_date = dt.date(year=2017,month=1,day=1)  #  I need some range in the past
end_date = dt.datetime.now().date()
max_days = end_date-start_date

#st.header("FDA Product Recalls")

df = pd.read_excel('data/recalls.xlsx')
#df["Date"] = pd.to_datetime(df["Date"])
#df["Date"] = df["Date"].dt.strftime("%Y-%m-%d") #MMM DD, YYYY
df["Date"] = df["Date"].astype('datetime64[ns]')
df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d") # MMM DD, YYYY
#st.write(df.dtypes)
#st.write(df)

test_sort = df.sort_values(['Date'], ascending=[False])[:20]
#test_sort = pd.DataFrame('test_sort')
#st.write(test_sort)

slider = st.sidebar.slider('Select the range in days', min_value=0, value=30, max_value=60)
selected_date=end_date -relativedelta(days=slider)


# Sanity check
st.sidebar.table(pd.DataFrame([[selected_date, end_date]],
                      columns=['selected date',
                               'end date'],
                      index=['date']))

st.sidebar.markdown("# Historical data 🎈")
min_bar = st.sidebar.slider("Minimum bars for charts", 5, 40, 5, 1)
image_size = st.sidebar.slider("Word Cloud Image Width", 100, 800, 400, 10)
st.sidebar.markdown("Exclude terminated recalls?")
rem_terminated = st.sidebar.checkbox('Yes')

# Select DataFrame rows between two dates using DataFrame.isin()
#df2 = df[df["Date"].isin(pd.date_range(selected_date, end_date))]

# CSS to inject contained in a string
hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """

# Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)


if rem_terminated:
    df = df[(~df['Terminated Recall'].str.contains('Terminated', case=False, na=False))]

# Constrict dataframe between two dates    
df2 = df.query('Date > @selected_date and Date < @end_date')

# Join string from each row of a column
text = " ".join(review for review in df['Product-Types'].astype(str))


tab1, tab2, tab3 = st.tabs(['Recent Recalls', 'Bar Chart', 'Word Cloud'])
with tab1:
    st.markdown("### Recent Recalls ❄️")
    test_sort2 = df2.sort_values(['Date'], ascending=[False])
    st.table(test_sort2)
with tab2:
    # create two columns for charts
    fig_col1, fig_col2 = st.columns(2)
    with fig_col1:
        alt.data_transformers.disable_max_rows()
        st.markdown("### Most Recalled Product Types")
        type_count = df.groupby(['Product-Types'])['Product-Types'].count().reset_index(name='count').sort_values(by=['count'], ascending=False)[:min_bar]
        #search_count
        type = alt.Chart(type_count).mark_bar().encode(
        x='count:Q',
        y=alt.Y("Product-Types:O", sort='-x')
        )
        st.altair_chart(type)

    with fig_col2:
        alt.data_transformers.disable_max_rows()
        st.markdown("### Most Recalled Brand Names")
        brand_count = df.groupby(['Brand-Names'])['Brand-Names'].count().reset_index(name='count').sort_values(by=['count'], ascending=False)[:min_bar]
        #search_count
        brand = alt.Chart(brand_count).mark_bar().encode(
        x='count:Q',
        y=alt.Y("Brand-Names:O", sort='-x')
        )
        st.altair_chart(brand)
        st.write(brand_count.iloc[0:1,0:1])
    st.write('* Results shown above are for historical data.')
with tab3:
    st.markdown("### Word cloud of Product-Types")
    text = " ".join(review for review in df['Product-Types'].astype(str))
    
    stopwords = set(STOPWORDS)
    stopwords.update(["Food & Beverages,"])
    cloud = WordCloud(stopwords=stopwords, background_color="white", width=800, height=400)
    wc = cloud.generate(text)
    word_cloud = cloud.to_file('wordcloud.png')
    st.image(wc.to_array(), width=image_size)
    st.write("There are {} words in the combination of all cells in column Product-Types.".format(len(text)))
    
    
    st.markdown("### Word cloud of Recall-Reason-Description")
    text1 = " ".join(review for review in df['Recall-Reason-Description'].astype(str))
    cloud1 = WordCloud(stopwords=stopwords, background_color="yellow", width=800, height=400)
    wc1 = cloud1.generate(text1)
    word_cloud1 = wc1.to_file('wordcloud1.png')
    st.image(word_cloud1.to_array(), width=image_size)
    st.write("There are {} words in the combination of all cells in column Recall-Reason-Description.".format(len(text1)))
    #st.write(wc1.words_.keys())
    st.write('* Results shown above are for historical data.')

st.write("**Disclaimer:** This is app is for experimental and educational purpose only. The dataset may not be current and therefore would result in inaccurate and outdate information. The developer does not take any responsibility in the event of potential harm caused by the inadvertent use of this app.")

    

