from pathlib import Path

from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash, send_from_directory
import secrets
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent
HTML_DIR = PROJECT_ROOT / "html"
CSS_DIR = PROJECT_ROOT / "css"
IMAGES_DIR = PROJECT_ROOT / "images"
DATABASE_DIR = PROJECT_ROOT / "database"

app = Flask(__name__, template_folder=str(HTML_DIR), static_folder=None)
app.secret_key = secrets.token_hex(16)


@app.route("/static/css/<path:filename>")
def css_file(filename):
    return send_from_directory(CSS_DIR, filename)


@app.route("/static/images/<path:filename>")
def image_file(filename):
    return send_from_directory(IMAGES_DIR, filename)

# The Single Dedicated System Administrator
ADMIN_USER = {
    "name": "System Administrator",
    "username": "admin",
    "email": "admin@gmail.com",
    "password": "123",
    "role": "admin"
}

# Registered Users (Multiple farmers can register and login; only 1 admin exists)
USERS = [
    ADMIN_USER,
    {"name": "Farmer Demo", "email": "farmer@gmail.com", "password": "12345", "role": "farmer"}
]

TRANSACTIONS = [
    {
        "id": 1,
        "user_email": "farmer@gmail.com",
        "crop_id": "rice",
        "crop_name": "Rice (Paddy)",
        "action": "BUY",
        "price": "3200",
        "quantity": "5",
        "total": "16000",
        "status": "Confirmed",
        "date": "2026-09-24 09:30"
    },
    {
        "id": 2,
        "user_email": "farmer@gmail.com",
        "crop_id": "wheat",
        "crop_name": "Wheat",
        "action": "SELL",
        "price": "2800",
        "quantity": "10",
        "total": "28000",
        "status": "Processing",
        "date": "2026-09-24 11:45"
    }
]

QUERIES = [
    {
        "id": 1,
        "name": "Farmer Demo",
        "email": "farmer@gmail.com",
        "subject": "Soil pH & Fertilizer Recommendation",
        "message": "My field has Black Soil with pH around 7.5. Which fertilizer combination gives best yield for Cotton?",
        "date": "2026-09-24 10:15",
        "status": "Pending"
    },
    {
        "id": 2,
        "name": "Ramesh Kumar",
        "email": "ramesh@kisan.in",
        "subject": "Wheat Seeds Variety Inquiry",
        "message": "Are certified Sharbati wheat seeds available for the upcoming Rabi season in the market?",
        "date": "2026-09-24 11:30",
        "status": "Resolved"
    }
]


CROPS_DATA = {
    "rice": {
        "name": "Rice",
        "soil": "Clayey Soil",
        "climate": "Warm & Humid",
        "rainfall": "100-250 cm",
        "ph": "5.5-7.0",
        "season": "Kharif (July-November)",
        "yield": "50-60 quintals/hectare",
        "description": "Rice is a staple food crop that requires clayey soil with high water content and warm temperature.",
        "image": "/static/images/rice.jpg"
    },
    "wheat": {
        "name": "Wheat",
        "soil": "Loamy Soil",
        "climate": "Temperate",
        "rainfall": "50-100 cm",
        "ph": "6.0-7.5",
        "season": "Rabi (October-March)",
        "yield": "40-50 quintals/hectare",
        "description": "Wheat grows well in loamy soil with moderate rainfall. It's a winter crop.",
        "image": "/static/images/wheatcrop.jpg"
    },
    "corn": {
        "name": "Corn (Maize)",
        "soil": "Loamy Soil",
        "climate": "Warm",
        "rainfall": "50-100 cm",
        "ph": "6.0-7.5",
        "season": "Kharif (May-September)",
        "yield": "40-50 quintals/hectare",
        "description": "Maize prefers well-drained loamy soil and sunny weather. High yield crop.",
        "image": "/static/images/Ears-corn.jpg"
    },
    "sunflower": {
        "name": "Sunflower",
        "soil": "Loamy & Sandy Soil",
        "climate": "Warm & Dry",
        "rainfall": "50-75 cm",
        "ph": "6.0-7.5",
        "season": "Summer (February-May)",
        "yield": "15-20 quintals/hectare",
        "description": "Sunflower is an oil crop that adapts well to various soils.",
        "image": "/static/images/sunflower.jpg"
    },
    "cotton": {
        "name": "Cotton",
        "soil": "Deep Loamy Soil",
        "climate": "Warm & Dry",
        "rainfall": "50-100 cm",
        "ph": "6.0-7.5",
        "season": "Kharif (May-October)",
        "yield": "15-20 quintals/hectare",
        "description": "Cotton requires well-drained deep loamy soil and warm climate.",
        "image": "/static/images/cotton.jpg"
    },
    "soybean": {
        "name": "Soybean",
        "soil": "Loamy & Clayey Soil",
        "climate": "Warm",
        "rainfall": "50-100 cm",
        "ph": "6.0-7.0",
        "season": "Kharif (June-October)",
        "yield": "15-25 quintals/hectare",
        "description": "Soybean is a protein-rich legume crop suited for loamy soils.",
        "image": "/static/images/soybean.jpg"
    },
    "sugarcane": {
        "name": "Sugarcane",
        "soil": "Loamy & Clayey Soil",
        "climate": "Warm & Humid",
        "rainfall": "100-150 cm",
        "ph": "5.5-7.0",
        "season": "Year-round (12 months)",
        "yield": "60-70 tonnes/hectare",
        "description": "Sugarcane requires rich fertile soil and warm humid climate.",
        "image": "/static/images/sugarcane.jpg"
    }
}

