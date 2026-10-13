# MySQL database

This folder contains the persistent MySQL database definition:

- `schema.sql` creates the users, crops, soils, fertilizers, market data,
  transactions, and farmer queries tables.
- `seed.sql` inserts the initial administrator, demo farmer, reference data,
  sample orders, and sample inquiries without duplicating existing rows.

Copy `.env.example` to `.env`, enter the MySQL credentials, and run:

```powershell
python python\init_db.py
```

The initializer creates the configured database automatically. Running
`python python\app.py` also initializes the database before starting Flask.
