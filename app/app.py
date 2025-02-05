from flask import Flask, request, make_response
from flask_mysqldb import MySQL
import socket
import datetime
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),  # Log to stdout for Docker
        logging.FileHandler('/var/log/app.log')  # Keep logging to a file
    ]
)

app = Flask(__name__)

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
    container_name = socket.gethostname()  # Get container name
    container_ip = socket.gethostbyname(container_name)  # Get internal IP
    client_ip = request.remote_addr
    date_time = datetime.datetime.now()

    logging.info(f"Received request from {client_ip}. Processed by container: {container_name} (IP: {container_ip})")

    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO access_log (date_time, client_ip, internal_ip) VALUES (%s, %s, %s)",
                   (date_time, client_ip, container_ip))
    mysql.connection.commit()
    cursor.close()

    # Check if the cookie already exists
    existing_cookie = request.cookies.get('internal_ip')

    if not existing_cookie:
        response = make_response(f"Internal IP: {container_ip}")  # Display only IP in browser
        response.set_cookie('internal_ip', container_name, max_age=300)  # Store container *name* in cookie
    else:
        try:
            resolved_ip = socket.gethostbyname(existing_cookie)  # Resolve stored container name to IP
            response = make_response(f"Internal IP: {resolved_ip}")
        except socket.gaierror:
            response = make_response("Internal IP: (Unknown)")

    return response


@app.route("/showcount", methods=["GET"])
def show_count():
    return f"Global counter value: {counter}"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)  # Make sure it's accessible from all IPs
