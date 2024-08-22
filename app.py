import streamlit as st
import pandas as pd
import pymysql

# Connect to MySQL database and fetch the data
def get_bus_data():
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        passwd='Appaamma@123',
        db='redbus_scrapd_data'
    )
    query = "SELECT * FROM bus_routes"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Initialize Streamlit app
st.set_page_config(page_title="Bus Routes Data", layout="wide")

# App title
st.title("🚌 Bus Routes Data Explorer 🚌")

# Introduction
st.markdown("""
Welcome to the Bus Routes Data Explorer! Use the filters in the sidebar to narrow down your search.
""")

# Load bus data
bus_data = get_bus_data()

# Sidebar filters
st.sidebar.header("Filter Bus Routes")
selected_bustype = st.sidebar.multiselect("Bus Type", bus_data['bus_type'].unique())
selected_route = st.sidebar.multiselect("Route", bus_data['route_name'].unique())
price_range = st.sidebar.slider("Price Range (₹)", int(bus_data['price'].min()), int(bus_data['price'].max()), (int(bus_data['price'].min()), int(bus_data['price'].max())))
star_rating = st.sidebar.slider("Minimum Star Rating", 0.0, 5.0, 3.0)
availability = st.sidebar.slider("Minimum Seats Available", 0, int(bus_data['seat_availability'].max()), 1)

# Filtering data based on user inputs
filtered_data = bus_data.copy()

if selected_bustype:
    filtered_data = filtered_data[filtered_data['bus_type'].isin(selected_bustype)]

if selected_route:
    filtered_data = filtered_data[filtered_data['route_name'].isin(selected_route)]

filtered_data = filtered_data[
    (filtered_data['price'] >= price_range[0]) & 
    (filtered_data['price'] <= price_range[1]) &
    (filtered_data['star_rating'] >= star_rating) &
    (filtered_data['seat_availability'] >= availability)
]

# Check if filtered data is empty
if filtered_data.empty:
    st.warning("No bus routes match the selected criteria. Please adjust the filters.")
else:
    # Display the filtered data
    st.markdown("### Filtered Bus Routes")
    st.dataframe(filtered_data)

    # Display some statistics
    st.markdown("### Statistics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Average Price (₹)", f"{filtered_data['price'].mean():.2f}")
    col2.metric("Average Star Rating", f"{filtered_data['star_rating'].mean():.2f}")
    col3.metric("Average Seats Available", f"{filtered_data['seat_availability'].mean():.0f}")

    # Add a download button for the filtered data
    st.markdown("### Download Data")
    csv = filtered_data.to_csv(index=False)
    st.download_button(label="Download as CSV", data=csv, file_name='filtered_bus_routes.csv', mime='text/csv')

# Footer
st.markdown("""
---
*Created with ⌨ by [Balamurugan Arunachalam]*
""")
