# Kaidee backend interview
## How to start server
First, make a copy of `.env.template` file in `backend` directory and rename it to `.env` and fill the environment variable into it, e.g.
```bash
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_SERVER=db
POSTGRES_PORT=5432
POSTGRES_DB=postgres
```
and then use `docker compose up` to start the API server. After the server has started, open up `localhost:8000` to see all available resources.
## How to run test
You can run the test by using `docker compose exec server pytest -v`.