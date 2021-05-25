# Coop_MMR

# Creating and loading sample data

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
