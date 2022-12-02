import streamlit as st
upc_code = st.text_input("Enter UPC code:")
import requests
import json
#import xmltodict

if upc_code != '':
    url = "https://edamam-food-and-grocery-database.p.rapidapi.com/parser"
    querystring = {"upc":upc_code}
    headers = {
        'x-rapidapi-key': "d0d8d22272msh0680aab1bc4db91p13c138jsn0fd6ead00eeb",
        'x-rapidapi-host': "edamam-food-and-grocery-database.p.rapidapi.com"
        }
    response = requests.request("GET", url, headers=headers, params=querystring)
    #st.write(response.text)
    data = response.json()
    label=data['hints'][0]["food"]["label"]
    brand=data['hints'][0]["food"]["brand"]
    st.write(label,", ", brand)
#    with open(response,'r') as y:
    #response_text = response.text
    #response_dict = json.dumps(xmltodict.parse(response_text))
    #y=response_dict
    #y=pd.read_json(response.text)
#print(y)
#        t=y["hints"]
#        s=t[0]
#        r=s["food"]
#        print(r["label"])
#        print(r["brand"])

    #y=response.text
#t=y["hints"]
#    s=t[0]
#    r=s["food"]
#    st.write(r["label"])

st.write("Example: 046675013624")