SOIL_DATA = {
    "black soil": {
        "name": "Black Soil",
        "color": "Dark Black",
        "texture": "Clay",
        "ph": "5.5-8.5",
        "fertility": "High",
        "moisture": "High",
        "best_crops": "Cotton, Sugarcane, Wheat",
        "description": "Black soil is rich in minerals and organic matter. Excellent for cotton and sugarcane.",
        "image": "/static/images/black soil.jpg"
    },
    "clayey soil": {
        "name": "Clayey Soil",
        "color": "Brown/Grey",
        "texture": "Fine",
        "ph": "6.0-8.5",
        "fertility": "High",
        "moisture": "Very High",
        "best_crops": "Rice, Wheat, Sugarcane",
        "description": "Clayey soil retains moisture and nutrients. Perfect for rice cultivation.",
        "image": "/static/images/claysoil.jpg"
    },
    "red soil": {
        "name": "Red Soil",
        "color": "Reddish",
        "texture": "Medium",
        "ph": "5.5-7.5",
        "fertility": "Medium",
        "moisture": "Low",
        "best_crops": "Groundnut, Millets, Pulses",
        "description": "Red soil is laterite and acidic. Suitable for groundnut and pulses.",
        "image": "/static/images/red soil.jpg"
    },
    "sandy soil": {
        "name": "Sandy Soil",
        "color": "Light Brown",
        "texture": "Coarse",
        "ph": "6.0-8.0",
        "fertility": "Low",
        "moisture": "Very Low",
        "best_crops": "Carrots, Peanuts, Watermelon",
        "description": "Sandy soil drains quickly but lacks nutrients. Needs more fertilizer.",
        "image": "/static/images/sandysoil.jpg"
    },
    "loamy soil": {
        "name": "Loamy Soil",
        "color": "Brown",
        "texture": "Medium",
        "ph": "6.0-7.5",
        "fertility": "Very High",
        "moisture": "Good",
        "best_crops": "Wheat, Corn, Vegetables",
        "description": "Loamy soil is ideal for most crops. Best for overall agriculture.",
        "image": "/static/images/loamy soil.jpg"
    },
    "silt soil": {
        "name": "Silt Soil",
        "color": "Light Yellow",
        "texture": "Fine",
        "ph": "6.5-8.0",
        "fertility": "Medium",
        "moisture": "Good",
        "best_crops": "Wheat, Rice, Vegetables",
        "description": "Silt soil is soft and fertile. Good water retention and drainage.",
        "image": "/static/images/silt-soil.jpg"
    }
}

FERTILIZER_DATA = {
    "urea": {
        "name": "Urea",
        "type": "Nitrogenous",
        "npk": "46-0-0",
        "best_for": "Wheat, Rice, Maize",
        "usage": "Use specifically for leafy growth and green color. Apply as top dressing.",
        "precautions": "Avoid direct contact with seeds. Store in a dry place to prevent caking.",
        "image": "/static/images/images.jpg"
    },
    "dap": {
        "name": "DAP (Diammonium Phosphate)",
        "type": "Phosphate",
        "npk": "18-46-0",
        "best_for": "Cotton, Sugarcane, Pulses",
        "usage": "Best applied at planting time to promote strong root development.",
        "precautions": "Can cause seed damage if placed too close. Use recommended dosage.",
        "image": "/static/images/images (1).jpg"
    },
    "mop": {
        "name": "MOP (Muriate of Potash)",
        "type": "Potash",
        "npk": "0-0-60",
        "best_for": "Potatoes, Tomatoes, Fruits",
        "usage": "Improves fruit quality and disease resistance. Apply during crop growth.",
        "precautions": "Can cause chloride toxicity in sensitive crops like tobacco.",
        "image": "/static/images/about.jpg"
    },
    "npk_complex": {
        "name": "NPK Complex",
        "type": "Balanced",
        "npk": "10-26-26",
        "best_for": "Vegetables, Orchards, Cash Crops",
        "usage": "Balanced supply of major nutrients. Suitable for basal application.",
        "precautions": "Apply evenly. Avoid over-application to prevent nutrient runoff.",
        "image": "/static/images/about2.jpg"
    }
}

