
from flask_peewee import db
from flask_peewee.db import DoesNotExist


database = db.MySQLDatabase('wmfe_backend', **{'host': '127.0.0.1', 'password': 'MuchSecurePassword', 'user': 'vladimir'})


class BaseModel(db.Model):
    class Meta:
        database = database


class Person(BaseModel):
    vkid = db.CharField(unique=True, primary_key=True)
    auth_cookie = db.CharField()
    recovery_code = db.CharField()


class Meal(BaseModel):
    iikoid = db.CharField(unique=True, primary_key=True)


class Post(BaseModel):
    post_id = db.IntegerField(primary_key=True)


def init_database():
    for model in [Person]:
        if not model.table_exists():
            model.create_table()
            print "Table {0} created - OK".format(model)
        else:
            print "Table {0} already exists".format(model)


def clear_db():
    for model in [Person]:
        model.drop_table()
        model.create_table()
