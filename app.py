import streamlit as st
import pymysql

# Function to filter options based on selected RTC type
def get_filtered_options(rtc_type=None):
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        passwd='Appaamma@123',
        db='redbus_scrapd_data'
    )
    cursor = conn.cursor()

    # Fetch bus types based on selected RTC type
    if rtc_type:
        cursor.execute("SELECT DISTINCT bus_type FROM bus_routes WHERE rtc_type IN ({})".format(
            ','.join(f"'{rt}'" for rt in rtc_type)))
        bus_types = [row[0] for row in cursor.fetchall()]
        
        cursor.execute("SELECT DISTINCT route_name FROM bus_routes WHERE rtc_type IN ({})".format(
            ','.join(f"'{rt}'" for rt in rtc_type)))
        route_names = [row[0] for row in cursor.fetchall()]
        
        cursor.execute("SELECT DISTINCT bus_name FROM bus_routes WHERE rtc_type IN ({})".format(
            ','.join(f"'{rt}'" for rt in rtc_type)))
        bus_names = [row[0] for row in cursor.fetchall()]
    else:
        cursor.execute("SELECT DISTINCT bus_type FROM bus_routes")
        bus_types = [row[0] for row in cursor.fetchall()]
        
        cursor.execute("SELECT DISTINCT route_name FROM bus_routes")
        route_names = [row[0] for row in cursor.fetchall()]
        
        cursor.execute("SELECT DISTINCT bus_name FROM bus_routes")
        bus_names = [row[0] for row in cursor.fetchall()]

    conn.close()

    return bus_types, route_names, bus_names

# Function to filter bus data based on user inputs
def get_filtered_bus_data(bus_type=None, route_name=None, bus_name=None, rtc_type=None, departing_time_range=None, reaching_time_range=None, price_min=None, price_max=None, star_rating_min=None, availability_min=None):
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        passwd='Appaamma@123',
        db='redbus_scrapd_data'
    )
    
    # Base query
    query = "SELECT * FROM bus_routes WHERE 1=1"
    
    # Dynamic filtering
    if bus_type:
        query += " AND bus_type IN ({})".format(','.join(f"'{bt}'" for bt in bus_type))
    
    if route_name:
        query += " AND route_name IN ({})".format(','.join(f"'{rn}'" for rn in route_name))
    
    if bus_name:
        query += " AND bus_name IN ({})".format(','.join(f"'{bn}'" for bn in bus_name))
    
    if rtc_type:
        query += " AND rtc_type IN ({})".format(','.join(f"'{rt}'" for rt in rtc_type))
    
    if departing_time_range and departing_time_range != 'Select a time range':
        if departing_time_range == 'Before 6 AM':
            query += " AND TIME(departing_time) < '06:00:00'"
        elif departing_time_range == '6 AM to 12 PM':
            query += " AND TIME(departing_time) BETWEEN '06:00:00' AND '11:59:59'"
        elif departing_time_range == '12 PM to 6 PM':
            query += " AND TIME(departing_time) BETWEEN '12:00:00' AND '17:59:59'"
        elif departing_time_range == 'After 6 PM':
            query += " AND TIME(departing_time) >= '18:00:00'"
    
    if reaching_time_range and reaching_time_range != 'Select a time range':
        if reaching_time_range == 'Before 6 AM':
            query += " AND TIME(reaching_time) < '06:00:00'"
        elif reaching_time_range == '6 AM to 12 PM':
            query += " AND TIME(reaching_time) BETWEEN '06:00:00' AND '11:59:59'"
        elif reaching_time_range == '12 PM to 6 PM':
            query += " AND TIME(reaching_time) BETWEEN '12:00:00' AND '17:59:59'"
        elif reaching_time_range == 'After 6 PM':
            query += " AND TIME(reaching_time) >= '18:00:00'"
    
    if price_min is not None and price_max is not None:
        query += f" AND price BETWEEN {price_min} AND {price_max}"
    
    if star_rating_min is not None:
        query += f" AND star_rating >= {star_rating_min}"
    
    if availability_min is not None:
        query += f" AND seat_availability >= {availability_min}"
    
    # Execute query
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    
    # Fetch column names
    column_names = [desc[0] for desc in cursor.description]

    conn.close()

    # Convert results to a list of dictionaries
    filtered_data = [dict(zip(column_names, row)) for row in results]

    return filtered_data

# Initialize Streamlit app
st.set_page_config(page_title="Bus Routes Data", layout="wide")

# App title
st.title("🚌 Bus Routes Data Explorer 🚌")

# Introduction
st.markdown("""
Welcome to the Bus Routes Data Explorer! Use the filters in the sidebar to narrow down your search.
""")

# Sidebar filters
st.sidebar.header("Filter Bus Routes")
conn = pymysql.connect(
    host='127.0.0.1',
    user='root',
    passwd='Appaamma@123',
    db='redbus_scrapd_data'
)
cursor = conn.cursor()

cursor.execute("SELECT DISTINCT rtc_type FROM bus_routes")
rtc_types = [row[0] for row in cursor.fetchall()]

conn.close()

selected_rtc_type = st.sidebar.multiselect("RTC Type", rtc_types)

# Update other filters based on selected RTC type
bus_types, route_names, bus_names = get_filtered_options(rtc_type=selected_rtc_type)

selected_bus_type = st.sidebar.multiselect("Bus Type", bus_types)
selected_route = st.sidebar.multiselect("Route", route_names)
selected_bus_name = st.sidebar.multiselect("Bus Name", bus_names)

# Time range selection for departing and arriving times using selectbox with an initial "Select a time range" option
departing_time_range = st.sidebar.selectbox(
    "Departure Time",
    ('Select a time range', 'Before 6 AM', '6 AM to 12 PM', '12 PM to 6 PM', 'After 6 PM')
)

reaching_time_range = st.sidebar.selectbox(
    "Arraiving Time",
    ('Select a time range', 'Before 6 AM', '6 AM to 12 PM', '12 PM to 6 PM', 'After 6 PM')
)

# Assuming that you want the full price range and availability directly from the database:
conn = pymysql.connect(
    host='127.0.0.1',
    user='root',
    passwd='Appaamma@123',
    db='redbus_scrapd_data'
)

cursor = conn.cursor()
cursor.execute("SELECT MIN(price), MAX(price) FROM bus_routes")
price_min, price_max = cursor.fetchone()

cursor.execute("SELECT MIN(seat_availability), MAX(seat_availability) FROM bus_routes")
availability_min, availability_max = cursor.fetchone()

conn.close()

price_range = st.sidebar.slider("Price Range (₹)", int(price_min), int(price_max), (int(price_min), int(price_max)))
star_rating = st.sidebar.slider("Minimum Star Rating", 0.0, 5.0, 3.0)
availability = st.sidebar.slider("Minimum Seats Available", 0, int(availability_max), 1)

# Get filtered data based on user inputs
filtered_data = get_filtered_bus_data(
    bus_type=selected_bus_type,
    route_name=selected_route,
    bus_name=selected_bus_name,
    rtc_type=selected_rtc_type,
    departing_time_range=departing_time_range,
    reaching_time_range=reaching_time_range,
    price_min=price_range[0],
    price_max=price_range[1],
    star_rating_min=star_rating,
    availability_min=availability
)

# Check if filtered data is empty
if not filtered_data:
    st.warning("No bus routes match the selected criteria. Please adjust the filters.")
else:
    # Display the filtered data
    st.dataframe(filtered_data)

# Footer
st.markdown("""
---
*Created with ⌨ by [Balamurugan Arunachalam]*
""")
