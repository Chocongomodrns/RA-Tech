import random 

import sys 

from faker import Faker 

from flask import Flask, redirect, render_template, request, url_for

from flask_sqlalchemy import SQLAlchemy

 

app = Flask(__name__) 

app.config["DEBUG"] = True 

app.app_context().push() 

  

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format( 

    username="Chocongomodrns", 

    password="Nubefrankland14",  #psswd sin @ 

    hostname="Chocongomodrns.mysql.pythonanywhere-services.com", 

    databasename="Chocongomodrns$user", 

) 

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI 

app.config["SQLALCHEMY_POOL_RECYCLE"] = 299 

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False 

  

db = SQLAlchemy(app) 

  

class User(db.Model): 

    id = db.Column(db.Integer, primary_key=True) 

    name = db.Column(db.String(64), index=True) 

    age = db.Column(db.Integer, index=True) 

    address = db.Column(db.String(256)) 

    phone = db.Column(db.String(20)) 

    email = db.Column(db.String(120), index=True) 

  

with app.app_context(): 

    db.create_all() 

  

  

def create_fake_users(n): 

    """Crea usuarios ficticios.""" 

    faker = Faker() 

    for i in range(n): 

        user = User(name=faker.name(), 

                    age=random.randint(20, 80), 

                    address=faker.address().replace('\n', ', '), 

                    phone=faker.phone_number(), 

                    email=faker.email()) 

        db.session.add(user) 

    db.session.commit() 

    print(f'Se agregaron {n} fake users a la base de datos.') 

  

  

if __name__ == '__main__': 

    if len(sys.argv) <= 1: 

        print('escribe como argumento el número de datos ficticios que deseas crear.') 

        sys.exit(1) 

    with app.app_context(): 

        create_fake_users(int(sys.argv[1]))