# Local LLM + Database (Postgres) Playground

A minimal, provider‑agnostic pipeline that turns natural‑language questions into safe SQL for a local Postgres database, runs the query, and prints nicely formatted results. The project is structured so you can plug in different LLM or DB providers with minimal changes.

Key capabilities:
- LLM‑to‑SQL pipeline with schema/context awareness and sample‑data hints.
- Strict SQL safety validation (single SELECT only; blocks DDL/DML, CTEs, etc.).
- Provider‑agnostic abstractions for LLMs and databases.
- Docker Compose for local Postgres and a script to seed the Northwind dataset.


## Project layout
- common/ — config and helpers (env loading, printing tables)
- db/ — provider‑agnostic DB client Protocol and a Postgres implementation
- llm/ — provider‑agnostic LLM client Protocol, prompts, pipeline, validation
- test_data/ — the Northwind SQL dump used for seeding
- docker-compose.yml — Postgres service
- setup_local.sh — start Docker + seed DB
- run.sh — prompt for a question and run the app
- main.py — CLI entry point for a single question

The LLM and DB layers are pluggable:
- LLM providers live under llm/providers/<provider>/ (Gemini included)
- DB providers live under db/providers/<provider>/ (Postgres included)

For a deeper architectural overview and refactor plan, see docs/LLM_STRUCTURE.md (if present).


## Prerequisites
- Docker (Docker Desktop) with docker compose
- Python 3.10+
- A Google Gemini API key (for the default LLM provider)


## Quick start

1) Clone and set up environment
- Copy the example env file and adjust values as needed:

  cp .env.example .env

- The defaults in .env.example are:
  - DB_PROVIDER=POSTGRES
  - LLM_PROVIDER=GEMINI
  - DB_HOST=127.0.0.1
  - DB_PORT=5433
  - DB_NAME=local_llm
  - DB_USER=local_llm
  - DB_PASSWORD=local_llm
  - GEMINI_API_KEY=REPLACE_WITH_YOUR_KEY

2) Start Postgres and seed Northwind

  ./setup_local.sh

By default this seeds test_data/northwind.sql into the Postgres container local-llm-postgres created by docker-compose.yml. You can pass a custom SQL file path:

  ./setup_local.sh path/to/your_dump.sql

3) Install Python dependencies
Use the provided requirements.txt:

  python3 -m venv .venv && source .venv/bin/activate
  pip install --upgrade pip
  pip install -r requirements.txt

Notes:
- psycopg2-binary is recommended for local development convenience. If you prefer building from source, install psycopg2 and ensure libpq is available.

4) Run the app
- Interactive prompt:

  ./run.sh

- Or pass a question directly:

  python3 main.py "List the top 5 customers by total order amount"

The app will:
- Introspect the database schema and data samples.
- Ask the LLM to propose tables for sample extraction (optional context boost).
- Ask the LLM to generate a single safe SELECT.
- Validate the SQL for safety.
- Execute it against Postgres and print results with an optional "Notes" section.


## Environment variables
The application loads variables from your .env using python-dotenv. Summary:

- DB_PROVIDER: Which DB provider to use. Default: POSTGRES (currently supported).
- LLM_PROVIDER: Which LLM provider to use. Default: GEMINI (currently supported).
- DB_HOST: Host to connect to (from your machine). Default: 127.0.0.1.
- DB_PORT: Port to connect to (host port published by docker-compose). Default: 5433.
- DB_NAME: Database name inside Postgres.
- DB_USER: Database user.
- DB_PASSWORD: Database user password.
- GEMINI_API_KEY: Your Google Gemini API key.

docker-compose.yml uses DB_NAME, DB_USER, DB_PASSWORD for the container’s initial database/user. The app uses the same values to connect via DB_HOST/DB_PORT.


## Scripts
- setup_local.sh — Start Docker services and seed the DB with Northwind (or a provided SQL file). It will wait until Postgres is ready and then apply the SQL inside the container.
- run.sh — Prompt for a natural‑language question and run the pipeline end‑to‑end.


## Extensibility notes
- To add another LLM provider, implement llm/core/client.py’s LLMClient protocol and register it in llm/run.py next to GeminiClient.
- To add another DB provider, implement db/core/client.py’s DatabaseClient protocol and register it in db/service.py.
- Prompts live in llm/prompt/, and the orchestration pipeline is in llm/pipelines/text_to_sql.py.
- SQL safety rules live in llm/validate.py.


## License
This repository is provided as‑is, for local experimentation and development.

## Prompt example

