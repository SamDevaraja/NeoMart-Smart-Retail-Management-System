from flask import Blueprint, redirect, url_for, session, render_template, request
from database.mongo import get_db
from bson import ObjectId

cart_bp = Blueprint("cart", __name__)

@cart_bp.route("/cart/add/<product_id>")
def add_to_cart(product_id):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    db = get_db()
    product = db.products.find_one({"_id": ObjectId(product_id)})

    if not product or product.get("stock", 0) <= 0:
        return redirect(request.referrer or url_for("user.dashboard"))

    existing_item = db.cart.find_one({
        "user_id": session["user_id"],
        "product_id": str(product["_id"])
    })

    if existing_item:
        db.cart.update_one(
            {"_id": existing_item["_id"]},
            {"$inc": {"quantity": 1}}
        )
    else:
        db.cart.insert_one({
            "user_id": session["user_id"],
            "product_id": str(product["_id"]),
            "name": product["name"],
            "price": product["price"],
            "quantity": 1
        })

    # ✅ Stay on same page instead of redirecting to cart
    return redirect(request.referrer or url_for("user.dashboard"))


@cart_bp.route("/cart")
def view_cart():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    db = get_db()
    items = list(db.cart.find({"user_id": session["user_id"]}))
    total = sum(item["price"] * item.get("quantity", 1) for item in items)

    return render_template(
        "user/cart.html",
        items=items,
        total=total
    )
@cart_bp.route("/cart/remove/<item_id>")
def remove_from_cart(item_id):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    db = get_db()
    db.cart.delete_one({
        "_id": ObjectId(item_id),
        "user_id": session["user_id"]
    })

    return redirect(url_for("cart.view_cart"))
@cart_bp.route("/cart/increase/<item_id>")
def increase_quantity(item_id):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    db = get_db()
    db.cart.update_one(
        {"_id": ObjectId(item_id), "user_id": session["user_id"]},
        {"$inc": {"quantity": 1}}
    )
    return redirect(url_for("cart.view_cart"))


@cart_bp.route("/cart/decrease/<item_id>")
def decrease_quantity(item_id):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    db = get_db()
    item = db.cart.find_one({"_id": ObjectId(item_id)})

    if not item:
        return redirect(url_for("cart.view_cart"))

    if item.get("quantity", 1) > 1:
        db.cart.update_one(
            {"_id": ObjectId(item_id)},
            {"$inc": {"quantity": -1}}
        )
    else:
        db.cart.delete_one({"_id": ObjectId(item_id)})

    return redirect(url_for("cart.view_cart"))
