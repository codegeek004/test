import mysql.connector
#database configuration
db_config = {
        'host' : "localhost",
        'user':"root",
        'password' : "root",
        'database' : "yash"}
#create a connection to the mysql database
db = mysql.connector.connect(**db_config)
#initialize the cursor
cursor = db.cursor()


