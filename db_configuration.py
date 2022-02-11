# !/usr/bin/env python3

from flask import Flask, current_app, g, render_template, url_for, flash, redirect, request, abort
import psycopg2
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

UPLOAD_FOLDER = '/uploads/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)

se = URLSafeTimedSerializer('This is secreate!')

# Flask mail configuration

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'dummytesting32@gmail.com'
app.config['MAIL_PASSWORD'] = 'Perpetua123'
# app.config['MAIL_USERNAME'] = 'kiruthika.m@perpetua.co.in'
# app.config['MAIL_PASSWORD'] = 'kirthiorange@5'
# app.config['MAIL_USERNAME'] = 'sethupathi.t@perpetua.co.in'
# app.config['MAIL_PASSWORD'] = 'perpetua123'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['SECRET_KEY'] = "random string"


# instantiate the Mail class
mail = Mail(app)

filename = "db.txt"
fp = open(filename)
for i, line in enumerate(fp):
    if i == 0:
        site_admin_db = line
        
    if i == 1:
        dms_db = line

site_admin_db = site_admin_db.strip()
dms_db = dms_db.strip()


app.config['SESSION_COOKIE_NAME'] = "websitesession"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:perpetua@localhost/azure_scopiq_web'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/azure_scopiq_web')
engine2 = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+dms_db)
engine1 = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+site_admin_db)
Base = declarative_base()
Session = sessionmaker(bind=engine)
Session1 = sessionmaker(bind=engine1)
Session2 = sessionmaker(bind=engine2)
sessions = Session()
sessions1 = Session1()
sessions2 = Session2()

db = SQLAlchemy(app)



def connection():

    connection = psycopg2.connect(user="postgres",
                                  password="perpetua",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="scopiq_web")
    return connection


def connection1():

    connection1 = psycopg2.connect(user="postgres",
                                   password="perpetua",
                                   host="127.0.0.1",
                                   port="5432",
                                   database=site_admin_db)
    return connection1


def connection2():

    connection2 = psycopg2.connect(user="postgres",
                                   password="perpetua",
                                   host="127.0.0.1",
                                   port="5432",
                                   database=dms_db)
    return connection2

# from scopiq_wegram_service import program
# app.register_blueprint(program)

@app.before_request
def get_db_one():
    if 'db0' not in g:
        g.db0 = connection()
    return g.db0

@app.after_request
def close_db(e=None):
    db0 = g.pop('db0', None)
    if db0 is not None:
        db0.close()


@app.before_request
def get_db_two():
    if 'db1' not in g:
        g.db1 = connection1()
    return g.db1


@app.after_request
def close_db_two(e=None):
    db1 = g.pop('db1', None)
    if db1 is not None:
        db1.close()


@app.before_request
def get_db_three():
    if 'db2' not in g:
        g.db2 = connection2()
    return g.db2


@app.after_request
def close_db_three(e=None):
    db2 = g.pop('db2', None)
    if db2 is not None:
        db2.close()

# host = "127.0.0.1"
# host = "10.0.0.20"
# host = "192.168.19.96"
host = "0.0.0.0"
port = "5002"
