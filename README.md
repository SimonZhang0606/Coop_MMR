# Co-op MMR

## Quick Start - Docker

1. Run `docker-compose up`.
1. Visit http://localhost:8080/?server=db&username=root&db=coop_mmr to check out the DB with Adminer. When prompted for a login, use the username `root` and password `ThankMrGoose`.

## Slow Start

Assuming MySQL and PHP are installed:

### Creating sample database

Enter the following commands into the command line:

    $ mysql -u root
    mysql> CREATE DATABASE appDB;

    mysql> USE appDB;
    mysql> CREATE TABLE student(uid DECIMAL(3, 0) NOT NULL PRIMARY KEY, name VARCHAR(30), term DECIMAL(3, 0));
    mysql> INSERT INTO student VALUES(1, 'shawn', 3);
    mysql> INSERT INTO student VALUES(2, 'simon', 6);

    mysql> create user 'justin'@'localhost' identified by 'my_secure_password';
    mysql> grant all on appDB.* to 'justin'@'localhost';
    mysql> alter user 'justin'@'localhost' identified with mysql_native_password by 'my_secure_password';

### Loading application

Enter the following commands into the command line (from the directory of the php file):

    $ php -S 127.0.0.1:8000

Now go to http://127.0.0.1:8000/appDB.php in the browser.
