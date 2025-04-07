from flask import Flask,render_template,request
app = Flask(__name__)

# @app.route("/") 
# def index():
#     return "hello"

@app.route("/security", methods=["POST","GET"]) 
def security():
 return render_template("security.html")


@app.route("/Overview", methods=["POST","GET"]) 
def Overview ():
 return render_template("Visitor_overview.html")

@app.route("/All", methods=["POST","GET"]) 
def All():
 return render_template("All_visitor.html")

@app.route("/Visitor", methods=["POST","GET"]) 
def Visitor():
 return render_template("visitor.html")
 
@app.route("/Rejected", methods=["POST","GET"]) 
def Rejecte():
 return render_template("rejected.html")


if __name__== "__main__":
    app.run(debug=True,)