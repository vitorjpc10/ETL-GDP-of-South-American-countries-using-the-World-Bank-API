import requests
import os
import psycopg2
from tabulate import tabulate


def fetch_gdp_data():
    print("Fetching data from World Bank API...")

    #? Increased per_page size to minimize possible number of requests based on possible pagination
    base_url = "https://api.worldbank.org/v2/country/ARG;BOL;BRA;CHL;COL;ECU;GUY;PRY;PER;SUR;URY;VEN/indicator/NY.GDP.MKTP.CD?format=json&per_page=1000&page={page}"

    # Fetch the first page to determine the total number of pages
    response = requests.get(base_url.format(page=1))
    if response.status_code != 200:
        raise Exception("Failed to fetch data from World Bank API")

    data = response.json()
    if len(data) < 2:
        raise Exception("Unexpected API response format. Expecting pagination details and country info list.")

    combined_data = data[1]  # Start with the data from the first page
    total_pages = data[0]['pages']

    # Fetch data from subsequent pages if there are more than one page
    for page in range(2, total_pages + 1):
        response = requests.get(base_url.format(page=page))
        if response.status_code != 200:
            raise Exception(f"Failed to fetch data from World Bank API on page {page}")

        page_data = response.json()
        if len(page_data) < 2:
            raise Exception(f"Unexpected API response format on page {page}. Expecting pagination details and country info list.")

        combined_data.extend(page_data[1])

    print("Successfully fetched data from World Bank API.")
    return combined_data

def load_data_to_db(data, db_connection):
    print("Writing data to database...")

    cursor = db_connection.cursor()

    # Create country table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS country (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            iso3_code VARCHAR(3) UNIQUE
        )
    ''')

    # Create gdp table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gdp (
            id SERIAL PRIMARY KEY,
            country_id INTEGER REFERENCES country(id),
            year INTEGER,
            value FLOAT
        )
    ''')


    # Extract country and gdp data from the API response
    countries = {item['country']['value']: item['countryiso3code'] for item in data}
    gdp_data = [(item['country']['value'], item['date'], item['value']) for item in data]

    # Insert unique countries into the country table
    for name, iso3_code in countries.items():
        cursor.execute('''
            INSERT INTO country (name, iso3_code) VALUES (%s, %s) 
            ON CONFLICT (iso3_code) DO NOTHING
        ''', (name, iso3_code))

    # Insert gdp data into the gdp table
    for name, year, value in gdp_data:
        cursor.execute('''
            INSERT INTO gdp (country_id, year, value)
            VALUES (
                (SELECT id FROM country WHERE name=%s), %s, %s
            )
        ''', (name, year, value))

    # Commit the transaction
    db_connection.commit()

    # Close the cursor
    cursor.close()
    print("Successfully wrote data to database.")

def run_query_from_file(query_file_path, db_connection):
    cursor = db_connection.cursor()

    with open(query_file_path, 'r') as file:
        query = file.read()

    cursor.execute(query)
    results = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    print(f"Running Query from file: {query_file_path}")
    print(tabulate(results, headers=columns, tablefmt='psql'))

    cursor.close()

if __name__ == "__main__":
    # Fetch GDP data from the World Bank API
    data = fetch_gdp_data()

    # Connect to the PostgreSQL database using the provided credentials
    db_connection = psycopg2.connect(
        dbname=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD'],
        host=os.environ['DB_HOST'],
        port=os.environ['DB_PORT']
    )

    # Load the fetched data into the PostgreSQL database
    load_data_to_db(data, db_connection)

    # Run the query from the provided SQL file and output the results
    run_query_from_file("query.sql", db_connection)

    # Close the database connection
    db_connection.close()