```
Prompt: give me all orders where city is boise

Notes: Step 1: The user wants 'all orders', which translates to selecting all columns (`*`) from the `orders` table.
Step 2: The filtering condition is 'where city is boise'. I identified the `ship_city` column in the `orders` table as the relevant column for the city of an order. I will filter using `WHERE ship_city = 'Boise'`.
Step 3: No specific limit or ordering was requested, so the query will return all matching rows.

SQL: SELECT * FROM orders WHERE ship_city = 'Boise'

order_id | customer_id | employee_id | order_date | required_date | shipped_date | ship_via | freight | ship_name          | ship_address    | ship_city | ship_region | ship_postal_code | ship_country
---------+-------------+-------------+------------+---------------+--------------+----------+---------+--------------------+-----------------+-----------+-------------+------------------+-------------
   10324 | SAVEA       |           9 | 1996-10-08 | 1996-11-05    | 1996-10-10   |        1 |  214.27 | Save-a-lot Markets | 187 Suffolk Ln. | Boise     | ID          | 83720            | USA         
   10393 | SAVEA       |           1 | 1996-12-25 | 1997-01-22    | 1997-01-03   |        3 |  126.56 | Save-a-lot Markets | 187 Suffolk Ln. | Boise     | ID          | 83720            | USA         
   10398 | SAVEA       |           2 | 1996-12-30 | 1997-01-27    | 1997-01-09   |        3 |   89.16 | Save-a-lot Markets | 187 Suffolk Ln. | Boise     | ID          | 83720            | USA         
   10440 | SAVEA       |           4 | 1997-02-10 | 1997-03-10    | 1997-02-28   |        2 |   86.53 | Save-a-lot Markets | 187 Suffolk Ln. | Boise     | ID          | 83720            | USA         
   10452 | SAVEA       |           8 | 1997-02-20 | 1997-03-20    | 1997-02-26   |        1 |  140.26 | Save-a-lot Markets | 187 Suffolk Ln. | Boise     | ID          | 83720            | USA         
   10510 | SAVEA       |           6 | 1997-04-18 | 1997-05-16    | 1997-04-28   |        3 |  367.63 | Save-a-lot Markets | 187 Suffolk Ln. | Boise     | ID          | 83720            | USA         
   10555 | SAVEA       |           6 | 1997-06-02 | 1997-06-30    | 1997-06-04   |        3 |  252.49 | Save-a-lot Markets | 187 Suffolk Ln. | Boise     | ID          | 83720            | USA         
   10603 | SAVEA       |           8 | 1997-07-18 | 1997-08-15    | 1997-08-08   |        2 |   48.77 | Save-a-lot Markets | 187 Suffolk Ln. | Boise     | ID          | 83720            | USA         
   10607 | SAVEA       |           5 | 1997-07-22 | 1997-08-19    | 1997-07-25   |        1 |  200.24 | Save-a-lot Markets | 187 Suffolk Ln. | Boise     | ID          | 83720            | USA         
   10612 | SAVEA       |           1 | 1997-07-28 | 1997-08-25    | 1997-08-01   |        2 |  544.08 | Save-a-lot Markets | 187 Suffolk Ln. | Boise     | ID          | 83720            | USA         
   10627 | SAVEA       |           8 | 1997-08-11 | 1997-09-22    | 1997-08-21   |        3 |  107.46 | Save-a-lot Markets | 187 Suffolk Ln. | Boise     | ID          | 83720            | USA         
   10657 | SAVEA       |           2 | 1997-09-04 | 1997-10-02    | 1997-09-15   |        2 |  352.69 | Save-a-lot Markets | 187 Suffolk Ln. | Boise     | ID          | 83720            | USA         
   10678 | SAVEA       |           7 | 1997-09-23 | 1997-10-21    | 1997-10-16   |        3 |  388.98 | Save-a-lot Markets | 187 Suffolk Ln. | Boise     | ID          | 83720            | USA         
   10700 | SAVEA       |           3 | 1997-10-10 | 1997-11-07    | 1997-10-16   |        1 |    65.1 | Save-a-lot Markets | 187 Suffolk Ln. | Boise     | ID          | 83720            | USA         
   10711 | SAVEA       |           5 | 1997-10-21 | 1997-12-02    | 1997-10-29   |        2 |   52.41 | Save-a-lot Markets | 187 Suffolk Ln. | Boise     | ID          | 83720            | USA         
   10713 | SAVEA       |           1 | 1997-10-22 | 1997-11-19    | 1997-10-24   |        1 |  167.05 | Save-a-lot Markets | 187 Suffolk Ln. | Boise     | ID          | 83720            | USA         
   10714 | SAVEA       |           5 | 1997-10-22 | 1997-11-19    | 1997-10-27   |        3 |   24.49 | Save-a-lot Markets | 187 Suffolk Ln. | Boise     | ID          | 83720            | USA         
   10722 | SAVEA       |           8 | 1997-10-29 | 1997-12-10    | 1997-11-04   |        1 |   74.58 | Save-a-lot Markets | 187 Suffolk Ln. | Boise     | ID          | 83720            | USA         
   10748 | SAVEA       |           3 | 1997-11-20 | 1997-12-18    | 1997-11-28   |        1 |  232.55 | Save-a-lot Markets | 187 Suffolk Ln. | Boise     | ID          | 83720            | USA         
   10757 | SAVEA       |           6 | 1997-11-27 | 1997-12-25    | 1997-12-15   |        1 |    8.19 | Save-a-lot Markets | 187 Suffolk Ln. | Boise     | ID          | 83720            | USA         
   10815 | SAVEA       |           2 | 1998-01-05 | 1998-02-02    | 1998-01-14   |        3 |   14.62 | Save-a-lot Markets | 187 Suffolk Ln. | Boise     | ID          | 83720            | USA         
   10847 | SAVEA       |           4 | 1998-01-22 | 1998-02-05    | 1998-02-10   |        3 |  487.57 | Save-a-lot Markets | 187 Suffolk Ln. | Boise     | ID          | 83720            | USA         
   10882 | SAVEA       |           4 | 1998-02-11 | 1998-03-11    | 1998-02-20   |        3 |    23.1 | Save-a-lot Markets | 187 Suffolk Ln. | Boise     | ID          | 83720            | USA         
   10894 | SAVEA       |           1 | 1998-02-18 | 1998-03-18    | 1998-02-20   |        1 |  116.13 | Save-a-lot Markets | 187 Suffolk Ln. | Boise     | ID          | 83720            | USA         
   10941 | SAVEA       |           7 | 1998-03-11 | 1998-04-08    | 1998-03-20   |        2 |  400.81 | Save-a-lot Markets | 187 Suffolk Ln. | Boise     | ID          | 83720            | USA         
   10983 | SAVEA       |           2 | 1998-03-27 | 1998-04-24    | 1998-04-06   |        2 |  657.54 | Save-a-lot Markets | 187 Suffolk Ln. | Boise     | ID          | 83720            | USA         
   10984 | SAVEA       |           1 | 1998-03-30 | 1998-04-27    | 1998-04-03   |        3 |  211.22 | Save-a-lot Markets | 187 Suffolk Ln. | Boise     | ID          | 83720            | USA         
   11002 | SAVEA       |           4 | 1998-04-06 | 1998-05-04    | 1998-04-16   |        1 |  141.16 | Save-a-lot Markets | 187 Suffolk Ln. | Boise     | ID          | 83720            | USA         
   11030 | SAVEA       |           7 | 1998-04-17 | 1998-05-15    | 1998-04-27   |        2 |  830.75 | Save-a-lot Markets | 187 Suffolk Ln. | Boise     | ID          | 83720            | USA         
   11031 | SAVEA       |           6 | 1998-04-17 | 1998-05-15    | 1998-04-24   |        2 |  227.22 | Save-a-lot Markets | 187 Suffolk Ln. | Boise     | ID          | 83720            | USA         
   11064 | SAVEA       |           1 | 1998-05-01 | 1998-05-29    | 1998-05-04   |        1 |   30.09 | Save-a-lot Markets | 187 Suffolk Ln. | Boise     | ID          | 83720            | USA         


31 row(s).
1 message(s). 

Choose the file format (press ENTER to skip file export):
  (*) CSV
  (*) XML
  (*) EXCEL
  (*) PARQUET
  quit/exit  Exit the program

> 
Enter your question (press ENTER to just show this prompt again, or type 'quit' to exit):
  :history   Show prompt history indexes and questions
  :reset     Clear prompt history
  quit/exit  Exit the program

> now from previous response give me only those columns that do not have same value for each row
Prompt: now from previous response give me only those columns that do not have same value for each row

Notes: Step 1: The user is asking for a follow-up to the previous query, specifically requesting columns that do not have the same value for each row in the result set from the query `SELECT * FROM orders WHERE ship_city = 'Boise'`.
Step 2: I reviewed the `query_result_preview` from the previous turn, which showed orders where `ship_city` is 'Boise'.
Step 3: I analyzed each column in the preview to determine if its value varied across the returned rows:
    - `order_id`: Varies (e.g., 10324, 10393) -> Keep
    - `customer_id`: Constant ('SAVEA') -> Exclude
    - `employee_id`: Varies (e.g., 9, 1, 2) -> Keep
    - `order_date`: Varies -> Keep
    - `required_date`: Varies -> Keep
    - `shipped_date`: Varies -> Keep
    - `ship_via`: Varies (e.g., 1, 3, 2) -> Keep
    - `freight`: Varies -> Keep
    - `ship_name`: Constant ('Save-a-lot Markets') -> Exclude
    - `ship_address`: Constant ('187 Suffolk Ln.') -> Exclude
    - `ship_city`: Constant ('Boise', due to the WHERE clause) -> Exclude
    - `ship_region`: Constant ('ID') -> Exclude
    - `ship_postal_code`: Constant ('83720') -> Exclude
    - `ship_country`: Constant ('USA') -> Exclude
Step 4: Based on this analysis, the columns to select are `order_id`, `employee_id`, `order_date`, `required_date`, `shipped_date`, `ship_via`, and `freight` from the `orders` table.
Step 5: The `WHERE` clause from the previous query (`WHERE ship_city = 'Boise'`) remains the same to filter the initial result set.

SQL: SELECT order_id, employee_id, order_date, required_date, shipped_date, ship_via, freight FROM orders WHERE ship_city = 'Boise'

order_id | employee_id | order_date | required_date | shipped_date | ship_via | freight
---------+-------------+------------+---------------+--------------+----------+--------
   10324 |           9 | 1996-10-08 | 1996-11-05    | 1996-10-10   |        1 |  214.27
   10393 |           1 | 1996-12-25 | 1997-01-22    | 1997-01-03   |        3 |  126.56
   10398 |           2 | 1996-12-30 | 1997-01-27    | 1997-01-09   |        3 |   89.16
   10440 |           4 | 1997-02-10 | 1997-03-10    | 1997-02-28   |        2 |   86.53
   10452 |           8 | 1997-02-20 | 1997-03-20    | 1997-02-26   |        1 |  140.26
   10510 |           6 | 1997-04-18 | 1997-05-16    | 1997-04-28   |        3 |  367.63
   10555 |           6 | 1997-06-02 | 1997-06-30    | 1997-06-04   |        3 |  252.49
   10603 |           8 | 1997-07-18 | 1997-08-15    | 1997-08-08   |        2 |   48.77
   10607 |           5 | 1997-07-22 | 1997-08-19    | 1997-07-25   |        1 |  200.24
   10612 |           1 | 1997-07-28 | 1997-08-25    | 1997-08-01   |        2 |  544.08
   10627 |           8 | 1997-08-11 | 1997-09-22    | 1997-08-21   |        3 |  107.46
   10657 |           2 | 1997-09-04 | 1997-10-02    | 1997-09-15   |        2 |  352.69
   10678 |           7 | 1997-09-23 | 1997-10-21    | 1997-10-16   |        3 |  388.98
   10700 |           3 | 1997-10-10 | 1997-11-07    | 1997-10-16   |        1 |    65.1
   10711 |           5 | 1997-10-21 | 1997-12-02    | 1997-10-29   |        2 |   52.41
   10713 |           1 | 1997-10-22 | 1997-11-19    | 1997-10-24   |        1 |  167.05
   10714 |           5 | 1997-10-22 | 1997-11-19    | 1997-10-27   |        3 |   24.49
   10722 |           8 | 1997-10-29 | 1997-12-10    | 1997-11-04   |        1 |   74.58
   10748 |           3 | 1997-11-20 | 1997-12-18    | 1997-11-28   |        1 |  232.55
   10757 |           6 | 1997-11-27 | 1997-12-25    | 1997-12-15   |        1 |    8.19
   10815 |           2 | 1998-01-05 | 1998-02-02    | 1998-01-14   |        3 |   14.62
   10847 |           4 | 1998-01-22 | 1998-02-05    | 1998-02-10   |        3 |  487.57
   10882 |           4 | 1998-02-11 | 1998-03-11    | 1998-02-20   |        3 |    23.1
   10894 |           1 | 1998-02-18 | 1998-03-18    | 1998-02-20   |        1 |  116.13
   10941 |           7 | 1998-03-11 | 1998-04-08    | 1998-03-20   |        2 |  400.81
   10983 |           2 | 1998-03-27 | 1998-04-24    | 1998-04-06   |        2 |  657.54
   10984 |           1 | 1998-03-30 | 1998-04-27    | 1998-04-03   |        3 |  211.22
   11002 |           4 | 1998-04-06 | 1998-05-04    | 1998-04-16   |        1 |  141.16
   11030 |           7 | 1998-04-17 | 1998-05-15    | 1998-04-27   |        2 |  830.75
   11031 |           6 | 1998-04-17 | 1998-05-15    | 1998-04-24   |        2 |  227.22
   11064 |           1 | 1998-05-01 | 1998-05-29    | 1998-05-04   |        1 |   30.09


31 row(s).
2 message(s).
```