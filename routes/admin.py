from flask import Blueprint, render_template, session, redirect, url_for, request, Response
from database.mongo import get_db
from werkzeug.utils import secure_filename
from bson import ObjectId
from config import Config
from datetime import datetime
import os

admin_bp = Blueprint("admin", __name__)

# ==========================
# ADMIN DASHBOARD
# ==========================
@admin_bp.route("/admin/dashboard")
def dashboard():
    if "user_id" not in session or session.get("role") != "admin":
        return redirect(url_for("auth.login"))

    db = get_db()

    total_products = db.products.count_documents({})
    total_orders = db.orders.count_documents({})

    revenue = sum(o.get("total", 0) for o in db.orders.find())
    out_of_stock = db.products.count_documents({"stock": {"$lte": 0}})
    low_stock_products = list(db.products.find({"stock": {"$lte": 2}}))

    status_filter = request.args.get("status", "All")
    query = {} if status_filter == "All" else {"status": status_filter}

    orders = list(db.orders.find(query).sort("created_at", -1))

    return render_template(
        "admin/dashboard.html",
        total_products=total_products,
        total_orders=total_orders,
        revenue=revenue,
        out_of_stock=out_of_stock,
        low_stock_products=low_stock_products,
        orders=orders,
        status_filter=status_filter
    )

# ==========================
# MANAGE PRODUCTS
# ==========================
@admin_bp.route("/admin/products", methods=["GET", "POST"])
def manage_products():
    if "user_id" not in session or session.get("role") != "admin":
        return redirect(url_for("auth.login"))

    db = get_db()

    if request.method == "POST":
        image = request.files.get("image")
        filename = ""

        if image and "." in image.filename:
            filename = secure_filename(image.filename)
            image.save(os.path.join(Config.UPLOAD_FOLDER, filename))

        db.products.insert_one({
            "name": request.form.get("name"),
            "price": int(request.form.get("price")),
            "category": request.form.get("category"),
            "image": filename,
            "stock": int(request.form.get("stock")),
            "is_active": True,
            "created_at": datetime.now()
        })

        return redirect(url_for("admin.manage_products"))

    products = list(db.products.find())
    return render_template("admin/manage_products.html", products=products)

# ==========================
# TOGGLE PRODUCT VISIBILITY
# ==========================
@admin_bp.route("/admin/products/toggle/<pid>")
def toggle_product(pid):
    if "user_id" not in session or session.get("role") != "admin":
        return redirect(url_for("auth.login"))

    db = get_db()

    product = db.products.find_one({"_id": ObjectId(pid)})
    if not product:
        return redirect(url_for("admin.manage_products"))

    # Default to True if field missing
    current_status = product.get("is_active", True)

    db.products.update_one(
        {"_id": ObjectId(pid)},
        {"$set": {"is_active": not current_status}}
    )

    return redirect(url_for("admin.manage_products"))
# ==========================
# DELETE PRODUCT
# ==========================
@admin_bp.route("/admin/products/delete/<pid>")
def delete_product(pid):
    if "user_id" not in session or session.get("role") != "admin":
        return redirect(url_for("auth.login"))

    db = get_db()
    db.products.delete_one({"_id": ObjectId(pid)})

    return redirect(url_for("admin.manage_products"))


# ==========================
# UPDATE STOCK (INCREASE)
# ==========================
@admin_bp.route("/admin/products/stock/<pid>", methods=["POST"])
def update_stock(pid):
    if "user_id" not in session or session.get("role") != "admin":
        return redirect(url_for("auth.login"))

    qty = int(request.form.get("quantity", 0))
    if qty <= 0:
        return redirect(url_for("admin.manage_products"))

    db = get_db()
    db.products.update_one(
        {"_id": ObjectId(pid)},
        {"$inc": {"stock": qty}}
    )

    return redirect(url_for("admin.manage_products"))

# ==========================
# EXPORT ORDERS CSV
# ==========================
@admin_bp.route("/admin/orders/export")
def export_orders_csv():
    if "user_id" not in session or session.get("role") != "admin":
        return redirect(url_for("auth.login"))

    db = get_db()
    orders = list(db.orders.find())

    def generate():
        yield "Order ID,User ID,Total,Status,Created At\n"
        for order in orders:
            created_at = ""
            if order.get("created_at"):
                created_at = order["created_at"].strftime("%Y/%m/%d %H:%M")

            yield f'{order["_id"]},{order["user_id"]},{order["total"]},{order.get("status","Placed")},{created_at}\n'

    filename = f"minimart_orders_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    return Response(
        generate(),
        mimetype="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )
@admin_bp.route("/admin/orders/update/<order_id>", methods=["POST"])
def update_order_status(order_id):
    if "user_id" not in session or session.get("role") != "admin":
        return redirect(url_for("auth.login"))

    new_status = request.form.get("status")
    current_filter = request.args.get("status", "All")

    db = get_db()
    db.orders.update_one(
        {"_id": ObjectId(order_id)},
        {"$set": {"status": new_status}}
    )

    # ✅ Redirect BACK to dashboard with SAME filter
    return redirect(url_for("admin.dashboard", status=current_filter))
