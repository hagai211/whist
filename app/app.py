from flask import Flask, request, make_response
from flask_mysqldb import MySQL
import socket
import datetime
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(filename='/var/log/app.log', level=logging.INFO)

# MySQL configuration
app.config['MYSQL_HOST'] = 'db'  # Change to your MySQL host
app.config['MYSQL_USER'] = 'user'  # Change to your MySQL username
app.config['MYSQL_PASSWORD'] = 'password'  # Change to your MySQL password
app.config['MYSQL_DB'] = 'mydb'  # Change to your MySQL database name

mysql = MySQL(app)

counter = 0


@app.route("/", methods=["GET"])
def index():
    global counter
    counter += 1
    internal_ip = socket.gethostbyname(socket.gethostname())
    client_ip = request.remote_addr
    date_time = datetime.datetime.now()
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO access_log (date_time, client_ip, internal_ip) VALUES (%s, %s, %s)",
                   (date_time, client_ip, internal_ip))
    mysql.connection.commit()
    cursor.close()
    # Check if the cookie already exists
    existing_cookie = request.cookies.get('internal_ip')

    # Set the cookie only if it doesn't exist
    if not existing_cookie:
        response = make_response(f"Internal IP: {internal_ip}")
        response.set_cookie('internal_ip', internal_ip, max_age=300)  # Cookie for 5 minutes
    else:
        response = make_response(f"Internal IP: {existing_cookie}")
    return response


@app.route("/showcount", methods=["GET"])
def show_count():
    return f"Global counter value: {counter}"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)  # Make sure it's accessible from all IPs
