import mysql.connector

def get_connection():
    connection = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "root",
        database = "IMS_APPLICATION"
    )
    return connection