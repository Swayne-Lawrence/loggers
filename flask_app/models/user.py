from unittest import result
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.pet import Pet
from flask import flash
class User:
    db="loggers"
    def __init__(self,data):
        self.id=data["id"]
        self.username=data["username"]
        self.password=data["password"]
        self.email=data["email"]
        self.created_at=data["created_at"]
        self.updated_at=data["updated_at"]
        self.pets=[]
    @classmethod
    def save(cls,data):
        query="insert into user(username,password,email) values(%(username)s,%(password)s,%(email)s);"
        return  connectToMySQL(cls.db).query_db(query,data)
    @classmethod
    def get_all(cls):
        query="select * from user;"
        results=connectToMySQL(cls.db).query_db(query)
        users=[]
        for re in results:
            users.append(cls(re))
        return users
    @classmethod
    def get_one(cls,data):
        query="select * from user where id=%(id)s;"
        results=connectToMySQL(cls.db).query_db(query,data)
        return  cls(results[0])
    @classmethod
    def get_user_with_pet(cls,data):
        query="select * from user left join pet on user.id= pet.user_id where user.id=%(id)s;"
        results=connectToMySQL(cls.db).query_db(query,data)
        user=cls(results[0])
        for re in results:
            pet_dic={
                "id":re["pet.id"],
                "name":re["name"],
                "species":re["species"],
                "created_at":re["pet.created_at"],
                "updated_at":re["updated_at"]

            }
            user.pets.append(Pet(pet_dic))
        return user
    @classmethod
    def check_username(cls,data):
        query="select * from user where username=%(username)s;"
        results=connectToMySQL(cls.db).query_db(query,data)
        if len(results)<1:
            return False
        return cls(results[0])

    @staticmethod
    def validate(user):
        is_valid=True
        query="select * from user where email=%(email)s;"
        results=connectToMySQL(User.db).query_db(query,user)
        if len(user["username"])<2:
            flash("too short")
            is_valid=False
        if len(results)>0:
            flash("email already exist")
            is_valid=False
        if len(user["email"])<1:
            flash("email too short")
            is_valid=False
        if len(user["password"])<8:
            flash("password too short")
            is_valid=False
        if user["password"] != user["confirm"]:
            flash("password dont match")
            is_valid=False

        return is_valid