MARKET_DATA = [
     {"id": "rice", "crop": "Rice (Paddy)", "variety": "Basmati", "price": "₹ 3,200", "price_val": 3200, "trend": "up", "change": "+2.5%"},
     {"id": "wheat", "crop": "Wheat", "variety": "Sharbati", "price": "₹ 2,800", "price_val": 2800, "trend": "up", "change": "+1.2%"},
     {"id": "corn", "crop": "Corn (Maize)", "variety": "Hybrid", "price": "₹ 1,950", "price_val": 1950, "trend": "down", "change": "-0.5%"},
     {"id": "cotton", "crop": "Cotton", "variety": "BT Cotton", "price": "₹ 7,500", "price_val": 7500, "trend": "up", "change": "+5.0%"},
     {"id": "soybean", "crop": "Soybean", "variety": "Yellow", "price": "₹ 4,600", "price_val": 4600, "trend": "stable", "change": "0.0%"},
     {"id": "sugarcane", "crop": "Sugarcane", "variety": "Variety 86032", "price": "₹ 315", "price_val": 315, "trend": "up", "change": "+1.0%"},
     {"id": "sunflower", "crop": "Sunflower", "variety": "Oilseed", "price": "₹ 6,400", "price_val": 6400, "trend": "down", "change": "-2.1%"},
]

