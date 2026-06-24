import mysql.connector

def get_connection():
    connection = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "YOUR_PASSWORD_HERE",
        database = "IMS_APPLICATION"
    )
    return connection