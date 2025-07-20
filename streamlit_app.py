# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Customize Your Smoothie! 🥤")
st.write("Choose the fruits you want in your custom Smoothie!")

cnx = st.connection('snowflake')
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
name_on_order = st.text_input("Name on Smoothie:")

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:', 
    my_dataframe, 
    max_selections=None
)

ingredients_str = ''

for fruits_chosen in ingredients_list:
    ingredients_str += fruits_chosen + ' '

my_insert_stmt = f"insert into smoothies.public.orders(ingredients, name_on_order) values ('{ingredients_str}', '{name_on_order}')"
time_to_insert = st.button('Submit Order')

if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")
