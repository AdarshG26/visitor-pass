from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
from bson import ObjectId       
import os
import pytesseract
from PIL import Image
import cv2
import re


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

            role = user_data.get("role","")

            flash("Login successful!", "success")

            if role == "admin":
                return redirect(url_for('security_dashboard'))
            elif role == "super admin":
                return redirect(url_for('admin_dashboard'))
        else:
            flash("Invalid email or password", "danger")
            
    return render_template("login.html")


@app.route("/security_dashboard")
@login_required
def security_dashboard():   
    return render_template("security_dashboard.html", username=current_user.username)


@app.route("/admin_dashoard")
@login_required
def admin_dashboard():
    return render_template("admin_dashboard.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logout!", "info")
    return redirect(url_for("login"))



#------------------------------------- code for extracting details from cards and saving to database ----------------------------------------


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def convert_image_to_text(image_path):
    # Read the image using OpenCV
    img = cv2.imread(image_path)

    # Check if the image is loaded correctly
    if img is None:
        raise ValueError(f"Error: Image not found at path {image_path}")
    
    # Convert the image to grayscale (optional, but often helps OCR accuracy)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Use pytesseract to extract text from the imagesaxs
    extracted_text = pytesseract.image_to_string(gray_img)
    return extracted_text


def parse_aadhaar_details(text):
    aadhaar_number = re.search(r"\d{4} \d{4} \d{4}", text)
    name_match = re.search(r"(?i)(?:Name|नाम):?\s*(.*)", text)
    dob_match = re.search(r"(?i)(?:DOB|Date\s*of\s*Birth|जन्म\s*तिथि)[^\d]{0,10}(\d{2}/\d{2}/\d{4})", text)
    gender_match = re.search(r"(?i)(?:Male|Female|Transgender|पुरुष|महिला)", text)

    return {
        "aadhaar_number": aadhaar_number.group(0) if aadhaar_number else None,
        "full_name": name_match.group(1) if name_match else None,
        "dob": dob_match.group(1) if dob_match else None,
        "gender": gender_match.group(0) if gender_match else None
    }


def parse_pan_details(text):
    pan_number = re.search(r"[A-Z]{5}[0-9]{4}[A-Z]", text)
    name_match = re.search(r"(?i)(?:Name|नाम):?\s*(.*)", text)
    father_match = re.search(r"(?i)(?:Father's Name|पिता का नाम):?\s*(.*)", text)
    dob_match = re.search(r"(?i)(?:DOB|Date\s*of\s*Birth|जन्म\s*तिथि|जन्म\s*की\s*तारीख)[^\d]{0,10}(\d{2}/\d{2}/\d{4})", text)


    return {
        "pan_number": pan_number.group(0) if pan_number else None,
        "full_name": name_match.group(1) if name_match else None,
        "father_name": father_match.group(1) if father_match else None,
        "dob": dob_match.group(1) if dob_match else None
    }


@app.route("/pan_details", methods=["GET", "POST"])
def pan_details():
    pan_img_path = "static/css/imgs/pan.jpg"
    pan_data = {}

    if os.path.exists(pan_img_path):
        pan_text = convert_image_to_text(pan_img_path)
        pan_data = parse_pan_details(pan_text)
    
    #----------------- saving extracted data into db ----------------------
    if request.method == "POST":
        pan_number = request.form.get("pan_number")
        full_name = request.form.get("full_name")
        father_name = request.form.get("father_name")
        dob = request.form.get("dob")

        db.pan_card_details.insert_one({
            "pan_number": pan_number,
            "full_name": full_name,
            "father_name": father_name,
            "dob": dob,
        })
        return redirect(url_for("aadhaar_details"))
    
    return render_template("pan_details.html", pan=pan_data)


@app.route("/aadhaar_details", methods=["GET", "POST"])
def aadhaar_details():
    aadhaar_img_path = "static/css/imgs/adharcard.jpg"
    aadhaar_data = {}

    if os.path.exists(aadhaar_img_path):
        aadhaar_text = convert_image_to_text(aadhaar_img_path)
        aadhaar_data = parse_aadhaar_details(aadhaar_text)
        
    #----------------- saving extracted data into db ----------------------
    if request.method == "POST":
        aadhaar_number = request.form.get("aadhaar_number")
        full_name = request.form.get("full_name")
        dob = request.form.get("dob")
        gender = request.form.get("gender")

        db.aadhaar_card_details.insert_one({
            "aadhaar_number": aadhaar_number,
            "full_name":full_name, 
            "dob":dob, 
            "gender": gender
        })
        return redirect(url_for("aadhaar_details"))

    return render_template("aadhaar_details.html", aadhaar=aadhaar_data)


if __name__ == "__main__":
    app.run(debug=True)
