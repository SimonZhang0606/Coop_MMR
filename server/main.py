import mysql.connector

connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='ThankMrGoose',
    database='coop_mmr',
)

cursor = connection.cursor()

# Example: print all table names
cursor.execute("SHOW TABLES;")
for table_name, in cursor.fetchall():
    print(table_name)

connection.close()
