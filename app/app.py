from flask import Flask,render_template
import socket
import mysql.connector
from mysql.connector import errorcode
import os
from dotenv import load_dotenv
load_dotenv()

user = os.getenv('user')
password = os.getenv('password')
dbname = os.getenv('dbname')
dbhost = os.getenv('dbhost')

app = Flask(__name__)
try:
  cnx = mysql.connector.connect(user=user,password=password,database=dbname,host=dbhost)
  print("Successfully connected")
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)

  
@app.route("/")
def index():
    print('Flask app default page is called')
    try:
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
        ##Insert the host_name and the host_ip into MySQL database
        cursor = cnx.cursor(buffered=True)
        add_host = ("INSERT INTO hosts_history "
               "(host_name, host_ip) "
               "VALUES (%s, %s)")
        data_host = (host_name, host_ip)
        cursor.execute(add_host, data_host)
        cursor.close()
        cnx.commit()
        ## 
        return render_template('index.html', hostname=host_name, ip=host_ip)
    except:
        return render_template('error.html')

@app.route("/hosts")
def hosts():
    try:
        ##Insert the host_name and the host_ip into MySQL database
        cursor = cnx.cursor(buffered=True)
        all_host = ("SELECT * FROM hosts_history")
        cursor.execute(all_host)
        dict_data={}
        for (host_id, host_name, host_ip) in cursor:
           dict_data[host_id] = [host_name, host_ip]
        cursor.close()
        ## 
        return dict_data
    except:
        return render_template('error.html')


if __name__ == "__main__":
    print('My Flask app is running')
    app.run(host='0.0.0.0', port=5000)


