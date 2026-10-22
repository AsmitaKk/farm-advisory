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

## Smart Irrigation Planner

Authenticated farmers can open `/irrigation` to save one farm profile, retrieve
live Open-Meteo weather, calculate an FAO-56-based irrigation estimate, record
irrigation and review water-use analytics. Open-Meteo requires no API key, but
the server needs outbound HTTPS access. Run `python python\init_db.py` once after
updating to create the two irrigation tables.

The planner is fully functional without field hardware. Soil moisture and system
flow rate are optional manual readings; without moisture, recommendations are
marked as weather-only estimates, and without flow rate no runtime is claimed.
Browser alerts require the farmer's permission. Figures are decision support and
should be checked against field conditions and local extension guidance.

## Multilingual voice assistant

Every page includes a farmer-focused assistant supporting Marathi (`mr-IN`),
Hindi (`hi-IN`), and English (`en-IN`). It accepts typed questions and, in
Google Chrome, voice input through the Web Speech API. Answers can be read aloud
through the browser SpeechSynthesis API. Crop and soil guidance comes from the
local catalogue, market answers use only the live data.gov.in-backed feed, and
weather answers use Open-Meteo only after a farmer saves a location in the
Smart Irrigation Planner. No paid AI key is required.

Microphone recognition depends on Chrome's speech service, the user's permission,
network availability, and the operating system's installed language support.
If recognition or a matching voice is unavailable, typed chat remains usable and
the assistant displays the answer without fabricating speech or live data.

The real `.env` file is ignored by Git so credentials are not uploaded.
