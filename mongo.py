from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
import os

app = Flask(__name__)
client = MongoClient(os.getenv('mongodb://localhost:27017/'))
db=client["index_data"]  # Database Name
collection = db["index"]  # Collection Name
  
  # connect a form of PAN and Adhard card information store
@app.route("/form", methods=["GET", "POST"])
def hello():
    if request.method == "POST":
        database = {
            "username": request.form["username"],
            "father_name": request.form["father_name"],
            "dob": request.form["dob"],
            "gender": request.form["gender"],
            "uid": request.form["uid"],
            "email": request.form["email"],
            "number": request.form["number"],
            "approved_by": request.form["approved_by"]
        }
        
        # Insert into MongoDB
        collection.insert_one(database)
        
        return "Registration Successful!"
    
    return render_template('form.html')  # Renders the HTML form

if __name__ == "__main__":
    app.run(debug=True)
