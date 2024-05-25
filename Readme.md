# Password Manager Application

## Overview

This is a 2-tier Password Manager Application developed using Python for the GUI and Database connection and MySQL for the database. The application provides secure storage and management of user passwords, with added security features such as device-based login notifications. The server handles all client operations and both the client device and server must be connected through the same hotspot for communication.

## Features

- **User Authentication:** Includes a login and sign-up interface where users can register and log in with their details.
- **Device-based Login Notification:** Users receive an email notification if they log in from a different device than the one used during sign-up.
- **Password Storage:** Users can store their website login details and passwords securely.
- **Password Generation:** Users can generate random, secure passwords.
- **Forgot Password:** Users can retrieve their forgotten passwords from the database.
- **Mail Configuration:** Users need to configure their mail ID and password after downloading the application from GitHub.

## Installation and Setup

### Prerequisites

- Python 3.x
- MySQL Server
- MySQL Connector for Python
- Required Python packages:
    - tkinter
    - smtplib
    - email
    - random
    - string

### Database Setup

- Install MySQL Server and create a database for the application.
- Create the necessary tables using the provided SQL scripts.

### Python Environment Setup

1. Clone the repository from GitHub.

    ```bash
    # Clone the repo

    git clone https://github.com/AlphaQ6353/PasswordManager
    
    # Navigate to project directory

    cd password-manager
2. Install python packages

    ```bash
    pip install mysql-connector-python
### Configuration

1. Update the database connection settings in the  server.py file

    ```bash
    mydb = mysql.connector.connect(host='your_host_name',
                               user='your_user_name',
                               password='your_db_password',
                               database='your_database_file'
                               )
2. Configure the email settings in the server.py file. Replace placeholders with your email and password.

    ```bash
    my_email = "your_mail_id"

    # password obtained from 2-step verification from your mail settings
    password_mail = "mail_password"

## Running the Application

1. Start the server by running the code

    ```bash
    python server.py
2. Start the client by running the code

    ```bash
    python client.py
## Usage
- **Sign Up:** Open the application and sign up with your details.
- **Login:** Log in using your credentials. If logging in from a new device, you will receive an email notification.
- **Forgot Password:** If you forget your password, use the "Forgot Password" option to retrieve it from the database.
- **Manage Passwords:** After logging in, you can add new website credentials, view saved credentials, and generate random passwords.

## Security
- Ensure that your MySQL server is secured and accessible only from trusted devices.
- Update your email and password in the configuration files to maintain security.
- Use strong, unique passwords for your email and database accounts.
