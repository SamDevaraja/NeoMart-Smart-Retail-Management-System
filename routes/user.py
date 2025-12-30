from flask import Blueprint, render_template, session, redirect, url_for, request
from database.mongo import get_db
from datetime import datetime

user_bp = Blueprint("user", __name__)

@user_bp.route("/user/dashboard")
def dashboard():
    if "user_id" not in session or session.get("role") != "user":
        return redirect(url_for("auth.login"))

    db = get_db()

    # --- SAFE GET PARAMS ---
    search = request.args.get("q", "").strip()
    category = request.args.get("category", "All")
    sort = request.args.get("sort")

    query = {"is_active": True}

    # --- CATEGORY FILTER ---
    if category != "All":
        query["category"] = category

    # --- SEARCH FILTER ---
    if search != "":
        query["name"] = {"$regex": search, "$options": "i"}

    # --- SORT ---
    sort_option = None
    if sort == "low":
        sort_option = [("price", 1)]
    elif sort == "high":
        sort_option = [("price", -1)]

    if sort_option:
        products = list(db.products.find(query).sort(sort_option))
    else:
        products = list(db.products.find(query))

    categories = db.products.distinct("category")

    return render_template(
        "user/dashboard.html",
        products=products,
        categories=categories,
        selected_category=category,
        search_query=search,
        selected_sort=sort,
        now=datetime.now()
    )


# ==========================
# USER PROFILE
# ==========================
@user_bp.route("/profile")
def profile():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    db = get_db()
    orders = list(db.orders.find({"user_id": session["user_id"]}))
    total_spent = sum(o.get("total", 0) for o in orders)

    return render_template(
        "user/profile.html",
        order_count=len(orders),
        total_spent=total_spent,
        user_id=session["user_id"]
    )
