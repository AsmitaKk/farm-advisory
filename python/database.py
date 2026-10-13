import os
from contextlib import contextmanager
from pathlib import Path

import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_DIR = PROJECT_ROOT / "database"
load_dotenv(PROJECT_ROOT / ".env")
DATABASE_NAME = os.getenv("MYSQL_DATABASE", "farm_advisory")


def database_config(include_database=True):
    config = {
        "host": os.getenv("MYSQL_HOST", "127.0.0.1"),
        "port": int(os.getenv("MYSQL_PORT", "3306")),
        "user": os.getenv("MYSQL_USER", "root"),
        "password": os.getenv("MYSQL_PASSWORD", ""),
        "charset": "utf8mb4",
        "use_unicode": True,
    }
    if include_database:
        config["database"] = DATABASE_NAME
    return config


@contextmanager
def connection():
    db = mysql.connector.connect(**database_config())
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def fetch_all(query, params=()):
    with connection() as db:
        cursor = db.cursor(dictionary=True)
        try:
            cursor.execute(query, params)
            return cursor.fetchall()
        finally:
            cursor.close()


def fetch_one(query, params=()):
    with connection() as db:
        cursor = db.cursor(dictionary=True)
        try:
            cursor.execute(query, params)
            return cursor.fetchone()
        finally:
            cursor.close()


def execute(query, params=()):
    with connection() as db:
        cursor = db.cursor()
        try:
            cursor.execute(query, params)
            return cursor.rowcount, cursor.lastrowid
        finally:
            cursor.close()


def execute_script(path):
    sql = Path(path).read_text(encoding="utf-8")
    statements = [statement.strip() for statement in sql.split(";") if statement.strip()]
    with connection() as db:
        cursor = db.cursor()
        try:
            for statement in statements:
                cursor.execute(statement)
        finally:
            cursor.close()


def initialize_database():
    """Create the configured database, tables, and initial demo data."""
    server = mysql.connector.connect(**database_config(include_database=False))
    try:
        cursor = server.cursor()
        try:
            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS `{DATABASE_NAME}` "
                "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
        finally:
            cursor.close()
        server.commit()
    finally:
        server.close()

    execute_script(DATABASE_DIR / "schema.sql")
    user_count = fetch_one("SELECT COUNT(*) AS count FROM users")["count"]
    if user_count == 0:
        execute_script(DATABASE_DIR / "seed.sql")


def check_connection():
    try:
        row = fetch_one("SELECT DATABASE() AS database_name")
        return True, row["database_name"]
    except Error as exc:
        return False, str(exc)


def get_users():
    return fetch_all("SELECT name, username, email, password, role FROM users ORDER BY id")


def get_user_by_login(login_id):
    return fetch_one(
        "SELECT name, username, email, password, role FROM users "
        "WHERE LOWER(email) = %s OR LOWER(username) = %s LIMIT 1",
        (login_id.lower(), login_id.lower()),
    )


def create_user(name, email, password, role="farmer", username=None):
    return execute(
        "INSERT INTO users (name, username, email, password, role) VALUES (%s, %s, %s, %s, %s)",
        (name, username, email, password, role),
    )


def delete_user(email):
    return execute("DELETE FROM users WHERE LOWER(email) = %s AND role <> 'admin'", (email.lower(),))[0]


def rows_by_key(table):
    allowed = {"crops", "soils", "fertilizers"}
    if table not in allowed:
        raise ValueError("Unsupported table")
    rows = fetch_all(f"SELECT * FROM {table} ORDER BY id")
    return {row.pop("id"): row for row in rows}


def get_crops():
    return rows_by_key("crops")


def get_soils():
    return rows_by_key("soils")


def get_fertilizers():
    return rows_by_key("fertilizers")


def upsert_crop(crop_id, crop):
    return execute(
        """INSERT INTO crops
        (id, name, soil, climate, rainfall, ph, season, `yield`, description, image)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE name=VALUES(name), soil=VALUES(soil),
        climate=VALUES(climate), rainfall=VALUES(rainfall), ph=VALUES(ph),
        season=VALUES(season), `yield`=VALUES(`yield`), description=VALUES(description),
        image=VALUES(image)""",
        (
            crop_id, crop["name"], crop["soil"], crop["climate"], crop["rainfall"],
            crop["ph"], crop["season"], crop["yield"], crop["description"], crop["image"],
        ),
    )


def delete_crop(crop_id):
    return execute("DELETE FROM crops WHERE id = %s", (crop_id,))[0]


def get_market_data():
    return fetch_all(
        "SELECT id, crop, variety, CONCAT('₹ ', FORMAT(price_val, 0, 'en_IN')) AS price, "
        "price_val, trend, `change` FROM market_data ORDER BY display_order, id"
    )


def get_market_item(crop_id):
    return fetch_one(
        "SELECT id, crop, variety, CONCAT('₹ ', FORMAT(price_val, 0, 'en_IN')) AS price, "
        "price_val, trend, `change` FROM market_data WHERE id = %s",
        (crop_id,),
    )


def upsert_market_item(crop_id, crop, variety, price_val, trend, change):
    return execute(
        """INSERT INTO market_data (id, crop, variety, price_val, trend, `change`)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE crop=VALUES(crop), variety=VALUES(variety),
        price_val=VALUES(price_val), trend=VALUES(trend), `change`=VALUES(`change`)""",
        (crop_id, crop, variety, price_val, trend, change),
    )


def update_market_item(crop_id, price_val, trend, change):
    return execute(
        "UPDATE market_data SET price_val=%s, trend=%s, `change`=%s WHERE id=%s",
        (price_val, trend, change, crop_id),
    )[0]


def delete_market_item(crop_id):
    return execute("DELETE FROM market_data WHERE id = %s", (crop_id,))[0]


def get_transactions(email=None):
    query = "SELECT id, user_email, crop_id, crop_name, action, price, quantity, total, status, DATE_FORMAT(created_at, '%Y-%m-%d %H:%i') AS date FROM transactions"
    params = ()
    if email:
        query += " WHERE user_email = %s"
        params = (email,)
    query += " ORDER BY id"
    return fetch_all(query, params)


def create_transaction(user_email, crop_id, crop_name, action, price, quantity, total, status="Confirmed"):
    return execute(
        """INSERT INTO transactions
        (user_email, crop_id, crop_name, action, price, quantity, total, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
        (user_email, crop_id, crop_name, action, price, quantity, total, status),
    )


def update_transaction_status(order_id, status):
    return execute("UPDATE transactions SET status = %s WHERE id = %s", (status, order_id))[0]


def delete_transaction(order_id):
    return execute("DELETE FROM transactions WHERE id = %s", (order_id,))[0]


def get_queries(email=None):
    query = "SELECT id, name, email, subject, message, DATE_FORMAT(created_at, '%Y-%m-%d %H:%i') AS date, status FROM farmer_queries"
    params = ()
    if email:
        query += " WHERE email = %s"
        params = (email,)
    query += " ORDER BY id"
    return fetch_all(query, params)


def create_query(name, email, subject, message):
    return execute(
        "INSERT INTO farmer_queries (name, email, subject, message, status) VALUES (%s, %s, %s, %s, 'Pending')",
        (name, email, subject, message),
    )


def toggle_query_status(query_id):
    return execute(
        "UPDATE farmer_queries SET status = IF(status = 'Pending', 'Resolved', 'Pending') WHERE id = %s",
        (query_id,),
    )[0]


def delete_query(query_id):
    return execute("DELETE FROM farmer_queries WHERE id = %s", (query_id,))[0]
