
# Redbus Project: Web Scraping and Data Analysis

## Overview

This project involves web scraping data from [Redbus](https://www.redbus.in/) using Selenium, storing the data in a database, and building a Streamlit application to visualize and filter the data. The project demonstrates how to extract, analyze, and present bus route information, including bus types, routes, prices, star ratings, and availability.


## Features

- **Web Scraping**: Automated data extraction from the Redbus website using Selenium.
- **Data Storage**: Scraped data stored in a SQLite database.
- **Interactive Dashboard**: A Streamlit application to filter and visualize bus route data.
- **Filtering Options**: Filter by bus type, route, price range, star rating, and availability.
- **SQL Queries**: Perform custom SQL queries to analyze the data.



## Tech Stack

- **Python**: Programming language for web scraping, data processing, and application development.
- **Selenium**: Tool for automating web browser interaction.
- **SQLite**: Database for storing the scraped data.
- **Streamlit**: Framework for building interactive web applications.
- **Pandas**: Library for data manipulation and analysis.


## Installation

To set up the project on your local machine, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/balamurugan-arunachalam/Redbus_Project.git
   
   cd redbus-project
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv env
   source env/bin/activate   # On Windows: env\Scripts\activate
   ```

3. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**:
   Ensure that your SQLite database is set up and the tables are created as per the schema provided.

5. **Run the Streamlit application**:
   ```bash
   streamlit run app.py
   ```
    
## Usage

1. **Web Scraping**:
   - Run the Selenium script to start scraping data from the Redbus website.
   - The scraped data will be stored in the SQLite database.

2. **Data Analysis**:
   - Use SQL queries to filter and analyze the data stored in the database.

3. **Streamlit Application**:
   - Access the Streamlit dashboard to visualize the data and apply various filters based on your requirements.

## Database Design

The database consists of tables that store information about buses, routes, prices, ratings, and availability. The schema is designed to allow efficient querying and filtering of data.

## Web Scraping Process

The Selenium script navigates through the Redbus website, extracts relevant data such as bus types, routes, prices, star ratings, and availability, and stores it in the SQLite database.

## Streamlit Application

The Streamlit app provides an interactive interface to visualize the bus data. Users can filter the data by bus type, route, price range, star rating, and availability.




## Screenshots

![Screenshot 2024-08-21 173237](https://github.com/user-attachments/assets/69bdc100-181f-4ca5-9c55-f41ec8cf5d82)


![Screenshot 2024-08-21 173328](https://github.com/user-attachments/assets/32ee002a-b853-47c8-bbff-9f8230b79ff9)


## Future Improvements

- **Additional Data Points**: Scrape more data points such as user reviews and bus facilities.
- **Real-Time Updates**: Implement real-time data scraping and updating the database.
- **Advanced Filtering**: Add more advanced filtering options to the Streamlit app.