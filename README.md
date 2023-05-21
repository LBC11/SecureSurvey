# SecureSurvey
Secure Survey is a survey service that uses Homomorphic Encryption (pi-heaan) to securely handle user data while identifying respondents that meet the company's criteria. By efficiently sending surveys to selected users, companies can conduct effective data analysis while ensuring the protection of personal information.  

## Technologies Used
The technologies and versions used in this project are as follows:

- Database: MariaDB
- Backend: Django
- Language: Python
- Virtual Environment: venv

## Folder Structure
The folder structure for running the project is as follows:

- secure_survey: folder containing Django code and HTML files

## Getting Started

### Database Setup
1. Install MariaDB: 
    - If MariaDB is already installed, proceed to the next step.
    - If MariaDB is not installed, download and install MariaDB from [here](https://mariadb.org/download/).
2. Create Database:
    - Connect to the MariaDB client.
    - Execute the command "CREATE DATABASE secure;".

### Backend Setup
1. Check Python Installation:
    - If Python is already installed, proceed to the next step.
    - If Python is not installed, download and install Python from [here](https://www.python.org/downloads/).
2. Create and Activate a Virtual Environment:
    - Navigate to the `secure_survey` folder in the terminal.
    - Run the command `python -m venv venv` to create a new virtual environment.
    - Activate the virtual environment. On Windows, use the command `venv\Scripts\activate`. On macOS/Linux, use `source venv/bin/activate`.
3. Install Django and Other Dependencies:
    - Navigate to the `secure_survey/secure_survey_project` folder in the terminal.
    - With the virtual environment activated, install the required dependencies by running the command: `pip install -r requirements.txt`.
4. Configure Local Settings:
    - Navigate to `secure_survey/secure_survey_project` and create a new file named `local_settings.py`.
    - Add the following to the file, filling in the information for each item:
 
    ```python
    DEBUG = True

    SECRET_KEY = 'Put the secret_key you received here.'

    DATABASE_NAME = 'your database name'
    DATABASE_USER = 'your database user'
    DATABASE_PASSWORD = 'your database password'
    DATABASE_HOST = 'your database host'
    DATABASE_PORT = 'your database port'

    EMAIL_HOST_USER = 'your google id'
    EMAIL_HOST_PASSWORD = 'your google app password'
    ```
5. Run the Django Server:
    - Run the server with the command: `python manage.py runserver`.
    - If everything is set up correctly, the secure survey web page will be accessible at [http://localhost:8000](http://localhost:8000) in your web browser. 
    ![image](https://github.com/LBC11/SecureSurvey/assets/107410759/33798f0c-2465-4913-b7fb-8e2df6d4da6e)

