import os
import shutil
import psycopg2
import random
import math
import db_configuration
import base64
import hashlib
import urllib
import urllib.parse
import string
import ast
import subprocess
import re

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import cast
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from sqlalchemy import Table, Column, Integer, String, MetaData, DateTime, BigInteger, DECIMAL, and_
from sqlalchemy.ext.declarative import declarative_base
from flask import *
from flask_mail import *
from flask import Flask, request, render_template, flash, redirect, url_for, session, abort
from werkzeug import security
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from psycopg2 import connect, extensions, sql
from apscheduler.scheduler import Scheduler

from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Protocol.KDF import PBKDF2
from collections import Counter
from db_configuration import *
from db_configuration import sessions
from web_models import *
from models import *

metadata = MetaData()

from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta

BLOCK_SIZE = 16
bs = 16
pad = lambda s: bytes(s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE), 'utf-8')
unpad = lambda s: s[:-ord(s[len(s) - 1:])]
passcr = "thisisdemo"
# def _pad(s):
#       return s + (bs - len(s) % bs) * chr(bs - len(s) % bs)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
main_dir_path = APP_ROOT.rsplit('/', 1)[0]
text_value = open('settings.txt')
content = text_value.read()
source_code_folder_name = content.strip()
actual_src_path = main_dir_path+"/"+source_code_folder_name

# Financial Year Calculation
presentdate = datetime.date(datetime.now())
present_date = presentdate.strftime('%Y-%m-%d')
financial_year = presentdate.strftime('%y')
nxt_fin_year = int(financial_year) + 1

bill_code = "SQ"
purchase_code = "SQAG"

# Financial Year Calculation

def get_private_key(passcr):
    salt = b"this is a salt"
    kdf = PBKDF2(passcr, salt, 64, 1000)
    key = kdf[:32]
    return key


@app.template_filter('encryptdata')
def encryptdata(raw):
    private_key = get_private_key(passcr)
    raw = pad(str(raw))
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    encrypt_id = base64.b64encode(iv + cipher.encrypt(raw))
    return encrypt_id.decode()


def decrypt(enc, passcr):
    private_key = get_private_key(passcr)
    enc = base64.b64decode(enc)
    iv = enc[:16]
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc[16:]))


def rand_pass(size):

    # Declare a digits variable
    # which stores all digits
    digits = "0123456789"
    OTP = ""

    # length of password can be chaged
    # by changing value in range
    for i in range(size):
        OTP += digits[math.floor(random.random() * 10)]

    return OTP


def rand_pass_alpha(size):

    # Takes random choices from
    # ascii_letters and digits
    generate_pass = ''.join([random.choice(string.ascii_uppercase +
                                           string.ascii_lowercase +
                                           string.digits)
                             for n in range(size)])

    return generate_pass



# def register_userdetails(first_name, last_name, email, password_hash, referred_by_userid):
#     freetrial_email_count = sessions.query(RegUsers).filter(RegUsers.email == email,RegUsers.status == 2).count()
#     email_count = sessions.query(RegUsers).filter(RegUsers.email == email,RegUsers.status == 1).count()
#     print(freetrial_email_count,email_count)

#     if freetrial_email_count == 0:
#         if email_count == 0:
#             msg = Message('OTP', sender='username@gmail.com', recipients=[email])
#             otp = rand_pass(6)
#             msg.body = otp
#             msg.html = render_template('emails/otp_email.html', otp=otp)
#             mail.send(msg)
#             registerd_email_count = sessions.query(RegUsers).filter(RegUsers.email == email).filter(RegUsers.status == 0).count()
#             if registerd_email_count == 1:
#                 updated_user = sessions.query(RegUsers).filter(RegUsers.email == email,RegUsers.status == 0).update({RegUsers.first_name: first_name, RegUsers.last_name: last_name, RegUsers.password: password_hash, RegUsers.verification_code:otp })
#                 result = sessions.query(RegUsers.user_id).filter(RegUsers.email == email).first()[0]

#             else:
#                 if referred_by_userid is None:
#                     inserted_user = RegUsers(first_name=first_name, last_name=last_name, email=email, password=password_hash, verification_code=otp, status=0)
#                     sessions.add(inserted_user)
#                     sessions.flush()
#                     result = inserted_user.user_id


#                 else:
#                     inserted_user = RegUsers(first_name=first_name, last_name=last_name, email=email, password=password_hash, verification_code=otp, status=0, referred_by=referred_by_userid)
#                     sessions.add(inserted_user)
#                     sessions.flush()
#                     result = inserted_user.user_id

#             sessions.commit()
#         else:
#             result = "Email already exists"

#     else:
#         print("else")
#         if email_count == 0:
#             print("else")
#             msg = Message('OTP', sender='username@gmail.com', recipients=[email])
#             otp = rand_pass(6)
#             msg.body = otp
#             msg.html = render_template('emails/otp_email.html', otp=otp)
#             mail.send(msg)
#             registerd_email_count = sessions.query(RegUsers).filter(RegUsers.email == email).filter(RegUsers.status == 0).count()
#             if registerd_email_count == 1:
#                 updated_user = sessions.query(RegUsers).filter(RegUsers.email == email,RegUsers.status == 0).update({RegUsers.first_name: first_name, RegUsers.last_name: last_name, RegUsers.password: password_hash, RegUsers.verification_code:otp })
#                 result = sessions.query(RegUsers.user_id).filter(RegUsers.email == email).first()[0]

#             else:
#                 if referred_by_userid is None:
#                     inserted_user = RegUsers(first_name=first_name, last_name=last_name, email=email, password=password_hash, verification_code=otp, status=0)
#                     sessions.add(inserted_user)
#                     sessions.flush()
#                     result = inserted_user.user_id


#                 else:
#                     inserted_user = RegUsers(first_name=first_name, last_name=last_name, email=email, password=password_hash, verification_code=otp, status=0, referred_by=referred_by_userid)
#                     sessions.add(inserted_user)
#                     sessions.flush()
#                     result = inserted_user.user_id

#             sessions.commit()
#         else:
#             result = "Email already exists"

#     return result



def register_userdetails(first_name, last_name, email, password_hash, referred_by_userid):
    freetrial_email_count = sessions.query(RegUsers).filter(RegUsers.email == email,RegUsers.status == 2).count()
    email_count = sessions.query(RegUsers).filter(RegUsers.email == email,RegUsers.status == 1).count()
    print(freetrial_email_count,email_count)

    if freetrial_email_count >= 0:
        if email_count == 0:
            msg = Message('OTP', sender='username@gmail.com', recipients=[email])
            otp = rand_pass(6)
            msg.body = otp
            msg.html = render_template('emails/otp_email.html', otp=otp)
            mail.send(msg)
            registerd_email_count = sessions.query(RegUsers).filter(RegUsers.email == email).filter(RegUsers.status == 0).count()
            if registerd_email_count == 1:
                updated_user = sessions.query(RegUsers).filter(RegUsers.email == email,RegUsers.status == 0).update({RegUsers.first_name: first_name, RegUsers.last_name: last_name, RegUsers.password: password_hash, RegUsers.verification_code:otp })
                result = sessions.query(RegUsers.user_id).filter(RegUsers.email == email).first()[0]

            else:
                if referred_by_userid is None:
                    inserted_user = RegUsers(first_name=first_name, last_name=last_name, email=email, password=password_hash, verification_code=otp, status=0)
                    sessions.add(inserted_user)
                    sessions.flush()
                    result = inserted_user.user_id


                else:
                    inserted_user = RegUsers(first_name=first_name, last_name=last_name, email=email, password=password_hash, verification_code=otp, status=0, referred_by=referred_by_userid)
                    sessions.add(inserted_user)
                    sessions.flush()
                    result = inserted_user.user_id

            sessions.commit()
        else:
            result = "Email already exists"

    return result


def insert_company(email, site_name, address, company_name, country, state, city, userid, company_code):
    user_email = session['email']
    comp_details_count = sessions.query(CompanyDetails).filter_by(user_id=userid).count()
    if comp_details_count == 0:
        inserted_company = CompanyDetails(company_name=company_name, address=address, email=email, site_name=site_name, country_id=country, state_id=state, city_id=city, user_id=userid, company_code=company_code)
        sessions.add(inserted_company)
        sessions.flush()
        company_id = inserted_company.company_id

        referral_users_count = sessions.query(RegUsers).filter(RegUsers.email==user_email,RegUsers.status==1).count()
        if referral_users_count != 1:
            sessions.query(RegUsers).filter(RegUsers.user_id != userid,RegUsers.email==user_email,RegUsers.status==1).update({RegUsers.status: 3 }) # status as 3 for registered and not login users

        inserted_location = Location(location_name=site_name, company_id=company_id)
        sessions.add(inserted_location)
        sessions.flush()

        inserted_comp_his = CompanyDetailsHistory(company_id=company_id,company_name=company_name, address=address, email=email, site_name=site_name, country_id=country, state_id=state, city_id=city, user_id=userid, company_code=company_code)
        sessions.add(inserted_comp_his)
        sessions.flush()

        sessions.commit()
        session['company_name'] = company_name
        result = "Added Successfully"

    else:
        country_id = sessions.query(CompanyDetails.country_id).filter_by(user_id=userid).first()[0]

        if str(country_id) != country:
            sessions.query(ProductSelectionList).filter_by(user_id=userid).delete()
            sessions.query(UserSelectionList).filter_by(user_id=userid).delete()
            sessions.query(CloudSelection).filter_by(user_id=userid).delete()
            # cursor.execute(f"delete from product_selection_list where user_id={userid}")
            # cursor.execute(f"delete from user_selection_list where user_id={userid}")
            # cursor.execute(f"delete from cloud_selection where user_id={userid}")

        sessions.query(CompanyDetails).filter(CompanyDetails.user_id == userid).update({CompanyDetails.company_name: company_name, CompanyDetails.address: address,CompanyDetails.email: email, CompanyDetails.site_name: site_name,CompanyDetails.country_id: country, CompanyDetails.state_id: state, CompanyDetails.city_id: city, CompanyDetails.company_code: company_code})

        company_id = sessions.query(CompanyDetails.company_id).filter(CompanyDetails.user_id == userid).first()[0]
        sessions.query(Location).filter(Location.company_id == company_id).update({Location.location_name: site_name})

        inserted_comp_his = CompanyDetailsHistory(company_id=company_id, company_name=company_name, address=address, email=email, site_name=site_name, country_id=country, state_id=state, city_id=city, user_id=userid, company_code=company_code)
        sessions.add(inserted_comp_his)
        sessions.flush()
        sessions.commit()

        session['company_name'] = company_name
        result = "Updated Successfully"
        # else:
        #     result="Email already exists"

    return result


# def insert_billing_details(bill_no, invoice_company, gst_vat, invoice_address, country, state, city, userid,total_gst_amnt):

#     cursor.execute(f"INSERT into billing_details (bill_no,user_id,invoice_company_name,invoice_billing_address,gst_no,country_id,state_id,city_id)values {(bill_no,userid,invoice_company,invoice_address,gst_vat,country,state,city)} ")
#     currency_type = session['currency']
#     currency_symbol = session['currency_symbol']
#     current_date = datetime.date(datetime.now())
#     payment_date = current_date.strftime('%Y-%m-%d')

#     cursor.execute(f"select selc_id,pkg_id,product_id,amount,actual_amount,discount from product_selection_list where user_id={userid} order by selc_id desc ")
#     prod_selc_list = cursor.fetchone()
#     pkg_id = prod_selc_list[1]
#     pkg_product_id = prod_selc_list[2]
#     pkg_amount = prod_selc_list[3]
#     actual_amount = prod_selc_list[4]
#     discount = prod_selc_list[5]
#     pkg_renewal_datetime = current_date + relativedelta(years=1, days=-1)
#     pkg_renewal_date = pkg_renewal_datetime.strftime('%Y-%m-%d')
#     cursor.execute(f"INSERT into package_purchase_list (user_id,pkg_id,product_id,amount,currency_type,currency_symbol,latest_entry,payment_date,created_by,actual_amount,discount,renewal_date)values {(userid,pkg_id,pkg_product_id,pkg_amount,currency_type,currency_symbol,1,payment_date,userid,actual_amount,discount,pkg_renewal_date)} returning pkg_pur_id")
#     pkg_pur_id = cursor.fetchone()[0]

#     cursor.execute(f"INSERT into package_purchase_history (pkg_pur_id,user_id,pkg_id,product_id,amount,currency_type,currency_symbol,latest_entry,payment_date,created_by,actual_amount,discount,renewal_date)values {(pkg_pur_id,userid,pkg_id,pkg_product_id,pkg_amount,currency_type,currency_symbol,1,payment_date,userid,actual_amount,discount,pkg_renewal_date)} ")

#     cursor.execute(f"select user_selc_id,admin_user_count,admin_user_amount,general_user_count,general_user_amount,limited_user_count,limited_user_amount,billing_frequency from user_selection_list where user_id={userid} order by user_selc_id desc ")
#     user_selc_list = cursor.fetchone()
#     admin_user_count = user_selc_list[1]
#     admin_user_amount = user_selc_list[2]
#     general_user_count = user_selc_list[3]
#     general_user_amount = user_selc_list[4]
#     limited_user_count = user_selc_list[5]
#     limited_user_amount = user_selc_list[6]
#     billing_frequency = user_selc_list[7]

#     cursor.execute(f"select * from user_type order by user_type_id asc ")
#     user_selc_list = cursor.fetchall()
#     admin_user_id = user_selc_list[0][0]
#     general_user_id = user_selc_list[1][0]
#     limited_user_id = user_selc_list[2][0]
#     if billing_frequency == 'M':
#         user_renewal_datetime = current_date + relativedelta(months=1, days=-1)
#     else:
#         user_renewal_datetime = current_date + relativedelta(years=1, days=-1)
#     user_renewal_date = user_renewal_datetime.strftime('%Y-%m-%d')

#     if admin_user_count != 0:
#         cursor.execute(f"INSERT into user_purchase_list (user_id,user_type_id,no_of_users,amount,currency_type,currency_symbol,latest_entry,payment_date,created_by,billing_frequency,renewal_date)values {(userid,admin_user_id,admin_user_count,admin_user_amount,currency_type,currency_symbol,1,payment_date,userid,billing_frequency,user_renewal_date)} returning user_pur_id")
#         user_pur_admin_id = cursor.fetchone()[0]

#         cursor.execute(f"INSERT into user_purchase_history (user_pur_id,user_id,user_type_id,no_of_users,amount,currency_type,currency_symbol,latest_entry,payment_date,created_by,billing_frequency,renewal_date)values {(user_pur_admin_id,userid,admin_user_id,0,0,currency_type,currency_symbol,1,payment_date,userid,billing_frequency,user_renewal_date)} ")

#     else:

#         cursor.execute(f"INSERT into user_purchase_list (user_id,user_type_id,no_of_users,amount,currency_type,currency_symbol,latest_entry,payment_date,created_by,billing_frequency,renewal_date)values {(userid,admin_user_id,0,0,currency_type,currency_symbol,1,payment_date,userid,billing_frequency,user_renewal_date)} returning user_pur_id")
#         user_pur_admin_id = cursor.fetchone()[0]

#         cursor.execute(f"INSERT into user_purchase_history (user_pur_id,user_id,user_type_id,no_of_users,amount,currency_type,currency_symbol,latest_entry,payment_date,created_by,billing_frequency,renewal_date)values {(user_pur_admin_id,userid,admin_user_id,admin_user_count,admin_user_amount,currency_type,currency_symbol,1,payment_date,userid,billing_frequency,user_renewal_date)} ")


#     if general_user_count != 0:
#         cursor.execute(f"INSERT into user_purchase_list (user_id,user_type_id,no_of_users,amount,currency_type,currency_symbol,latest_entry,payment_date,created_by,billing_frequency,renewal_date)values {(userid,general_user_id,general_user_count,general_user_amount,currency_type,currency_symbol,1,payment_date,userid,billing_frequency,user_renewal_date)} returning user_pur_id")
#         user_pur_general_id = cursor.fetchone()[0]

#         cursor.execute(f"INSERT into user_purchase_history (user_pur_id,user_id,user_type_id,no_of_users,amount,currency_type,currency_symbol,latest_entry,payment_date,created_by,billing_frequency,renewal_date)values {(user_pur_general_id,userid,general_user_id,general_user_count,general_user_amount,currency_type,currency_symbol,1,payment_date,userid,billing_frequency,user_renewal_date)} ")

#     else:

#         cursor.execute(f"INSERT into user_purchase_list (user_id,user_type_id,no_of_users,amount,currency_type,currency_symbol,latest_entry,payment_date,created_by,billing_frequency,renewal_date)values {(userid,general_user_id,0,0,currency_type,currency_symbol,1,payment_date,userid,billing_frequency,user_renewal_date)} returning user_pur_id")
#         user_pur_general_id = cursor.fetchone()[0]

#         cursor.execute(f"INSERT into user_purchase_history (user_pur_id,user_id,user_type_id,no_of_users,amount,currency_type,currency_symbol,latest_entry,payment_date,created_by,billing_frequency,renewal_date)values {(user_pur_general_id,userid,general_user_id,0,0,currency_type,currency_symbol,1,payment_date,userid,billing_frequency,user_renewal_date)} ")

#     if limited_user_count != 0:
#         cursor.execute(f"INSERT into user_purchase_list (user_id,user_type_id,no_of_users,amount,currency_type,currency_symbol,latest_entry,payment_date,created_by,billing_frequency,renewal_date)values {(userid,limited_user_id,limited_user_count,limited_user_amount,currency_type,currency_symbol,1,payment_date,userid,billing_frequency,user_renewal_date)} returning user_pur_id ")
#         user_pur_limited_id = cursor.fetchone()[0]

#         cursor.execute(f"INSERT into user_purchase_history (user_pur_id,user_id,user_type_id,no_of_users,amount,currency_type,currency_symbol,latest_entry,payment_date,created_by,billing_frequency,renewal_date)values {(user_pur_limited_id,userid,limited_user_id,limited_user_count,limited_user_amount,currency_type,currency_symbol,1,payment_date,userid,billing_frequency,user_renewal_date)} ")
#     else:

#         cursor.execute(f"INSERT into user_purchase_list (user_id,user_type_id,no_of_users,amount,currency_type,currency_symbol,latest_entry,payment_date,created_by,billing_frequency,renewal_date)values {(userid,limited_user_id,0,0,currency_type,currency_symbol,1,payment_date,userid,billing_frequency,user_renewal_date)} returning user_pur_id")
#         user_pur_limited_id = cursor.fetchone()[0]

#         cursor.execute(f"INSERT into user_purchase_history (user_pur_id,user_id,user_type_id,no_of_users,amount,currency_type,currency_symbol,latest_entry,payment_date,created_by,billing_frequency,renewal_date)values {(user_pur_limited_id,userid,limited_user_id,0,0,currency_type,currency_symbol,1,payment_date,userid,billing_frequency,user_renewal_date)} ")

