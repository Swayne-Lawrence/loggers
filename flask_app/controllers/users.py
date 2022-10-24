
from flask_app import app
from flask import redirect,flash,render_template,request,session
from flask_bcrypt import Bcrypt
from flask_app.models.user import User

bcrypt= Bcrypt(app)

@app.route("/")
def register():
    if "user_id" in session:
        return redirect("/home")
    return render_template("index.html")
@app.route("/create_user", methods=["post"])
def create_user():
    if User.validate(request.form)==False:
        return redirect("/")
    pw_hash=bcrypt.generate_password_hash(request.form["password"])
    data={
        "username":request.form["username"],
        "password":pw_hash,
        "email":request.form["email"]
    }
    print(data)
    User.save(data)
    return redirect("/home")
@app.route("/log_form", methods=["post"])
def log_form():
    user_db= User.check_username(request.form)
    if(not user_db) or (not bcrypt.check_password_hash(user_db.password,request.form["password"])):
        flash("invalid email/password")
        return redirect("/")
    session["user_id"]=user_db.id
    print(session["user_id"])
    return redirect("/home")
@app.route("/home")
def home():
    if "user_id" not in session:
        return redirect("/")
    data=User.get_all()
    return render_template("home.html",data=data)
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
