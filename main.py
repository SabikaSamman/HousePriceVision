import streamlit as st
import json
import pickle
import numpy as np

# Function to load Json data from a file
with open('columns.json', 'r') as f:
    data=json.load(f)


#set the title of the page
st.set_page_config(page_title='My Web', layout='wide')
st.image("banner.jpg", width=100, use_column_width=True)
st.title('Welcome to My Web.')

selected_location= st.selectbox(
    'Select Desired Location',
    data['data_columns'][3:],
)
area=st.text_input('Enter the area of the house(in square feet)',value='1000')
bedrooms_bhk=st.text_input('Enter the number of BHK / Bedrooms' ,value='5')
bathrooms=st.text_input('Enter the number of Bathrooms' ,value='3')

# Load the pre-trained model
with open('home_prices_model.pickle', 'rb') as f:
    model= pickle.load(f)

def predict_price(location,sqft,bath,bhk):
    loc_index=np.where(np.array(data['data_columns']) == selected_location)[0][0]
    x=np.zeros(len(data['data_columns']))
    x[0]=sqft
    x[1]=bath
    x[2]=bhk
    if loc_index >=0:
        x[loc_index] =1
    #print(x)
    return model.predict([x])[0]



if st.button('Start Prediction'):
    try:
        area=float(area)
        bedrooms = int(bedrooms_bhk)
        bathrooms = int(bathrooms)
    except ValueError:
        st.warning('Please enter valid input')

    try:
        predicted_price=predict_price(selected_location,area,bathrooms,bedrooms_bhk)
        st.success(str(round(predicted_price,2))+' (IND LAKH)')
    except Exception:
        st.warning('Problem in model')

    


    #st.success('House Price is:*****')
#else:
#   st.error('There is a Problem: Try Later')


