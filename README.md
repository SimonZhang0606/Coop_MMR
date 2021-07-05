# Co-op MMR

Co-op MMR is a place for University of Waterloo students to look up and compare co-op jobs.

What's implemented:

- Browse Jobs page (Feature 4 in the report)
- Browse Companies page
- Breakdown of Company Hires by Work Term
- MMR
- sorting on each column

TODO by tomorrow:

- leaving a review
- job hires by work term

## Data Scraping and Populating the Database

1. Ensure all required dependencies have been installed by running `pip3 install -r sql_scripts/requirement.txt`.
1. Run `sql_scripts/linkedin_scraper`. It should take less than two hours for the script to run. The scraped data are stored in the `data` folder.
1. To populate the database using docker, follow [Quick Start with Docker](#quick-start-with-docker). To populate a local database, execute the following steps.
1. Go to `sql_scripts` directory.
1. Run `mysql -u root appDB < ./create_tables.sql` to drop existing table schemas and to create new ones.
1. Run `mysql -u root appDB < ./populate_tables.sql` to populate the tables with production data.

## Quick Start with Docker

This is the quickest and easiest way to get everything set up – all you need to install is [Docker](https://www.docker.com/).

> Unfortunately, Docker does not run on all systems. Follow [Getting Started without Docker](#getting-started-without-docker) if you cannot install Docker.

> **Warning**: if you pull this code on Windows, you will need to manually convert the `sql_scripts/data/*.tsv` files to have LF endings instead of CRLF.

1. Run `docker compose up`.
1. Visit http://localhost:5000/jobs to see the demo endpoint in action.
1. Visit http://localhost:3000/ to see the demo frontend in action.

To look into the database, visit http://localhost:8080/?server=db&username=root&db=coop_mmr to check out the DB in Adminer. When prompted for a login, use the username `root` and password `ThankMrGoose`.

## Getting Started without Docker

### Web App

1. Go to the `web` folder.
1. Run `npm install` to install dependencies.
1. Run `npm start`.

### Web Server

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
