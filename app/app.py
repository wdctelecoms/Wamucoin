from flask import Flask, render_template, request, redirect, session, url_for, jsonify
from functools import wraps
import sqlite3
import hashlib
import json
from datetime import datetime
import smtplib
import os
import ssl
from email.message import EmailMessage
from dotenv import load_dotenv
import threading
import socket

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = "finshield_secret_key"
# Database path: prefer explicit `DATABASE_PATH` env var, else use a writable
# runtime location. Vercel's filesystem is ephemeral but `/tmp` is writable
# during runtime which prevents "unable to open database file" errors.
DB = os.environ.get("DATABASE_PATH", os.path.join("/tmp", "database.db"))

# Ensure DB directory exists (no-op for /tmp but safe for custom paths)
try:
    db_dir = os.path.dirname(DB)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
except Exception:
    # If directory creation fails, fall back to in-memory DB to avoid crashes
    DB = ":memory:"

# Email / SMTP configuration
SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))
EMAIL_SENDER = os.environ.get("EMAIL_SENDER", "finshieldAI@gmail.com")
SMTP_USERNAME = os.environ.get("SMTP_USERNAME", EMAIL_SENDER)
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "")

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
        email TEXT UNIQUE,
        password TEXT,
        account_type TEXT,
        email_verified INTEGER DEFAULT 0,
        verification_token TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT,
        risk TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        recipient TEXT,
        amount REAL,
        description TEXT,
        risk_score INTEGER,
        risk_level TEXT,
        scam_type TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        warnings TEXT,
        FOREIGN KEY(username) REFERENCES users(username)
    )
    """)

    conn.commit()
    conn.close()

# Advanced AI Fraud Detection System
class FraudDetectionAI:
    def __init__(self):
        self.high_risk_keywords = {
            "urgent": 20,
            "double your money": 30,
            "crypto giveaway": 35,
            "guaranteed profit": 30,
            "send money now": 25,
            "act now": 15,
            "limited time": 15,
            "claim reward": 20,
            "verify account": 20,
            "update payment": 25,
            "confirm identity": 20,
            "wire transfer": 15,
            "gift card": 20,
            "bitcoin": 10,
            "ethereum": 10,
            "get rich": 25,
            "easy money": 25,
            "no risk": 20,
            "special offer": 10,
            "exclusive deal": 10,
            "free money": 30,
            "click here": 10,
            "confirm details": 15
        }
        
        self.investment_scam_indicators = {
            "ponzi": 40,
            "pyramid": 40,
            "mlm": 35,
            "multi-level": 35,
            "guaranteed returns": 35,
            "high yield": 25,
            "investment opportunity": 15,
            "get started today": 20,
            "passive income": 20
        }
        
        self.crypto_scam_indicators = {
            "blockchain": 15,
            "defi": 20,
            "presale": 25,
            "ico": 25,
            "seed phrase": 40,
            "private key": 40,
            "wallet address": 15,
            "nft": 15,
            "token": 15,
            "lambo": 25,
            "moon": 20
        }
        
        self.romance_scam_indicators = {
            "love": 10,
            "dear": 5,
            "sweetheart": 15,
            "business emergency": 30,
            "help me": 15,
            "stranded": 25,
            "hospital": 20
        }
        
        self.phishing_indicators = {
            "verify": 15,
            "confirm": 15,
            "update": 15,
            "re-enter": 20,
            "click link": 20,
            "download attachment": 25,
            "re-activate": 20,
            "suspended": 25,
            "locked": 20
        }

    def analyze_transaction(self, recipient, amount, description):
        """Comprehensive transaction analysis with risk scoring"""
        risk_score = 0
        warnings = []
        scam_types = []
        
        # Amount analysis
        if amount > 10000:
            risk_score += 15
            warnings.append("Large transaction amount - verify recipient")
        
        if amount < 0:
            risk_score += 20
            warnings.append("Invalid amount detected")
        
        # Recipient analysis
        if recipient.lower() in ["unknown", "anonymous", "stranger", "unknown person"]:
            risk_score += 25
            warnings.append("Unknown or suspicious recipient")
        
        if len(recipient) < 3:
            risk_score += 15
            warnings.append("Recipient name too short")
        
        # Description analysis
        description_lower = description.lower()
        
        # Check for high-risk keywords
        for keyword, score in self.high_risk_keywords.items():
            if keyword in description_lower:
                risk_score += score
                warnings.append(f"⚠️ Alert word detected: '{keyword}'")
        
        # Check for investment scams
        for keyword, score in self.investment_scam_indicators.items():
            if keyword in description_lower:
                risk_score += score
                warnings.append(f"🚨 Investment scam indicator: '{keyword}'")
                if "ponzi" in keyword or "pyramid" in keyword:
                    scam_types.append("Ponzi/Pyramid Scheme")
                elif "mlm" in keyword or "multi-level" in keyword:
                    scam_types.append("MLM Scam")
                else:
                    scam_types.append("Fake Investment Scheme")
        
        # Check for crypto scams
        for keyword, score in self.crypto_scam_indicators.items():
            if keyword in description_lower:
                risk_score += score
                if "seed phrase" in keyword or "private key" in keyword:
                    warnings.append(f"🚨 CRITICAL: Someone asking for {keyword} - This is a scam!")
                    scam_types.append("Cryptocurrency Theft Scam")
                else:
                    warnings.append(f"⚠️ Crypto indicator: '{keyword}'")
                    if "presale" in keyword or "ico" in keyword:
                        scam_types.append("Fake ICO/Presale")
                    else:
                        scam_types.append("Crypto Scam")
        
        # Check for romance/urgency scams
        for keyword, score in self.romance_scam_indicators.items():
            if keyword in description_lower:
                risk_score += score
                if "stranded" in keyword or "hospital" in keyword or "emergency" in keyword:
                    scam_types.append("Romance/Urgency Scam")
                    warnings.append(f"🚨 Common scam tactic: '{keyword}'")
        
        # Check for phishing
        for keyword, score in self.phishing_indicators.items():
            if keyword in description_lower:
                risk_score += score
                if "download attachment" in keyword or "click link" in keyword:
                    scam_types.append("Phishing Attempt")
        
        # Multiple red flags increase risk exponentially
        if len(warnings) > 3:
            risk_score += 20
            warnings.append("Multiple red flags detected - HIGH SUSPICION")
        
        # Cap risk score at 100
        risk_score = min(risk_score, 100)
        
        # Determine risk level
        if risk_score >= 80:
            risk_level = "CRITICAL 🚨"
        elif risk_score >= 60:
            risk_level = "HIGH ⚠️"
        elif risk_score >= 40:
            risk_level = "MEDIUM ⚠️"
        elif risk_score >= 20:
            risk_level = "LOW 🟡"
        else:
            risk_level = "SAFE ✅"
        
        # Remove duplicates
        scam_types = list(set(scam_types))
        
        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "warnings": warnings,
            "scam_types": scam_types
        }
    
    def analyze_text(self, text):
        """Analyze text for scam indicators"""
        text_lower = text.lower()
        risk_score = 0
        detected_types = []
        
        # Check investment scams
        investment_keywords = ["invest", "returns", "profit", "yield", "interest"]
        if any(keyword in text_lower for keyword in investment_keywords):
            risk_score += 20
            detected_types.append("Investment Related")
        
        # Check high-risk phrases
        if any(keyword in text_lower for keyword in self.high_risk_keywords.keys()):
            risk_score += 30
        
        # Check crypto keywords
        if any(keyword in text_lower for keyword in self.crypto_scam_indicators.keys()):
            risk_score += 25
            detected_types.append("Crypto Related")
        
        risk_score = min(risk_score, 100)
        
        if risk_score >= 80:
            return "CRITICAL 🚨"
        elif risk_score >= 60:
            return "HIGH ⚠️"
        elif risk_score >= 40:
            return "MEDIUM ⚠️"
        elif risk_score >= 20:
            return "LOW 🟡"
        else:
            return "SAFE ✅"

fraud_ai = FraudDetectionAI()

def detect_scam(text):
    """Legacy function for backward compatibility"""
    return fraud_ai.analyze_text(text)


def send_verification_email_async(to_email, token, base_url):
    """Send verification email asynchronously (background thread)."""
    if not SMTP_PASSWORD:
        print("SMTP_PASSWORD not set; skipping sending verification email")
        return

    link = f"{base_url}/verify_email/{token}"
    subject = "Verify your FinShield account"
    body = (
        f"Hello,\n\nPlease verify your FinShield account by clicking the link below:\n{link}\n\n"
        "If you did not sign up, ignore this email.\n\n— FinShield Team"
    )

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = to_email
    msg.set_content(body)

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10) as server:
            server.starttls(context=context)
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
        print(f"Verification email sent to {to_email}")
    except socket.timeout:
        print(f"SMTP timeout sending to {to_email}")
    except Exception as e:
        print(f"Failed to send verification email to {to_email}: {e}")


def send_verification_email(to_email, token):
    """Send verification email (non-blocking). Returns immediately."""
    if not SMTP_PASSWORD:
        print("SMTP_PASSWORD not set; skipping email sending")
        return False

    try:
        base = request.url_root.rstrip('/')
    except RuntimeError:
        base = "http://localhost:5000"

    # Send email in background thread to avoid blocking request
    thread = threading.Thread(
        target=send_verification_email_async,
        args=(to_email, token, base)
    )
    thread.daemon = True
    thread.start()
    return True

@app.route("/analyze_transaction", methods=["GET", "POST"])
@login_required
def analyze_transaction():
    """Real-time transaction analysis with risk scoring"""
    result = None
    if request.method == "POST":
        recipient = request.form.get("recipient", "")
        amount = request.form.get("amount", 0)
        description = request.form.get("description", "")
        
        try:
            amount = float(amount)
        except:
            amount = 0
        
        # Analyze transaction
        analysis = fraud_ai.analyze_transaction(recipient, amount, description)
        
        # Save to database
        try:
            conn = sqlite3.connect(DB)
            c = conn.cursor()
            c.execute(
                """INSERT INTO transactions 
                   (username, recipient, amount, description, risk_score, risk_level, scam_type, warnings)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    session["user"],
                    recipient,
                    amount,
                    description,
                    analysis["risk_score"],
                    analysis["risk_level"],
                    ",".join(analysis["scam_types"]),
                    json.dumps(analysis["warnings"])
                )
            )
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error saving transaction: {e}")
        
        result = analysis
    
    return render_template("analyze_transaction.html", result=result)

