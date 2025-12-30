from flask import Blueprint, render_template, request, redirect, url_for, session
from database.mongo import get_db
import bcrypt

auth_bp = Blueprint("auth", __name__)

# ---------------- LOGIN ----------------
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        db = get_db()
        user = db.users.find_one({"email": email})

        if not user:
            return render_template(
                "auth/login.html",
                error="Invalid email or password"
            )

        hashed_password = user["password"]
        if isinstance(hashed_password, str):
            hashed_password = hashed_password.encode("utf-8")

        if not bcrypt.checkpw(password.encode("utf-8"), hashed_password):
            return render_template(
                "auth/login.html",
                error="Invalid email or password"
            )

        session["user_id"] = str(user["_id"])
        session["role"] = user.get("role", "user")

        if session["role"] == "admin":
            return redirect(url_for("admin.dashboard"))
        return redirect(url_for("user.dashboard"))

    return render_template("auth/login.html")


# ---------------- REGISTER ----------------
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        db = get_db()

        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        )

        db.users.insert_one({
            "name": name,
            "email": email,
            "password": hashed_password,
            "role": "user"
        })

        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


# ---------------- FORGOT PASSWORD ----------------
@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email")
        db = get_db()

        user = db.users.find_one({"email": email})
        if not user:
            return render_template(
                "auth/forgot_password.html",
                error="Email not registered"
            )

        # Store email temporarily
        session["reset_email"] = email
        return redirect(url_for("auth.reset_password"))

    return render_template("auth/forgot_password.html")


# ---------------- RESET PASSWORD ----------------
@auth_bp.route("/reset-password", methods=["GET", "POST"])
def reset_password():
    if "reset_email" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        password = request.form.get("password")

        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        )

        db = get_db()
        db.users.update_one(
            {"email": session["reset_email"]},
            {"$set": {"password": hashed_password}}
        )

        session.pop("reset_email")
        return redirect(url_for("auth.login"))

    return render_template("auth/reset_password.html")


# ---------------- LOGOUT ----------------
@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