#     cursor.execute(f"select cloud_id,cl_type_id,amount from cloud_selection where user_id={userid} order by cloud_id desc ")
#     cloud_selc_list = cursor.fetchone()
#     cl_type_id = cloud_selc_list[1]
#     cloud_amount = cloud_selc_list[2]

#     cloud_renewal_datetime = current_date + relativedelta(years=1, days=-1)
#     cloud_renewal_date = cloud_renewal_datetime.strftime('%Y-%m-%d')

#     cursor.execute(f"INSERT into cloud_purchase_list (user_id,cloud_type_id,amount,currency_type,currency_symbol,latest_entry,payment_date,created_by,renewal_date)values {(userid,cl_type_id,cloud_amount,currency_type,currency_symbol,1,payment_date,userid,cloud_renewal_date)} returning cloud_pur_id ")
#     cloud_pur_id = cursor.fetchone()[0]

#     cursor.execute(f"INSERT into cloud_purchase_history (cloud_pur_id,user_id,cloud_type_id,amount,currency_type,currency_symbol,latest_entry,payment_date,created_by,renewal_date)values {(cloud_pur_id,userid,cl_type_id,cloud_amount,currency_type,currency_symbol,1,payment_date,userid,cloud_renewal_date)} ")
#     session['billing_count'] = 1

#     # cursor.execute(f"delete from product_selection_list where user_id={userid}")
#     # cursor.execute(f"delete from user_selection_list where user_id={userid}")
#     # cursor.execute(f"delete from cloud_selection where user_id={userid}")
#     # connection.commit()

#     cursor.execute(f"Insert into payment_history(payment_date,mode_of_payment,amount,transaction_details,user_id,status) values {(payment_date,'credit_card',total_gst_amnt,'1246566',userid,1)} ")

#     # card_no = str(encryptdata('09764')).replace("b", "").replace("'", "")
#     # cvv_no = str(encryptdata('998')).replace("b", "").replace("'", "")
#     # expiry_date = str(encryptdata('04/2020')).replace("b", "").replace("'", "")

#     card_no_val = '09764'
#     card_no = encryptdata(card_no_val)
#     cvv_no_val = '998'
#     cvv_no = encryptdata(cvv_no_val)
#     expiry_date_val = '04/20'
#     expiry_date = encryptdata(expiry_date_val)

#     cursor.execute(f"Insert into payment_mode(mode_of_payment,card_number,account_holder_name,cvv,expiry_date,user_id) values {('credit_card',card_no,'scopiq',cvv_no,expiry_date,userid)} ")
#     # connection.commit()
#     result = "Added Successfully"
#     return result


def insert_renewal_billing_details(bill_no, userid, product_id, amount, subscription_type, bill_id):
    if subscription_type == 1:
        cursor.execute(f"SELECT renewal_date+ INTERVAL '30 DAYS' from billing_details where bill_id={bill_id};")
        renewal_date = cursor.fetchone()[0]
    elif subscription_type == 2:
        cursor.execute(f"SELECT renewal_date + INTERVAL '90 DAYS' from billing_details where bill_id={bill_id};")
        renewal_date = cursor.fetchone()[0]
    elif subscription_type == 3:
        cursor.execute(f"SELECT renewal_date + INTERVAL '365 DAYS' from billing_details where bill_id={bill_id};")
        renewal_date = cursor.fetchone()[0]
    elif subscription_type == 4:
        cursor.execute(f"SELECT renewal_date + INTERVAL '99 YEARS' from billing_details where bill_id={bill_id};")
        renewal_date = cursor.fetchone()[0]
    new_renewaldate = str(renewal_date)
    cursor.execute(f"INSERT into billing_details (bill_no,user_id,product_id,amount,paid_status,subscription_type,renewal_date,latest_entry)values {(bill_no,userid,product_id,amount,1,subscription_type,new_renewaldate,1)} ")

    cursor.execute(f"update billing_details set latest_entry=0 where bill_id={bill_id}")
    connection.commit()
    result = "Added Successfully"
    return result


def insert_referral(email, first_name, last_name, userid, random_password, random_password_hash):
    session_email = session['email']
    email_count = sessions.query(RegUsers).filter(RegUsers.email==email,RegUsers.referred_by==userid).count()
    if email_count == 0:
        if session_email != email:
            inserted_users = RegUsers(email=email, first_name=first_name, last_name=last_name, referred_by=userid, status=1, password=random_password_hash, verification_code=0,user_type='P')
            sessions.add(inserted_users)
            sessions.flush()
            sessions.commit()
            msg = Message('Link', sender='username@gmail.com', recipients=[email])
            link = url_for('login', _external=True)
            msg.body = 'Your link is {}'.format(link)
            msg.html = render_template('emails/link_email.html', link=link, username=email, password=random_password)
            mail.send(msg)
            result = ""
        else:
            result = "You cannot send link to your own mail"
    else:
        result = "Already mail sent to this email"
    return result


def insert_prod_selection(userid, addtocart, product_id, amount, actual_amount, discount_amount):
    prod_selec_count = sessions.query(ProductSelectionList).filter(ProductSelectionList.user_id == userid).count()
    if prod_selec_count != 0:
        sessions.query(ProductSelectionList).filter(ProductSelectionList.user_id == userid).delete()

    inserted_products = ProductSelectionList(user_id=userid, pkg_id=addtocart, product_id=product_id, amount=amount, status=1, actual_amount=actual_amount, discount=discount_amount)
    sessions.add(inserted_products)
    sessions.flush()
    sessions.commit()


def insert_user_selection(admin_count, adminus, general_count, genus, limited_count, limus, totamnt, userid, billing_frequency, actual_amount, discount):
    user_selec_count = sessions.query(UserSelectionList).filter(UserSelectionList.user_id == userid).count()
    if user_selec_count != 0:
        sessions.query(UserSelectionList).filter(UserSelectionList.user_id == userid).delete()
    inserted_users = UserSelectionList(admin_user_count=admin_count, admin_user_amount=adminus, general_user_count=general_count, general_user_amount=genus, limited_user_count=limited_count, limited_user_amount=limus, amount=totamnt, status=1, user_id=userid, billing_frequency=billing_frequency, actual_amount=actual_amount, discount=discount)
    sessions.add(inserted_users)
    sessions.flush()
    sessions.commit()


# def insert_upgrade_user_selection(admin_count, adminus, general_count, genus, limited_count, limus, totamnt, userid, billing_frequency, actual_amount, discount):
#     cursor.execute(f"select count(*) from user_selection_list where user_id={userid}")
#     user_selec_count = cursor.fetchone()[0]
#     if user_selec_count != 0:
#         cursor.execute(f"delete from user_selection_list where user_id={userid}")
#         connection.commit()
#     cursor.execute(f"INSERT INTO user_selection_list(admin_user_count,admin_user_amount,general_user_count,general_user_amount,limited_user_count,limited_user_amount,amount,status,user_id,billing_frequency,actual_amount,discount)values {(admin_count,adminus,general_count,genus,limited_count,limus,totamnt,1,userid,billing_frequency,actual_amount,discount)}")
#     connection.commit()


def insert_server_settings(cloud_package, cloud_amount, userid):
    cloud_selec_count = sessions.query(CloudSelection).filter(CloudSelection.user_id == userid).count()
    if cloud_selec_count != 0:
        sessions.query(CloudSelection).filter(CloudSelection.user_id == userid).delete()
    inserted_cloud = CloudSelection(cl_type_id=cloud_package, amount=cloud_amount, user_id=userid,status=1)
    sessions.add(inserted_cloud)
    sessions.flush()
    sessions.commit()


