import mysql.connector
from dotenv import load_dotenv
import os
load_dotenv()



pongdb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = os.environ.get("mysql_password")
)


cursor = pongdb.cursor()


try:
    cursor.execute("CREATE DATABASE pongdb")
    
except:
    
    cursor.execute("DROP DATABASE pongdb")
    cursor.execute("CREATE DATABASE pongdb")

