# Flask Machine Option App
This Flask web app allows you to manage Products, Options, and Product-Option Relations using PostgreSQL.

## Prerequisites
- Python 3.x
- PostgreSQL installed
- WSL users: peer authentication (username = masato)

## Setup
1. Clone the repository:
git clone https://github.com/yourusername/flask_machine_option.git
cd flask_machine_option

2. Run the setup script:
bash setup.sh
This will:
- Create a Python virtual environment
- Install Flask, SQLAlchemy, psycopg
- Create app.py, models.py, requirements.txt, and templates

3. Activate virtual environment:
source venv/bin/activate

4. Make sure PostgreSQL database exists (masato in this example):
createdb masato

## Run the app
python app.py
Open browser: http://127.0.0.1:5000

## Database Configuration
- Database URL is set in app.py:
DATABASE_URL = "postgresql+psycopg:///masato"
- Adjust masato if your database name is different.
- Peer authentication is used (no password). Ensure your PostgreSQL user matches your WSL username.
- Tables (products, options, product_options) are automatically created on first run.

## Features
- Product CRUD: Add, edit, delete products
- Option CRUD: Add, edit, delete options
- Product-Option Relations CRUD: Add, edit, delete relations with description
- All relations are cascade-deleted when products or options are deleted

## Notes
- Templates are basic placeholders in templates/ folder. You can customize HTML as needed.
- If you want sample data, you can manually add products, options, and relations via the web interface.
- The app uses SQLAlchemy ORM and psycopg3 for PostgreSQL connectivity.
- Debug mode is enabled for development purposes. Turn off in production by changing app.run(debug=True).

