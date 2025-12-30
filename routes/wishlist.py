from flask import Blueprint, redirect, url_for, session, render_template
from database.mongo import get_db
from bson import ObjectId
from datetime import datetime

wishlist_bp = Blueprint("wishlist", __name__)

# ==========================
# ADD TO WISHLIST (ALL PRODUCTS)
# ==========================
@wishlist_bp.route("/wishlist/add/<product_id>")
def add_to_wishlist(product_id):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    db = get_db()
    product = db.products.find_one({"_id": ObjectId(product_id)})

    if not product:
        return redirect(url_for("user.dashboard"))

    exists = db.wishlist.find_one({
        "user_id": session["user_id"],
        "product_id": str(product["_id"])
    })

    if not exists:
        db.wishlist.insert_one({
            "user_id": session["user_id"],
            "product_id": str(product["_id"]),
            "name": product["name"],
            "price": product["price"],
            "image": product.get("image", ""),
            "added_at": datetime.now()
        })

    return redirect(url_for("user.dashboard"))


# ==========================
# VIEW WISHLIST
# ==========================
@wishlist_bp.route("/wishlist")
def view_wishlist():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    db = get_db()
    items = list(db.wishlist.find({"user_id": session["user_id"]}))
    return render_template("user/wishlist.html", items=items)


# ==========================
# REMOVE FROM WISHLIST
# ==========================
@wishlist_bp.route("/wishlist/remove/<item_id>")
def remove_from_wishlist(item_id):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    db = get_db()
    db.wishlist.delete_one({"_id": ObjectId(item_id)})
    return redirect(url_for("wishlist.view_wishlist"))