def insert_upgrade_billing(selected_product_id, selected_user_id, selected_cloud_id, userid, selected_packages_amount,location_id,company_id,new_bill_no,new_pur_no,bill_num_val,pur_num_val):
    reg_user_type = sessions.query(RegUsers.user_type).filter(RegUsers.user_id == userid).first()[0]

    email = session['email']

    # company_id = sessions.query(CompanyDetails.company_id).filter_by(user_id=userid).first()[0]
    site_admin_db = str("scopiq_site_admin_")+str(company_id)+"_"+str(location_id)
    dms_db = str("scopiq_dms_")+str(company_id)+"_"+str(location_id)
    cms_db = str("scopiq_cms_")+str(company_id)+"_"+str(location_id)
    ams_db = str("scopiq_ams_")+str(company_id)+"_"+str(location_id)
    dsm_db = str("scopiq_dsm_")+str(company_id)+"_"+str(location_id)
    sms_db = str("scopiq_sms_")+str(company_id)+"_"+str(location_id)
    
    dsm_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+dsm_db)
    ams_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+ams_db)
    cms_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+cms_db)
    dms_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+dms_db)
    siteadmin_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+site_admin_db)
    sms_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+sms_db)

    Base = declarative_base()
    siteadmin_session = sessionmaker(bind=siteadmin_engine)
    dms_session = sessionmaker(bind=dms_engine)
    cms_session = sessionmaker(bind=cms_engine)
    ams_session = sessionmaker(bind=ams_engine)
    dsm_session = sessionmaker(bind=dsm_engine)
    sms_session = sessionmaker(bind=sms_engine)

    siteadmin_session_set = siteadmin_session()
    dms_session_set = dms_session()
    cms_session_set = cms_session()
    ams_session_set = ams_session()
    dsm_session_set = dsm_session()
    sms_session_set = sms_session()


    siteadmin_userid = siteadmin_session_set.query(Users.user_id).filter(Users.email==email).first()[0]
    

    # cursor1.execute(f"select user_id from users where email='{email}' ")
    # siteadmin_userid = cursor1.fetchone()[0]

    current_date = datetime.date(datetime.now())
    payment_date = current_date.strftime('%Y-%m-%d')

    currency_type = session['currency']
    currency_symbol = session['currency_symbol']

    pkg_renewal_date = sessions.query(PackagePurchaseList.renewal_date).filter(PackagePurchaseList.user_id==userid).first()[0]

    # cursor.execute(f"select renewal_date from package_purchase_list where user_id={userid}")
    # pkg_renewal_date = cursor.fetchone()[0]

    user_renewal_date = sessions.query(UserPurchaseList.renewal_date).filter(UserPurchaseList.user_id==userid).first()[0]

    # cursor.execute(f"select renewal_date from user_purchase_list where user_id={userid}")
    # user_renewal_date = cursor.fetchone()[0]

    if selected_product_id != '':
        prod_sel_list = sessions.query(ProductSelectionList).with_entities(ProductSelectionList.selc_id, ProductSelectionList.pkg_id, ProductSelectionList.product_id, ProductSelectionList.amount, ProductSelectionList.actual_amount, ProductSelectionList.discount).filter(ProductSelectionList.user_id==userid).order_by(ProductSelectionList.selc_id.desc()).first()

        # cursor.execute(f"select selc_id,pkg_id,product_id,amount,actual_amount,discount from product_selection_list where user_id={userid}")
        # prod_sel_list = cursor.fetchone()

        pkg_id = prod_sel_list[1]
        pkg_product_id = prod_sel_list[2]
        pkg_amount = prod_sel_list[3]
        actual_amount = prod_sel_list[4]
        discount = prod_sel_list[5]

        amount = sessions.query(PackagePurchaseList).with_entities(PackagePurchaseList.amount, PackagePurchaseList.renewal_date).filter(PackagePurchaseList.user_id==userid).first()
        pkg_tot_amount = pkg_amount+amount[0]

        if reg_user_type == "F":
            product_renewal_date = current_date + relativedelta(years=1, days=-1)
            prod_renewal_date = product_renewal_date.strftime('%Y-%m-%d')
        else:
            product_renewal_date = amount[1]
            prod_renewal_date = product_renewal_date.strftime('%Y-%m-%d')

        # cursor.execute(f"select amount,renewal_date from package_purchase_list where user_id={userid}")
        # amount = cursor.fetchone()
        # pkg_tot_amount = pkg_amount+amount[0]

        update_pkg = sessions.query(PackagePurchaseList).filter(PackagePurchaseList.user_id == userid).update({PackagePurchaseList.pkg_id: pkg_id, PackagePurchaseList.product_id: pkg_product_id,PackagePurchaseList.amount: pkg_tot_amount, PackagePurchaseList.currency_type: currency_type,PackagePurchaseList.currency_symbol: currency_symbol, PackagePurchaseList.latest_entry:1 , PackagePurchaseList.payment_date:payment_date ,PackagePurchaseList.created_by:userid ,PackagePurchaseList.renewal_date:prod_renewal_date, PackagePurchaseList.actual_amount:actual_amount, PackagePurchaseList.discount:discount,PackagePurchaseList.product_amount:pkg_amount})

        pkg_pur_id = sessions.query(PackagePurchaseList.pkg_pur_id).filter(PackagePurchaseList.user_id == userid).first()[0]

        inserted_pkg_pur_his = PackagePurchaseHistory(pkg_pur_id=pkg_pur_id,user_id=userid, pkg_id=pkg_id, product_id=pkg_product_id, amount=pkg_tot_amount, currency_type=currency_type, currency_symbol=currency_symbol, latest_entry=1, payment_date=payment_date, created_by=userid, actual_amount=actual_amount, discount=discount, renewal_date=prod_renewal_date, product_amount=pkg_amount)
        sessions.add(inserted_pkg_pur_his)
        sessions.flush()
        pkg_pur_his_id = inserted_pkg_pur_his.pkg_history_id


        sessions.query(ProductSelectionList).filter_by(user_id=userid).delete()

        package_product_list = list(pkg_product_id.split(","))

        siteadmin_session_set.query(Packages).filter_by(user_id=siteadmin_userid).delete()
        for pkg_product_id in package_product_list:
            product_id = encryptdata(pkg_product_id)

            insertsite_prod = Packages(user_id=siteadmin_userid, product_id=product_id, link='localhost:5003', renewal_date=prod_renewal_date)
            siteadmin_session_set.add(insertsite_prod)
            siteadmin_session_set.flush()
            
            check_count = siteadmin_session_set.query(MenuRolesList).filter(and_(MenuRolesList.user_id==siteadmin_userid, MenuRolesList.product_id==pkg_product_id)).count()
            
            
            if check_count == 0:

                insertsite_menu_role_list = MenuRolesList(user_id=siteadmin_userid,product_id=pkg_product_id, role_ids = 5)
                
                siteadmin_session_set.add(insertsite_menu_role_list)
                siteadmin_session_set.flush()

                insertsite_menu_role_list_his = MenuRolesHistory(user_id=siteadmin_userid, product_id=pkg_product_id, role_ids = 5)
                
                siteadmin_session_set.add(insertsite_menu_role_list_his)
                siteadmin_session_set.flush()

                # # fetch users from site_admin db and insert into new product db
                
                # if int(pkg_product_id) == int(9):
                #     fetch_siteadmin_users = sessions.query(Users).all()
                #     for site_data in fetch_siteadmin_users:

                #         users_add_dsm = Users(department_id=site_data.department_id, email=site_data.email, username=site_data.username, first_name=site_data.first_name, last_name=site_data.last_name, blood_group=site_data.blood_group, personal_contact=site_data.personal_contact, password_hash=site_data.password_hash, role_id=site_data.role_id, employee_code=site_data.employee_code, created_by=site_data.created_by, location_id=site_data.location_id, company_id=site_data.company_id, filedata=site_data.filedata, type_of_user=site_data.type_of_user, sys_role=site_data.sys_role, status=site_data.status, phone_code=site_data.phone_code, initial_type_of_user=site_data.initial_type_of_user,reporting_manager_id=site_data.reporting_manager_id,old_emp_id=site_data.old_emp_id,dob=site_data.dob,doj=site_data.doj,reassign_status = site_data.reassign_status,left_date= site_data.left_date,country_id=site_data.country_id,state_id=site_data.state_id,city_id=site_data.city_id)
                #         dsm_session_set.add(users_add_dsm)
                #         dsm_session_set.flush()

                #     dsm_session_set.commit()


    
    else:
        pkg_pur_his_id = 0

    if selected_user_id != '':
        user_selc_list = sessions.query(UserSelectionList).with_entities(UserSelectionList.user_selc_id, UserSelectionList.admin_user_count, UserSelectionList.admin_user_amount, UserSelectionList.general_user_count, UserSelectionList.general_user_amount, UserSelectionList.limited_user_count, UserSelectionList.limited_user_amount, UserSelectionList.billing_frequency).filter(UserSelectionList.user_id==userid).order_by(UserSelectionList.user_selc_id.desc()).first()

        admin_user_count = user_selc_list[1]
        admin_user_amount = user_selc_list[2]
        general_user_count = user_selc_list[3]
        general_user_amount = user_selc_list[4]
        limited_user_count = user_selc_list[5]
        limited_user_amount = user_selc_list[6]
        billing_frequency = user_selc_list[7]

        history_billing_frequency = sessions.query(UserPurchaseHistory.billing_frequency).filter(UserPurchaseHistory.user_id==userid).order_by(UserPurchaseHistory.user_history_id.desc()).first()[0]

        if reg_user_type == "F":
            if billing_frequency == "A":
                user_renewal_date = current_date + relativedelta(years=1, days=-1)
                renewal_date = user_renewal_date.strftime('%Y-%m-%d')
            else:
               user_renewal_date = current_date + relativedelta(months=1, days=-1)
               renewal_date = user_renewal_date.strftime('%Y-%m-%d') 
        else:
            if history_billing_frequency == 'M' and billing_frequency == "A":
                renewal_date = pkg_renewal_date
            elif history_billing_frequency == 'M' and billing_frequency == "M":
                renewal_date = user_renewal_date
            else:  # Annual to Annual
                renewal_date = user_renewal_date

        if reg_user_type != "F":
            if admin_user_count != 0:
                amount =  sessions.query(UserPurchaseList.amount).filter(UserPurchaseList.user_id==userid, UserPurchaseList.user_type_id == 1).first()[0]
                admin_user_tot_amount = float(amount)+float(admin_user_amount)

                existing_admin_user_count = sessions.query(UserPurchaseList.no_of_users).filter(UserPurchaseList.user_id==userid, UserPurchaseList.user_type_id == 1).first()[0]

                actual_admin_user_count = admin_user_count - existing_admin_user_count

                update_user = sessions.query(UserPurchaseList).filter(UserPurchaseList.user_id == userid, UserPurchaseList.user_type_id == 1).update({UserPurchaseList.no_of_users: admin_user_count, UserPurchaseList.amount: admin_user_tot_amount , UserPurchaseList.payment_date: payment_date , UserPurchaseList.billing_frequency: billing_frequency , UserPurchaseList.renewal_date: renewal_date, UserPurchaseList.actual_no_of_users:actual_admin_user_count,UserPurchaseList.actual_amount:admin_user_amount})
                
                user_pur_admin_id = sessions.query(UserPurchaseList.user_pur_id).filter(UserPurchaseList.user_id == userid, UserPurchaseList.user_type_id == 1).first()[0]
                
                inserted_usr_pur_admin_his = UserPurchaseHistory(user_pur_id=user_pur_admin_id,user_id=userid,user_type_id=1, no_of_users=admin_user_count, amount=admin_user_tot_amount, currency_type=currency_type, currency_symbol=currency_symbol, latest_entry=1, payment_date=payment_date, created_by=userid, billing_frequency=billing_frequency, renewal_date=renewal_date,actual_no_of_users=actual_admin_user_count,actual_amount=admin_user_amount)
                sessions.add(inserted_usr_pur_admin_his)
                sessions.flush()
                admin_usr_his_id = inserted_usr_pur_admin_his.user_history_id

            else:
                admin_usr_his_id = ""
                
            if general_user_count != 0:
                amount =  sessions.query(UserPurchaseList.amount).filter(UserPurchaseList.user_id==userid, UserPurchaseList.user_type_id ==2).first()[0]
                general_user_tot_amount = float(amount)+float(general_user_amount)

                existing_general_user_count = sessions.query(UserPurchaseList.no_of_users).filter(UserPurchaseList.user_id==userid, UserPurchaseList.user_type_id == 2).first()[0]

                actual_general_user_count = general_user_count - existing_general_user_count

                update_gen_user = sessions.query(UserPurchaseList).filter(UserPurchaseList.user_id == userid, UserPurchaseList.user_type_id == 2).update({UserPurchaseList.no_of_users: general_user_count, UserPurchaseList.amount: general_user_tot_amount , UserPurchaseList.payment_date: payment_date , UserPurchaseList.billing_frequency: billing_frequency , UserPurchaseList.renewal_date: renewal_date, UserPurchaseList.actual_no_of_users:actual_general_user_count,UserPurchaseList.actual_amount:general_user_amount })
                
                user_pur_general_id = sessions.query(UserPurchaseList.user_pur_id).filter(UserPurchaseList.user_id == userid, UserPurchaseList.user_type_id == 2).first()[0]

                inserted_usr_pur_general_his = UserPurchaseHistory(user_pur_id=user_pur_general_id,user_id=userid,user_type_id=2, no_of_users=general_user_count, amount=general_user_tot_amount, currency_type=currency_type, currency_symbol=currency_symbol, latest_entry=1, payment_date=payment_date, created_by=userid, billing_frequency=billing_frequency, renewal_date=renewal_date, actual_no_of_users=actual_general_user_count,actual_amount=general_user_amount)
                sessions.add(inserted_usr_pur_general_his)
                sessions.flush()
                gen_usr_his_id = inserted_usr_pur_general_his.user_history_id

            else:
                gen_usr_his_id = ""

            if limited_user_count != 0:
                amount =  sessions.query(UserPurchaseList.amount).filter(UserPurchaseList.user_id==userid, UserPurchaseList.user_type_id ==3).first()[0]

                limited_user_tot_amount = float(amount) + float(limited_user_amount)

                existing_limited_user_count = sessions.query(UserPurchaseList.no_of_users).filter(UserPurchaseList.user_id==userid, UserPurchaseList.user_type_id == 3).first()[0]

                actual_limited_user_count = limited_user_count - existing_limited_user_count

                update_lim_user = sessions.query(UserPurchaseList).filter(UserPurchaseList.user_id == userid, UserPurchaseList.user_type_id == 3).update({UserPurchaseList.no_of_users: limited_user_count, UserPurchaseList.amount: limited_user_tot_amount , UserPurchaseList.payment_date: payment_date , UserPurchaseList.billing_frequency: billing_frequency , UserPurchaseList.renewal_date: renewal_date, UserPurchaseList.actual_no_of_users:actual_limited_user_count,UserPurchaseList.actual_amount:limited_user_amount})
                
                user_pur_limited_id = sessions.query(UserPurchaseList.user_pur_id).filter(UserPurchaseList.user_id == userid, UserPurchaseList.user_type_id == 3).first()[0]

                inserted_usr_pur_lim_his = UserPurchaseHistory(user_pur_id=user_pur_limited_id,user_id=userid,user_type_id=3, no_of_users=limited_user_count, amount=limited_user_tot_amount, currency_type=currency_type, currency_symbol=currency_symbol, latest_entry=1, payment_date=payment_date, created_by=userid, billing_frequency=billing_frequency, renewal_date=renewal_date, actual_no_of_users=actual_limited_user_count,actual_amount=limited_user_amount)
                sessions.add(inserted_usr_pur_lim_his)
                sessions.flush()
                lim_usr_his_id = inserted_usr_pur_lim_his.user_history_id

            else:
                lim_usr_his_id = ""
            
            if admin_usr_his_id != "" and gen_usr_his_id != "" and lim_usr_his_id != "":
                usr_pur_his_id = str(admin_usr_his_id)+","+str(gen_usr_his_id)+","+str(lim_usr_his_id)
            elif admin_usr_his_id != "" and gen_usr_his_id == "" and lim_usr_his_id == "":
                usr_pur_his_id = str(admin_usr_his_id)
            elif admin_usr_his_id == "" and gen_usr_his_id != "" and lim_usr_his_id == "":
                usr_pur_his_id = str(gen_usr_his_id)
            elif admin_usr_his_id == "" and gen_usr_his_id == "" and lim_usr_his_id != "":
                usr_pur_his_id = str(lim_usr_his_id)
            elif admin_usr_his_id != "" and gen_usr_his_id != "" and lim_usr_his_id == "":
                usr_pur_his_id = str(admin_usr_his_id)+","+str(gen_usr_his_id)
            elif admin_usr_his_id != "" and gen_usr_his_id == "" and lim_usr_his_id != "":
                usr_pur_his_id = str(admin_usr_his_id)+","+str(lim_usr_his_id)
            elif admin_usr_his_id == "" and gen_usr_his_id != "" and lim_usr_his_id != "":
                usr_pur_his_id = str(gen_usr_his_id)+","+str(lim_usr_his_id)
            elif admin_usr_his_id == "" and gen_usr_his_id == "" and lim_usr_his_id == "":
                usr_pur_his_id = ""




        else:
            usr_pur_his_id = ""
        sessions.query(UserSelectionList).filter_by(user_id=userid).delete()

        siteadmin_session_set.query(UserList).filter_by(user_id=siteadmin_userid).delete()

        # cursor.execute(f"delete from user_selection_list where user_id={userid}")

        # cursor1.execute(f"delete from user_list where user_id='{siteadmin_userid}'")

        usr_purchased_list = sessions.query(UserPurchaseList).with_entities(UserPurchaseList.user_type_id, UserPurchaseList.no_of_users).filter(UserPurchaseList.user_id == userid).all()

        # cursor.execute(f"select * from user_purchase_list where user_id={userid}")
        # columns = [col[0] for col in cursor.description]
        # usr_purchased_list = [dict(zip(columns, row)) for row in cursor.fetchall()]
        for usr_pur_list in usr_purchased_list:
            user_type_id = usr_pur_list[0]
            no_of_users = usr_pur_list[1]
            
            user_type = encryptdata(user_type_id)
            user_count = encryptdata(no_of_users)

            insertsite_user = UserList(user_id=siteadmin_userid, user_type_id=user_type, no_of_users=user_count, renewal_date=renewal_date)
            siteadmin_session_set.add(insertsite_user)
            siteadmin_session_set.flush()

            # cursor1.execute(
            #     f"INSERT into user_list(user_id,user_type_id,no_of_users,renewal_date) values {(siteadmin_userid, user_type,user_count,str(renewal_date) )} ")

        # connection.commit()
        # connection1.commit()

    else:
        usr_pur_his_id = ""

    if selected_cloud_id != '':
        cloud_selc_list = sessions.query(CloudSelection).with_entities(CloudSelection.cloud_id, CloudSelection.cl_type_id,CloudSelection.amount).filter(CloudSelection.user_id==userid).order_by(CloudSelection.cloud_id.desc()).first()

        # cursor.execute(f"select cloud_id,cl_type_id,amount from cloud_selection where user_id={userid} order by cloud_id desc ")
        # cloud_selc_list = cursor.fetchone()
        cl_type_id = cloud_selc_list[1]
        cloud_amount = cloud_selc_list[2]

        # cursor.execute(f"select amount,renewal_date from cloud_purchase_list where user_id={userid}")
        # amount = cursor.fetchone()
        amount = sessions.query(CloudPurchaseList).with_entities(CloudPurchaseList.amount, CloudPurchaseList.renewal_date).filter(CloudPurchaseList.user_id==userid).first()
        
        cloud_tot_amount = int(cloud_amount)+amount[0]

        if reg_user_type == "F":
            cld_renewal_date = current_date + relativedelta(years=1, days=-1)
            cloud_renewal_date = cld_renewal_date.strftime('%Y-%m-%d')
        
        else:
            cld_renewal_date = amount[1]
            cloud_renewal_date = cld_renewal_date.strftime('%Y-%m-%d')

        update_cloud = sessions.query(CloudPurchaseList).filter(CloudPurchaseList.user_id == userid).update({CloudPurchaseList.cloud_type_id: cl_type_id,CloudPurchaseList.amount: cloud_tot_amount, CloudPurchaseList.currency_type: currency_type,CloudPurchaseList.currency_symbol: currency_symbol, CloudPurchaseList.latest_entry:1 , CloudPurchaseList.payment_date:payment_date ,CloudPurchaseList.created_by:userid,CloudPurchaseList.renewal_date:cld_renewal_date, CloudPurchaseList.actual_amount:cloud_amount})
        cloud_pur_id = sessions.query(CloudPurchaseList.cloud_pur_id).filter(CloudPurchaseList.user_id == userid).first()[0]

        # cursor.execute(f"Update cloud_purchase_list set cloud_type_id={cl_type_id},amount={cloud_tot_amount},currency_type='{currency_type}',currency_symbol='{currency_symbol}',payment_date='{payment_date}',created_by={userid} where user_id={userid} returning cloud_pur_id")
        # cloud_pur_id = cursor.fetchone()[0]

        inserted_cld_pur_his = CloudPurchaseHistory(cloud_pur_id=cloud_pur_id,user_id=userid, cloud_type_id=cl_type_id, amount=cloud_tot_amount, currency_type=currency_type, currency_symbol=currency_symbol, latest_entry=1, payment_date=payment_date, created_by=userid, renewal_date=cloud_renewal_date, actual_amount=cloud_amount)
        sessions.add(inserted_cld_pur_his)
        sessions.flush()
        cld_pur_his_id = inserted_cld_pur_his.cloud_history_id

        # cursor.execute(f"INSERT into cloud_purchase_history (cloud_pur_id,user_id,cloud_type_id,amount,currency_type,currency_symbol,latest_entry,payment_date,created_by)values {(cloud_pur_id,userid,cl_type_id,cloud_tot_amount,currency_type,currency_symbol,1,payment_date,userid)} ")
        siteadmin_session_set.query(CloudList).filter_by(user_id=siteadmin_userid).delete()

        # cursor1.execute(f"delete from cloud_list where user_id='{siteadmin_userid}'")

        cloudtype_id = encryptdata(cl_type_id)

        insertsite_cloud = CloudList(user_id=siteadmin_userid, cloud_type_id=cloudtype_id , renewal_date=cloud_renewal_date)
        siteadmin_session_set.add(insertsite_cloud)
        siteadmin_session_set.flush()

        # cursor1.execute(
        #     f"INSERT into cloud_list(user_id,cloud_type_id,renewal_date) values {(siteadmin_userid, cloudtype_id,cloud_renewal_date )} ")

        sessions.query(CloudSelection).filter_by(user_id=userid).delete()
        # cursor.execute(f"delete from cloud_selection where user_id={userid}")
        # connection.commit()

    else:
        cld_pur_his_id = 0

    inserted_pay_his = PaymentHistory(payment_date=payment_date, mode_of_payment='credit_card', amount=selected_packages_amount, transaction_details='1246566', user_id=userid, status=1, pkg_pur_his_id= pkg_pur_his_id, user_pur_his_id=usr_pur_his_id, cld_pur_his_id=cld_pur_his_id,bill_no=new_bill_no,purchase_no=new_pur_no,bill_series_no=bill_num_val,purchase_series_no=pur_num_val)
    sessions.add(inserted_pay_his)
    sessions.flush()

    last_insert_pay_his_id = inserted_pay_his.payment_history_id

    card_no_val = '09764'
    card_no = encryptdata(card_no_val)
    cvv_no_val = '998'
    cvv_no = encryptdata(cvv_no_val)
    expiry_date_val = '04/20'
    expiry_date = encryptdata(expiry_date_val)

    inserted_pay_his = PaymentMode(mode_of_payment='credit_card', card_number=card_no, account_holder_name='scopiq', cvv=cvv_no, expiry_date=expiry_date, user_id=userid)
    sessions.add(inserted_pay_his)
    sessions.flush()

    if reg_user_type == "F":
        sessions.query(RegUsers).filter(RegUsers.user_id == userid).update({RegUsers.user_type: 'P'})

    sessions.commit()
    siteadmin_session_set.commit()
    
    return last_insert_pay_his_id

    # cursor.execute(f"Insert into payment_mode(mode_of_payment,card_number,account_holder_name,cvv,expiry_date,user_id) values {('credit_card',card_no,'scopiq',cvv_no,expiry_date,userid)} ")
    # connection.commit()
    # connection1.commit()


def update_upgrade_company(email, site_name, address, company_name, userid, usr_country,usr_state,usr_city):
    # cursor.execute(
    #     f"select company_id from company_details WHERE user_id={userid} ")
    # comp_id = cursor.fetchone()[0]
    company_id = sessions.query(CompanyDetails.company_id).filter_by(user_id=userid).first()[0]

    location_list = sessions.query(Location).with_entities(Location.location_id,Location.location_name).filter(Location.company_id == company_id).first()
    location_id = location_list[0]
    location_name = location_list[1]

    site_admin_db = str("scopiq_site_admin_")+str(company_id)+"_"+str(location_id)
    dms_db = str("scopiq_dms_")+str(company_id)+"_"+str(location_id)
    cms_db = str("scopiq_cms_")+str(company_id)+"_"+str(location_id)
    ams_db = str("scopiq_ams_")+str(company_id)+"_"+str(location_id)
    kms_db = str("scopiq_kms_")+str(company_id)+"_"+str(location_id)
    dsm_db = str("scopiq_dsm_")+str(company_id)+"_"+str(location_id)
    sms_db = str("scopiq_sms_")+str(company_id)+"_"+str(location_id)
    
    sms_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+sms_db)
    dsm_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+dsm_db)
    kms_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+kms_db)
    ams_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+ams_db)
    cms_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+cms_db)
    dms_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+dms_db)
    siteadmin_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+site_admin_db)

    Base = declarative_base()
    siteadmin_session = sessionmaker(bind=siteadmin_engine)
    dms_session = sessionmaker(bind=dms_engine)
    cms_session = sessionmaker(bind=cms_engine)
    ams_session = sessionmaker(bind=ams_engine)
    kms_session = sessionmaker(bind=kms_engine)
    dsm_session = sessionmaker(bind=dsm_engine)
    sms_session = sessionmaker(bind=sms_engine)

    siteadmin_session_set = siteadmin_session()
    dms_session_set = dms_session()
    cms_session_set = cms_session()
    ams_session_set = ams_session()
    kms_session_set = kms_session()
    dsm_session_set = dsm_session()
    sms_session_set = sms_session()

    sessions.query(CompanyDetails).filter(CompanyDetails.user_id == userid).update({CompanyDetails.company_name: company_name, CompanyDetails.address: address,CompanyDetails.email: email, CompanyDetails.site_name: site_name})

    comp_id = sessions.query(CompanyDetails.company_id).filter(CompanyDetails.user_id == userid).first()[0]

    dynamic_table_name = sessions.query(CompanyDetails.dynamic_table_name).filter(CompanyDetails.company_id == comp_id).first()[0]

    sessions.query(Location).filter(Location.company_id == comp_id).update({Location.location_name: site_name})

    inserted_comp_his = CompanyDetailsHistory(company_id=comp_id,company_name=company_name, address=address, email=email, site_name=site_name, country_id=usr_country, state_id=usr_state, city_id=usr_city, user_id=userid)
    sessions.add(inserted_comp_his)
    sessions.flush()
    sessions.commit()

    siteadmin_session_set.query(Company).filter(Company.dynamic_table_name == dynamic_table_name).update({Company.company_name: company_name, Company.address: address,Company.email: email})

    siteadmin_comp_id = siteadmin_session_set.query(Company.company_id).filter(Company.dynamic_table_name == dynamic_table_name).first()[0]

    dms_session_set.query(Company).filter(Company.company_id == siteadmin_comp_id).update({Company.company_name: company_name, Company.address: address,Company.email: email})

    cms_session_set.query(Company).filter(Company.company_id == siteadmin_comp_id).update({Company.company_name: company_name, Company.address: address,Company.email: email})
    
    ams_session_set.query(Company).filter(Company.company_id == siteadmin_comp_id).update({Company.company_name: company_name, Company.address: address,Company.email: email})

    kms_session_set.query(Company).filter(Company.company_id == siteadmin_comp_id).update({Company.company_name: company_name, Company.address: address,Company.email: email})
    
    dsm_session_set.query(Company).filter(Company.company_id == siteadmin_comp_id).update({Company.company_name: company_name, Company.address: address,Company.email: email})


    sms_session_set.query(Company).filter(Company.company_id == siteadmin_comp_id).update({Company.company_name: company_name, Company.address: address,Company.email: email})
    

    siteadmin_session_set.commit()
    dms_session_set.commit()
    cms_session_set.commit()
    ams_session_set.commit()
    kms_session_set.commit()
    dsm_session_set.commit()
    sms_session_set.commit()
    
    # cursor1.execute(
    #     f"update company set company_name='{company_name}',address='{address}',email='{email}' where dynamic_table_name='{dynamic_table_name}' returning company_id")
    # siteadmin_comp_id = cursor1.fetchone()[0]

    # cursor2.execute(
    #     f"update company set company_name='{company_name}',address='{address}',email='{email}' where company_id='{siteadmin_comp_id}' ")
    
    # connection.commit()
    # connection1.commit()
    # connection2.commit()

    session['company_name'] = company_name
    result = "Updated Successfully"
    return result


