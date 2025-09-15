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
