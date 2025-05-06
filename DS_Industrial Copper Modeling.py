import streamlit as st
import pickle
import numpy as np
from streamlit_option_menu import option_menu

# Function to load models
def load_model(file_path):
    try:
        with open(file_path, "rb") as f:
            model = pickle.load(f)
        return model
    except FileNotFoundError:
        st.error("Model file not found. Please check the file path.")
        return None

# Function to predict status
def predict_status(model, data):
    y_pred = model.predict(data)
    return y_pred

# Function to predict selling price
def predict_selling_price(model, data):
    y_pred = model.predict(data)
    ac_y_pred = np.exp(y_pred[0])
    return ac_y_pred

# Streamlit app
st.set_page_config(layout="wide")
st.title(":blue[**INDUSTRIAL COPPER MODELING**]")

with st.sidebar:
    option = option_menu('Main menu', options=["PREDICT SELLING PRICE", "PREDICT STATUS"])

if option == "PREDICT STATUS":
    st.header("PREDICT STATUS (Won / Lose)")
    st.write(" ")

    col1, col2 = st.columns(2)

    with col1:
        country = st.number_input(label="**Enter the Value for COUNTRY**/ Min:25.0, Max:113.0")
        item_type = st.number_input(label="**Enter the Value for ITEM TYPE**/ Min:0.0, Max:6.0")
        application = st.number_input(label="**Enter the Value for APPLICATION**/ Min:2.0, Max:87.5")
        width = st.number_input(label="**Enter the Value for WIDTH**/ Min:700.0, Max:1980.0")
        product_ref = st.number_input(label="**Enter the Value for PRODUCT_REF**/ Min:611728, Max:1722207579")
        quantity_tons_log = st.number_input(label="**Enter the Value for QUANTITY_TONS (Log Value)**/ Min:-0.322, Max:6.924", format="%0.15f")
        customer_log = st.number_input(label="**Enter the Value for CUSTOMER (Log Value)**/ Min:17.21910, Max:17.23015", format="%0.15f")
        thickness_log = st.number_input(label="**Enter the Value for THICKNESS (Log Value)**/ Min:-1.71479, Max:3.28154", format="%0.15f")
    
    with col2:
        selling_price_log = st.number_input(label="**Enter the Value for SELLING PRICE (Log Value)**/ Min:5.97503, Max:7.39036", format="%0.15f")
        item_date_day = st.selectbox("**Select the Day for ITEM DATE**", tuple(str(i) for i in range(1, 32)))
        item_date_month = st.selectbox("**Select the Month for ITEM DATE**", tuple(str(i) for i in range(1, 13)))
        item_date_year = st.selectbox("**Select the Year for ITEM DATE**", ("2020", "2021"))
        delivery_date_day = st.selectbox("**Select the Day for DELIVERY DATE**", tuple(str(i) for i in range(1, 32)))
        delivery_date_month = st.selectbox("**Select the Month for DELIVERY DATE**", tuple(str(i) for i in range(1, 13)))
        delivery_date_year = st.selectbox("**Select the Year for DELIVERY DATE**", ("2020", "2021", "2022"))

    button = st.button(":violet[***PREDICT THE STATUS***]", use_container_width=True)

    if button:
        model = load_model("F:/New folder (4)/GUVI_Project_5/output_data.pkl")
        if model:
            data = np.array([[country, item_type, application, width, product_ref, quantity_tons_log,
                              customer_log, thickness_log, selling_price_log, int(item_date_day), int(item_date_month),
                              int(item_date_year), int(delivery_date_day), int(delivery_date_month), int(delivery_date_year)]])
            status = predict_status(model, data)
            if status is not None:
                if status == 1:
                    st.write("## :green[**The Status is WON**]")
                else:
                    st.write("## :red[**The Status is LOSE**]")

if option == "PREDICT SELLING PRICE":
    st.header("**PREDICT SELLING PRICE**")
    st.write(" ")

    col1, col2 = st.columns(2)

    with col1:
        country = st.number_input(label="**Enter the Value for COUNTRY**/ Min:25.0, Max:113.0")
        status = st.number_input(label="**Enter the Value for STATUS**/ Min:0.0, Max:8.0")
        item_type = st.number_input(label="**Enter the Value for ITEM TYPE**/ Min:0.0, Max:6.0")
        application = st.number_input(label="**Enter the Value for APPLICATION**/ Min:2.0, Max:87.5")
        width = st.number_input(label="**Enter the Value for WIDTH**/ Min:700.0, Max:1980.0")
        product_ref = st.number_input(label="**Enter the Value for PRODUCT_REF**/ Min:611728, Max:1722207579")
        quantity_tons_log = st.number_input(label="**Enter the Value for QUANTITY_TONS (Log Value)**/ Min:-0.322, Max:6.924", format="%0.15f")
        customer_log = st.number_input(label="**Enter the Value for CUSTOMER (Log Value)**/ Min:17.21910, Max:17.23015", format="%0.15f")
    
    with col2:
        thickness_log = st.number_input(label="**Enter the Value for THICKNESS (Log Value)**/ Min:-1.71479, Max:3.28154", format="%0.15f")
        item_date_day = st.selectbox("**Select the Day for ITEM DATE**", tuple(str(i) for i in range(1, 32)))
        item_date_month = st.selectbox("**Select the Month for ITEM DATE**", tuple(str(i) for i in range(1, 13)))
        item_date_year = st.selectbox("**Select the Year for ITEM DATE**", ("2020", "2021"))
        delivery_date_day = st.selectbox("**Select the Day for DELIVERY DATE**", tuple(str(i) for i in range(1, 32)))
        delivery_date_month = st.selectbox("**Select the Month for DELIVERY DATE**", tuple(str(i) for i in range(1, 13)))
        delivery_date_year = st.selectbox("**Select the Year for DELIVERY DATE**", ("2020", "2021", "2022"))

    button = st.button(":violet[***PREDICT THE SELLING PRICE***]", use_container_width=True)

    if button:
        model = load_model("F:/New folder (4)/GUVI_Project_5/output_data.pkl")
        if model:
            data = np.array([[country, status, item_type, application, width, product_ref, quantity_tons_log,
                              customer_log, thickness_log, int(item_date_day), int(item_date_month),
                              int(item_date_year), int(delivery_date_day), int(delivery_date_month), int(delivery_date_year)]])
            price = predict_selling_price(model, data)
            if price is not None:
                st.write("## :green[**The Selling Price is :**]", price)