def insert_billing_details(bill_no, invoice_company, gst_vat, invoice_address, country, state, city, userid,total_gst_amnt,company_id,location_id,new_bill_no,bill_num_val,new_pur_no,pur_num_val,company_code):
        site_admin_db = str("scopiq_site_admin_")+str(company_id)+"_"+str(location_id)
        dms_db = str("scopiq_dms_")+str(company_id)+"_"+str(location_id)
        cms_db = str("scopiq_cms_")+str(company_id)+"_"+str(location_id)
        ams_db = str("scopiq_ams_")+str(company_id)+"_"+str(location_id)
        kms_db = str("scopiq_kms_")+str(company_id)+"_"+str(location_id)
        dsm_db = str("scopiq_dsm_")+str(company_id)+"_"+str(location_id)
        sms_db = str("scopiq_sms_")+str(company_id)+"_"+str(location_id)
        cams_db = str("scopiq_cams_")+str(company_id)+"_"+str(location_id)
        capa_db = str("scopiq_capa_")+str(company_id)+"_"+str(location_id)

        capa_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+capa_db)
        cams_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+cams_db)
        sms_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+sms_db)
        dsm_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+dsm_db)
        kms_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+kms_db)
        ams_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+ams_db)
        cms_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+cms_db)
        dms_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+dms_db)
        siteadmin_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+site_admin_db)

        Base = declarative_base()
        siteadmin_session = sessionmaker(bind=siteadmin_engine)
        
        dms_session = sessionmaker(bind=dms_engine)
        cms_session = sessionmaker(bind=cms_engine)
        ams_session = sessionmaker(bind=ams_engine)
        kms_session = sessionmaker(bind=kms_engine)
        dsm_session = sessionmaker(bind=dsm_engine)
        sms_session = sessionmaker(bind=sms_engine)
        cams_session = sessionmaker(bind=cams_engine)
        capa_session = sessionmaker(bind=capa_engine)


        siteadmin_session_set = siteadmin_session()
        dms_session_set = dms_session()
        cms_session_set = cms_session()
        ams_session_set = ams_session()
        kms_session_set = kms_session()
        dsm_session_set = dsm_session()
        sms_session_set = sms_session()
        cams_session_set = cams_session()
        capa_session_set = capa_session()
        
        prod_details_list = ['Document Management','Certificate Management','Audit Management','CAPA','Supplier Management','Calibration Management','Workflow','Knowledge Management','Storage Vault']
        
        if len(prod_details_list) > 0:
            prod_increment_id = 1
            for prod_data in range(len(prod_details_list)):
                insert_prod_details = ProductList(product_id=prod_increment_id,product_name=prod_details_list[prod_data])
                
                siteadmin_session_set.add(insert_prod_details)
                siteadmin_session_set.flush()
                
                prod_increment_id = prod_increment_id + 1
                
        # inserting default table values into site admin db
                
        sys_role_list = ['Module Admin','Program Admin','Manager','Approver','User','Location Admin','No Access','Releaser','HR Admin','Authorised Personnel','Lead Auditor','Auditor','Auditee','Process Manager']
        if len(sys_role_list) > 0:
            sys_role_increment_id = 1
            for sys_role_data in range(len(sys_role_list)):
                insert_sys_role_details = Systemrole(roleid=sys_role_increment_id,rolename=sys_role_list[sys_role_data])
                
                siteadmin_session_set.add(insert_sys_role_details)
                siteadmin_session_set.flush()
                
                sys_role_increment_id = sys_role_increment_id + 1
        date_format_list = ['DD-MM-YYYY','YYYY-MM-DD','YYYY-mm-DD','mm-dd-YYYY']
        if len(date_format_list) > 0:
            df_increment_id = 1
            for df_data in range(len(date_format_list)):
                insert_df_details = DateFormat(date_format_id=df_increment_id,date_format=date_format_list[df_data],status=1)
                
                siteadmin_session_set.add(insert_df_details)
                siteadmin_session_set.flush()
                
                df_increment_id = df_increment_id + 1    
        country_name_list = ['India','United States']
        country_code_list = ['IN','US']
        country_phn_code_list = ['91','1']
        country_curr_list = ['INR','USD']
        country_curr_sym_list = ['???','$']
        if len(country_name_list) > 0:
            cl_increment_id = 1
            for cl_data in range(len(country_name_list)):
                insert_cl_details = Country(country_id=cl_increment_id,country_name=country_name_list[cl_data],country_code=country_code_list[cl_data],phone_code=country_phn_code_list[cl_data],currency=country_curr_list[cl_data],currency_symbol=country_curr_sym_list[cl_data])
                
                siteadmin_session_set.add(insert_cl_details)
                siteadmin_session_set.flush()
                
                cl_increment_id = cl_increment_id + 1
        state_name_list = ['Kerala','TamilNadu','California','New York']
        state_countryid_list = [1,1,2,2]
        if len(state_name_list) > 0:
            snl_increment_id = 1
            for sl_data in range(len(state_name_list)):
                insert_sl_details = State(state_id=snl_increment_id,state_name=state_name_list[sl_data],country_id=state_countryid_list[sl_data])
                
                siteadmin_session_set.add(insert_sl_details)
                siteadmin_session_set.flush()
                
                snl_increment_id = snl_increment_id + 1         
        city_name_list = ['Guruvayur','Idukki','Madurai','Thoothukudi','Sunland','Sunnyvale','North Valley','Silver City']
        city_stateid_list = [1,1,2,2,3,3,4,4]
        if len(city_name_list) > 0:
            citylist_increment_id = 1
            for citylist_data in range(len(city_name_list)):
                insert_citylist_details = City(city_id=citylist_increment_id,city_name=city_name_list[citylist_data],state_id=city_stateid_list[citylist_data])
                
                siteadmin_session_set.add(insert_citylist_details)
                siteadmin_session_set.flush()
                
                citylist_increment_id = citylist_increment_id + 1
                
        # inserting default table values into dms db
              
        dms_sys_role_list = ['Module Admin','Program Admin','Manager','Approver','User','Location Admin','No Access','Releaser','HR Admin','Authorised Personnel','Lead Auditor','Auditor','Auditee','Process Manager']
        if len(dms_sys_role_list) > 0:
            dms_sys_role_increment_id = 1
            for dms_sys_role_data in range(len(dms_sys_role_list)):
                insert_dms_sysrole = Systemrole(roleid=dms_sys_role_increment_id,rolename=dms_sys_role_list[dms_sys_role_data])
                
                dms_session_set.add(insert_dms_sysrole)
                dms_session_set.flush()
                
                dms_sys_role_increment_id = dms_sys_role_increment_id + 1
        dms_date_format_list = ['DD-MM-YYYY','YYYY-MM-DD','YYYY-mm-DD','mm-dd-YYYY']
        if len(dms_date_format_list) > 0:
            dms_df_increment_id = 1
            for dms_df_data in range(len(dms_date_format_list)):
                insert_dms_df_details = DateFormat(date_format_id=dms_df_increment_id,date_format=dms_date_format_list[dms_df_data],status=1)
                
                dms_session_set.add(insert_dms_df_details)
                dms_session_set.flush()
                
                dms_df_increment_id = dms_df_increment_id + 1    
        country_name_list = ['India','United States']
        country_code_list = ['IN','US']
        country_phn_code_list = ['91','1']
        country_curr_list = ['INR','USD']
        country_curr_sym_list = ['???','$']
        if len(country_name_list) > 0:
            dms_cl_increment_id = 1
            for cl_data in range(len(country_name_list)):
                insert_dms_cl_details = Country(country_id=dms_cl_increment_id,country_name=country_name_list[cl_data],country_code=country_code_list[cl_data],phone_code=country_phn_code_list[cl_data],currency=country_curr_list[cl_data],currency_symbol=country_curr_sym_list[cl_data])
                
                dms_session_set.add(insert_dms_cl_details)
                dms_session_set.flush()
                
                dms_cl_increment_id = dms_cl_increment_id + 1
        state_name_list = ['Kerala','TamilNadu','California','New York']
        state_countryid_list = [1,1,2,2]
        if len(state_name_list) > 0:
            dms_snl_increment_id = 1
            for sl_data in range(len(state_name_list)):
                insert_dms_sl_details = State(state_id=dms_snl_increment_id,state_name=state_name_list[sl_data],country_id=state_countryid_list[sl_data])
                
                dms_session_set.add(insert_dms_sl_details)
                dms_session_set.flush()
                
                dms_snl_increment_id = dms_snl_increment_id + 1         
        city_name_list = ['Guruvayur','Idukki','Madurai','Thoothukudi','Sunland','Sunnyvale','North Valley','Silver City']
        city_stateid_list = [1,1,2,2,3,3,4,4]
        if len(city_name_list) > 0:
            dms_citylist_increment_id = 1
            for citylist_data in range(len(city_name_list)):
                insert_dms_citylist_details = City(city_id=dms_citylist_increment_id,city_name=city_name_list[citylist_data],state_id=city_stateid_list[citylist_data])
                
                dms_session_set.add(insert_dms_citylist_details)
                dms_session_set.flush()
                
                dms_citylist_increment_id = dms_citylist_increment_id + 1
        
        revision_rules_list =['Only Major Single Digit','Minor With One Decimal','Minor With Two Decimal','Roman Numbers','Single Digit String','Double Digit String','Only Major Single Digit(Start with 0)','Minor With Two Decimal(Start with 0)']
        revision_minor_list = ['','x+0.1','x+0.01','','','','','x+0.01']
        revision_major_list =  ['x+1','float(float(x))+1.0','float(float(x))+1.00','x+1','chr(ord(x)+1)','x+AA','x+1','float(float(x))+1.00']
        revision_starting_number = ['1','0.0','0.01','I','A','AA','0','0.00']
        rule_id_example =['1,2,3,4, ... etc','0.0,0.1,0.2,0.3, ... etc','0.01,0.02,0.03, ... etc','I,II,III,IV, ... etc','A,B,C,D, ... etc','AA,AB,AC,AD, ... etc','0,1,2,3, ... etc','0.00,0.01,0.02, ... etc']
        if len(revision_rules_list) > 0:
            dms_revision_increment_id = 1
            for revision_rules_list_data in range(len(revision_rules_list)):
                insert_dms_revision_details = Revisionrule(revision_rule_id=dms_revision_increment_id,rules=revision_rules_list[revision_rules_list_data],minor_addend=revision_minor_list[revision_rules_list_data],major_addend=revision_major_list[revision_rules_list_data],created_date=datetime.now(),starting_number=revision_starting_number[revision_rules_list_data],rule_id_example=rule_id_example[revision_rules_list_data])
                
                dms_session_set.add(insert_dms_revision_details)
                dms_session_set.flush()
                
                dms_revision_increment_id = dms_revision_increment_id + 1

        # type_name =['OSHA','Safety','EHS','Quality','Procedure']
       
        # if len(type_name) > 0:
        #     dms_global_increment_id = 1
        #     for global_program in range(len(type_name)):
        #         insert_global_details = GlobalProgramType(gpt_id=dms_global_increment_id,type_name=type_name[global_program],status = 1, created_date=datetime.now())
                
        #         sessions.add(insert_global_details)
        #         sessions.flush()
                
        #         dms_global_increment_id = dms_global_increment_id + 1
                
                
        format_temp_media = ['DOUBLEPAGEWITHOUT.doc', 'DOUBLEPAGEWITHOUT.doc']
        format_temp_template_code = ['DEFAULTTEMPLATE', 'HTMLDEFAULTTEMPLATE']
        format_temp_description = ['default template1@@@default', 'default template1@@@default']
        format_temp_status = ['1','1']
        format_temp_comp_id = ['1', '1']
        format_temp_template_name = ['DEFAULTTEMPLATE', 'HTMLDEFAULTTEMPLATE']
        if len(format_temp_media) > 0:
            dms_format_temp_increment_id = 1
            for format_temp_data in range(len(format_temp_media)):
                
                insert_dms_format_templates = FormatTemplates(media = format_temp_media[format_temp_data], template_code = format_temp_template_code[format_temp_data], description = format_temp_description[format_temp_data], status = format_temp_status[format_temp_data], company_id = 1, template_name = format_temp_template_name[format_temp_data])
                
                dms_session_set.add(insert_dms_format_templates)
                dms_session_set.flush()
                
        format_all_temp_media = ['prog_coverpage_WL_WB.html','prog_coverpage_WL_WISO_WOB.html','prog_coverpage_WL_WOB.html','prog_coverpage_WL_WP_WA_WOB.html','prog_coverpage_WL_WP_WISO_WOB.html','node_coverpage_WL_WB.html','node_coverpage_WL_WISO_WOB.html','node_coverpage_WL_WOB.html','node_coverpage_WL_WP_WA_WOB.html','node_coverpage_WL_WP_WISO_WOB.html','tablecontentpage_logoleft_WB.html','tablecontentpage_logoleft_WOB.html','coverpage_logoleft_PAA_WB_RY.html','coverpage_logoleft_PA_WB_RN.html','coverpage_logoleft_PRAL_WB_RN.html','coverpage_logoleft_PRAL_WB_RY.html','coverpage_logoleft_PRA_WB_RN.html','coverpage_logoleft_PRA_WB_RY.html','coverpage_logoleft_PRA_WOB_RN.html','coverpage_logoright_PRA_WB_RY.html','contentpage_logoleft_WB.html','contentpage_logoright_split_WB.html','contentpage_logoright_split_WOB.html','contentpage_logoright_WB.html']    
        format_all_temp_img_name =['prog_coverpage_WL_WB.jpg','prog_coverpage_WL_WISO_WOB.jpg','prog_coverpage_WL_WOB.jpg','prog_coverpage_WL_WP_WA_WOB.jpg','prog_coverpage_WL_WP_WISO_WOB.jpg','node_coverpage_WL_WB.jpg','node_coverpage_WL_WISO_WOB.jpg','node_coverpage_WL_WOB.jpg','node_coverpage_WL_WP_WA_WOB.jpg','node_coverpage_WL_WP_WISO_WOB.jpg','tablecontentpage_logoleft_WB.jpg','tablecontentpage_logoleft_WOB.jpg','coverpage_logoleft_PAA_WB_RY.jpg','coverpage_logoleft_PA_WB_RN.jpg','coverpage_logoleft_PRAL_WB_RN.jpg','coverpage_logoleft_PRAL_WB_RY.jpg','coverpage_logoleft_PRA_WB_RN.jpg','coverpage_logoleft_PRA_WB_RY.jpg','coverpage_logoleft_PRA_WOB_RN.jpg','coverpage_logoright_PRA_WB_RY.jpg','contentpage_logoleft_WB.jpg','contentpage_logoright_split_WB.jpg','contentpage_logoright_split_WOB.jpg','contentpage_logoright_WB.jpg']
        format_all_temp_type = ['1','1','1','1','1','2','2','2','2','2','3','3','4','4','4','4','4','4','4','4','5','5','5','5']  
        format_all_temp_rev_check =['no','no','no','no','no','no','no','no','no','no','no','no','yes','no','no','yes','no','yes','no','yes','no','no','no','no']
        format_all_prepared_count = [0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0]
        format_all_reviewd_count =  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0]
        format_all_approved_count = [0,0,0,0,0,0,0,0,0,0,0,0,2,1,1,1,1,1,1,1,0,0,0,0]
        format_all_released_count = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0]
        format_all_temp_source =    ['-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-']
        if len(format_all_temp_media) > 0:
            dms_format_temp_all_increment_id = 1
            for format_temp_data in range(len(format_all_temp_media)):
               
                insert_dms_format_all_templates = TemplateDetails(temp_file_name = format_all_temp_media[format_temp_data], temp_image_name = format_all_temp_img_name[format_temp_data], temp_type = format_all_temp_type[format_temp_data], temp_rev_check = format_all_temp_rev_check[format_temp_data], prepared_count = format_all_prepared_count[format_temp_data],reviewed_count =format_all_reviewd_count[format_temp_data],approved_count =format_all_approved_count[format_temp_data],released_count =format_all_released_count[format_temp_data],temp_source =format_all_temp_source[format_temp_data] )
               
                dms_session_set.add(insert_dms_format_all_templates)
                dms_session_set.flush()
                dms_format_temp_all_increment_id = dms_format_temp_all_increment_id + 1
                
        # inserting default table values into cms db
              
        cms_sys_role_list = ['Module Admin','Program Admin','Manager','Approver','User','Location Admin','No Access','Releaser','HR Admin','Authorised Personnel','Lead Auditor','Auditor','Auditee','Process Manager']
        if len(cms_sys_role_list) > 0:
            cms_sys_role_increment_id = 1
            for cms_sys_role_data in range(len(cms_sys_role_list)):
                insert_cms_sysrole = Systemrole(roleid=cms_sys_role_increment_id,rolename=cms_sys_role_list[cms_sys_role_data])
                
                cms_session_set.add(insert_cms_sysrole)
                cms_session_set.flush()
                
                cms_sys_role_increment_id = cms_sys_role_increment_id + 1
        cms_date_format_list = ['DD-MM-YYYY','YYYY-MM-DD','YYYY-mm-DD','mm-dd-YYYY']
        if len(cms_date_format_list) > 0:
            cms_df_increment_id = 1
            for cms_df_data in range(len(cms_date_format_list)):
                insert_cms_df_details = DateFormat(date_format_id=cms_df_increment_id,date_format=cms_date_format_list[cms_df_data],status=1)
                
                cms_session_set.add(insert_cms_df_details)
                cms_session_set.flush()
                
                cms_df_increment_id = cms_df_increment_id + 1    
        country_name_list = ['India','United States']
        country_code_list = ['IN','US']
        country_phn_code_list = ['91','1']
        country_curr_list = ['INR','USD']
        country_curr_sym_list = ['???','$']
        if len(country_name_list) > 0:
            cms_cl_increment_id = 1
            for cl_data in range(len(country_name_list)):
                insert_cms_cl_details = Country(country_id=cms_cl_increment_id,country_name=country_name_list[cl_data],country_code=country_code_list[cl_data],phone_code=country_phn_code_list[cl_data],currency=country_curr_list[cl_data],currency_symbol=country_curr_sym_list[cl_data])
                
                cms_session_set.add(insert_cms_cl_details)
                cms_session_set.flush()
                
                cms_cl_increment_id = cms_cl_increment_id + 1
        state_name_list = ['Kerala','TamilNadu','California','New York']
        state_countryid_list = [1,1,2,2]
        if len(state_name_list) > 0:
            cms_snl_increment_id = 1
            for sl_data in range(len(state_name_list)):
                insert_cms_sl_details = State(state_id=cms_snl_increment_id,state_name=state_name_list[sl_data],country_id=state_countryid_list[sl_data])
                
                cms_session_set.add(insert_cms_sl_details)
                cms_session_set.flush()
                
                cms_snl_increment_id = cms_snl_increment_id + 1         
        city_name_list = ['Guruvayur','Idukki','Madurai','Thoothukudi','Sunland','Sunnyvale','North Valley','Silver City']
        city_stateid_list = [1,1,2,2,3,3,4,4]
        if len(city_name_list) > 0:
            cms_citylist_increment_id = 1
            for citylist_data in range(len(city_name_list)):
                insert_cms_citylist_details = City(city_id=cms_citylist_increment_id,city_name=city_name_list[citylist_data],state_id=city_stateid_list[citylist_data])
                
                cms_session_set.add(insert_cms_citylist_details)
                cms_session_set.flush()
                
                cms_citylist_increment_id = cms_citylist_increment_id + 1
        
        type_name_list = ['Personal Certification','Company Certification']
        indiv_comp_list = [1,1]
        if len(type_name_list) > 0:
            cms_typelist_increment_id = 1
            for typelist_data in range(len(type_name_list)):
                insert_cms_typelist_details = Type(typename=type_name_list[typelist_data],indiv_comp=indiv_comp_list[typelist_data])
                
                cms_session_set.add(insert_cms_typelist_details)
                cms_session_set.flush()
                
                cms_typelist_increment_id = cms_typelist_increment_id + 1


        # inserting default table values into ams db
              
        ams_sys_role_list = ['Module Admin','Program Admin','Manager','Approver','User','Location Admin','No Access','Releaser','HR Admin','Authorised Personnel','Lead Auditor','Auditor','Auditee','Process Manager']
        if len(ams_sys_role_list) > 0:
            ams_sys_role_increment_id = 1
            for ams_sys_role_data in range(len(ams_sys_role_list)):
                insert_ams_sysrole = Systemrole(roleid=ams_sys_role_increment_id,rolename=ams_sys_role_list[ams_sys_role_data])
                
                ams_session_set.add(insert_ams_sysrole)
                ams_session_set.flush()
                
                ams_sys_role_increment_id = ams_sys_role_increment_id + 1

        ams_date_format_list = ['DD-MM-YYYY','YYYY-MM-DD','YYYY-mm-DD','mm-dd-YYYY']
        if len(ams_date_format_list) > 0:
            ams_df_increment_id = 1
            for ams_df_data in range(len(ams_date_format_list)):
                insert_ams_df_details = DateFormat(date_format_id=ams_df_increment_id,date_format=ams_date_format_list[ams_df_data],status=1)
                
                ams_session_set.add(insert_ams_df_details)
                ams_session_set.flush()
                
                ams_df_increment_id = ams_df_increment_id + 1 
                
        country_name_list = ['India','United States']
        country_code_list = ['IN','US']
        country_phn_code_list = ['91','1']
        country_curr_list = ['INR','USD']
        country_curr_sym_list = ['???','$']
        if len(country_name_list) > 0:
            ams_cl_increment_id = 1
            for al_data in range(len(country_name_list)):
                insert_ams_cl_details = Country(country_id=ams_cl_increment_id,country_name=country_name_list[al_data],country_code=country_code_list[al_data],phone_code=country_phn_code_list[al_data],currency=country_curr_list[al_data],currency_symbol=country_curr_sym_list[al_data])
                
                ams_session_set.add(insert_ams_cl_details)
                ams_session_set.flush()
                
                ams_cl_increment_id = ams_cl_increment_id + 1

        state_name_list = ['Kerala','TamilNadu','California','New York']
        state_countryid_list = [1,1,2,2]
        if len(state_name_list) > 0:
            ams_snl_increment_id = 1
            for sl_data in range(len(state_name_list)):
                insert_ams_sl_details = State(state_id=ams_snl_increment_id,state_name=state_name_list[sl_data],country_id=state_countryid_list[sl_data])
                
                ams_session_set.add(insert_ams_sl_details)
                ams_session_set.flush()
                
                ams_snl_increment_id = ams_snl_increment_id + 1         

        city_name_list = ['Guruvayur','Idukki','Madurai','Thoothukudi','Sunland','Sunnyvale','North Valley','Silver City']
        city_stateid_list = [1,1,2,2,3,3,4,4]
        if len(city_name_list) > 0:
            ams_citylist_increment_id = 1
            for citylist_data in range(len(city_name_list)):
                insert_ams_citylist_details = City(city_id=ams_citylist_increment_id,city_name=city_name_list[citylist_data],state_id=city_stateid_list[citylist_data])
                
                ams_session_set.add(insert_ams_citylist_details)
                ams_session_set.flush()
                
                ams_citylist_increment_id = ams_citylist_increment_id + 1
        
        type_name_list = ['Quality','Safety','EHS','OSHA']
        type_code_list = ['QA','SA','ES','OS']
        if len(type_name_list) > 0:
            ams_typelist_increment_id = 1
            for typelist_data in range(len(type_name_list)):
                insert_ams_typelist_details = AuditType(typename=type_name_list[typelist_data],status=1,typecode=type_code_list[typelist_data])
                
                ams_session_set.add(insert_ams_typelist_details)
                ams_session_set.flush()
                
                ams_typelist_increment_id = ams_typelist_increment_id + 1


        # inserting default table values into ams db

        kms_sys_role_list = ['Module Admin','Program Admin','Manager','Approver','User','Location Admin','No Access','Releaser','HR Admin','Authorised Personnel','Lead Auditor','Auditor','Auditee','Process Manager']
        if len(kms_sys_role_list) > 0:
            kms_sys_role_increment_id = 1
            for kms_sys_role_data in range(len(kms_sys_role_list)):
                insert_kms_sys_role_details = Systemrole(roleid=kms_sys_role_increment_id,rolename=kms_sys_role_list[kms_sys_role_data])
                
                kms_session_set.add(insert_kms_sys_role_details)
                kms_session_set.flush()
                
                kms_sys_role_increment_id = kms_sys_role_increment_id + 1

        kms_date_format_list = ['DD-MM-YYYY','YYYY-MM-DD','YYYY-mm-DD','mm-dd-YYYY']
        if len(kms_date_format_list) > 0:
            kms_df_increment_id = 1
            for kms_df_data in range(len(kms_date_format_list)):
                insert_kms_df_details = DateFormat(date_format_id=kms_df_increment_id,date_format=kms_date_format_list[kms_df_data],status=1)
                
                kms_session_set.add(insert_kms_df_details)
                kms_session_set.flush()
                
                kms_df_increment_id = kms_df_increment_id + 1


        country_name_list = ['India','United States']
        country_code_list = ['IN','US']
        country_phn_code_list = ['91','1']
        country_curr_list = ['INR','USD']
        country_curr_sym_list = ['???','$']
        if len(country_name_list) > 0:
            kl_increment_id = 1
            for kl_data in range(len(country_name_list)):
                insert_kl_details = Country(country_id=kl_increment_id,country_name=country_name_list[kl_data],country_code=country_code_list[kl_data],phone_code=country_phn_code_list[kl_data],currency=country_curr_list[kl_data],currency_symbol=country_curr_sym_list[kl_data])
                
                kms_session_set.add(insert_kl_details)
                kms_session_set.flush()
                
                kl_increment_id = kl_increment_id + 1


        state_name_list = ['Kerala','TamilNadu','California','New York']
        state_countryid_list = [1,1,2,2]
        if len(state_name_list) > 0:
            snkl_increment_id = 1
            for skl_data in range(len(state_name_list)):
                insert_skl_details = State(state_id=snkl_increment_id,state_name=state_name_list[skl_data],country_id=state_countryid_list[skl_data])
                
                kms_session_set.add(insert_skl_details)
                kms_session_set.flush()
                
                snkl_increment_id = snkl_increment_id + 1  



        city_name_list = ['Guruvayur','Idukki','Madurai','Thoothukudi','Sunland','Sunnyvale','North Valley','Silver City']
        city_stateid_list = [1,1,2,2,3,3,4,4]
        if len(city_name_list) > 0:
            kms_citylist_increment_id = 1
            for kcitylist_data in range(len(city_name_list)):
                insert_kcitylist_details = City(city_id=kms_citylist_increment_id,city_name=city_name_list[kcitylist_data],state_id=city_stateid_list[kcitylist_data])
                
                kms_session_set.add(insert_kcitylist_details)
                kms_session_set.flush()
                
                kms_citylist_increment_id = kms_citylist_increment_id + 1
        ###DSM
        # inserting default table values into dsm db
              
        dsm_sys_role_list = ['Module Admin','Program Admin','Manager','Approver','User','Location Admin','No Access','Releaser','HR Admin','Authorised Personnel','Lead Auditor','Auditor','Auditee','Process Manager']
        if len(dsm_sys_role_list) > 0:
            dsm_sys_role_increment_id = 1
            for dsm_sys_role_data in range(len(dsm_sys_role_list)):
                insert_dsm_sysrole = Systemrole(roleid=dsm_sys_role_increment_id,rolename=dsm_sys_role_list[dsm_sys_role_data])
                
                dsm_session_set.add(insert_dsm_sysrole)
                dsm_session_set.flush()
                
                dsm_sys_role_increment_id = dsm_sys_role_increment_id + 1
        dsm_date_format_list = ['DD-MM-YYYY','YYYY-MM-DD','YYYY-mm-DD','mm-dd-YYYY']
        if len(dsm_date_format_list) > 0:
            dsm_df_increment_id = 1
            for dsm_df_data in range(len(dsm_date_format_list)):
                insert_dsm_df_details = DateFormat(date_format_id=dsm_df_increment_id,date_format=dsm_date_format_list[dsm_df_data],status=1)
                
                dsm_session_set.add(insert_dsm_df_details)
                dsm_session_set.flush()
                
                dsm_df_increment_id = dsm_df_increment_id + 1    
        country_name_list = ['India','United States']
        country_code_list = ['IN','US']
        country_phn_code_list = ['91','1']
        country_curr_list = ['INR','USD']
        country_curr_sym_list = ['???','$']
        if len(country_name_list) > 0:
            dsm_cl_increment_id = 1
            for cl_data in range(len(country_name_list)):
                insert_dsm_cl_details = Country(country_id=dsm_cl_increment_id,country_name=country_name_list[cl_data],country_code=country_code_list[cl_data],phone_code=country_phn_code_list[cl_data],currency=country_curr_list[cl_data],currency_symbol=country_curr_sym_list[cl_data])
                
                dsm_session_set.add(insert_dsm_cl_details)
                dsm_session_set.flush()
                
                dsm_cl_increment_id = dsm_cl_increment_id + 1
        state_name_list = ['Kerala','TamilNadu','California','New York']
        state_countryid_list = [1,1,2,2]
        if len(state_name_list) > 0:
            dsm_snl_increment_id = 1
            for sl_data in range(len(state_name_list)):
                insert_dsm_sl_details = State(state_id=dsm_snl_increment_id,state_name=state_name_list[sl_data],country_id=state_countryid_list[sl_data])
                
                dsm_session_set.add(insert_dsm_sl_details)
                dsm_session_set.flush()
                
                dsm_snl_increment_id = dsm_snl_increment_id + 1         
        city_name_list = ['Guruvayur','Idukki','Madurai','Thoothukudi','Sunland','Sunnyvale','North Valley','Silver City']
        city_stateid_list = [1,1,2,2,3,3,4,4]
        if len(city_name_list) > 0:
            dsm_citylist_increment_id = 1
            for citylist_data in range(len(city_name_list)):
                insert_dsm_citylist_details = City(city_id=dsm_citylist_increment_id,city_name=city_name_list[citylist_data],state_id=city_stateid_list[citylist_data])
                
                dsm_session_set.add(insert_dsm_citylist_details)
                dsm_session_set.flush()
                
                dsm_citylist_increment_id = dsm_citylist_increment_id + 1


        ###CAMS
        # inserting default table values into cams db
        group_name_list = ['Plant and Machinery','Instruments']
        group_code_list = ['PM','IA']
        if len(group_name_list) > 0:
            cams_grouplist_increment_id = 1
            for codelist_data in range(len(group_name_list)):
                insert_cams_group_details = CamsGroupList(group_id=cams_grouplist_increment_id,group_name=group_name_list[codelist_data],short_code=group_code_list[codelist_data],status = 1,sub_group_status = 1)
                
                cams_session_set.add(insert_cams_group_details)
                cams_session_set.flush()
                
                cams_grouplist_increment_id = cams_grouplist_increment_id + 1
              
        cams_sys_role_list = ['Module Admin','Program Admin','Manager','Approver','User','Location Admin','No Access','Releaser','HR Admin','Authorised Personnel','Lead Auditor','Auditor','Auditee','Process Manager']
        if len(cams_sys_role_list) > 0:
            cams_sys_role_increment_id = 1
            for cams_sys_role_data in range(len(cams_sys_role_list)):
                insert_cams_sysrole = Systemrole(roleid=cams_sys_role_increment_id,rolename=cams_sys_role_list[cams_sys_role_data])
                
                cams_session_set.add(insert_cams_sysrole)
                cams_session_set.flush()
                
                cams_sys_role_increment_id = cams_sys_role_increment_id + 1


        cams_date_format_list = ['DD-MM-YYYY','YYYY-MM-DD','YYYY-mm-DD','mm-dd-YYYY']
        if len(cams_date_format_list) > 0:
            cams_df_increment_id = 1
            for cams_df_data in range(len(cams_date_format_list)):
                insert_cams_df_details = DateFormat(date_format_id=cams_df_increment_id,date_format=cams_date_format_list[cams_df_data],status=1)
                
                cams_session_set.add(insert_cams_df_details)
                cams_session_set.flush()
                
                cams_df_increment_id = cams_df_increment_id + 1   

        country_name_list = ['India','United States']
        country_code_list = ['IN','US']
        country_phn_code_list = ['91','1']
        country_curr_list = ['INR','USD']
        country_curr_sym_list = ['???','$']
        if len(country_name_list) > 0:
            cams_cl_increment_id = 1
            for cl_data in range(len(country_name_list)):
                insert_cams_cl_details = Country(country_id=cams_cl_increment_id,country_name=country_name_list[cl_data],country_code=country_code_list[cl_data],phone_code=country_phn_code_list[cl_data],currency=country_curr_list[cl_data],currency_symbol=country_curr_sym_list[cl_data])
                
                cams_session_set.add(insert_cams_cl_details)
                cams_session_set.flush()
                
                cams_cl_increment_id = cams_cl_increment_id + 1

        state_name_list = ['Kerala','TamilNadu','California','New York']
        state_countryid_list = [1,1,2,2]
        if len(state_name_list) > 0:
            cams_snl_increment_id = 1
            for sl_data in range(len(state_name_list)):
                insert_cams_sl_details = State(state_id=cams_snl_increment_id,state_name=state_name_list[sl_data],country_id=state_countryid_list[sl_data])
                
                cams_session_set.add(insert_cams_sl_details)
                cams_session_set.flush()
                
                cams_snl_increment_id = cams_snl_increment_id + 1      

        city_name_list = ['Guruvayur','Idukki','Madurai','Thoothukudi','Sunland','Sunnyvale','North Valley','Silver City']
        city_stateid_list = [1,1,2,2,3,3,4,4]
        if len(city_name_list) > 0:
            cams_citylist_increment_id = 1
            for citylist_data in range(len(city_name_list)):
                insert_cams_citylist_details = City(city_id=cams_citylist_increment_id,city_name=city_name_list[citylist_data],state_id=city_stateid_list[citylist_data])
                
                cams_session_set.add(insert_cams_citylist_details)
                cams_session_set.flush()
                
                cams_citylist_increment_id = cams_citylist_increment_id + 1
        
        # dsm_date_format_list = ['DD-MM-YYYY','YYYY-MM-DD','YYYY-mm-DD','mm-dd-YYYY']
        # if len(dsm_date_format_list) > 0:
        #     dsm_df_increment_id = 1
        #     for dsm_df_data in range(len(dsm_date_format_list)):
        #         insert_dsm_df_details = DateFormat(date_format_id=dsm_df_increment_id,date_format=dsm_date_format_list[dsm_df_data],status=1)
                
        #         dsm_session_set.add(insert_dsm_df_details)
        #         dsm_session_set.flush()
                
        #         dsm_df_increment_id = dsm_df_increment_id + 1
        ###CAPA
        # inserting default table values into capa db
        nc_type_list = ['Customer Complaint','Product Complaint','Quality Process','Quality Product','Safety','Administration','Risk Assessment','Ext / Customer udit NC']
        group_code_list = ['CC','PC','QPR','QPD','SAF','ADM','RA','AUD']
        if len(nc_type_list) > 0:
            capa_grouplist_increment_id = 1
            for codelist_data in range(len(nc_type_list)):
                insert_capa_group_details = CapaNcType(nc_type_id=capa_grouplist_increment_id,nc_typename=nc_type_list[codelist_data],nc_typecode=group_code_list[codelist_data],status = 1)
                
                capa_session_set.add(insert_capa_group_details)
                capa_session_set.flush()
                
                capa_grouplist_increment_id = capa_grouplist_increment_id + 1
              
        capa_sys_role_list = ['Module Admin','Program Admin','Manager','Approver','User','Location Admin','No Access','Releaser','HR Admin','Authorised Personnel','Lead Auditor','Auditor','Auditee','Process Manager']
        if len(capa_sys_role_list) > 0:
            capa_sys_role_increment_id = 1
            for capa_sys_role_data in range(len(capa_sys_role_list)):
                insert_capa_sysrole = Systemrole(roleid=capa_sys_role_increment_id,rolename=capa_sys_role_list[capa_sys_role_data])
                
                capa_session_set.add(insert_capa_sysrole)
                capa_session_set.flush()
                
                capa_sys_role_increment_id = capa_sys_role_increment_id + 1


        capa_date_format_list = ['DD-MM-YYYY','YYYY-MM-DD','YYYY-mm-DD','mm-dd-YYYY']
        if len(capa_date_format_list) > 0:
            capa_df_increment_id = 1
            for capa_df_data in range(len(capa_date_format_list)):
                insert_cams_df_details = DateFormat(date_format_id=capa_df_increment_id,date_format=capa_date_format_list[capa_df_data],status=1)
                
                capa_session_set.add(insert_cams_df_details)
                capa_session_set.flush()
                
                capa_df_increment_id = capa_df_increment_id + 1   

        country_name_list = ['India','United States']
        country_code_list = ['IN','US']
        country_phn_code_list = ['91','1']
        country_curr_list = ['INR','USD']
        country_curr_sym_list = ['???','$']
        if len(country_name_list) > 0:
            cams_cl_increment_id = 1
            for cl_data in range(len(country_name_list)):
                insert_cams_cl_details = Country(country_id=cams_cl_increment_id,country_name=country_name_list[cl_data],country_code=country_code_list[cl_data],phone_code=country_phn_code_list[cl_data],currency=country_curr_list[cl_data],currency_symbol=country_curr_sym_list[cl_data])
                
                capa_session_set.add(insert_cams_cl_details)
                capa_session_set.flush()
                
                cams_cl_increment_id = cams_cl_increment_id + 1

        state_name_list = ['Kerala','TamilNadu','California','New York']
        state_countryid_list = [1,1,2,2]
        if len(state_name_list) > 0:
            cams_snl_increment_id = 1
            for sl_data in range(len(state_name_list)):
                insert_cams_sl_details = State(state_id=cams_snl_increment_id,state_name=state_name_list[sl_data],country_id=state_countryid_list[sl_data])
                
                capa_session_set.add(insert_cams_sl_details)
                capa_session_set.flush()
                
                cams_snl_increment_id = cams_snl_increment_id + 1      

        city_name_list = ['Guruvayur','Idukki','Madurai','Thoothukudi','Sunland','Sunnyvale','North Valley','Silver City']
        city_stateid_list = [1,1,2,2,3,3,4,4]
        if len(city_name_list) > 0:
            cams_citylist_increment_id = 1
            for citylist_data in range(len(city_name_list)):
                insert_cams_citylist_details = City(city_id=cams_citylist_increment_id,city_name=city_name_list[citylist_data],state_id=city_stateid_list[citylist_data])
                
                capa_session_set.add(insert_cams_citylist_details)
                capa_session_set.flush()
                
                cams_citylist_increment_id = cams_citylist_increment_id + 1
        
        # inserting default table values into capa db
        nc_type_list = ['CAR','5-Why']
        group_code_list = ['CAR','FIW']
        if len(nc_type_list) > 0:
            capa_grouplist_increment_id = 1
            for codelist_data in range(len(nc_type_list)):
                insert_capa_group_details = CapaWorkFlowType(wf_type_id=capa_grouplist_increment_id,wf_typename=nc_type_list[codelist_data],wf_typecode=group_code_list[codelist_data],status = 1)
                
                capa_session_set.add(insert_capa_group_details)
                capa_session_set.flush()
                
                capa_grouplist_increment_id = capa_grouplist_increment_id + 1
        
        # inserting default table values into capa db
        nc_type_list = ['HML','Rating']
        if len(nc_type_list) > 0:
            capa_grouplist_increment_id = 1
            for codelist_data in range(len(nc_type_list)):
                insert_capa_group_details = NcRiskLevelName(nc_risk_id=capa_grouplist_increment_id,nc_riskname=nc_type_list[codelist_data],status = 1)
                
                capa_session_set.add(insert_capa_group_details)
                capa_session_set.flush()
                
                capa_grouplist_increment_id = capa_grouplist_increment_id + 1
                
        # inserting default table values into capa db
        nc_riskname_id = [1,1,1,2,2,2,2,2]
        nc_risk_number = [5,3,1,1,2,3,4,5]
        nc_risk_value = ['High','Mid','Low','V. Low','Low','Mid','High','V.High']
        if len(nc_riskname_id) > 0:
            capa_grouplist_increment_id = 1
            for codelist_data in range(len(nc_riskname_id)):
                insert_capa_group_details = NcRiskLevel(nc_riskid=capa_grouplist_increment_id,nc_riskname_id=nc_riskname_id[codelist_data],nc_risk_number = nc_risk_number[codelist_data],nc_risk_value = nc_risk_value[codelist_data] ,status = 1)
                
                capa_session_set.add(insert_capa_group_details)
                capa_session_set.flush()
                
                capa_grouplist_increment_id = capa_grouplist_increment_id + 1        

        
                                
    # try:
        # print("one")
        dynamic_tablename = "admin_" + str(company_id) + "_" + str(userid)
        dynamic_table = Table(dynamic_tablename, metadata,Column('user_id', Integer, primary_key=True), Column('user_name', String, nullable=False), Column('emp_code', String), Column('email', String, nullable=False), Column('created_by', BigInteger), Column('created_date', DateTime(timezone=True), default=func.now(), nullable=False), Column('updated_by', BigInteger), Column('updated_date', DateTime(timezone=True), default=func.now()), Column('status', String),extend_existing=True)
        metadata.create_all(engine)
        print("two")

        # cursor.execute(f"create table if not exists admin_{company_id}_{userid}(user_id serial PRIMARY KEY,user_name varchar,emp_code varchar, email varchar not null,created_date timestamp with time zone DEFAULT now() NOT NULL,created_by bigint,updated_date timestamp with time zone, updated_by bigint)")

        updated_user = sessions.query(CompanyDetails).filter(CompanyDetails.company_id == company_id).update({CompanyDetails.dynamic_table_name: dynamic_tablename })

        # cursor.execute(f"update company_details set dynamic_table_name='admin_{company_id}_{userid}' where company_id={company_id}")

        

        inserted_billing = BillingDetails(bill_no=bill_no,user_id=userid, invoice_company_name=invoice_company, invoice_billing_address=invoice_address, gst_no=gst_vat, country_id=country, state_id=state, city_id=city)
        sessions.add(inserted_billing)
        sessions.flush()
        
        # cursor.execute(f"INSERT into billing_details (bill_no,user_id,invoice_company_name,invoice_billing_address,gst_no,country_id,state_id,city_id)values {(bill_no,userid,invoice_company,invoice_address,gst_vat,country,state,city)} ")

        currency_type = session['currency']
        currency_symbol = session['currency_symbol']
        current_date = datetime.date(datetime.now())
        payment_date = current_date.strftime('%Y-%m-%d')
        
        prod_selc_list = sessions.query(ProductSelectionList).with_entities(ProductSelectionList.selc_id, ProductSelectionList.pkg_id, ProductSelectionList.product_id, ProductSelectionList.amount, ProductSelectionList.actual_amount, ProductSelectionList.discount).filter(ProductSelectionList.user_id==userid).order_by(ProductSelectionList.selc_id.desc()).first()

        # cursor.execute(f"select selc_id,pkg_id,product_id,amount,actual_amount,discount from product_selection_list where user_id={userid} order by selc_id desc ")
        # prod_selc_list = cursor.fetchone()
        pkg_id = prod_selc_list[1]
        pkg_product_id = prod_selc_list[2]
        pkg_amount = prod_selc_list[3]
        actual_amount = prod_selc_list[4]
        discount = prod_selc_list[5]
        reg_user_type = sessions.query(RegUsers.user_type).filter(RegUsers.user_id == userid).first()[0]

        if reg_user_type == "F":
            pkg_renewal_datetime = current_date + relativedelta(months=3, days=-1)
        else:
            pkg_renewal_datetime = current_date + relativedelta(years=1, days=-1)
        pkg_renewal_date = pkg_renewal_datetime.strftime('%Y-%m-%d')

        inserted_pkg_pur = PackagePurchaseList(user_id=userid, pkg_id=pkg_id, product_id=pkg_product_id, amount=pkg_amount, currency_type=currency_type, currency_symbol=currency_symbol, latest_entry=1, payment_date=payment_date, created_by=userid, actual_amount=actual_amount, discount=discount, renewal_date=pkg_renewal_date, product_amount=pkg_amount)
        sessions.add(inserted_pkg_pur)
        sessions.flush()
        pkg_pur_id = inserted_pkg_pur.pkg_pur_id

        # cursor.execute(f"INSERT into package_purchase_list (user_id,pkg_id,product_id,amount,currency_type,currency_symbol,latest_entry,payment_date,created_by,actual_amount,discount,renewal_date)values {(userid,pkg_id,pkg_product_id,pkg_amount,currency_type,currency_symbol,1,payment_date,userid,actual_amount,discount,pkg_renewal_date)} returning pkg_pur_id")
        # pkg_pur_id = cursor.fetchone()[0]

        inserted_pkg_pur_his = PackagePurchaseHistory(pkg_pur_id=pkg_pur_id,user_id=userid, pkg_id=pkg_id, product_id=pkg_product_id, amount=pkg_amount, currency_type=currency_type, currency_symbol=currency_symbol, latest_entry=1, payment_date=payment_date, created_by=userid, actual_amount=actual_amount, discount=discount, renewal_date=pkg_renewal_date, product_amount=pkg_amount)
        sessions.add(inserted_pkg_pur_his)
        sessions.flush()
        pkg_pur_his_id = inserted_pkg_pur_his.pkg_history_id

        # cursor.execute(f"INSERT into package_purchase_history (pkg_pur_id,user_id,pkg_id,product_id,amount,currency_type,currency_symbol,latest_entry,payment_date,created_by,actual_amount,discount,renewal_date)values {(pkg_pur_id,userid,pkg_id,pkg_product_id,pkg_amount,currency_type,currency_symbol,1,payment_date,userid,actual_amount,discount,pkg_renewal_date)} ")

        user_selc_list = sessions.query(UserSelectionList).with_entities(UserSelectionList.user_selc_id, UserSelectionList.admin_user_count, UserSelectionList.admin_user_amount, UserSelectionList.general_user_count, UserSelectionList.general_user_amount, UserSelectionList.limited_user_count, UserSelectionList.limited_user_amount, UserSelectionList.billing_frequency).filter(UserSelectionList.user_id==userid).order_by(UserSelectionList.user_selc_id.desc()).first()

        # cursor.execute(f"select user_selc_id,admin_user_count,admin_user_amount,general_user_count,general_user_amount,limited_user_count,limited_user_amount,billing_frequency from user_selection_list where user_id={userid} order by user_selc_id desc ")
        # user_selc_list = cursor.fetchone()
        admin_user_count = user_selc_list[1]
        admin_user_amount = user_selc_list[2]
        general_user_count = user_selc_list[3]
        general_user_amount = user_selc_list[4]
        limited_user_count = user_selc_list[5]
        limited_user_amount = user_selc_list[6]
        billing_frequency = user_selc_list[7]

        user_selc_list = sessions.query(UserType.user_type_id).order_by(UserType.user_type_id.asc()).all()

        # cursor.execute(f"select * from user_type order by user_type_id asc ")
        # user_selc_list = cursor.fetchall()
        admin_user_id = user_selc_list[0][0]
        general_user_id = user_selc_list[1][0]
        limited_user_id = user_selc_list[2][0]

        if reg_user_type == "F":
            user_renewal_datetime = current_date + relativedelta(months=3, days=-1)

        else:
            if billing_frequency == 'M':
                user_renewal_datetime = current_date + relativedelta(months=1, days=-1)
            else:
                user_renewal_datetime = current_date + relativedelta(years=1, days=-1)

        user_renewal_date = user_renewal_datetime.strftime('%Y-%m-%d')

        if admin_user_count != 0:
            inserted_usr_admin_pur = UserPurchaseList(user_id=userid,user_type_id=admin_user_id, no_of_users=admin_user_count, amount=admin_user_amount, currency_type=currency_type, currency_symbol=currency_symbol, latest_entry=1, payment_date=payment_date, created_by=userid, billing_frequency=billing_frequency, renewal_date=user_renewal_date, actual_no_of_users=admin_user_count, actual_amount=admin_user_amount)
            sessions.add(inserted_usr_admin_pur)
            sessions.flush()
            user_pur_admin_id = inserted_usr_admin_pur.user_pur_id

            inserted_usr_pur_admin_his = UserPurchaseHistory(user_pur_id=user_pur_admin_id,user_id=userid,user_type_id=admin_user_id, no_of_users=admin_user_count, amount=admin_user_amount, currency_type=currency_type, currency_symbol=currency_symbol, latest_entry=1, payment_date=payment_date, created_by=userid, billing_frequency=billing_frequency, renewal_date=user_renewal_date, actual_no_of_users=admin_user_count, actual_amount=admin_user_amount)
            sessions.add(inserted_usr_pur_admin_his)
            sessions.flush()
            admin_pur_his_id = inserted_usr_pur_admin_his.user_history_id
            
        else:
            inserted_usr_admin_pur = UserPurchaseList(user_id=userid,user_type_id=admin_user_id, no_of_users=0, amount=0, currency_type=currency_type, currency_symbol=currency_symbol, latest_entry=1, payment_date=payment_date, created_by=userid, billing_frequency=billing_frequency, renewal_date=user_renewal_date, actual_no_of_users=0, actual_amount=0)
            sessions.add(inserted_usr_admin_pur)
            sessions.flush()
            user_pur_admin_id = inserted_usr_admin_pur.user_pur_id

            inserted_usr_pur_admin_his = UserPurchaseHistory(user_pur_id=user_pur_admin_id,user_id=userid,user_type_id=admin_user_id, no_of_users=0, amount=0, currency_type=currency_type, currency_symbol=currency_symbol, latest_entry=1, payment_date=payment_date, created_by=userid, billing_frequency=billing_frequency, renewal_date=user_renewal_date, actual_no_of_users=0, actual_amount=0)
            sessions.add(inserted_usr_pur_admin_his)
            sessions.flush()
            admin_pur_his_id = inserted_usr_pur_admin_his.user_history_id

        if general_user_count != 0:
            inserted_usr_general_pur = UserPurchaseList(user_id=userid,user_type_id=general_user_id, no_of_users=general_user_count, amount=general_user_amount, currency_type=currency_type, currency_symbol=currency_symbol, latest_entry=1, payment_date=payment_date, created_by=userid, billing_frequency=billing_frequency, renewal_date=user_renewal_date, actual_no_of_users=general_user_count, actual_amount=general_user_amount)
            sessions.add(inserted_usr_general_pur)
            sessions.flush()
            user_pur_gen_id = inserted_usr_general_pur.user_pur_id

            inserted_usr_pur_gen_his = UserPurchaseHistory(user_pur_id=user_pur_gen_id,user_id=userid,user_type_id=general_user_id, no_of_users=general_user_count, amount=general_user_amount, currency_type=currency_type, currency_symbol=currency_symbol, latest_entry=1, payment_date=payment_date, created_by=userid, billing_frequency=billing_frequency, renewal_date=user_renewal_date, actual_no_of_users=general_user_count, actual_amount=general_user_amount)
            sessions.add(inserted_usr_pur_gen_his)
            sessions.flush()
            gen_pur_his_id = inserted_usr_pur_gen_his.user_history_id

        else:
            inserted_usr_general_pur = UserPurchaseList(user_id=userid,user_type_id=general_user_id, no_of_users=0, amount=0, currency_type=currency_type, currency_symbol=currency_symbol, latest_entry=1, payment_date=payment_date, created_by=userid, billing_frequency=billing_frequency, renewal_date=user_renewal_date, actual_no_of_users=0, actual_amount=0)
            sessions.add(inserted_usr_general_pur)
            sessions.flush()
            user_pur_gen_id = inserted_usr_general_pur.user_pur_id

            inserted_usr_pur_gen_his = UserPurchaseHistory(user_pur_id=user_pur_gen_id,user_id=userid,user_type_id=general_user_id, no_of_users=0, amount=0, currency_type=currency_type, currency_symbol=currency_symbol, latest_entry=1, payment_date=payment_date, created_by=userid, billing_frequency=billing_frequency, renewal_date=user_renewal_date, actual_no_of_users=0, actual_amount=0)
            sessions.add(inserted_usr_pur_gen_his)
            sessions.flush()
            gen_pur_his_id = inserted_usr_pur_gen_his.user_history_id

        if limited_user_count != 0:
            inserted_usr_lim_pur = UserPurchaseList(user_id=userid,user_type_id=limited_user_id, no_of_users=limited_user_count, amount=limited_user_amount, currency_type=currency_type, currency_symbol=currency_symbol, latest_entry=1, payment_date=payment_date, created_by=userid, billing_frequency=billing_frequency, renewal_date=user_renewal_date, actual_no_of_users=limited_user_count, actual_amount=limited_user_amount)
            sessions.add(inserted_usr_lim_pur)
            sessions.flush()
            user_pur_lim_id = inserted_usr_lim_pur.user_pur_id

            inserted_usr_pur_lim_his = UserPurchaseHistory(user_pur_id=user_pur_lim_id,user_id=userid,user_type_id=limited_user_id, no_of_users=limited_user_count, amount=limited_user_amount, currency_type=currency_type, currency_symbol=currency_symbol, latest_entry=1, payment_date=payment_date, created_by=userid, billing_frequency=billing_frequency, renewal_date=user_renewal_date, actual_no_of_users=limited_user_count, actual_amount=limited_user_amount)
            sessions.add(inserted_usr_pur_lim_his)
            sessions.flush()
            lim_pur_his_id = inserted_usr_pur_lim_his.user_history_id

        else:
            inserted_usr_lim_pur = UserPurchaseList(user_id=userid,user_type_id=limited_user_id, no_of_users=0, amount=0, currency_type=currency_type, currency_symbol=currency_symbol, latest_entry=1, payment_date=payment_date, created_by=userid, billing_frequency=billing_frequency, renewal_date=user_renewal_date, actual_no_of_users=0, actual_amount=0)
            sessions.add(inserted_usr_lim_pur)
            sessions.flush()
            user_pur_lim_id = inserted_usr_lim_pur.user_pur_id

            inserted_usr_pur_lim_his = UserPurchaseHistory(user_pur_id=user_pur_lim_id,user_id=userid,user_type_id=limited_user_id, no_of_users=0, amount=0, currency_type=currency_type, currency_symbol=currency_symbol, latest_entry=1, payment_date=payment_date, created_by=userid, billing_frequency=billing_frequency, renewal_date=user_renewal_date, actual_no_of_users=0, actual_amount=0)
            sessions.add(inserted_usr_pur_lim_his)
            sessions.flush()
            lim_pur_his_id = inserted_usr_pur_lim_his.user_history_id

        cloud_selc_list = sessions.query(CloudSelection).with_entities(CloudSelection.cloud_id, CloudSelection.cl_type_id,CloudSelection.amount).filter(CloudSelection.user_id==userid).order_by(CloudSelection.cloud_id.desc()).first()

        cl_type_id = cloud_selc_list[1]
        cloud_amount = cloud_selc_list[2]

        if reg_user_type == "F":
            cloud_renewal_datetime = current_date + relativedelta(months=3, days=-1)

        else:
            cloud_renewal_datetime = current_date + relativedelta(years=1, days=-1)
        cloud_renewal_date = cloud_renewal_datetime.strftime('%Y-%m-%d')

        inserted_cld_pur = CloudPurchaseList(user_id=userid, cloud_type_id=cl_type_id, amount=cloud_amount, currency_type=currency_type, currency_symbol=currency_symbol, latest_entry=1, payment_date=payment_date, created_by=userid, renewal_date=cloud_renewal_date, actual_amount=cloud_amount)
        sessions.add(inserted_cld_pur)
        sessions.flush()
        cloud_pur_id = inserted_cld_pur.cloud_pur_id

        inserted_cld_pur_his = CloudPurchaseHistory(cloud_pur_id=cloud_pur_id,user_id=userid, cloud_type_id=cl_type_id, amount=cloud_amount, currency_type=currency_type, currency_symbol=currency_symbol, latest_entry=1, payment_date=payment_date, created_by=userid, renewal_date=cloud_renewal_date, actual_amount=cloud_amount)
        sessions.add(inserted_cld_pur_his)
        sessions.flush()
        cloud_pur_his_id = inserted_cld_pur_his.cloud_history_id

        session['billing_count'] = 1
        usr_pur_his_id = str(admin_pur_his_id)+","+str(gen_pur_his_id)+","+str(lim_pur_his_id)
        inserted_pay_his = PaymentHistory(payment_date=payment_date, mode_of_payment='credit_card', amount=total_gst_amnt, transaction_details='1246566', user_id=userid, status=1, pkg_pur_his_id= pkg_pur_his_id, user_pur_his_id=usr_pur_his_id, cld_pur_his_id=cloud_pur_his_id,bill_no=new_bill_no,purchase_no=new_pur_no,bill_series_no=bill_num_val,purchase_series_no=pur_num_val)
        sessions.add(inserted_pay_his)
        sessions.flush()

        last_insert_pay_his_id = inserted_pay_his.payment_history_id

        card_no_val = '09764'
        card_no = encryptdata(card_no_val)
        cvv_no_val = '998'
        cvv_no = encryptdata(cvv_no_val)
        expiry_date_val = '04/20'
        expiry_date = encryptdata(expiry_date_val)

        inserted_pay_his = PaymentMode(mode_of_payment='credit_card', card_number=card_no, account_holder_name='scopiq', cvv=cvv_no, expiry_date=expiry_date, user_id=userid)
        sessions.add(inserted_pay_his)
        sessions.flush()

        #  inserting company,users,location in site admin and dms

        user_details = sessions.query(RegUsers).with_entities(RegUsers.first_name, RegUsers.email,RegUsers.password,RegUsers.last_name).filter(RegUsers.user_id==userid).first()
        # cursor.execute(
        #     f"select first_name,email,password,last_name from users where user_id={userid}")
        # user_details = cursor.fetchone()
        first_name = user_details[0]
        email = user_details[1]
        password = user_details[2]
        last_name = user_details[3]
        username = first_name + " " + last_name

        company_details = sessions.query(CompanyDetails).with_entities(CompanyDetails.company_id, CompanyDetails.company_name,CompanyDetails.address,CompanyDetails.email,CompanyDetails.country_id,CompanyDetails.state_id,CompanyDetails.city_id).filter(CompanyDetails.user_id==userid).first()
        # cursor.execute(
        #     f"select company_id,company_name,address,email,country_id,state_id,city_id from company_details where user_id={userid}")
        # company_details = cursor.fetchone()
        web_company_id = company_details[0]
        company_name = company_details[1]
        company_address = company_details[2]
        company_email = company_details[3]
        #  gst_or_vat=company_details[4]
        company_country = company_details[4]
        company_state = company_details[5]
        company_city = company_details[6]

        location_details = sessions.query(Location).with_entities(Location.location_id, Location.location_name).filter(Location.company_id==web_company_id).first()
        # cursor.execute(
        #     f"select location_id,location_name from location where company_id={web_company_id}")
        # location_details = cursor.fetchone()
        web_location_id = location_details[0]
        location_name = location_details[1]

        dynamic_table_name = "admin_"+str(web_company_id)+"_"+str(userid)
        
        insertsite_comp = Company(company_name=company_name,address=company_address, email=company_email, date_format=1, login_type=3, country_id=company_country, state_id=company_state, city_id=company_city, dynamic_table_name=dynamic_table_name,company_code=company_code)

        siteadmin_session_set.add(insertsite_comp)
        siteadmin_session_set.flush()

        insertsite_comp_history = CompanyHistory(company_name=company_name,address=company_address, email=company_email, date_format=1, login_type=3, country_id=company_country, state_id=company_state, city_id=company_city, dynamic_table_name=dynamic_table_name,company_code=company_code)
        
        siteadmin_session_set.add(insertsite_comp_history)
        siteadmin_session_set.flush()
        
        user_company_id = insertsite_comp.company_id

        # cursor1.execute(
        #     f"INSERT into company(company_name,address,email,date_format,login_type,country_id,state_id,city_id,dynamic_table_name) values {(company_name,company_address,company_email,1,1,company_country,company_state,company_city,dynamic_table_name)} returning company_id")
        # user_company_id = cursor1.fetchone()[0]

        insertsite_loc = LocationList(location_name=location_name, company_id=user_company_id, login_type=1, country_id=company_country, state_id=company_state, city_id=company_city)
        
        siteadmin_session_set.add(insertsite_loc)
        siteadmin_session_set.flush()
        
        user_location_id = insertsite_loc.location_id

        # cursor1.execute(
        #     f"INSERT into location(location_name,company_id,login_type,country_id,state_id,city_id) values {(location_name,user_company_id,1,company_country,company_state,company_city)} returning location_id")
        # user_location_id = cursor1.fetchone()[0]

        insertsite_user = Users(first_name=first_name, last_name=last_name, username=username, email=email, password_hash=password, sys_role=6, company_id=user_company_id, location_id=user_location_id, type_of_user=1, status=1,old_emp_id=0, company_code=company_code )
        
        siteadmin_session_set.add(insertsite_user)
        siteadmin_session_set.flush()
        
        siteadmin_user_id = insertsite_user.user_id

        # cursor1.execute(
        #     f"INSERT into users(first_name,last_name,username,email,password_hash,sys_role,company_id,location_id,type_of_user,status) values {(first_name,last_name,username,email,password,6,user_company_id,user_location_id,1,1)} returning user_id" )
        # siteadmin_user_id = cursor1.fetchone()[0]

        package_product_list = list(pkg_product_id.split(","))

        for pkg_product_id in package_product_list:
            product_id = encryptdata(pkg_product_id)

            insertsite_prod = Packages(user_id=siteadmin_user_id, product_id=product_id, link='localhost:5003', renewal_date=pkg_renewal_date)
            
            siteadmin_session_set.add(insertsite_prod)
            siteadmin_session_set.flush()
            
            insertsite_menu_role_list = MenuRolesList(user_id=siteadmin_user_id, product_id=pkg_product_id, role_ids = 5)
            
            siteadmin_session_set.add(insertsite_menu_role_list)
            siteadmin_session_set.flush()

            insertsite_menu_role_list_his = MenuRolesHistory(user_id=siteadmin_user_id, product_id=pkg_product_id, role_ids = 5)
            
            siteadmin_session_set.add(insertsite_menu_role_list_his)
            siteadmin_session_set.flush()

            # cursor1.execute(
            #     f"INSERT into package_list(user_id,product_id,link,renewal_date) values {(siteadmin_user_id, product_id,'localhost:5003',pkg_renewal_date )} ")

        # if admin_user_count != 0:
        admin_user_type = encryptdata(1)
        admin_count = encryptdata(admin_user_count)

        insertsite_adminuser = UserList(user_id=siteadmin_user_id, user_type_id=admin_user_type, no_of_users=admin_count, renewal_date=user_renewal_date)
        
        siteadmin_session_set.add(insertsite_adminuser)
        siteadmin_session_set.flush()

            # cursor1.execute(
            #     f"INSERT into user_list(user_id,user_type_id,no_of_users,renewal_date) values {(siteadmin_user_id, admin_user_type,admin_count,user_renewal_date )} ")

        # if general_user_count != 0:
        general_user_type = encryptdata(2)
        general_count = encryptdata(general_user_count)

        insertsite_genuser = UserList(user_id=siteadmin_user_id, user_type_id=general_user_type, no_of_users=general_count, renewal_date=user_renewal_date)
        
        siteadmin_session_set.add(insertsite_genuser)
        siteadmin_session_set.flush()
            # cursor1.execute(
            #     f"INSERT into user_list(user_id,user_type_id,no_of_users,renewal_date) values {(siteadmin_user_id,general_user_type,general_count,user_renewal_date )} ")

        # if limited_user_count != 0:
        limited_user_type = encryptdata(3)
        limited_count = encryptdata(limited_user_count)

        insertsite_limuser = UserList(user_id=siteadmin_user_id, user_type_id=limited_user_type, no_of_users=limited_count, renewal_date=user_renewal_date)
        
        siteadmin_session_set.add(insertsite_limuser)
        siteadmin_session_set.flush()
            # cursor1.execute(
            #     f"INSERT into user_list(user_id,user_type_id,no_of_users,renewal_date) values {(siteadmin_user_id,limited_user_type,limited_count,user_renewal_date )} ")

        cloudtype_id = encryptdata(cl_type_id)

        insertsite_cloud = CloudList(user_id=siteadmin_user_id, cloud_type_id=cloudtype_id , renewal_date=cloud_renewal_date)
        
        siteadmin_session_set.add(insertsite_cloud)
        siteadmin_session_set.flush()

        # cursor1.execute(
        #     f"INSERT into cloud_list(user_id,cloud_type_id,renewal_date) values {(siteadmin_user_id, cloudtype_id,cloud_renewal_date )} ")

        # cursor1.execute(f"INSERT into server(server_type,server_url,server_uname,server_pwd,server_port,company_id,location_id,server_status) values {(server_type,server_url,server_uname,server_password,server_port,user_company_id,user_location_id,1)} returning server_id")
        # user_server_id=cursor1.fetchone()[0]
        # connection1.commit()

        ins = dynamic_table.insert().values(user_name=username,email=email)
        conn = engine.connect()
        conn.execute(ins)


        # cursor.execute(
        #     f"INSERT into {dynamic_table_name} (user_name,email) values {(username,email)}")

        insertdms_comp = Company(company_id=user_company_id,company_name=company_name,address=company_address, email=company_email, date_format=1, country_id=company_country, state_id=company_state, city_id=company_city, login_type=1 ,company_code=company_code)
        
        dms_session_set.add(insertdms_comp)
        dms_session_set.flush()

        insertdms_loc = LocationList(location_id=user_location_id, location_name=location_name, company_id=user_company_id, login_type=1, country_id=company_country, state_id=company_state, city_id=company_city)
        
        dms_session_set.add(insertdms_loc)
        dms_session_set.flush()
        
        user_location_id = insertdms_loc.location_id

        insertdms_user = Users(user_id=siteadmin_user_id, first_name=first_name, last_name=last_name, username=username, email=email, password_hash=password, sys_role=6, company_id=user_company_id, location_id=user_location_id, type_of_user=1,login_sys_role=1, status=1, company_code=company_code)
        
        dms_session_set.add(insertdms_user)
        dms_session_set.flush()
        
        ################CMS########################
        insertcms_comp = Company(company_id=user_company_id,company_name=company_name,address=company_address, email=company_email, date_format=1, country_id=company_country, state_id=company_state, city_id=company_city, login_type=1 ,company_code=company_code)
        
        cms_session_set.add(insertcms_comp)
        cms_session_set.flush()

        insertcms_loc = LocationList(location_id=user_location_id, location_name=location_name, company_id=user_company_id, login_type=1, country_id=company_country, state_id=company_state, city_id=company_city)
        
        cms_session_set.add(insertcms_loc)
        cms_session_set.flush()
        
        user_location_id = insertcms_loc.location_id

        insertcms_user = Users(user_id=siteadmin_user_id, first_name=first_name, last_name=last_name, username=username, email=email, password_hash=password, sys_role=6, company_id=user_company_id, location_id=user_location_id, type_of_user=1,login_sys_role=1, status=1, company_code=company_code)
        
        cms_session_set.add(insertcms_user)
        cms_session_set.flush()
        ################CMS########################

        ################AMS########################
        insertams_comp = Company(company_id=user_company_id,company_name=company_name,address=company_address, email=company_email, date_format=1, country_id=company_country, state_id=company_state, city_id=company_city, login_type=1 ,company_code=company_code)
        
        ams_session_set.add(insertams_comp)
        ams_session_set.flush()

        insertams_loc = LocationList(location_id=user_location_id, location_name=location_name, company_id=user_company_id, login_type=1, country_id=company_country, state_id=company_state, city_id=company_city)
        
        ams_session_set.add(insertams_loc)
        ams_session_set.flush()
        
        user_location_id = insertams_loc.location_id

        insertams_user = Users(user_id=siteadmin_user_id, first_name=first_name, last_name=last_name, username=username, email=email, password_hash=password, sys_role=6, company_id=user_company_id, location_id=user_location_id, type_of_user=1,login_sys_role=1, status=1, company_code=company_code)
        
        ams_session_set.add(insertams_user)
        ams_session_set.flush()

         ################AMS########################

          ################KMS########################
        insertkms_comp = Company(company_id=user_company_id,company_name=company_name,address=company_address, email=company_email, date_format=1, country_id=company_country, state_id=company_state, city_id=company_city, login_type=1 ,company_code=company_code)
        
        kms_session_set.add(insertkms_comp)
        kms_session_set.flush()

        insertkms_loc = LocationList(location_id=user_location_id, location_name=location_name, company_id=user_company_id, login_type=1, country_id=company_country, state_id=company_state, city_id=company_city)
        
        kms_session_set.add(insertkms_loc)
        kms_session_set.flush()
        
        user_location_id = insertkms_loc.location_id

        insertkms_user = Users(user_id=siteadmin_user_id, first_name=first_name, last_name=last_name, username=username, email=email, password_hash=password, sys_role=6, company_id=user_company_id, location_id=user_location_id, type_of_user=1,login_sys_role=1, status=1, company_code=company_code)
        
        kms_session_set.add(insertkms_user)
        kms_session_set.flush()


        insert_userstatus = UserStatus(user_transfer=0,user_id=siteadmin_user_id,status=1,fin_year='2021-22')
        kms_session_set.add(insert_userstatus)
        kms_session_set.flush()

         ################KMS########################

          ################DSM########################
        insertdsm_comp = Company(company_id=user_company_id,company_name=company_name,address=company_address, email=company_email, date_format=1, country_id=company_country, state_id=company_state, city_id=company_city, login_type=1 ,company_code=company_code)
        
        dsm_session_set.add(insertdsm_comp)
        dsm_session_set.flush()

        insertdsm_loc = LocationList(location_id=user_location_id, location_name=location_name, company_id=user_company_id, login_type=1, country_id=company_country, state_id=company_state, city_id=company_city)
        
        dsm_session_set.add(insertdsm_loc)
        dsm_session_set.flush()
        
        user_location_id = insertdsm_loc.location_id

        insertdsm_user = Users(user_id=siteadmin_user_id, first_name=first_name, last_name=last_name, username=username, email=email, password_hash=password, sys_role=6, company_id=user_company_id, location_id=user_location_id, type_of_user=1,login_sys_role=1, status=1, company_code=company_code)
        
        dsm_session_set.add(insertdsm_user)
        dsm_session_set.flush()

         ################DSM########################

         ################SMS########################
        insertsms_comp = Company(company_id=user_company_id,company_name=company_name,address=company_address, email=company_email, date_format=1, country_id=company_country, state_id=company_state, city_id=company_city, login_type=1 ,company_code=company_code)
        
        sms_session_set.add(insertsms_comp)
        sms_session_set.flush()

        insertsms_loc = LocationList(location_id=user_location_id, location_name=location_name, company_id=user_company_id, login_type=1, country_id=company_country, state_id=company_state, city_id=company_city)
        
        sms_session_set.add(insertsms_loc)
        sms_session_set.flush()
        
        user_location_id = insertsms_loc.location_id

        insertsms_user = Users(user_id=siteadmin_user_id, first_name=first_name, last_name=last_name, username=username, email=email, password_hash=password, sys_role=6, company_id=user_company_id, location_id=user_location_id, type_of_user=1,login_sys_role=1, status=1, company_code=company_code)
        
        sms_session_set.add(insertsms_user)
        sms_session_set.flush()
        ################SMS########################


        ################CAMS########################
        
        insertcams_comp = Company(company_id=user_company_id,company_name=company_name,address=company_address, email=company_email, date_format=1, country_id=company_country, state_id=company_state, city_id=company_city, login_type=1 ,company_code=company_code)
        
        cams_session_set.add(insertcams_comp)
        cams_session_set.flush()

        insertcams_loc = LocationList(location_id=user_location_id, location_name=location_name, company_id=user_company_id, login_type=1, country_id=company_country, state_id=company_state, city_id=company_city)
        
        cams_session_set.add(insertcams_loc)
        cams_session_set.flush()
        
        user_location_id = insertcams_loc.location_id

        insertcams_user = Users(user_id=siteadmin_user_id, first_name=first_name, last_name=last_name, username=username, email=email, password_hash=password, sys_role=6, company_id=user_company_id, location_id=user_location_id, type_of_user=1,login_sys_role=1, status=1, company_code=company_code)
        
        cams_session_set.add(insertcams_user)
        cams_session_set.flush()

         ################CAMS########################


        ################CAPA########################
        
        insertcapa_comp = Company(company_id=user_company_id,company_name=company_name,address=company_address, email=company_email, date_format=1, country_id=company_country, state_id=company_state, city_id=company_city, login_type=1 ,company_code=company_code)
        
        capa_session_set.add(insertcapa_comp)
        capa_session_set.flush()

        insertcapa_loc = LocationList(location_id=user_location_id, location_name=location_name, company_id=user_company_id, login_type=1, country_id=company_country, state_id=company_state, city_id=company_city)
        
        capa_session_set.add(insertcapa_loc)
        capa_session_set.flush()
        
        user_location_id = insertcams_loc.location_id

        insertcapa_user = Users(user_id=siteadmin_user_id, first_name=first_name, last_name=last_name, username=username, email=email, password_hash=password, sys_role=6, company_id=user_company_id, location_id=user_location_id, type_of_user=1,login_sys_role=1, status=1, company_code=company_code)
        
        capa_session_set.add(insertcapa_user)
        capa_session_set.flush()

        ################CAMS########################


        # cursor2.execute(
        #     f"INSERT into users(user_id,first_name,last_name,username,email,password_hash,sys_role,company_id,location_id,type_of_user,status) values {(siteadmin_user_id,first_name,last_name,username,email,password,6,user_company_id,user_location_id,1,1)}" )

        #  cursor2.execute(f"INSERT into users(username,email,password_hash,sys_role,company_id,location_id) values {(username,email,password,6,user_company_id,user_location_id)}")
        #  cursor2.execute(f"INSERT into server(server_type,server_url,server_uname,server_pwd,server_port,company_id,location_id,server_status,add_or_edit) values {(server_type,server_url,server_uname,server_password,server_port,user_company_id,user_location_id,1,1)}")
        print("hi")

        sessions.query(ProductSelectionList).filter_by(user_id=userid).delete()
        sessions.query(UserSelectionList).filter_by(user_id=userid).delete()
        sessions.query(CloudSelection).filter_by(user_id=userid).delete()

        # cursor.execute(f"delete from product_selection_list where user_id={userid}")
        # cursor.execute(f"delete from user_selection_list where user_id={userid}")
        # cursor.execute(f"delete from cloud_selection where user_id={userid}")
            
        # connection.commit()
        
        # connection1.commit()
        # connection2.commit()


        ################################### 2-2-2022 ###################################
        
        for j in range(0,10):
            if j == 0:
                scopiq_web_db = 'azure_scopiq_web'
                insert_db_details = DbList(company_id=company_id, pdb_name=scopiq_web_db,status=1,sort_order=0,company_code=company_code)
            elif j == 1:
                insert_db_details = DbList(company_id=company_id, pdb_name=site_admin_db,status=1,sort_order=1,company_code=company_code)
            elif j == 2:
                insert_db_details = DbList(company_id=company_id, pdb_name=dms_db,status=1,sort_order=2,company_code=company_code)
            elif j == 3:
                insert_db_details = DbList(company_id=company_id, pdb_name=cms_db,status=1,sort_order=3,company_code=company_code)
            elif j == 4:
                insert_db_details = DbList(company_id=company_id, pdb_name=ams_db,status=1,sort_order=4,company_code=company_code)
            elif j == 5:
                insert_db_details = DbList(company_id=company_id, pdb_name=kms_db,status=1,sort_order=5,company_code=company_code)
            elif j == 6:
                insert_db_details = DbList(company_id=company_id, pdb_name=dsm_db,status=1,sort_order=6,company_code=company_code)
            elif j == 7:
                insert_db_details = DbList(company_id=company_id, pdb_name=sms_db,status=1,sort_order=7,company_code=company_code)
            elif j == 8:
                insert_db_details = DbList(company_id=company_id, pdb_name=cams_db,status=1,sort_order=8,company_code=company_code)
            elif j == 9:
                insert_db_details = DbList(company_id=company_id, pdb_name=capa_db,status=1,sort_order=9,company_code=company_code)  

            sessions.add(insert_db_details)
            sessions.flush()  

        ################################### 2-2-2022 ###################################


        sessions.commit()
        siteadmin_session_set.commit()
        dms_session_set.commit()
        cms_session_set.commit()
        ams_session_set.commit()
        kms_session_set.commit()
        dsm_session_set.commit()
        sms_session_set.commit()
        cams_session_set.commit()
        capa_session_set.commit()

        # return 'download'
        return last_insert_pay_his_id

    # except Exception as ex:
    #     connection.rollback()
    #     connection1.rollback()
    #     connection2.rollback()
    #     flash(str(ex))




