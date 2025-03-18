from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
from bson import ObjectId       
import os

app = Flask(__name__)
app.secret_key = "secret123"

login_manager = LoginManager(app)
login_manager.login_view = "login"
bcrypt = Bcrypt(app)

client = MongoClient(os.getenv('MONGO_URI'))
db = client["visitor_pass"]


# User Model for login
class User(UserMixin):
    def __init__(self, user_id, username, email, password):
        self.id = user_id
        self.username = username
        self.email = email
        self.password = password


@login_manager.user_loader
def load_user(user_id):
    try:
        user_data = db.user.find_one({"_id": ObjectId(user_id)})
        if user_data:
            return User(str(user_data["_id"]), user_data["user_name"], user_data["email"], user_data["password"])
    except:
        return None
    return None


@app.route("/")
def test():
    return redirect(url_for('login'))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user_name = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        cpassword = request.form.get("cpassword")

        existing_user = db.user.find_one({"email": email})
        if existing_user:
            flash("User already registered!", "danger")
            return redirect(url_for("register"))

        if password != cpassword:
            flash("Password did not match", "danger")
            return redirect(url_for("register"))
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        db.user.insert_one({
            "user_name":user_name, 
            "email":email, 
            "password": hashed_password
        })

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("login"))
    
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user_data = db.user.find_one({"email": email})
        if user_data and bcrypt.check_password_hash(user_data["password"], password):
            user = User(str(user_data["_id"]), user_data["user_name"], user_data["email"], user_data["password"])
            login_user(user)

            flash("Login successful!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid email or password", "danger")
            
    return render_template("login.html")


@app.route("/dashboard")
@login_required
def dashboard():   
    return render_template("dashboard.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logout!", "info")
    return redirect(url_for("login"))



if __name__ == "__main__":
    app.run(debug=True)
