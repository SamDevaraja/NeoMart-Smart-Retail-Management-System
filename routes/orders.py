from flask import Blueprint, redirect, url_for, session, render_template, request
from database.mongo import get_db
from datetime import datetime
from bson import ObjectId

orders_bp = Blueprint("orders", __name__)

# ==========================
# PLACE ORDER
# ==========================
@orders_bp.route("/orders/place")
def place_order():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    db = get_db()
    cart_items = list(db.cart.find({"user_id": session["user_id"]}))

    if not cart_items:
        return redirect(url_for("cart.view_cart"))

    total = sum(item["price"] * item.get("quantity", 1) for item in cart_items)

    db.orders.insert_one({
        "user_id": session["user_id"],
        "items": cart_items,
        "total": total,
        "status": "Placed",
        "created_at": datetime.now()
    })

    for item in cart_items:
        db.products.update_one(
            {"_id": ObjectId(item["product_id"])},
            {"$inc": {"stock": -item.get("quantity", 1)}}
        )

    db.cart.delete_many({"user_id": session["user_id"]})
    return redirect(url_for("orders.my_orders", success=1))


# ==========================
# MY ORDERS
# ==========================
@orders_bp.route("/orders")
def my_orders():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    db = get_db()
    orders = list(db.orders.find(
        {"user_id": session["user_id"]}
    ).sort("created_at", -1))

    total_spent = sum(o.get("total", 0) for o in orders)
    order_count = len(orders)

    return render_template(
        "user/orders.html",
        orders=orders,
        total_spent=total_spent,
        order_count=order_count
    )


# ==========================
# ORDER DETAILS (FEATURE 1)
# ==========================
@orders_bp.route("/orders/<order_id>")
def order_details(order_id):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    db = get_db()
    order = db.orders.find_one({
        "_id": ObjectId(order_id),
        "user_id": session["user_id"]
    })

    if not order:
        return redirect(url_for("orders.my_orders"))

    return render_template(
        "user/order_details.html",
        order=order
    )
