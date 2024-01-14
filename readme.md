# Setting up queue-manager-api Environment
This is a guide for setting up the QueueManager development environment. This guide assumes that you already have Python3 installed on your machine.

## Creating a virtual environment
The first step is to create a virtual environment using venv. A virtual environment is a way to isolate project dependencies from the operating system. To create a virtual environment, run the following command:

```python3
python3 -m venv .venv
```

This command will create a virtual environment in the .venv directory. You can choose a different name if you wish.

## Activating the virtual environment
After creating the virtual environment, you need to activate it. To activate the virtual environment, run the following command:

```bash
source .venv/bin/activate
```

This command will activate the virtual environment and you will be able to install project dependencies without affecting the operating system.

## Installing dependencies
With the virtual environment activated, you can install project dependencies. To install dependencies, run the following command:

```pip3
pip3 install -r requirements.txt
```

This command will install all the dependencies listed in the requirements.txt file.

## Performing migrations
Before running the application, you need to perform database migrations. To perform migrations, run the following command:

```flask
python3 manage.py migrate
```

This command will apply pending migrations.

## Running the application
To run the application, run the following command:

```flask
python3 manage.py runserver
```

This command will start the application on port 8000.