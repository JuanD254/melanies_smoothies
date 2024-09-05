# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
from snowflake.snowpark.context import get_active_session

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """
    **Choose the fruits you want in your custom smoothie!**
    """
)
name_of_order = st.text_input("Name of Smoothie:")
st.write("The name of your Smoothie will be:", name_of_order)

session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

fruits_list = st.multiselect(
    "Choose up to 5 fruits:",
    my_dataframe,
    max_selections = 5
)

if fruits_list:    
    #st.write(fruits_list)
    #st.text(fruits_list)

    fruits_string = ''
    for fruit_chosen in fruits_list:
        fruits_string += fruit_chosen + ' '
        
    #st.write(fruits_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, NAME_ON_ORDER)
    values ('""" + fruits_string + """', '""" + name_of_order + """')"""

    #st.write(my_insert_stmt)
    
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
        
    st.stop()
