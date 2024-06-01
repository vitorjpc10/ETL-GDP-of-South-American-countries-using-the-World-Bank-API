import requests
import os
import psycopg2

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

def load_data_to_db(data):
    print("Writing data to database...")
    # conn = psycopg2.connect(
    #     dbname=os.environ['DB_NAME'],
    #     user=os.environ['DB_USER'],
    #     password=os.environ['DB_PASSWORD'],
    #     host=os.environ['DB_HOST'],
    #     port=os.environ['DB_PORT']
    # )
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="admin",
        host="localhost",
        port="5432"
    )

    cur = conn.cursor()

    #! Drop gdp table if it exists (REMOVE)
    cur.execute('''
        DROP TABLE IF EXISTS gdp
    ''')

    #! Drop country table if it exists (REMOVE)
    cur.execute('''
        DROP TABLE IF EXISTS country
    ''')

    conn.commit()

    # Create country table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS country (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            iso3_code VARCHAR(3) UNIQUE
        )
    ''')

    conn.commit()

    # Create gdp table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS gdp (
            id SERIAL PRIMARY KEY,
            country_id INTEGER REFERENCES country(id),
            year INTEGER,
            value FLOAT
        )
    ''')

    conn.commit()


    # Extract country and gdp data from the API response
    countries = {item['country']['value']: item['countryiso3code'] for item in data}
    gdp_data = [(item['country']['value'], item['date'], item['value']) for item in data]

    # Insert unique countries into the country table
    for name, iso3_code in countries.items():
        cur.execute('''
            INSERT INTO country (name, iso3_code) VALUES (%s, %s) 
            ON CONFLICT (iso3_code) DO NOTHING
        ''', (name, iso3_code))
        conn.commit()

    # Insert gdp data into the gdp table
    for name, year, value in gdp_data:
        cur.execute('''
            INSERT INTO gdp (country_id, year, value)
            VALUES (
                (SELECT id FROM country WHERE name=%s), %s, %s
            )
        ''', (name, year, value))
        conn.commit()

    # Commit the transaction
    conn.commit()

    # Close the cursor and connection
    cur.close()
    conn.close()
    print("Successfully wrote data to database.")

if __name__ == "__main__":
    data = fetch_gdp_data()
    load_data_to_db(data)
