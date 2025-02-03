# Whist Application

This project consists of a Flask application deployed using Docker, along with a MySQL database and an NGINX load balancer. The architecture is designed to handle incoming requests with session stickiness based on a cookie, ensuring that requests from the same client are routed to the same application container for a period of 5 minutes.

## Project Structure

. ├── app │ ├── Dockerfile │ └── app.py ├── db │ ├── Dockerfile │ └── ... ├── logs │ ├── app_logs │ └── db_logs ├── nginx │ └── nginx.conf ├── scripts │ ├── scale-down.sh │ └── scale-up.sh └── docker-compose.yaml

## Components

1. **Flask Application**: The core of the application that processes incoming requests and interacts with the MySQL database.
2. **MySQL Database**: A containerized MySQL database for storing application data and logs.
3. **NGINX Load Balancer**: An NGINX container that balances incoming requests across multiple Flask application containers, providing session stickiness.
4. **Logging**: Application and database logs are persisted to local directories for easy access and debugging.

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Configuration

1. **Database Configuration**: Update the database credentials in the Flask application's configuration if necessary.
2. **NGINX Configuration**: Ensure the `nginx.conf` file is properly set up for your needs.

### Running the Application

1. Clone the repository:
   git clone https://github.com/hagai211/whist.git
   cd Whist
   docker-compose up --build
