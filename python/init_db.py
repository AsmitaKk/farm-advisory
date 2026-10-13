from mysql.connector import Error

from database import check_connection, initialize_database


if __name__ == "__main__":
    print("Creating the MySQL database, tables, and initial data...")
    try:
        initialize_database()
    except Error as exc:
        raise SystemExit(
            "Could not connect to MySQL. Start MySQL Server and verify the "
            f"MYSQL_* settings in .env. Details: {exc}"
        ) from None
    connected, detail = check_connection()
    if not connected:
        raise SystemExit(f"Database initialization failed: {detail}")
    print(f"MySQL database '{detail}' is ready.")
