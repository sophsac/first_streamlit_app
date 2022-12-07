import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Menu')

streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page
streamlit.dataframe(fruits_to_show)

# create a repeatable code block / function
def get_fruityvice_data(this_fruit_choice):
  # import requests
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
  # streamlit.text(fruityvice_response.json()) # just writes the data to the screen
  # take the json version of the fruityvice_response and normalise it 
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized
  
# new section to display fruityvice api response
streamlit.header('Fruityvice Fruit Advice!')
try:
  # adds text entry box and sends the input to fruityvice as part of API call
  fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else: 
    back_from_function = get_fruityvice_data(fruit_choice)
    # creates dataframe of normalised fruityvice_response
    streamlit.dataframe(back_from_function)
    
except URLError as e:
  streamlit.error()

# dont run anything past here while we troubleshoot
#streamlit.stop()

# tells py file to use the library (Requirements) that's been added to the project
# import snowflake.connector

streamlit.header("The fruit load list contains:")
# snowflake-related functions
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * from fruit_load_list")
    return my_cur.fetchall()
 
# add a button to load the fruit
if streamlit.button('Get Fruit Load List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  streamlit.dataframe(my_data_rows)
  
# allow user to add fruit to the list
def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into fruit_load_list values ('from streamlist')")
    return "Thanks for adding " + new_fruit + "!"
  
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a Fruit to the List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_function = insert_row_snowflake(add_my_fruit)
  streamlit.text(back_from_function)

# will not work correctly initially
# my_cur.execute("insert into fruit_load_list values ('from streamlist')")
