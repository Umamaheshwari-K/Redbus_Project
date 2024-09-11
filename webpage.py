import streamlit as st
import pandas as pd
import mysql.connector
from streamlit_option_menu import option_menu

# Variables
host = 'localhost'
user = 'root'
password = 'Redbus_2024'
database = 'redbus_db'
table_name = 'busdata'
column1 = 'state'
column2 = 'route'
rating_column = 'rating'

# Function to connect to the MySQL database
def get_db_connection():
    return mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        auth_plugin= 'mysql_native_password'
    )

# Function to fetch distinct values for the first dropdown (State)
def fetch_first_dropdown_options():
    conn = get_db_connection()
    query = f"SELECT DISTINCT {column1} FROM {table_name}"
    df = pd.read_sql(query, conn)
    conn.close()
    return df[column1].tolist()

# Function to fetch distinct values for the second dropdown (Route) based on State
def fetch_second_dropdown_options(selected_value):
    conn = get_db_connection()
    query = f"""
    SELECT DISTINCT {column2}
    FROM {table_name}
    WHERE {column1} = %s
    """
    df = pd.read_sql(query, conn, params=(selected_value,))
    conn.close()
    return df[column2].tolist()

# Define predefined departure time ranges (in intervals of 6 hours)
def fetch_departure_time_ranges():
    return [
        "00:00 to 06:00",
        "06:00 to 12:00",
        "12:00 to 18:00",
        "18:00 to 24:00",
        "All Times"
    ]
    
# Function to fetch rating range options
def fetch_rating_options():
    return ["1 to 3", "3 to 4", "4 to 5", "all ratings"]

# Function to retrieve filtered data based on selections
def get_filtered_data(state, route, fare_range, rating_range, departure_time_range):
    conn = get_db_connection()
    
    # Define fare and rating conditions for the query
    fare_conditions = {
        "Upto 1000": "fare <= 1000",
        "Upto 2000": "fare <= 2000",
        "2000 and above": "fare >= 2000"
    }
    
    rating_conditions = {
        "1 to 3": f"{rating_column} BETWEEN 1 AND 3",
        "3 to 4": f"{rating_column} BETWEEN 3 AND 4",
        "4 to 5": f"{rating_column} BETWEEN 4 AND 5",
        "all ratings": f"{rating_column} BETWEEN 1 AND 5"
    }

    # Define time conditions based on selected departure time range
    time_conditions = ""
    if departure_time_range != "All Times":
        start_time, end_time = departure_time_range.split(" to ")
        time_conditions = f"AND departure >= '{start_time}' AND departure <= '{end_time}'"
        
    # SQL query to fetch data with filters
    query = f"""
    SELECT *
    FROM {table_name}
    WHERE {column1} = %s AND {column2} = %s AND {fare_conditions[fare_range]} 
    AND {rating_conditions[rating_range]} {time_conditions}
    """
    
    df = pd.read_sql(query, conn, params=(state, route))
    conn.close()
    return df

# Function to load additional data (if needed)
def load_data():
    conn = get_db_connection()
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Streamlit App Layout and Pages
st.set_page_config(page_title="RedBus Home Page", layout="wide")

# Creating a sidebar menu for navigation
with st.sidebar:
    st.image("C:/Users/Velum_aie1t0b/Desktop/redbus_project/logo/logo.jpg", use_column_width=100)
    web = option_menu(menu_title="RedBus Booking System",
                      options=["Project Overview", "Home", "States and Routes"],
                      icons=["info-circle", "house", "list"],
                      orientation="vertical",
                      default_index=0)

# Project Overview Page
if web == "Project Overview":
    st.title("__Redbus Data Scraping with Selenium & Dynamic Filtering using Streamlit__")
    st.subheader("Domain: Transportation")
    st.subheader("Objective:")
    st.markdown("""
    **The Redbus Data Scraping and Filtering with Streamlit Application** aims to revolutionize the transportation industry by providing a comprehensive solution.
    """)
    st.subheader("Overview:")
    st.markdown("""
    - **Python**: The core language used for developing the entire application.
    - **Selenium**: Tool used for web scraping to extract data from websites.
    - **Pandas**: For data manipulation and analysis.
    - **Streamlit**: Framework for building interactive web applications.
    - **MySQL**: SQL database used for the seamless integration of the dataset.
    """)
    st.subheader("Skills Acquired: Python, MySQL, Pandas, Selenium, Streamlit")
    st.markdown("Developed by: **Umamaheshwari Kaliappan**")
# Home Page
elif web == "Home":
    st.title("Welcome to RedBus Booking System")
    st.markdown("""
    **RedBus** is your one-stop solution for booking bus tickets with ease. Whether you're planning a trip within the city or across states, we've got you covered.
    """)
    st.markdown("""
    ### Features:
    - **Search Routes:** Find buses between cities quickly.
    - **Compare Fares:** View and compare prices for different routes.
    """)
    st.markdown("""
    ### Get Started:
    Use the sidebar to navigate:
    - **States and Routes:** Browse and filter bus routes by state and fare, rating, departure range.
    """)

# States and Routes Page
elif web == "States and Routes":
    st.header("States and Routes")
    
    # Fetch options for the first dropdown (State)
    first_dropdown_options = fetch_first_dropdown_options()

    # Create columns for the first two select boxes
    col1, col2 = st.columns(2)

    # Create the first dropdown (State)
    selected_state = col1.selectbox("Select State", first_dropdown_options)

    # Fetch options for the second dropdown (Route) based on the selected state
    second_dropdown_options = fetch_second_dropdown_options(selected_state)

    # Create the second dropdown (Route)
    selected_route = col2.selectbox("Select Route", second_dropdown_options)

    # Fare range options
    fare_range_options = {
        "Upto 1000": "Upto 1000",
        "Upto 2000": "Upto 2000",
        "2000 and above": "2000 and above"
    }

    # Fetch rating options and departure time ranges
    rating_options = fetch_rating_options()
    departure_time_ranges = fetch_departure_time_ranges()
    # Create columns for fare range, rating, and departure time range
    col3, col4, col5 = st.columns(3)

    # Fare range, rating range, and departure time range selection
    fare_range = col3.selectbox("Choose Bus Fare Range", list(fare_range_options.keys()))
    selected_rating_range = col4.selectbox("Select Rating Range", rating_options)
    selected_departure_time_range = col5.selectbox("Select Departure Time Range", departure_time_ranges)

    # If a route is selected, retrieve and display filtered data
    if selected_route:
        try:
            filtered_data = get_filtered_data(
                selected_state, selected_route, fare_range, 
                selected_rating_range, selected_departure_time_range
            )
            
            if not filtered_data.empty:
                st.write("Bus Details:")
                st.dataframe(filtered_data, use_container_width=True)
            else:
                st.write("No buses found for the selected criteria.")
        except mysql.connector.Error as err:
            st.write(f"Error: {err}")
    else:
        st.write("Please select a route to filter results.")
