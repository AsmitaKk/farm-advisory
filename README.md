# Farm Advisory

A smart agriculture platform providing crop, soil, fertilizer, vegetable,
weather, and field advisory information to help farmers make better farming
decisions.

## Project structure

```text
farm-advisory-/
|-- html/       # Flask templates
|-- python/     # Python application files
|-- css/        # Stylesheets
|-- database/   # Database files, schemas, migrations, and seeds
|-- images/     # Image assets
|-- requirements.txt
`-- run.bat
```

## Run locally

From the repository root in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
notepad .env
python python\init_db.py
python python\app.py
```

Open <http://127.0.0.1:5000> in a browser. On Windows, `run.bat` performs the
dependency installation, initializes MySQL, and starts the same application.

## MySQL requirements

Install and start MySQL Server before initializing the application. The default
database name is `farm_advisory`. Connection settings are read from `.env`:

```text
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
MYSQL_DATABASE=farm_advisory
FLASK_SECRET_KEY=your_long_random_secret
```

The real `.env` file is ignored by Git so credentials are not uploaded.
