# Co-op MMR

Co-op MMR is a place for University of Waterloo students to look up and compare co-op jobs.

## Features

In the backend, all backend endpoints are implemented in `server/src/app.py`. All queries are implemented in `server/src/queries.py`, and are executed using functions in `server/src/drivers.py`.

- Browse Jobs page (Feature 6 in the report)
  - Frontend: `web/src/Jobs.js`
  - Endpoint: `GET /jobs`
- Browse Companies page (Feature 1 in the report)
  - Frontend: `web/src/Companies.js`
  - Endpoint: `GET /companies`
- Viewing a company's job listings (Feature 3 in the report)
  - Frontend: `web/src/Company.js`
  - Endpoint: `GET /companies/:cid`
- Viewing a company's hire breakdowns by work term (Feature 4 in the report)
  - Frontend: `web/src/Company.js`
  - Endpoint: `GET /companies/:cid`
- Viewing job details and reviews, hiring breakdowns by work term (Features 5, 7, 11 in the report)
  - Frontend: `web/src/Job.js`
  - Endpoint: `GET /jobs/:jid`
- Leaving a review for a job (Features 12, 13 in the report)
  - Frontend: `web/src/Job.js`
  - Endpoint: `POST /jobs/:jid/review`
- MMR (Feature 14 in the report)
  - MMR Calculations: `sql_scripts/linkedin_scraper.py`
  - Endpoints that include MMR: `GET /companies`, `GET /companies/:cid`, `GET /jobs`, `GET /jobs/:jid`

## Data Scraping and Populating the Database

1. Ensure all required dependencies have been installed by running `pip install -r sql_scripts/requirements.txt`.
1. Run `sql_scripts/linkedin_scraper.py`. It should take less than two hours for the script to run. The scraped data is stored in the `sql_scripts/data` folder.
1. To populate the database using Docker, follow [Quick Start with Docker](#quick-start-with-docker). To populate a local database, execute the following steps.
1. Go to the `sql_scripts` directory.
1. Run `mysql -u root appDB < ./create_tables.sql` to drop existing table schemas and to create new ones.
1. Run `mysql -u root appDB < ./populate_tables.sql` to populate the tables with production data.

## Quick Start with Docker

This is the quickest and easiest way to get everything set up ??? all you need to install is [Docker](https://www.docker.com/).

> Unfortunately, Docker does not run on all systems. Follow [Getting Started without Docker](#getting-started-without-docker) if you cannot install Docker.

> **Warning**: If you pull this code on Windows, you will need to manually convert the `sql_scripts/data/*.tsv` files to have LF endings instead of CRLF.

1. Run `docker compose up`.
1. Visit http://localhost:5000/companies and http://localhost:5000/jobs to see some endpoints in action.
1. Visit http://localhost:3000/ to see the demo frontend in action.

To look into the database, visit http://localhost:8080/?server=db&username=root&db=coop_mmr to check out the DB in Adminer. When prompted for a login, use the username `root` and password `ThankMrGoose`.

## Getting Started without Docker

### Web App

1. Go to the `web` folder.
1. Run `npm install` to install dependencies.
1. Run `npm start`.

### Web Server

1. Make sure local Python version >= 3.8.
1. Go to the `server` folder.
1. _Optional, but recommended_: Set up and activate a [Python virtual envrionment](https://docs.python.org/3/library/venv.html).
1. Run `pip install -r requirements.txt` to install dependencies.
1. Go to the `src` folder inside `server`.
1. Set the environment variables outlined in [Web Server Configuration](#web-server-configuration).
1. Run `python -m flask run --port=5000`.

#### Web Server Configuration

| Variable    | Description                                  | Example Value  |
| ----------- | -------------------------------------------- | -------------- |
| DB_HOST     | the database host                            | `localhost`    |
| DB_USER     | the user to connect with                     | `root`         |
| DB_PASSWORD | the password for `DB_USER`                   | `ThankMrGoose` |
| DB_DATABASE | the database containing the Co-op MMR tables | `appDB`        |
