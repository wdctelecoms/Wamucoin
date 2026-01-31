from flask import Flask, render_template, request, redirect, session, url_for
from functools import wraps
import sqlite3
import hashlib

app = Flask(__name__)
app.secret_key = "finshield_secret_key"
DB = "database.db"

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        account_type TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT,
        risk TEXT
    )
    """)

    conn.commit()
    conn.close()

def detect_scam(text):
    keywords = [
        "urgent", "double your money", "crypto giveaway",
        "guaranteed profit", "send money now"
    ]
    for word in keywords:
        if word in text.lower():
            return "HIGH RISK ⚠️"
    return "LOW RISK ✅"

@app.route("/")
def index():
    if "user" in session:
        return redirect("/dashboard")
    return redirect("/intro")

@app.route("/intro")
def intro():
    return render_template("intro.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = hash_password(request.form["password"])
        account_type = request.form["account_type"]

        try:
            conn = sqlite3.connect(DB)
            c = conn.cursor()
            c.execute(
                "INSERT INTO users (username, password, account_type) VALUES (?, ?, ?)",
                (username, password, account_type)
            )
            conn.commit()
            conn.close()
            return redirect("/login")
        except:
            return "Username already exists"

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = hash_password(request.form["password"])

        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )
        user = c.fetchone()
        conn.close()

        if user:
            session["user"] = username
            session["type"] = user[3]
            return redirect("/dashboard")
        else:
            return "Invalid login"

    return render_template("login.html")

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user=session["user"], type=session["type"])

@app.route("/check", methods=["GET", "POST"])
@login_required
def check():
    result = None
    if request.method == "POST":
        result = detect_scam(request.form["text"])

    return render_template("check.html", result=result)

@app.route("/report", methods=["GET", "POST"])
@login_required
def report():
    if request.method == "POST":
        content = request.form["content"]
        risk = detect_scam(content)
        
        try:
            conn = sqlite3.connect(DB)
            c = conn.cursor()
            c.execute(
                "INSERT INTO reports (content, risk) VALUES (?, ?)",
                (content, risk)
            )
            conn.commit()
            conn.close()
            return render_template("report.html", message="Report submitted successfully!", success=True)
        except Exception as e:
            return render_template("report.html", message=f"Error submitting report: {str(e)}", success=False)
    
    return render_template("report.html")

@app.route("/alerts")
@login_required
def alerts():
    try:
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("SELECT * FROM reports ORDER BY id DESC LIMIT 50")
        reports = c.fetchall()
        conn.close()
        return render_template("alerts.html", alerts=reports)
    except:
        return render_template("alerts.html", alerts=[])

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
