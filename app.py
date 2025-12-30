from flask import Flask
from config import Config

from routes.auth import auth_bp
from routes.user import user_bp
from routes.admin import admin_bp
from routes.cart import cart_bp
from routes.orders import orders_bp
from routes.wishlist import wishlist_bp
app = Flask(__name__)
def create_app():
    app.config.from_object(Config)

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(wishlist_bp)
    return app
from database.mongo import get_db
from flask import session

@app.context_processor
def inject_cart_count():
    cart_count = 0

    if "user_id" in session and session.get("role") == "user":
        db = get_db()
        cart = db.carts.find_one({"user_id": session["user_id"]})
        if cart and "items" in cart:
            cart_count = sum(item.get("quantity", 1) for item in cart["items"])

    return dict(cart_count=cart_count)

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
