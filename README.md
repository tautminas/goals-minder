# Goals Minder Web Application

## About the application

Goals Minder is a Python Flask web application created with Bootstrap. It simplifies goal tracking with essential CRUD operations, complemented by sign-in and registration features. The data is securely stored in the application's SQL database.

## Running the application

Create virtual environment
```bash
python -m venv goals-minder
```

Activate the virtual environment based on the operating system:
- On Windows:
```bash
goals-minder\Scripts\activate
```
- On macOS and Linux:
```bash
source goals-minder/bin/activate
```

Install the required packages:
```bash
pip install -r requirements.txt
```

Run the application:
```bash
python main.py
```

After you are done using the application leave the virtual environment:
```bash
deactivate
```