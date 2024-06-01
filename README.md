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
    git clone https://github.com/yourusername/gdp_data_pipeline.git !Change this!!!
    cd gdp_data_pipeline
    ```

2. Build and run the Docker containers:
    ```bash
    docker-compose up --build
    ```

3. The data will be extracted and loaded into the PostgreSQL database.

4. To generate the pivoted report, access the PostgreSQL database and execute the `query.sql` script:
    ```bash
    docker exec -it gdp_data_pipeline_db_1 psql -U user
    ```
5. Once inside the database you can run the SQL query (see how i can change the docker compose to include copy of sql file)
Also change main you run and output sql query as well from file

## Assumptions and Design Decisions
- The project uses Docker and Docker Compose for containerization and orchestration.
- The PostgreSQL database is used for data storage.
- Pure Python and SQL are used for data manipulation without the use of dataframes libraries.
- The World Bank API is assumed to return consistent and accurate data.
