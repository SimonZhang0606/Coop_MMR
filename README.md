# Co-op MMR

<!-- ## Quick Start - Docker

1. Run `docker-compose up`.
1. Visit http://localhost:8080/?server=db&username=root&db=coop_mmr to check out the DB with Adminer. When prompted for a login, use the username `root` and password `ThankMrGoose`. -->

## Web App

1. From the ./web folder, run `npm install` to install dependencies/modules.
2. Run `npm start`.

## Web Server

1. In `./server` folder, run `python api.py --password CS348isgreat --database appDB`.

## Creating and Populating DB

1. Go to `sql_scripts`.
1. To create schemas , run `mysql -u root appDB < ./create_tables.sql`.
1. To populate schemas, run `mysql -u root appDB < ./populate_tables.sql`.
