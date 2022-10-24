from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.pet import Pet
from flask_app.models.user import User

@app.route("/create_pet")
def create_pet():
    if "user_id" not in session:
        return redirect("/")
    data={
        "id":session["user_id"]
    }
    user_data= User.get_one(data)
    return render_template("create_pet.html",user_data=user_data)
@app.route("/pet_form", methods=["post"])
def pet_form():
    print(request.form)
    Pet.save(request.form)
    return redirect("/home")
@app.route("/show_pets/<int:id>")
def show_pets(id):
    if "user_id" not in session:
        return redirect("/")
    data={
        "id":id
    }
    user_data=User.get_user_with_pet(data)
    return render_template("show_pets.html",user_data=user_data)
@app.route("/delete/<int:id>")
def delete(id):
    data={
        "id":id
    }
    Pet.delete(data)
    return redirect("/home")
@app.route("/update/<int:id>")
def update(id):
    data={
        "id":id
    }
    pet_db=Pet.get_one_pet_with_user(data)
    return render_template("update.html",pet_db=pet_db)
@app.route("/update_form",methods=["post"])
def update_form():
    print(request.form)
    Pet.update(request.form)
    return redirect("/home")