@app.route("/api/check_transaction", methods=["POST"])
@login_required
def api_check_transaction():
    """API endpoint for real-time transaction checking"""
    data = request.json
    recipient = data.get("recipient", "")
    amount = data.get("amount", 0)
    description = data.get("description", "")
    
    try:
        amount = float(amount)
    except:
        amount = 0
    
    analysis = fraud_ai.analyze_transaction(recipient, amount, description)
    
    return jsonify(analysis)

@app.route("/transaction_history")
@login_required
def transaction_history():
    """View all analyzed transactions"""
    try:
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute(
            "SELECT * FROM transactions WHERE username=? ORDER BY timestamp DESC",
            (session["user"],)
        )
        transactions = c.fetchall()
        conn.close()
        
        # Convert warnings from JSON string
        transactions_list = []
        for t in transactions:
            warnings = json.loads(t[8]) if t[8] else []
            transactions_list.append({
                "id": t[0],
                "recipient": t[1],
                "amount": t[2],
                "description": t[3],
                "risk_score": t[4],
                "risk_level": t[5],
                "scam_type": t[6],
                "timestamp": t[7],
                "warnings": warnings
            })
        
        return render_template("transaction_history.html", transactions=transactions_list)
    except Exception as e:
        print(f"Error loading transactions: {e}")
        return render_template("transaction_history.html", transactions=[])

