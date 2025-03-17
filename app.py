from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)
app.secret_key = "secret123"
bcrypt = Bcrypt(app)

client = MongoClient(os.getenv('MONGO_URI'))
# print(f"hello this is mongo uri: {client}")
db = client["visitor_pass"]


@app.route("/")
def login():
    return render_template("login.html")

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

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(debug=True)
