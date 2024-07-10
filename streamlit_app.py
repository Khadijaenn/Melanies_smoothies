# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import pandas as pd

# Write directly to the app
st.title("🥤 Customize Your Smoothie 🥤")
st.write("Choose the fruits you want in your custom Smoothie!")

# Input for name on order
name_on_order = st.text_input("Name On Smoothie")
st.write("The name on smoothie will be", name_on_order)

# Get Snowflake session
session = get_active_session()

# Fetch fruit options from the database
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME')).to_pandas()

# Multiselect for ingredients
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe['FRUIT_NAME'].tolist() 
    , max_selections = 6
)
# Button to submit the order
time_to_insert = st.button('Submit Order')

# Join selected ingredients into a single string
if time_to_insert and ingredients_list:
    ingredients_string = ', '.join(ingredients_list)

    # Construct the SQL insert statement safely
    my_insert_stmt = f"""INSERT INTO smoothies.public.orders (ingredients, name_on_order) 
                         VALUES ('{ingredients_string}', '{name_on_order}')"""

    # Execute the SQL statement using Snowflake session
    session.sql(my_insert_stmt).collect()

    # Show success message
    st.success('Your Smoothie is ordered!', icon="✅")
