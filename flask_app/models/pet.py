from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user

class Pet:
    db="loggers"
    def __init__(self,data):
        self.id=data["id"]
        self.name=data["name"]
        self.species=data["species"]
        self.created_at=data["created_at"]
        self.updated_at=data["updated_at"]
        self.user=None
    
    @classmethod
    def save(cls,data):
        query="insert into pet(name,species,user_id) values(%(name)s,%(species)s,%(user_id)s);"
        return connectToMySQL(cls.db).query_db(query,data)
    @classmethod
    def get_one_pet_with_user(cls,data):
        query="select * from pet join user on pet.user_id=user.id where pet.id=%(id)s;"
        results= connectToMySQL(cls.db).query_db(query,data)
        pet=cls(results[0])
        user_dic={
            "id":results[0]["user.id"],
            "username":results[0]["username"],
            "password":results[0]["password"],
            "email":results[0]["email"],
            "created_at":results[0]["user.created_at"],
            "updated_at":results[0]["updated_at"]

        }
        pet.user=user.User(user_dic)
        return pet
    @classmethod
    def delete(cls,data):
        query="delete from pet where id=%(id)s;"

        return connectToMySQL(cls.db).query_db(query,data)
    @classmethod
    def update(cls,data):
        query="update pet set name= %(name)s,species=%(species)s where id=%(id)s;"

        return connectToMySQL(cls.db).query_db(query,data)
