# FDA_recall
## Introduction
The Department of Health and Human Services is the federal agency that oversees the United States Food and Drug Administration. The FDA is responsible for protecting and promoting public health through the control and supervision of food safety, tobacco products, dietary supplements, prescription and over-the-counter pharmaceutical drugs (medications), vaccines, biopharmaceuticals, blood transfusions, medical devices, electromagnetic radiation emitting devices (ERED).

## What is a food recall?
A food recall occurs when a food manufacturer withdraws a product from the market because they have reason to believe that it may cause consumer illness. In some circumstances, government agencies may request or require a food recall. Food recalls can have many reasons, including but not limited to:

Detection of organisms including bacteria such as Salmonella and parasites such as Cyclospora, find foreign objects such as broken glass or metal. Discovery of major allergens not listed on the product label.

A food recall is the removal from the market of food that violates US Food and Drug Administration (FDA) regulations. Food recalls are usually initiated voluntarily by the food manufacturer or distributor. In some cases, the FDA may request or order a recall. Although, the FDA database is comprehensive, it presents challenges to general public due to complex and technical interface.

## About this app
This app is designed to provide a easy to use user interface for checking the recent recalls enforced by the Food and Drug Administration (FDA). It also provides a visual analysis of the FDA’s recall history, presents trends and shows the most common recall reasons.

## Dataset
**Live update:** FDA live recalls in XML format used in this app is available at: https://www.fda.gov/media/145551/download. 

**Source:** The excel file used for this app can be dowloaded at: https://www.fda.gov/safety/recalls-market-withdrawals-safety-alerts. 

**Note:** The recall list is only Firm-issued recall dataset.

Excel file is read into the dataframe as below:
```
df = pd.read_excel('data/recalls.xlsx')
df["Date"] = df["Date"].astype('datetime64[ns]')
```
Alternately, the xml link can be parsed as such:
```
def getxml():
    url = "https://www.fda.gov/media/155924/download"
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    try:
        data = xmltodict.parse(response.data, encoding='utf-8')
    except:
        st.write("Failed to parse xml from response (%s)" % traceback.format_exc())
    return data
data = getxml()
dict_ = getxml()
label = dict_['recallsdata']['recalls']
df = pd.DataFrame(label)
df['Date'] = pd.to_datetime(df['Date'])
```
**Please note:** The XML parsing code is available in FDA_Recall_Status.py file but is commented out. Only the excel file based dataset is used.

## API_KEY
The ‘page’ UPC search uses RapidAPI access to enable ‘Edamam Food Database’. Ensure you enter your personal API_KEY=“PASSKEY” for the application to work as expected. Also, ensure to keep you personal API_KEY private and not share or make it public. One way is to make a .env file and enable .gitignore to prevent the .env file from being committed to the gitHub repository. A dummy .env is made available in the repository. Also, ensure that the the API_KEY added to the secret section of the Streamlit app available in the app's settings.

## Future work
The app is designed for point-of-use, such as grocery stores and or to quickly search the recalled products with minimal efforts. A barcode scanner is in works using the st.camera feature of the Streamlit app. ALthough, a QR code scanner has been successfully demonstrated there are some hurdles deploying it on the streamlit cloud. Also, the barcode scanner has been sub-optimal. Hopefully, these libraries will be updated for efficient immplementation in the Streamlit app in the future.

# Streamlit App
The Streamlit app is available at: https://rishipalb-fda-recall-fda-recall-search-edlw5f.streamlit.app/

## Disclaimer
This is app is for experimental and educational purpose only. The dataset may not be current and therefore would result in inaccurate and outdate information. The developer does not take any responsibility in the event of potential harm caused by the inadvertent use of this app.
