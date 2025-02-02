from flask import Flask
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(filename='/var/log/app.log', level=logging.INFO)


@app.route('/')
def hello():
    logging.info("Hello World was accessed")
    return "Hello, World!"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
