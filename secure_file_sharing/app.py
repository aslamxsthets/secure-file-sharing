import os
from functools import wraps
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_file, session, abort
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from io import BytesIO

from crypto_utils import encrypt_file, decrypt_file
from mongo_db import users_collection, logs_collection

print("RUNNING APP FROM:", os.path.abspath(__file__))
print("CURRENT WORKING DIR:", os.getcwd())

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = os.urandom(24)

BASE_UPLOAD = "uploads/encrypted"
os.makedirs(BASE_UPLOAD, exist_ok=True)

# ---------------- AUTH DECORATORS ----------------
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return func(*args, **kwargs)
    return wrapper

def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get("role") != "admin":
            abort(403)
        return func(*args, **kwargs)
    return wrapper

def user_folder():
    folder = os.path.join(BASE_UPLOAD, f"user_{session['user_id']}")
    os.makedirs(folder, exist_ok=True)
    return folder

# ---------------- AUTH ROUTES ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = generate_password_hash(request.form["password"])

        if users_collection.find_one({"username": username}):
            return "User already exists", 409

        users_collection.insert_one({
            "username": username,
            "password": password,
            "role": "user"
        })
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = users_collection.find_one({"username": request.form["username"].strip()})
        if user and check_password_hash(user["password"], request.form["password"]):
            session["user_id"] = str(user["_id"])
            session["username"] = user["username"]
            session["role"] = user.get("role", "user")
            return redirect(url_for("dashboard"))
        return "Invalid credentials", 401

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ---------------- DASHBOARD ----------------
@app.route("/")
@login_required
def dashboard():
    files = os.listdir(user_folder())
    return render_template("index.html", files=files, user=session["username"])

# ---------------- FILE OPS ----------------
@app.route("/upload", methods=["POST"])
@login_required
def upload():
    file = request.files.get("file")
    if not file:
        return redirect(url_for("dashboard"))

    filename = secure_filename(file.filename)
    encrypted = encrypt_file(file.read())

    with open(os.path.join(user_folder(), filename + ".enc"), "wb") as f:
        f.write(encrypted)

    logs_collection.insert_one({
        "user": session["username"],
        "action": "UPLOAD",
        "filename": filename,
        "ip": request.remote_addr,
        "timestamp": datetime.utcnow()
    })
    return redirect(url_for("dashboard"))

@app.route("/download/<filename>")
@login_required
def download(filename):
    path = os.path.join(user_folder(), secure_filename(filename))
    if not os.path.exists(path):
        abort(403)

    with open(path, "rb") as f:
        decrypted = decrypt_file(f.read())

    logs_collection.insert_one({
        "user": session["username"],
        "action": "DOWNLOAD",
        "filename": filename,
        "ip": request.remote_addr,
        "timestamp": datetime.utcnow()
    })

    return send_file(BytesIO(decrypted),
                     download_name=filename.replace(".enc", ""),
                     as_attachment=True)

# ---------------- ADMIN ----------------
@app.route("/admin/logs")
@login_required
@admin_required
def admin_logs():
    logs = logs_collection.find().sort("timestamp", -1)
    return render_template("admin_logs.html", logs=logs)

@app.route("/admin/dashboard")
@login_required
@admin_required
def admin_dashboard():
    uploads = logs_collection.count_documents({"action": "UPLOAD"})
    downloads = logs_collection.count_documents({"action": "DOWNLOAD"})
    return render_template("admin_dashboard.html", uploads=uploads, downloads=downloads)

# ---------------- RUN ----------------
if __name__ == "__main__":
    print(">>> Flask starting (HTTP mode) <<<")
    app.run(host="127.0.0.1", port=5000, debug=True, use_reloader=False)
