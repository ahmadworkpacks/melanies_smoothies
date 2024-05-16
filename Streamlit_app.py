# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Example StreamLit App")
st.write(
    """Choose the Fruits you want in your custome Smothie!
    """
)
name_on_order=st.text_input("Name on Smoothie:")
st.write("The Name of Smoothie will be:",name_on_order)
session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)
ingredientes_list=st.multiselect('Choose up to 5 ingredients',my_dataframe,max_selections=5)
if ingredientes_list:
    ingredients_string=' '
    for fruit in ingredientes_list:
        ingredients_string +=fruit + '  '
    time_to_insert=st.button('Submit Order')
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """' )"""
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")