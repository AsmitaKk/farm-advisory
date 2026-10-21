from pathlib import Path
import os
import json
import time
from urllib import request as urlrequest
from urllib.error import HTTPError, URLError
from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash, send_from_directory
from werkzeug.security import check_password_hash, generate_password_hash
import database as db
from agronomy import build_catalog
from fertilizer_catalog import build_fertilizer_catalog, fertilizer_matches

PROJECT_ROOT = Path(__file__).resolve().parent.parent
HTML_DIR = PROJECT_ROOT / "html"
CSS_DIR = PROJECT_ROOT / "css"
IMAGES_DIR = PROJECT_ROOT / "images"
DATABASE_DIR = PROJECT_ROOT / "database"

app = Flask(__name__, template_folder=str(HTML_DIR), static_folder=None)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "development-only-change-this-secret")

FINNID_PRICE_URL = "https://finnid.in/MarketLinkage/GetMandiPrices"
_live_price_cache = {}


@app.errorhandler(db.Error)
def database_error(error):
    app.logger.error("MySQL error: %s", error)
    return (
        "MySQL is unavailable. Start MySQL Server and check the MYSQL_* values "
        "in your .env file.",
        503,
    )


@app.route("/static/css/<path:filename>")
def css_file(filename):
    return send_from_directory(CSS_DIR, filename)


@app.route("/static/images/<path:filename>")
def image_file(filename):
    return send_from_directory(IMAGES_DIR, filename)

# The dedicated administrator identifiers are protected from registration/deletion.
ADMIN_USERNAME = "admin"
ADMIN_EMAIL = "admin@gmail.com"


def password_matches(stored_password, submitted_password):
    if stored_password.startswith(("scrypt:", "pbkdf2:")):
        return check_password_hash(stored_password, submitted_password)
    return stored_password == submitted_password
