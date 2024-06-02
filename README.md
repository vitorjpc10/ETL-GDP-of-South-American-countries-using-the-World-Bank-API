# GDP Data Pipeline

## Description
This project extracts GDP data for South American countries from the World Bank API and loads it into a PostgreSQL database. The data is then queried to produce a pivoted report for the last 5 years.

## Setup

### Prerequisites
- Docker
- Docker Compose

### Steps to Run

1. Clone the repository:
    ```bash
    git clone https://github.com/vitorjpc10/ETL-GDP-of-South-American-countries-using-the-World-Bank-API/tree/main
    cd ETL-GDP-of-South-American-countries-using-the-World-Bank-API
    ```

2. Build and run the Docker containers:
    ```bash
    docker-compose up --build
    ```

3. The data will be extracted and loaded, based on the logic from 'main.py', into the PostgreSQL database.

4. To generate the pivoted report, access the PostgreSQL database and execute the `query.sql` SQL File:
    ```bash
    docker exec -it etl-gdp-of-south-american-countries-using-the-world-bank-api-db-1 psql -U postgres -c "\i query.sql"
    ```

## Assumptions and Design Decisions
- The project uses Docker and Docker Compose for containerization and orchestration.
- The PostgreSQL database is used for data storage.
- Pure Python and SQL are used for data manipulation without the use of dataframes libraries.
- The World Bank API is assumed to return consistent and accurate data.

## Pivot Table Ouput Example:
![img.png](img.png)