def freetrial_billing_details(bill_no, invoice_company, gst_vat, invoice_address, country, state, city, userid,total_gst_amnt,company_id,location_id,new_bill_no,bill_num_val,new_pur_no,pur_num_val):
    reg_user_type = sessions.query(RegUsers.user_type).filter(RegUsers.user_id == userid).first()[0]
    email = session['email']

    site_admin_db = str("scopiq_site_admin_")+str(company_id)+"_"+str(location_id)
    dms_db = str("scopiq_dms_")+str(company_id)+"_"+str(location_id)
    cms_db = str("scopiq_cms_")+str(company_id)+"_"+str(location_id)
    ams_db = str("scopiq_ams_")+str(company_id)+"_"+str(location_id)
    kms_db = str("scopiq_kms_")+str(company_id)+"_"+str(location_id)
    dsm_db = str("scopiq_dsm_")+str(company_id)+"_"+str(location_id)
    sms_db = str("scopiq_sms_")+str(company_id)+"_"+str(location_id)
    
    sms_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+sms_db)
    dsm_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+dsm_db)
    kms_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+kms_db)
    ams_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+ams_db)
    cms_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+cms_db)
    dms_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+dms_db)
    siteadmin_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+site_admin_db)
    
    Base = declarative_base()
    siteadmin_session = sessionmaker(bind=siteadmin_engine)
    dms_session = sessionmaker(bind=dms_engine)
    cms_session = sessionmaker(bind=cms_engine)
    ams_session = sessionmaker(bind=ams_engine)
    kms_session = sessionmaker(bind=kms_engine)
    dsm_session = sessionmaker(bind=dsm_engine)
    sms_session = sessionmaker(bind=sms_engine)

    siteadmin_session_set = siteadmin_session()
    dms_session_set = dms_session()
    cms_session_set = cms_session()
    ams_session_set = ams_session()
    kms_session_set = kms_session()
    dsm_session_set = dsm_session()
    sms_session_set = sms_session()

    siteadmin_userid = siteadmin_session_set.query(Users.user_id).filter(Users.email==email).first()[0]

    sessions.query(BillingDetails).filter(BillingDetails.user_id == userid).update({BillingDetails.bill_no:bill_no, BillingDetails.user_id:userid, BillingDetails.invoice_company_name:invoice_company, BillingDetails.invoice_billing_address:invoice_address, BillingDetails.gst_no:gst_vat,BillingDetails.country_id:country, BillingDetails.state_id:state, BillingDetails.city_id:city})
    
    # inserted_billing = BillingDetails(bill_no=bill_no, user_id=userid, invoice_company_name=invoice_company, invoice_billing_address=invoice_address, gst_no=gst_vat, country_id=country, state_id=state, city_id=city)
    # sessions.add(inserted_billing)
    # sessions.flush()

    currency_type = session['currency']
    currency_symbol = session['currency_symbol']
    current_date = datetime.date(datetime.now())
    payment_date = current_date.strftime('%Y-%m-%d')
    
    '''select from temporary table'''
    prod_sel_list = sessions.query(ProductSelectionList).with_entities(ProductSelectionList.selc_id, ProductSelectionList.pkg_id, ProductSelectionList.product_id, ProductSelectionList.amount, ProductSelectionList.actual_amount, ProductSelectionList.discount).filter(ProductSelectionList.user_id==userid).order_by(ProductSelectionList.selc_id.desc()).first()

    pkg_id = prod_sel_list[1]
    pkg_product_id = prod_sel_list[2]
    pkg_amount = prod_sel_list[3]
    actual_amount = prod_sel_list[4]
    discount = prod_sel_list[5]

    amount = sessions.query(PackagePurchaseList).with_entities(PackagePurchaseList.amount, PackagePurchaseList.renewal_date).filter(PackagePurchaseList.user_id==userid).first()
    pkg_tot_amount = pkg_amount+amount[0]

    if reg_user_type == "F":
        product_renewal_date = current_date + relativedelta(years=1, days=-1)
        prod_renewal_date = product_renewal_date.strftime('%Y-%m-%d')
    else:
        product_renewal_date = amount[1]
        prod_renewal_date = product_renewal_date.strftime('%Y-%m-%d')

    '''update in permanent table(PackagePurchaseList)'''

    update_pkg = sessions.query(PackagePurchaseList).filter(PackagePurchaseList.user_id == userid).update({PackagePurchaseList.pkg_id: pkg_id, PackagePurchaseList.product_id: pkg_product_id,PackagePurchaseList.amount: pkg_tot_amount, PackagePurchaseList.currency_type: currency_type,PackagePurchaseList.currency_symbol: currency_symbol, PackagePurchaseList.latest_entry:1 , PackagePurchaseList.payment_date:payment_date ,PackagePurchaseList.created_by:userid ,PackagePurchaseList.renewal_date:prod_renewal_date, PackagePurchaseList.actual_amount:actual_amount, PackagePurchaseList.discount:discount})
    
    pkg_pur_id = sessions.query(PackagePurchaseList.pkg_pur_id).filter(PackagePurchaseList.user_id == userid).first()[0]

    inserted_pkg_pur_his = PackagePurchaseHistory(pkg_pur_id=pkg_pur_id,user_id=userid, pkg_id=pkg_id, product_id=pkg_product_id, amount=pkg_tot_amount, currency_type=currency_type, currency_symbol=currency_symbol, latest_entry=1, payment_date=payment_date, created_by=userid, actual_amount=actual_amount, discount=discount, renewal_date=prod_renewal_date, product_amount=pkg_amount)
    sessions.add(inserted_pkg_pur_his)
    sessions.flush()
    pkg_pur_his_id = inserted_pkg_pur_his.pkg_history_id


    sessions.query(ProductSelectionList).filter_by(user_id=userid).delete()

    package_product_list = list(pkg_product_id.split(","))

    siteadmin_session_set.query(Packages).filter_by(user_id=siteadmin_userid).delete()

    '''insert in siteadmin packages'''

    for pkg_product_id in package_product_list:
        product_id = encryptdata(pkg_product_id)

        insertsite_prod = Packages(user_id=siteadmin_userid, product_id=product_id, link='localhost:5003', renewal_date=prod_renewal_date)
        siteadmin_session_set.add(insertsite_prod)
        siteadmin_session_set.flush()
        
        check_count = siteadmin_session_set.query(MenuRolesList).filter(and_(MenuRolesList.user_id==siteadmin_userid, MenuRolesList.product_id==pkg_product_id)).count()

        if check_count == 0:

            insertsite_menu_role_list = MenuRolesList(user_id=siteadmin_userid,product_id=pkg_product_id, role_ids = 5)
            
            siteadmin_session_set.add(insertsite_menu_role_list)
            siteadmin_session_set.flush()

            insertsite_menu_role_list_his = MenuRolesHistory(user_id=siteadmin_userid, product_id=pkg_product_id, role_ids = 5)
            
            siteadmin_session_set.add(insertsite_menu_role_list_his)
            siteadmin_session_set.flush()

    '''select from temporary table'''

    user_selc_list = sessions.query(UserSelectionList).with_entities(UserSelectionList.user_selc_id, UserSelectionList.admin_user_count, UserSelectionList.admin_user_amount, UserSelectionList.general_user_count, UserSelectionList.general_user_amount, UserSelectionList.limited_user_count, UserSelectionList.limited_user_amount, UserSelectionList.billing_frequency).filter(UserSelectionList.user_id==userid).order_by(UserSelectionList.user_selc_id.desc()).first()

    admin_user_count = user_selc_list[1]
    admin_user_amount = user_selc_list[2]
    general_user_count = user_selc_list[3]
    general_user_amount = user_selc_list[4]
    limited_user_count = user_selc_list[5]
    limited_user_amount = user_selc_list[6]
    billing_frequency = user_selc_list[7]

    if billing_frequency == 'M':
        user_renewal_datetime = current_date + relativedelta(months=1, days=-1)
    else:
        user_renewal_datetime = current_date + relativedelta(years=1, days=-1)

    renewal_date = user_renewal_datetime.strftime('%Y-%m-%d')

    '''select admin user amount and update admin users in user purchase list '''

    admin_amount =  sessions.query(UserPurchaseList.amount).filter(UserPurchaseList.user_id==userid, UserPurchaseList.user_type_id == 1).first()[0]

    admin_user_tot_amount = float(admin_amount)+float(admin_user_amount)

    update_user = sessions.query(UserPurchaseList).filter(UserPurchaseList.user_id == userid, UserPurchaseList.user_type_id == 1).update({UserPurchaseList.no_of_users: admin_user_count, UserPurchaseList.amount: admin_user_tot_amount , UserPurchaseList.payment_date: payment_date , UserPurchaseList.billing_frequency: billing_frequency , UserPurchaseList.renewal_date: renewal_date})
    
    user_pur_admin_id = sessions.query(UserPurchaseList.user_pur_id).filter(UserPurchaseList.user_id == userid, UserPurchaseList.user_type_id == 1).first()[0]
    

    inserted_usr_pur_admin_his = UserPurchaseHistory(user_pur_id=user_pur_admin_id,user_id=userid,user_type_id=1, no_of_users=admin_user_count, amount=admin_user_tot_amount, currency_type=currency_type, currency_symbol=currency_symbol, latest_entry=1, payment_date=payment_date, created_by=userid, billing_frequency=billing_frequency, renewal_date=renewal_date,actual_no_of_users=admin_user_count, actual_amount=admin_user_amount)
    sessions.add(inserted_usr_pur_admin_his)
    sessions.flush()
    admin_pur_his_id = inserted_usr_pur_admin_his.user_history_id


    '''select general user amount and update general users in user purchase list '''

    gen_amount =  sessions.query(UserPurchaseList.amount).filter(UserPurchaseList.user_id==userid, UserPurchaseList.user_type_id ==2).first()[0]

    general_user_tot_amount = float(gen_amount)+float(general_user_amount)

    update_gen_user = sessions.query(UserPurchaseList).filter(UserPurchaseList.user_id == userid, UserPurchaseList.user_type_id == 2).update({UserPurchaseList.no_of_users: general_user_count, UserPurchaseList.amount: general_user_tot_amount , UserPurchaseList.payment_date: payment_date , UserPurchaseList.billing_frequency: billing_frequency , UserPurchaseList.renewal_date: renewal_date})
    
    user_pur_general_id = sessions.query(UserPurchaseList.user_pur_id).filter(UserPurchaseList.user_id == userid, UserPurchaseList.user_type_id == 2).first()[0]

    inserted_usr_pur_general_his = UserPurchaseHistory(user_pur_id=user_pur_general_id,user_id=userid,user_type_id=2, no_of_users=general_user_count, amount=general_user_tot_amount, currency_type=currency_type, currency_symbol=currency_symbol, latest_entry=1, payment_date=payment_date, created_by=userid, billing_frequency=billing_frequency, renewal_date=renewal_date,actual_no_of_users=general_user_count, actual_amount=general_user_amount)
    sessions.add(inserted_usr_pur_general_his)
    sessions.flush()
    gen_pur_his_id = inserted_usr_pur_general_his.user_history_id


    '''select limited user amount and update limited users in user purchase list '''

    lim_amount =  sessions.query(UserPurchaseList.amount).filter(UserPurchaseList.user_id==userid, UserPurchaseList.user_type_id ==3).first()[0]

    limited_user_tot_amount = float(lim_amount) + float(limited_user_amount)

    update_lim_user = sessions.query(UserPurchaseList).filter(UserPurchaseList.user_id == userid, UserPurchaseList.user_type_id == 3).update({UserPurchaseList.no_of_users: limited_user_count, UserPurchaseList.amount: limited_user_tot_amount , UserPurchaseList.payment_date: payment_date , UserPurchaseList.billing_frequency: billing_frequency , UserPurchaseList.renewal_date: renewal_date})
    
    user_pur_limited_id = sessions.query(UserPurchaseList.user_pur_id).filter(UserPurchaseList.user_id == userid, UserPurchaseList.user_type_id == 3).first()[0]

    inserted_usr_pur_lim_his = UserPurchaseHistory(user_pur_id=user_pur_limited_id,user_id=userid,user_type_id=3, no_of_users=limited_user_count, amount=limited_user_tot_amount, currency_type=currency_type, currency_symbol=currency_symbol, latest_entry=1, payment_date=payment_date, created_by=userid, billing_frequency=billing_frequency, renewal_date=renewal_date,actual_no_of_users=limited_user_count, actual_amount=limited_user_amount)
    sessions.add(inserted_usr_pur_lim_his)
    sessions.flush()
    lim_pur_his_id = inserted_usr_pur_lim_his.user_history_id

    sessions.query(UserSelectionList).filter_by(user_id=userid).delete()

    siteadmin_session_set.query(UserList).filter_by(user_id=siteadmin_userid).delete()


    usr_purchased_list = sessions.query(UserPurchaseList).with_entities(UserPurchaseList.user_type_id, UserPurchaseList.no_of_users).filter(UserPurchaseList.user_id == userid).all()

    '''insert in siteadmin userslist '''

    for usr_pur_list in usr_purchased_list:
        user_type_id = usr_pur_list[0]
        no_of_users = usr_pur_list[1]
        
        user_type = encryptdata(user_type_id)
        user_count = encryptdata(no_of_users)

        insertsite_user = UserList(user_id=siteadmin_userid, user_type_id=user_type, no_of_users=user_count, renewal_date=renewal_date)
        siteadmin_session_set.add(insertsite_user)
        siteadmin_session_set.flush()

    '''select cloud from temporary table'''

    cloud_selc_list = sessions.query(CloudSelection).with_entities(CloudSelection.cloud_id, CloudSelection.cl_type_id,CloudSelection.amount).filter(CloudSelection.user_id==userid).order_by(CloudSelection.cloud_id.desc()).first()

    cl_type_id = cloud_selc_list[1]
    cloud_amount = cloud_selc_list[2]

    '''select amount and update in permanent table'''

    amount = sessions.query(CloudPurchaseList).with_entities(CloudPurchaseList.amount, CloudPurchaseList.renewal_date).filter(CloudPurchaseList.user_id==userid).first()
    
    cloud_tot_amount = int(cloud_amount)+amount[0]

    if reg_user_type == "F":
        cld_renewal_date = current_date + relativedelta(years=1, days=-1)
        cloud_renewal_date = cld_renewal_date.strftime('%Y-%m-%d')
    
    else:
        cld_renewal_date = amount[1]
        cloud_renewal_date = cld_renewal_date.strftime('%Y-%m-%d')

    update_cloud = sessions.query(CloudPurchaseList).filter(CloudPurchaseList.user_id == userid).update({CloudPurchaseList.cloud_type_id: cl_type_id,CloudPurchaseList.amount: cloud_tot_amount, CloudPurchaseList.currency_type: currency_type,CloudPurchaseList.currency_symbol: currency_symbol, CloudPurchaseList.latest_entry:1 , CloudPurchaseList.payment_date:payment_date ,CloudPurchaseList.created_by:userid,CloudPurchaseList.renewal_date:cld_renewal_date})
    cloud_pur_id = sessions.query(CloudPurchaseList.cloud_pur_id).filter(CloudPurchaseList.user_id == userid).first()[0]

    inserted_cld_pur_his = CloudPurchaseHistory(cloud_pur_id=cloud_pur_id,user_id=userid, cloud_type_id=cl_type_id, amount=cloud_tot_amount, currency_type=currency_type, currency_symbol=currency_symbol, latest_entry=1, payment_date=payment_date, created_by=userid, renewal_date=cloud_renewal_date, actual_amount=cloud_amount)
    sessions.add(inserted_cld_pur_his)
    sessions.flush()
    cld_pur_his_id = inserted_cld_pur_his.cloud_history_id

    siteadmin_session_set.query(CloudList).filter_by(user_id=siteadmin_userid).delete()

    # cursor1.execute(f"delete from cloud_list where user_id='{siteadmin_userid}'")

    cloudtype_id = encryptdata(cl_type_id)

    insertsite_cloud = CloudList(user_id=siteadmin_userid, cloud_type_id=cloudtype_id , renewal_date=cloud_renewal_date)
    siteadmin_session_set.add(insertsite_cloud)
    siteadmin_session_set.flush()

    # cursor1.execute(
    #     f"INSERT into cloud_list(user_id,cloud_type_id,renewal_date) values {(siteadmin_userid, cloudtype_id,cloud_renewal_date )} ")

    sessions.query(CloudSelection).filter_by(user_id=userid).delete()

    session['billing_count'] = 1
    usr_pur_his_id = str(admin_pur_his_id)+","+str(gen_pur_his_id)+","+str(lim_pur_his_id)
    inserted_pay_his = PaymentHistory(payment_date=payment_date, mode_of_payment='credit_card', amount=total_gst_amnt, transaction_details='1246566', user_id=userid, status=1, pkg_pur_his_id= pkg_pur_his_id, user_pur_his_id=usr_pur_his_id, cld_pur_his_id=cld_pur_his_id,bill_no=new_bill_no,purchase_no=new_pur_no,bill_series_no=bill_num_val,purchase_series_no=pur_num_val)
    sessions.add(inserted_pay_his)
    sessions.flush()

    last_insert_pay_his_id = inserted_pay_his.payment_history_id

    card_no_val = '09764'
    card_no = encryptdata(card_no_val)
    cvv_no_val = '998'
    cvv_no = encryptdata(cvv_no_val)
    expiry_date_val = '04/20'
    expiry_date = encryptdata(expiry_date_val)

    inserted_pay_his = PaymentMode(mode_of_payment='credit_card', card_number=card_no, account_holder_name='scopiq', cvv=cvv_no, expiry_date=expiry_date, user_id=userid)
    sessions.add(inserted_pay_his)
    sessions.flush()
    sessions.query(RegUsers).filter(RegUsers.user_id == userid).update({RegUsers.user_type: 'P'})

    sessions.commit()
    siteadmin_session_set.commit()
    
    # return 'download'
    return last_insert_pay_his_id