@app.route("/dashboard")
@login_required
def dashboard():
    """Enhanced dashboard with transaction stats"""
    try:
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        
        # Get transaction stats
        c.execute(
            "SELECT COUNT(*) FROM transactions WHERE username=?",
            (session["user"],)
        )
        total_transactions = c.fetchone()[0]
        
        c.execute(
            "SELECT COUNT(*) FROM transactions WHERE username=? AND risk_score >= 60",
            (session["user"],)
        )
        high_risk_count = c.fetchone()[0]
        
        c.execute(
            "SELECT COUNT(*) FROM transactions WHERE username=? AND risk_score < 40",
            (session["user"],)
        )
        safe_count = c.fetchone()[0]
        
        c.execute(
            "SELECT SUM(amount) FROM transactions WHERE username=? AND risk_score < 40",
            (session["user"],)
        )
        result = c.fetchone()[0]
        safe_amount = result if result else 0
        
        conn.close()
        
        stats = {
            "total_transactions": total_transactions,
            "high_risk_count": high_risk_count,
            "safe_count": safe_count,
            "safe_amount": safe_amount
        }
    except Exception as e:
        print(f"Error loading stats: {e}")
        stats = {
            "total_transactions": 0,
            "high_risk_count": 0,
            "safe_count": 0,
            "safe_amount": 0
        }
    
    return render_template("dashboard.html", user=session["user"], type=session["type"], stats=stats)