@app.route("/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("fullname", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "").strip()

        if not name or not email or not password:
            return render_template("reg.html", error="All fields are required.")

        # Disallow taking admin email or username
        if email in [ADMIN_EMAIL, ADMIN_USERNAME] or name.lower() == ADMIN_USERNAME:
            return render_template("reg.html", error="This username/email is reserved exclusively for the system administrator.")

        # Check if user already exists
        if db.get_user_by_login(email):
            return render_template("reg.html", error="Email already registered. Please login.")

        # Multiple users can register, but all registered users are farmers (single admin only)
        db.create_user(name, email, generate_password_hash(password))
        flash(f"Account registered successfully for {name}! Please login below.", "success")
        return redirect(url_for("login"))

    return render_template("reg.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        login_id = request.form.get("username_or_email", request.form.get("email", "")).strip().lower()
        password = request.form.get("password", "").strip()
        
        user = db.get_user_by_login(login_id)
        if user and not password_matches(user.get("password", ""), password):
            user = None

        if user:
            session['user'] = {key: user.get(key) for key in ("name", "username", "email", "role")}
            if user.get('role') == 'admin':
                flash("Welcome, Administrator! You have logged into the Admin Command Center.", "success")
                return redirect(url_for("admin_dashboard"))
            flash(f"Welcome back, {user['name']}!", "success")
            return redirect(url_for("dashboard"))
        else:
            error = "Invalid Username/Email or Password. Please verify and try again."
            return render_template("log.html", error=error)

    return render_template("log.html")

@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect(url_for("register"))

@app.route("/trade-action", methods=["POST"])
def trade_action():
    if 'user' not in session:
        return redirect(url_for("login"))
    
    crop_id = request.form.get("crop_id")
    action = request.form.get("action", "BUY").upper()
    price = request.form.get("price", "0")
    quantity = request.form.get("quantity", "1")
    
    crop_info = db.get_market_item(crop_id)
    crop_name = crop_info["crop"] if crop_info else (crop_id.capitalize() if crop_id else "Crop")
    
    try:
        clean_p = int(''.join(c for c in str(price) if c.isdigit()) or "0")
        total_val = clean_p * int(quantity)
    except Exception:
        total_val = 0

    db.create_transaction(
        session['user']['email'], crop_id, crop_name, action,
        clean_p, quantity, total_val,
    )
    flash("Order placed successfully!", "success")
    return redirect(url_for("cart"))

# ==========================================
# 1) ADMIN DASHBOARD - FULL WEBSITE MANAGEMENT
# ==========================================

@app.route("/admin-dashboard")
def admin_dashboard():
    if 'user' not in session or session['user'].get('role') != 'admin':
        flash("Admin access required. Please login with an administrator account.", "error")
        return redirect(url_for("login"))
    
    users = db.get_users()
    crops = db.get_crops()
    market_data = db.get_market_data()
    soils = db.get_soils()
    fertilizers = db.get_fertilizers()
    transactions = db.get_transactions()
    queries = db.get_queries()

    total_users = len(users)
    total_farmers = len([u for u in users if u.get('role') == 'farmer'])
    total_admins = len([u for u in users if u.get('role') == 'admin'])
    total_crops = len(crops)
    total_market_items = len(market_data)
    total_orders = len(transactions)
    pending_queries = len([q for q in queries if q.get('status') == 'Pending'])

    return render_template(
        "admin_dashboard.html",
        users=users,
        crops=crops,
        market_data=market_data,
        soils=soils,
        fertilizers=fertilizers,
        transactions=transactions,
        queries=queries,
        stats={
            "total_users": total_users,
            "total_farmers": total_farmers,
            "total_admins": total_admins,
            "total_crops": total_crops,
            "total_market_items": total_market_items,
            "total_orders": total_orders,
            "pending_queries": pending_queries
        }
    )

# Admin: User Management
@app.route("/admin/add-user", methods=["POST"])
def admin_add_user():
    if 'user' not in session or session['user'].get('role') != 'admin':
        return redirect(url_for("login"))
    
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "").strip()

    if not name or not email or not password:
        flash("All fields are required to add a user.", "error")
        return redirect(url_for("admin_dashboard"))

    if email in [ADMIN_EMAIL, ADMIN_USERNAME] or db.get_user_by_login(email):
        flash(f"User with email '{email}' already exists or is reserved!", "error")
        return redirect(url_for("admin_dashboard"))

    # Only 1 admin is permitted in the system. All other accounts are farmers/users.
    db.create_user(name, email, generate_password_hash(password))
    flash(f"Farmer user '{name}' ({email}) registered successfully!", "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/delete-user/<email>", methods=["POST"])
def admin_delete_user(email):
    if 'user' not in session or session['user'].get('role') != 'admin':
        return redirect(url_for("login"))
    
    clean_email = email.strip().lower()
    if clean_email in [ADMIN_EMAIL, ADMIN_USERNAME]:
        flash("Action denied: The primary single administrator account is permanent and cannot be deleted!", "error")
        return redirect(url_for("admin_dashboard"))

    if db.delete_user(clean_email):
        flash(f"Farmer user '{email}' has been removed successfully.", "success")
    else:
        flash(f"User '{email}' not found.", "error")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/toggle-role/<email>", methods=["POST"])
def admin_toggle_role(email):
    if 'user' not in session or session['user'].get('role') != 'admin':
        return redirect(url_for("login"))
    
    flash("Action denied: Only ONE person can be the system administrator. Additional admin accounts are not permitted.", "error")
    return redirect(url_for("admin_dashboard"))

# Admin: Crop Management
@app.route("/admin/add-crop", methods=["POST"])
def admin_add_crop():
    if 'user' not in session or session['user'].get('role') != 'admin':
        return redirect(url_for("login"))
    
    crop_name = request.form.get("name", "").strip()
    if not crop_name:
        flash("Crop name cannot be empty.", "error")
        return redirect(url_for("admin_dashboard"))

    crop_key = crop_name.lower().replace(" ", "_")
    soil = request.form.get("soil", "Loamy Soil").strip()
    climate = request.form.get("climate", "Tropical").strip()
    rainfall = request.form.get("rainfall", "75-120 cm").strip()
    ph = request.form.get("ph", "6.0-7.5").strip()
    season = request.form.get("season", "Kharif").strip()
    crop_yield = request.form.get("yield", "30-40 quintals/hectare").strip()
    description = request.form.get("description", "Quality agricultural harvest.").strip()
    image = request.form.get("image", "/static/images/farm.avif").strip()

    crop = {
        "name": crop_name,
        "soil": soil,
        "climate": climate,
        "rainfall": rainfall,
        "ph": ph,
        "season": season,
        "yield": crop_yield,
        "description": description,
        "image": image if image else "/static/images/farm.avif"
    }
    db.upsert_crop(crop_key, crop)
    flash(f"Crop '{crop_name}' published to catalog successfully!", "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/delete-crop/<crop_id>", methods=["POST"])
def admin_delete_crop(crop_id):
    if 'user' not in session or session['user'].get('role') != 'admin':
        return redirect(url_for("login"))
    
    crop = db.get_crops().get(crop_id)
    if crop:
        cname = crop["name"]
        db.delete_crop(crop_id)
        flash(f"Crop '{cname}' deleted from website.", "success")
    else:
        flash("Crop not found.", "error")
    return redirect(url_for("admin_dashboard"))

# Admin: Market Mandi Rates Management
@app.route("/admin/update-market-price", methods=["POST"])
def admin_update_market_price():
    if 'user' not in session or session['user'].get('role') != 'admin':
        return redirect(url_for("login"))

    crop_id = request.form.get("crop_id")
    price = request.form.get("price", "").strip()
    trend = request.form.get("trend", "stable")
    change = request.form.get("change", "0.0%").strip()
    item = db.get_market_item(crop_id)
    clean_num = ''.join(c for c in price if c.isdigit())
    if item and clean_num:
        db.update_market_item(crop_id, int(clean_num), trend, change)
        flash(f"Market rate for '{item['crop']}' updated successfully ({trend})!", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/add-market-crop", methods=["POST"])
def admin_add_market_crop():
    if 'user' not in session or session['user'].get('role') != 'admin':
        return redirect(url_for("login"))

    crop = request.form.get("crop", "").strip()
    variety = request.form.get("variety", "Hybrid").strip()
    price = request.form.get("price", "2500").strip()
    trend = request.form.get("trend", "stable")
    change = request.form.get("change", "+1.0%").strip()
    crop_id = crop.lower().replace(" ", "_")

    if not crop:
        flash("Crop name is required.", "error")
        return redirect(url_for("admin_dashboard"))

    clean_num = ''.join(c for c in price if c.isdigit()) or "2500"
    db.upsert_market_item(crop_id, crop, variety, int(clean_num), trend, change)
    flash(f"Commodity '{crop}' added to live market ticker!", "success")
    return redirect(url_for("admin_dashboard"))
@app.route("/admin/delete-market-crop/<crop_id>", methods=["POST"])
def admin_delete_market_crop(crop_id):
    if 'user' not in session or session['user'].get('role') != 'admin':
        return redirect(url_for("login"))
    
    db.delete_market_item(crop_id)
    flash(f"Market listing '{crop_id}' removed.", "success")
    return redirect(url_for("admin_dashboard"))

# Admin: Orders Management
@app.route("/admin/update-order-status/<int:order_id>", methods=["POST"])
def admin_update_order_status(order_id):
    if 'user' not in session or session['user'].get('role') != 'admin':
        return redirect(url_for("login"))
    
    new_status = request.form.get("status", "Confirmed")
    if db.update_transaction_status(order_id, new_status):
        flash(f"Order #{order_id} marked as '{new_status}'.", "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/delete-order/<int:order_id>", methods=["POST"])
def admin_delete_order(order_id):
    if 'user' not in session or session['user'].get('role') != 'admin':
        return redirect(url_for("login"))
    
    db.delete_transaction(order_id)
    flash(f"Order #{order_id} deleted successfully.", "success")
    return redirect(url_for("admin_dashboard"))

# Admin: Farmer Inquiries Management
@app.route("/admin/resolve-query/<int:query_id>", methods=["POST"])
def admin_resolve_query(query_id):
    if 'user' not in session or session['user'].get('role') != 'admin':
        return redirect(url_for("login"))
    
    if db.toggle_query_status(query_id):
        flash(f"Inquiry #{query_id} status changed successfully.", "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/delete-query/<int:query_id>", methods=["POST"])
def admin_delete_query(query_id):
    if 'user' not in session or session['user'].get('role') != 'admin':
        return redirect(url_for("login"))
    
    db.delete_query(query_id)
    flash(f"Query #{query_id} deleted.", "success")
    return redirect(url_for("admin_dashboard"))


# ==========================================
# 2) USER / FARMER DASHBOARD
# ==========================================

@app.route("/dashboard")
def dashboard():
    user = session.get('user')
    user_email = user['email'] if user else None
    
    # Filter transactions & queries for current user
    user_transactions = db.get_transactions(user_email) if user_email else []
    user_queries = db.get_queries(user_email) if user_email else []
    market_data = db.get_market_data()
    crops_data = db.get_crops()
    soils_data = db.get_soils()
    fertilizers_data = db.get_fertilizers()
    
    return render_template(
        "dashboard.html",
        user=user,
        transactions=user_transactions,
        queries=user_queries,
        market_data=market_data,
        crops_count=len(crops_data),
        soils_count=len(soils_data),
        fertilizers_count=len(fertilizers_data),
        crops_data=crops_data
    )

@app.route("/farmer/submit-query", methods=["POST"])
def farmer_submit_query():
    name = request.form.get("name")
    email = request.form.get("email")
    subject = request.form.get("subject", "Agricultural Query").strip()
    message = request.form.get("message", "").strip()
    
    if not message:
        flash("Message content cannot be blank.", "error")
        return redirect(url_for("dashboard"))
    
    curr_user = session.get('user', {})
    sender_name = name or curr_user.get('name', 'Farmer User')
    sender_email = email or curr_user.get('email', 'farmer@gmail.com')
    
    db.create_query(
        sender_name,
        sender_email,
        subject if subject else "General Farm Inquiry",
        message,
    )
    flash("Your inquiry has been submitted to the portal administrator! You will see updates in your dashboard.", "success")
    return redirect(url_for("dashboard"))

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/crops")
def crops():
    crops, soils = build_catalog(db.get_crops(), db.get_soils())
    return render_template("farming_guide.html", crops=crops, soils=soils, initial_section="crops")

@app.route("/crop/<crop_id>")
def crop_detail(crop_id):
    crops, _ = build_catalog(db.get_crops(), db.get_soils())
    crop = crops.get(crop_id)
    if not crop:
        return "Crop not found", 404
    return render_template("crop_detail.html", crop=crop)

@app.route("/soil")
def soil():
    crops, soils = build_catalog(db.get_crops(), db.get_soils())
    return render_template("farming_guide.html", crops=crops, soils=soils, initial_section="soils")

@app.route("/soil/<soil_id>")
def soil_detail(soil_id):
    _, soils = build_catalog(db.get_crops(), db.get_soils())
    soil = soils.get(soil_id)
    if not soil:
        return "Soil not found", 404
    return render_template("soil_detail.html", soil=soil)

@app.route("/crop-finder")
def crop_finder():
    crops, soils = build_catalog(db.get_crops(), db.get_soils())
    return render_template("crop-finder.html", crops=crops, soils=soils)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/fertilizers")
def fertilizers():
    query = request.args.get("q", "").strip()[:80]
    crops, soils = build_catalog(db.get_crops(), db.get_soils())
    all_fertilizers = build_fertilizer_catalog(db.get_fertilizers())
    matches = [item for item in all_fertilizers if fertilizer_matches(item, query)]
    return render_template(
        "fertilizers.html", fertilizers=matches, total_fertilizers=len(all_fertilizers),
        query=query, crops=crops, soils=soils,
    )

@app.route("/market")
def market():
    # Market prices are loaded client-side from the Finnid live-price proxy.
    # Do not fall back to database-seeded/sample prices.
    return render_template("market.html")


@app.route("/api/live-market-prices")
def live_market_prices():
    """Proxy Finnid's data.gov.in-backed mandi feed for Maharashtra."""
    filters = {
        "state": "Maharashtra",
        "district": request.args.get("district", "").strip()[:100],
        "market": request.args.get("market", "").strip()[:120],
        "commodity": request.args.get("commodity", "").strip()[:120],
        "grade": request.args.get("grade", "").strip()[:80],
    }
    cache_key = tuple(filters.values())
    cached = _live_price_cache.get(cache_key)
    if cached and time.time() - cached[0] < 600:
        return jsonify(cached[1])

    payload = json.dumps(filters).encode("utf-8")
    upstream_request = urlrequest.Request(
        FINNID_PRICE_URL,
        data=payload,
        headers={"Content-Type": "application/json", "Accept": "application/json", "User-Agent": "AgricultureHelper/1.0"},
        method="POST",
    )
    try:
        with urlrequest.urlopen(upstream_request, timeout=20) as response:
            upstream = json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as error:
        app.logger.warning("Finnid live price request failed: %s", error)
        if cached:
            stale = dict(cached[1])
            stale["stale"] = True
            return jsonify(stale)
        return jsonify({"success": False, "error": "Live mandi prices are temporarily unavailable."}), 502

    records = upstream.get("data", []) if upstream.get("success") else []
    clean_records = []
    for row in records[:1000]:
        clean_records.append({
            "commodity": row.get("commodity", ""), "market": row.get("market", ""),
            "state": row.get("state", ""), "district": row.get("district", ""),
            "grade": row.get("grade", ""), "minPrice": row.get("minPrice", 0),
            "maxPrice": row.get("maxPrice", 0), "modalPrice": row.get("modalPrice", 0),
            "arrivalDate": row.get("arrivalDate", ""), "source": row.get("source", "data.gov.in"),
        })
    result = {
        "success": True, "data": clean_records, "count": len(clean_records),
        "provider": "Finnid Live Prices", "providerUrl": "https://finnid.in/MarketLinkage/LivePrices",
        "source": "data.gov.in", "fetchedAt": int(time.time()),
    }
    _live_price_cache[cache_key] = (time.time(), result)
    return jsonify(result)

@app.route("/trade/<crop_id>")
def trade(crop_id):
    crop = db.get_market_item(crop_id)
    if not crop:
        return "Crop Market Data not found", 404
    return render_template("trading.html", crop=crop)

# API for searching crops, soils, and fertilizers
@app.route("/api/search", methods=["POST"])
def search():
    search_query = request.json.get("query", "").lower().strip()
    if not search_query:
        return jsonify({
            "type": "not_found",
            "message": "Please enter a search term"
        }), 400
    
    crops, soils = build_catalog(db.get_crops(), db.get_soils())

    # 1. Search in crops
    for key, crop in crops.items():
        if search_query == key or search_query in crop["name"].lower() or key in search_query:
            return jsonify({
                "type": "crop",
                "data": crop
            })
    
    # 2. Search in soils
    for key, soil in soils.items():
        clean_key = key.replace(" soil", "").strip()
        if search_query == key or search_query == clean_key or search_query in soil["name"].lower() or clean_key in search_query:
            return jsonify({
                "type": "soil",
                "data": soil
            })
        
    # 3. Search in fertilizers
    for fert in build_fertilizer_catalog(db.get_fertilizers()):
        if fertilizer_matches(fert, search_query):
            return jsonify({
                "type": "fertilizer",
                "data": fert
            })
    
    return jsonify({
        "type": "not_found",
        "message": f"No results found for '{search_query}'"
    }), 404

if __name__ == "__main__":
    try:
        db.initialize_database()
    except db.Error as error:
        raise SystemExit(
            "Could not connect to MySQL. Start MySQL Server and verify the "
            f"MYSQL_* settings in .env. Details: {error}"
        ) from None
    app.run(debug=True)
