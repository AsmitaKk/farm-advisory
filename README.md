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
python python\app.py
```

Open <http://127.0.0.1:5000> in a browser. On Windows, `run.bat` performs the
dependency installation and starts the same application.
