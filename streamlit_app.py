# Import python packages
import requests
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie with 5 ingredients! :cup_with_straw:")
st.write(
    """
    **Choose the fruits you want in your custom smoothie!**
    """
)
name_of_order = st.text_input("Name of Smoothie:")
st.write("The name of your Smoothie will be:", name_of_order)

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
st.dataframe(data=my_dataframe, use_container_width=True)
st.stop()

fruits_list = st.multiselect(
    "Choose up to 5 fruits:",
    my_dataframe,
    max_selections = 6
)

if fruits_list:    
    #st.write(fruits_list)
    #st.text(fruits_list)

    fruits_string = ''
    for fruit_chosen in fruits_list:
        fruits_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + ' Nutrition information')
        fruityvice_response = requests.get("https://www.fruityvice.com/api/fruit/" + fruit_chosen)
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
        
    #st.write(fruits_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, NAME_ON_ORDER)
    values ('""" + fruits_string + """', '""" + name_of_order + """')"""

    #st.write(my_insert_stmt)
    
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
        
    st.stop()

