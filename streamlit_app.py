# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Customize Your Smoothie! 🥤")
st.write("Choose the fruits you want in your custom Smoothie!")

cnx = st.connection('snowflake')
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
name_on_order = st.text_input("Name on Smoothie:")

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:', 
    my_dataframe, 
    max_selections=None
)

ingredients_str = ''

# Convert the Snowpark Dataframe to a Pandas Dataframe so we can use the LOC function
pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)

for fruit_chosen in ingredients_list:
    ingredients_str += fruit_chosen + ' '
    search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
    st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
    
    st.subheader(fruit_chosen + ' Nutrition Information')

    try:
        smoothiefroot_response = requests.get(f"https://fruityvice.com/api/fruit/{search_on}")
        data = smoothiefroot_response.json()
        sf_df = st.dataframe(data=data, use_container_width=True)
    except Exception as e:
         st.error(f"Something went wrong: {e}")
        

my_insert_stmt = f"insert into smoothies.public.orders(ingredients, name_on_order) values ('{ingredients_str}', '{name_on_order}')"
time_to_insert = st.button('Submit Order')

if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")

