from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
import os

app = Flask(__name__)
client = MongoClient(os.getenv('MONGO_URI'))
db = client["visitor_pass"]

@app.route("/adhaar_details", methods=["GET", "POST"])
def adhaar_details():
    if request.method == "POST":
        adhaar_number = request.form.get("adhaar_number")
        full_name = request.form.get("full_name")
        dob = request.form.get("dob")
        gender = request.form.get("gender")
        address = request.form.get("address")


        db.adhaar_card_details.insert_one({
            "adhaar_number": adhaar_number,
            "full_name":full_name, 
            "dob":dob, 
            "gender": gender,
            "address": address
        })
    return render_template('adhaar_form.html')  


@app.route("/pan_details", methods=["GET", "POST"])
def pan_details():
    if request.method == "POST":
        pan_number = request.form.get("pan_number")
        full_name = request.form.get("full_name")
        father_name = request.form.get("father_name")
        dob = request.form.get("dob")
        issued_by = request.form.get("issued_by")


        db.pan_card_details.insert_one({
            "pan_number": pan_number,
            "full_name": full_name,
            "father_name": father_name,
            "dob": dob,
            "issued_by": issued_by
        })
    return render_template('pan_form.html') 

if __name__ == "__main__":
    app.run(debug=True)
