# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize your Smoothie! ")
st.write("Choose your fruits you want in your custom smoothie!")
title = st.text_input(label="Name of smoothie", value="Melly Mel")
st.write("The current movie title is ", title)
session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))

ingredient_list = st.multiselect("Choose up to 5 ingredients",my_dataframe, max_selections=5)
if ingredient_list:
    st.write(ingredient_list)
    st.text(ingredient_list)
    ingredient_string = ""
    for fruit_choosen in ingredient_list:
        ingredient_string += fruit_choosen+" "
    st.write(ingredient_string)
    my_insert_stmt = f"insert into smoothies.public.orders (ingredients, name_on_order) values ('{ingredient_string}','{title}')"
    st.write(my_insert_stmt)
    time_to_insert = st.button("Submit order")
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f"Your smoothie is ordered, {title}")