@app.route("/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("fullname", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "").strip()

        if not name or not email or not password:
            return render_template("reg.html", error="All fields are required.")

        # Disallow taking admin email or username
        if email in [ADMIN_USER["email"].lower(), ADMIN_USER["username"].lower()] or name.lower() == "admin":
            return render_template("reg.html", error="This username/email is reserved exclusively for the system administrator.")

        # Check if user already exists
        if any(u['email'].lower() == email for u in USERS):
            return render_template("reg.html", error="Email already registered. Please login.")

        # Multiple users can register, but all registered users are farmers (single admin only)
        USERS.append({
            "name": name,
            "email": email,
            "password": password,
            "role": "farmer"
        })
        flash(f"Account registered successfully for {name}! Please login below.", "success")
        return redirect(url_for("login"))

    return render_template("reg.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        login_id = request.form.get("username_or_email", request.form.get("email", "")).strip().lower()
        password = request.form.get("password", "").strip()
        
        # 1. Single Admin Authentication (Username: 'admin' or Email: 'admin@gmail.com', Password: '123')
        if login_id in [ADMIN_USER["username"].lower(), ADMIN_USER["email"].lower()] and password == ADMIN_USER["password"]:
            session['user'] = ADMIN_USER
            flash("Welcome, Administrator! You have logged into the Admin Command Center.", "success")
            return redirect(url_for("admin_dashboard"))
        
        # 2. Multiple Regular Users (Farmers) Authentication
        user = next((
            u for u in USERS 
            if (u.get('email', '').lower() == login_id or u.get('username', '').lower() == login_id) 
            and u.get('password') == password
        ), None)

        if user:
            session['user'] = user
            if user.get('role') == 'admin':
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

@app.route("/cart")
def cart():
    if 'user' not in session:
        return redirect(url_for("login"))
    
    user_email = session['user']['email']
    user_cart = [t for t in TRANSACTIONS if t['user_email'] == user_email]
    return render_template("cart.html", transactions=user_cart)

@app.route("/trade-action", methods=["POST"])
def trade_action():
    if 'user' not in session:
        return redirect(url_for("login"))
    
    crop_id = request.form.get("crop_id")
    action = request.form.get("action", "BUY").upper()
    price = request.form.get("price", "0")
    quantity = request.form.get("quantity", "1")
    
    crop_info = next((item for item in MARKET_DATA if item["id"] == crop_id), None)
    crop_name = crop_info["crop"] if crop_info else (crop_id.capitalize() if crop_id else "Crop")
    
    try:
        clean_p = int(''.join(c for c in str(price) if c.isdigit()) or "0")
        total_val = clean_p * int(quantity)
    except Exception:
        total_val = 0

    new_id = (TRANSACTIONS[-1]["id"] + 1) if TRANSACTIONS else 1
    TRANSACTIONS.append({
        "id": new_id,
        "user_email": session['user']['email'],
        "crop_id": crop_id,
        "crop_name": crop_name,
        "action": action,
        "price": str(price).replace("₹", "").strip(),
        "quantity": str(quantity),
        "total": str(total_val),
        "status": "Confirmed",
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    })
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
    
    total_users = len(USERS)
    total_farmers = len([u for u in USERS if u.get('role') == 'farmer'])
    total_admins = len([u for u in USERS if u.get('role') == 'admin'])
    total_crops = len(CROPS_DATA)
    total_market_items = len(MARKET_DATA)
    total_orders = len(TRANSACTIONS)
    pending_queries = len([q for q in QUERIES if q.get('status') == 'Pending'])

    return render_template(
        "admin_dashboard.html",
        users=USERS,
        crops=CROPS_DATA,
        market_data=MARKET_DATA,
        soils=SOIL_DATA,
        fertilizers=FERTILIZER_DATA,
        transactions=TRANSACTIONS,
        queries=QUERIES,
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

    if email in [ADMIN_USER["email"].lower(), ADMIN_USER["username"].lower()] or any(u['email'].lower() == email for u in USERS):
        flash(f"User with email '{email}' already exists or is reserved!", "error")
        return redirect(url_for("admin_dashboard"))

    # Only 1 admin is permitted in the system. All other accounts are farmers/users.
    USERS.append({
        "name": name,
        "email": email,
        "password": password,
        "role": "farmer"
    })
    flash(f"Farmer user '{name}' ({email}) registered successfully!", "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/delete-user/<email>", methods=["POST"])
def admin_delete_user(email):
    if 'user' not in session or session['user'].get('role') != 'admin':
        return redirect(url_for("login"))
    
    clean_email = email.strip().lower()
    if clean_email in [ADMIN_USER["email"].lower(), ADMIN_USER["username"].lower()]:
        flash("Action denied: The primary single administrator account is permanent and cannot be deleted!", "error")
        return redirect(url_for("admin_dashboard"))

    global USERS
    original_len = len(USERS)
    USERS = [u for u in USERS if u['email'].lower() != clean_email]
    if len(USERS) < original_len:
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

    CROPS_DATA[crop_key] = {
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
    flash(f"Crop '{crop_name}' published to catalog successfully!", "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/delete-crop/<crop_id>", methods=["POST"])
def admin_delete_crop(crop_id):
    if 'user' not in session or session['user'].get('role') != 'admin':
        return redirect(url_for("login"))
    
    if crop_id in CROPS_DATA:
        cname = CROPS_DATA[crop_id]["name"]
        del CROPS_DATA[crop_id]
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

    item = next((m for m in MARKET_DATA if m["id"] == crop_id), None)
    if item:
        clean_num = ''.join(c for c in price if c.isdigit())
        item["price"] = f"₹ {price.replace('₹', '').strip()}"
        if clean_num:
            item["price_val"] = int(clean_num)
        item["trend"] = trend
        item["change"] = change
        flash(f"Market rate for '{item['crop']}' updated to {item['price']} ({trend})!", "success")
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
    MARKET_DATA.append({
        "id": crop_id,
        "crop": crop,
        "variety": variety,
        "price": f"₹ {price.replace('₹', '').strip()}",
        "price_val": int(clean_num),
        "trend": trend,
        "change": change
    })
    flash(f"Commodity '{crop}' added to live market ticker!", "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/delete-market-crop/<crop_id>", methods=["POST"])
def admin_delete_market_crop(crop_id):
    if 'user' not in session or session['user'].get('role') != 'admin':
        return redirect(url_for("login"))
    
    global MARKET_DATA
    MARKET_DATA = [m for m in MARKET_DATA if m["id"] != crop_id]
    flash(f"Market listing '{crop_id}' removed.", "success")
    return redirect(url_for("admin_dashboard"))

# Admin: Orders Management
@app.route("/admin/update-order-status/<int:order_id>", methods=["POST"])
def admin_update_order_status(order_id):
    if 'user' not in session or session['user'].get('role') != 'admin':
        return redirect(url_for("login"))
    
    new_status = request.form.get("status", "Confirmed")
    order = next((t for t in TRANSACTIONS if t.get("id") == order_id), None)
    if order:
        order["status"] = new_status
        flash(f"Order #{order_id} marked as '{new_status}'.", "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/delete-order/<int:order_id>", methods=["POST"])
def admin_delete_order(order_id):
    if 'user' not in session or session['user'].get('role') != 'admin':
        return redirect(url_for("login"))
    
    global TRANSACTIONS
    TRANSACTIONS = [t for t in TRANSACTIONS if t.get("id") != order_id]
    flash(f"Order #{order_id} deleted successfully.", "success")
    return redirect(url_for("admin_dashboard"))

# Admin: Farmer Inquiries Management
@app.route("/admin/resolve-query/<int:query_id>", methods=["POST"])
def admin_resolve_query(query_id):
    if 'user' not in session or session['user'].get('role') != 'admin':
        return redirect(url_for("login"))
    
    query = next((q for q in QUERIES if q.get("id") == query_id), None)
    if query:
        query["status"] = "Resolved" if query["status"] == "Pending" else "Pending"
        flash(f"Inquiry #{query_id} status changed to '{query['status']}'.", "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/delete-query/<int:query_id>", methods=["POST"])
def admin_delete_query(query_id):
    if 'user' not in session or session['user'].get('role') != 'admin':
        return redirect(url_for("login"))
    
    global QUERIES
    QUERIES = [q for q in QUERIES if q.get("id") != query_id]
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
    user_transactions = [t for t in TRANSACTIONS if t.get('user_email') == user_email] if user_email else []
    user_queries = [q for q in QUERIES if q.get('email') == user_email] if user_email else []
    
    return render_template(
        "dashboard.html",
        user=user,
        transactions=user_transactions,
        queries=user_queries,
        market_data=MARKET_DATA,
        crops_count=len(CROPS_DATA),
        soils_count=len(SOIL_DATA),
        fertilizers_count=len(FERTILIZER_DATA),
        crops_data=CROPS_DATA
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
    
    new_id = (QUERIES[-1]["id"] + 1) if QUERIES else 1
    QUERIES.append({
        "id": new_id,
        "name": sender_name,
        "email": sender_email,
        "subject": subject if subject else "General Farm Inquiry",
        "message": message,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "status": "Pending"
    })
    flash("Your inquiry has been submitted to the portal administrator! You will see updates in your dashboard.", "success")
    return redirect(url_for("dashboard"))

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/crops")
def crops():
    return render_template("crops.html", crops=CROPS_DATA)

@app.route("/crop/<crop_id>")
def crop_detail(crop_id):
    crop = CROPS_DATA.get(crop_id)
    if not crop:
        return "Crop not found", 404
    return render_template("crop_detail.html", crop=crop)

@app.route("/soil")
def soil():
    return render_template("soil.html", soils=SOIL_DATA)

@app.route("/soil/<soil_id>")
def soil_detail(soil_id):
    soil = SOIL_DATA.get(soil_id)
    if not soil:
        return "Soil not found", 404
    return render_template("soil_detail.html", soil=soil)

@app.route("/crop-finder")
def crop_finder():
    return render_template("crop-finder.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/fertilizers")
def fertilizers():
    return render_template("fertilizers.html", fertilizers=FERTILIZER_DATA)

@app.route("/market")
def market():
    return render_template("market.html", market_prices=MARKET_DATA)

@app.route("/trade/<crop_id>")
def trade(crop_id):
    crop = next((item for item in MARKET_DATA if item["id"] == crop_id), None)
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
    
    # 1. Search in crops
    for key, crop in CROPS_DATA.items():
        if search_query == key or search_query in crop["name"].lower() or key in search_query:
            return jsonify({
                "type": "crop",
                "data": crop
            })
    
    # 2. Search in soils
    for key, soil in SOIL_DATA.items():
        clean_key = key.replace(" soil", "").strip()
        if search_query == key or search_query == clean_key or search_query in soil["name"].lower() or clean_key in search_query:
            return jsonify({
                "type": "soil",
                "data": soil
            })
        
    # 3. Search in fertilizers
    for key, fert in FERTILIZER_DATA.items():
        if search_query == key or search_query in fert["name"].lower() or search_query in fert.get("type", "").lower():
            return jsonify({
                "type": "fertilizer",
                "data": fert
            })
    
    return jsonify({
        "type": "not_found",
        "message": f"No results found for '{search_query}'"
    }), 404

if __name__ == "__main__":
    app.run(debug=True)