@app.route("/")
def index():
    if "user" in session:
        return redirect("/dashboard")
    return redirect("/intro")

@app.route("/intro")
def intro():
    return render_template("intro.html")

@app.route("/verify_email/<token>")
def verify_email(token):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE verification_token=?", (token,))
    user = c.fetchone()
    
    if user:
        c.execute("UPDATE users SET email_verified=1, verification_token=NULL WHERE id=?", (user[0],))
        conn.commit()
        conn.close()
        return render_template("email_verified.html", message="Email verified successfully! You can now login.")
    else:
        conn.close()
        return render_template("email_verified.html", message="Invalid verification link.", error=True)

@app.route("/resend_verification", methods=["GET", "POST"])
def resend_verification():
    if request.method == "POST":
        email = request.form["email"]
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email=? AND email_verified=0", (email,))
        user = c.fetchone()
        
        if user:
            # Fetch verification token and resend
            verification_token = user[6]
            conn.close()
            if verification_token:
                send_verification_email(email, verification_token)
                return render_template("verify_email.html", email=email, message=f"Verification email resent from {EMAIL_SENDER}. Check your inbox.")
            else:
                return render_template("resend_verification.html", error="No verification token found for this account.")
        else:
            conn.close()
            return render_template("resend_verification.html", error="Email not found or already verified.")
    
    return render_template("resend_verification.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = hash_password(request.form["password"])
        account_type = request.form["account_type"]
        
        # Generate verification token
        import secrets
        verification_token = secrets.token_urlsafe(32)

        try:
            conn = sqlite3.connect(DB)
            c = conn.cursor()
            c.execute(
                "INSERT INTO users (username, email, password, account_type, verification_token, email_verified) VALUES (?, ?, ?, ?, ?, ?)",
                (username, email, password, account_type, verification_token, 0)
            )
            conn.commit()
            conn.close()
            # Send verification email (non-blocking)
            send_verification_email(email, verification_token)
            return render_template("verify_email.html", email=email, message=f"Account created! Verification email sent from {EMAIL_SENDER}. Check your inbox.")
        except Exception as e:
            return render_template("register.html", error=f"Registration failed: {str(e)}")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login_input = request.form["login"]  # Can be username or email
        password = hash_password(request.form["password"])

        conn = sqlite3.connect(DB)
        c = conn.cursor()
        
        # Try login by username or email
        c.execute(
            "SELECT * FROM users WHERE (username=? OR email=?) AND password=?",
            (login_input, login_input, password)
        )
        user = c.fetchone()
        conn.close()

        if user:
            # Check if email is verified
            if user[5] == 0:  # email_verified column
                return render_template("login.html", error="Please verify your email before logging in. Check your email for the verification link.")
            
            session["user"] = user[1]  # username
            session["email"] = user[2]  # email
            session["type"] = user[4]  # account_type
            return redirect("/dashboard")
        else:
            return render_template("login.html", error="Invalid login credentials")

    return render_template("login.html")

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
