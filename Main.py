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
st.sidebar.markdown("# Recall Status 🎈")

def main_page():
    st.markdown("# Main page 🎈")
    st.sidebar.markdown("# Main page 🎈")

def page2():
    st.markdown("# Page 2 ❄️")
    st.sidebar.markdown("# Recall Search ❄️")

def page2():
    st.markdown("# Page 3 ❄️")
    st.sidebar.markdown("# Page 3 ❄️")




today = dt.date.today()
today_date = st.sidebar.date_input('Today:', today)
## Range selector
cols1,_ = st.columns((1,2)) # To make it narrower
format = 'MMM DD, YYYY'  # format output # strftime("%Y-%m-%d")
start_date = dt.date(year=2017,month=1,day=1)  #  I need some range in the past
end_date = dt.datetime.now().date()
max_days = end_date-start_date

#st.header("FDA Product Recalls")

df = pd.read_excel('data/recalls.xlsx')
df["Date"] = pd.to_datetime(df["Date"])
df["Date"] = df["Date"].dt.strftime("%Y-%m-%d") #MMM DD, YYYY
#st.write(df)
st.markdown("### Recent Recalls ❄️")
test_sort = df.sort_values(['Date'], ascending=[False])[:20]
#test_sort = pd.DataFrame('test_sort')
st.write(test_sort)

slider = st.sidebar.slider('Select the range in days', min_value=0, value=30, max_value=60)
selected_date=end_date -relativedelta(days=slider)
min_bar = st.sidebar.slider("Minimum bars for charts", 5, 100, 40, 1)
image_size = st.sidebar.slider("Word Cloud Image Width", 100, 800, 400, 10)
terminated = st.sidebar.checkbox('Terminated')

## Sanity check
#st.table(pd.DataFrame([[start_date, selected_date, end_date]],
#                      columns=['start',
#                               'selected',
#                               'end'],
#                      index=['date']))

# Select DataFrame rows between two dates using DataFrame.isin()
df2 = df[df["Date"].isin(pd.date_range(selected_date, end_date))]
#st.write(df2)


text = " ".join(review for review in df['Product-Types'].astype(str))


tab1, tab2 = st.tabs(['Bar Chart', 'Word Cloud'])

with tab1:
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

with tab2:
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
#'''
#df1 = df.groupby(['Product-Types'])['Product-Types'].count().reset_index(name='count').sort_values(by=['count'], ascending=False)[:min_bar]
#df1 = test_count.sort_values(by=['count'], ascending=False)[:min_bar]
#st.write(df1)
#st.markdown("### Most Recalled Brand Names1")
##brand_count = df.groupby(['Brand-Names'])['Brand-Names'].count().reset_index(name='count')
#search_count
#brand1 = alt.Chart(df1).mark_bar().encode(
#x=alt.X("Product-Types:O", sort='-y'),
#y='count:Q'
#)

#st.altair_chart(brand1) '''