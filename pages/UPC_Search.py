import streamlit as st
import requests
import json
#import xmltodict
import pandas as pd
import cv2
import numpy as np
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")

st.markdown("# Product UPC Search")

df = pd.read_excel('recalls.xlsx')
df["Date"] = df["Date"].astype('datetime64[ns]')
df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d") # MMM DD, YYYY
#st.write(df)


def upc_check(upc_code):
    if upc_code != '':
        if len(upc_code) == 12:
            url = "https://edamam-food-and-grocery-database.p.rapidapi.com/parser"
            querystring = {"upc":upc_code}
            headers = {
                'x-rapidapi-key': API_KEY,
                'x-rapidapi-host': "edamam-food-and-grocery-database.p.rapidapi.com"
                }
            response = requests.request("GET", url, headers=headers, params=querystring)
            res = response.status_code
        
            if res == 200:
                st.write("Connection Success!")
                #st.write(response.text)
                data = response.json()
                label=data['hints'][0]["food"]["label"]
        
                #brand=data['hints'][0]["food"]["brand"]
                #if label !='':
                st.write("**Product Name:**", label)
                new_df1 = df[(df['Product-Description'].str.contains(label, case=False, na=False))].sort_values(by=['Date'], ascending=False)
                if not new_df1.empty:
                # write dataframe to screen
                    st.write("Test", new_df1)
                else:
                    st.write("**Recall history:** Could not find a match.")
            elif res != 200:
                st.write("**Error code:**", response.status_code, ". Try again or use another UPC code.")
        else:
            st.write("**Input error:** Please enter UPC code with 12 digits.")

tab1, tab2 = st.tabs(['Search UPC', 'Scan QR code'])
with tab1:
    st.markdown("## UPC Search")
    upc_check(st.text_input("**Enter UPC code:**"))
with tab2:
    st.markdown("## QR Scan")
    cam_on = st.checkbox("Turn camera on")
    
    if cam_on:
        image = st.camera_input("**Show QR code**")


        if image is not None:
            bytes_data = image.getvalue()
            cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

            detector = cv2.QRCodeDetector()

            data, bbox, straight_qrcode = detector.detectAndDecode(cv2_img)

            #st.write("Here!")
            st.write(data)
            upc_check(data)

st.write("**Example**: 046675013624, 046675013501.")
st.write("UPC search is powered by RapidAPI and Edamam-Food Database API.")
st.write("**Disclaimer**: This is app is for experimental and educational purpose only. The dataset may not be current and therefore would result in inaccurate and outdate information. The developer does not take any responsibility in the event of potential harm caused by the inadvertent use of this app.")