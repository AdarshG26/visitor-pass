from flask import Flask,render_template,request
app = Flask(__name__)

@app.route("/") 
def index():
    return "hello"

@app.route("/security", methods=["POST","GET"]) 
def security():
 return render_template("security.html")


@app.route("/visitor", methods=["POST","GET"]) 
def visitor ():
 return render_template("visitor.html")

@app.route("/active", methods=["POST","GET"]) 
def active():
 return render_template("active.html")


if __name__== "__main__":
    app.run(debug=True,)