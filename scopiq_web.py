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
import pdfkit


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import cast
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from sqlalchemy import Table, Column, Integer, String, MetaData, DateTime, BigInteger, DECIMAL, and_, or_
from sqlalchemy.ext.declarative import declarative_base
from flask import *
from flask_mail import *
from flask import Flask, request, render_template, flash, redirect, url_for, session, abort
from werkzeug import security
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from psycopg2 import connect, extensions, sql
from apscheduler.scheduler import Scheduler
from flask import make_response

from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Protocol.KDF import PBKDF2
from collections import Counter
from db_configuration import *
from scopiq_web_functions import *
from db_configuration import sessions
from web_models import *

connection = db_configuration.connection()
cursor = connection.cursor()

connection1 = db_configuration.connection1()
cursor1 = connection1.cursor()

connection2 = db_configuration.connection2()
cursor2 = connection2.cursor()

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from models import *

metadata = MetaData()

site_admin = Blueprint('scopiq_web', __name__, template_folder="../templates/scopiq_web/")

with app.app_context():
    db1 = get_db_one()
    cursor = g.db0.cursor()
    db2 = get_db_two()
    cursor1 = g.db1.cursor()
    db3 = get_db_three()
    cursor2 = g.db2.cursor()

# Flask mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587

app.config['MAIL_USERNAME'] = 'dummytesting32@gmail.com'
app.config['MAIL_PASSWORD'] = 'Perpetua123'

# app.config['MAIL_USERNAME'] = 'kiruthikamurugesan90@gmail.com'
# app.config['MAIL_PASSWORD'] = 'kiruthikav'

# app.config['MAIL_USERNAME'] = 'sethupathi.t@perpetua.co.in'
# app.config['MAIL_PASSWORD'] = 'perpetua123'

# app.config['MAIL_USERNAME'] = 'kiruthika.m@perpetua.co.in'
# app.config['MAIL_PASSWORD'] = 'kirthiorange@5'

app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['SECRET_KEY'] = "random string"
# #instantiate the Mail class
mail = Mail(app)

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
print(actual_src_path,'actual_src_path')
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

cron = Scheduler(daemon=True)
# Explicitly kick off the background thread
cron.start()


''' cronjob function to send alert mail for package and users before renewal date '''


@cron.interval_schedule(hours=24)
def mail_remainder():
    alert_interval_annual_list = sessions.query(AlertIntervalList).with_entities(AlertIntervalList.alert_start_days, AlertIntervalList.renewal_alert_days).filter(AlertIntervalList.renewal_type=="A").first()

    annual_remainder_users = []
    mon_remainder_users = []

    alert_start_days_annual = alert_interval_annual_list[0]
    alert_interval_annual = - + alert_interval_annual_list[1]  # for decrementing values

    for alerts in range(alert_start_days_annual, 0, alert_interval_annual):  # range(start,stop,step)
        alert_period = alerts
        current_date = datetime.date(datetime.now())
        payment_date = current_date + relativedelta(days=alert_period)
        mail_user_pkgcount = sessions.query(PackagePurchaseList).filter(PackagePurchaseList.renewal_date == payment_date).count()
        # print(mail_user_pkgcount,"mail_user_pkgcount")

        if mail_user_pkgcount != 0:
            mail_remainder_user = sessions.query(PackagePurchaseList, RegUsers).with_entities(PackagePurchaseList.user_id, RegUsers.email , PackagePurchaseList.renewal_date).join(RegUsers, PackagePurchaseList.user_id == RegUsers.user_id).filter(PackagePurchaseList.renewal_date == payment_date,RegUsers.user_type == "P").all()
            # print(mail_remainder_user,"mail_remainder_user")

            # for mail_rem_user in mail_remainder_user:
            #     user_email = mail_rem_user[1]
            #     renewal_date = (mail_rem_user[2].strftime('%d-%m-%Y'))
            #     with app.app_context():
            #         msg = Message('Expire', sender='sneha.r@perpetua.co.in', recipients=[user_email])
            #         expiry_details = "Your Annual Pack will expire on " + str(renewal_date)
            #         msg.body = expiry_details
            #         msg.html = render_template('emails/alert_mail_remainder.html', expiry_details=expiry_details)
            #         mail.send(msg)


        else:
            mail_remainder_user = []

        annual_remainder_users = annual_remainder_users + mail_remainder_user
    # print(annual_remainder_users,"annual_remainder_users")

    alert_interval_monthly_list = sessions.query(AlertIntervalList).with_entities(AlertIntervalList.alert_start_days, AlertIntervalList.renewal_alert_days).filter(AlertIntervalList.renewal_type=="M").first()

    alert_start_days_monthly = alert_interval_monthly_list[0]
    alert_interval_monthly = - + alert_interval_monthly_list[1]  # for decrementing values


    for alerts in range(alert_start_days_monthly, 0, alert_interval_monthly):  # range(start,stop,step)
        alert_period = alerts
        current_date = datetime.date(datetime.now())
        payment_date = current_date + relativedelta(days=alert_period)
        mail_alert_user_count = sessions.query(UserPurchaseList).filter(UserPurchaseList.renewal_date == payment_date, UserPurchaseList.billing_frequency == "M").count()

        if mail_alert_user_count != 0:
            mail_remainder_user = sessions.query(UserPurchaseList, RegUsers).with_entities(UserPurchaseList.user_id, RegUsers.email , UserPurchaseList.renewal_date).join(RegUsers, UserPurchaseList.user_id == RegUsers.user_id).filter(UserPurchaseList.renewal_date == payment_date, UserPurchaseList.billing_frequency == "M",RegUsers.user_type == "P").all()

            for mail_rem_user in mail_remainder_user:
                user_email = mail_rem_user[1]
                renewal_date = (mail_rem_user[2].strftime('%d-%m-%Y'))
                with app.app_context():
                    msg = Message('Expire', sender='sneha.r@perpetua.co.in', recipients=[user_email])
                    expiry_details = "Your monthly package will expire on " + str(renewal_date)
                    msg.body = expiry_details
                    msg.html = render_template('emails/alert_mail_remainder.html', expiry_details=expiry_details)
                    mail.send(msg)

        else:
            mail_remainder_user = []

        mon_remainder_users = mon_remainder_users + mail_remainder_user

    # print(mon_remainder_users,"mon_remainder_users")
    all_users = annual_remainder_users + mon_remainder_users
    # print(all_users,"all_users")

    for mail_rem_user in all_users:
        user_email = mail_rem_user[1]
        renewal_date = (mail_rem_user[2].strftime('%d-%m-%Y'))
        with app.app_context():
            msg = Message('Expire', sender='sneha.r@perpetua.co.in', recipients=[user_email])
            expiry_details = "Your package will expire on " + str(renewal_date)
            msg.body = expiry_details
            msg.html = render_template('emails/alert_mail_remainder.html', expiry_details=expiry_details)
            mail.send(msg)


''' cronjob function to send alert mail for card expiry '''


@cron.interval_schedule(hours=24)
def card_expiry():
    payment_mode_details = sessions.query(PaymentMode, RegUsers).with_entities(PaymentMode.expiry_date, PaymentMode.user_id ,RegUsers.email ).join(RegUsers, PaymentMode.user_id == RegUsers.user_id).all()
    # print(payment_mode_details,"payment_mode_details")

    for payment_mode_det in payment_mode_details:
        email = payment_mode_det[2]
        expiry_date = payment_mode_det[0]

        expiry_date_decrypt = decrypt(expiry_date, passcr)

        decrypted_expiry_date = str(expiry_date_decrypt).replace("'", '').replace('b', '')

        expdate = "01/" + str(decrypted_expiry_date)

        exp = str(expdate).replace('/', '-')

        expiry_date_format = datetime.strptime(exp, '%d-%m-%y').date()

        expiry_format = expiry_date_format + relativedelta(months=-1)

        current_date = datetime.date(datetime.now())

        if current_date == expiry_format:

            with app.app_context():
                msg = Message('Expire', sender='sneha.r@perpetua.co.in', recipients=[email])
                expiry_details = "Your Card will expire in " + str(payment_mode_det[0])
                msg.body = expiry_details
                msg.html = render_template('emails/alert_mail_remainder.html', expiry_details=expiry_details)
                mail.send(msg)


''' cronjob function for auto renewal payment process.If payment status is true,update all info in permanent tables else insert in new table '''

@cron.interval_schedule(hours=24)
def payment_renewal():
    print('Entered Payment Renewal')
    current_date = datetime.date(datetime.now())
    print(current_date,'current_date')

    ''' auto renewal if user billing is monthly '''

    payamount_monthly_user_id = sessions.query(UserPurchaseList).with_entities(UserPurchaseList.user_id.distinct()).filter(UserPurchaseList.billing_frequency=='M' , UserPurchaseList.renewal_date == current_date)
    # print(payamount_monthly_user_id,"payamount_monthly_user_id")

    for payment_monthly_user_id in payamount_monthly_user_id:
        pay_monthly_user_id = payment_monthly_user_id[0]
        user_email = sessions.query(RegUsers.email).filter(RegUsers.user_id == pay_monthly_user_id,RegUsers.user_type == "P").first()[0]
        company_id = sessions.query(CompanyDetails.company_id).filter(CompanyDetails.user_id == pay_monthly_user_id).first()[0]

        dynamic_table_name = sessions.query(CompanyDetails.dynamic_table_name).filter(CompanyDetails.user_id == pay_monthly_user_id).first()[0]
        print(dynamic_table_name,'dynamic_table_name')

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
        cams_db = str("scopiq_cams_")+str(company_id)+"_"+str(location_id)
        capa_db = str("scopiq_capa_")+str(company_id)+"_"+str(location_id)


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


        siteadmin_userid = siteadmin_session_set.query(Users.user_id).filter(Users.email==user_email).first()[0]

        get_gst_count = sessions.query(Gst, CompanyDetails ).with_entities(Gst.gst_per).join(CompanyDetails, Gst.country_id == CompanyDetails.country_id).filter(CompanyDetails.user_id==pay_monthly_user_id,Gst.effective_from_date <= current_date).count()
        if get_gst_count > 0:
            gst_percent = sessions.query(Gst, CompanyDetails ).with_entities(Gst.gst_per).join(CompanyDetails, Gst.country_id == CompanyDetails.country_id).filter(CompanyDetails.user_id==pay_monthly_user_id,Gst.effective_from_date <= current_date).order_by(Gst.gst_id.desc()).first()[0]
        else:
            gst_percent = "0%"

        # gst_percent = sessions.query(Gst, CompanyDetails ).with_entities(Gst.gst_per).join(CompanyDetails, Gst.country_id == CompanyDetails.country_id).filter(CompanyDetails.user_id==pay_monthly_user_id).first()[0]

        alert_table_count = sessions.query(AlertUserPurchase).filter(AlertUserPurchase.user_id == pay_monthly_user_id).count()

        if alert_table_count == 0:
            user_monthly_amount = sessions.query(UserPurchaseList).with_entities(func.sum(UserPurchaseList.amount.cast(DECIMAL)).label('amount')).filter(UserPurchaseList.user_id == pay_monthly_user_id).first()[0]

            user_packages_amount_monthly = float(user_monthly_amount) + float(user_monthly_amount) * (float(gst_percent.strip('%'))/100)

        else:  # in alert table
            user_monthly_amount = sessions.query(AlertUserPurchase).with_entities(func.sum(AlertUserPurchase.amount.cast(DECIMAL)).label('amount')).filter(AlertUserPurchase.user_id == pay_monthly_user_id).first()[0]

            update_usr_billing_freq = sessions.query(AlertUserPurchase.billing_frequency).filter(AlertUserPurchase.user_id==pay_monthly_user_id).first()[0]

            if update_usr_billing_freq == "M":
                user_packages_amount_monthly = float(user_monthly_amount) + (float(user_monthly_amount) * (float(gst_percent.strip('%'))/100))

            else:
                date_1 = current_date
                date_2 = sessions.query(PackagePurchaseList.renewal_date).filter(PackagePurchaseList.user_id==pay_monthly_user_id).first()[0]
                print(date_2,'date_2')

                remaining_months = alert_period(date_2,date_1)
                print(remaining_months,'remaining_months')

                no_of_months = remaining_months[0]['months']
                print(no_of_months,'remaining_months')

                user_annual_remaining_amount = float(user_monthly_amount) * float(no_of_months)
                print(user_annual_remaining_amount,'user_annual_remaining_amount')

                user_packages_amount_monthly = float(user_annual_remaining_amount) + (float(user_annual_remaining_amount) * (float(gst_percent.strip('%'))/100))
                print(user_packages_amount_monthly,'user_packages_amount_monthly')

        payment_status = True

        if payment_status is True:
            pkg_pur_his_id = 0
            usr_pur_his_id = ''
            cld_pur_his_id = 0

            if alert_table_count == 0:

                get_existing_details = sessions.query(UserPurchaseList).filter(UserPurchaseList.user_id == payment_user_id, UserPurchaseList.billing_frequency=='M').all()
                for existng_data in get_existing_details:
                    typeid = existng_data.user_type_id
                    noofusers = existng_data.no_of_users
                    amtval = existng_data.amount

                    updateduser = sessions.query(UserPurchaseList).filter(UserPurchaseList.user_id == payment_user_id,UserPurchaseList.user_type_id==typeid).update({ UserPurchaseList.actual_no_of_users:noofusers, UserPurchaseList.actual_amount:amtval})

                user_renewal_datetime = current_date + relativedelta(months=1, days=-1)
                updated_user = sessions.query(UserPurchaseList).filter(UserPurchaseList.user_id == pay_monthly_user_id).update({ UserPurchaseList.payment_date:current_date, UserPurchaseList.renewal_date:user_renewal_datetime  })

                usr_purchased_list = sessions.query(UserPurchaseList).with_entities(UserPurchaseList.user_type_id, UserPurchaseList.no_of_users).filter(UserPurchaseList.user_id==pay_monthly_user_id).all()

                ''' insert Users list in siteadmin  '''

                siteadmin_session_set.query(UserList).filter_by(user_id=siteadmin_userid).delete()

                for usr_pur_list in usr_purchased_list:
                    user_type_id = usr_pur_list[0]
                    no_of_users = usr_pur_list[1]

                    user_type = encryptdata(user_type_id)
                    user_count = encryptdata(no_of_users)
                    # print(user_count,"user_count")

                    insert_userslist = UserList(user_id=siteadmin_userid, user_type_id=user_type, no_of_users=user_count, renewal_date=user_renewal_datetime)
                    siteadmin_session_set.add(insert_userslist)
                    siteadmin_session_set.flush()

            else:  # in alert table
                # adminuser_before_billing = sessions.query(UserPurchaseList.no_of_users).filter(UserPurchaseList.user_id == pay_monthly_user_id, UserPurchaseList.user_type_id == 1).first()[0]

                # generaluser_before_billing = sessions.query(UserPurchaseList.no_of_users).filter(UserPurchaseList.user_id == pay_monthly_user_id, UserPurchaseList.user_type_id == 2).first()[0]

                # limiteduser_before_billing = sessions.query(UserPurchaseList.no_of_users).filter(UserPurchaseList.user_id == pay_monthly_user_id, UserPurchaseList.user_type_id == 3).first()[0]

                update_usr_purchase = sessions.query(AlertUserPurchase).with_entities(AlertUserPurchase.user_pur_id, AlertUserPurchase.user_id , AlertUserPurchase.user_type_id , AlertUserPurchase.no_of_users , AlertUserPurchase.amount , AlertUserPurchase.currency_type, AlertUserPurchase.currency_symbol , AlertUserPurchase.latest_entry , AlertUserPurchase.payment_date , AlertUserPurchase.renewal_date , AlertUserPurchase.billing_frequency).filter(AlertUserPurchase.user_id==pay_monthly_user_id).all()

                update_usr_billing_freq = sessions.query(AlertUserPurchase.billing_frequency).filter(AlertUserPurchase.user_id==pay_monthly_user_id).first()[0]

                if update_usr_billing_freq == "A":
                    usr_renewal_date = sessions.query(PackagePurchaseList.renewal_date).filter(PackagePurchaseList.user_id==pay_monthly_user_id).first()[0]
                else:
                    usr_renewal_date = current_date + relativedelta(months=1, days=-1)

                for update_usr_pur in update_usr_purchase:
                    sessions.query(UserPurchaseList).filter(UserPurchaseList.user_id==pay_monthly_user_id, update_usr_pur[1]==pay_monthly_user_id, UserPurchaseList.user_type_id == update_usr_pur[2]).update({UserPurchaseList.user_id: update_usr_pur[1], UserPurchaseList.user_type_id: update_usr_pur[2], UserPurchaseList.no_of_users: update_usr_pur[3], UserPurchaseList.amount: update_usr_pur[4],UserPurchaseList.currency_type: update_usr_pur[5], UserPurchaseList.currency_symbol: update_usr_pur[6],UserPurchaseList.latest_entry: update_usr_pur[7], UserPurchaseList.payment_date: current_date,UserPurchaseList.renewal_date: usr_renewal_date, UserPurchaseList.billing_frequency: update_usr_pur[10],UserPurchaseList.actual_no_of_users:update_usr_pur[3], UserPurchaseList.actual_amount:update_usr_pur[4]  })

                ''' insert Users list in siteadmin  '''

                siteadmin_session_set.query(UserList).filter_by(user_id=siteadmin_userid).delete()

                usr_purchased_list = sessions.query(AlertUserPurchase).with_entities(AlertUserPurchase.user_type_id, AlertUserPurchase.no_of_users).filter(AlertUserPurchase.user_id==pay_monthly_user_id).all()

                for usr_pur_list in usr_purchased_list:
                    user_type_id = usr_pur_list[0]
                    no_of_users = usr_pur_list[1]

                    user_type = encryptdata(user_type_id)
                    user_count = encryptdata(no_of_users)
                    # print(user_count,"user_count")

                    insert_userslist = UserList(user_id=siteadmin_userid, user_type_id=user_type, no_of_users=user_count, renewal_date=usr_renewal_date)
                    siteadmin_session_set.add(insert_userslist)
                    siteadmin_session_set.flush()

                    ''' no of users based on user type in siteadmin '''

                    siteadmin_users_count = siteadmin_session_set.query(Users).filter(Users.type_of_user == str(user_type_id)).count()
                    # print(siteadmin_users_count,"siteadmin_users_count")

                    if siteadmin_users_count > no_of_users:
                        # if user_type_id == 1:
                        #     to_delete_users = adminuser_before_billing - no_of_users

                        # elif user_type_id == 2:
                        #     to_delete_users = generaluser_before_billing - no_of_users

                        # elif user_type_id == 3:
                        #     to_delete_users = limiteduser_before_billing - no_of_users

                        delete_users_count = siteadmin_session_set.query(Users.user_id).filter(Users.type_of_user == str(user_type_id)).count()

                        siteadmin_deleteusers_count = delete_users_count - no_of_users
                        if siteadmin_deleteusers_count > 0:
                            delete_users = siteadmin_session_set.query(Users.user_id).filter(Users.type_of_user == str(user_type_id)).order_by(Users.user_id.desc()).limit(siteadmin_deleteusers_count).all()
                            for delete_users in delete_users:
                                print(delete_users[0],'delete_users[0]')
                                siteadmin_session_set.query(Users).filter(Users.user_id == delete_users[0]).delete()

                                 # dms
                                dms_session_set.query(Users).filter(Users.user_id == delete_users[0]).delete()
                                # cms
                                cms_session_set.query(Users).filter(Users.user_id == delete_users[0]).delete()
                                # ams
                                ams_session_set.query(Users).filter(Users.user_id == delete_users[0]).delete()
                                # kms
                                kms_session_set.query(Users).filter(Users.user_id == delete_users[0]).delete()
                                #dsm
                                dsm_session_set.query(Users).filter(Users.user_id == delete_users[0]).delete()

                                # only if admin users are downgraded, delete from website dynamic table
                                if user_type_id == 1:
                                    cursor.execute(f"delete from {dynamic_table_name} WHERE user_id={delete_users[0]}")
                                    db1.commit()

                        siteadmin_session_set.query(Alert_notify_list).filter(Alert_notify_list.type_id == 1).delete()

                        # fetch users who are changed from admin users to other type of users.
                        if user_type_id == 1:
                            initial_admin_users_count = siteadmin_session_set.query(Users.user_id).filter(Users.initial_type_of_user == "1",Users.type_of_user != "1").count()

                            if initial_admin_users_count > 0:

                                fetch_users_lists = siteadmin_session_set.query(Users.user_id,Users.type_of_user).filter(Users.initial_type_of_user == str(user_type_id),Users.type_of_user != str(user_type_id)).all()

                                for fetched_user_data in fetch_users_lists:
                                    fetched_user_id = fetched_user_data[0]
                                    fetched_type_of_user_val = fetched_user_data[1]

                                    siteadmin_session_set.query(Users).filter(Users.user_id==fetched_user_id).update({Users.initial_type_of_user: fetched_type_of_user_val})
                                    # dms
                                    dms_session_set.query(Users).filter(Users.user_id==fetched_user_id).update({Users.initial_type_of_user: fetched_type_of_user_val})
                                    # cms
                                    cms_session_set.query(Users).filter(Users.user_id==fetched_user_id).update({Users.initial_type_of_user: fetched_type_of_user_val})
                                    # ams
                                    ams_session_set.query(Users).filter(Users.user_id==fetched_user_id).update({Users.initial_type_of_user: fetched_type_of_user_val})
                                    # kms
                                    kms_session_set.query(Users).filter(Users.user_id==fetched_user_id).update({Users.initial_type_of_user: fetched_type_of_user_val})
                                    # dsm
                                    dsm_session_set.query(Users).filter(Users.user_id==fetched_user_id).update({Users.initial_type_of_user: fetched_type_of_user_val}) 

                                    cursor.execute(f"delete from {dynamic_table_name} WHERE user_id={fetched_user_id}")
                                    db1.commit()


            select_usr_purchase = sessions.query(UserPurchaseList).with_entities(UserPurchaseList.user_pur_id, UserPurchaseList.user_id , UserPurchaseList.user_type_id , UserPurchaseList.no_of_users , UserPurchaseList.amount , UserPurchaseList.currency_type, UserPurchaseList.currency_symbol , UserPurchaseList.latest_entry , UserPurchaseList.payment_date , UserPurchaseList.renewal_date , UserPurchaseList.billing_frequency,UserPurchaseList.actual_no_of_users, UserPurchaseList.actual_amount).filter(UserPurchaseList.user_id==pay_monthly_user_id).all()

            for select_usr_pur in select_usr_purchase:
                inserted_usr_pur_his = UserPurchaseHistory(user_pur_id=select_usr_pur[0], user_id=select_usr_pur[1], user_type_id=select_usr_pur[2], no_of_users=select_usr_pur[3], amount=select_usr_pur[4],currency_type=select_usr_pur[5], currency_symbol=select_usr_pur[6],latest_entry=select_usr_pur[7], payment_date=select_usr_pur[8],renewal_date=select_usr_pur[9], billing_frequency=select_usr_pur[10], actual_no_of_users=select_usr_pur[11],actual_amount=select_usr_pur[12] )
                sessions.add(inserted_usr_pur_his)
                sessions.flush()
                if usr_pur_his_id == '':
                    usr_pur_his_id = str(inserted_usr_pur_his.user_history_id)
                else:
                    usr_pur_his_id = str(usr_pur_his_id) + ',' + str(inserted_usr_pur_his.user_history_id)

            sessions.query(AlertUserPurchase).filter_by(user_id=pay_monthly_user_id).delete()
            print(usr_pur_his_id,"usr_pur_his_id")

            get_bill_details = get_bill_no()
            bill_no = get_bill_details[0]['bill_no']
            pur_no = get_bill_details[0]['pur_no']
            bill_num_val = get_bill_details[0]['bill_num_val']
            pur_num_val = get_bill_details[0]['pur_num_val']

            inserted_pay_his = PaymentHistory(payment_date=current_date, mode_of_payment='credit_card', amount=user_packages_amount_monthly, transaction_details='1246566', user_id=pay_monthly_user_id, status=1, pkg_pur_his_id= pkg_pur_his_id, user_pur_his_id=usr_pur_his_id, cld_pur_his_id=cld_pur_his_id,bill_no=bill_no,purchase_no=pur_no,bill_series_no=bill_num_val,purchase_series_no=pur_num_val,payment_type="AM")
            sessions.add(inserted_pay_his)
            sessions.flush()

            card_no_val = '09764'
            card_no = encryptdata(card_no_val)
            cvv_no_val = '998'
            cvv_no = encryptdata(cvv_no_val)
            expiry_date_val = '04/20'
            expiry_date = encryptdata(expiry_date_val)

            inserted_pay_his = PaymentMode(mode_of_payment='credit_card', card_number=card_no, account_holder_name='scopiq', cvv=cvv_no, expiry_date=expiry_date, user_id=pay_monthly_user_id)
            sessions.add(inserted_pay_his)
            sessions.flush()

            sessions.commit()
            siteadmin_session_set.commit()
            dms_session_set.commit()
            cms_session_set.commit()
            ams_session_set.commit()
            kms_session_set.commit()
            dsm_session_set.commit()

            user_email = sessions.query(RegUsers.email).filter(RegUsers.user_id == pay_monthly_user_id).first()[0]

            with app.app_context():
                msg = Message('Payment Information', sender='sneha.r@perpetua.co.in', recipients=[user_email])
                message = "Your Monthly payment was Successful"
                msg.body = message
                msg.html = render_template('emails/alert_mail_remainder.html', expiry_details=message)
                mail.send(msg)


        elif payment_status is not True:
            card_no_val = '09764'
            card_no = encryptdata(card_no_val)
            cvv_no_val = '998'
            cvv_no = encryptdata(cvv_no_val)
            expiry_date_val = '04/20'
            expiry_date = encryptdata(expiry_date_val)

            alert_days_monthly = sessions.query(AlertIntervalList.alert_start_days).filter(AlertIntervalList.renewal_type == "BM").first()[0]
            to_date = current_date + relativedelta(days=alert_days_monthly)
            # print(to_date,"to_date")

            inserted_pay_status = PaymentStatus(user_id=pay_monthly_user_id,mode_of_payment='credit_card', card_number=card_no, account_holder_name='scopiq', amount=user_packages_amount_monthly, from_date=current_date, to_date=to_date, payment_type="M")
            sessions.add(inserted_pay_his)
            sessions.flush()
            sessions.commit()

            user_email = sessions.query(RegUsers.email).filter(RegUsers.user_id == pay_monthly_user_id).first()[0]

            with app.app_context():
                msg = Message('Payment Information', sender='sneha.r@perpetua.co.in', recipients=[user_email])
                message = "Your payment was failed"
                msg.body = message
                msg.html = render_template('emails/alert_mail_remainder.html', expiry_details=message)
                mail.send(msg)

    ''' auto renewal if package,user,cloud billing is annual '''

    payamount_annual_user_id = sessions.query(PackagePurchaseList).with_entities(PackagePurchaseList.user_id).filter( PackagePurchaseList.renewal_date == current_date).all()
    # print(payamount_annual_user_id,"payamount_annual_user_id")


    for payment_user_id in payamount_annual_user_id:
        payment_user_id = payment_user_id[0]
        user_email = sessions.query(RegUsers.email).filter(RegUsers.user_id == payment_user_id,RegUsers.user_type == "P").first()[0]
        company_id = sessions.query(CompanyDetails.company_id).filter(CompanyDetails.user_id == payment_user_id).first()[0]

        dynamic_table_name = sessions.query(CompanyDetails.dynamic_table_name).filter(CompanyDetails.user_id == payment_user_id).first()[0]
        print(dynamic_table_name,'dynamic_table_name Annual')

        location_list = sessions.query(Location).with_entities(Location.location_id,Location.location_name).filter(Location.company_id == company_id).first()
        location_id = location_list[0]
        location_name = location_list[1]

        site_admin_db = str("scopiq_site_admin_")+str(company_id)+"_"+str(location_id)
        dms_db = str("scopiq_dms_")+str(company_id)+"_"+str(location_id)
        cms_db = str("scopiq_cms_")+str(company_id)+"_"+str(location_id)
        ams_db = str("scopiq_ams_")+str(company_id)+"_"+str(location_id)
        kms_db = str("scopiq_kms_")+str(company_id)+"_"+str(location_id)
        dsm_db = str("scopiq_dsm_")+str(company_id)+"_"+str(location_id)
        
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

        siteadmin_session_set = siteadmin_session()
        dms_session_set = dms_session()
        cms_session_set = cms_session()
        ams_session_set = ams_session()
        kms_session_set = kms_session()
        dsm_session_set = dsm_session()
        
        siteadmin_userid = siteadmin_session_set.query(Users.user_id).filter(Users.email==user_email).first()[0]

        get_gst_count = sessions.query(Gst, CompanyDetails ).with_entities(Gst.gst_per).join(CompanyDetails, Gst.country_id == CompanyDetails.country_id).filter(CompanyDetails.user_id==payment_user_id,Gst.effective_from_date <= current_date).count()

        if get_gst_count > 0:
            gst_percent = sessions.query(Gst, CompanyDetails ).with_entities(Gst.gst_per).join(CompanyDetails, Gst.country_id == CompanyDetails.country_id).filter(CompanyDetails.user_id==payment_user_id,Gst.effective_from_date <= current_date).order_by(Gst.gst_id.desc()).first()[0]
        else:
            gst_percent = "0%"

        
        # gst_percent = sessions.query(Gst, CompanyDetails ).with_entities(Gst.gst_per).join(CompanyDetails, Gst.country_id == CompanyDetails.country_id).filter(CompanyDetails.user_id==payment_user_id).first()[0]

        alert_pkg_table_count = sessions.query(AlertPackagePurchase).filter(AlertPackagePurchase.user_id == payment_user_id).count()

        alert_cloud_table_count = sessions.query(AlertCloudPurchase).filter(AlertCloudPurchase.user_id == payment_user_id).count()

        pkg_renewal_datetime = current_date + relativedelta(years=1, days=-1)

        ''' get packages billing amount by checking in package alert table '''

        if alert_pkg_table_count == 0:
            next_pkg = sessions.query(PackagePurchaseList).with_entities(PackagePurchaseList.pkg_id,PackagePurchaseList.product_id).filter(PackagePurchaseList.user_id == payment_user_id).first()
            pkg_id = next_pkg[0]
            prod_id = next_pkg[1]
            currency_type = sessions.query(PackagePurchaseList.currency_type).filter(PackagePurchaseList.user_id == payment_user_id).first()[0]
            currency = currency_type.lower()
            if pkg_id != 4: # pkg amount if its is packages
                next_pkg = sessions.query(PackagePurchaseList,PackageList).with_entities(PackagePurchaseList.pkg_id,getattr(PackageList,currency).label('package_amount')).join(PackageList, PackageList.pkg_id == PackagePurchaseList.pkg_id).filter(PackagePurchaseList.user_id == payment_user_id).first()
                pkg_amount = next_pkg[1]
                # pkg_amount = sessions.query(PackagePurchaseList.amount).filter(PackagePurchaseList.user_id == payment_user_id).first()[0]
            else: # check the products are within the packages and calculate amount
                # pkg_amount = next_billing_customize(prod_id)
                allVals = prod_id

                if allVals != '""':
                    newvalue = str(allVals).replace("'", "").replace('"', "")
                    li = list(newvalue.split(","))
                    list_count = len(li)
                    
                    amount_list = []
                    sub_lists = ''
                    pkg_amount = 0
                    effective_date = sessions.query(PackageList.effective_date).first()[0]
                    current_date = datetime.date(datetime.now())

                    if effective_date <= current_date:
                        customize_amount = sessions.query(PackageList).with_entities(getattr(PackageList,currency).label('package_amount')).filter_by(pkg_id=4).first()[0]
                        # cursor.execute(
                        #     f"select {currency} as package_amount from package_list where pkg_id=4 ")
                        # customize_amount = cursor.fetchone()[0]
                        total_customize_amount = list_count*customize_amount

                        all_product_id = sessions.query(PackageList).with_entities(PackageList.product_id,PackageList.pkg_id, getattr(PackageList,currency)).filter(PackageList.pkg_id!=4, PackageList.pkg_id!=5).order_by(PackageList.pkg_id.asc()).all()
                        # cursor.execute(
                        #     f"select product_id,pkg_id,{currency} from package_list where pkg_id!=4 order by pkg_id asc")
                        # all_product_id = cursor.fetchall()
                    else:
                        customize_amount = sessions.query(PackageListHistory).with_entities(getattr(PackageListHistory,currency).label('package_amount')).filter_by(pkg_id=4).filter(PackageListHistory.effective_date <= current_date ).first()[0]
                        total_customize_amount = list_count*customize_amount

                        prod_id_count = sessions.query(PackageList).filter(PackageList.pkg_id!=4).count()

                        all_product_id = sessions.query(PackageListHistory).with_entities(PackageListHistory.product_id,PackageListHistory.pkg_id, getattr(PackageListHistory,currency)).filter(PackageListHistory.pkg_id!=4, PackageListHistory.pkg_id!=5).filter(PackageListHistory.effective_date <= current_date ).order_by(PackageListHistory.pkg_his_id.desc()).limit(prod_id_count).all()
                        all_product_id.sort(key = lambda x: x[1])
                        # cursor.execute(
                        #     f"select product_id,pkg_id,{currency} from package_list where pkg_id!=4 order by pkg_id asc")
                        # all_product_id1 = cursor.fetchall()

                    for all_product_ids in all_product_id:
                        sub_list = list(all_product_ids[0].split(","))
                        test_list = li
                        flag = 0
                        if((set(sub_list) & set(test_list)) == set(sub_list)):
                            flag = 1
                        if (flag):
                            if all_product_ids[1] == 1:
                                sub_lists = sub_list
                                pkg_amount = all_product_ids[2]
                            elif all_product_ids[1] == 2:
                                sub_lists = sub_list
                                pkg_amount = all_product_ids[2]
                            elif all_product_ids[1] == 3:
                                sub_lists = sub_list
                                pkg_amount = all_product_ids[2]

                        # else :
                        #     amount=list_count*amount
                    #  sub_list_len=len(sub_lists)
                    print(sub_lists,"sub_lists")
                    print(list_count,len(sub_lists))
                    balance_count = list_count-len(sub_lists)
                    print(balance_count,"balance_count",pkg_amount)
                    total_amount = pkg_amount+(balance_count*customize_amount)
                    discount_amount = total_customize_amount-total_amount

                else:
                    total_customize_amount = 0
                    total_amount = 0
                    discount_amount = 0
                amount_list =str(total_amount)
                print(total_amount,"total_amount")
                pkg_amount = total_amount

        else:  # in alert table
            pkg_amount = sessions.query(AlertPackagePurchase.amount).filter(AlertPackagePurchase.user_id == payment_user_id).first()[0]

        '''get user billing amount by checking in user alert table '''

        alert_user_annual_count = sessions.query(UserPurchaseList).filter(UserPurchaseList.user_id == payment_user_id, UserPurchaseList.billing_frequency=='A').count()
        
        if alert_user_annual_count != 0:  # check if user in package list is annual in users_list

            alert_user_table_count = sessions.query(AlertUserPurchase).filter(AlertUserPurchase.user_id == payment_user_id).count()

            if alert_user_table_count == 0:
                user_amount = sessions.query(UserPurchaseList).with_entities(func.sum(UserPurchaseList.amount.cast(DECIMAL)).label('amount')).filter(UserPurchaseList.user_id == payment_user_id).first()[0]

                users_amount_annual = float(user_amount) * 12
                users_amount = users_amount_annual - (users_amount_annual * (10/100))

            else:  # in alert table
                user_amount = sessions.query(AlertUserPurchase).with_entities(func.sum(AlertUserPurchase.amount.cast(DECIMAL)).label('amount')).filter(AlertUserPurchase.user_id == payment_user_id).first()[0]

                update_usr_billing_freq = sessions.query(AlertUserPurchase.billing_frequency).filter(AlertUserPurchase.user_id==payment_user_id).first()[0]

                if update_usr_billing_freq == "M":
                    users_amount = float(user_amount) 

                else:
                    users_amount_annual = float(user_amount) * 12
                    users_amount = users_amount_annual- (users_amount_annual * (10/100))

        else:
            users_amount = 0

        ''' get cloud billing amount by checking in cloud alert table '''

        if alert_cloud_table_count == 0:
            cloud_amount = sessions.query(CloudPurchaseList.amount).filter(CloudPurchaseList.user_id == payment_user_id).first()[0]


        else:  # in alert table
            cloud_amount = sessions.query(AlertCloudPurchase.amount).filter(AlertCloudPurchase.user_id == payment_user_id).first()[0]


        prod_user_cloud_amount = float(pkg_amount) + float(users_amount) + float(cloud_amount)
        total_packages_amount = float(prod_user_cloud_amount) + float(prod_user_cloud_amount) * (float(gst_percent.strip('%'))/100)

        payment_status = True
        # print("hi",payment_status)

        if payment_status is True:
            pkg_pur_his_id = 0
            usr_pur_his_id = ''
            cld_pur_his_id = 0

            if alert_pkg_table_count == 0:
                updated_pur = sessions.query(PackagePurchaseList).filter(PackagePurchaseList.user_id == payment_user_id).update({ PackagePurchaseList.amount:pkg_amount,PackagePurchaseList.payment_date:current_date, PackagePurchaseList.renewal_date:pkg_renewal_datetime,PackagePurchaseList.product_amount:pkg_amount  })

                billing_product_id = sessions.query(PackagePurchaseList.product_id).filter(PackagePurchaseList.user_id==payment_user_id).first()[0]

                product_id_list = list(billing_product_id.split(",")) 

            else:  # in alert table
                update_pkg_purchase = sessions.query(AlertPackagePurchase).with_entities(AlertPackagePurchase.pkg_pur_id, AlertPackagePurchase.user_id , AlertPackagePurchase.pkg_id , AlertPackagePurchase.product_id , AlertPackagePurchase.amount , AlertPackagePurchase.currency_type, AlertPackagePurchase.currency_symbol , AlertPackagePurchase.latest_entry , AlertPackagePurchase.payment_date ,AlertPackagePurchase.actual_amount, AlertPackagePurchase.discount, AlertPackagePurchase.renewal_date).filter(AlertPackagePurchase.user_id==payment_user_id).all()

                # product_id before in alert
                # print(payment_user_id,"payment_user_id")
                alert_product_id = sessions.query(AlertPackagePurchase).with_entities(AlertPackagePurchase.product_id).filter(AlertPackagePurchase.user_id==payment_user_id).first()[0]

                # product_id before update in billing
                billing_product_id = sessions.query(PackagePurchaseList.product_id).filter(PackagePurchaseList.user_id==payment_user_id).first()[0]

                for update_pkg_pur in update_pkg_purchase:
                    sessions.query(PackagePurchaseList).filter(PackagePurchaseList.user_id==payment_user_id).update({PackagePurchaseList.user_id: update_pkg_pur[1], PackagePurchaseList.pkg_id: update_pkg_pur[2], PackagePurchaseList.product_id: update_pkg_pur[3], PackagePurchaseList.amount: update_pkg_pur[4],PackagePurchaseList.currency_type: update_pkg_pur[5], PackagePurchaseList.currency_symbol: update_pkg_pur[6],PackagePurchaseList.latest_entry: update_pkg_pur[7], PackagePurchaseList.payment_date: current_date, PackagePurchaseList.actual_amount: update_pkg_pur[9], PackagePurchaseList.discount: update_pkg_pur[10],PackagePurchaseList.renewal_date: pkg_renewal_datetime,PackagePurchaseList.product_amount: update_pkg_pur[4]})

                test_list = list(billing_product_id.split(","))
                sub_list = list(alert_product_id.split(","))

                if((set(sub_list) & set(test_list)) == set(test_list)):
                    flag = 1
                else:
                    flag = 0
                if flag == 1:
                    product_id_list = list(alert_product_id.split(","))  # values from alert table to insert in siteadmin

                else:
                    product_id_list = list(alert_product_id.split(","))  # values from alert table to insert in siteadmin
                    balance_products = list(set(test_list) - set(sub_list))

                    for balance_prod in balance_products:
                        siteadmin_session_set.query(MenuRolesList).filter_by(user_id=siteadmin_userid).delete()

            ''' insert product list in siteadmin  '''
            
            siteadmin_session_set.query(Packages).filter_by(user_id=siteadmin_userid).delete()
            for pkg_product_id in product_id_list:
                # product_id = pkg_product_id
                product_id = encryptdata(pkg_product_id)
                insertsite_prod = Packages(user_id=siteadmin_userid, product_id=product_id, link='localhost:5003', renewal_date=pkg_renewal_datetime)
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

            select_pkg_purchase = sessions.query(PackagePurchaseList).with_entities(PackagePurchaseList.pkg_pur_id, PackagePurchaseList.user_id , PackagePurchaseList.pkg_id , PackagePurchaseList.product_id , PackagePurchaseList.amount , PackagePurchaseList.currency_type, PackagePurchaseList.currency_symbol , PackagePurchaseList.latest_entry , PackagePurchaseList.payment_date , PackagePurchaseList.actual_amount , PackagePurchaseList.discount , PackagePurchaseList.renewal_date, PackagePurchaseList.product_amount) .filter(PackagePurchaseList.user_id==payment_user_id).all()

            for select_pkg_pur in select_pkg_purchase:
                pkg_pur_his = PackagePurchaseHistory(pkg_pur_id=select_pkg_pur[0], user_id=select_pkg_pur[1], pkg_id=select_pkg_pur[2], product_id=select_pkg_pur[3], amount=select_pkg_pur[4],currency_type=select_pkg_pur[5], currency_symbol=select_pkg_pur[6],latest_entry=select_pkg_pur[7], payment_date=select_pkg_pur[8], actual_amount=select_pkg_pur[9] ,discount=select_pkg_pur[10] ,renewal_date=select_pkg_pur[11],product_amount=select_pkg_pur[12] )
                sessions.add(pkg_pur_his)
                sessions.flush()
                pkg_pur_his_id=pkg_pur_his.pkg_history_id
            # print("hi")
            sessions.query(AlertPackagePurchase).filter_by(user_id=payment_user_id).delete()
         

            if alert_user_annual_count != 0:
                if alert_user_table_count == 0:

                    get_existing_details = sessions.query(UserPurchaseList).filter(UserPurchaseList.user_id == payment_user_id, UserPurchaseList.billing_frequency=='A').all()
                    for existng_data in get_existing_details:
                        typeid = existng_data.user_type_id
                        noofusers = existng_data.no_of_users
                        amtval = existng_data.amount
                        updated_user = sessions.query(UserPurchaseList).filter(UserPurchaseList.user_id == payment_user_id,UserPurchaseList.user_type_id==typeid).update({ UserPurchaseList.actual_no_of_users:noofusers, UserPurchaseList.actual_amount:amtval})

                    updated_user = sessions.query(UserPurchaseList).filter(UserPurchaseList.user_id == payment_user_id).update({ UserPurchaseList.payment_date:current_date, UserPurchaseList.renewal_date:pkg_renewal_datetime  })

                    usr_purchased_list = sessions.query(UserPurchaseList).with_entities(UserPurchaseList.user_type_id, UserPurchaseList.no_of_users).filter(UserPurchaseList.user_id==payment_user_id).all()

                    ''' insert Users list in siteadmin  '''

                    siteadmin_session_set.query(UserList).filter_by(user_id=siteadmin_userid).delete()

                    for usr_pur_list in usr_purchased_list:
                        user_type_id = usr_pur_list[0]
                        no_of_users = usr_pur_list[1]

                        user_type = encryptdata(user_type_id)
                        user_count = encryptdata(no_of_users)
                        # print(user_count,"user_count")

                        insert_userslist = UserList(user_id=siteadmin_userid, user_type_id=user_type, no_of_users=user_count, renewal_date=pkg_renewal_datetime)
                        siteadmin_session_set.add(insert_userslist)
                        siteadmin_session_set.flush()


                else:  # in alert table
                    # adminuser_before_billing = sessions.query(UserPurchaseList.no_of_users).filter(UserPurchaseList.user_id == payment_user_id, UserPurchaseList.user_type_id == 1).first()[0]

                    # generaluser_before_billing = sessions.query(UserPurchaseList.no_of_users).filter(UserPurchaseList.user_id == payment_user_id, UserPurchaseList.user_type_id == 2).first()[0]

                    # limiteduser_before_billing = sessions.query(UserPurchaseList.no_of_users).filter(UserPurchaseList.user_id == payment_user_id, UserPurchaseList.user_type_id == 3).first()[0]

                    update_usr_purchase = sessions.query(AlertUserPurchase).with_entities(AlertUserPurchase.user_pur_id, AlertUserPurchase.user_id , AlertUserPurchase.user_type_id , AlertUserPurchase.no_of_users , AlertUserPurchase.amount , AlertUserPurchase.currency_type, AlertUserPurchase.currency_symbol , AlertUserPurchase.latest_entry , AlertUserPurchase.payment_date , AlertUserPurchase.renewal_date , AlertUserPurchase.billing_frequency).filter(AlertUserPurchase.user_id==payment_user_id).all()

                    update_usr_billing_freq = sessions.query(AlertUserPurchase.billing_frequency).filter(AlertUserPurchase.user_id==payment_user_id).first()[0]

                    if update_usr_billing_freq == "A":
                        usr_renewal_date = pkg_renewal_datetime
                    else:
                        usr_renewal_date = current_date + relativedelta(months=1, days=-1)

                    for update_usr_pur in update_usr_purchase:
                        sessions.query(UserPurchaseList).filter(UserPurchaseList.user_id==payment_user_id, update_usr_pur[1]==payment_user_id, UserPurchaseList.user_type_id == update_usr_pur[2]).update({UserPurchaseList.user_id: update_usr_pur[1], UserPurchaseList.user_type_id: update_usr_pur[2], UserPurchaseList.no_of_users: update_usr_pur[3], UserPurchaseList.amount: update_usr_pur[4],UserPurchaseList.currency_type: update_usr_pur[5], UserPurchaseList.currency_symbol: update_usr_pur[6],UserPurchaseList.latest_entry: update_usr_pur[7], UserPurchaseList.payment_date: current_date,UserPurchaseList.renewal_date: usr_renewal_date, UserPurchaseList.billing_frequency: update_usr_pur[10],UserPurchaseList.actual_no_of_users:update_usr_pur[3],UserPurchaseList.actual_amount:update_usr_pur[4] })

                    ''' insert Users list in siteadmin  '''

                    siteadmin_session_set.query(UserList).filter_by(user_id=siteadmin_userid).delete()

                    usr_purchased_list = sessions.query(AlertUserPurchase).with_entities(AlertUserPurchase.user_type_id, AlertUserPurchase.no_of_users).filter(AlertUserPurchase.user_id==payment_user_id).all()

                    for usr_pur_list in usr_purchased_list:
                        user_type_id = usr_pur_list[0]
                        no_of_users = usr_pur_list[1]

                        user_type = encryptdata(user_type_id)
                        user_count = encryptdata(no_of_users)
                        # print(user_count,"user_count")

                        insert_userslist = UserList(user_id=siteadmin_userid, user_type_id=user_type, no_of_users=user_count, renewal_date=usr_renewal_date)
                        siteadmin_session_set.add(insert_userslist)
                        siteadmin_session_set.flush()

                        ''' no of users based on user type in siteadmin '''
                        # print(user_type_id,"user_type_id")

                        siteadmin_users_count = siteadmin_session_set.query(Users).filter(Users.type_of_user == str(user_type_id)).count()
                        # print(siteadmin_users_count,"siteadmin_users_count")

                        if siteadmin_users_count > no_of_users:
                            # if user_type_id == 1:
                            #     to_delete_users = adminuser_before_billing - no_of_users

                            # elif user_type_id == 2:
                            #     to_delete_users = generaluser_before_billing - no_of_users

                            # elif user_type_id == 3:
                            #     to_delete_users = limiteduser_before_billing - no_of_users

                            delete_users_count = siteadmin_session_set.query(Users.user_id).filter(Users.type_of_user == str(user_type_id)).count()

                            siteadmin_deleteusers_count = delete_users_count - no_of_users
                            if siteadmin_deleteusers_count > 0:
                                delete_users = siteadmin_session_set.query(Users.user_id).filter(Users.type_of_user == str(user_type_id)).order_by(Users.user_id.desc()).limit(siteadmin_deleteusers_count).all()
                                for delete_users in delete_users:
                                    print(delete_users[0],'delete_users[0]')
                                    siteadmin_session_set.query(Users).filter(Users.user_id == delete_users[0]).delete()
                                    # dms
                                    dms_session_set.query(Users).filter(Users.user_id == delete_users[0]).delete()
                                    # cms
                                    cms_session_set.query(Users).filter(Users.user_id == delete_users[0]).delete()
                                    # ams
                                    ams_session_set.query(Users).filter(Users.user_id == delete_users[0]).delete()
                                    # kms
                                    kms_session_set.query(Users).filter(Users.user_id == delete_users[0]).delete()
                                    # dsm
                                    dsm_session_set.query(Users).filter(Users.user_id == delete_users[0]).delete()

                                    # only if admin users are downgraded, delete from website dynamic table
                                    if user_type_id == 1:
                                        cursor.execute(f"delete from {dynamic_table_name} WHERE user_id={delete_users[0]}")
                                        db1.commit()


                            siteadmin_session_set.query(Alert_notify_list).filter(Alert_notify_list.type_id == 1).delete()



                            # fetch users who are changed from admin users to other type of users.
                            if user_type_id == 1:
                                initial_admin_users_count = siteadmin_session_set.query(Users.user_id).filter(Users.initial_type_of_user == "1",Users.type_of_user != "1").count()

                                if initial_admin_users_count > 0:

                                    fetch_users_lists = siteadmin_session_set.query(Users.user_id,Users.type_of_user).filter(Users.initial_type_of_user == str(user_type_id),Users.type_of_user != str(user_type_id)).all()

                                    for fetched_user_data in fetch_users_lists:
                                        fetched_user_id = fetched_user_data[0]
                                        fetched_type_of_user_val = fetched_user_data[1]

                                        siteadmin_session_set.query(Users).filter(Users.user_id==fetched_user_id).update({Users.initial_type_of_user: fetched_type_of_user_val})
                                        # dms
                                        dms_session_set.query(Users).filter(Users.user_id==fetched_user_id).update({Users.initial_type_of_user: fetched_type_of_user_val})
                                        # cms
                                        cms_session_set.query(Users).filter(Users.user_id==fetched_user_id).update({Users.initial_type_of_user: fetched_type_of_user_val})
                                        # ams
                                        ams_session_set.query(Users).filter(Users.user_id==fetched_user_id).update({Users.initial_type_of_user: fetched_type_of_user_val})
                                        # kms
                                        kms_session_set.query(Users).filter(Users.user_id==fetched_user_id).update({Users.initial_type_of_user: fetched_type_of_user_val})
                                        # dsm
                                        dsm_session_set.query(Users).filter(Users.user_id==fetched_user_id).update({Users.initial_type_of_user: fetched_type_of_user_val})

                                        cursor.execute(f"delete from {dynamic_table_name} WHERE user_id={fetched_user_id}")
                                        db1.commit()




                
                select_usr_purchase = sessions.query(UserPurchaseList).with_entities(UserPurchaseList.user_pur_id, UserPurchaseList.user_id , UserPurchaseList.user_type_id , UserPurchaseList.no_of_users , UserPurchaseList.amount , UserPurchaseList.currency_type, UserPurchaseList.currency_symbol , UserPurchaseList.latest_entry , UserPurchaseList.payment_date , UserPurchaseList.renewal_date , UserPurchaseList.billing_frequency,UserPurchaseList.actual_no_of_users, UserPurchaseList.actual_amount).filter(UserPurchaseList.user_id==payment_user_id).all()

                for select_usr_pur in select_usr_purchase:
                    inserted_usr_pur_his = UserPurchaseHistory(user_pur_id=select_usr_pur[0], user_id=select_usr_pur[1], user_type_id=select_usr_pur[2], no_of_users=select_usr_pur[3], amount=select_usr_pur[4],currency_type=select_usr_pur[5], currency_symbol=select_usr_pur[6],latest_entry=select_usr_pur[7], payment_date=select_usr_pur[8],renewal_date=select_usr_pur[9], billing_frequency=select_usr_pur[10],actual_no_of_users=select_usr_pur[11],actual_amount=select_usr_pur[12] )
                    sessions.add(inserted_usr_pur_his)
                    sessions.flush()
                    if usr_pur_his_id == '':
                        usr_pur_his_id = str(inserted_usr_pur_his.user_history_id)
                    else:
                        usr_pur_his_id = str(usr_pur_his_id) + ',' + str(inserted_usr_pur_his.user_history_id)


                sessions.query(AlertUserPurchase).filter_by(user_id=payment_user_id).delete()

            if alert_cloud_table_count == 0:
                updated_cloud = sessions.query(CloudPurchaseList).filter(CloudPurchaseList.user_id == payment_user_id).update({ CloudPurchaseList.payment_date:current_date, CloudPurchaseList.renewal_date:pkg_renewal_datetime  })

                cloud_type = sessions.query(CloudPurchaseList.cloud_type_id).filter(CloudPurchaseList.user_id == payment_user_id).first()[0]

                siteadmin_session_set.query(CloudList).filter(CloudList.user_id == siteadmin_userid).delete()

                cloudtype_id = encryptdata(cloud_type)

                inserted_site_cloud = CloudList(user_id=siteadmin_userid, cloud_type_id=cloudtype_id, renewal_date=pkg_renewal_datetime)
                siteadmin_session_set.add(inserted_site_cloud)
                siteadmin_session_set.flush()

            else:  # in alert table
                update_cloud_purchase = sessions.query(AlertCloudPurchase).with_entities(AlertCloudPurchase.cloud_pur_id, AlertCloudPurchase.user_id , AlertCloudPurchase.cloud_type_id, AlertCloudPurchase.amount , AlertCloudPurchase.currency_type, AlertCloudPurchase.currency_symbol , AlertCloudPurchase.latest_entry , AlertCloudPurchase.payment_date , AlertCloudPurchase.renewal_date).filter(AlertCloudPurchase.user_id==payment_user_id).all()

                for update_cloud_pur in update_cloud_purchase:
                    sessions.query(CloudPurchaseList).filter(CloudPurchaseList.user_id==payment_user_id, update_cloud_pur[1]==payment_user_id).update({CloudPurchaseList.user_id: update_cloud_pur[1], CloudPurchaseList.cloud_type_id: update_cloud_pur[2], CloudPurchaseList.amount: update_cloud_pur[3],CloudPurchaseList.currency_type: update_cloud_pur[4], CloudPurchaseList.currency_symbol: update_cloud_pur[5],CloudPurchaseList.latest_entry: update_cloud_pur[6], CloudPurchaseList.payment_date: current_date, CloudPurchaseList.renewal_date: pkg_renewal_datetime,CloudPurchaseList.actual_amount:update_cloud_pur[3] })

                    siteadmin_session_set.query(CloudList).filter(CloudList.user_id == siteadmin_userid).delete()

                    cloudtype_id = encryptdata(update_cloud_pur[2])

                    inserted_site_cloud = CloudList(user_id=siteadmin_userid, cloud_type_id=cloudtype_id, renewal_date=pkg_renewal_datetime)
                    siteadmin_session_set.add(inserted_site_cloud)
                    siteadmin_session_set.flush()

           
            select_cloud_purchase = sessions.query(CloudPurchaseList).with_entities(CloudPurchaseList.cloud_pur_id, CloudPurchaseList.user_id , CloudPurchaseList.cloud_type_id , CloudPurchaseList.amount , CloudPurchaseList.currency_type, CloudPurchaseList.currency_symbol , CloudPurchaseList.latest_entry , CloudPurchaseList.payment_date , CloudPurchaseList.renewal_date, CloudPurchaseList.actual_amount).filter(CloudPurchaseList.user_id==payment_user_id).all()

            for select_cld_pur in select_cloud_purchase:
                insert_cloud_pur = CloudPurchaseHistory(cloud_pur_id=select_cld_pur[0], user_id=select_cld_pur[1], cloud_type_id=select_cld_pur[2],  amount=select_cld_pur[3],currency_type=select_cld_pur[4], currency_symbol=select_cld_pur[5],latest_entry=select_cld_pur[6], payment_date=select_cld_pur[7],renewal_date=select_cld_pur[8], actual_amount=select_cld_pur[9] )
                sessions.add(insert_cloud_pur)
                sessions.flush()
                cld_pur_his_id=insert_cloud_pur.cloud_history_id
                

            # sessions.flush()

            sessions.query(AlertCloudPurchase).filter_by(user_id=payment_user_id).delete()


            get_bill_details = get_bill_no()
            bill_no = get_bill_details[0]['bill_no']
            pur_no = get_bill_details[0]['pur_no']
            bill_num_val = get_bill_details[0]['bill_num_val']
            pur_num_val = get_bill_details[0]['pur_num_val']
            print('Entered new column Value')
            inserted_pay_his = PaymentHistory(payment_date=current_date, mode_of_payment='credit_card', amount=total_packages_amount, transaction_details='1246566', user_id=payment_user_id, status=1, pkg_pur_his_id= pkg_pur_his_id, user_pur_his_id=usr_pur_his_id, cld_pur_his_id=cld_pur_his_id,bill_no=bill_no,purchase_no=pur_no,bill_series_no=bill_num_val,purchase_series_no=pur_num_val,payment_type='A')
            sessions.add(inserted_pay_his)
            sessions.flush()


            card_no_val = '09764'
            card_no = encryptdata(card_no_val)
            cvv_no_val = '998'
            cvv_no = encryptdata(cvv_no_val)
            expiry_date_val = '04/20'
            expiry_date = encryptdata(expiry_date_val)

            inserted_pay_his = PaymentMode(mode_of_payment='credit_card', card_number=card_no, account_holder_name='scopiq', cvv=cvv_no, expiry_date=expiry_date, user_id=payment_user_id)
            sessions.add(inserted_pay_his)
            sessions.flush()

            sessions.commit()
            siteadmin_session_set.commit()
            dms_session_set.commit()
            cms_session_set.commit()
            ams_session_set.commit()
            kms_session_set.commit()
            dsm_session_set.commit()

            # user_email = sessions.query(RegUsers.email).filter(RegUsers.user_id == payment_user_id).first()[0]
            # sessions.commit()

            with app.app_context():
                msg = Message('Payment Information', sender='sneha.r@perpetua.co.in', recipients=[user_email])
                message = "Your payment was Successful"
                msg.body = message
                msg.html = render_template('emails/alert_mail_remainder.html', expiry_details=message)
                mail.send(msg)

        elif payment_status is not True:
            card_no_val = '09764'
            card_no = encryptdata(card_no_val)
            cvv_no_val = '998'
            cvv_no = encryptdata(cvv_no_val)
            expiry_date_val = '04/20'
            expiry_date = encryptdata(expiry_date_val)

            alert_days_annual = sessions.query(AlertIntervalList.alert_start_days).filter(AlertIntervalList.renewal_type == "BA").first()[0]

            to_date = current_date + relativedelta(days=alert_days_annual)

            inserted_pay_status = PaymentStatus(user_id=payment_user_id,mode_of_payment='credit_card', card_number=card_no, account_holder_name='scopiq', amount=total_packages_amount, from_date=current_date, to_date=to_date, payment_type="A")
            sessions.add(inserted_pay_status)
            sessions.flush()
            sessions.commit()

            # user_email = sessions.query(RegUsers.email).filter(RegUsers.user_id == payment_user_id).first()[0]

            with app.app_context():
                msg = Message('Payment Information', sender='sneha.r@perpetua.co.in', recipients=[user_email])
                message = "Your payment was failed"
                msg.body = message
                msg.html = render_template('emails/alert_mail_remainder.html', expiry_details=message)
                mail.send(msg)



def next_billing_customize(allVals):
    if allVals != '""':
        newvalue = str(allVals).replace("'", "").replace('"', "")
        li = list(newvalue.split(","))
        list_count = len(li)
        currency_type = session['currency']
        currency = currency_type.lower()
        amount_list = []
        sub_lists = ''
        pkg_amount = 0
        effective_date = sessions.query(PackageList.effective_date).first()[0]
        current_date = datetime.date(datetime.now())

        if effective_date <= current_date:
            customize_amount = sessions.query(PackageList).with_entities(getattr(PackageList,currency).label('package_amount')).filter_by(pkg_id=4).first()[0]
            # cursor.execute(
            #     f"select {currency} as package_amount from package_list where pkg_id=4 ")
            # customize_amount = cursor.fetchone()[0]
            total_customize_amount = list_count*customize_amount

            all_product_id = sessions.query(PackageList).with_entities(PackageList.product_id,PackageList.pkg_id, getattr(PackageList,currency)).filter(PackageList.pkg_id!=4, PackageList.pkg_id!=5).order_by(PackageList.pkg_id.asc()).all()
            # cursor.execute(
            #     f"select product_id,pkg_id,{currency} from package_list where pkg_id!=4 order by pkg_id asc")
            # all_product_id = cursor.fetchall()
        else:
            customize_amount = sessions.query(PackageListHistory).with_entities(getattr(PackageListHistory,currency).label('package_amount')).filter_by(pkg_id=4).filter(PackageListHistory.effective_date <= current_date ).first()[0]
            total_customize_amount = list_count*customize_amount

            prod_id_count = sessions.query(PackageList).filter(PackageList.pkg_id!=4).count()

            all_product_id = sessions.query(PackageListHistory).with_entities(PackageListHistory.product_id,PackageListHistory.pkg_id, getattr(PackageListHistory,currency)).filter(PackageListHistory.pkg_id!=4, PackageListHistory.pkg_id!=5).filter(PackageListHistory.effective_date <= current_date ).order_by(PackageListHistory.pkg_his_id.desc()).limit(prod_id_count).all()
            all_product_id.sort(key = lambda x: x[1])
            # cursor.execute(
            #     f"select product_id,pkg_id,{currency} from package_list where pkg_id!=4 order by pkg_id asc")
            # all_product_id1 = cursor.fetchall()

        for all_product_ids in all_product_id:
            sub_list = list(all_product_ids[0].split(","))
            test_list = li
            flag = 0
            if((set(sub_list) & set(test_list)) == set(sub_list)):
                flag = 1
            if (flag):
                if all_product_ids[1] == 1:
                    sub_lists = sub_list
                    pkg_amount = all_product_ids[2]
                elif all_product_ids[1] == 2:
                    sub_lists = sub_list
                    pkg_amount = all_product_ids[2]
                elif all_product_ids[1] == 3:
                    sub_lists = sub_list
                    pkg_amount = all_product_ids[2]

            # else :
            #     amount=list_count*amount
        #  sub_list_len=len(sub_lists)
        print(sub_lists,"sub_lists")
        print(list_count,len(sub_lists))
        balance_count = list_count-len(sub_lists)
        print(balance_count,"balance_count",pkg_amount)
        total_amount = pkg_amount+(balance_count*customize_amount)
        discount_amount = total_customize_amount-total_amount

    else:
        total_customize_amount = 0
        total_amount = 0
        discount_amount = 0
    amount_list =str(total_amount)
    print(total_amount,"total_amount")
    return str(amount_list)

    #  for li in li:
    #      print(enumerate(list),"newvalueli")



''' cronjob function to send mail if auto renewal payment process fails '''


@cron.interval_schedule(hours=24)
def resending_payment_renewal():
    current_date = datetime.date(datetime.now())
    payment_status_details = sessions.query(PaymentStatus, RegUsers).with_entities(PaymentStatus.from_date,PaymentStatus.to_date, RegUsers.email, RegUsers.user_id).join(RegUsers, PaymentStatus.user_id == RegUsers.user_id).all()
    print(payment_status_details,"payment_mode_details")
    
    for payment_status_details in payment_status_details:
        user_email = payment_status_details[2]
        from_date = payment_status_details[0]
        to_date = payment_status_details[1]
        expired_user = payment_status_details[3]

        one_day_after = to_date + relativedelta(days=1)

        if current_date == one_day_after:
            sessions.query(RegUsers).filter(RegUsers.user_id == expired_user).update({ RegUsers.status:2 })
            sessions.commit()
            company_details = sessions.query(CompanyDetails).with_entities(CompanyDetails.company_id,CompanyDetails.company_name).filter(CompanyDetails.user_id == expired_user).first()
            company_id = company_details[0]
            company_name = company_details[1]


            location_list = sessions.query(Location).with_entities(Location.location_id,Location.location_name).filter(Location.company_id == company_id).first()
            location_id = location_list[0]
            location_name = location_list[1]

            stop_service(company_name,location_name)

        two_days_before = to_date + relativedelta(days=-2)

        # send mail if current date is between from date and two days before to date
        if from_date < current_date <= two_days_before:
            with app.app_context():
                msg = Message('Payment Information', sender='sneha.r@perpetua.co.in', recipients=[user_email])
                link = url_for('loginredirect', email=user_email,types='auto_renewal',  _external=True)
                msg.body = 'Your payment was failed.Click here to pay {}'.format(link)
                msg.html = render_template('emails/payment_failure.html', link=link)
                mail.send(msg)

        # send mail if current date is between two days after to date and to date

        elif two_days_before < current_date <= to_date:
            print("else")
            with app.app_context():
                msg = Message('Payment Information', sender='sneha.r@perpetua.co.in', recipients=[user_email])
                # message = "your subscription will be cancelled since payment not done"
                link = url_for('loginredirect', email=user_email,types='auto_renewal',  _external=True)
                print(link)
                msg.body = 'your subscription will be cancelled since payment not done.Click here to pay {}'.format(link)
                msg.html = render_template('emails/payment_failure.html', link=link)
                mail.send(msg)


''' function to alert mail for free trial '''


@cron.interval_schedule(hours=24)
def alert_free_trial_mail():
    alert_interval_free_list = sessions.query(AlertIntervalList).with_entities(AlertIntervalList.alert_start_days, AlertIntervalList.renewal_alert_days).filter(AlertIntervalList.renewal_type=="F").first()

    free_remainder_users = []

    alert_start_days_free = alert_interval_free_list[0]
    alert_interval_free = - + alert_interval_free_list[1]

    for alerts in range(alert_start_days_free, 0, alert_interval_free):  # range(start,stop,step)
        alert_period = alerts
        current_date = datetime.date(datetime.now())
        payment_date = current_date + relativedelta(days=alert_period)
        mail_user_pkgcount = sessions.query(PackagePurchaseList).join(RegUsers, PackagePurchaseList.user_id == RegUsers.user_id).filter(PackagePurchaseList.renewal_date == payment_date, RegUsers.user_type == 'F').count()

        if mail_user_pkgcount != 0:
            mail_remainder_user = sessions.query(PackagePurchaseList, RegUsers).with_entities(PackagePurchaseList.user_id, RegUsers.email , PackagePurchaseList.renewal_date).join(RegUsers, PackagePurchaseList.user_id == RegUsers.user_id).filter(PackagePurchaseList.renewal_date == payment_date, RegUsers.user_type == 'F').all()

            for mail_rem_user in mail_remainder_user:
                user_email = mail_rem_user[1]
                renewal_date = (mail_rem_user[2].strftime('%d-%m-%Y'))
                with app.app_context():
                    msg = Message('Expire', sender='sneha.r@perpetua.co.in', recipients=[user_email])
                    expiry_details = "Your Free Trial will expire on " + str(renewal_date) +" Please upgrade your packages."
                    msg.body = expiry_details
                    msg.html = render_template('emails/alert_mail_remainder.html', expiry_details=expiry_details)
                    mail.send(msg)


''' function to deactivate users when they didnt purchase after free trial '''

@cron.interval_schedule(hours=24)
def deactivate_free_trial_users():
    current_date = datetime.date(datetime.now())

    expired_users = sessions.query(PackagePurchaseList, RegUsers).with_entities(PackagePurchaseList.user_id, PackagePurchaseList.renewal_date).join(RegUsers, PackagePurchaseList.user_id == RegUsers.user_id).filter(RegUsers.user_type == 'F').all()
    if len(expired_users)>0:
        for expired_users in expired_users:
            renewal_date = expired_users[1]
            one_day_after = renewal_date + relativedelta(days=1)

            if current_date == one_day_after:
                expired_user = expired_users[0]
                company_details = sessions.query(CompanyDetails).with_entities(CompanyDetails.company_id,CompanyDetails.company_name).filter(CompanyDetails.user_id == expired_user).first()
                company_id = company_details[0]
                company_name = company_details[1]


                location_list = sessions.query(Location).with_entities(Location.location_id,Location.location_name).filter(Location.company_id == company_id).first()
                location_id = location_list[0]
                location_name = location_list[1]

                stop_service(company_name,location_name)
                sessions.query(RegUsers).filter(RegUsers.user_id == expired_user).update({ RegUsers.status:2 })
                sessions.commit()

        
def stop_service(company_name,location_name):
    # os.system('/home/user/venv/bin/python3 '+main_dir_path+"/"+company_name+"/"+source_code_folder_name+"/runserver.py")
    company_name = company_name.replace(" ","")
    cmp_name = company_name.lower()

    location_name = location_name.replace(" ","")
    location_name = location_name.lower()
    
    compname = ""
    for character in cmp_name:
        if character.isalnum():
            compname += character

    locname = ""
    for loc_character in location_name:
        if loc_character.isalnum():
            locname += loc_character

    service_filename = str(compname)+str(locname)+".service"
    os.system('sudo systemctl stop '+service_filename)



@app.route('/get_invoice', methods=['GET', 'POST'])
def get_invoice():
    user_count = 0
    user_amount = 0.0
    pay_his_id = request.args.get('id')
    mode = request.args.get('mode')
    print('Kirthi',pay_his_id)
    payment_history_details = sessions.query(PaymentHistory).filter(PaymentHistory.payment_history_id==pay_his_id).all()

    
    pay_his_details = sessions.query(PaymentHistory).filter(PaymentHistory.payment_history_id==pay_his_id).first()
    bill_no = pay_his_details.bill_series_no
    purchase_no = pay_his_details.purchase_series_no
    userid = pay_his_details.user_id
    pay_amt = pay_his_details.amount
    payment_type_val = pay_his_details.payment_type
    comp_details = sessions.query(CompanyDetails).filter(CompanyDetails.user_id==userid).first()
    company_name = comp_details.company_name
    address = comp_details.address
    reg_user_details = sessions.query(RegUsers).filter(RegUsers.user_id==userid).first()
    email_id = reg_user_details.email
    payment_date = pay_his_details.payment_date
    pkg_purchase_details = sessions.query(PackagePurchaseList).filter(PackagePurchaseList.user_id==userid).first()
    currency_type = pkg_purchase_details.currency_type
    currency_symbol = session['currency_symbol']
    gst = session['gst']
    gst_val = int(session['gst'].strip('%'))

    print(pay_his_details.cld_pur_his_id,'Cloud id')

    # ////////////////////////////// Package Start///////////////////////////////
    if pay_his_details.pkg_pur_his_id != 0:
        pkg_his_details = sessions.query(PackagePurchaseHistory).filter(PackagePurchaseHistory.pkg_history_id==pay_his_details.pkg_pur_his_id).first()
        package_id = pkg_his_details.pkg_id
        pkg_details = sessions.query(PackageList).filter(PackageList.pkg_id==package_id).first()
        package_name = pkg_details.pkg_name
        paydate = pkg_his_details.payment_date
        pdate = datetime.strptime(str(paydate), '%Y-%m-%d').strftime('%d-%b-%Y')
        renewdate = pkg_his_details.renewal_date
        rdate = datetime.strptime(str(renewdate), '%Y-%m-%d').strftime('%d-%b-%Y')
        package_service_period = str(pdate) + ' to ' + str(rdate)

        package_amount = pkg_his_details.product_amount
        package_gst_amt = package_amount*gst_val/100
        package_total_amt = float(package_amount) + float(package_gst_amt)

        # if (pay_his_details.pkg_pur_his_id != 0 and pay_his_details.user_pur_his_id == '' and pay_his_details.cld_pur_his_id == 0) or (pay_his_details.pkg_pur_his_id != 0 and pay_his_details.user_pur_his_id != '' and pay_his_details.cld_pur_his_id == 0):
        #     package_amount = pkg_his_details.product_amount
        #     package_gst_amt = package_amount*gst_val/100
        #     package_total_amt = float(package_amount) + float(package_gst_amt)

        # elif pay_his_details.pkg_pur_his_id != 0:
        #     package_amount = pkg_his_details.amount
        #     package_gst_amt = package_amount*gst_val/100
        #     package_total_amt = float(package_amount) + float(package_gst_amt)
    else:
        package_name = '-'
        package_service_period = '-'
        package_amount = 0
        package_gst_amt = 0
        package_total_amt = 0


     # ////////////////////////////// Package End///////////////////////////////
    admin_user_count=0
    general_user_count=0
    limited_user_count=0
    if  pay_his_details.user_pur_his_id != '':
        user_pur_his_ids = pay_his_details.user_pur_his_id.split(',')
        if len(user_pur_his_ids)>0:
            for user_pur_his_id in user_pur_his_ids:
                user_pur_his_details = sessions.query(UserPurchaseHistory).filter(UserPurchaseHistory.user_history_id==user_pur_his_id).first()
                if user_pur_his_details.user_type_id==1:
                    admin_user_count = user_pur_his_details.actual_no_of_users
                    user_renewal_date = user_pur_his_details.renewal_date
                if user_pur_his_details.user_type_id==2:
                    general_user_count = user_pur_his_details.actual_no_of_users
                    user_renewal_date = user_pur_his_details.renewal_date
                if user_pur_his_details.user_type_id==3:
                    limited_user_count = user_pur_his_details.actual_no_of_users
                    user_renewal_date = user_pur_his_details.renewal_date
                
                user_count += user_pur_his_details.actual_no_of_users
                userpaydate = user_pur_his_details.payment_date
                uspdate = datetime.strptime(str(userpaydate), '%Y-%m-%d').strftime('%d-%b-%Y')
                userrenewdate = user_pur_his_details.renewal_date
                usredate = datetime.strptime(str(userrenewdate), '%Y-%m-%d').strftime('%d-%b-%Y')
                user_service_period = str(uspdate) + ' to ' + str(usredate)

                user_amount = float(user_amount) + float(user_pur_his_details.actual_amount)

            if user_pur_his_details.billing_frequency == 'A' and mode == 'billing':
                useramount = float(user_amount)*12
                discount_user_amount = int(useramount)*10/100
                annual_amt = int(useramount) - int(discount_user_amount)
                user_gst_amt = annual_amt*gst_val/100
                user_total_amt = float(annual_amt) + float(user_gst_amt)
            elif user_pur_his_details.billing_frequency == 'A' and mode == 'upgrade':
                current_date = datetime.date(datetime.now())
                date_1 = current_date
                date_2 = sessions.query(PackagePurchaseList.renewal_date).filter(PackagePurchaseList.user_id==userid).first()[0]
                remaining_months = alert_period(date_2,date_1)
                no_of_months = remaining_months[0]['months']

                if no_of_months > 0:
                    useramount = float(user_amount)*no_of_months
                    annual_amt = useramount
                    user_gst_amt = annual_amt*gst_val/100
                    user_total_amt = float(annual_amt) + float(user_gst_amt)
                else:
                    useramount = float(user_amount)*12
                    annual_amt = int(useramount)
                    user_gst_amt = annual_amt*gst_val/100
                    user_total_amt = float(annual_amt) + float(user_gst_amt)

            elif user_pur_his_details.billing_frequency == 'M':
                useramount = float(user_amount)
                annual_amt = int(useramount)
                user_gst_amt = annual_amt*gst_val/100
                user_total_amt = float(annual_amt) + float(user_gst_amt)
            else:
                if user_pur_his_details.billing_frequency == 'A' and pay_his_details.pkg_pur_his_id == 0 and pay_his_details.cld_pur_his_id == 0:
                    current_date = datetime.date(datetime.now())
                    date_1 = current_date
                    date_2 = sessions.query(PackagePurchaseList.renewal_date).filter(PackagePurchaseList.user_id==userid).first()[0]
                    print(date_2,'date_2')

                    remaining_months = alert_period(date_2,date_1)
                    print(remaining_months,'remaining_months')

                    no_of_months = remaining_months[0]['months']
                    print(no_of_months,'remaining_months')
                
                    useramount = float(user_amount)*no_of_months
                    annual_amt = useramount

                    user_gst_amt = annual_amt*gst_val/100
                    user_total_amt = pay_amt

                else:
                    # this is to differentiate between auto renewal billing happening and manual upgrade is happening (in both cases, all three products, users and cloud will be upgrade)
                    if payment_type_val=='A':
                        useramount = float(user_amount)*12
                        discount_user_amount = int(useramount)*10/100

                        annual_amt = useramount - int(discount_user_amount)
                        user_gst_amt = annual_amt*gst_val/100
                        user_total_amt = float(annual_amt) + float(user_gst_amt)

                    else:
                        useramount = float(user_amount)*12
                        annual_amt = int(useramount)
                        user_gst_amt = annual_amt*gst_val/100
                        user_total_amt = float(annual_amt) + float(user_gst_amt)

        
        # elif pay_his_details.user_pur_his_id != '':
        #     user_pur_his_ids = pay_his_details.user_pur_his_id.split(',')
        #     if len(user_pur_his_ids)>0:
        #         for user_pur_his_id in user_pur_his_ids:
        #             user_pur_his_details = sessions.query(UserPurchaseHistory).filter(UserPurchaseHistory.user_history_id==user_pur_his_id).first()
        #             user_count += user_pur_his_details.no_of_users
        #             user_service_period = str(user_pur_his_details.payment_date) + ' to ' + str(user_pur_his_details.renewal_date)
        #             user_amount = float(user_amount) + float(user_pur_his_details.amount)
                    

        #         if user_pur_his_details.billing_frequency == 'A':
        #                 user_amount = float(user_amount)*12
        #                 discount_user_amount = int(user_amount)*10/100
        #                 annual_amt = int(user_amount) - int(discount_user_amount)


        #         user_gst_amt = annual_amt*gst_val/100
        #         user_total_amt = float(annual_amt) + float(user_gst_amt)
    else:
        user_count = 0
        user_amount = 0
        user_service_period = '-'
        user_gst_amt = 0
        user_total_amt = 0
        annual_amt = 0
        
    # ////////////////////////////// Cloud Start ///////////////////////////////
    if pay_his_details.cld_pur_his_id != 0:
        cld_his_details = sessions.query(CloudPurchaseHistory).filter(CloudPurchaseHistory.cloud_history_id==pay_his_details.cld_pur_his_id).first()
        cld_type_id = cld_his_details.cloud_type_id
        cld_type_details = sessions.query(CloudType).filter(CloudType.cl_type_id==cld_type_id).first()
        cld_name = cld_type_details.cl_type_name
        cldpaydate = cld_his_details.payment_date
        cldpdate = datetime.strptime(str(cldpaydate), '%Y-%m-%d').strftime('%d-%b-%Y')
        cldrenewdate = cld_his_details.renewal_date
        cldrdate = datetime.strptime(str(cldrenewdate), '%Y-%m-%d').strftime('%d-%b-%Y')
        cloud_service_period = str(cldpdate) + ' to ' + str(cldrdate)

        cloud_amount = cld_his_details.actual_amount
        cloud_gst_amt = float(cloud_amount)*gst_val/100
        cloud_total_amt = float(cloud_amount) + float(cloud_gst_amt)

        # if pay_his_details.cld_pur_his_id != 0 and pay_his_details.user_pur_his_id != '' and pay_his_details.pkg_pur_his_id != 0:
        #     cloud_amount = cld_his_details.amount
        #     cloud_gst_amt = cloud_amount*gst_val/100
        #     cloud_total_amt = float(cloud_amount) + float(cloud_gst_amt)

        # elif (pay_his_details.pkg_pur_his_id == 0 and pay_his_details.user_pur_his_id == '' and pay_his_details.cld_pur_his_id != 0) or (pay_his_details.pkg_pur_his_id != 0 and pay_his_details.user_pur_his_id == '' and pay_his_details.cld_pur_his_id != 0) or (pay_his_details.pkg_pur_his_id == 0 and pay_his_details.user_pur_his_id != '' and pay_his_details.cld_pur_his_id != 0):
        #     cloud_amount = cld_his_details.actual_amount
        #     cloud_gst_amt = float(cloud_amount)*gst_val/100
        #     cloud_total_amt = float(cloud_amount) + float(cloud_gst_amt)
    else:
        cld_name = '-'
        cloud_amount = 0
        cloud_gst_amt = 0
        cloud_total_amt = 0
        cloud_service_period = '-'
    # ////////////////////////////// Cloud End ///////////////////////////////
    
    total_amt = package_total_amt + float(user_total_amt) + cloud_total_amt
    tax_amount = package_gst_amt+float(user_gst_amt)+cloud_gst_amt
    setting_details = sessions.query(Settings).filter(Settings.setting_id==1).first()
    discount_price = setting_details.user_dis_price
    
    return render_template('invoice.html', company_name=company_name, address=address, email_id=email_id, payment_date=payment_date, currency_type=currency_type, package_name=package_name, user_count=user_count, cld_name=cld_name, package_service_period=package_service_period, user_service_period=user_service_period, cloud_service_period=cloud_service_period, package_amount=package_amount, user_amount=annual_amt, cloud_amount=cloud_amount, pay_his_details=pay_his_details, payment_history_details=payment_history_details, gst=gst, tax_amount=tax_amount, package_gst_amt=package_gst_amt, user_gst_amt=user_gst_amt, cloud_gst_amt=cloud_gst_amt, package_total_amt=package_total_amt, user_total_amt=user_total_amt, cloud_total_amt=cloud_total_amt, total_amt=total_amt, discount_price=discount_price,currency_symbol=currency_symbol,admin_user_count=admin_user_count,general_user_count=general_user_count,limited_user_count=limited_user_count,bill_no=bill_no,purchase_no=purchase_no)


@app.route('/download_invoice', methods=['GET', 'POST'])
def download_invoice():
    pdf = pdfkit.from_url('144.48.49.10:5006/get_invoice?id=476','Invoice.pdf')
    filename = 'Invoice.pdf'
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=Invoice.pdf"
    return response


@app.route('/print_invoice', methods=['GET', 'POST'])
def print_invoice():
    user_count = 0
    user_amount = 0.0
    pay_his_id = request.args.get('id')
    mode = request.args.get('mode')
    print('Kirthi',pay_his_id)
    payment_history_details = sessions.query(PaymentHistory).filter(PaymentHistory.payment_history_id==pay_his_id).all()

    
    pay_his_details = sessions.query(PaymentHistory).filter(PaymentHistory.payment_history_id==pay_his_id).first()
    bill_no = pay_his_details.bill_series_no
    purchase_no = pay_his_details.purchase_series_no
    userid = pay_his_details.user_id
    pay_amt = pay_his_details.amount
    payment_type_val = pay_his_details.payment_type
    comp_details = sessions.query(CompanyDetails).filter(CompanyDetails.user_id==userid).first()
    company_name = comp_details.company_name
    address = comp_details.address
    reg_user_details = sessions.query(RegUsers).filter(RegUsers.user_id==userid).first()
    email_id = reg_user_details.email
    payment_date = pay_his_details.payment_date
    pkg_purchase_details = sessions.query(PackagePurchaseList).filter(PackagePurchaseList.user_id==userid).first()
    currency_type = pkg_purchase_details.currency_type
    currency_symbol = session['currency_symbol']
    gst = session['gst']
    gst_val = int(session['gst'].strip('%'))

    print(pay_his_details.cld_pur_his_id,'Cloud id')

    # ////////////////////////////// Package Start///////////////////////////////
    if pay_his_details.pkg_pur_his_id != 0:
        pkg_his_details = sessions.query(PackagePurchaseHistory).filter(PackagePurchaseHistory.pkg_history_id==pay_his_details.pkg_pur_his_id).first()
        package_id = pkg_his_details.pkg_id
        pkg_details = sessions.query(PackageList).filter(PackageList.pkg_id==package_id).first()
        package_name = pkg_details.pkg_name
        paydate = pkg_his_details.payment_date
        pdate = datetime.strptime(str(paydate), '%Y-%m-%d').strftime('%d-%b-%Y')
        renewdate = pkg_his_details.renewal_date
        rdate = datetime.strptime(str(renewdate), '%Y-%m-%d').strftime('%d-%b-%Y')
        package_service_period = str(pdate) + ' to ' + str(rdate)

        package_amount = pkg_his_details.product_amount
        package_gst_amt = package_amount*gst_val/100
        package_total_amt = float(package_amount) + float(package_gst_amt)

        # if (pay_his_details.pkg_pur_his_id != 0 and pay_his_details.user_pur_his_id == '' and pay_his_details.cld_pur_his_id == 0) or (pay_his_details.pkg_pur_his_id != 0 and pay_his_details.user_pur_his_id != '' and pay_his_details.cld_pur_his_id == 0):
        #     package_amount = pkg_his_details.product_amount
        #     package_gst_amt = package_amount*gst_val/100
        #     package_total_amt = float(package_amount) + float(package_gst_amt)

        # elif pay_his_details.pkg_pur_his_id != 0:
        #     package_amount = pkg_his_details.amount
        #     package_gst_amt = package_amount*gst_val/100
        #     package_total_amt = float(package_amount) + float(package_gst_amt)
    else:
        package_name = '-'
        package_service_period = '-'
        package_amount = 0
        package_gst_amt = 0
        package_total_amt = 0


     # ////////////////////////////// Package End///////////////////////////////
    admin_user_count=0
    general_user_count=0
    limited_user_count=0
    if  pay_his_details.user_pur_his_id != '':
        user_pur_his_ids = pay_his_details.user_pur_his_id.split(',')
        if len(user_pur_his_ids)>0:
            for user_pur_his_id in user_pur_his_ids:
                user_pur_his_details = sessions.query(UserPurchaseHistory).filter(UserPurchaseHistory.user_history_id==user_pur_his_id).first()
                if user_pur_his_details.user_type_id==1:
                    admin_user_count = user_pur_his_details.actual_no_of_users
                    user_renewal_date = user_pur_his_details.renewal_date
                if user_pur_his_details.user_type_id==2:
                    general_user_count = user_pur_his_details.actual_no_of_users
                    user_renewal_date = user_pur_his_details.renewal_date
                if user_pur_his_details.user_type_id==3:
                    limited_user_count = user_pur_his_details.actual_no_of_users
                    user_renewal_date = user_pur_his_details.renewal_date
                
                user_count += user_pur_his_details.actual_no_of_users
                userpaydate = user_pur_his_details.payment_date
                uspdate = datetime.strptime(str(userpaydate), '%Y-%m-%d').strftime('%d-%b-%Y')
                userrenewdate = user_pur_his_details.renewal_date
                usredate = datetime.strptime(str(userrenewdate), '%Y-%m-%d').strftime('%d-%b-%Y')
                user_service_period = str(uspdate) + ' to ' + str(usredate)

                user_amount = float(user_amount) + float(user_pur_his_details.actual_amount)

            if user_pur_his_details.billing_frequency == 'A' and mode == 'billing':
                useramount = float(user_amount)*12
                discount_user_amount = int(useramount)*10/100
                annual_amt = int(useramount) - int(discount_user_amount)
                user_gst_amt = annual_amt*gst_val/100
                user_total_amt = float(annual_amt) + float(user_gst_amt)
            elif user_pur_his_details.billing_frequency == 'A' and mode == 'upgrade':
                current_date = datetime.date(datetime.now())
                date_1 = current_date
                date_2 = sessions.query(PackagePurchaseList.renewal_date).filter(PackagePurchaseList.user_id==userid).first()[0]
                remaining_months = alert_period(date_2,date_1)
                no_of_months = remaining_months[0]['months']

                if no_of_months > 0:
                    useramount = float(user_amount)*no_of_months
                    annual_amt = useramount
                    user_gst_amt = annual_amt*gst_val/100
                    user_total_amt = float(annual_amt) + float(user_gst_amt)
                else:
                    useramount = float(user_amount)*12
                    annual_amt = int(useramount)
                    user_gst_amt = annual_amt*gst_val/100
                    user_total_amt = float(annual_amt) + float(user_gst_amt)

            elif user_pur_his_details.billing_frequency == 'M':
                useramount = float(user_amount)
                annual_amt = int(useramount)
                user_gst_amt = annual_amt*gst_val/100
                user_total_amt = float(annual_amt) + float(user_gst_amt)
            else:
                if user_pur_his_details.billing_frequency == 'A' and pay_his_details.pkg_pur_his_id == 0 and pay_his_details.cld_pur_his_id == 0:
                    current_date = datetime.date(datetime.now())
                    date_1 = current_date
                    date_2 = sessions.query(PackagePurchaseList.renewal_date).filter(PackagePurchaseList.user_id==userid).first()[0]
                    print(date_2,'date_2')

                    remaining_months = alert_period(date_2,date_1)
                    print(remaining_months,'remaining_months')

                    no_of_months = remaining_months[0]['months']
                    print(no_of_months,'remaining_months')
                
                    useramount = float(user_amount)*no_of_months
                    annual_amt = useramount

                    user_gst_amt = annual_amt*gst_val/100
                    user_total_amt = pay_amt

                else:
                    # this is to differentiate between auto renewal billing happening and manual upgrade is happening (in both cases, all three products, users and cloud will be upgrade)
                    if payment_type_val=='A':
                        useramount = float(user_amount)*12
                        discount_user_amount = int(useramount)*10/100

                        annual_amt = useramount - int(discount_user_amount)
                        user_gst_amt = annual_amt*gst_val/100
                        user_total_amt = float(annual_amt) + float(user_gst_amt)

                    else:
                        useramount = float(user_amount)*12
                        annual_amt = int(useramount)
                        user_gst_amt = annual_amt*gst_val/100
                        user_total_amt = float(annual_amt) + float(user_gst_amt)

        
        # elif pay_his_details.user_pur_his_id != '':
        #     user_pur_his_ids = pay_his_details.user_pur_his_id.split(',')
        #     if len(user_pur_his_ids)>0:
        #         for user_pur_his_id in user_pur_his_ids:
        #             user_pur_his_details = sessions.query(UserPurchaseHistory).filter(UserPurchaseHistory.user_history_id==user_pur_his_id).first()
        #             user_count += user_pur_his_details.no_of_users
        #             user_service_period = str(user_pur_his_details.payment_date) + ' to ' + str(user_pur_his_details.renewal_date)
        #             user_amount = float(user_amount) + float(user_pur_his_details.amount)
                    

        #         if user_pur_his_details.billing_frequency == 'A':
        #                 user_amount = float(user_amount)*12
        #                 discount_user_amount = int(user_amount)*10/100
        #                 annual_amt = int(user_amount) - int(discount_user_amount)


        #         user_gst_amt = annual_amt*gst_val/100
        #         user_total_amt = float(annual_amt) + float(user_gst_amt)
    else:
        user_count = 0
        user_amount = 0
        user_service_period = '-'
        user_gst_amt = 0
        user_total_amt = 0
        annual_amt = 0
        
    # ////////////////////////////// Cloud Start ///////////////////////////////
    if pay_his_details.cld_pur_his_id != 0:
        cld_his_details = sessions.query(CloudPurchaseHistory).filter(CloudPurchaseHistory.cloud_history_id==pay_his_details.cld_pur_his_id).first()
        cld_type_id = cld_his_details.cloud_type_id
        cld_type_details = sessions.query(CloudType).filter(CloudType.cl_type_id==cld_type_id).first()
        cld_name = cld_type_details.cl_type_name
        cldpaydate = cld_his_details.payment_date
        cldpdate = datetime.strptime(str(cldpaydate), '%Y-%m-%d').strftime('%d-%b-%Y')
        cldrenewdate = cld_his_details.renewal_date
        cldrdate = datetime.strptime(str(cldrenewdate), '%Y-%m-%d').strftime('%d-%b-%Y')
        cloud_service_period = str(cldpdate) + ' to ' + str(cldrdate)

        cloud_amount = cld_his_details.actual_amount
        cloud_gst_amt = float(cloud_amount)*gst_val/100
        cloud_total_amt = float(cloud_amount) + float(cloud_gst_amt)

        # if pay_his_details.cld_pur_his_id != 0 and pay_his_details.user_pur_his_id != '' and pay_his_details.pkg_pur_his_id != 0:
        #     cloud_amount = cld_his_details.amount
        #     cloud_gst_amt = cloud_amount*gst_val/100
        #     cloud_total_amt = float(cloud_amount) + float(cloud_gst_amt)

        # elif (pay_his_details.pkg_pur_his_id == 0 and pay_his_details.user_pur_his_id == '' and pay_his_details.cld_pur_his_id != 0) or (pay_his_details.pkg_pur_his_id != 0 and pay_his_details.user_pur_his_id == '' and pay_his_details.cld_pur_his_id != 0) or (pay_his_details.pkg_pur_his_id == 0 and pay_his_details.user_pur_his_id != '' and pay_his_details.cld_pur_his_id != 0):
        #     cloud_amount = cld_his_details.actual_amount
        #     cloud_gst_amt = float(cloud_amount)*gst_val/100
        #     cloud_total_amt = float(cloud_amount) + float(cloud_gst_amt)
    else:
        cld_name = '-'
        cloud_amount = 0
        cloud_gst_amt = 0
        cloud_total_amt = 0
        cloud_service_period = '-'
    # ////////////////////////////// Cloud End ///////////////////////////////
    
    total_amt = package_total_amt + float(user_total_amt) + cloud_total_amt
    tax_amount = package_gst_amt+float(user_gst_amt)+cloud_gst_amt
    setting_details = sessions.query(Settings).filter(Settings.setting_id==1).first()
    discount_price = setting_details.user_dis_price
    
    return render_template('print_invoice.html', company_name=company_name, address=address, email_id=email_id, payment_date=payment_date, currency_type=currency_type, package_name=package_name, user_count=user_count, cld_name=cld_name, package_service_period=package_service_period, user_service_period=user_service_period, cloud_service_period=cloud_service_period, package_amount=package_amount, user_amount=annual_amt, cloud_amount=cloud_amount, pay_his_details=pay_his_details, payment_history_details=payment_history_details, gst=gst, tax_amount=tax_amount, package_gst_amt=package_gst_amt, user_gst_amt=user_gst_amt, cloud_gst_amt=cloud_gst_amt, package_total_amt=package_total_amt, user_total_amt=user_total_amt, cloud_total_amt=cloud_total_amt, total_amt=total_amt, discount_price=discount_price,currency_symbol=currency_symbol,admin_user_count=admin_user_count,general_user_count=general_user_count,limited_user_count=limited_user_count,bill_no=bill_no,purchase_no=purchase_no)


    


''' function to view the home page '''


@app.route('/', methods=['GET', 'POST'])
def index():
    if len(session) == 0:
        return render_template('index.html')
    else:
        status = session['status']
        email = session['email']
        count_values = get_all_count()
        return render_template('index.html', status=status, email=email,count_values=count_values)


''' function to add companies for a user '''


@app.route('/company_details', methods=['GET', 'POST'])
def company_details():
    current_date = datetime.date(datetime.now())
    if len(session) == 0:
        return redirect(url_for('logout'))

    userid = session['userid']
    status = session['status']
    email = session['email']
    count_values = get_all_count()
    states_list = " "
    cities_list = " "
    # server_count = session['server_count']
    email_domain = email.split('@')[1]
    emaildomain = "@"+str(email_domain)
    countries_list = sessions.query(Country).all()
    sample_cmpy_list = sessions.query(CompanyDetails.company_name).filter(CompanyDetails.email==emaildomain).group_by(CompanyDetails.company_name).all()

    comp_details_count = sessions.query(CompanyDetails).filter(CompanyDetails.user_id==userid).count()

    if comp_details_count != 0:
        comp_details = sessions.query(CompanyDetails).filter(CompanyDetails.user_id==userid).first()

        usr_cmpy_name = comp_details.company_name
        usr_address = comp_details.address
        usr_email = comp_details.email
        usr_site = comp_details.site_name
        usr_country = comp_details.country_id
        usr_state = comp_details.state_id
        usr_city = comp_details.city_id
        company_code = comp_details.company_code
        if usr_country is not None:
            states_list = sessions.query(State).filter(State.country_id==usr_country).all()

        if usr_state is not None:
            cities_list = sessions.query(City).filter(City.state_id==usr_state).all()

    else:

        usr_cmpy_name = ""
        usr_address = ""
        user_email_domain = email.split('@')[1]
        usr_email = "@"+user_email_domain
        usr_site = ""
        usr_country = ""
        usr_state = ""
        usr_city = ""
        company_code = ""

    if request.method == 'POST':
        try:
            email = request.form['email']
            
            site_name = request.form['site_name']
            site_names = site_name.strip()
            address = request.form['address']
            sample_company = request.form['sample_company']
            country = request.form['country']
            state = request.form['state']
            city = request.form['city']
            if sample_company == "new":
                company_name = request.form['company_name']
            else:
                company_name = sample_company

            company_code = request.form['company_code']
            
            currency = sessions.query(Country).filter_by(country_id=country).first()

            gst_per_count = sessions.query(Gst).filter_by(country_id=country).count()

            
            session_email = session['email']
            get_user_id = sessions.query(RegUsers.user_id).filter_by(email=session_email).first()[0]
            print(get_user_id,'get_user_id')

            get_cur_comp_count = sessions.query(CompanyDetails).filter_by(user_id=get_user_id).count()
            if get_cur_comp_count != 0:
                get_cur_comp_id = sessions.query(CompanyDetails.company_id).filter_by(user_id=get_user_id).first()[0]
                print(get_cur_comp_id,'get_cur_comp_id')

            #     short_count = sessions.query(Location).filter(func.lower(Location.location_name)== func.lower(site_names)).filter(Location.company_id != get_comp_id).count()

            #     if short_count != 0:
            #         result = "Site Name Already Exist for the Selected Company"
            #         flash(result)
            #         return redirect(url_for('company_details'))

            companyids=[]
            get_comp_count = sessions.query(CompanyDetails.company_id).filter_by(company_name=sample_company).count()
            if get_comp_count != 0:
                get_compids = sessions.query(CompanyDetails.company_id).filter_by(company_name=sample_company).all()
                for data in get_compids:
                    compids = data['company_id']
                    companyids.append(compids)

                site_count = sessions.query(CompanyDetails).filter(func.lower(CompanyDetails.site_name)== func.lower(site_names)).filter(CompanyDetails.company_id.in_(companyids)).filter(CompanyDetails.user_id!=get_user_id).count()
                if site_count != 0:
                    result = "Site Name Already Exist for the Selected Company"
                    flash(result)
                    return redirect(url_for('company_details'))

            if gst_per_count != 0:
                gst_per = sessions.query(Gst.gst_per).filter(Gst.country_id==country,Gst.effective_from_date <= current_date).order_by(Gst.gst_id.desc()).first()[0]
            else:
                gst_per = "0%"

            session['gst'] = gst_per
            session['currency'] = currency.currency
            session['currency_symbol'] = currency.currency_symbol
            result = insert_company(
                email, site_name, address, company_name, country, state, city, userid, company_code)
            reg_user_type = sessions.query(RegUsers.user_type).filter(RegUsers.user_id == userid).first()[0]
            if result == "Added Successfully" or result == "Updated Successfully":
                if reg_user_type == "F":
                    # product_id = sessions.query(PackageList.product_id).filter(PackageList.pkg_id == 5).first()[0]

                    # # FOR FREE TRIAL PACKAGE INSERT
                    # prod_selec_count = sessions.query(ProductSelectionList).filter(ProductSelectionList.user_id == userid).count()
                    # if prod_selec_count != 0:
                    #     sessions.query(ProductSelectionList).filter(ProductSelectionList.user_id == userid).delete()

                    # inserted_products = ProductSelectionList(user_id=userid, pkg_id=5, product_id=product_id, amount=0, status=1, actual_amount=0, discount=0)
                    # sessions.add(inserted_products)
                    # sessions.flush()
                    # sessions.commit()

                    # # FOR FREE TRIAL USER INSERT

                    # user_selec_count = sessions.query(UserSelectionList).filter(UserSelectionList.user_id == userid).count()
                    # if user_selec_count != 0:
                    #     sessions.query(UserSelectionList).filter(UserSelectionList.user_id == userid).delete()
                    # inserted_users = UserSelectionList(admin_user_count=2, admin_user_amount=0, general_user_count=5, general_user_amount=0, limited_user_count=5, limited_user_amount=0, amount=0, status=1, user_id=userid, billing_frequency='M', actual_amount=0, discount=0)
                    # sessions.add(inserted_users)
                    # sessions.flush()
                    # sessions.commit()
                  
                    # # FOR FREE TRIAL CLOUD INSERT

                    # cloud_selec_count = sessions.query(CloudSelection).filter(CloudSelection.user_id == userid).count()
                    # if cloud_selec_count != 0:
                    #     sessions.query(CloudSelection).filter(CloudSelection.user_id == userid).delete()
                    # inserted_cloud = CloudSelection(cl_type_id=1, amount=0, user_id=userid,status=1)
                    # sessions.add(inserted_cloud)
                    # sessions.flush()

                    # sessions.query(RegUsers).filter(RegUsers.user_id == userid).update({RegUsers.user_type: 'F'})
                    # sessions.commit()

                    return redirect(url_for('plan_selection'))
                else:
                    return redirect(url_for('pricing'))
            else:
                return render_template('company_details.html', comp_name=company_name, addr=address, email_domain=email, usr_site_name=site_name, status=status, email=email, server_count=server_count, sample_cmpy_list=sample_cmpy_list, comp_details_count=comp_details_count, countries_list=countries_list, states_list=states_list, cities_list=cities_list, com_country=country, com_state=state, com_city=city, count_values=count_values, result=result)

        except Exception as ex:
            sessions.rollback()
            flash(str(ex))
            return redirect(url_for('company_details'))

    return render_template('company_details.html', comp_name=usr_cmpy_name, addr=usr_address, email_domain=usr_email, usr_site_name=usr_site, status=status, email=email, sample_cmpy_list=sample_cmpy_list, comp_details_count=comp_details_count, countries_list=countries_list, com_country=usr_country, states_list=states_list, cities_list=cities_list, com_state=usr_state, com_city=usr_city,  count_values=count_values,company_code=company_code)

@app.route('/plan_selection', methods=['GET', 'POST'])
def plan_selection():
    userid = session['userid']
    status = session['status']
    email = session['email']
    count_values = get_all_count()

    currency_type = session['currency']
    currency = currency_type.lower()

    product_list = sessions.query(ProductList).order_by(ProductList.product_id.asc()).all()

    package_list = sessions.query(PackageList).with_entities(PackageList.pkg_id.label('pkg_id'),PackageList.pkg_name.label('pkg_name'),PackageList.product_id.label('product_id'),getattr(PackageList,currency).label('package_amount')).filter(PackageList.pkg_id == 5).order_by(PackageList.pkg_id.asc())


    if request.method == "POST":
        print("hi")
        packages_type = request.form['packages_type']
        product_id = request.form['product_id']
        print(packages_type,"packages_type")
        if packages_type == "freetrial":
            print("if")
            sessions.query(ProductSelectionList).filter_by(user_id=userid).delete()
            sessions.query(UserSelectionList).filter_by(user_id=userid).delete()
            sessions.query(CloudSelection).filter_by(user_id=userid).delete()


            # need to change here - user selected product id should be captured
            # product_id = sessions.query(PackageList.product_id).filter(PackageList.pkg_id == 5).first()[0]

            # FOR FREE TRIAL PACKAGE INSERT
            prod_selec_count = sessions.query(ProductSelectionList).filter(ProductSelectionList.user_id == userid).count()
            if prod_selec_count != 0:
                sessions.query(ProductSelectionList).filter(ProductSelectionList.user_id == userid).delete()

            inserted_products = ProductSelectionList(user_id=userid, pkg_id=5, product_id=product_id, amount=0, status=1, actual_amount=0, discount=0)
            sessions.add(inserted_products)
            sessions.flush()
            sessions.commit()

            # FOR FREE TRIAL USER INSERT

            user_selec_count = sessions.query(UserSelectionList).filter(UserSelectionList.user_id == userid).count()
            if user_selec_count != 0:
                sessions.query(UserSelectionList).filter(UserSelectionList.user_id == userid).delete()
            inserted_users = UserSelectionList(admin_user_count=5, admin_user_amount=0, general_user_count=5, general_user_amount=0, limited_user_count=5, limited_user_amount=0, amount=0, status=1, user_id=userid, billing_frequency='M', actual_amount=0, discount=0)
            sessions.add(inserted_users)
            sessions.flush()
            sessions.commit()
            
            # FOR FREE TRIAL CLOUD INSERT

            cloud_selec_count = sessions.query(CloudSelection).filter(CloudSelection.user_id == userid).count()
            if cloud_selec_count != 0:
                sessions.query(CloudSelection).filter(CloudSelection.user_id == userid).delete()
            inserted_cloud = CloudSelection(cl_type_id=1, amount=0, user_id=userid,status=1)
            sessions.add(inserted_cloud)
            sessions.flush()

            sessions.query(RegUsers).filter(RegUsers.user_id == userid).update({RegUsers.user_type: 'F'})
            sessions.commit()

            print('Harthik')
            return redirect(url_for('billing_information'))

        elif packages_type == "pur_pkg":
            print("elif")
            sessions.query(ProductSelectionList).filter_by(user_id=userid).delete()
            sessions.query(UserSelectionList).filter_by(user_id=userid).delete()
            sessions.query(CloudSelection).filter_by(user_id=userid).delete()

            sessions.query(RegUsers).filter(RegUsers.user_id == userid).update({RegUsers.user_type: 'P'})
            sessions.commit()
            return redirect(url_for('pricing'))
    return render_template('plan_selection.html', count_values=count_values, package_list=package_list,product_list=product_list)
    

''' function to check if the email exists or not in login function '''


@app.route('/ajax_load_company', methods=['GET', 'POST'])
def ajax_load_company():
    comp_name = request.args.get('comp_name')
    email = session['email']
    email_domain = email.split('@')[1]
    emaildomain = "@"+str(email_domain)
    cmp_name = comp_name.lower()
    comp_count = sessions.query(CompanyDetails).filter(or_(func.lower(func.replace(CompanyDetails.company_name, ' ', '')) == cmp_name,func.lower(CompanyDetails.company_name) == cmp_name), CompanyDetails.email == emaildomain).count()
    return str(comp_count)


''' onchange function to load state on country select '''


@app.route('/ajax_load_state', methods=['GET', 'POST'])
def ajax_load_state():
    country_name = request.args.get('country')
    states_list = sessions.query(State).filter(State.country_id==country_name).all()
    return render_template('ajax/state.html', states=states_list)


''' onchange function to load city on state select '''


@app.route('/ajax_load_city', methods=['GET', 'POST'])
def ajax_load_city():
    state = request.args.get('state')
    cities_list = sessions.query(City).filter(City.state_id==state).all()
    return render_template('ajax/city.html', cities=cities_list)


@app.route('/ajax_admin_slab', methods=['GET', 'POST'])
def ajax_admin_slab():
    users_count1 = request.args.get('users_count1')
    print('d')
    print(users_count1,'users_count1')
    currency_type = session['currency']
    currency = currency_type.lower()
    current_date = datetime.date(datetime.now())
    print(current_date)
    # cursor.execute(f"select effective_date from user_pricing where user_type_id=1 ")
    # admin_effective_date = cursor.fetchone()[0]
    admin_effective_date = sessions.query(UserPricing.effective_date).filter_by(user_type_id=1).first()[0]

    if admin_effective_date <= current_date:
        admin_user = sessions.query(UserPricing).with_entities(UserPricing.lower.label('lower_value'),UserPricing.upper.label('higher_value'),getattr(UserPricing,currency).label('amount'),UserPricing.user_pricing_id.label('user_pricing_id')).filter_by(user_type_id=1)

        # cursor.execute(f"select lower as lower_value,upper as higher_value,{currency} as amount,user_pricing_id from user_pricing where user_type_id=1")
        # columns = [col[0] for col in cursor.description]
        # admin_user = [dict(zip(columns, row)) for row in cursor.fetchall()]

    else:
        admin_cnt = sessions.query(UserPricing).filter_by(user_type_id = 1).count()
        admin_user = sessions.query(UserPricingHistory).with_entities(UserPricingHistory.lower.label('lower_value'),UserPricingHistory.upper.label('higher_value'),getattr(UserPricingHistory,currency).label('amount'),UserPricingHistory.user_pricing_id.label('user_pricing_id')).filter_by(user_type_id=1).filter(UserPricingHistory.effective_date<=current_date).order_by(UserPricingHistory.user_pricing_his_id.desc()).limit(admin_cnt)

        # cursor.execute(f"select count(*) from user_pricing where user_type_id=1")
        # admin_cnt = cursor.fetchone()[0]
        # cursor.execute(f"select lower as lower_value,upper as higher_value,{currency} as amount,user_pricing_id from user_pricing_history where user_type_id=1 and effective_date<=current_date  order by user_pricing_his_id desc LIMIT {admin_cnt}")
        # columns = [col[0] for col in cursor.description]
        # admin_user = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    print(admin_user, "admin_user")
    return render_template('ajax/ajax_admin_slab.html', admin_user=admin_user, users_count1=users_count1)


@app.route('/ajax_general_slab', methods=['GET', 'POST'])
def ajax_general_slab():
    users_count = request.args.get('users_count2')
    print('d')
    print(users_count)
    currency_type = session['currency']
    currency = currency_type.lower()
    print(users_count)
    current_date = datetime.date(datetime.now())
    print(current_date)
    # cursor.execute(f"select effective_date from user_pricing where user_type_id=2 ")
    # general_effective_date = cursor.fetchone()[0]

    general_effective_date = sessions.query(UserPricing.effective_date).filter_by(user_type_id=2).first()[0]

    if general_effective_date <= current_date:
        general_user = sessions.query(UserPricing).with_entities(UserPricing.lower.label('lower_value'),UserPricing.upper.label('higher_value'),getattr(UserPricing,currency).label('amount'),UserPricing.user_pricing_id.label('user_pricing_id')).filter_by(user_type_id=2)

    else:
        general_cnt = sessions.query(UserPricing).filter_by(user_type_id = 2).count()
        general_user = sessions.query(UserPricingHistory).with_entities(UserPricingHistory.lower.label('lower_value'),UserPricingHistory.upper.label('higher_value'),getattr(UserPricingHistory,currency).label('amount'),UserPricingHistory.user_pricing_id.label('user_pricing_id')).filter_by(user_type_id=2).filter(UserPricingHistory.effective_date<=current_date).order_by(UserPricingHistory.user_pricing_his_id.desc()).limit(general_cnt)

        # cursor.execute(f"select count(*) from user_pricing where user_type_id=2")
        # general_cnt = cursor.fetchone()[0]
        # cursor.execute(f"select lower as lower_value,upper as higher_value,{currency} as amount,user_pricing_id from user_pricing_history where user_type_id=2 and effective_date<=current_date  order by user_pricing_his_id desc LIMIT {general_cnt}")
        # columns = [col[0] for col in cursor.description]
        # general_user = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return render_template('ajax/ajax_general_slab.html', general_user=general_user, users_count=users_count)


@app.route('/ajax_limited_slab', methods=['GET', 'POST'])
def ajax_limited_slab():
    users_count = request.args.get('users_count3')
    print('d')
    print(users_count)
    currency_type = session['currency']
    currency = currency_type.lower()
    print(users_count)
    current_date = datetime.date(datetime.now())
    print(current_date)
    # cursor.execute(f"select effective_date from user_pricing where user_type_id=3 ")
    # limited_effective_date = cursor.fetchone()[0]

    limited_effective_date = sessions.query(UserPricing.effective_date).filter_by(user_type_id=3).first()[0]

    if limited_effective_date <= current_date:
        limited_user = sessions.query(UserPricing).with_entities(UserPricing.lower.label('lower_value'),UserPricing.upper.label('higher_value'),getattr(UserPricing,currency).label('amount'),UserPricing.user_pricing_id.label('user_pricing_id')).filter_by(user_type_id=3)

        # cursor.execute(f"select lower as lower_value,upper as higher_value,{currency} as amount,user_pricing_id from user_pricing where user_type_id=3")
        # columns = [col[0] for col in cursor.description]
        # limited_user = [dict(zip(columns, row)) for row in cursor.fetchall()]

    else:
        limited_cnt = sessions.query(UserPricing).filter_by(user_type_id = 3).count()
        limited_user = sessions.query(UserPricingHistory).with_entities(UserPricingHistory.lower.label('lower_value'),UserPricingHistory.upper.label('higher_value'),getattr(UserPricingHistory,currency).label('amount'),UserPricingHistory.user_pricing_id.label('user_pricing_id')).filter_by(user_type_id=3).filter(UserPricingHistory.effective_date<=current_date).order_by(UserPricingHistory.user_pricing_his_id.desc()).limit(limited_cnt)

        # cursor.execute(f"select count(*) from user_pricing where user_type_id=3")
        # limited_cnt = cursor.fetchone()[0]
        # cursor.execute(f"select lower as lower_value,upper as higher_value,{currency} as amount,user_pricing_id from user_pricing_history where user_type_id=3 and effective_date<=current_date  order by user_pricing_his_id desc LIMIT {limited_cnt}")
        # columns = [col[0] for col in cursor.description]
        # limited_user = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return render_template('ajax/ajax_limited_slab.html', limited_user=limited_user,users_count=users_count)


''' function to clear all sessions '''


@app.route('/logout')
def logout():
    #   session.pop('email', None)
    #   session.pop('type', None)
    session.clear()
    return redirect('/')


''' function to register a user and a mail is sent to that user '''


@app.route('/register', methods=['GET', 'POST'])
def register():
    referred_by_userid = request.args.get('id')
    addtocart = request.args.get('add_to_cart')
    print(addtocart,"add_to_cart")
    if request.method == 'POST':
        try:
            email = request.form['email']
            name = request.form['first_name']
            first_name = name.lower().title()
            last_name = request.form['last_name']
            password = request.form['password']
            password_hash = generate_password_hash(password)
            confirm_password = request.form['confirm_password']

            # validation for free trial users if free trial has expired

            if addtocart == "free_trial":
                freetrial_email_count = sessions.query(RegUsers).filter(RegUsers.email == email,RegUsers.status == 2,RegUsers.user_type == 'F').count()
                if freetrial_email_count == 0:
                    result = register_userdetails(first_name, last_name, email, password_hash, referred_by_userid)
                else:
                    result = "You have already purchased for free trial"
                    flash(result)
                    return redirect(url_for('register'))
            else:
                 result = register_userdetails(first_name, last_name, email, password_hash, referred_by_userid)


            if result == "Email already exists":
                flash(result)
                return render_template('register.html', email=email, name=name, last_name=last_name)
            else:
                userid = result
                session['email'] = email
                session['userid'] = userid
                session['status'] = 0
                print(type(addtocart))
                if addtocart == "free_trial":
                    print("hi")
                    sessions.query(RegUsers).filter(RegUsers.user_id == userid).update({RegUsers.user_type: 'F'})
                    sessions.commit()

                else:
                    sessions.query(RegUsers).filter(RegUsers.user_id == userid).update({RegUsers.user_type: 'P'})
                    sessions.commit()

                message = "OTP has been sent to your registered email"
                flash(message,"success")
                return redirect(url_for('otp_generation'))
        except Exception as ex:
            sessions.rollback()
            flash(str(ex))
            return redirect(url_for('register'))

    return render_template('register.html')


''' function to send a otp to the registered user's mail and verify with that otp number '''


@app.route('/otp_generation', methods=['GET', 'POST'])
def otp_generation():
    email_id = session['email']
    userid = session['userid']

    verification_code = sessions.query(RegUsers.verification_code).filter(RegUsers.user_id == userid).first()[0]
    
    if request.method == 'POST':
        try:
            types = request.form['submit']
            if types == "Submit":
                otp = request.form['otp']
                if otp == verification_code:
                    session['status'] = 1
                    session['currency'] = ""
                    # session['server_count'] = 0
                    sessions.query(RegUsers).filter(RegUsers.user_id == userid).update({RegUsers.status: 1})
                    sessions.flush()
                    sessions.commit()
                    billing_count = sessions.query(BillingDetails).filter_by(user_id=userid).count()
                    session['billing_count'] = billing_count
                    if billing_count != 0:
                        return redirect('/my_account')
                    else:
                        return redirect(url_for('company_details'))
                else:
                    message = "Wrong OTP"
                    flash(message,"error")
                    return redirect(url_for('otp_generation'))
            else:
                
                msg = Message('OTP', sender='username@gmail.com',
                            recipients=[email_id])
                otp = rand_pass(6)
                msg.body = otp
                msg.html = render_template('emails/otp_email.html', otp=otp)
                mail.send(msg)
                sessions.query(RegUsers).filter(RegUsers.user_id == userid).update({RegUsers.verification_code: otp})
                sessions.flush()
                sessions.commit()
                message = "Mail sent to the registered mail"
                flash(message,"success")
                return redirect(url_for('otp_generation'))
            

        except Exception as ex:
            sessions.rollback()
            flash(str(ex))
            return redirect(url_for('otp_generation'))

    return render_template('otp_generation.html')


''' function to login the page with email id and password '''


@app.route('/login', methods=['GET', 'POST'])
def login():
    current_date = datetime.date(datetime.now())
    if request.method == "POST":
        try:
            email = request.form['email']
            print(email)
            password = request.form['password']

            if email and password and request.method == 'POST':
                reg_users_count = sessions.query(RegUsers).filter_by(email=email).count()
                print(reg_users_count,"reg_users_count")

                freetrial_email_count = sessions.query(RegUsers).filter(RegUsers.email == email,RegUsers.status == 2).count()

                print(freetrial_email_count,"freetrial_email_count")
                if freetrial_email_count == 0 or (freetrial_email_count == 1 and reg_users_count > 1):
                    rows = sessions.query(RegUsers).filter_by(email=email).order_by(RegUsers.user_id.desc())
                    if rows:
                        for row in rows:
                            user_password = row.password
                            user_id = row.user_id
                            status = row.status
                            if status == 1:
                                if check_password_hash(user_password, password):
                                    session['email'] = email
                                    session['userid'] = user_id
                                    print(session['userid'],"session['userid']")
                                    session['status'] = 1
                                    company_count = sessions.query(CompanyDetails).filter_by(user_id=user_id).count()
                                    if company_count != 0:
                                        company_details = sessions.query(CompanyDetails).filter_by(user_id=user_id).first()
                                        country_id = company_details.country_id
                                        company_name = company_details.company_name

                                        currency = sessions.query(Country).filter_by(country_id=country_id).first()

                                        gst_per_count = sessions.query(Gst).filter_by(country_id=country_id).count()

                                        if gst_per_count != 0:
                                            gst_per = sessions.query(Gst.gst_per).filter(Gst.country_id==country_id,Gst.effective_from_date <= current_date).order_by(Gst.gst_id.desc()).first()[0]
                                        else:
                                            gst_per = "0%"
                                        session['gst'] = gst_per
                                        session['currency'] = currency.currency
                                        session['currency_symbol'] = currency.currency_symbol
                                        session['company_name'] = company_name
                                    else:
                                        session['currency'] = ""

                                    billing_count = sessions.query(BillingDetails).filter_by(user_id=user_id).count()

                                    session['billing_count'] = billing_count
                                    print(billing_count,"billing_count")
                                    if billing_count != 0:
                                        return redirect('/my_account')
                                    else:
                                        return redirect('/company_details')

                                else:
                                    result = 'Invalid password'
                                    # flash(result,"error")
                                    # return redirect('/login')       

                            elif status == 0:
                                result = 'Not Activated'

                            elif status == 3:
                                if check_password_hash(user_password, password):
                                    result = 'You are already a registered user.You cannot login'
                                else:
                                    result = 'Invalid password'
                            elif status == 4:
                                print('Entered',status)
                                if check_password_hash(user_password, password):
                                    session['email'] = email
                                    print('Email',email)
                                    parent_user_id = sessions.query(RegUsers.parent_user_id).filter(RegUsers.email==email).first()[0]
                                    session['userid'] = parent_user_id
                                    print('Parent User Id',parent_user_id)
                                    print(session['userid'],"session['userid']")
                                    session['status'] = 1
                                    company_count = sessions.query(CompanyDetails).filter_by(user_id=parent_user_id).count()
                                    if company_count != 0:
                                        company_details = sessions.query(CompanyDetails).filter_by(user_id=parent_user_id).first()
                                        country_id = company_details.country_id
                                        company_name = company_details.company_name

                                        currency = sessions.query(Country).filter_by(country_id=country_id).first()

                                        gst_per_count = sessions.query(Gst).filter_by(country_id=country_id).count()

                                        if gst_per_count != 0:
                                            gst_per = sessions.query(Gst.gst_per).filter(Gst.country_id==country_id,Gst.effective_from_date <= current_date).order_by(Gst.gst_id.desc()).first()[0]
                                        else:
                                            gst_per = "0%"
                                        session['gst'] = gst_per
                                        session['currency'] = currency.currency
                                        session['currency_symbol'] = currency.currency_symbol
                                        session['company_name'] = company_name
                                    else:
                                        session['currency'] = ""

                                    billing_count = sessions.query(BillingDetails).filter_by(user_id=parent_user_id).count()

                                    session['billing_count'] = billing_count
                                   
                                    return redirect('/my_account')
                                
                        flash(result,"error")
                        return redirect('/login')
                    else:
                        flash('Invalid email/password',"error")
                        return render_template('login.html')
                else:
                    flash('Your free trial subscription is over.Register to purchase products',"error")
                    return render_template('login.html') 
                
        except Exception as ex:
            sessions.rollback()
            flash(str(ex),"error")
            return redirect(url_for('login'))

    return render_template('login.html')


''' function to change audio captcha '''


@app.route('/ajax_load_audiocaptcha', methods=['GET', 'POST'])
def ajax_load_audiocaptcha():
    test_list = [25559, 83236, 67816, 65375, 13221, 19647, 21361, 52554, 64255, 97482]
    random_num = random.choice(test_list)
    return str(random_num)


''' function to redirect the page when the user wants to switch over from siteadmin screen to web screen '''


@app.route('/loginredirect', methods=['GET', 'POST'])
def loginredirect():
    current_date = datetime.date(datetime.now())
    email = request.args.get('email')
    types = request.args.get('types')
    print(types,"type")

    # cursor.execute(f"SELECT * FROM users WHERE email='{email}' ")
    # row = cursor.fetchone()

    row = sessions.query(RegUsers).filter(RegUsers.email==email).first()
    user_id = row.user_id
    status = row.status

    session['email'] = email
    session['userid'] = user_id
    session['status'] = 1
    # server_count = sessions.query(ServerSettings).filter_by(user_id=user_id).count()
    # cursor.execute(
    #     f"select count(*) from server_settings where user_id={(user_id)}")
    # server_count = cursor.fetchone()[0]
    # session['server_count'] = server_count
    company_count = sessions.query(CompanyDetails).filter(CompanyDetails.user_id==user_id).count()
    # cursor.execute(
    #     f"select count(*) from company_details where user_id={(user_id)}")
    # company_count = cursor.fetchone()[0]
    if company_count != 0:
        company_details = sessions.query(CompanyDetails).filter(CompanyDetails.user_id==user_id).first()
        # cursor.execute(
        #     f"select country_id,company_name from company_details where user_id={(user_id)}")
        # company_details = cursor.fetchone()
        country_id = company_details.country_id
        company_name = company_details.company_name
        currency = sessions.query(Country).filter(Country.country_id==country_id).first()
        # cursor.execute(
        #     f"select currency,currency_symbol from country where country_id={(country_id)}")
        # currency = cursor.fetchone()
        gst_per_count = sessions.query(Gst).filter(Gst.country_id==country_id).count()
        # cursor.execute(
        #     f"select count(*) from gst where country_id={country_id}")
        # gst_per_count = cursor.fetchone()[0]
        if gst_per_count != 0:
            gst_per = sessions.query(Gst.gst_per).filter(Gst.country_id==country_id,Gst.effective_from_date <= current_date).order_by(Gst.gst_id.desc()).first()[0]
            # cursor.execute(
            #     f"select gst_per from gst where country_id={country_id}")
            # gst_per = cursor.fetchone()[0]
        else:
            gst_per = "0%"
        session['gst'] = gst_per
        session['currency'] = currency.currency
        session['currency_symbol'] = currency.currency_symbol
        session['company_name'] = company_name
    else:
        session['currency'] = ""
    billing_count = sessions.query(BillingDetails).filter(BillingDetails.user_id==user_id).count()
    # cursor.execute(
    #     f"select count(*) from billing_details where user_id={(user_id)}")
    # billing_count = cursor.fetchone()[0]
    session['billing_count'] = billing_count
    if types == "auto_renewal":
        return redirect('/auto_renewal')
    else:
        if billing_count != 0:
            return redirect('/my_account')
        else:
            return redirect('/company_details')


''' function to get user's payment details,all selected packages and after billing insert users,company,location in siteadmin and dms '''


@app.route('/billing_information', methods=['GET', 'POST'])
def billing_information():
    if len(session) == 0:
        return redirect(url_for('logout'))
    userid = session['userid']
    
    logged_in_emailid = session['email']
    reg_user_type = sessions.query(RegUsers.user_type).filter(RegUsers.user_id == userid).first()[0]

    billing_count = sessions.query(BillingDetails).filter(BillingDetails.user_id == userid).count()
    if billing_count == 0:
        status = session['status']
        email = session['email']
        gst = float(session['gst'].strip('%'))
        # server_count = session['server_count']
        count_values = get_all_count()
        # print(count_values,"count_values")
        countries_list = sessions.query(Country).with_entities(Country.country_id, Country.country_name,Country.country_code).all()

        company_list = sessions.query(CompanyDetails).with_entities(CompanyDetails.country_id, CompanyDetails.state_id, CompanyDetails.city_id, CompanyDetails.company_id, CompanyDetails.company_name, CompanyDetails.company_code).filter(CompanyDetails.user_id == userid).first()
        # print(company_list,"company_list")

        comp_country_id = company_list[0]

        comp_country_name = sessions.query(Country.country_name).filter(Country.country_id==comp_country_id).first()[0]

        print(comp_country_id,'comp_country_id')
        print(comp_country_name,'comp_country_name')

        comp_state_id = company_list[1]
        comp_city_id = company_list[2]
        company_id = company_list[3]
        company_name = company_list[4]
        company_code = company_list[5]
        
        location_list = sessions.query(Location).with_entities(Location.location_id,Location.location_name).filter(Location.company_id == company_id).first()
        location_id = location_list[0]
        location_name = location_list[1]

        product_amount = sessions.query(ProductSelectionList.amount).filter(ProductSelectionList.user_id == userid).first()[0]

        user_amount = sessions.query(UserSelectionList.amount).filter(UserSelectionList.user_id == userid).first()[0]

        cloud_amount = sessions.query(CloudSelection.amount).filter(CloudSelection.user_id == userid).first()[0]
 
        total_bill_amount = float(product_amount) + float(user_amount) + float(cloud_amount)
        total_gst_amnt = total_bill_amount + ((gst/100) * total_bill_amount)
        if total_gst_amnt == 0.0:
            total_gst_amnt = "NIL"

        states_list = sessions.query(State).with_entities(State.state_id, State.state_name,State.state_code).filter(State.country_id == comp_country_id).all()

        cities_list = sessions.query(City).with_entities(City.city_id, City.city_name).filter(State.state_id == comp_state_id).all()

        payment_made = 'false'
        last_pay_his_id = 0

        if request.method == 'POST':
            # try:
                invoice_Company = request.form['invoice_Company']
                gst_vat = request.form['gst_vat']
                invoice_address = request.form['invoice_address']
                country = request.form['country']
                if country == "":
                    country = request.form['comp_country']
                state = request.form['state']
                if state == "":
                    state = request.form['comp_state']
                city = request.form['city']
                if city == "":
                    city = request.form['comp_city']

                bill_no = rand_pass(6)

                # create dynamic databases based on Company ID
                # first scopiq_site_admin_database
                site_admin_db = 'scopiq_site_admin_'+str(company_id)+"_"+str(location_id)
                create_db(site_admin_db)

                # second scopiq_dms database
                dms_db = 'scopiq_dms_'+str(company_id)+"_"+str(location_id)
                create_db(dms_db)
                
                # third - scopiq cms database
                cms_db = 'scopiq_cms_'+str(company_id)+"_"+str(location_id)
                create_db(cms_db)

                # fourth - scopiq ams database
                ams_db = 'scopiq_ams_'+str(company_id)+"_"+str(location_id)
                create_db(ams_db)

                # fifth - scopiq kms database
                kms_db = 'scopiq_kms_'+str(company_id)+"_"+str(location_id)
                create_db(kms_db)
                
                # sixth - scopiq dsm database
                dsm_db = 'scopiq_dsm_'+str(company_id)+"_"+str(location_id)
                create_db(dsm_db)

                # Sevent - scopiq sms database
                sms_db = 'scopiq_sms_'+str(company_id)+"_"+str(location_id)
                create_db(sms_db)

                # Eightth - scopiq cams database
                cams_db = 'scopiq_cams_'+str(company_id)+"_"+str(location_id)
                create_db(cams_db)
                
                # Nineth - scopiq capa database
                capa_db = 'scopiq_capa_'+str(company_id)+"_"+str(location_id)
                create_db(capa_db)
                
                # create tables inside dynamic database based on Company ID
                # first scopiq_site_admin_database tables
                create_table_site_admin(site_admin_db)
                
                # second scopiq_dms_database tables
                create_table_dms(dms_db)
                
                # third scopiq_cms_database tables
                create_table_cms(cms_db)

                # fourth scopiq_ams_database tables
                create_table_ams(ams_db)

                # fourth scopiq_ams_database tables
                create_table_kms(kms_db)
                
                # sixth scopiq_dsm_database tables
                create_table_dsm(dsm_db)

                # Sevent scopiq_sms_database tables
                create_table_sms(sms_db)

                # Eigth scopiq_sms_database tables
                create_table_cams(cams_db)
                
                # Nineth scopiq_sms_database tables
                create_table_capa(capa_db)

                # function to create and copy source code folder based on  Company Name
                # create_folder_structure(company_name,location_name,site_admin_db,dms_db,cms_db,ams_db,kms_db,dsm_db,sms_db,cams_db,capa_db)
                
                # function to create settings file and write port number and databases name into
                port_no = create_file_into_folder(company_name,location_name,site_admin_db,dms_db,cms_db,ams_db,kms_db,dsm_db,sms_db,cams_db,company_id,capa_db,company_code)

                if total_gst_amnt == "NIL":
                    total_gst_amnt = 0.0
                    new_bill_no = 0
                    bill_num_val = ''
                    new_pur_no = 0
                    pur_num_val = ''
                    pur_no = 0
                    payment_made = 'false'
                else:
                    payment_made = 'true'
                    get_bill_details = get_bill_no()
                    bill_no = get_bill_details[0]['bill_no']
                    pur_no = get_bill_details[0]['pur_no']
                    bill_num_val = get_bill_details[0]['bill_num_val']
                    pur_num_val = get_bill_details[0]['pur_num_val']

                
                res = insert_billing_details(bill_no, invoice_Company, gst_vat, invoice_address, country, state, city, userid, total_gst_amnt, company_id,location_id,bill_no,bill_num_val,pur_no,pur_num_val,company_code)

                last_pay_his_id = res
                
                ############################02-02-2022####################################
                
                # start_service(company_name,location_name)
                
                # msg = Message('Link', sender='username@gmail.com', recipients=[logged_in_emailid])
                # link='http://13.232.237.125:'+str(port_no)+'/login'
                # msg.body = 'Your link is {}'.format(link)
                # msg.html = render_template('emails/site_link.html', link=link)
                # mail.send(msg)

               

                
                # flash('Mail sent to the registered email.Your Port No is {}'.format(port_no),"success")
                flash('Billing Done Successfully',"success")

                ############################02-02-2022###################################

                # return redirect('/my_account')
                return redirect(url_for('my_account', payment_made=payment_made,last_pay_his_id=last_pay_his_id, mode='billing', **request.args))

            # except Exception as ex:
            #     sessions.rollback()
            #     sessions1.rollback()
            #     sessions2.rollback()
            #     flash(str(ex))
            #     return redirect(url_for('billing_information'))

        return render_template('billing_information.html', status=status, email=email, countries_list=countries_list, states_list=states_list, cities_list=cities_list, comp_state_id=comp_state_id, comp_city_id=comp_city_id, comp_country_id=comp_country_id, count_values=count_values, total_gst_amnt=total_gst_amnt,reg_user_type=reg_user_type, last_pay_his_id=last_pay_his_id, payment_made=payment_made,comp_country_name=comp_country_name )

    else:
        return redirect(url_for('my_account'))


def create_db(db_name):
    # declare a new PostgreSQL connection object
    conn = connect(
                   dbname="scopiq_web",
                   user="postgres",
                   host="127.0.0.1",
                   port="5432",
                   password="perpetua"
                   )

    # object type: psycopg2.extensions.connection
    # print ("\ntype(conn):", type(conn))

    # string for the new database name to be created
    DB_NAME = db_name

    # get the isolation leve for autocommit
    autocommit = extensions.ISOLATION_LEVEL_AUTOCOMMIT
    # print ("ISOLATION_LEVEL_AUTOCOMMIT:", extensions.ISOLATION_LEVEL_AUTOCOMMIT)

    """
    ISOLATION LEVELS for psycopg2
    0 = READ UNCOMMITTED
    1 = READ COMMITTED
    2 = REPEATABLE READ
    3 = SERIALIZABLE
    4 = DEFAULT
    """

    # set the isolation level for the connection's cursors
    # will raise ActiveSqlTransaction exception otherwise
    conn.set_isolation_level(autocommit)

    # instantiate a cursor object from the connection
    cursor = conn.cursor()

    # use the execute() method to make a SQL request
    # cursor.execute('CREATE DATABASE ' + str(DB_NAME))

    # use the sql module instead to avoid SQL injection attacks
    cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB_NAME)))

    # close the cursor to avoid memory leaks
    cursor.close()

    # close the connection to avoid memory leaks
    conn.close()


def create_table_site_admin(db_name):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:perpetua@localhost/'+db_name
    app.config['SQLALCHEMY_BINDS'] = {
    'sql_siteadmin': 'postgresql+psycopg2://postgres:perpetua@localhost/'+db_name
    }
    db.create_all()
    db.session.commit()


def create_table_dms(db_name):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:perpetua@localhost/'+db_name
    app.config['SQLALCHEMY_BINDS'] = {
    'sql_dms': 'postgresql+psycopg2://postgres:perpetua@localhost/'+db_name
    }
    db.create_all()
    db.session.commit()
 
 
def create_table_cms(db_name):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:perpetua@localhost/'+db_name
    app.config['SQLALCHEMY_BINDS'] = {
    'sql_cms': 'postgresql+psycopg2://postgres:perpetua@localhost/'+db_name
    }
    db.create_all()
    db.session.commit()


def create_table_ams(db_name):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:perpetua@localhost/'+db_name
    app.config['SQLALCHEMY_BINDS'] = {
    'sql_ams': 'postgresql+psycopg2://postgres:perpetua@localhost/'+db_name
    }
    db.create_all()
    db.session.commit()


def create_table_kms(db_name):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:perpetua@localhost/'+db_name
    app.config['SQLALCHEMY_BINDS'] = {
    'sql_kms': 'postgresql+psycopg2://postgres:perpetua@localhost/'+db_name
    }
    db.create_all()
    db.session.commit()
    
def create_table_dsm(db_name):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:perpetua@localhost/'+db_name
    app.config['SQLALCHEMY_BINDS'] = {
    'sql_dsm': 'postgresql+psycopg2://postgres:perpetua@localhost/'+db_name
    }
    db.create_all()
    db.session.commit()   


def create_table_sms(db_name):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:perpetua@localhost/'+db_name
    app.config['SQLALCHEMY_BINDS'] = {
    'sql_sms': 'postgresql+psycopg2://postgres:perpetua@localhost/'+db_name
    }
    db.create_all()
    db.session.commit() 


def create_table_cams(db_name):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:perpetua@localhost/'+db_name
    app.config['SQLALCHEMY_BINDS'] = {
    'sql_cams': 'postgresql+psycopg2://postgres:perpetua@localhost/'+db_name
    }
    db.create_all()
    db.session.commit()
    
def create_table_capa(db_name):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:perpetua@localhost/'+db_name
    app.config['SQLALCHEMY_BINDS'] = {
    'sql_capa': 'postgresql+psycopg2://postgres:perpetua@localhost/'+db_name
    }
    db.create_all()
    db.session.commit()    

    
def create_folder_structure(company_name,location_name,site_admin_db,dms_db,cms_db,ams_db,kms_db,dsm_db,sms_db,cams_db,capa_db):
    src = actual_src_path
    company_name = str(company_name).replace(" ","")
    company_name = company_name.lower()
    location_name = str(location_name).replace(" ","")
    location_name = location_name.lower()
    company_folder_name = str(company_name)+"_"+str(location_name)
    if not os.path.isdir(main_dir_path+"/"+company_folder_name+"/"+source_code_folder_name):
        os.makedirs(main_dir_path+"/"+company_folder_name+"/"+source_code_folder_name)
    dest = main_dir_path+"/"+company_folder_name+"/"+source_code_folder_name
    copytree(src, dest)
    
    own_filename = "dbnew.txt"
    if os.path.isfile(own_filename):
        os.remove(own_filename)
    
    text_list = [site_admin_db,dms_db,cms_db,ams_db,kms_db,dsm_db,sms_db,cams_db,capa_db]
    with open(own_filename, 'w') as f:
        f.writelines("%s\n" % data for data in text_list)
        
    return 1


def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


def start_service(company_name,location_name):
    # os.system('/home/user/venv/bin/python3 '+main_dir_path+"/"+company_name+"/"+source_code_folder_name+"/runserver.py")
    company_name = company_name.replace(" ","")
    cmp_name = company_name.lower()
    
    location_name = location_name.replace(" ","")
    location_name = location_name.lower()
    
    compname = ""
    for character in cmp_name:
        if character.isalnum():
            compname += character
            
    locname = ""
    for loc_character in location_name:
        if loc_character.isalnum():
            locname += loc_character
        
    service_filename = str(compname)+str(locname)+".service"
    os.system('sudo systemctl start '+service_filename)

def create_file_into_folder_backup(company_name,location_name,site_admin_db,dms_db,cms_db,ams_db,kms_db,dsm_db,sms_db,cams_db,company_id,capa_db):
    cursor.execute(f"select port_no from port_list where status=0 order by port_id asc")
    port_no = cursor.fetchone()[0]
    port_value = str('PORT = ')+str(port_no)
    port_status = 1
    
    sessions.query(PortList).filter(PortList.port_no == port_no).update({PortList.status: port_status, PortList.company_id:company_id})

    default_db = 'scopiq_web'
    dblist = [default_db,site_admin_db,dms_db,cms_db,ams_db,kms_db,dsm_db,sms_db,cams_db,capa_db]
    
    company_name = str(company_name).replace(" ","")
    cmp_name = company_name.lower()
    location_name = str(location_name).replace(" ","")
    location_name = location_name.lower()
    company_folder_name = str(cmp_name)+"_"+str(location_name)
    
    service_file_content = '''
    [Unit]
    Description=Flask Web Service
    
    [Service]
    Type=Simple
    ExecStart=/home/centos/venv/bin/python3 /var/www/html/{cn}/{sfn}/runserver.py
    StandardInput=tty-force
    
    [Install]
    WantedBy=multi-user.target
    '''
    
    context = {
    "cn":  company_folder_name,
    "sfn": source_code_folder_name
    }
    
    compname = ""
    for character in cmp_name:
        if character.isalnum():
            compname += character
            
    locname = ""
    for loc_character in location_name:
        if loc_character.isalnum():
            locname += loc_character
            
    service_filename = str(compname)+str(locname)+str('.service')
    service_file = main_dir_path+"/"+company_folder_name+"/"+source_code_folder_name+"/"+service_filename
    filename = main_dir_path+"/"+company_folder_name+"/"+source_code_folder_name+"/scopiq/settings.cfg"
    dbfilename = main_dir_path+"/"+company_folder_name+"/"+source_code_folder_name+"/db.txt"
    os.remove(filename)
    os.remove(dbfilename)  
    
    with  open(service_file,'w') as myfile:
        myfile.write(service_file_content.format(**context))
    
    f = open(filename,'w')  # w : writing mode  /  r : reading mode  /  a  :  appending mode
    f.write('{}'.format(port_value))
    f.close()

    with open(dbfilename, 'w') as filehandle:
        filehandle.writelines("%s\n" % data for data in dblist)
    
    os.system('sudo cp "{}" /etc/systemd/system'.format(service_file))
    
    return port_no


def create_file_into_folder(company_name,location_name,site_admin_db,dms_db,cms_db,ams_db,kms_db,dsm_db,sms_db,cams_db,company_id,capa_db,company_code):
    default_db = 'azure_scopiq_web'
    dblist = [default_db,site_admin_db,dms_db,cms_db,ams_db,kms_db,dsm_db,sms_db,cams_db,capa_db]
    
    company_name = str(company_name).replace(" ","")
    cmp_name = company_name.lower()
    location_name = str(location_name).replace(" ","")
    location_name = location_name.lower()
    company_folder_name = str(cmp_name)+"_"+str(location_name)

    dbfilename = actual_src_path+"/ScopiQ/"+company_code+".txt"

    # new directory creation
    new_dir_path_target = actual_src_path+"/ScopiQ/scopiq/static/"
    # if not os.path.isdir(new_dir_path_target):
    os.umask(0)
    os.mkdir(new_dir_path_target+company_code)
 
    
    with open(dbfilename, 'w') as filehandle:
        filehandle.writelines("%s\n" % data for data in dblist)
    
    return "success"
    
    
@app.route('/ajax_load_invoice_address', methods=['GET', 'POST'])
def ajax_load_invoice_address():
    userid = session['userid']
    # cursor.execute(
    #     f"select country_id,state_id,city_id,address from company_details where user_id={userid}")
    # company_info = cursor.fetchone()
    company_info = sessions.query(CompanyDetails).with_entities(CompanyDetails.country_id , CompanyDetails.state_id ,CompanyDetails.city_id , CompanyDetails.address).filter(CompanyDetails.user_id==userid).first()
    company_details = str(company_info[0])+"@"+str(company_info[1]) + \
        "@"+str(company_info[2])+"@"+str(company_info[3])
    return str(company_details)


@app.route('/payment', methods=['GET', 'POST'])
def payment():
    return render_template('payment.html')


''' function to view products,users and cloud have been purchased and to view the next expiry date '''


@app.route('/my_account', methods=['GET', 'POST'])
def my_account():
    if len(session) == 0:
        return redirect(url_for('logout'))

    payment_made = request.args.get('payment_made')
    last_pay_his_id = request.args.get('last_pay_his_id')
    mode = request.args.get('mode')
        
    if not payment_made or not last_pay_his_id:
        payment_made = 'false'
        last_pay_his_id = 0
        mode = 'billing'
        
    gst = session['gst']
    userid = session['userid']
    currency_type = session['currency']
    cur_sym = session['currency_symbol']
    currency = currency_type.lower()
    count_values = get_all_count()
    reg_user_type = sessions.query(RegUsers.user_type).filter(RegUsers.user_id == userid).first()[0]
    current_date = datetime.date(datetime.now())

    company_details = sessions.query(CompanyDetails).filter(CompanyDetails.user_id==userid).first()
    country_id = company_details.country_id
    new_gst_per = session['gst']
        
    try:
        pkg_pur_list = sessions.query(PackagePurchaseList,PackageList).with_entities(PackageList.pkg_name,PackagePurchaseList.currency_symbol,PackagePurchaseList.amount,PackagePurchaseList.product_id.label('prod_id'),PackagePurchaseList.payment_date,PackagePurchaseList.renewal_date).join(PackageList, PackageList.pkg_id == PackagePurchaseList.pkg_id).filter(PackagePurchaseList.user_id == userid,PackagePurchaseList.latest_entry==1)

        product_list = sessions.query(ProductList).order_by(ProductList.product_id.asc()).all()

        user_pur_list = sessions.query(UserPurchaseList,UserType).with_entities(UserPurchaseList.amount,UserPurchaseList.user_type_id,UserType.user_type_name,UserPurchaseList.no_of_users,UserPurchaseList.currency_symbol,UserPurchaseList.billing_frequency,UserPurchaseList.payment_date,UserPurchaseList.renewal_date).join(UserType, UserPurchaseList.user_type_id == UserType.user_type_id).filter(UserPurchaseList.user_id == userid,UserPurchaseList.latest_entry==1)

        usr_total_amount = 0
        for user_pur_lists in user_pur_list:
            user_pur = user_pur_lists[0]
            user_pur_amount = float(user_pur)
            usr_total_amount = usr_total_amount+user_pur_amount

        ''' calculate remaining months amount in user details tab '''

        pkg_renewal_date = sessions.query(PackagePurchaseList.renewal_date).filter(PackagePurchaseList.user_id==userid).first()[0]

        next_renewal_date = pkg_renewal_date
        get_gst_count = sessions.query(Gst.gst_per).filter(Gst.country_id==country_id).count()
        if get_gst_count > 0:
            new_gst_per = sessions.query(Gst.gst_per).filter(Gst.country_id==country_id,Gst.effective_from_date <= next_renewal_date).order_by(Gst.gst_id.desc()).first()[0]
        else:
            new_gst_per = session['gst']

        # cursor.execute(f"select renewal_date from package_purchase_list where user_id={userid}")
        # pkg_renewal_date = cursor.fetchone()[0]
        user_payment_date = sessions.query(UserPurchaseList.payment_date).filter(UserPurchaseList.user_id==userid, UserPurchaseList.latest_entry==1).first()[0]
        # print(user_payment_date,"user_payment_date")

        user_billing_frequency_count = sessions.query(UserPurchaseHistory).filter(UserPurchaseHistory.user_id==userid, UserPurchaseHistory.latest_entry==1,UserPurchaseHistory.user_type_id==1).order_by(UserPurchaseHistory.user_history_id.desc()).count()
        if user_billing_frequency_count > 1: # getting previous billing frequency from history table
            user_billing_frequency = sessions.query(UserPurchaseHistory).with_entities(UserPurchaseHistory.billing_frequency).filter(UserPurchaseHistory.user_id==userid, UserPurchaseHistory.latest_entry==1,UserPurchaseHistory.user_type_id==1).order_by(UserPurchaseHistory.user_history_id.desc())
            user_prev_billing_frequency = user_billing_frequency[1][0] # second row is taken as the previous billing frequency since new insert is done in checkout
        else:
            user_prev_billing_frequency = "A" # assign previous billing frequency "A" as static when only first billing is done 

        # print(user_prev_billing_frequency,"user_prev_billing_frequency")

        date_1 = pkg_renewal_date
        # current_date = datetime.date(datetime.now())
        # payment_date = current_date.strftime('%Y-%m-%d')
        date_2 = user_payment_date
        remaining_months = alert_period(date_1,date_2)
        # print(pkg_renewal_date,"current_date",current_date)
        no_of_months = remaining_months[0]['months']
        # print(no_of_months,"no_of_months")

        cloud_pur_list = sessions.query(CloudPurchaseList,CloudType, CloudPricing).with_entities(CloudType.cl_type_name,CloudPurchaseList.currency_symbol, CloudPurchaseList.amount, CloudPricing.features, CloudPurchaseList.payment_date,CloudPurchaseList.renewal_date).join(CloudType, CloudType.cl_type_id == CloudPurchaseList.cloud_type_id).join(CloudPricing, CloudPricing.cl_type_id == CloudPurchaseList.cloud_type_id).filter(CloudPurchaseList.user_id == userid,CloudPurchaseList.latest_entry==1)

        alert_table_count = sessions.query(AlertPackagePurchase).filter(AlertPackagePurchase.user_id == userid).count()

        if alert_table_count == 0:
            next_pkg = sessions.query(PackagePurchaseList).with_entities(PackagePurchaseList.pkg_id,PackagePurchaseList.product_id).filter(PackagePurchaseList.user_id == userid).first()
            pkg_id = next_pkg[0]
            prod_id = next_pkg[1]
            if pkg_id != 4: # pkg amount if it is packages
                next_pkg = sessions.query(PackagePurchaseList,PackageList).with_entities(PackagePurchaseList.pkg_id,getattr(PackageList,currency).label('package_amount')).join(PackageList, PackageList.pkg_id == PackagePurchaseList.pkg_id).filter(PackagePurchaseList.user_id == userid).first()
                next_pkg_amount = next_pkg[1]
            else: # check the products are within the packages and calculate amount
                next_pkg_amount = next_billing_customize(prod_id)

        else: # in alert table
            next_pkg_amount = sessions.query(AlertPackagePurchase.amount).filter(AlertPackagePurchase.user_id == userid).first()[0]

        alert_usr_table_count = sessions.query(AlertUserPurchase).filter(AlertUserPurchase.user_id == userid).count()

        if alert_usr_table_count == 0:
            next_user_details = sessions.query(UserPurchaseList).with_entities(func.sum(UserPurchaseList.amount.cast(DECIMAL)).label('amount'), UserPurchaseList.billing_frequency ).filter(UserPurchaseList.user_id == userid).group_by(UserPurchaseList.billing_frequency).first()
            next_user_amount = next_user_details[0]
            next_billing_frequency = next_user_details[1]


        else: # in alert table
            # print("else")
            next_user_details = sessions.query(AlertUserPurchase).with_entities(func.sum(AlertUserPurchase.amount.cast(DECIMAL)).label('amount'), AlertUserPurchase.billing_frequency ).filter(AlertUserPurchase.user_id == userid).group_by(AlertUserPurchase.billing_frequency).first()
            next_user_amount = next_user_details[0]
            next_billing_frequency = next_user_details[1]

            if next_user_amount == 0:
                next_user_details = sessions.query(UserPurchaseList).with_entities(func.sum(UserPurchaseList.amount.cast(DECIMAL)).label('amount'), UserPurchaseList.billing_frequency ).filter(UserPurchaseList.user_id == userid).group_by(UserPurchaseList.billing_frequency).first()
                next_user_amount = next_user_details[0]
       

        alert_cloud_table_count = sessions.query(AlertCloudPurchase).filter(AlertCloudPurchase.user_id == userid).count()


        if alert_cloud_table_count == 0:
            next_cloud_amount = sessions.query(CloudPurchaseList.amount).filter(CloudPurchaseList.user_id == userid).first()[0]


        else: # in alert table
            next_cloud_amount = sessions.query(AlertCloudPurchase.amount).filter(AlertCloudPurchase.user_id == userid).first()[0]


        payment_status_count = sessions.query(PaymentStatus).filter(PaymentStatus.user_id == userid,PaymentStatus.from_date < current_date, current_date < PaymentStatus.to_date).count()

        
        return render_template('my_account.html', pkg_pur_list=pkg_pur_list, product_list=product_list, user_pur_list=user_pur_list, cloud_pur_list=cloud_pur_list, usr_total_amount=usr_total_amount, count_values=count_values, next_pkg_amount=next_pkg_amount,next_user_amount=next_user_amount,next_billing_frequency=next_billing_frequency,next_cloud_amount=next_cloud_amount,payment_status_count=payment_status_count,reg_user_type=reg_user_type,user_prev_billing_frequency=user_prev_billing_frequency,no_of_months=no_of_months,payment_made=payment_made, last_pay_his_id=last_pay_his_id,new_gst_per=new_gst_per,mode=mode,cur_sym=cur_sym)

    except Exception as ex:
        sessions.rollback()
        flash(str(ex))
        return redirect(url_for('my_account'))


def next_billing_customize(allVals):
    if allVals != '""':
        newvalue = str(allVals).replace("'", "").replace('"', "")
        li = list(newvalue.split(","))
        list_count = len(li)
        currency_type = session['currency']
        currency = currency_type.lower()
        amount_list = []
        sub_lists = ''
        pkg_amount = 0
        effective_date = sessions.query(PackageList.effective_date).first()[0]
        current_date = datetime.date(datetime.now())

        if effective_date <= current_date:
            customize_amount = sessions.query(PackageList).with_entities(getattr(PackageList,currency).label('package_amount')).filter_by(pkg_id=4).first()[0]
            # cursor.execute(
            #     f"select {currency} as package_amount from package_list where pkg_id=4 ")
            # customize_amount = cursor.fetchone()[0]
            total_customize_amount = list_count*customize_amount

            all_product_id = sessions.query(PackageList).with_entities(PackageList.product_id,PackageList.pkg_id, getattr(PackageList,currency)).filter(PackageList.pkg_id!=4, PackageList.pkg_id!=5).order_by(PackageList.pkg_id.asc()).all()
            # cursor.execute(
            #     f"select product_id,pkg_id,{currency} from package_list where pkg_id!=4 order by pkg_id asc")
            # all_product_id = cursor.fetchall()
        else:
            customize_amount = sessions.query(PackageListHistory).with_entities(getattr(PackageListHistory,currency).label('package_amount')).filter_by(pkg_id=4).filter(PackageListHistory.effective_date <= current_date ).first()[0]
            total_customize_amount = list_count*customize_amount

            prod_id_count = sessions.query(PackageList).filter(PackageList.pkg_id!=4).count()

            all_product_id = sessions.query(PackageListHistory).with_entities(PackageListHistory.product_id,PackageListHistory.pkg_id, getattr(PackageListHistory,currency)).filter(PackageListHistory.pkg_id!=4, PackageListHistory.pkg_id!=5).filter(PackageListHistory.effective_date <= current_date ).order_by(PackageListHistory.pkg_his_id.desc()).limit(prod_id_count).all()
            all_product_id.sort(key = lambda x: x[1])
            # cursor.execute(
            #     f"select product_id,pkg_id,{currency} from package_list where pkg_id!=4 order by pkg_id asc")
            # all_product_id1 = cursor.fetchall()

        for all_product_ids in all_product_id:
            sub_list = list(all_product_ids[0].split(","))
            test_list = li
            flag = 0
            if((set(sub_list) & set(test_list)) == set(sub_list)):
                flag = 1
            if (flag):
                if all_product_ids[1] == 1:
                    sub_lists = sub_list
                    pkg_amount = all_product_ids[2]
                elif all_product_ids[1] == 2:
                    sub_lists = sub_list
                    pkg_amount = all_product_ids[2]
                elif all_product_ids[1] == 3:
                    sub_lists = sub_list
                    pkg_amount = all_product_ids[2]

            # else :
            #     amount=list_count*amount
        #  sub_list_len=len(sub_lists)
        print(sub_lists,"sub_lists")
        print(list_count,len(sub_lists))
        balance_count = list_count-len(sub_lists)
        print(balance_count,"balance_count",pkg_amount)
        total_amount = pkg_amount+(balance_count*customize_amount)
        discount_amount = total_customize_amount-total_amount

    else:
        total_customize_amount = 0
        total_amount = 0
        discount_amount = 0
    # print(total_customize_amount,"er",discount_amount,"dfde",total_amount)
    amount_list =str(total_amount)
    print(total_amount,"total_amount")
    #  amount_list.append({'total_customize_amount':total_customize_amount,'total_amount':total_amount,'discount_amount':discount_amount})
    return str(amount_list)

    #  for li in li:
    #      print(enumerate(list),"newvalueli")


# @app.route('/renewal', methods=['GET', 'POST'])
# def renewal():
#     if len(session)==0:
#         return redirect(url_for('logout'))
#     status = session['status']
#     userid = session['userid']
#     email = session['email']
#     server_count = session['server_count']
#     cursor.execute(
#         f"select b.product_name,c.subscription_type,a.purchase_date,c.renewal_date,a.product_selection_id,c.bill_id from product_selection a left join product_list b on a.product_id=b.product_id left join billing_details c on a.product_id=c.product_id where c.latest_entry=1 and a.user_id={userid} and c.user_id={userid} and a.status=1 and c.subscription_type!=4")
#     bill_detail = cursor.fetchall()
#     if request.method == 'POST':
#         selected_bill_id = request.form['submit']
#         if selected_bill_id != '':
#             bill_no = rand_pass(6)
#             bill_id_list = list(selected_bill_id.split(","))
#             bill_payment = []
#             tot_bill_amount = []
#             for bill_id in bill_id_list:
#                 cursor.execute(
#                     f"select product_id,subscription_type,amount from billing_details where bill_id={bill_id}")
#                 bill_details = cursor.fetchone()
#                 product_id = bill_details[0]
#                 amount = bill_details[2]
#                 subscription_type = bill_details[1]

#                 cursor.execute(
#                     f"select a.product_id,a.subscription_type,a.amount,b.product_name from billing_details a left join product_list b on a.product_id=b.product_id where a.bill_id={bill_id}")
#                 bill_pay_details = cursor.fetchone()
#                 bill_amount = bill_pay_details[2]
#                 tot_bill_amount.append(bill_amount)
#                 bill_payment.append(bill_pay_details)

#                 result = insert_renewal_billing_details(
#                     bill_no, userid, product_id, amount, subscription_type, bill_id)

#             total = 0
#             for element in range(0, len(tot_bill_amount)):
#                 total = total + tot_bill_amount[element]
#             return render_template('renewal_billing.html', total_bill_amount=total, bill_pay=bill_payment, server_count=server_count)
#         else:
#             result = "No product is selected"
#             flash(result)
#             return redirect('/renewal')
#     return render_template('renewal.html', status=status, email=email, bill_details=bill_detail, server_count=server_count)


''' function to refer someone to use this product and the referred one will  '''


@app.route('/referral', methods=['GET', 'POST'])
def referral():
    if len(session) == 0:
        return redirect(url_for('logout'))
    status = session['status']
    userid = session['userid']
    session_email = session['email']
    count_values = get_all_count()
    if request.method == 'POST':
        try:
            email = request.form['email']
            # location_name = request.form['location_name']
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            # address = request.form['address']
            random_password = rand_pass_alpha(10)
            random_password_hash = generate_password_hash(random_password)
            result = insert_referral(
                email, first_name, last_name, userid, random_password, random_password_hash)
            if result == "Already mail sent to this email" or result =="You cannot send link to your own mail":
                flash(result)
                return render_template('referral.html', status=status, userid=userid, email=session_email, ref_email=email, ref_first_name=first_name, ref_last_name=last_name, count_values=count_values)
            else:
                result = "Link sent to the provided email"
                flash(result)

        except Exception as ex:
            sessions.rollback()
            flash(str(ex))
            return redirect(url_for('referral'))
    return render_template('referral.html', status=status, userid=userid, email=session_email,  count_values=count_values)


''' function to send a random password to the mail when the password has forgotten '''


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        email_count = sessions.query(RegUsers).filter(RegUsers.email==email).count()
        if email_count == 1:
            # random_password = rand_pass_alpha(10)
            random_password = rand_pass(6)
            random_password_hash = generate_password_hash(random_password)
            sessions.query(RegUsers).filter(RegUsers.email == email).update({RegUsers.password: random_password_hash})
            sessions.commit()
            msg = Message('Your Password',
                          sender='sneha.r@perpetua.co.in', recipients=[email])
            msg.body = random_password
            msg.html = render_template(
                'emails/email.html', random_user_password=random_password, email=email)
            mail.send(msg)
            result = "Mail sent to the registered email"
        else:
            result = "Incorrect Email"
        flash(result)
    return render_template('forgot_password.html')


''' function to send a random password to the mail when the password has forgotten '''


@app.route('/view_referral', methods=['GET', 'POST'])
def view_referral():
    if len(session) == 0:
        return redirect(url_for('logout'))
    status = session['status']
    userid = session['userid']
    session_email = session['email']
    count_values = get_all_count()
    referred_users = sessions.query(RegUsers).filter(RegUsers.referred_by==userid).all()
    # cursor.execute(f"select email,first_name,last_name,user_id from users where referred_by={userid}")
    # columns = [col[0] for col in cursor.description]
    # referred_users = [dict(zip(columns, row)) for row in cursor.fetchall()]

    try:
        referred_user_id = request.args.get('id')
        if referred_user_id is not None:
            email = sessions.query(RegUsers.email).filter(RegUsers.referred_by==userid).filter(RegUsers.user_id==referred_user_id).first()[0]
            # cursor.execute(f"select email from users where referred_by={userid} and user_id={referred_user_id}")
            # email = cursor.fetchone()[0]
            random_password = rand_pass_alpha(10)
            random_password_hash = generate_password_hash(random_password)
            msg = Message('Link', sender='username@gmail.com', recipients=[email])
            link = url_for('login', _external=True)
            msg.body = 'Your link is {}'.format(link)
            msg.html = render_template('emails/link_email.html', link=link, username=email, password=random_password)
            mail.send(msg)

            sessions.query(RegUsers).filter(RegUsers.user_id == referred_user_id).update({RegUsers.password: random_password_hash})
            sessions.commit()

            result = "Link sent to the provided email"
            flash(result)
            return redirect(url_for('view_referral'))

    except Exception as ex:
        sessions.rollback()
        flash(str(ex))
        return redirect(url_for('referral'))
    return render_template('view_referral.html', status=status, userid=userid,  email=session_email,  count_values=count_values, referred_users=referred_users)


''' function to send a mail to scopiq when need a contact '''


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if len(session) != 0:
        count_values = get_all_count()
    else:
        count_values = ""
    if request.method == 'POST':
        try:
            email = request.form['email']
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            phonenumber = request.form['phonenumber']
            comments = request.form['comments']
            msg = Message('CONTACT US', sender='username@gmail.com', recipients=['immanuel.j@perpetua.co.in'])
            msg.body = email
            msg.html = render_template('emails/contact_email.html', first_name=first_name, last_name=last_name, email=email, phonenumber=phonenumber, comments=comments)
            mail.send(msg)
            result = "Mail sent"
            flash(result)

        except Exception as ex:
            sessions.rollback()
            flash(str(ex))
            return redirect(url_for('contact'))

    return render_template('contact.html',count_values=count_values)


''' function to list the cloud package and add '''


@app.route('/server_settings', methods=['GET', 'POST'])
def server_settings():
    if len(session) == 0 or session['currency'] == "":
        return redirect(url_for('logout'))
    userid = session['userid']
    billing_count = sessions.query(BillingDetails).filter(BillingDetails.user_id == userid).count()

    if billing_count == 0:
        currency_type = session['currency']
        currency = currency_type.lower()
        count_values = get_all_count()
        effective_date = sessions.query(CloudPricing.effective_date).first()[0]
        current_date = datetime.date(datetime.now())

        if effective_date <= current_date:
            cloud_list = sessions.query(CloudPricing,CloudType).with_entities(CloudType.cl_type_name,getattr(CloudPricing,currency).label('amount'),CloudPricing.features,CloudType.cl_type_id).join(CloudType, CloudType.cl_type_id == CloudPricing.cl_type_id).order_by(CloudPricing.cl_type_id.asc())

        else:
            cloud_id_count = sessions.query(CloudPricing).count()

            cloud_list = sessions.query(CloudPricingHistory,CloudType).with_entities(CloudType.cl_type_name,getattr(CloudPricingHistory,currency).label('amount'),CloudPricingHistory.features,CloudType.cl_type_id).join(CloudType, CloudType.cl_type_id == CloudPricingHistory.cl_type_id).filter(CloudPricingHistory.effective_date<=current_date).order_by(CloudPricingHistory.cloud_pricing_his_id.desc()).limit(cloud_id_count)

        cloud_selec_list = sessions.query(CloudSelection).with_entities(CloudSelection.cl_type_id).filter(CloudSelection.user_id==userid).order_by(CloudSelection.cloud_id.desc()).first()

        if request.method == 'POST':
            try:
                cloud_package = request.form['cloud_package']
                cloud_pac_amount = "cloud_amount_"+cloud_package
                cloud_amount = request.form[cloud_pac_amount]
                result = insert_server_settings(cloud_package, cloud_amount, userid)
                cloud_type = sessions.query(CloudType.cloud_type).filter(CloudType.cl_type_id==cloud_package).first()[0]
                session['cloud_setup'] = cloud_type
                if cloud_type == 'p':
                    return redirect('/private_setup')
                else:
                    return redirect('/estimation')

            except Exception as ex:
                sessions.rollback()
                flash(str(ex))
                return redirect(url_for('server_settings'))

        return render_template('server_settings.html', cloud_list=cloud_list, count_values=count_values, cloud_selec_list=cloud_selec_list)

    else:
        return redirect(url_for('my_account'))


''' function to list the product packages with their products and add packages for billing '''


@app.route('/pricing', methods=['GET', 'POST'])
def pricing():
    if len(session) == 0 or session['currency'] == "":
        return redirect(url_for('logout'))

    userid = session['userid']
    billing_count = sessions.query(BillingDetails).filter(BillingDetails.user_id == userid).count()

    if billing_count == 0:
        currency_type = session['currency']
        currency = currency_type.lower()
        count_values = get_all_count()
        effective_date = sessions.query(PackageList.effective_date).first()[0]
        current_date = datetime.date(datetime.now())

        if effective_date <= current_date:         
            package_list = sessions.query(PackageList).with_entities(PackageList.pkg_id.label('pkg_id'),PackageList.pkg_name.label('pkg_name'),PackageList.product_id.label('product_id'),getattr(PackageList,currency).label('package_amount')).filter(PackageList.pkg_id != 5).order_by(PackageList.pkg_id.asc())

        else:
            prod_id_count = sessions.query(PackageList).count()

            package_list = sessions.query(PackageListHistory).with_entities(PackageListHistory.pkg_id.label('pkg_id'), PackageListHistory.pkg_name.label('pkg_name'), PackageListHistory.product_id.label('product_id'), getattr(PackageListHistory,currency).label('package_amount')).filter(PackageListHistory.effective_date <= current_date ).filter(PackageListHistory.pkg_id != 5).order_by(PackageListHistory.pkg_his_id.desc()).limit(prod_id_count)


        prod_selec_list = sessions.query(ProductSelectionList).with_entities(ProductSelectionList.user_id, ProductSelectionList.pkg_id, ProductSelectionList.product_id,ProductSelectionList.amount,ProductSelectionList.actual_amount,ProductSelectionList.discount).filter(ProductSelectionList.user_id==userid).order_by(ProductSelectionList.selc_id.desc()).first()

        product_list = sessions.query(ProductList).order_by(ProductList.product_id.asc()).all()
        
        if request.method == "POST":
            try:
                addtocart = request.form['addtocart']
                packagepostvalue = 'pkg_name_'+addtocart
                pkg_name = request.form.get(packagepostvalue)
                amountpostvalue = 'pkg_amount_'+addtocart
                pkg_amount = request.form.get(amountpostvalue)
                cus_pro = request.form.getlist('cus_pro')
                if addtocart == "4":
                    product_id = ','.join(cus_pro)
                    amount = request.form['totamont']
                    discount_amount = request.form['discount_amount']
                    actual_amount = request.form['actual_amount']
                else:
                    product_id = sessions.query(PackageList.product_id).filter(PackageList.pkg_id == addtocart).first()[0]                   
                    amount = pkg_amount
                    discount_amount = 0
                    actual_amount = pkg_amount
                # CODE FOR FREE TRAIL

                # if addtocart == "5":

                #     # FOR FREE TRIAL PACKAGE INSERT
                #     prod_selec_count = sessions.query(ProductSelectionList).filter(ProductSelectionList.user_id == userid).count()
                #     if prod_selec_count != 0:
                #         sessions.query(ProductSelectionList).filter(ProductSelectionList.user_id == userid).delete()

                #     inserted_products = ProductSelectionList(user_id=userid, pkg_id=addtocart, product_id=product_id, amount=0, status=1, actual_amount=0, discount=0)
                #     sessions.add(inserted_products)
                #     sessions.flush()
                #     sessions.commit()

                #     # FOR FREE TRIAL USER INSERT

                #     user_selec_count = sessions.query(UserSelectionList).filter(UserSelectionList.user_id == userid).count()
                #     if user_selec_count != 0:
                #         sessions.query(UserSelectionList).filter(UserSelectionList.user_id == userid).delete()
                #     inserted_users = UserSelectionList(admin_user_count=2, admin_user_amount=0, general_user_count=5, general_user_amount=0, limited_user_count=5, limited_user_amount=0, amount=0, status=1, user_id=userid, billing_frequency='M', actual_amount=0, discount=0)
                #     sessions.add(inserted_users)
                #     sessions.flush()
                #     sessions.commit()
                  
                #     # FOR FREE TRIAL CLOUD INSERT

                #     cloud_selec_count = sessions.query(CloudSelection).filter(CloudSelection.user_id == userid).count()
                #     if cloud_selec_count != 0:
                #         sessions.query(CloudSelection).filter(CloudSelection.user_id == userid).delete()
                #     inserted_cloud = CloudSelection(cl_type_id=1, amount=0, user_id=userid,status=1)
                #     sessions.add(inserted_cloud)
                #     sessions.flush()

                #     sessions.query(RegUsers).filter(RegUsers.user_id == userid).update({RegUsers.user_type: 'F'})
                #     sessions.commit()

                #     return redirect('/billing_information')
                # else:    
                result = insert_prod_selection(
                    userid, addtocart, product_id, amount, actual_amount, discount_amount)
                # sessions.query(RegUsers).filter(RegUsers.user_id == userid).update({RegUsers.user_type: 'P'})
                sessions.commit()
                return redirect('/user_selection')

            except Exception as ex:
                sessions.rollback()
                flash(str(ex))
                return redirect(url_for('user_selection'))
        return render_template('pricing.html', package_list=package_list, product_list=product_list, count_values=count_values, prod_selec_list=prod_selec_list)

    else:
        return redirect(url_for('my_account'))


''' function to list the user packages and add number of users for billing '''


@app.route('/user_selection', methods=['GET', 'POST'])
def user_selection():
    if len(session)==0 or session['currency'] == "":
        return redirect(url_for('logout'))

    userid = session['userid']

    billing_count = sessions.query(BillingDetails).filter(BillingDetails.user_id == userid).count()

    if billing_count == 0:
        currency_type = session['currency']
        currency = currency_type.lower()
        count_values = get_all_count()

        user_selec_list = sessions.query(UserSelectionList).with_entities(UserSelectionList.user_selc_id, UserSelectionList.admin_user_count,UserSelectionList.admin_user_amount,UserSelectionList.general_user_count,UserSelectionList.general_user_amount,UserSelectionList.limited_user_count,UserSelectionList.limited_user_amount,UserSelectionList.amount,UserSelectionList.status,UserSelectionList.user_id,UserSelectionList.created_by,UserSelectionList.created_date,UserSelectionList.updated_by,UserSelectionList.updated_date,UserSelectionList.billing_frequency,UserSelectionList.actual_amount,UserSelectionList.discount).filter(UserSelectionList.user_id==userid).order_by(UserSelectionList.user_selc_id.desc()).first()
        user_type_name = sessions.query(UserType.user_type_name).order_by(UserType.user_type_id.asc())

        current_date = datetime.date(datetime.now())
        admin_effective_date = sessions.query(UserPricing.effective_date).filter_by(user_type_id=1).first()[0]
        general_effective_date = sessions.query(UserPricing.effective_date).filter_by(user_type_id=2).first()[0]
        limited_effective_date = sessions.query(UserPricing.effective_date).filter_by(user_type_id=3).first()[0]

        if admin_effective_date <= current_date:
            admin_user = sessions.query(UserPricing).with_entities(UserPricing.lower.label('lower_value'),UserPricing.upper.label('higher_value'),getattr(UserPricing,currency).label('amount'),UserPricing.user_pricing_id.label('user_pricing_id')).filter_by(user_type_id=1)
        
        else:
            admin_cnt = sessions.query(UserPricing).filter_by(user_type_id = 1).count()
            admin_user = sessions.query(UserPricingHistory).with_entities(UserPricingHistory.lower.label('lower_value'),UserPricingHistory.upper.label('higher_value'),getattr(UserPricingHistory,currency).label('amount'),UserPricingHistory.user_pricing_id.label('user_pricing_id')).filter_by(user_type_id=1).filter(UserPricingHistory.effective_date<=current_date).order_by(UserPricingHistory.user_pricing_his_id.desc()).limit(admin_cnt)

        if general_effective_date <= current_date:
            general_user = sessions.query(UserPricing).with_entities(UserPricing.lower.label('lower_value'),UserPricing.upper.label('higher_value'),getattr(UserPricing,currency).label('amount'),UserPricing.user_pricing_id.label('user_pricing_id')).filter_by(user_type_id=2)
            
        else:
            general_cnt = sessions.query(UserPricing).filter_by(user_type_id = 2).count()
            general_user = sessions.query(UserPricingHistory).with_entities(UserPricingHistory.lower.label('lower_value'),UserPricingHistory.upper.label('higher_value'),getattr(UserPricingHistory,currency).label('amount'),UserPricingHistory.user_pricing_id.label('user_pricing_id')).filter_by(user_type_id=2).filter(UserPricingHistory.effective_date<=current_date).order_by(UserPricingHistory.user_pricing_his_id.desc()).limit(general_cnt)
        
        if limited_effective_date <= current_date:
            limited_user = sessions.query(UserPricing).with_entities(UserPricing.lower.label('lower_value'),UserPricing.upper.label('higher_value'),getattr(UserPricing,currency).label('amount'),UserPricing.user_pricing_id.label('user_pricing_id')).filter_by(user_type_id=3)

        else:
            limited_cnt = sessions.query(UserPricing).filter_by(user_type_id = 3).count()
            limited_user = sessions.query(UserPricingHistory).with_entities(UserPricingHistory.lower.label('lower_value'),UserPricingHistory.upper.label('higher_value'),getattr(UserPricingHistory,currency).label('amount'),UserPricingHistory.user_pricing_id.label('user_pricing_id')).filter_by(user_type_id=3).filter(UserPricingHistory.effective_date<=current_date).order_by(UserPricingHistory.user_pricing_his_id.desc()).limit(limited_cnt)

        if request.method == "POST":
            try:
                admin_count = request.form['admin_count']
                adminus = request.form['adminus']

                general_count = request.form['general_count']
                genus = request.form['genus']

                limited_count = request.form['limited_count']
                limus = request.form['limus']

                totamnt = request.form['totamnt']
                billing_frequency = request.form['billing_frequency']
                if billing_frequency == 'M':
                    totamnt = request.form['totamnt']
                    actual_amount = ''
                    discount = ''
                elif billing_frequency == 'A':
                    totamnt = request.form['annualized_hidden']
                    actual_amount = request.form['totamnt']
                    discount = request.form['discount_hidden']
                result = insert_user_selection(admin_count, adminus, general_count, genus, limited_count,limus, totamnt, userid, billing_frequency, actual_amount, discount)

                return redirect('/server_settings')

            except Exception as ex:
                sessions.rollback()
                flash(str(ex))
                return redirect(url_for('user_selection'))
        return render_template('user_selection.html', admin_user=admin_user, general_user=general_user, limited_user=limited_user, count_values=count_values, user_selec_list=user_selec_list, user_type_name=user_type_name)

    else:
        return redirect(url_for('my_account'))


''' function to calculate the amount onchanging number of users'''


@app.route('/ajax_load_user_amount', methods=['GET', 'POST'])
def ajax_load_user_amount():
    currency_type = session['currency']
    currency = currency_type.lower()
    users_count = request.args.get('users_count')
    user_type = request.args.get('usertype')
    
    current_date = datetime.date(datetime.now())
    user_effective_date = sessions.query(UserPricing.effective_date).filter(UserPricing.user_type_id==user_type).first()[0]

    if user_effective_date <= current_date:
        upper_value = sessions.query(UserPricing.upper).filter(UserPricing.user_type_id==user_type).order_by(UserPricing.user_pricing_id.desc()).first()[0]

    else:
        upper_value = sessions.query(UserPricingHistory.upper).filter(UserPricingHistory.user_type_id==user_type).filter(UserPricingHistory.effective_date<=current_date).order_by(UserPricingHistory.user_pricing_his_id.desc()).limit(1).first()[0]

    if upper_value == '':
        maxvalue = ''
    else:
        maxvalue = int(upper_value)

    if users_count != "0":
        if user_effective_date <= current_date:
            user_pricing_list = sessions.query(UserPricing).with_entities(UserPricing.lower,UserPricing.upper,getattr(UserPricing,currency)).filter(UserPricing.user_type_id==user_type).all()

        else:
            usr_cnt = sessions.query(UserPricing).filter(UserPricing.user_type_id==user_type).count()

            user_pricing_list = sessions.query(UserPricingHistory).with_entities(UserPricingHistory.lower,UserPricingHistory.upper,getattr(UserPricingHistory,currency)).filter(UserPricingHistory.user_type_id==user_type).filter(UserPricingHistory.effective_date<=current_date).order_by(UserPricingHistory.user_pricing_his_id.desc()).limit(usr_cnt).all()

        for user_pricing_lists in user_pricing_list:
            lower_value = user_pricing_lists[0]
            # new_lower_value=int(lower_vale)
            # print(new_lower_value)
            upper_value = user_pricing_lists[1]
            usr_pricing_amount = user_pricing_lists[2]
            if upper_value != "":
                if(int(lower_value) <= int(users_count) and int(upper_value) >= int(users_count)):
                    amount = usr_pricing_amount

            else:
                lower = lower_value
                new_lower_val = lower.replace('>', '')
                if(int(new_lower_val) < int(users_count)):
                    amount = usr_pricing_amount

    else:
        amount = 0
    # print(amount,"amount")
    amount_and_maxvalue = str(amount)+"@"+str(maxvalue)
    return str(amount_and_maxvalue)


''' function to calculate the amount onselecting the customized products'''


@app.route('/ajax_load_customize', methods=['GET', 'POST'])
def ajax_load_customize():
    allVals = request.args.get('allVals')
    print(allVals,"allVals")
    if allVals != '""':
        newvalue = str(allVals).replace("'", "").replace('"', "")
        li = list(newvalue.split(","))
        list_count = len(li)
        currency_type = session['currency']
        currency = currency_type.lower()
        amount_list = []
        sub_lists = ''
        pkg_amount = 0
        effective_date = sessions.query(PackageList.effective_date).first()[0]
        current_date = datetime.date(datetime.now())

        if effective_date <= current_date:
            customize_amount = sessions.query(PackageList).with_entities(getattr(PackageList,currency).label('package_amount')).filter_by(pkg_id=4).first()[0]
            # cursor.execute(
            #     f"select {currency} as package_amount from package_list where pkg_id=4 ")
            # customize_amount = cursor.fetchone()[0]
            total_customize_amount = list_count*customize_amount

            all_product_id = sessions.query(PackageList).with_entities(PackageList.product_id,PackageList.pkg_id, getattr(PackageList,currency)).filter(PackageList.pkg_id!=4, PackageList.pkg_id!=5).order_by(PackageList.pkg_id.asc()).all()
            # cursor.execute(
            #     f"select product_id,pkg_id,{currency} from package_list where pkg_id!=4 order by pkg_id asc")
            # all_product_id = cursor.fetchall()
        else:
            customize_amount = sessions.query(PackageListHistory).with_entities(getattr(PackageListHistory,currency).label('package_amount')).filter_by(pkg_id=4).filter(PackageListHistory.effective_date <= current_date ).first()[0]
            total_customize_amount = list_count*customize_amount

            prod_id_count = sessions.query(PackageList).filter(PackageList.pkg_id!=4).count()

            all_product_id = sessions.query(PackageListHistory).with_entities(PackageListHistory.product_id,PackageListHistory.pkg_id, getattr(PackageListHistory,currency)).filter(PackageListHistory.pkg_id!=4, PackageListHistory.pkg_id!=5).filter(PackageListHistory.effective_date <= current_date ).order_by(PackageListHistory.pkg_his_id.desc()).limit(prod_id_count).all()
            all_product_id.sort(key = lambda x: x[1])
            # cursor.execute(
            #     f"select product_id,pkg_id,{currency} from package_list where pkg_id!=4 order by pkg_id asc")
            # all_product_id1 = cursor.fetchall()

        for all_product_ids in all_product_id:
            sub_list = list(all_product_ids[0].split(","))
            test_list = li
            flag = 0
            if((set(sub_list) & set(test_list)) == set(sub_list)):
                flag = 1
            if (flag):
                if all_product_ids[1] == 1:
                    sub_lists = sub_list
                    pkg_amount = all_product_ids[2]
                elif all_product_ids[1] == 2:
                    sub_lists = sub_list
                    pkg_amount = all_product_ids[2]
                elif all_product_ids[1] == 3:
                    sub_lists = sub_list
                    pkg_amount = all_product_ids[2]

            # else :
            #     amount=list_count*amount
        #  sub_list_len=len(sub_lists)
        print(sub_lists,"sub_lists")
        print(list_count,len(sub_lists))
        balance_count = list_count-len(sub_lists)
        print(balance_count,"balance_count",pkg_amount)
        total_amount = pkg_amount+(balance_count*customize_amount)
        discount_amount = total_customize_amount-total_amount

    else:
        total_customize_amount = 0
        total_amount = 0
        discount_amount = 0
    # print(total_customize_amount,"er",discount_amount,"dfde",total_amount)
    amount_list = str(total_customize_amount)+"," + \
        str(discount_amount)+","+str(total_amount)
    print(total_amount,"total_amount")
    #  amount_list.append({'total_customize_amount':total_customize_amount,'total_amount':total_amount,'discount_amount':discount_amount})
    return str(amount_list)

    #  for li in li:
    #      print(enumerate(list),"newvalueli")


''' function to calculate the amount onselecting the customized products in upgrade packages '''


@app.route('/ajax_load_customize_upgrade', methods=['GET', 'POST'])
def ajax_load_customize_upgrade():
    allVals = request.args.get('allVals')
    # print(allVals,"allVals")
    if allVals != '""':
        newvalue = str(allVals).replace("'", "").replace('"', "")
        li = list(newvalue.split(","))
        list_count = len(li)
        currency = session['currency']
        amount_list = []
        sub_lists = ''
        pkg_amount = 0

       

        cursor.execute(
            f"select {currency} as package_amount from package_list where pkg_id=4 ")
        customize_amount = cursor.fetchone()[0]
        total_customize_amount = list_count*customize_amount

        cursor.execute(
            f"select product_id,pkg_id,{currency} from package_list where pkg_id!=4 order by pkg_id asc")
        all_product_id = cursor.fetchall()
        for all_product_ids in all_product_id:
            sub_list = list(all_product_ids[0].split(","))
            test_list = li
            flag = 0
            if((set(sub_list) & set(test_list)) == set(sub_list)):
                flag = 1

            # printing result
            if (flag):
                if all_product_ids[1] == 1:
                    sub_lists = sub_list
                    pkg_amount = all_product_ids[2]
                elif all_product_ids[1] == 2:
                    sub_lists = sub_list
                    pkg_amount = all_product_ids[2]
                else:
                    sub_lists = sub_list
                    pkg_amount = all_product_ids[2]

            # else :
            #     amount=list_count*amount
        #  sub_list_len=len(sub_lists)
        balance_count = list_count-len(sub_lists)
        total_amount = pkg_amount+(balance_count*customize_amount)
        discount_amount = total_customize_amount-total_amount

    else:
        total_customize_amount = 0
        total_amount = 0
        discount_amount = 0
    print(total_customize_amount,"er",discount_amount,"dfde",total_amount)
    amount_list = str(total_customize_amount)+"," + \
        str(discount_amount)+","+str(total_amount)
    #  amount_list.append({'total_customize_amount':total_customize_amount,'total_amount':total_amount,'discount_amount':discount_amount})
    return str(amount_list)

    #  for li in li:
    #      print(enumerate(list),"newvalueli")



# @app.route('/ajax_load_customize_upgrade', methods=['GET', 'POST'])
# def ajax_load_customize_upgrade():
#     allVals = request.args.get('allVals')
#     print(allVals,"allVals")
#     if allVals != '""':
#         newvalue = str(allVals).replace("'", "").replace('"', "")
#         li = list(newvalue.split(","))
        

#         userid = session['userid']

#         cursor.execute(f"select count(*) from product_selection_list where user_id={userid}")
#         prod_select_count = cursor.fetchone()[0]
#         if prod_select_count == 0:
#             cursor.execute(f"select count(*) from alert_package_purchase where user_id={userid}")
#             alert_prod_count = cursor.fetchone()[0]
#             if alert_prod_count == 0:
#                 cursor.execute(
#                     f"select user_id,pkg_id,product_id,amount,actual_amount,discount from package_purchase_list where user_id={userid} and latest_entry=1 ")
#                 prod_selec_list = cursor.fetchone()[2]

#             else:
#                 cursor.execute(
#                     f"select user_id,pkg_id,product_id,amount,actual_amount,discount from alert_package_purchase where user_id={userid} and latest_entry=1 ")
#                 prod_selec_list = cursor.fetchone()[2]

               
#         else:
#             cursor.execute(
#                 f"select user_id,pkg_id,product_id,amount,actual_amount,discount from product_selection_list where user_id={userid}  ")
#             prod_selec_list = cursor.fetchone()[2]



#         # cursor.execute(
#         #         f"select user_id,pkg_id,product_id,amount,actual_amount,discount from package_purchase_list where user_id={userid} and latest_entry=1 ")
#         # prod_selec_list = cursor.fetchone()[2]
#         # print(prod_selec_list)
#         # my_list = prod_selec_list.split(",")
        
#         # li = [i for i in li if i not in my_list] 

#         # if (prod_selec_list in li): 
#         #     remainprod=li.remove(prod_selec_list)
#         #     print ("Element Exists")
#         #     print(li)


#         list_count = len(li)
#         print(list_count,"list_count")
#         currency = session['currency']
#         amount_list = []
#         sub_lists = ''
#         pkg_amount = 0

        

#         cursor.execute(
#             f"select {currency} as package_amount from package_list where pkg_id=4 ")
#         customize_amount = cursor.fetchone()[0]
#         total_customize_amount = list_count*customize_amount
#         print(total_customize_amount,"total_customize_amount")
#         cursor.execute(
#             f"select product_id,pkg_id,{currency} from package_list where pkg_id!=4 order by pkg_id asc")
#         all_product_id = cursor.fetchall()
#         for all_product_ids in all_product_id:
#             sub_list = list(all_product_ids[0].split(","))
#             test_list = li
#             flag = 0
#             print(sub_list)
#             print(test_list,"Dd")
#             if((set(sub_list) & set(test_list)) == set(sub_list)):
#                 flag = 1
#             print(flag,"flag")

#             # printing result
#             if (flag):
#                 print(all_product_ids[1],"all_product_ids[1]")
#                 if all_product_ids[1] == 1:
#                     sub_lists = sub_list
#                     pkg_amount = all_product_ids[2]
#                 elif all_product_ids[1] == 2:
#                     print(all_product_ids[1])
#                     sub_lists = sub_list
#                     pkg_amount = all_product_ids[2]
#                 else:
#                     sub_lists = sub_list
#                     pkg_amount = all_product_ids[2]

#             # else :
#             #     amount=list_count*amount
#         #  sub_list_len=len(sub_lists)
#         print(len(sub_lists))
#         balance_count = list_count-len(sub_lists)
#         total_amount = pkg_amount+(balance_count*customize_amount)
#         discount_amount = total_customize_amount-total_amount
#         print(balance_count)
#         print(total_amount)
#         print(total_customize_amount)

#     else:
#         total_customize_amount = 0
#         total_amount = 0
#         discount_amount = 0

#     amount_list = str(total_customize_amount)+"," + \
#         str(discount_amount)+","+str(total_amount)
#     #  amount_list.append({'total_customize_amount':total_customize_amount,'total_amount':total_amount,'discount_amount':discount_amount})
#     return str(amount_list)

#     #  for li in li:
#     #      print(enumerate(list),"newvalueli")


''' function to show the individual packages amount and also the total amount to be paid with gst'''


@app.route('/estimation', methods=['GET', 'POST'])
def estimation():
    if len(session)==0:
        return redirect(url_for('logout'))
    userid = session['userid']
    billing_count = sessions.query(BillingDetails).filter(BillingDetails.user_id == userid).count()
    company_details = sessions.query(CompanyDetails).filter(CompanyDetails.user_id==userid).first()
    country_id = company_details.country_id

    comp_country_name = sessions.query(Country.country_name).filter(Country.country_id==country_id).first()[0]

    if billing_count == 0:
        count_values = get_all_count()
        user_type_name = sessions.query(UserType.user_type_name).order_by(UserType.user_type_id.asc())

        selected_pkg_prod = sessions.query(ProductSelectionList, PackageList).with_entities(ProductSelectionList.pkg_id, PackageList.pkg_name, ProductSelectionList.product_id, ProductSelectionList.amount).join(PackageList, ProductSelectionList.pkg_id == PackageList.pkg_id).filter(ProductSelectionList.user_id == userid).order_by(ProductSelectionList.selc_id.desc()).first()

        selected_users_amount = sessions.query(UserSelectionList).with_entities(UserSelectionList.admin_user_count, UserSelectionList.admin_user_amount, UserSelectionList.general_user_count, UserSelectionList.general_user_amount,UserSelectionList.limited_user_count, UserSelectionList.limited_user_amount, UserSelectionList.amount, UserSelectionList.user_selc_id,UserSelectionList.billing_frequency, UserSelectionList.actual_amount,UserSelectionList.discount).order_by(UserSelectionList.user_selc_id.desc()).first()

        cloud_pack_amount = sessions.query(CloudSelection, CloudType, CloudPricing ).with_entities(CloudSelection.cloud_id, CloudSelection.amount, CloudType.cl_type_name, CloudPricing.features).join(CloudType, CloudSelection.cl_type_id == CloudType.cl_type_id).join(CloudPricing, CloudSelection.cl_type_id == CloudPricing.cl_type_id).filter(CloudSelection.user_id == userid).order_by(CloudSelection.cloud_id.desc()).first()

        newdate = datetime.date(datetime.now())
        newdates = newdate + relativedelta(years=1, days=-1)
        monthdates = newdate + relativedelta(months=1, days=-1)

        product_list = sessions.query(ProductList).order_by(ProductList.product_id.asc()).all()
        next_renewal_date = newdates
        get_gst_count =  sessions.query(Gst.gst_per).filter(Gst.country_id==country_id).count()
        if get_gst_count > 0:
            new_gst_per = sessions.query(Gst.gst_per).filter(Gst.country_id==country_id,Gst.effective_from_date <= next_renewal_date).order_by(Gst.gst_id.desc()).first()[0]
        else:
            new_gst_per = "0%"

        if request.method == "POST":
            return redirect("/billing_information")

        return render_template('estimation.html', selected_pkg_prod=selected_pkg_prod, product_list=product_list, selected_users_amount=selected_users_amount, cloud_pack_amount=cloud_pack_amount, count_values=count_values, newdates=newdates, monthdates=monthdates, user_type_name=user_type_name,new_gst_per=new_gst_per,comp_country_name=comp_country_name)

    else:
       return redirect(url_for('my_account'))


''' function to change product packages after billing.This function checks whether the date is within the annual alert period.If it is so,there will be no need for payment '''


@app.route('/upgrade_package_oldsss', methods=['GET', 'POST'])
def upgrade_package_oldsss():

    if len(session)==0:
        return redirect(url_for('logout'))

    currency_type = session['currency']
    currency = currency_type.lower()
    # currency = currency_type
    currency_symbol = session['currency_symbol']
    userid = session['userid']
    reg_user_type = sessions.query(RegUsers.user_type).filter(RegUsers.user_id == userid).first()[0]
    email = session['email']
    
    company_id = sessions.query(CompanyDetails.company_id).filter_by(user_id=userid).first()[0]

    location_list = sessions.query(Location).with_entities(Location.location_id,Location.location_name).filter(Location.company_id == company_id).first()
    location_id = location_list[0]
    location_name = location_list[1]
    
    site_admin_db = str("scopiq_site_admin_")+str(company_id)+"_"+str(location_id)
    dms_db = str("scopiq_dms_")+str(company_id)+"_"+str(location_id)
    cms_db = str("scopiq_cms_")+str(company_id)+"_"+str(location_id)
    dsm_db = str("scopiq_dsm_")+str(company_id)+"_"+str(location_id)
    
    dsm_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+dsm_db)
    cms_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+cms_db)
    dms_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+dms_db)
    siteadmin_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+site_admin_db)
    Base = declarative_base()
    siteadmin_session = sessionmaker(bind=siteadmin_engine)
    dms_session = sessionmaker(bind=dms_engine)
    cms_session = sessionmaker(bind=cms_engine)
    dsm_session = sessionmaker(bind=dsm_engine)
    siteadmin_session_set = siteadmin_session()
    dms_session_set = dms_session()
    cms_session_set = cms_session()
    dsm_session_set = dsm_session()
    
    count_values = get_all_count()
    package_list = sessions.query(PackageList).with_entities(PackageList.pkg_id, PackageList.pkg_name, PackageList.product_id, getattr(PackageList,currency).label('package_amount')).order_by(PackageList.pkg_id.asc())

    effective_date = sessions.query(PackageList.effective_date).first()[0]
    current_date = datetime.date(datetime.now())

    if effective_date <= current_date:         
        package_list = sessions.query(PackageList).with_entities(PackageList.pkg_id.label('pkg_id'),PackageList.pkg_name.label('pkg_name'),PackageList.product_id.label('product_id'),getattr(PackageList,currency).label('package_amount')).filter(PackageList.pkg_id != 5).order_by(PackageList.pkg_id.asc())

    else:
        prod_id_count = sessions.query(PackageList).count()

        package_list = sessions.query(PackageListHistory).with_entities(PackageListHistory.pkg_id.label('pkg_id'), PackageListHistory.pkg_name.label('pkg_name'), PackageListHistory.product_id.label('product_id'), getattr(PackageListHistory,currency).label('package_amount')).filter(PackageListHistory.effective_date <= current_date ).filter(PackageListHistory.pkg_id != 5).order_by(PackageListHistory.pkg_his_id.desc()).limit(prod_id_count)

    # if not in in alert period
    current_pkg_prod_id = sessions.query(PackagePurchaseList).with_entities(PackagePurchaseList.pkg_id,PackagePurchaseList.product_id).filter(PackagePurchaseList.user_id == userid).first()

    current_pkg_id = current_pkg_prod_id[0]
    current_prod_id = current_pkg_prod_id[1]
    if reg_user_type == "F":
        current_prod_id = 0

    prod_select_count = sessions.query(ProductSelectionList).filter(ProductSelectionList.user_id == userid).count()

    if prod_select_count == 0:
        alert_prod_count = sessions.query(AlertPackagePurchase).filter(AlertPackagePurchase.user_id == userid).count()

        if alert_prod_count == 0:
            prod_selec_list = sessions.query(PackagePurchaseList).with_entities(PackagePurchaseList.user_id, PackagePurchaseList.pkg_id, PackagePurchaseList.product_id, PackagePurchaseList.amount, PackagePurchaseList.actual_amount, PackagePurchaseList.discount).filter(PackagePurchaseList.user_id == userid, PackagePurchaseList.latest_entry == 1).first()

        else:
            prod_selec_list = sessions.query(AlertPackagePurchase).with_entities(AlertPackagePurchase.user_id, AlertPackagePurchase.pkg_id, AlertPackagePurchase.product_id, AlertPackagePurchase.amount, AlertPackagePurchase.actual_amount, AlertPackagePurchase.discount).filter(AlertPackagePurchase.user_id == userid, AlertPackagePurchase.latest_entry == 1).first()

            # if in in alert period
            current_pkg_id = sessions.query(AlertPackagePurchase.pkg_id).filter(AlertPackagePurchase.user_id == userid).first()[0]

    else:
        prod_selec_list = sessions.query(ProductSelectionList).with_entities(ProductSelectionList.user_id, ProductSelectionList.pkg_id, ProductSelectionList.product_id, ProductSelectionList.amount, ProductSelectionList.actual_amount, ProductSelectionList.discount).filter(ProductSelectionList.user_id == userid).first()

    product_list = sessions.query(ProductList).order_by(ProductList.product_id.asc()).all()

    prod_purchase = sessions.query(PackagePurchaseList).with_entities(PackagePurchaseList.renewal_date, PackagePurchaseList.amount, PackagePurchaseList.pkg_id, PackagePurchaseList.product_id).filter(PackagePurchaseList.user_id==userid, PackagePurchaseList.latest_entry==1).first()
    prod_renewal_date = prod_purchase[0]
    paid_amount = prod_purchase[1]
    current_package_id = prod_purchase[2]
    current_product_id = prod_purchase[3]

    date_1 = prod_renewal_date
    current_date = datetime.date(datetime.now())
    payment_date = current_date.strftime('%Y-%m-%d')
    date_2 = current_date
    remaining_months = alert_period(date_1,date_2)
    if remaining_months != "error":
        alert_time_period = remaining_months[0]['alert']
    else:
        alert_time_period = ''

    # if free trial there is no alert period and assign current product as empty
    if reg_user_type == "F":
        current_prod_id = 0
        alert_time_period = ''

    if request.method == "POST":
        try:
            # print("try")
            addtocart = request.form['addtocart']
            packagepostvalue = 'pkg_name_'+addtocart
            pkg_name = request.form.get(packagepostvalue)
            amountpostvalue = 'pkg_amount_'+addtocart
            pkg_amount = request.form.get(amountpostvalue)
            print(pkg_amount,"pkg_amount")
            cus_pro = request.form.getlist('cus_pro')
            if addtocart == "4":
                product_id = ','.join(cus_pro)
                new_pkg_amount = request.form['totamont']
                print(new_pkg_amount,"new_pkg_amount")
                discount_amount = request.form['discount_amount']
                actual_amount = request.form['actual_amount']
            else:
                #cursor.execute(
                    #f"select product_id from package_list where pkg_id={addtocart}")
                #product_id = cursor.fetchone()[0]
                product_id = sessions.query(PackageList.product_id).filter(PackageList.pkg_id == addtocart).first()[0]
                new_pkg_amount = pkg_amount
                discount_amount = 0
                actual_amount = pkg_amount

            siteadmin_userid = siteadmin_session_set.query(Users.user_id).filter(Users.email==email).first()[0]

            # num_months = (date_1.year - date_2.year) * 12 + (date_1.month - date_2.month)
            if remaining_months != "error":
                num_months = remaining_months[0]['months']
                alert_time_period = remaining_months[0]['alert']
                if reg_user_type == "F":
                    alert_time_period = 0
                pkg_renewal_date = prod_renewal_date.strftime('%Y-%m-%d')
                
                if alert_time_period == 0:
                    # print("alert_period")
                    if current_package_id != 4: # pkg to customization
                        if addtocart != "4":
                            print("else","pkg-pkg")
                            if int(new_pkg_amount) > int(paid_amount):
                                balance_prod_amount = int(new_pkg_amount) - int(paid_amount)
                                balance_amount = float(balance_prod_amount*float(num_months/12))

                            else: #(elif int(new_pkg_amount) < int(paid_amount):)
                                balance_amount = 0
                                balance_prod_amount = 0

                        else:#(if addtocart == 4:)
                            print("else","pkg-cus")
                            test_list = list(current_product_id.split(","))
                            sub_list = list(product_id.split(","))
                            print(test_list,sub_list,"hjk")
                            # result =  all(elem in list1  for elem in list2)
            
                            if((set(sub_list) & set(test_list)) == set(test_list)):
                                flag = 1
                            else:
                                flag = 0
                            if flag == 1:
                                print(new_pkg_amount,paid_amount)
                                if int(new_pkg_amount) > int(paid_amount):
                                    print("if--flag1")
                                    balance_prod_amount = int(new_pkg_amount) - int(paid_amount)
                                    # remaining_prod = len(test_list) - len(sub_list)
                                    # balance_prod_amount = int(remaining_prod * pkg_amount) 
                                    balance_amount = float(balance_prod_amount*float(num_months/12))

                                else: #(elif int(new_pkg_amount) < int(paid_amount):)
                                    balance_amount = 0
                                    balance_prod_amount = 0

                            else:
                                print("if--flag0")
                                print(new_pkg_amount,paid_amount)
                                if int(new_pkg_amount) > int(paid_amount):
                                    print(new_pkg_amount,paid_amount)
                                    current_prod_list = list(current_product_id.split(","))
                                    current_prod_length = len(current_prod_list)

                                    selected_prod_list = list(product_id.split(","))
                                    selected_prod_length = len(selected_prod_list)
                                    print(current_prod_length,selected_prod_length)

                                    balance_prod_list = list(set(selected_prod_list) - set(current_prod_list)) 
                                    
                                    balance_prod_length = len(balance_prod_list)

                                    # cursor.execute(f"select {currency} as package_amount from package_list where pkg_id=4 ")
                                    # customize_amount = cursor.fetchone()[0]
                                    customize_amount = pkg_amount

                                    balance_prod_amount = balance_prod_length * customize_amount
                                    balance_amount = float(balance_prod_amount*float(num_months/12))

                                else: #(elif int(new_pkg_amount) < int(paid_amount):)
                                    balance_amount = 0
                                    balance_prod_amount = 0
                            # balance_amount = float(float(new_pkg_amount)*float((num_months/12)))
                            # print(balance_amount,product_id,current_product_id)

                            # new_prod_list(product_id,current_product_id) # new_prod_list(new_products,old_products)

                        if reg_user_type == "F":  # if free trial, calculate full amount
                            balance_amount = balance_prod_amount
                        else:
                            balance_amount = balance_amount

                        print(balance_amount,"HARTHIK balance_amount")
                        print(reg_user_type,'Keerthi')
                        if balance_amount != 0:
                            result = insert_prod_selection(userid, addtocart, product_id, balance_amount, actual_amount, discount_amount)
                            cloud_selec_count = sessions.query(CloudSelection).filter(CloudSelection.user_id == userid).count()

                            # for free trial cloud will set default value
                            if reg_user_type == "F":
                                if cloud_selec_count != 0:
                                    sessions.query(CloudSelection).filter(CloudSelection.user_id == userid).delete()
                                inserted_cloud = CloudSelection(cl_type_id=1, amount=0, user_id=userid,status=1)
                                sessions.add(inserted_cloud)
                                sessions.flush()
                                sessions.commit()
                            flash('Added To Cart',"success")

                        else:
                            sessions.query(PackagePurchaseList).filter(PackagePurchaseList.user_id == userid).update({PackagePurchaseList.pkg_id: addtocart, PackagePurchaseList.product_id: product_id})

                            # cursor.execute(f"update package_purchase_list set pkg_id={addtocart},product_id='{product_id}' where user_id ={userid} ")

                            ''' insert product list in siteadmin  '''  

                            siteadmin_session_set.query(Packages).filter_by(user_id=siteadmin_userid).delete()

                            # cursor1.execute(f"delete from package_list where user_id='{siteadmin_userid}' ")
                            product_id_list = list(product_id.split(","))
                            for pkg_product_id in product_id_list:
                                product_id = encryptdata(pkg_product_id)
                                insertsite_prod = Packages(user_id=siteadmin_userid, product_id=product_id, link='localhost:5003', renewal_date=pkg_renewal_date)
                                siteadmin_session_set.add(insertsite_prod)
                                siteadmin_session_set.flush()

                                # cursor1.execute(
                                #     f"INSERT into package_list(user_id,product_id,link,renewal_date) values {(siteadmin_userid, product_id,'localhost:5003',pkg_renewal_date )} ")

                            sessions.commit()
                            siteadmin_session_set.commit()    
                            flash("Your Payment will be changed from next billing","success")


                    else: # customization to customization
                        # print("hi")
                        # print("else")
                        test_list = list(current_product_id.split(","))
                        sub_list = list(product_id.split(","))
                        # print(test_list,sub_list,"hjk")
                        # result =  all(elem in list1  for elem in list2)
        
                        if((set(sub_list) & set(test_list)) == set(test_list)):
                            flag = 1
                        else:
                            flag = 0
                        if flag == 1:
                            print("cus-cusflag1",new_pkg_amount,paid_amount)
                            if int(new_pkg_amount) > int(paid_amount):
                                balance_prod_amount = int(new_pkg_amount) - int(paid_amount)
                                balance_amount = float(balance_prod_amount*float(num_months/12))

                            else: #(elif int(new_pkg_amount) < int(paid_amount):)
                                balance_amount = 0
                                balance_prod_amount = 0

                        else:
                            print("cus-cusflag0",new_pkg_amount,paid_amount)
                            if int(new_pkg_amount) > int(paid_amount):
                                # print(new_pkg_amount,paid_amount)
                                current_prod_list = list(current_product_id.split(","))
                                current_prod_length = len(current_prod_list)

                                selected_prod_list = list(product_id.split(","))
                                selected_prod_length = len(selected_prod_list)
                                # print(current_prod_length,selected_prod_length)

                                balance_prod_list = list(set(selected_prod_list) - set(current_prod_list)) 
                                
                                balance_prod_length = len(balance_prod_list)

                                # cursor.execute(f"select {currency} as package_amount from package_list where pkg_id=4 ")
                                # customize_amount = cursor.fetchone()[0]
                                customize_amount = pkg_amount

                                balance_prod_amount = balance_prod_length * customize_amount
                                balance_amount = float(balance_prod_amount*float(num_months/12))

                            else: #(elif int(new_pkg_amount) < int(paid_amount):)
                                balance_amount = 0
                                balance_prod_amount = 0
                        # balance_amount = float(float(new_pkg_amount)*float((num_months/12)))
                        # print(balance_amount,product_id,current_product_id)

                        # new_prod_list(product_id,current_product_id) # new_prod_list(new_products,old_products)

                        if reg_user_type == "F":  # if free trial, calculate full amount
                            balance_amount = balance_prod_amount
                        else:
                            balance_amount = balance_amount


                        if balance_amount != 0:
                            result = insert_prod_selection(userid, addtocart, product_id, balance_amount, actual_amount, discount_amount)
                            cloud_selec_count = sessions.query(CloudSelection).filter(CloudSelection.user_id == userid).count()
                            # for free trial cloud will set default value
                            if reg_user_type == "F":
                                if cloud_selec_count != 0:
                                    sessions.query(CloudSelection).filter(CloudSelection.user_id == userid).delete()
                                inserted_cloud = CloudSelection(cl_type_id=1, amount=0, user_id=userid,status=1)
                                sessions.add(inserted_cloud)
                                sessions.flush()
                                sessions.commit()
                            flash('Added To Cart',"success")

                        else:
                            sessions.query(PackagePurchaseList).filter(PackagePurchaseList.user_id == userid).update({PackagePurchaseList.pkg_id: addtocart, PackagePurchaseList.product_id: product_id})

                            # cursor.execute(f"update package_purchase_list set pkg_id={addtocart},product_id='{product_id}' where user_id ={userid} ")

                            ''' insert product list in siteadmin  '''  

                            siteadmin_session_set.query(Packages).filter_by(user_id=siteadmin_userid).delete()

                            # cursor1.execute(f"delete from package_list where user_id='{siteadmin_userid}' ")
                            product_id_list = list(product_id.split(","))
                            for pkg_product_id in product_id_list:
                                product_id = encryptdata(pkg_product_id)
                                insertsite_prod = Packages(user_id=siteadmin_userid, product_id=product_id, link='localhost:5003', renewal_date=pkg_renewal_date)
                                siteadmin_session_set.add(insertsite_prod)
                                siteadmin_session_set.flush()

                                # cursor1.execute(
                                #     f"INSERT into package_list(user_id,product_id,link,renewal_date) values {(siteadmin_userid, product_id,'localhost:5003',pkg_renewal_date )} ")

                            sessions.commit()
                            siteadmin_session_set.commit()   

                            flash("Your Payment will be changed from next billing","success")

                else:
                    sessions.query(AlertPackagePurchase).filter(AlertPackagePurchase.user_id==userid).delete()
                    # cursor.execute(f"delete from alert_package_purchase where user_id={userid}")
                   
                    inserted_alert_pkg = AlertPackagePurchase(user_id=userid, pkg_id=addtocart, product_id=product_id, amount=new_pkg_amount, actual_amount=actual_amount, discount=discount_amount, currency_type=currency, currency_symbol=currency_symbol, latest_entry=1, payment_date=payment_date, renewal_date=pkg_renewal_date)
                    sessions.add(inserted_alert_pkg)
                    sessions.flush()

                    test_list = list(current_product_id.split(","))
                    sub_list = list(product_id.split(","))
                    # print(test_list,sub_list,"hjk")
    
                    if((set(sub_list) & set(test_list)) == set(test_list)):
                        flag = 1
                    else:
                        flag = 0
                    # print(flag,"flagsss")
                    if flag == 1:
                        # print("flasg11",product_id)
                        product_id_list = list(product_id.split(","))
                        # print("ifproduct_id_list",product_id_list)
                    else:
                        # print("flag0")
                        balance_products =  list(set(sub_list) - set(test_list))
                        # print(balance_products,"balance_products")
                        products_in_alert = test_list + balance_products
                        # print(products_in_alert,"products_in_alert")
                        product_id_list = products_in_alert
                        # print("elseproduct_id_list",product_id_list)

                    # print("product_id_list",product_id_list)
                    ''' insert product list in siteadmin  '''  
                    siteadmin_session_set.query(Packages).filter_by(user_id=siteadmin_userid).delete()
                    
                    # cursor1.execute(f"delete from package_list where user_id='{siteadmin_userid}' ")
                    
                    for pkg_product_id in product_id_list:
                        print("pkg_product_id",pkg_product_id)
                        # product_id = pkg_product_id
                        if pkg_product_id != "":
                            product_id = encryptdata(pkg_product_id)
                            insertsite_prod = Packages(user_id=siteadmin_userid, product_id=product_id, link='localhost:5003', renewal_date=pkg_renewal_date)
                            siteadmin_session_set.add(insertsite_prod)
                            siteadmin_session_set.flush()
                        # cursor1.execute(
                        #     f"INSERT into package_list(user_id,product_id,link,renewal_date) values {(siteadmin_userid, product_id,'localhost:5003',pkg_renewal_date )} ")

                    sessions.commit()
                    siteadmin_session_set.commit()
                    flash('No need for payment since you upgrade in the alert period',"success")


            else:
                flash("Please Enter Alert Interval List","error")

            return redirect(url_for('upgrade_package'))

        except Exception as ex:
            sessions.rollback()
            flash(str(ex),"error")
            return redirect(url_for('upgrade_package'))
    
    print('Harthik',current_prod_id)
    return render_template('upgrade_package.html', package_list=package_list, product_list=product_list, count_values=count_values, prod_selec_list=prod_selec_list,current_pkg_id=current_pkg_id,alert_time_period=alert_time_period,current_paid_package_id=current_package_id,current_prod_id=current_prod_id,reg_user_type=reg_user_type)




@app.route('/upgrade_package', methods=['GET', 'POST'])
def upgrade_package():

    if len(session)==0:
        return redirect(url_for('logout'))

    currency_type = session['currency']
    currency = currency_type.lower()
    # currency = currency_type
    currency_symbol = session['currency_symbol']
    userid = session['userid']
    reg_user_type = sessions.query(RegUsers.user_type).filter(RegUsers.user_id == userid).first()[0]
    email = session['email']
    
    company_id = sessions.query(CompanyDetails.company_id).filter_by(user_id=userid).first()[0]

    location_list = sessions.query(Location).with_entities(Location.location_id,Location.location_name).filter(Location.company_id == company_id).first()
    location_id = location_list[0]
    location_name = location_list[1]
    
    site_admin_db = str("scopiq_site_admin_")+str(company_id)+"_"+str(location_id)
    dms_db = str("scopiq_dms_")+str(company_id)+"_"+str(location_id)
    cms_db = str("scopiq_cms_")+str(company_id)+"_"+str(location_id)
    dsm_db = str("scopiq_dsm_")+str(company_id)+"_"+str(location_id)
    cams_db = str("scopiq_cams_")+str(company_id)+"_"+str(location_id)
    capa_db = str("scopiq_capa_")+str(company_id)+"_"+str(location_id)
    
    capa_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+capa_db)
    cams_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+cams_db)
    dsm_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+dsm_db)
    cms_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+cms_db)
    dms_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+dms_db)
    siteadmin_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+site_admin_db)
    Base = declarative_base()
    siteadmin_session = sessionmaker(bind=siteadmin_engine)
    dms_session = sessionmaker(bind=dms_engine)
    cms_session = sessionmaker(bind=cms_engine)
    dsm_session = sessionmaker(bind=dsm_engine)
    cams_session = sessionmaker(bind=cams_engine)
    capa_session = sessionmaker(bind=capa_engine)
    
    siteadmin_session_set = siteadmin_session()
    dms_session_set = dms_session()
    cms_session_set = cms_session()
    dsm_session_set = dsm_session()
    cams_session_set = cams_session()
    capa_session_set = capa_session()
    
    count_values = get_all_count()
    package_list = sessions.query(PackageList).with_entities(PackageList.pkg_id, PackageList.pkg_name, PackageList.product_id, getattr(PackageList,currency).label('package_amount')).order_by(PackageList.pkg_id.asc())

    effective_date = sessions.query(PackageList.effective_date).first()[0]
    current_date = datetime.date(datetime.now())

    if effective_date <= current_date:         
        package_list = sessions.query(PackageList).with_entities(PackageList.pkg_id.label('pkg_id'),PackageList.pkg_name.label('pkg_name'),PackageList.product_id.label('product_id'),getattr(PackageList,currency).label('package_amount')).filter(PackageList.pkg_id != 5).order_by(PackageList.pkg_id.asc())

    else:
        prod_id_count = sessions.query(PackageList).count()

        package_list = sessions.query(PackageListHistory).with_entities(PackageListHistory.pkg_id.label('pkg_id'), PackageListHistory.pkg_name.label('pkg_name'), PackageListHistory.product_id.label('product_id'), getattr(PackageListHistory,currency).label('package_amount')).filter(PackageListHistory.effective_date <= current_date ).filter(PackageListHistory.pkg_id != 5).order_by(PackageListHistory.pkg_his_id.desc()).limit(prod_id_count)

    # if not in in alert period
    current_pkg_prod_id = sessions.query(PackagePurchaseList).with_entities(PackagePurchaseList.pkg_id,PackagePurchaseList.product_id).filter(PackagePurchaseList.user_id == userid).first()

    current_pkg_id = current_pkg_prod_id[0]
    current_prod_id = current_pkg_prod_id[1]
    if reg_user_type == "F":
        current_prod_id = 0

    prod_select_count = sessions.query(ProductSelectionList).filter(ProductSelectionList.user_id == userid).count()

    if prod_select_count == 0:
        alert_prod_count = sessions.query(AlertPackagePurchase).filter(AlertPackagePurchase.user_id == userid).count()

        if alert_prod_count == 0:
            prod_selec_list = sessions.query(PackagePurchaseList).with_entities(PackagePurchaseList.user_id, PackagePurchaseList.pkg_id, PackagePurchaseList.product_id, PackagePurchaseList.amount, PackagePurchaseList.actual_amount, PackagePurchaseList.discount).filter(PackagePurchaseList.user_id == userid, PackagePurchaseList.latest_entry == 1).first()

        else:
            prod_selec_list = sessions.query(AlertPackagePurchase).with_entities(AlertPackagePurchase.user_id, AlertPackagePurchase.pkg_id, AlertPackagePurchase.product_id, AlertPackagePurchase.amount, AlertPackagePurchase.actual_amount, AlertPackagePurchase.discount).filter(AlertPackagePurchase.user_id == userid, AlertPackagePurchase.latest_entry == 1).first()

            # if in in alert period
            current_pkg_id = sessions.query(AlertPackagePurchase.pkg_id).filter(AlertPackagePurchase.user_id == userid).first()[0]

    else:
        prod_selec_list = sessions.query(ProductSelectionList).with_entities(ProductSelectionList.user_id, ProductSelectionList.pkg_id, ProductSelectionList.product_id, ProductSelectionList.amount, ProductSelectionList.actual_amount, ProductSelectionList.discount).filter(ProductSelectionList.user_id == userid).first()

    product_list = sessions.query(ProductList).order_by(ProductList.product_id.asc()).all()

    prod_purchase = sessions.query(PackagePurchaseList).with_entities(PackagePurchaseList.renewal_date, PackagePurchaseList.amount, PackagePurchaseList.pkg_id, PackagePurchaseList.product_id).filter(PackagePurchaseList.user_id==userid, PackagePurchaseList.latest_entry==1).first()
    prod_renewal_date = prod_purchase[0]
    paid_amount = prod_purchase[1]
    current_package_id = prod_purchase[2]
    current_product_id = prod_purchase[3]

    date_1 = prod_renewal_date
    current_date = datetime.date(datetime.now())
    payment_date = current_date.strftime('%Y-%m-%d')
    date_2 = current_date
    remaining_months = alert_period(date_1,date_2)
    if remaining_months != "error":
        alert_time_period = remaining_months[0]['alert']
    else:
        alert_time_period = ''

    # if free trial there is no alert period and assign current product as empty
    ft_prod_id = 1
    if reg_user_type == "F":
        current_prod_id = 0
        alert_time_period = ''
        ft_prod_id = 0

    if request.method == "POST":
        try:
            # print("try")
            addtocart = request.form['addtocart']
            packagepostvalue = 'pkg_name_'+addtocart
            pkg_name = request.form.get(packagepostvalue)
            amountpostvalue = 'pkg_amount_'+addtocart
            pkg_amount = request.form.get(amountpostvalue)
            print(pkg_amount,"pkg_amount")
            cus_pro = request.form.getlist('cus_pro')
            if addtocart == "4":
                product_id = ','.join(cus_pro)
                new_pkg_amount = request.form['totamont']
                print(new_pkg_amount,"new_pkg_amount")
                discount_amount = request.form['discount_amount']
                actual_amount = request.form['actual_amount']
            else:
                #cursor.execute(
                    #f"select product_id from package_list where pkg_id={addtocart}")
                #product_id = cursor.fetchone()[0]
                product_id = sessions.query(PackageList.product_id).filter(PackageList.pkg_id == addtocart).first()[0]
                new_pkg_amount = pkg_amount
                discount_amount = 0
                actual_amount = pkg_amount

            siteadmin_userid = siteadmin_session_set.query(Users.user_id).filter(Users.email==email).first()[0]

            # num_months = (date_1.year - date_2.year) * 12 + (date_1.month - date_2.month)
            if remaining_months != "error":
                num_months = remaining_months[0]['months']
                alert_time_period = remaining_months[0]['alert']
                if reg_user_type == "F":
                    alert_time_period = 0
                pkg_renewal_date = prod_renewal_date.strftime('%Y-%m-%d')
                
                if alert_time_period == 0:
                    # print("alert_period")
                    if current_package_id != 4: # pkg to customization
                        if addtocart != "4":
                            print("else","pkg-pkg")
                            if int(new_pkg_amount) > int(paid_amount):
                                balance_prod_amount = int(new_pkg_amount) - int(paid_amount)
                                balance_amount = float(balance_prod_amount*float(num_months/12))

                            else: #(elif int(new_pkg_amount) < int(paid_amount):)
                                balance_amount = 0
                                balance_prod_amount = 0

                        else:#(if addtocart == 4:)
                            print("else","pkg-cus")
                            test_list = list(current_product_id.split(","))
                            sub_list = list(product_id.split(","))
                            print(test_list,sub_list,"hjk")
                            # result =  all(elem in list1  for elem in list2)
            
                            if((set(sub_list) & set(test_list)) == set(test_list)):
                                flag = 1
                            else:
                                flag = 0
                            if flag == 1:
                                print(new_pkg_amount,paid_amount)
                                if int(new_pkg_amount) > int(paid_amount):
                                    print("if--flag1")
                                    balance_prod_amount = int(new_pkg_amount) - int(paid_amount)
                                    # remaining_prod = len(test_list) - len(sub_list)
                                    # balance_prod_amount = int(remaining_prod * pkg_amount) 
                                    balance_amount = float(balance_prod_amount*float(num_months/12))

                                else: #(elif int(new_pkg_amount) < int(paid_amount):)
                                    balance_amount = 0
                                    balance_prod_amount = 0

                            else:
                                print("if--flag0")
                                print(new_pkg_amount,paid_amount)
                                if int(new_pkg_amount) > int(paid_amount):
                                    print(new_pkg_amount,paid_amount)
                                    current_prod_list = list(current_product_id.split(","))
                                    current_prod_length = len(current_prod_list)
                                    print(current_prod_list,'current_prod_list')

                                    selected_prod_list = list(product_id.split(","))
                                    selected_prod_length = len(selected_prod_list)

                                    print(current_prod_length,selected_prod_length)

                                    print(selected_prod_list,'selected_prod_list')

                                    balance_prod_list = list(set(selected_prod_list) - set(current_prod_list)) 
                                    
                                    balance_prod_length = len(balance_prod_list)
                                    print(balance_prod_length,'balance_prod_length')

                                    # cursor.execute(f"select {currency} as package_amount from package_list where pkg_id=4 ")
                                    # customize_amount = cursor.fetchone()[0]
                                    customize_amount = pkg_amount

                                    balance_prod_amount = int(balance_prod_length) * int(customize_amount)

                                    print(balance_prod_amount,'balance_prod_amount')


                                    balance_amount = float(balance_prod_amount*float(num_months/12))

                                    print(balance_amount,'balance_amount')

                                else: #(elif int(new_pkg_amount) < int(paid_amount):)
                                    balance_amount = 0
                                    balance_prod_amount = 0
                            # balance_amount = float(float(new_pkg_amount)*float((num_months/12)))
                            # print(balance_amount,product_id,current_product_id)

                            # new_prod_list(product_id,current_product_id) # new_prod_list(new_products,old_products)

                        if reg_user_type == "F":  # if free trial, calculate full amount
                            balance_amount = balance_prod_amount
                        else:
                            balance_amount = balance_amount
                        print(balance_amount,"balance_amount")

                        if balance_amount != 0:
                            result = insert_prod_selection(userid, addtocart, product_id, balance_amount, actual_amount, discount_amount)
                            cloud_selec_count = sessions.query(CloudSelection).filter(CloudSelection.user_id == userid).count()

                            # for free trial cloud will set default value
                            if reg_user_type == "F":
                                if cloud_selec_count != 0:
                                    sessions.query(CloudSelection).filter(CloudSelection.user_id == userid).delete()
                                inserted_cloud = CloudSelection(cl_type_id=1, amount=0, user_id=userid,status=1)
                                sessions.add(inserted_cloud)
                                sessions.flush()
                                sessions.commit()
                            flash('Added To Cart',"success")

                        else:
                            sessions.query(PackagePurchaseList).filter(PackagePurchaseList.user_id == userid).update({PackagePurchaseList.pkg_id: addtocart, PackagePurchaseList.product_id: product_id})

                            # cursor.execute(f"update package_purchase_list set pkg_id={addtocart},product_id='{product_id}' where user_id ={userid} ")

                            ''' insert product list in siteadmin  '''  

                            siteadmin_session_set.query(Packages).filter_by(user_id=siteadmin_userid).delete()

                            # cursor1.execute(f"delete from package_list where user_id='{siteadmin_userid}' ")
                            product_id_list = list(product_id.split(","))
                            for pkg_product_id in product_id_list:
                                product_id = encryptdata(pkg_product_id)
                                insertsite_prod = Packages(user_id=siteadmin_userid, product_id=product_id, link='localhost:5003', renewal_date=pkg_renewal_date)
                                siteadmin_session_set.add(insertsite_prod)
                                siteadmin_session_set.flush()

                                # cursor1.execute(
                                #     f"INSERT into package_list(user_id,product_id,link,renewal_date) values {(siteadmin_userid, product_id,'localhost:5003',pkg_renewal_date )} ")

                            sessions.commit()
                            siteadmin_session_set.commit()    
                            flash("Your Payment will be changed from next billing","success")


                    else: # customization to customization
                        # print("hi")
                        # print("else")
                        test_list = list(current_product_id.split(","))
                        sub_list = list(product_id.split(","))
                        # print(test_list,sub_list,"hjk")
                        # result =  all(elem in list1  for elem in list2)
        
                        if((set(sub_list) & set(test_list)) == set(test_list)):
                            flag = 1
                        else:
                            flag = 0
                        if flag == 1:
                            print("cus-cusflag1",new_pkg_amount,paid_amount)
                            if int(new_pkg_amount) > int(paid_amount):
                                balance_prod_amount = int(new_pkg_amount) - int(paid_amount)
                                balance_amount = float(balance_prod_amount*float(num_months/12))

                            else: #(elif int(new_pkg_amount) < int(paid_amount):)
                                balance_amount = 0
                                balance_prod_amount = 0

                        else:
                            print("cus-cusflag0",new_pkg_amount,paid_amount)
                            if int(new_pkg_amount) > int(paid_amount):
                                # print(new_pkg_amount,paid_amount)
                                current_prod_list = list(current_product_id.split(","))
                                current_prod_length = len(current_prod_list)

                                selected_prod_list = list(product_id.split(","))
                                selected_prod_length = len(selected_prod_list)
                                # print(current_prod_length,selected_prod_length)

                                balance_prod_list = list(set(selected_prod_list) - set(current_prod_list)) 
                                
                                balance_prod_length = len(balance_prod_list)

                                # cursor.execute(f"select {currency} as package_amount from package_list where pkg_id=4 ")
                                # customize_amount = cursor.fetchone()[0]
                                customize_amount = pkg_amount

                                balance_prod_amount = int(balance_prod_length) * int(customize_amount)
                                balance_amount = float(balance_prod_amount*float(num_months/12))

                            else: #(elif int(new_pkg_amount) < int(paid_amount):)
                                balance_amount = 0
                                balance_prod_amount = 0
                        # balance_amount = float(float(new_pkg_amount)*float((num_months/12)))
                        # print(balance_amount,product_id,current_product_id)

                        # new_prod_list(product_id,current_product_id) # new_prod_list(new_products,old_products)

                        if reg_user_type == "F":  # if free trial, calculate full amount
                            balance_amount = balance_prod_amount
                        else:
                            balance_amount = balance_amount


                        if balance_amount != 0:
                            result = insert_prod_selection(userid, addtocart, product_id, balance_amount, actual_amount, discount_amount)
                            cloud_selec_count = sessions.query(CloudSelection).filter(CloudSelection.user_id == userid).count()
                            # for free trial cloud will set default value
                            if reg_user_type == "F":
                                if cloud_selec_count != 0:
                                    sessions.query(CloudSelection).filter(CloudSelection.user_id == userid).delete()
                                inserted_cloud = CloudSelection(cl_type_id=1, amount=0, user_id=userid,status=1)
                                sessions.add(inserted_cloud)
                                sessions.flush()
                                sessions.commit()
                            flash('Added To Cart',"success")

                        else:
                            sessions.query(PackagePurchaseList).filter(PackagePurchaseList.user_id == userid).update({PackagePurchaseList.pkg_id: addtocart, PackagePurchaseList.product_id: product_id})

                            # cursor.execute(f"update package_purchase_list set pkg_id={addtocart},product_id='{product_id}' where user_id ={userid} ")

                            ''' insert product list in siteadmin  '''  

                            siteadmin_session_set.query(Packages).filter_by(user_id=siteadmin_userid).delete()

                            # cursor1.execute(f"delete from package_list where user_id='{siteadmin_userid}' ")
                            product_id_list = list(product_id.split(","))
                            for pkg_product_id in product_id_list:
                                product_id = encryptdata(pkg_product_id)
                                insertsite_prod = Packages(user_id=siteadmin_userid, product_id=product_id, link='localhost:5003', renewal_date=pkg_renewal_date)
                                siteadmin_session_set.add(insertsite_prod)
                                siteadmin_session_set.flush()

                                # cursor1.execute(
                                #     f"INSERT into package_list(user_id,product_id,link,renewal_date) values {(siteadmin_userid, product_id,'localhost:5003',pkg_renewal_date )} ")

                            sessions.commit()
                            siteadmin_session_set.commit()   

                            flash("Your Payment will be changed from next billing","success")

                else:
                    sessions.query(AlertPackagePurchase).filter(AlertPackagePurchase.user_id==userid).delete()
                    # cursor.execute(f"delete from alert_package_purchase where user_id={userid}")
                   
                    inserted_alert_pkg = AlertPackagePurchase(user_id=userid, pkg_id=addtocart, product_id=product_id, amount=new_pkg_amount, actual_amount=actual_amount, discount=discount_amount, currency_type=currency, currency_symbol=currency_symbol, latest_entry=1, payment_date=payment_date, renewal_date=pkg_renewal_date)
                    sessions.add(inserted_alert_pkg)
                    sessions.flush()

                    test_list = list(current_product_id.split(","))
                    sub_list = list(product_id.split(","))
                    # print(test_list,sub_list,"hjk")
    
                    if((set(sub_list) & set(test_list)) == set(test_list)):
                        flag = 1
                    else:
                        flag = 0
                    # print(flag,"flagsss")
                    if flag == 1:
                        # print("flasg11",product_id)
                        product_id_list = list(product_id.split(","))
                        # print("ifproduct_id_list",product_id_list)
                    else:
                        # print("flag0")
                        balance_products =  list(set(sub_list) - set(test_list))
                        # print(balance_products,"balance_products")
                        products_in_alert = test_list + balance_products
                        # print(products_in_alert,"products_in_alert")
                        product_id_list = products_in_alert
                        # print("elseproduct_id_list",product_id_list)

                    # print("product_id_list",product_id_list)
                    ''' insert product list in siteadmin  '''  
                    siteadmin_session_set.query(Packages).filter_by(user_id=siteadmin_userid).delete()
                    
                    # cursor1.execute(f"delete from package_list where user_id='{siteadmin_userid}' ")
                    
                    for pkg_product_id in product_id_list:
                        print("pkg_product_id",pkg_product_id)
                        # product_id = pkg_product_id
                        if pkg_product_id != "":
                            product_id = encryptdata(pkg_product_id)
                            insertsite_prod = Packages(user_id=siteadmin_userid, product_id=product_id, link='localhost:5003', renewal_date=pkg_renewal_date)
                            siteadmin_session_set.add(insertsite_prod)
                            siteadmin_session_set.flush()
                        # cursor1.execute(
                        #     f"INSERT into package_list(user_id,product_id,link,renewal_date) values {(siteadmin_userid, product_id,'localhost:5003',pkg_renewal_date )} ")

                    sessions.commit()
                    siteadmin_session_set.commit()
                    flash('No need for payment since you upgrade in the alert period',"success")


            else:
                flash("Please Enter Alert Interval List","error")

            return redirect(url_for('upgrade_package'))

        except Exception as ex:
            sessions.rollback()
            flash(str(ex),"error")
            return redirect(url_for('upgrade_package'))

    print(ft_prod_id,'KKKKKKKKKK')
    return render_template('upgrade_package.html', package_list=package_list, product_list=product_list, count_values=count_values, prod_selec_list=prod_selec_list,current_pkg_id=current_pkg_id,alert_time_period=alert_time_period,current_paid_package_id=current_package_id,current_prod_id=current_prod_id,reg_user_type=reg_user_type,ft_prod_id=ft_prod_id)



''' function to change user packages after billing.This function checks whether the date is within the annual alert period or monthly alert period .If it is so,there will be no need for payment '''


@app.route('/upgrade_user', methods=['GET', 'POST'])
def upgrade_user():
    if len(session)==0:
        return redirect(url_for('logout'))
    currency_type = session['currency']
    currency = currency_type.lower()
    currency_symbol = session['currency_symbol']
    userid = session['userid']
    reg_user_type = sessions.query(RegUsers.user_type).filter(RegUsers.user_id == userid).first()[0]
    count_values = get_all_count()
    current_date = datetime.date(datetime.now())
    ft_total_amt = 0
    company_id = sessions.query(CompanyDetails.company_id).filter_by(user_id=userid).first()[0]
    
    location_list = sessions.query(Location).with_entities(Location.location_id,Location.location_name).filter(Location.company_id == company_id).first()
    location_id = location_list[0]
    location_name = location_list[1]
    
    site_admin_db = str("scopiq_site_admin_")+str(company_id)+"_"+str(location_id)
    dms_db = str("scopiq_dms_")+str(company_id)+"_"+str(location_id)
    cms_db = str("scopiq_cms_")+str(company_id)+"_"+str(location_id)
    dsm_db = str("scopiq_dsm_")+str(company_id)+"_"+str(location_id)
    cams_db = str("scopiq_cams_")+str(company_id)+"_"+str(location_id)
    capa_db = str("scopiq_capa_")+str(company_id)+"_"+str(location_id)
    
    capa_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+capa_db)
    cams_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+cams_db)
    dsm_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+dsm_db)
    cms_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+cms_db)
    dms_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+dms_db)
    siteadmin_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+site_admin_db)
    Base = declarative_base()
    siteadmin_session = sessionmaker(bind=siteadmin_engine)
    dms_session = sessionmaker(bind=dms_engine)
    cms_session = sessionmaker(bind=cms_engine)
    dsm_session = sessionmaker(bind=dsm_engine)
    cams_session = sessionmaker(bind=cams_engine)
    capa_session = sessionmaker(bind=capa_engine)
    
    siteadmin_session_set = siteadmin_session()
    dms_session_set = dms_session()
    cms_session_set = cms_session()
    dsm_session_set = dsm_session()
    cams_session_set = cams_session()
    capa_session_set = capa_session()


    # for alert period calculation
    admin_user_amount_alert =  sessions.query(UserPurchaseList).with_entities(UserPurchaseList.amount).filter(UserPurchaseList.user_id==userid, UserPurchaseList.latest_entry==1,UserPurchaseList.user_type_id==1).first()[0]

    general_user_amount_alert =  sessions.query(UserPurchaseList).with_entities(UserPurchaseList.amount).filter(UserPurchaseList.user_id==userid, UserPurchaseList.latest_entry==1,UserPurchaseList.user_type_id==2).first()[0]

    limited_user_amount_alert =  sessions.query(UserPurchaseList).with_entities(UserPurchaseList.amount).filter(UserPurchaseList.user_id==userid, UserPurchaseList.latest_entry==1,UserPurchaseList.user_type_id==3).first()[0]

    ''' calculating remaining months in alert for ajax  '''

    pkg_renewal_date = sessions.query(PackagePurchaseList.renewal_date).filter(PackagePurchaseList.user_id==userid).first()[0]
    # cursor.execute(f"select renewal_date from package_purchase_list where user_id={userid}")
    # pkg_renewal_date = cursor.fetchone()[0]
    date_1 = pkg_renewal_date
    current_date = datetime.date(datetime.now())
    payment_date = current_date.strftime('%Y-%m-%d')
    date_2 = current_date
    remaining_months = alert_period(date_1,date_2)
    print(pkg_renewal_date,"current_date",current_date)
    no_of_months = remaining_months[0]['months']
    print(no_of_months,"no_of_months")

    # existing details after billing

    user_existng_details = sessions.query(UserPurchaseList).with_entities(UserPurchaseList.user_type_id, UserPurchaseList.no_of_users.cast(Integer), UserPurchaseList.amount).filter(UserPurchaseList.user_id==userid, UserPurchaseList.latest_entry==1).all()
    # cursor.execute(f"select * from user_purchase_list where user_id={userid} and latest_entry=1")
    # columns = [col[0] for col in cursor.description]
    # user_existng_details = [dict(zip(columns, row))
    #                             for row in cursor.fetchall()]
    user_renewal_date = sessions.query(UserPurchaseList.renewal_date).filter(UserPurchaseList.user_id == userid, UserPurchaseList.latest_entry==1).first()[0]
    
    user_billing_frequency = sessions.query(UserPurchaseList.billing_frequency).filter(UserPurchaseList.user_id==userid, UserPurchaseList.latest_entry==1).first()[0]
    user_exists_billing_frequency = user_billing_frequency

    if user_billing_frequency == "A":
        date_1 = user_renewal_date
        date_2 = current_date
        remaining_months = alert_period(date_1,date_2)
        if remaining_months != "error":
            alert_time_period = remaining_months[0]['alert']
        else:
            alert_time_period = ''
            
    if user_billing_frequency == "M":
        date_1 = user_renewal_date
        date_2 = current_date
        num_of_days = (date_1 - date_2)
        no_of_days = num_of_days.days
        alert_start_days_count = sessions.query(AlertIntervalList).filter(AlertIntervalList.renewal_type == "M").count()


        if alert_start_days_count != 0:
            alert_start_days_monthly = sessions.query(AlertIntervalList.alert_start_days).filter(AlertIntervalList.renewal_type == "M").first()[0]

            if no_of_days > alert_start_days_monthly:
                alert_time_period = 0
            else:
                alert_time_period = 1
    
    if user_billing_frequency == "F":
        alert_time_period = ""

    print(user_billing_frequency,"user_billing_frequency")
    
    user_select_count = sessions.query(UserSelectionList).filter(UserSelectionList.user_id == userid).count()

    print(reg_user_type,'reg_user_type')

    # if registered user purchased free trial
    if reg_user_type == "F":
        # set exists billing frequency is F for free trial
        alert_time_period = ''
        user_exists_billing_frequency = 'F'
        user_existng_details = [(1,0,'0'),(2,0,'0'),(3,0,'0')]

        # if registered user in temporary table
        if user_select_count == 0:
            adminamount = get_admin_slab()
            limitedamount = get_limited_slab()
            generalamount = get_general_slab()
            ft_admin_amount = int(adminamount) * 2
            ft_general_amount = int(generalamount) * 5
            ft_limited_amount = int(limitedamount) * 5
            # admin_user_selec_list = {'no_of_users':2,'amount':ft_admin_amount,'billing_frequency':'M'}
            # general_user_selec_list = {'no_of_users':5,'amount':ft_general_amount,'billing_frequency':'M'}
            # limited_user_selec_list = {'no_of_users':5,'amount':ft_limited_amount,'billing_frequency':'M'}


            admin_user_selec_list = {'no_of_users':0,'amount':0,'billing_frequency':'M'}
            general_user_selec_list = {'no_of_users':0,'amount':0,'billing_frequency':'M'}
            limited_user_selec_list = {'no_of_users':0,'amount':0,'billing_frequency':'M'}

            ft_total_amt = ft_admin_amount + ft_general_amount + ft_limited_amount
            
        
        # if registered user in purchase table
        else:
            admin_user_selec_list = sessions.query(UserSelectionList.admin_user_count.label('no_of_users'), UserSelectionList.admin_user_amount.label('amount'), UserSelectionList.billing_frequency.label('billing_frequency')).filter(UserSelectionList.user_id==userid).first()

            general_user_selec_list = sessions.query(UserSelectionList.general_user_count.label('no_of_users'), UserSelectionList.general_user_amount.label('amount'), UserSelectionList.billing_frequency.label('billing_frequency')).filter(UserSelectionList.user_id==userid).first()

            limited_user_selec_list = sessions.query(UserSelectionList.limited_user_count.label('no_of_users'), UserSelectionList.limited_user_amount.label('amount'), UserSelectionList.billing_frequency.label('billing_frequency')).filter(UserSelectionList.user_id==userid).first()
            
    # if registered user purchased packages
    else:
        # if registered user in temporary table
        if user_select_count == 0:
            alert_users_count = sessions.query(AlertUserPurchase).filter(AlertUserPurchase.user_id == userid).count()

            # cursor.execute(f"select count(*) from alert_user_purchase where user_id={userid}")
            # alert_users_count=cursor.fetchone()[0]
            if alert_users_count == 0:
                admin_user_selec_list = sessions.query(UserPurchaseList.no_of_users, UserPurchaseList.amount, UserPurchaseList.billing_frequency).with_entities(UserPurchaseList.no_of_users, UserPurchaseList.amount, UserPurchaseList.billing_frequency).filter(UserPurchaseList.user_id == userid, UserPurchaseList.user_type_id == 1, UserPurchaseList.latest_entry == 1).first()

                general_user_selec_list = sessions.query(UserPurchaseList).with_entities(UserPurchaseList.no_of_users, UserPurchaseList.amount, UserPurchaseList.billing_frequency).filter(UserPurchaseList.user_id == userid, UserPurchaseList.user_type_id == 2, UserPurchaseList.latest_entry == 1).first()

                limited_user_selec_list = sessions.query(UserPurchaseList).with_entities(UserPurchaseList.no_of_users, UserPurchaseList.amount, UserPurchaseList.billing_frequency).filter(UserPurchaseList.user_id == userid, UserPurchaseList.user_type_id == 3, UserPurchaseList.latest_entry == 1).first()

            else:
                admin_user_amount_alert =  sessions.query(AlertUserPurchase).with_entities(AlertUserPurchase.amount).filter(AlertUserPurchase.user_id==userid, AlertUserPurchase.latest_entry==1,AlertUserPurchase.user_type_id==1).first()[0]

                general_user_amount_alert =  sessions.query(AlertUserPurchase).with_entities(AlertUserPurchase.amount).filter(AlertUserPurchase.user_id==userid, AlertUserPurchase.latest_entry==1,AlertUserPurchase.user_type_id==2).first()[0]

                limited_user_amount_alert =  sessions.query(AlertUserPurchase).with_entities(AlertUserPurchase.amount).filter(AlertUserPurchase.user_id==userid, AlertUserPurchase.latest_entry==1,AlertUserPurchase.user_type_id==3).first()[0]

                admin_user_selec_list = sessions.query(AlertUserPurchase).with_entities(AlertUserPurchase.no_of_users, AlertUserPurchase.amount, AlertUserPurchase.billing_frequency).filter(AlertUserPurchase.user_id == userid, AlertUserPurchase.user_type_id == 1, AlertUserPurchase.latest_entry == 1).first()
                print(admin_user_selec_list)

                general_user_selec_list = sessions.query(AlertUserPurchase).with_entities(AlertUserPurchase.no_of_users, AlertUserPurchase.amount, AlertUserPurchase.billing_frequency).filter(AlertUserPurchase.user_id == userid, AlertUserPurchase.user_type_id == 2, AlertUserPurchase.latest_entry == 1).first()

                limited_user_selec_list = sessions.query(AlertUserPurchase).with_entities(AlertUserPurchase.no_of_users, AlertUserPurchase.amount, AlertUserPurchase.billing_frequency).filter(AlertUserPurchase.user_id == userid, AlertUserPurchase.user_type_id == 3, AlertUserPurchase.latest_entry == 1).first()

                # existing details if in alert table
                # user_existng_details = sessions.query(AlertUserPurchase).with_entities(AlertUserPurchase.user_type_id, AlertUserPurchase.no_of_users.cast(Integer), AlertUserPurchase.amount).filter(AlertUserPurchase.user_id==userid, AlertUserPurchase.latest_entry==1).all()

                user_renewal_date = sessions.query(AlertUserPurchase.renewal_date).filter(AlertUserPurchase.user_id == userid, AlertUserPurchase.latest_entry==1).first()[0]
        
                user_billing_frequency = sessions.query(AlertUserPurchase.billing_frequency).filter(AlertUserPurchase.user_id==userid, AlertUserPurchase.latest_entry==1).first()[0]

        # if registered user in purchase table
        else:
            admin_user_selec_list = sessions.query(UserSelectionList.admin_user_count.label('no_of_users'), UserSelectionList.admin_user_amount.label('amount'), UserSelectionList.billing_frequency.label('billing_frequency')).filter(UserSelectionList.user_id==userid).first()

            general_user_selec_list = sessions.query(UserSelectionList.general_user_count.label('no_of_users'), UserSelectionList.general_user_amount.label('amount'), UserSelectionList.billing_frequency.label('billing_frequency')).filter(UserSelectionList.user_id==userid).first()

            limited_user_selec_list = sessions.query(UserSelectionList.limited_user_count.label('no_of_users'), UserSelectionList.limited_user_amount.label('amount'), UserSelectionList.billing_frequency.label('billing_frequency')).filter(UserSelectionList.user_id==userid).first()

    print(user_billing_frequency)
    user_type_name = sessions.query(UserType).with_entities(UserType.user_type_name, UserType.user_type_id).order_by(UserType.user_type_id.asc()).all()

    admin_effective_date = sessions.query(UserPricing.effective_date).filter_by(user_type_id=1).first()[0]
    general_effective_date = sessions.query(UserPricing.effective_date).filter_by(user_type_id=2).first()[0]
    limited_effective_date = sessions.query(UserPricing.effective_date).filter_by(user_type_id=3).first()[0]

    if admin_effective_date <= current_date:
        admin_user = sessions.query(UserPricing).with_entities(UserPricing.lower.label('lower_value'),UserPricing.upper.label('higher_value'),getattr(UserPricing,currency).label('amount'),UserPricing.user_pricing_id.label('user_pricing_id')).filter_by(user_type_id=1)
    
    else:
        admin_cnt = sessions.query(UserPricing).filter_by(user_type_id = 1).count()
        admin_user = sessions.query(UserPricingHistory).with_entities(UserPricingHistory.lower.label('lower_value'),UserPricingHistory.upper.label('higher_value'),getattr(UserPricingHistory,currency).label('amount'),UserPricingHistory.user_pricing_id.label('user_pricing_id')).filter_by(user_type_id=1).filter(UserPricingHistory.effective_date<=current_date).order_by(UserPricingHistory.user_pricing_his_id.desc()).limit(admin_cnt)

    if general_effective_date <= current_date:
        general_user = sessions.query(UserPricing).with_entities(UserPricing.lower.label('lower_value'),UserPricing.upper.label('higher_value'),getattr(UserPricing,currency).label('amount'),UserPricing.user_pricing_id.label('user_pricing_id')).filter_by(user_type_id=2)
        
    else:
        general_cnt = sessions.query(UserPricing).filter_by(user_type_id = 2).count()
        general_user = sessions.query(UserPricingHistory).with_entities(UserPricingHistory.lower.label('lower_value'),UserPricingHistory.upper.label('higher_value'),getattr(UserPricingHistory,currency).label('amount'),UserPricingHistory.user_pricing_id.label('user_pricing_id')).filter_by(user_type_id=2).filter(UserPricingHistory.effective_date<=current_date).order_by(UserPricingHistory.user_pricing_his_id.desc()).limit(general_cnt)  

    if limited_effective_date <= current_date:
        limited_user = sessions.query(UserPricing).with_entities(UserPricing.lower.label('lower_value'),UserPricing.upper.label('higher_value'),getattr(UserPricing,currency).label('amount'),UserPricing.user_pricing_id.label('user_pricing_id')).filter_by(user_type_id=3)
        
    else:
        limited_cnt = sessions.query(UserPricing).filter_by(user_type_id = 3).count()
        limited_user = sessions.query(UserPricingHistory).with_entities(UserPricingHistory.lower.label('lower_value'),UserPricingHistory.upper.label('higher_value'),getattr(UserPricingHistory,currency).label('amount'),UserPricingHistory.user_pricing_id.label('user_pricing_id')).filter_by(user_type_id=3).filter(UserPricingHistory.effective_date<=current_date).order_by(UserPricingHistory.user_pricing_his_id.desc()).limit(limited_cnt)

    if request.method == "POST":
        try:
            admin_count = request.form['admin_count']
            print(admin_count,"admin_count")
            adminus = request.form['adminus']
            print(adminus,"adminus")
            general_count = request.form['general_count']
            genus = request.form['genus']
            print(admin_count,adminus,general_count,genus)

            limited_count = request.form['limited_count']
            print(limited_count)
            limus = request.form['limus']
            print(limus)

            totamnt = request.form['totamnt']
            print(admin_count,adminus,general_count,genus,limited_count,limus)
            billing_frequency = request.form['billing_frequency']
            print(admin_count,adminus,general_count,genus,limited_count,limus)

            existing_admin_user = request.form['existing_admin_user']
            existing_admin_totamnt = request.form['existing_admin_totamnt']
            existing_general_user = request.form['existing_general_user']
            existing_general_totamnt = request.form['existing_general_totamnt']
            existing_limited_user = request.form['existing_limited_user']
            exist_limited_totamnt = request.form['exist_limited_totamnt']
            print(existing_admin_user,existing_general_user,exist_limited_totamnt)

            if alert_time_period == 0:
                if existing_admin_user == admin_count:
                    adminus = 0
                else:
                    adminus = adminus

                if existing_general_user == general_count:
                    genus = 0
                else:
                    genus = genus

                if existing_limited_user == limited_count:
                    limus = 0
                else:
                    limus = limus
            print(billing_frequency,"billing_frequency")
            if billing_frequency == 'M':
                print("if")
                totamnt = request.form['totamnt']
                actual_amount = ''
                discount = ''
            else:
                print("else")
                totamnt = request.form['annualized_hidden'] # final total amount
                print(totamnt)
                actual_amount = request.form['totamnt'] # amount per month
                print(actual_amount)
                discount = request.form['discount_hidden']
                print(discount)
            print(user_exists_billing_frequency,"user_exists_billing_frequency")
            print(admin_count , existing_admin_user , general_count, existing_general_user , limited_count, existing_limited_user)
            if user_exists_billing_frequency == "A":
                date_1 = user_renewal_date
                # print(user_renewal_date,"user_renewal_date")
                current_date = datetime.date(datetime.now())
                payment_date = current_date.strftime('%Y-%m-%d')
                date_2 = current_date

                remaining_months_annual = alert_period(date_1,date_2)
                if remaining_months_annual != "error":
                    if billing_frequency == 'A': # annual to annual

                        if remaining_months_annual[0]['alert'] == 0 :
                            remaining_months = remaining_months_annual[0]['months']
                            if (int(admin_count) > int(existing_admin_user) and int(general_count) >= int(existing_general_user) and int(limited_count) >= int(existing_limited_user)) or (int(admin_count) >= int(existing_admin_user) and int(general_count) > int(existing_general_user) and int(limited_count) >= int(existing_limited_user)) or (int(admin_count) >= int(existing_admin_user) and int(general_count) >= int(existing_general_user) and int(limited_count) > int(existing_limited_user)):
                                if totamnt != "0":
                                    # if reg_user_type == "F":
                                    #     annualized_hidden = request.form['annualized_hidden_freetrial']
                                    #     total_balance_amount = float(annualized_hidden)
                                    # else:
                                    total_balance_amount = float(totamnt)*float((remaining_months/12))

                                    insert_user_selection(admin_count, adminus, general_count, genus, limited_count, limus, total_balance_amount, userid, billing_frequency, actual_amount, discount)

                                    flash("Added To Cart","success")

                                else:
                                    sessions.query(UserPurchaseList).filter(UserPurchaseList.user_id == userid, UserPurchaseList.user_type_id == 1).update({UserPurchaseList.no_of_users: admin_count})

                                    sessions.query(UserPurchaseList).filter(UserPurchaseList.user_id == userid, UserPurchaseList.user_type_id == 2).update({UserPurchaseList.no_of_users: general_count})

                                    sessions.query(UserPurchaseList).filter(UserPurchaseList.user_id == userid, UserPurchaseList.user_type_id == 3).update({UserPurchaseList.no_of_users: limited_count})
                                    sessions.commit()

                                    # cursor.execute(f"update user_purchase_list set no_of_users={admin_count} where user_id ={userid} and user_type_id=1 ")
                                    # cursor.execute(f"update user_purchase_list set no_of_users={general_count} where user_id ={userid} and user_type_id=2 ")
                                    # cursor.execute(f"update user_purchase_list set no_of_users={limited_count} where user_id ={userid} and user_type_id=3 ")
                                    flash("Your Payment will be changed from next billing","success")
                            else:
                                # flash("Downgrade will be done from next billing cycle","error")
                                flash("Downgrade cannot be done at this moment.Proceed with downgrade in your alert period.","error")
        
                            # return redirect('/upgrade_user')

                        else:
                            print("else")
                            renewal_date = user_renewal_date.strftime('%Y-%m-%d')
                            alert_insert_annual(admin_count,adminus,existing_admin_user,existing_admin_totamnt,general_count,genus,existing_general_user,existing_general_totamnt,limited_count,limus,existing_limited_user,exist_limited_totamnt,currency,currency_symbol,payment_date,userid,billing_frequency,renewal_date)
                            result = "No need for payment since you upgrade in the alert period"
                            flash(result,"success")
                            # return redirect('/upgrade_user')

                    else: # annual to monthly
                        
                        if remaining_months_annual[0]['alert'] == 0 :
                            # remaining_months = remaining_months_annual[0]['months']

                            # total_balance_amount = float(totamnt)*float((remaining_months/12))

                            # insert_user_selection(admin_count, adminus, general_count, genus, limited_count, limus, total_balance_amount, userid, billing_frequency, actual_amount, discount)

                            flash('Monthly Subscription will be done from next billing',"success")
                            # return redirect('/upgrade_user')

                        else:
                            renewal_date = user_renewal_date.strftime('%Y-%m-%d')
                            alert_insert_annual(admin_count,adminus,existing_admin_user,existing_admin_totamnt,general_count,genus,existing_general_user,existing_general_totamnt,limited_count,limus,existing_limited_user,exist_limited_totamnt,currency,currency_symbol,payment_date,userid,billing_frequency,renewal_date)

                            result = "No need for payment since you upgrade in the alert period"
                            flash(result,"success")
                            # return redirect('/upgrade_user')

                else:
                    flash("Please Enter Alert Interval List","error")

            elif user_exists_billing_frequency == "M":# if exisying billing is Monthly
                if billing_frequency == "M": # monthly to monthly
                    # existing billing frequency
                    user_monthly_renewal_date = sessions.query(UserPurchaseList.renewal_date).filter(UserPurchaseList.user_id == userid, UserPurchaseList.latest_entry==1).first()[0]
                    renewal_date = user_renewal_date
                    alert_insert_monthly(user_monthly_renewal_date, admin_count, adminus, general_count, genus, limited_count, limus, totamnt, userid, billing_frequency, actual_amount, discount, existing_admin_totamnt, existing_admin_user, existing_general_user, existing_general_totamnt, existing_limited_user, exist_limited_totamnt, renewal_date)

                else:# monthly to annual
                    # pkg_renewal_date = sessions.query(PackagePurchaseList.renewal_date).filter(PackagePurchaseList.user_id==userid).first()[0]
                    # # cursor.execute(f"select renewal_date from package_purchase_list where user_id={userid}")
                    # # pkg_renewal_date = cursor.fetchone()[0]
                    # date_1 = pkg_renewal_date
                    # current_date = datetime.date(datetime.now())
                    # payment_date = current_date.strftime('%Y-%m-%d')
                    # date_2 = current_date
                    # remaining_months = alert_period(date_1,date_2)
                    # no_of_months = remaining_months[0]['months']
                    # annual_remaining_amount = float(actual_amount) * float(no_of_months)
                    print("beforepay")

                    totamnt = request.form['payable_amount'] 
                    print(totamnt,"totamnt")
                    discount = ''
                    renewal_date = pkg_renewal_date

                    # existing billing frequency
                    user_monthly_renewal_date = sessions.query(UserPurchaseList.renewal_date).filter(UserPurchaseList.user_id == userid, UserPurchaseList.latest_entry==1).first()[0]

                    alert_insert_monthly(user_monthly_renewal_date, admin_count, adminus, general_count, genus, limited_count, limus, totamnt, userid, billing_frequency, actual_amount, discount, existing_admin_totamnt, existing_admin_user, existing_general_user, existing_general_totamnt, existing_limited_user, exist_limited_totamnt, renewal_date)
                    return redirect('/upgrade_user')
        
            else:
                if reg_user_type == "F":
                    # print("elseefree")
                    if billing_frequency == 'A':
                        # print(billing_frequency)
                        annualized_hidden = request.form['annualized_hidden_freetrial']
                        # print(annualized_hidden,"annualized_hidden")
                        total_balance_amount = float(annualized_hidden)
                    else:
                        total_balance_amount = float(totamnt)

                    insert_user_selection(admin_count, adminus, general_count, genus, limited_count, limus, total_balance_amount, userid, billing_frequency, actual_amount, discount)
                    flash("Added To Cart","success")


            return redirect('/upgrade_user')

        except Exception as ex:
            sessions.rollback()
            siteadmin_session_set.rollback()
            flash(str(ex),"error")
            return redirect(url_for('upgrade_user'))

    return render_template('upgrade_user.html', admin_user=admin_user, general_user=general_user, limited_user=limited_user, count_values=count_values, admin_user_selec_list=admin_user_selec_list, user_type_name=user_type_name, general_user_selec_list=general_user_selec_list, limited_user_selec_list=limited_user_selec_list,
    user_existng_details=user_existng_details,user_select_count=user_select_count,user_billing_frequency=user_exists_billing_frequency,alert_time_period=alert_time_period,reg_user_type=reg_user_type,admin_user_amount_alert=admin_user_amount_alert,general_user_amount_alert=general_user_amount_alert,limited_user_amount_alert=limited_user_amount_alert,remaining_months_alert=no_of_months,ft_total_amt=ft_total_amt)


''' function to check the days between the current date and the renewal date is within the annual alert period '''


def alert_period(date_1,date_2):
    diff = relativedelta(date_1, date_2)
    days = diff.days
    months = diff.months
    month_days = []

    num_of_days = (date_1 - date_2)
    print(num_of_days.days,'num_of_days.days')
    alert_start_days_count = sessions.query(AlertIntervalList).filter(AlertIntervalList.renewal_type == "A").count()

    if alert_start_days_count != 0:
        alert_start_days_annual = sessions.query(AlertIntervalList.alert_start_days).filter(AlertIntervalList.renewal_type == "A").first()[0]

        # cursor.execute(f"select alert_start_days from alert_interval_list where renewal_type='A'")
        # alert_start_days_annual = cursor.fetchone()[0]

        print(alert_start_days_annual,'alert_start_days_annual')
        if (num_of_days.days <= alert_start_days_annual):

            month_days.append({'alert':1, 'months':months, 'days':days})
            print(month_days,'month_days')
            return month_days # in alert period
            
        else:
            print('ELSE')
            if days > 0:
                months = months + 1
                
            month_days.append({'alert':0, 'months':months, 'days':days})
            print(month_days,'month_days')
            return month_days
            
    else:
        return "error"


''' function to insert the users count if the billing_frequency is annual '''


def alert_insert_annual(admin_count,adminus,existing_admin_user,existing_admin_totamnt,general_count,genus,existing_general_user,existing_general_totamnt,limited_count,limus,existing_limited_user,exist_limited_totamnt,currency,currency_symbol,payment_date,userid,billing_frequency,renewal_date):
    company_id = sessions.query(CompanyDetails.company_id).filter_by(user_id=userid).first()[0]
    location_list = sessions.query(Location).with_entities(Location.location_id,Location.location_name).filter(Location.company_id == company_id).first()
    location_id = location_list[0]
    location_name = location_list[1]
    
    site_admin_db = str("scopiq_site_admin_")+str(company_id)+"_"+str(location_id)
    dms_db = str("scopiq_dms_")+str(company_id)+"_"+str(location_id)
    cms_db = str("scopiq_cms_")+str(company_id)+"_"+str(location_id)
    dsm_db = str("scopiq_dsm_")+str(company_id)+"_"+str(location_id)
    cams_db = str("scopiq_cams_")+str(company_id)+"_"+str(location_id)
    capa_db = str("scopiq_capa_")+str(company_id)+"_"+str(location_id)
    
    capa_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+capa_db)
    cams_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+cams_db)
    dsm_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+dsm_db)
    cms_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+cms_db)
    dms_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+dms_db)
    siteadmin_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+site_admin_db)
    Base = declarative_base()
    siteadmin_session = sessionmaker(bind=siteadmin_engine)
    dms_session = sessionmaker(bind=dms_engine)
    cms_session = sessionmaker(bind=cms_engine)
    dsm_session = sessionmaker(bind=dsm_engine)
    cams_session = sessionmaker(bind=cams_engine)
    capa_session = sessionmaker(bind=capa_engine)

    siteadmin_session_set = siteadmin_session()
    dms_session_set = dms_session()
    cms_session_set = cms_session()
    dsm_session_set = dsm_session()
    cams_session_set = cams_session()
    capa_session_set = capa_session()


    email = session['email']
    sessions.query(AlertUserPurchase).filter_by(user_id=userid).delete()
    # cursor.execute(f"delete from alert_user_purchase where user_id={userid} ")
    # sessions.commit()   

    # admin_amount_alert = user_amount_alert(admin_count,1)
    # print(admin_amount_alert,"admin_amount_alert")
    # admin_totamnt = float(admin_amount_alert) * float(admin_count)

    inserted_alert_admin_users = AlertUserPurchase(user_id=userid, user_type_id=1, no_of_users=admin_count, amount=adminus, currency_type=currency, currency_symbol=currency_symbol, latest_entry=1, payment_date=payment_date, created_by=userid, billing_frequency=billing_frequency, renewal_date=renewal_date)
    sessions.add(inserted_alert_admin_users)
    sessions.flush()

    inserted_alert_general_users = AlertUserPurchase(user_id=userid, user_type_id=2, no_of_users=general_count, amount=genus, currency_type=currency, currency_symbol=currency_symbol, latest_entry=1, payment_date=payment_date, created_by=userid, billing_frequency=billing_frequency, renewal_date=renewal_date)
    sessions.add(inserted_alert_general_users)
    sessions.flush()

    inserted_alert_lim_users = AlertUserPurchase(user_id=userid, user_type_id=3, no_of_users=limited_count, amount=limus, currency_type=currency, currency_symbol=currency_symbol, latest_entry=1, payment_date=payment_date, created_by=userid, billing_frequency=billing_frequency, renewal_date=renewal_date)
    sessions.add(inserted_alert_lim_users)
    sessions.flush()

    ''' insert users count in siteadmin  '''

    siteadmin_userid = siteadmin_session_set.query(Users.user_id).filter(Users.email==email).first()[0]

    siteadmin_session_set.query(UserList).filter_by(user_id=siteadmin_userid).delete()

    usr_purchased_list = sessions.query(AlertUserPurchase).with_entities(AlertUserPurchase.user_type_id, AlertUserPurchase.no_of_users).filter(AlertUserPurchase.user_id==userid)
    user_list_details = []

    for usr_pur_list in usr_purchased_list:
        user_type_id = usr_pur_list[0]
        no_of_users = usr_pur_list[1]
        
        if user_type_id == 1:
            user_type_name = "Admin Users"
            if int(existing_admin_user) > no_of_users:
                total_users = existing_admin_user
                reduce_users =  int(existing_admin_user) - no_of_users
                user_list_details.append({'user_type_name':user_type_name,'user_type_id': user_type_id,'user_count':reduce_users})
            else:
                total_users = no_of_users

        elif user_type_id == 2:
            user_type_name = "General Users"
            if int(existing_general_user) > no_of_users:
                total_users = existing_general_user
                reduce_users = int(existing_general_user) - no_of_users
                user_list_details.append({'user_type_name':user_type_name,'user_type_id': user_type_id,'user_count':reduce_users})
            else:
                total_users = no_of_users
                
        elif user_type_id == 3:
            user_type_name = "Limited Users"
            if int(existing_limited_user) > no_of_users:
                total_users = existing_limited_user
                reduce_users = int(existing_limited_user) - no_of_users
                user_list_details.append({'user_type_name':user_type_name,'user_type_id': user_type_id,'user_count':reduce_users})
            else:
                total_users = no_of_users

        user_type = encryptdata(user_type_id)
        user_count = encryptdata(total_users)
        # print(user_count,"user_count")

        insert_userslist = UserList(user_id=siteadmin_userid, user_type_id=user_type, no_of_users=user_count, renewal_date=renewal_date)
        siteadmin_session_set.add(insert_userslist)
        siteadmin_session_set.flush()
        # print(no_of_users,"no_of_users")
        # print(total_users,"total_users")

    # print(user_list_details,"user_list_details")
    temp_user_details_message = ""
    if user_list_details != []:
        for user_list_det in user_list_details:
            user_details_message = str(user_list_det['user_type_name']) + " - " + str(user_list_det['user_count']) + "\n"
            temp_user_details_message = temp_user_details_message + user_details_message 
        print(temp_user_details_message,"user_det")
        message = 'Remove Users' + "\n" + str(temp_user_details_message)
        print(message,"message")
        insert_alert_notify_id = Alert_notify_list(role_name= "Location Admin" , type_id=1, message=message, created_by=userid)
        siteadmin_session_set.add(insert_alert_notify_id)
        alert_notify_id = insert_alert_notify_id.alert_notify_id
        siteadmin_session_set.flush()

        insert_alert_notify_his = Alert_notify_history(alert_notify_id=alert_notify_id,role_name= "Location Admin" , type_id=1, message=message, created_by=userid)
        siteadmin_session_set.add(insert_alert_notify_his)
        siteadmin_session_set.flush()

        msg = Message('Remove Users', sender='sneha.r@perpetua.co.in', recipients=[email])
        # msg.body = msg
        msg.html = render_template('emails/remove_users.html', user_list_details = user_list_details)
        mail.send(msg)

    # print(user_list_details,"user_list_details")
    sessions.commit()
    siteadmin_session_set.commit()


''' function to check the days between the current date and the renewal date is within the monthly alert period and to insert the users count if the billing_frequency is monthly '''


def alert_insert_monthly(user_renewal_date, admin_count, adminus, general_count, genus, limited_count, limus, totamnt, userid, billing_frequency, actual_amount, discount, existing_admin_totamnt, existing_admin_user, existing_general_user, existing_general_totamnt, existing_limited_user, exist_limited_totamnt, renewal_date):
    company_id = sessions.query(CompanyDetails.company_id).filter_by(user_id=userid).first()[0]

    location_list = sessions.query(Location).with_entities(Location.location_id,Location.location_name).filter(Location.company_id == company_id).first()
    location_id = location_list[0]
    location_name = location_list[1]
    
    site_admin_db = str("scopiq_site_admin_")+str(company_id)+"_"+str(location_id)
    dms_db = str("scopiq_dms_")+str(company_id)+"_"+str(location_id)
    cms_db = str("scopiq_cms_")+str(company_id)+"_"+str(location_id)
    dsm_db = str("scopiq_dsm_")+str(company_id)+"_"+str(location_id)
    sms_db = str("scopiq_sms_")+str(company_id)+"_"+str(location_id)
    cams_db = str("scopiq_cams_")+str(company_id)+"_"+str(location_id)
    capa_db = str("scopiq_capa_")+str(company_id)+"_"+str(location_id)
    
    capa_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+capa_db)
    cams_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+cams_db)
    sms_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+sms_db)
    dsm_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+dsm_db)
    cms_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+cms_db)
    dms_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+dms_db)
    siteadmin_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+site_admin_db)


    Base = declarative_base()
    siteadmin_session = sessionmaker(bind=siteadmin_engine)
    dms_session = sessionmaker(bind=dms_engine)
    cms_session = sessionmaker(bind=cms_engine)
    dsm_session = sessionmaker(bind=dsm_engine)
    sms_session = sessionmaker(bind=sms_engine)
    cams_session = sessionmaker(bind=cams_engine)
    capa_session = sessionmaker(bind=capa_engine)


    siteadmin_session_set = siteadmin_session()
    dms_session_set = dms_session()
    cms_session_set = cms_session()
    dsm_session_set = dsm_session()
    sms_session_set = sms_session()
    cams_session_set = cams_session()
    capa_session_set = capa_session()

    currency = session['currency']
    currency_symbol = session['currency_symbol']
    email = session['email']
    date_1 = user_renewal_date
    current_date = datetime.date(datetime.now())
    payment_date = current_date.strftime('%Y-%m-%d')
    date_2 = current_date
    num_of_days = (date_1 - date_2)
    no_of_days = num_of_days.days
    renewal_date = renewal_date.strftime('%Y-%m-%d')
    print(date_1,date_2,"renewal_date",no_of_days)

    alert_start_days_count = sessions.query(AlertIntervalList).filter(AlertIntervalList.renewal_type == "M").count()

    if alert_start_days_count != 0:
        alert_start_days_monthly = sessions.query(AlertIntervalList.alert_start_days).filter(AlertIntervalList.renewal_type == "M").first()[0]
        
        # Alert Period Check
        if no_of_days > alert_start_days_monthly:
            # Not in Alert Period
            print("Alert",no_of_days)

            if (int(admin_count) > int(existing_admin_user) and int(general_count) >= int(existing_general_user) and int(limited_count) >= int(existing_limited_user)) or (int(admin_count) >= int(existing_admin_user) and int(general_count) > int(existing_general_user) and int(limited_count) >= int(existing_limited_user)) or (int(admin_count) >= int(existing_admin_user) and int(general_count) >= int(existing_general_user) and int(limited_count) > int(existing_limited_user)) :
                
                insert_user_selection(admin_count, adminus, general_count, genus, limited_count, limus, totamnt, userid, billing_frequency, actual_amount, discount)
                flash("Added To Cart","success")

            else:
                flash("Downgrade cannot be done at this moment.Proceed with downgrade in your alert period.","error")

        else:
            # if in alert period
            sessions.query(AlertUserPurchase).filter_by(user_id=userid).delete()
            inserted_alert_admin_users = AlertUserPurchase(user_id=userid, user_type_id=1, no_of_users=admin_count, amount=adminus, currency_type=currency, currency_symbol=currency_symbol, latest_entry=1, payment_date=payment_date, created_by=userid, billing_frequency=billing_frequency, renewal_date=renewal_date)
            sessions.add(inserted_alert_admin_users)
            sessions.flush()

            inserted_alert_general_users = AlertUserPurchase(user_id=userid, user_type_id=2, no_of_users=general_count, amount=genus, currency_type=currency, currency_symbol=currency_symbol, latest_entry=1, payment_date=payment_date, created_by=userid, billing_frequency=billing_frequency, renewal_date=renewal_date)
            sessions.add(inserted_alert_general_users)
            sessions.flush()

            inserted_alert_lim_users = AlertUserPurchase(user_id=userid, user_type_id=3, no_of_users=limited_count, amount=limus, currency_type=currency, currency_symbol=currency_symbol, latest_entry=1, payment_date=payment_date, created_by=userid, billing_frequency=billing_frequency, renewal_date=renewal_date)
            sessions.add(inserted_alert_lim_users)
            sessions.flush()

            ''' insert users count in siteadmin  '''    
            siteadmin_userid = siteadmin_session_set.query(Users.user_id).filter(Users.email==email).first()[0]


            siteadmin_session_set.query(UserList).filter_by(user_id=siteadmin_userid).delete()

            usr_purchased_list = sessions.query(AlertUserPurchase).with_entities(AlertUserPurchase.user_type_id, AlertUserPurchase.no_of_users).filter(AlertUserPurchase.user_id==userid)

            user_list_details = []
            for usr_pur_list in usr_purchased_list:
                user_type_id = usr_pur_list[0]
                no_of_users = usr_pur_list[1]
                # print("hi")
                
                if user_type_id == 1:
                    user_type_name = "Admin Users"
                    if int(existing_admin_user) > no_of_users:
                        total_users = existing_admin_user
                        reduce_users = int(existing_admin_user) - no_of_users
                        user_list_details.append({'user_type_name':user_type_name,'user_type_id': user_type_id,'user_count':reduce_users})
                    else:
                        total_users = no_of_users

                elif user_type_id == 2:
                    user_type_name = "General Users"
                    if int(existing_general_user) > no_of_users:
                        total_users = existing_general_user
                        reduce_users = int(existing_general_user) - no_of_users
                        user_list_details.append({'user_type_name':user_type_name,'user_type_id': user_type_id,'user_count':reduce_users})
                    else:
                        total_users = no_of_users
                        
                elif user_type_id == 3:
                    user_type_name = "Limited Users"
                    if int(existing_limited_user) > no_of_users:
                        total_users = existing_limited_user
                        reduce_users = int(existing_limited_user) - no_of_users
                        user_list_details.append({'user_type_name':user_type_name,'user_type_id': user_type_id,'user_count':reduce_users})
                    else:
                        total_users = no_of_users

                user_type = encryptdata(user_type_id)
                user_count = encryptdata(total_users)

                insert_userslist = UserList(user_id=siteadmin_userid, user_type_id=user_type, no_of_users=user_count, renewal_date=renewal_date)
                siteadmin_session_set.add(insert_userslist)
                siteadmin_session_set.flush()
                # print(no_of_users,"no_of_users")
                # print(total_users,"total_users")

            # print(user_list_details,"user_list_details")
            temp_user_details_message = ""
            if user_list_details != []:
                for user_list_det in user_list_details:
                    user_details_message = str(user_list_det['user_type_name']) + " - " + str(user_list_det['user_count']) + "\n"
                    temp_user_details_message = temp_user_details_message + user_details_message 
                # print(temp_user_details_message,"user_det")
                message = 'Remove Users' + "\n" + str(temp_user_details_message)
                # print(message,"message")
                insert_alert_notify_id = Alert_notify_list(role_name= "Location Admin" , type_id=1, message=message, created_by=userid)
                siteadmin_session_set.add(insert_alert_notify_id)
                alert_notify_id = insert_alert_notify_id.alert_notify_id
                siteadmin_session_set.flush()

                insert_alert_notify_his = Alert_notify_history(alert_notify_id=alert_notify_id,role_name= "Location Admin" , type_id=1, message=message, created_by=userid)
                siteadmin_session_set.add(insert_alert_notify_his)
                siteadmin_session_set.flush()

                msg = Message('Remove Users', sender='sneha.r@perpetua.co.in', recipients=[email])
                # msg.body = msg
                msg.html = render_template('emails/remove_users.html', user_list_details = user_list_details)
                mail.send(msg)

            sessions.commit()
            siteadmin_session_set.commit()
            result = "No need for payment since you upgrade in the alert period"
            flash(result,"success")

    else:
        result = "Please Enter Alert Interval List"
        flash(result,"error")



# def user_amount_alert(user_total_count,type_of_user):
#     currency = session['currency']
#     # users_count = request.args.get('users_count')
#     # user_type = request.args.get('usertype')
#     users_count = user_total_count
#     user_type = type_of_user
#     current_date = datetime.date(datetime.now())
#     cursor.execute(f"select effective_date from user_pricing where user_type_id={user_type} ")
#     user_effective_date = cursor.fetchone()[0]

#     if user_effective_date <= current_date:
#         cursor.execute(
#             f"select upper from user_pricing where user_type_id={user_type} order by user_pricing_id desc;")
#         upper_value = cursor.fetchone()[0]

#     else:
#         cursor.execute(
#             f"select upper from user_pricing_history where user_type_id={user_type} and effective_date<=current_date  order by user_pricing_his_id desc LIMIT 1")
#         upper_value = cursor.fetchone()[0]

#     # if upper_value == '':
#     #     maxvalue = ''
#     # else:
#     #     maxvalue = int(upper_value)

#     if users_count != "0":
#         if user_effective_date <= current_date:
#             cursor.execute(
#                 f"select lower,upper,{currency} from user_pricing where user_type_id={user_type}")
#             user_pricing_list = cursor.fetchall()

#         else:
#             cursor.execute(f"select count(*) from user_pricing where user_type_id={user_type}")
#             usr_cnt = cursor.fetchone()[0]
#             cursor.execute(
#                 f"select lower,upper,{currency} from user_pricing_history where user_type_id={user_type} and effective_date<=current_date order by user_pricing_his_id desc LIMIT {usr_cnt}")
#             user_pricing_list = cursor.fetchall()
#         # print(user_pricing_list,"user_pricing_list")
#         for user_pricing_lists in user_pricing_list:
#             lower_value = user_pricing_lists[0]
#             # new_lower_value=int(lower_vale)
#             # print(new_lower_value)
#             upper_value = user_pricing_lists[1]
#             usr_pricing_amount = user_pricing_lists[2]
#             if upper_value != "":
#                 if(int(lower_value) <= int(users_count) and int(upper_value) >= int(users_count)):
#                     amount = usr_pricing_amount

#             else:
#                 lower = lower_value
#                 new_lower_val = lower.replace('>', '')
#                 if(int(new_lower_val) < int(users_count)):
#                     amount = usr_pricing_amount

#     else:
#         amount = 0
#     # print(amount,"amount")
#     # amount_and_maxvalue = str(amount)+"@"+str(maxvalue)
#     return str(amount)


''' function to change cloud packages after billing.This function checks whether the date is within the annual alert period.If it is so,there will be no need for payment '''


@app.route('/upgrade_cloud', methods=['GET', 'POST'])
def upgrade_cloud():
    if len(session)==0:
        return redirect(url_for('logout'))
    currency_type = session['currency']
    currency = currency_type.lower()
    currency_symbol = session['currency_symbol']
    userid = session['userid']
    reg_user_type = sessions.query(RegUsers.user_type).filter(RegUsers.user_id == userid).first()[0]
    email = session['email']
    count_values = get_all_count()
    
    company_id = sessions.query(CompanyDetails.company_id).filter_by(user_id=userid).first()[0]
    
    location_list = sessions.query(Location).with_entities(Location.location_id,Location.location_name).filter(Location.company_id == company_id).first()
    location_id = location_list[0]
    location_name = location_list[1]
    
    site_admin_db = str("scopiq_site_admin_")+str(company_id)+"_"+str(location_id)
    dms_db = str("scopiq_dms_")+str(company_id)+"_"+str(location_id)
    cms_db = str("scopiq_cms_")+str(company_id)+"_"+str(location_id)
    dsm_db = str("scopiq_dsm_")+str(company_id)+"_"+str(location_id)
    sms_db = str("scopiq_sms_")+str(company_id)+"_"+str(location_id)
    cams_db = str("scopiq_cams_")+str(company_id)+"_"+str(location_id)
    capa_db = str("scopiq_capa_")+str(company_id)+"_"+str(location_id)
    
    capa_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+capa_db)
    cams_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+cams_db)
    sms_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+sms_db)
    dsm_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+dsm_db)
    cms_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+cms_db)
    dms_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+dms_db)
    siteadmin_engine = create_engine('postgresql+psycopg2://postgres:perpetua@localhost/'+site_admin_db)
    Base = declarative_base()
    siteadmin_session = sessionmaker(bind=siteadmin_engine)
    dms_session = sessionmaker(bind=dms_engine)
    cms_session = sessionmaker(bind=cms_engine)
    dsm_session = sessionmaker(bind=dsm_engine)
    sms_session = sessionmaker(bind=sms_engine)
    cams_session = sessionmaker(bind=cams_engine)
    capa_session = sessionmaker(bind=capa_engine)


    siteadmin_session_set = siteadmin_session()
    dms_session_set = dms_session()
    cms_session_set = cms_session()
    dsm_session_set = dsm_session()
    sms_session_set = sms_session()
    cams_session_set = cams_session()
    capa_session_set = capa_session()

    # cursor.execute(
    #     f"select b.cl_type_name,{currency} as amount,a.features,b.cl_type_id from cloud_pricing a left join cloud_type b on a.cl_type_id=b.cl_type_id order by a.cl_type_id asc")
    # columns = [col[0] for col in cursor.description]
    # cloud_list = [dict(zip(columns, row)) for row in cursor.fetchall()]

    effective_date = sessions.query(CloudPricing.effective_date).first()[0]
    current_date = datetime.date(datetime.now())

    # cursor.execute(f"select effective_date from cloud_pricing")
    # effective_date = cursor.fetchone()[0]
    # current_date = datetime.date(datetime.now())

    if effective_date <= current_date:
        cloud_list = sessions.query(CloudPricing,CloudType).with_entities(CloudType.cl_type_name,getattr(CloudPricing,currency).label('amount'),CloudPricing.features,CloudType.cl_type_id).join(CloudType, CloudType.cl_type_id == CloudPricing.cl_type_id).order_by(CloudPricing.cl_type_id.asc())

    else:
        cloud_id_count = sessions.query(CloudPricing).count()

        cloud_list = sessions.query(CloudPricingHistory,CloudType).with_entities(CloudType.cl_type_name,getattr(CloudPricingHistory,currency).label('amount'),CloudPricingHistory.features,CloudType.cl_type_id).join(CloudType, CloudType.cl_type_id == CloudPricingHistory.cl_type_id).filter(CloudPricingHistory.effective_date<=current_date).order_by(CloudPricingHistory.cloud_pricing_his_id.desc()).limit(cloud_id_count)
    
    cloud_purchase = sessions.query(CloudPurchaseList).with_entities(CloudPurchaseList.renewal_date, CloudPurchaseList.amount, CloudPurchaseList.cloud_type_id).filter(CloudPurchaseList.user_id==userid, CloudPurchaseList.latest_entry==1).first()

    # cursor.execute(
    #         f"select renewal_date,amount,cloud_type_id from cloud_purchase_list where user_id={userid} and latest_entry=1 ")
    # cloud_purchase = cursor.fetchone()
    cloud_renewal_date = cloud_purchase[0]
    paid_cloud_amount = cloud_purchase[1]
    current_cloud_type = cloud_purchase[2]

    cloud_select_count = sessions.query(CloudSelection).filter(CloudSelection.user_id == userid).count()

    # cursor.execute(f"select count(*) from cloud_selection where user_id={userid}")
    # cloud_select_count=cursor.fetchone()[0]
    
    if cloud_select_count==0:
        alert_prod_count = sessions.query(AlertCloudPurchase).filter(AlertCloudPurchase.user_id == userid).count()

        # cursor.execute(f"select count(*) from alert_cloud_purchase where user_id={userid}")
        # alert_prod_count = cursor.fetchone()[0]
        if alert_prod_count == 0:
            cloud_selec_list = sessions.query(CloudPurchaseList).with_entities(CloudPurchaseList.cloud_type_id).filter(CloudPurchaseList.user_id == userid).first()

            # cursor.execute(f"select cloud_type_id from cloud_purchase_list where user_id={userid} and latest_entry=1 ")
            # cloud_selec_list = cursor.fetchone()

        else:
            cloud_selec_list = sessions.query(AlertCloudPurchase).with_entities(AlertCloudPurchase.cloud_type_id).filter(AlertCloudPurchase.user_id == userid, AlertCloudPurchase.latest_entry==1).first()

            # cursor.execute(f"select cloud_type_id from alert_cloud_purchase where user_id={userid} and latest_entry=1 ")
            # cloud_selec_list = cursor.fetchone()
            current_cloud_type = cloud_selec_list[0]

    else:
        cloud_selec_list = sessions.query(CloudSelection).with_entities(CloudSelection.cl_type_id).filter(CloudSelection.user_id == userid).first()
        # cursor.execute(f"select cl_type_id from cloud_selection where user_id={userid} ")
        # cloud_selec_list = cursor.fetchone()

    if request.method == 'POST':
        try:
            cloud_package = request.form['cloud_package']
            cloud_pac_amount = "cloud_amount_"+cloud_package
            cloud_amount = request.form[cloud_pac_amount]

            date_1 = cloud_renewal_date
            current_date = datetime.date(datetime.now())
            payment_date = current_date.strftime('%Y-%m-%d')
            date_2 = current_date
            # num_months = (date_1.year - date_2.year) * 12 + (date_1.month - date_2.month)
            remaining_months = alert_period(date_1,date_2)
            if remaining_months != "error":
                num_months = remaining_months[0]['months']
                alert_time_period = remaining_months[0]['alert']

                # if free trial there is no alert period
                if reg_user_type == "F":
                    alert_time_period = 0
                cld_renewal_date = cloud_renewal_date.strftime('%Y-%m-%d')
                
                if int(cloud_amount) > int(paid_cloud_amount):
                    if alert_time_period == 0:
                        balance_cloud_amount = int(cloud_amount) - int(paid_cloud_amount)
                        if reg_user_type == "F":
                            balance_amount = balance_cloud_amount
                        else:
                            balance_amount = int(balance_cloud_amount*(num_months/12))
                        insert_server_settings(cloud_package, balance_amount, userid)
                        flash('Added To Cart',"success")

                    else:
                        sessions.query(AlertCloudPurchase).filter(AlertCloudPurchase.user_id == userid).delete()
                        # cursor.execute(f"delete from alert_cloud_purchase where user_id={userid}")

                        inserted_alert_cloud = AlertCloudPurchase(user_id=userid, cloud_type_id=cloud_package, amount=cloud_amount, currency_type=currency, currency_symbol=currency_symbol, latest_entry=1, payment_date=payment_date, renewal_date=cld_renewal_date)
                        sessions.add(inserted_alert_cloud)
                        sessions.flush()
                        
                        # cursor.execute(f"Insert INTO alert_cloud_purchase (user_id,cloud_type_id,amount,currency_type,currency_symbol,latest_entry,payment_date,renewal_date) values {(userid,cloud_package,cloud_amount,currency,currency_symbol,1,payment_date,cld_renewal_date)}")

                        ''' insert cloud type in siteadmin  '''  

                        siteadmin_userid = siteadmin_session_set.query(Users.user_id).filter(Users.email==email).first()[0]

                        # cursor1.execute(f"select user_id from users where email='{email}' ")
                        # siteadmin_userid = cursor1.fetchone()[0]

                        siteadmin_session_set.query(CloudList).filter(CloudList.user_id == siteadmin_userid).delete()

                        # cursor1.execute(f"delete from cloud_list where user_id='{siteadmin_userid}'")

                        cloudtype_id = encryptdata(cloud_package)


                        inserted_site_cloud = CloudList(user_id=siteadmin_userid, cloud_type_id=cloudtype_id, renewal_date=cld_renewal_date)
                        siteadmin_session_set.add(inserted_site_cloud)
                        siteadmin_session_set.flush()

                        # cursor1.execute(
                        #     f"INSERT into cloud_list(user_id,cloud_type_id,renewal_date) values {(siteadmin_userid, cloudtype_id,cld_renewal_date )} ")
                        sessions.commit()
                        siteadmin_session_set.commit()
                        flash('No need for payment since you upgrade in the alert period',"success")

                else:
                    flash('cannot downgrade',"error")
            else:
                flash("Please Enter Alert Interval List","error")
            return redirect('/upgrade_cloud')

        except Exception as ex:
            sessions.rollback()
            flash(str(ex),"error")
            return redirect(url_for('upgrade_cloud'))    
    return render_template('upgrade_cloud.html', cloud_list=cloud_list,count_values=count_values, cloud_selec_list=cloud_selec_list,current_cloud_type=current_cloud_type)


''' function to show the amount of the individual packages selected '''


@app.route('/upgrade_estimation', methods=['GET', 'POST'])
def upgrade_estimation():
    if len(session)==0:
        return redirect(url_for('logout'))
    userid = session['userid']
    count_values = get_all_count()

    user_type_name = sessions.query(UserType.user_type_name).order_by(UserType.user_type_id.asc())

    # cursor.execute(
    #     f"select user_type_name from user_type order by user_type_id asc")
    # user_type_name = cursor.fetchall()

    reg_user_type = sessions.query(RegUsers.user_type).filter(RegUsers.user_id == userid).first()[0]
    print(reg_user_type,'reg_user_type')
    prod_count = sessions.query(ProductSelectionList).filter(ProductSelectionList.user_id == userid).count()

    # cursor.execute(f"select count(*) from product_selection_list a where a.user_id={userid}")
    # prod_count=cursor.fetchone()[0]

    if prod_count!=0:

        selected_pkg_prod = sessions.query(ProductSelectionList, PackageList).with_entities(ProductSelectionList.pkg_id, PackageList.pkg_name, ProductSelectionList.product_id, ProductSelectionList.amount).join(PackageList, ProductSelectionList.pkg_id == PackageList.pkg_id).filter(ProductSelectionList.user_id == userid).order_by(ProductSelectionList.selc_id.desc()).first()
        print(selected_pkg_prod,'selected_pkg_prod')
        if reg_user_type == 'F':
            pur_prod_only = selected_pkg_prod[2]
        else:
            if selected_pkg_prod[0] == 4:
                pkg_exist_prod = sessions.query(PackagePurchaseHistory.product_id).filter(PackagePurchaseList.user_id==userid).order_by(PackagePurchaseHistory.pkg_history_id.desc()).first()[0]

                pkg_exist_products = list(pkg_exist_prod.split(','))
                selected_pkg_prods = list(selected_pkg_prod[2].split(',')) 
                pur_prod_only = list(set(selected_pkg_prods) - set(pkg_exist_products))
            else:
                pur_prod_only = selected_pkg_prod[2]
        print(pur_prod_only,"pur_prod_only")



        # cursor.execute(
        #     f"select a.pkg_id,b.pkg_name,a.product_id,a.amount,a.selc_id from product_selection_list a left join package_list b on a.pkg_id=b.pkg_id where a.user_id={userid} order by a.selc_id desc")
        # selected_pkg_prod = cursor.fetchone()

    else:
       selected_pkg_prod = ''
       pur_prod_only = ''

    users_count = sessions.query(UserSelectionList).filter(UserSelectionList.user_id == userid).count()

    # cursor.execute(f"select count(*) from user_selection_list a where a.user_id={userid}")
    # users_count=cursor.fetchone()[0]

    if users_count!=0:
        selected_users_amount = sessions.query(UserSelectionList).with_entities(UserSelectionList.admin_user_count, UserSelectionList.admin_user_amount, UserSelectionList.general_user_count, UserSelectionList.general_user_amount,UserSelectionList.limited_user_count, UserSelectionList.limited_user_amount, UserSelectionList.amount, UserSelectionList.user_selc_id,UserSelectionList.billing_frequency, UserSelectionList.actual_amount,UserSelectionList.discount).order_by(UserSelectionList.user_selc_id.desc()).first()


        # cursor.execute(
        #     f"select a.admin_user_count,a.admin_user_amount,a.general_user_count,a.general_user_amount,a.limited_user_count, a.limited_user_amount,a.amount,a.user_selc_id,a.billing_frequency,a.actual_amount,a.discount from user_selection_list a  where a.user_id={userid} order by a.user_selc_id desc")
        # selected_users_amount = cursor.fetchone()
    else:
       selected_users_amount = ''

    cloud_count = sessions.query(CloudSelection).filter(CloudSelection.user_id == userid).count()

    # cursor.execute(f"select count(*) from cloud_selection a where a.user_id={userid}")
    # cloud_count=cursor.fetchone()[0]

    if cloud_count!=0:

        cloud_pack_amount = sessions.query(CloudSelection, CloudType, CloudPricing ).with_entities(CloudSelection.cloud_id, CloudSelection.amount, CloudType.cl_type_name, CloudPricing.features).join(CloudType, CloudSelection.cl_type_id == CloudType.cl_type_id).join(CloudPricing, CloudSelection.cl_type_id == CloudPricing.cl_type_id).filter(CloudSelection.user_id == userid).order_by(CloudSelection.cloud_id.desc()).first()

        # cursor.execute(
        #     f"select a.cloud_id,a.amount,b.cl_type_name,c.features from cloud_selection a left join cloud_type b on a.cl_type_id=b.cl_type_id left join cloud_pricing c on a.cl_type_id=c.cl_type_id where a.user_id={userid} order by a.cloud_id desc")
        # cloud_pack_amount = cursor.fetchone()

    else:
       cloud_pack_amount = ''       

    newdate = datetime.date(datetime.now())
    newdates = newdate + relativedelta(years=1, days=-1)
    monthdates = newdate + relativedelta(months=1, days=-1)

    product_list = sessions.query(ProductList).order_by(ProductList.product_id.asc()).all()

    # cursor.execute(f"select * from product_list")
    # columns = [col[0] for col in cursor.description]
    # product_list = [dict(zip(columns, row)) for row in cursor.fetchall()]

    pkg_renewal_date = sessions.query(PackagePurchaseList.renewal_date).filter(PackagePurchaseList.user_id==userid).first()[0]

    
# cursor.execute(
    #     f"select a.renewal_date from package_purchase_list a  where a.user_id={userid}")
    # pkg_renewal_date = cursor.fetchone()[0]

    user_renewal_date = sessions.query(UserPurchaseList.renewal_date).filter(UserPurchaseList.user_id==userid).first()[0]

    admin_exist_users = sessions.query(UserPurchaseList.no_of_users).filter(UserPurchaseList.user_id==userid,UserPurchaseList.user_type_id==1).first()[0]

    gen_exist_users = sessions.query(UserPurchaseList.no_of_users).filter(UserPurchaseList.user_id==userid,UserPurchaseList.user_type_id==2).first()[0]

    lim_exist_users = sessions.query(UserPurchaseList.no_of_users).filter(UserPurchaseList.user_id==userid,UserPurchaseList.user_type_id==3).first()[0]

    # cursor.execute(
    #     f"select a.renewal_date from user_purchase_list a  where a.user_id={userid}")
    # user_renewal_date = cursor.fetchone()[0]

    cloud_renewal_date = sessions.query(CloudPurchaseList.renewal_date).filter(CloudPurchaseList.user_id==userid).first()[0]

    # cursor.execute(
    #     f"select a.renewal_date from cloud_purchase_list a  where a.user_id={userid}")
    # cloud_renewal_date = cursor.fetchone()[0]

    date_1 = pkg_renewal_date
    current_date = datetime.date(datetime.now())
    payment_date = current_date.strftime('%Y-%m-%d')
    date_2 = current_date
    user_remaining_months = (date_1.year - date_2.year) * 12 + (date_1.month - date_2.month)

    if request.method == "POST":
        if reg_user_type == "F":
            if selected_pkg_prod == '':
                flash('Cannot proceed without Product packages',"error")
                return redirect("/upgrade_estimation")  
            elif selected_users_amount == '':
                flash('Cannot proceed without user packages',"error")
                return redirect("/upgrade_estimation")   
            else:
                print("else")
                return redirect("/free_trial_billing")
        else:
            return redirect("/checkout")

    return render_template('upgrade_estimation.html', selected_pkg_prod=selected_pkg_prod, product_list=product_list, selected_users_amount=selected_users_amount, cloud_pack_amount=cloud_pack_amount, count_values=count_values, newdates=newdates, monthdates=monthdates, user_type_name=user_type_name,pkg_renewal_date=pkg_renewal_date,user_renewal_date=user_renewal_date,cloud_renewal_date=cloud_renewal_date,user_remaining_months=user_remaining_months,admin_exist_users=admin_exist_users,gen_exist_users=gen_exist_users,lim_exist_users=lim_exist_users,pur_prod_only=pur_prod_only)


''' function to show the amount of the individual packages selected and the order summary of the selected products with gst '''


@app.route('/free_trial_billing', methods=['GET', 'POST'])
def free_trial_billing():
    if len(session)==0:
        return redirect(url_for('logout'))
    status = session['status']
    email = session['email']
    userid = session['userid']
    gst = float(session['gst'].strip('%'))
    # server_count = session['server_count']
    count_values = get_all_count()
    print(count_values,"count_values")

    company_id = sessions.query(CompanyDetails.company_id).filter_by(user_id=userid).first()[0]

    location_list = sessions.query(Location).with_entities(Location.location_id,Location.location_name).filter(Location.company_id == company_id).first()
    location_id = location_list[0]
    location_name = location_list[1]  

    countries_list = sessions.query(Country).with_entities(Country.country_id, Country.country_name,Country.country_code).all()

    company_list = sessions.query(CompanyDetails).with_entities(CompanyDetails.country_id, CompanyDetails.state_id, CompanyDetails.city_id, CompanyDetails.company_id, CompanyDetails.company_name).filter(CompanyDetails.user_id == userid).first()
    print(company_list,"company_list")

    comp_country_id = company_list[0]
    comp_state_id = company_list[1]
    comp_city_id = company_list[2]
    company_id = company_list[3]
    company_name = company_list[4]
    
    location_list = sessions.query(Location).with_entities(Location.location_id,Location.location_name).filter(Location.company_id == company_id).first()
    location_id = location_list[0]
    location_name = location_list[1]

    product_amount = sessions.query(ProductSelectionList.amount).filter(ProductSelectionList.user_id == userid).first()[0]

    user_amount = sessions.query(UserSelectionList.amount).filter(UserSelectionList.user_id == userid).first()[0]

    cloud_amount = sessions.query(CloudSelection.amount).filter(CloudSelection.user_id == userid).first()[0]

    total_bill_amount = float(product_amount) + float(user_amount) + float(cloud_amount)
    total_gst_amnt = total_bill_amount + ((gst/100) * total_bill_amount)

    states_list = sessions.query(State).with_entities(State.state_id, State.state_name,State.state_code).filter(State.country_id == comp_country_id).all()

    cities_list = sessions.query(City).with_entities(City.city_id, City.city_name).filter(State.state_id == comp_state_id).all()

    payment_made = 'false'
    last_pay_his_id = 0

    if request.method == 'POST':
        try:
            invoice_Company = request.form['invoice_Company']
            gst_vat = request.form['gst_vat']
            invoice_address = request.form['invoice_address']
            country = request.form['country']
            if country == "":
                country = request.form['comp_country']
            state = request.form['state']
            if state == "":
                state = request.form['comp_state']
            city = request.form['city']
            if city == "":
                city = request.form['comp_city']

            bill_no = rand_pass(6)

            get_bill_details = get_bill_no()
            bill_no = get_bill_details[0]['bill_no']
            pur_no = get_bill_details[0]['pur_no']
            bill_num_val = get_bill_details[0]['bill_num_val']
            pur_num_val = get_bill_details[0]['pur_num_val']


            res = freetrial_billing_details(bill_no, invoice_Company, gst_vat, invoice_address, country, state, city, userid, total_gst_amnt, company_id,location_id,bill_no,bill_num_val,pur_no,pur_num_val)
            last_pay_his_id = res
            # start_service(company_name,location_name)
            
            # msg = Message('Link', sender='username@gmail.com', recipients=[logged_in_emailid])
            # link = 'http://144.48.49.10:'+str(port_no)+'/login'
            # msg.body = 'Your link is {}'.format(link)
            # msg.html = render_template('emails/site_link.html', link=link)
            # mail.send(msg)

            # connection.commit()

            # flash(result)
            # return redirect('/my_account')
            payment_made = 'true'
            return redirect(url_for('my_account', payment_made=payment_made,last_pay_his_id=last_pay_his_id, mode='billing', **request.args))

        except Exception as ex:
            sessions.rollback()
            flash(str(ex),"error")
            return redirect(url_for('free_trial_billing'))     

    return render_template('free_trial_billing.html', status=status, email=email, countries_list=countries_list, states_list=states_list, cities_list=cities_list, comp_state_id=comp_state_id, comp_city_id=comp_city_id, comp_country_id=comp_country_id, count_values=count_values, total_gst_amnt=total_gst_amnt)


''' function to show the amount of the individual packages selected and the order summary of the selected products with gst '''


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if len(session)==0:
        return redirect(url_for('logout'))
    userid = session['userid']
    count_values = get_all_count()
    company_id = sessions.query(CompanyDetails.company_id).filter(CompanyDetails.user_id == userid).first()[0]

    location_list = sessions.query(Location).with_entities(Location.location_id,Location.location_name).filter(Location.company_id == company_id).first()
    location_id = location_list[0]
    location_name = location_list[1]


    user_type_name = sessions.query(UserType.user_type_name).order_by(UserType.user_type_id.asc())
    print(user_type_name,"user_type_name")
    # cursor.execute(
    #     f"select user_type_name from user_type order by user_type_id asc")
    # user_type_name = cursor.fetchall()

    prod_count = sessions.query(ProductSelectionList).filter(ProductSelectionList.user_id == userid).count()

    # cursor.execute(f"select count(*) from product_selection_list a where a.user_id={userid}")
    # prod_count=cursor.fetchone()[0]

    if prod_count!=0:
        selected_pkg_prod = sessions.query(ProductSelectionList, PackageList).with_entities(ProductSelectionList.pkg_id, PackageList.pkg_name, ProductSelectionList.product_id, ProductSelectionList.amount, ProductSelectionList.selc_id).join(PackageList, ProductSelectionList.pkg_id == PackageList.pkg_id).filter(ProductSelectionList.user_id == userid).order_by(ProductSelectionList.selc_id.desc()).first()

        # cursor.execute(
        #     f"select a.pkg_id,b.pkg_name,a.product_id,a.amount,a.selc_id from product_selection_list a left join package_list b on a.pkg_id=b.pkg_id where a.user_id={userid} order by a.selc_id desc")
        # selected_pkg_prod = cursor.fetchone()

    else:
       selected_pkg_prod = ''

    users_count = sessions.query(UserSelectionList).filter(UserSelectionList.user_id == userid).count()

    # cursor.execute(f"select count(*) from user_selection_list a where a.user_id={userid}")
    # users_count=cursor.fetchone()[0]

    if users_count!=0:
        selected_users_amount = sessions.query(UserSelectionList).with_entities(UserSelectionList.admin_user_count, UserSelectionList.admin_user_amount, UserSelectionList.general_user_count, UserSelectionList.general_user_amount,UserSelectionList.limited_user_count, UserSelectionList.limited_user_amount, UserSelectionList.amount, UserSelectionList.user_selc_id,UserSelectionList.billing_frequency, UserSelectionList.actual_amount,UserSelectionList.discount).order_by(UserSelectionList.user_selc_id.desc()).first()


        # cursor.execute(
        #     f"select a.admin_user_count,a.admin_user_amount,a.general_user_count,a.general_user_amount,a.limited_user_count, a.limited_user_amount,a.amount,a.user_selc_id,a.billing_frequency,a.actual_amount,a.discount from user_selection_list a  where a.user_id={userid} order by a.user_selc_id desc")
        # selected_users_amount = cursor.fetchone()
    else:
       selected_users_amount = ''

    cloud_count = sessions.query(CloudSelection).filter(CloudSelection.user_id == userid).count()

    # cursor.execute(f"select count(*) from cloud_selection a where a.user_id={userid}")
    # cloud_count=cursor.fetchone()[0]

    if cloud_count!=0:
        cloud_pack_amount = sessions.query(CloudSelection, CloudType, CloudPricing ).with_entities(CloudSelection.cloud_id, CloudSelection.amount, CloudType.cl_type_name, CloudPricing.features).join(CloudType, CloudSelection.cl_type_id == CloudType.cl_type_id).join(CloudPricing, CloudSelection.cl_type_id == CloudPricing.cl_type_id).filter(CloudSelection.user_id == userid).order_by(CloudSelection.cloud_id.desc()).first()

        # cursor.execute(
        #     f"select a.cloud_id,a.amount,b.cl_type_name,c.features from cloud_selection a left join cloud_type b on a.cl_type_id=b.cl_type_id left join cloud_pricing c on a.cl_type_id=c.cl_type_id where a.user_id={userid} order by a.cloud_id desc")
        # cloud_pack_amount = cursor.fetchone()

    else:
       cloud_pack_amount = ''       

    product_list = sessions.query(ProductList).order_by(ProductList.product_id.asc()).all()

    # cursor.execute(f"select * from product_list")
    # columns = [col[0] for col in cursor.description]
    # product_list = [dict(zip(columns, row)) for row in cursor.fetchall()]

    if request.method == "POST":
        try:
            print("try")
            selected_product_id= request.form['selected_product_id']
            selected_user_id=request.form['selected_user_id']
            selected_cloud_id=request.form['selected_cloud_id']
            selected_products_amount = request.form['selected_pkg_totamnt']
            print(selected_product_id,selected_user_id,selected_cloud_id,selected_products_amount)


            get_bill_details = get_bill_no()
            bill_no = get_bill_details[0]['bill_no']
            pur_no = get_bill_details[0]['pur_no']
            bill_num_val = get_bill_details[0]['bill_num_val']
            pur_num_val = get_bill_details[0]['pur_num_val']

            result = insert_upgrade_billing(selected_product_id,selected_user_id,selected_cloud_id,userid,selected_products_amount,location_id,company_id,bill_no,pur_no,bill_num_val,pur_num_val)
            print("result")

            last_pay_his_id = result
            payment_made = 'true'

            # return redirect(url_for('my_account'))
            return redirect(url_for('my_account', payment_made='true',last_pay_his_id=last_pay_his_id, mode='upgrade',  **request.args))

        except Exception as ex:
            sessions.rollback()
            flash(str(ex),"error")
            return redirect(url_for('checkout'))     

    return render_template('checkout.html', selected_pkg_prod=selected_pkg_prod, product_list=product_list, selected_users_amount=selected_users_amount, cloud_pack_amount=cloud_pack_amount, count_values=count_values, user_type_name=user_type_name)


''' function to edit the company name or site name or address after billing.Changes in this function will be updated in siteadmin '''


@app.route('/upgrade_company', methods=['GET', 'POST'])
def upgrade_company():
    if len(session)==0:
        return redirect(url_for('logout'))
    userid = session['userid']
    status = session['status']
    email = session['email']
    current_date = datetime.date(datetime.now())
    count_values = get_all_count()
    states_list = " "
    cities_list = " "
    # server_count = session['server_count']
    email_domain = email.split('@')[1]
    emaildomain = "@"+str(email_domain)
    #cursor.execute(f"select * from country")
    countries_list = sessions.query(Country).all()

    sample_cmpy_list = sessions.query(CompanyDetails.company_name).filter(CompanyDetails.email==emaildomain).group_by(CompanyDetails.company_name).all()

    comp_details_count = sessions.query(CompanyDetails).filter(CompanyDetails.user_id==userid).count()
    if comp_details_count != 0:
        comp_details = sessions.query(CompanyDetails).filter(CompanyDetails.user_id==userid).first()
        usr_cmpy_name = comp_details.company_name
        usr_address = comp_details.address
        usr_email = comp_details.email
        usr_site = comp_details.site_name
        usr_country = comp_details.country_id
        usr_state = comp_details.state_id
        usr_city = comp_details.city_id
        print(usr_country, usr_state,usr_city )
        if usr_country is not None:
            states_list = sessions.query(State).filter(State.country_id==usr_country).all()
        if usr_state is not None:
            cities_list = sessions.query(City).filter(City.state_id==usr_state).all()
    else:

        usr_cmpy_name = ""
        usr_address = ""
        usr_email = ""
        usr_site = ""
        usr_country = ""
        usr_state = ""
        usr_city = ""

    if request.method == 'POST':
        try:
            email = request.form['email']
            site_name = request.form['site_name']
            address = request.form['address']
            company_name = request.form['company_name']
            # sample_company = request.form['sample_company']
            # if sample_company == "new":
            #     company_name = request.form['company_name']
            # else:
            #     company_name = sample_company
            currency = sessions.query(Country).filter_by(country_id=usr_country).first()

            gst_per_count = sessions.query(Gst).filter_by(country_id=usr_country).count()

            if gst_per_count != 0:
                gst_per = sessions.query(Gst.gst_per).filter(Gst.country_id==usr_country,Gst.effective_from_date <= current_date).order_by(Gst.gst_id.desc()).first()[0]
            else:
                gst_per = "0%"

            session['gst'] = gst_per
            session['currency'] = currency.currency
            session['currency_symbol'] = currency.currency_symbol

            result = update_upgrade_company(
                email, site_name, address, company_name,  userid, usr_country,usr_state,usr_city)
            if result == "Added Successfully" or result == "Updated Successfully":
                flash(result)
                return redirect(url_for('upgrade_company'))
            else:
                return render_template('upgrade_company.html', comp_name=company_name, addr=address, email_domain=email, usr_site_name=site_name, status=status, email=email, server_count=server_count, sample_cmpy_list=sample_cmpy_list, comp_details_count=comp_details_count, countries_list=countries_list, states_list=states_list, cities_list=cities_list, com_country=country, com_state=state, com_city=city, count_values=count_values, result=result)

        except Exception as ex:
            sessions.rollback()
            flash(str(ex))
            return redirect(url_for('upgrade_company'))   

    return render_template('upgrade_company.html', comp_name=usr_cmpy_name, addr=usr_address, email_domain=usr_email, usr_site_name=usr_site, status=status, email=email,  sample_cmpy_list=sample_cmpy_list, comp_details_count=comp_details_count, countries_list=countries_list, com_country=usr_country, states_list=states_list, cities_list=cities_list, com_state=usr_state, com_city=usr_city,  count_values=count_values)


''' function to redirect to the about page '''


@app.route('/about', methods=['GET', 'POST'])
def about():
    if len(session) != 0:
        count_values = get_all_count()
    else:
        count_values = ""
    return render_template('about.html',count_values=count_values)


''' function to get all count values when packages are added before billing'''


def get_all_count():
    userid = session['userid']
    email = session['email']
    port_no = ' '
    company_count = sessions.query(CompanyDetails).filter(CompanyDetails.user_id==userid).count()

    billing_count = sessions.query(BillingDetails).filter(BillingDetails.user_id==userid).count()
    if billing_count != 0:
        company_port_det = sessions.query(CompanyDetails.company_id,PortList.port_no).join(PortList, CompanyDetails.company_id == PortList.company_id).filter(CompanyDetails.user_id==userid).first()
        # port_no = company_port_det[1]

        port_no = 0

    cloud_selection_count = sessions.query(CloudSelection).filter(CloudSelection.user_id==userid).count()

    product_count = sessions.query(ProductSelectionList).filter(ProductSelectionList.user_id==userid).count()

    user_selection_count = sessions.query(UserSelectionList).filter(UserSelectionList.user_id==userid).count()

    reg_user_type = sessions.query(RegUsers.user_type).filter(RegUsers.user_id == userid).first()[0]
    # cursor.execute(
    #     f"select count(*) from company_details where user_id={userid}")
    # company_count = cursor.fetchone()[0]
    # cursor.execute(
    #     f"select count(*) from cloud_selection where user_id={userid}")
    # cloud_selection_count = cursor.fetchone()[0]
    # cursor.execute(
    #     f"select count(*) from product_selection_list where user_id={userid}")
    # product_count = cursor.fetchone()[0]
    # cursor.execute(
    #     f"select count(*) from user_selection_list where user_id={userid}")
    # user_selection_count = cursor.fetchone()[0]
    free_trial_expire_count = sessions.query(RegUsers).filter(RegUsers.email==email,RegUsers.status==2,RegUsers.user_type=='F').count()
    total_count = cloud_selection_count + product_count + user_selection_count
    
    list = []
    # list.append(company_count)
    list.append({'company_count': company_count, 'cloud_selection_count': cloud_selection_count,
                 'product_count': product_count, 'user_selection_count': user_selection_count , 'total_count': total_count,'reg_user_type':reg_user_type,'free_trial_expire_count': free_trial_expire_count,'port_no':port_no})
    return list


''' function to list the admin users inserted in siteadmin for the particular company '''


@app.route('/company_users', methods=['GET', 'POST'])
def company_users():
    if len(session)==0:
        return redirect(url_for('logout'))
    userid = session['userid']
    count_values = get_all_count()
    dynamic_table_name = sessions.query(CompanyDetails.dynamic_table_name).filter(CompanyDetails.user_id==userid).first()[0]

    # payment_history_report = sessions.query(PaymentHistory).filter(PaymentHistory.user_id==userid).all()
    dynamic_table = Table(dynamic_table_name, metadata,Column('user_id', Integer, primary_key=True), Column('user_name', String, nullable=False), Column('emp_code', String), Column('email', String, nullable=False), Column('created_by', BigInteger), Column('created_date', DateTime(timezone=True), default=func.now(), nullable=False), Column('updated_by', BigInteger), Column('updated_date', DateTime(timezone=True), default=func.now()), Column('status', String),extend_existing=True)
    metadata.create_all(engine)

    ins = dynamic_table.select()
    conn = engine.connect()
    sample_cmpy_list = conn.execute(ins)
    print(sample_cmpy_list)
    
    # cursor.execute(
    #     f"select * from {dynamic_table_name} ")
    
    # columns = [col[0] for col in cursor.description]
    # sample_cmpy_list = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    return render_template('company_users.html', sample_cmpy_list=sample_cmpy_list,count_values=count_values)


''' function to redirect to the private setup page if the cloud package is private '''


@app.route('/private_setup', methods=['GET', 'POST'])
def private_setup():
    if len(session)==0:
        return redirect(url_for('logout'))
    count_values = get_all_count()
    return render_template('private_setup.html', count_values=count_values)


''' function to list all payments done by the user '''


@app.route('/payment_history_report', methods=['GET', 'POST'])
def payment_history_report():
    if len(session)==0:
        return redirect(url_for('logout'))
    userid = session['userid']
    cur_sym = session['currency_symbol']
    count_values = get_all_count()
    payment_history_report = sessions.query(PaymentHistory).filter(PaymentHistory.user_id==userid, PaymentHistory.amount != "0.0").order_by(PaymentHistory.payment_history_id.asc()).all()
    print(payment_history_report,"payment_history_report")

    product_list = sessions.query(ProductList).order_by(ProductList.product_id.asc()).all()

    pkg_pur_his = sessions.query(PackagePurchaseHistory).filter(PackagePurchaseHistory.user_id==userid).order_by(PackagePurchaseHistory.pkg_history_id.asc()).all()

    cloud_pur_his = sessions.query(CloudPurchaseHistory).filter(CloudPurchaseHistory.user_id==userid).order_by(CloudPurchaseHistory.cloud_history_id.asc()).all()

    user_pur_his = sessions.query(UserPurchaseHistory).filter(UserPurchaseHistory.user_id==userid).order_by(UserPurchaseHistory.user_history_id.asc()).all()
    cloud_list = sessions.query(CloudType).order_by(CloudType.cl_type_id.asc()).all()

    return render_template('payment_history_report.html', count_values=count_values, payment_history_report=payment_history_report,product_list=product_list,cloud_list=cloud_list,user_pur_his=user_pur_his,pkg_pur_his=pkg_pur_his,cloud_pur_his=cloud_pur_his,cur_sym=cur_sym)


''' function to check if the email exists or not in login function '''


@app.route('/ajax_load_email', methods=['GET', 'POST'])
def ajax_load_email():
    email = request.args.get('email')
    emailcount = sessions.query(RegUsers).filter(RegUsers.email==email).count()
    return str(emailcount)


''' function to change the password and a message is sent to the mail'''


@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    userid = session['userid']
    user_email = session['email']
    count_values = get_all_count()
    if request.method == 'POST':
        try:
            old_password = request.form['old_password']
            user_password = sessions.query(RegUsers.password).filter(RegUsers.user_id==userid).first()[0]

            if check_password_hash(user_password, old_password):
                new_password = request.form['new_password']
                password_hash = generate_password_hash(new_password)
                sessions.query(RegUsers).filter(RegUsers.user_id == userid).update({RegUsers.password: password_hash})
                sessions.commit()
                result = "Your password has been changed"

                msg = Message('Information', sender='sneha.r@perpetua.co.in', recipients=[user_email])
                message = "Your password has been reset"
                msg.body = message
                mail.send(msg)

                flash(result,"success")
            else:
                result = "Invalid Current Password"
                flash(result,"error")

        except Exception as ex:
            sessions.rollback()
            flash(str(ex))
            return redirect('/change_password')
        return redirect('/change_password')
    return render_template('change_password.html',count_values=count_values)


''' function to check if the password exists or not in change_password function '''


@app.route('/ajax_load_password', methods=['GET', 'POST'])
def ajax_load_password():
    userid = session['userid']
    password = request.args.get('old_password')
    user_password = sessions.query(RegUsers.password).filter(RegUsers.user_id==userid).first()[0]

    if check_password_hash(user_password, password):
        password_count = 1
    else:
        password_count = 0

    return str(password_count)


''' function to payment process after payment failure '''


@app.route('/auto_renewal', methods=['GET', 'POST'])
def auto_renewal():
    userid = session['userid']
    gst_percent = session['gst']
    count_values = get_all_count()
    current_date = datetime.date(datetime.now())

    failed_payment_details = sessions.query(PaymentStatus).filter(PaymentStatus.user_id == userid, PaymentStatus.from_date < current_date , current_date < PaymentStatus.to_date)
    
    # cursor.execute(f"select * from payment_status where user_id={userid} and from_date < current_date and current_date < to_date order by status_id ")
    # columns = [col[0] for col in cursor.description]
    # failed_payment_details = [dict(zip(columns, row)) for row in cursor.fetchall()]

    alert_pkg_count = sessions.query(AlertPackagePurchase).filter(AlertPackagePurchase.user_id == userid).count()

    # cursor.execute(f"select count(*) from alert_package_purchase where user_id={userid}")
    # alert_pkg_count = cursor.fetchone()[0]
    if alert_pkg_count != 0:
        pkg_amount = sessions.query(AlertPackagePurchase.amount).filter(AlertPackagePurchase.user_id == userid).first()[0]

        # cursor.execute(f"select amount from alert_package_purchase where user_id={userid}")
        # pkg_amount = cursor.fetchone()[0]

    else:
        pkg_amount = sessions.query(PackagePurchaseList.amount).filter(PackagePurchaseList.user_id == userid).first()[0]

        # cursor.execute(f"select amount from package_purchase_list where user_id={userid}")
        # pkg_amount = cursor.fetchone()[0]

    exist_user_billing_freq = sessions.query(UserPurchaseList.billing_frequency).filter(UserPurchaseList.user_id == userid).first()[0]

    # cursor.execute(f"select DISTINCT billing_frequency from user_purchase_list where user_id={userid}")
    # exist_user_billing_freq1 = cursor.fetchone()[0]
    alert_user_count = sessions.query(AlertUserPurchase).filter(AlertUserPurchase.user_id == userid).count()

    # cursor.execute(f"select count(*) from alert_user_purchase where user_id={userid}")
    # alert_user_count = cursor.fetchone()[0]
    if alert_user_count != 0:
        
        user_amount = sessions.query(AlertUserPurchase).with_entities(func.sum(AlertUserPurchase.amount.cast(DECIMAL)).label('amount')).filter(AlertUserPurchase.user_id == userid).first()[0]
        # cursor.execute(f"select amount from alert_user_purchase where user_id={userid}")
        # user_amount = cursor.fetchone()[0]

    else:
        user_amount = sessions.query(UserPurchaseList).with_entities(func.sum(UserPurchaseList.amount.cast(DECIMAL)).label('amount')).filter(UserPurchaseList.user_id == userid).first()[0]
        # cursor.execute(f"select amount from user_purchase_list where user_id={userid}")
        # user_amount = cursor.fetchone()[0]

    alert_cloud_count = sessions.query(AlertCloudPurchase).filter(AlertCloudPurchase.user_id == userid).count()

    # cursor.execute(f"select count(*) from alert_cloud_purchase where user_id={userid}")
    # alert_cloud_count = cursor.fetchone()[0]
    if alert_cloud_count != 0:
        cloud_amount = sessions.query(AlertCloudPurchase.amount).filter(AlertCloudPurchase.user_id == userid).first()[0]
        # cursor.execute(f"select amount from alert_cloud_purchase where user_id={userid}")
        # cloud_amount = cursor.fetchone()[0]

    else:
        cloud_amount = sessions.query(CloudPurchaseList.amount).filter(CloudPurchaseList.user_id == userid).first()[0]
        # cursor.execute(f"select amount from cloud_purchase_list where user_id={userid}")
        # cloud_amount = cursor.fetchone()[0]


    if request.method == "POST":
        paymentstatusid = request.form['paymentstatusid']
        paymentstatus_type = 'payment_type_'+paymentstatusid
        payment_type = request.form.get(paymentstatus_type)
        paymentstatus_amount = 'payment_amount_'+paymentstatusid
        payment_amount = request.form.get(paymentstatus_amount)
       
        if payment_type == "M":
            payment_amount_monthly = payment_amount
            usr_renewaldate = sessions.query(UserPurchaseList.renewal_date).filter(UserPurchaseList.user_id == userid).first()[0]

            # cursor.execute(f"select renewal_date from user_purchase_list where user_id={userid}")
            # usr_renewaldate = cursor.fetchone()[0]
            user_renewal_datetime = usr_renewaldate + relativedelta(months=1, days=-1)

            payment_status = True

            alert_user_table_count = sessions.query(AlertUserPurchase).filter(AlertUserPurchase.user_id == userid).count()


            # cursor.execute(f"select count(*) from alert_user_purchase where user_id = {userid} ")
            # alert_user_table_count = cursor.fetchone()[0]

            if payment_status is True:

                if alert_user_table_count == 0:
                    updated_user = sessions.query(UserPurchaseList).filter(UserPurchaseList.user_id == userid).update({ UserPurchaseList.payment_date:current_date, UserPurchaseList.renewal_date:user_renewal_datetime  })
                    

                    # cursor.execute(f"update user_purchase_list set payment_date='{current_date}',renewal_date='{user_renewal_datetime}' where user_id={userid} ")

                    # inserted_user_pur = UserPurchaseHistory(user_pur_id, user_id,user_type_id,no_of_users,amount,currency_type,currency_symbol,latest_entry,payment_date,renewal_date,billing_frequency).from_select(UserPurchaseList)
                    # sessions.add(inserted_user_pur)
                    # sessions.flush()
                    # sessions.commit()

                    
                    
                    # cursor.execute(f"INSERT INTO user_purchase_history(user_pur_id, user_id,user_type_id,no_of_users,amount,currency_type,currency_symbol,latest_entry,payment_date,renewal_date,billing_frequency) SELECT user_pur_id,user_id,user_type_id,no_of_users,amount,currency_type,currency_symbol,latest_entry,payment_date,renewal_date,billing_frequency FROM user_purchase_list where user_id={userid};")
                    
                    
                    # connection.commit()

                else:  # in alert table
                    update_usr_purchase = sessions.query(AlertUserPurchase).with_entities(AlertUserPurchase.user_pur_id, AlertUserPurchase.user_id , AlertUserPurchase.user_type_id , AlertUserPurchase.no_of_users , AlertUserPurchase.amount , AlertUserPurchase.currency_type, AlertUserPurchase.currency_symbol , AlertUserPurchase.latest_entry , AlertUserPurchase.payment_date , AlertUserPurchase.renewal_date , AlertUserPurchase.billing_frequency).filter(AlertUserPurchase.user_id==userid).all()

                    for update_usr_pur in update_usr_purchase:
                        sessions.query(UserPurchaseList).filter(UserPurchaseList.user_id==userid, update_usr_pur[1]==userid, UserPurchaseList.user_type_id == update_usr_pur[2]).update({UserPurchaseList.user_id: update_usr_pur[1], UserPurchaseList.user_type_id: update_usr_pur[2], UserPurchaseList.no_of_users: update_usr_pur[3], UserPurchaseList.amount: update_usr_pur[4],UserPurchaseList.currency_type: update_usr_pur[5], UserPurchaseList.currency_symbol: update_usr_pur[6],UserPurchaseList.latest_entry: update_usr_pur[7], UserPurchaseList.payment_date: current_date,UserPurchaseList.renewal_date: user_renewal_datetime, UserPurchaseList.billing_frequency: update_usr_pur[10] })
                    
                    # cursor.execute(f"Update user_purchase_list a set user_id=b.user_id,user_type_id=b.user_type_id,no_of_users=b.no_of_users ,amount=b.amount,currency_type=b.currency_type,currency_symbol=b.currency_symbol,latest_entry=b.latest_entry,payment_date='{current_date}',renewal_date='{user_renewal_datetime}',billing_frequency=b.billing_frequency from alert_user_purchase b where b.user_id={userid} and a.user_id={userid} and a.user_type_id=b.user_type_id")

                    # cursor.execute(f"INSERT INTO user_purchase_history(user_pur_id, user_id,user_type_id,no_of_users,amount,currency_type,currency_symbol,latest_entry,payment_date,renewal_date,billing_frequency) SELECT user_pur_id,user_id,user_type_id,no_of_users,amount,currency_type,currency_symbol,latest_entry,payment_date,renewal_date,billing_frequency FROM user_purchase_list where user_id={userid};")

                    # cursor.execute(f"delete from alert_user_purchase where user_id={userid} ")
                    sessions.query(AlertUserPurchase).filter_by(user_id=userid).delete()

                select_usr_purchase = sessions.query(UserPurchaseList).with_entities(UserPurchaseList.user_pur_id, UserPurchaseList.user_id , UserPurchaseList.user_type_id , UserPurchaseList.no_of_users , UserPurchaseList.amount , UserPurchaseList.currency_type, UserPurchaseList.currency_symbol , UserPurchaseList.latest_entry , UserPurchaseList.payment_date , UserPurchaseList.renewal_date , UserPurchaseList.billing_frequency).filter(UserPurchaseList.user_id==userid).all()

                for select_usr_pur in select_usr_purchase:
                    sessions.add(UserPurchaseHistory(user_pur_id=select_usr_pur[0], user_id=select_usr_pur[1], user_type_id=select_usr_pur[2], no_of_users=select_usr_pur[3], amount=select_usr_pur[4],currency_type=select_usr_pur[5], currency_symbol=select_usr_pur[6],latest_entry=select_usr_pur[7], payment_date=select_usr_pur[8],renewal_date=select_usr_pur[9], billing_frequency=select_usr_pur[10] ))
                    sessions.flush()

                # cursor.execute(f"Insert into payment_history(payment_date,mode_of_payment,amount,transaction_details,user_id,status) values {(str(current_date),'credit_card',payment_amount_monthly,'1246566',userid,1)} ")

                # card_no_val = '09764'
                # card_no = encryptdata(card_no_val)
                # cvv_no_val = '998'
                # cvv_no = encryptdata(cvv_no_val)

                # expiry_date_val = '04/20'
                # expiry_date = encryptdata(expiry_date_val)

                # cursor.execute(f"Insert into payment_mode(mode_of_payment,card_number,account_holder_name,cvv,expiry_date,user_id) values {('credit_card',card_no,'scopiq',cvv_no,expiry_date,userid)} ")
                # connection.commit()
                inserted_pay_his = PaymentHistory(payment_date=current_date, mode_of_payment='credit_card', amount=payment_amount_monthly, transaction_details='1246566', user_id=userid, status=1)
                sessions.add(inserted_pay_his)
                sessions.flush()

                card_no_val = '09764'
                card_no = encryptdata(card_no_val)
                cvv_no_val = '998'
                cvv_no = encryptdata(cvv_no_val)
                expiry_date_val = '04/20'
                expiry_date = encryptdata(expiry_date_val)

                inserted_pay_his = PaymentMode(mode_of_payment='credit_card', card_number=card_no, account_holder_name='scopiq', cvv=cvv_no, expiry_date=expiry_date, user_id=userid)
                sessions.add(inserted_pay_his)
                sessions.flush()

                sessions.commit()
                msg = Message('Payment Information', sender='sneha.r@perpetua.co.in', recipients=[user_email])
                message = "Your Monthly payment was Successful"
                msg.body = message
                msg.html = render_template('emails/alert_mail_remainder.html', expiry_details=message)
                mail.send(msg)
                
            else:
                flash('Your Payment was failed')

        elif payment_type == "A":
            payment_amount_annual = payment_amount
            pkg_renewaldate = sessions.query(PackagePurchaseList.renewal_date).filter(PackagePurchaseList.user_id == userid).first()[0]

            # cursor.execute(f"select renewal_date from package_purchase_list where user_id={userid}")
            # pkg_renewaldate = cursor.fetchone()[0]
            pkg_renewal_datetime = pkg_renewaldate + relativedelta(years=1, days=-1)
            print(pkg_renewal_datetime,"pkg_renewal_datetime")
            payment_status = True
            # print("hi",payment_status)
            alert_pkg_table_count = sessions.query(AlertPackagePurchase).filter(AlertPackagePurchase.user_id == userid).count()

            # cursor.execute(f"select count(*) from alert_package_purchase where user_id = {userid} ")
            # alert_pkg_table_count = cursor.fetchone()[0]

            alert_cloud_table_count = sessions.query(AlertCloudPurchase).filter(AlertCloudPurchase.user_id == userid).count()

            # cursor.execute(f"select count(*) from alert_cloud_purchase where user_id = {userid} ")
            # alert_cloud_table_count = cursor.fetchone()[0]

            alert_user_annual_count = sessions.query(UserPurchaseList).filter(UserPurchaseList.user_id == userid, UserPurchaseList.billing_frequency=="A").count()

            # cursor.execute(f"select count(*) from user_purchase_list where user_id = {userid} and billing_frequency='A' ")
            # alert_user_annual_count = cursor.fetchone()[0]

            if alert_user_annual_count != 0:  # check if user in package list is annual in users_list
                alert_user_table_count = sessions.query(AlertUserPurchase).filter(AlertUserPurchase.user_id == userid).count()
                # cursor.execute(f"select count(*) from alert_user_purchase where user_id = {userid}")
                # alert_user_table_count = cursor.fetchone()[0]

            if payment_status is True:
                if alert_pkg_table_count == 0:
                    updated_pur = sessions.query(PackagePurchaseList).filter(PackagePurchaseList.user_id == userid).update({ PackagePurchaseList.payment_date:current_date, PackagePurchaseList.renewal_date:pkg_renewal_datetime  })

                    # cursor.execute(f"update package_purchase_list set payment_date='{current_date}',renewal_date='{pkg_renewal_datetime}' where user_id={userid} ")

                    # cursor.execute(f"INSERT INTO package_purchase_history(pkg_pur_id, user_id,pkg_id,product_id,amount,currency_type,currency_symbol,latest_entry,payment_date,actual_amount,discount,renewal_date) SELECT pkg_pur_id,user_id,pkg_id,product_id,amount,currency_type,currency_symbol,latest_entry,payment_date,actual_amount,discount,renewal_date FROM package_purchase_list where user_id={userid};")
                    # connection.commit()

                else:  # in alert table
                    update_pkg_purchase = sessions.query(AlertPackagePurchase).with_entities(AlertPackagePurchase.pkg_pur_id, AlertPackagePurchase.user_id , AlertPackagePurchase.pkg_id , AlertPackagePurchase.product_id , AlertPackagePurchase.amount , AlertPackagePurchase.currency_type, AlertPackagePurchase.currency_symbol , AlertPackagePurchase.latest_entry , AlertPackagePurchase.payment_date ,AlertPackagePurchase.actual_amount, AlertPackagePurchase.discount, AlertPackagePurchase.renewal_date).filter(AlertPackagePurchase.user_id==userid).all()

                    for update_pkg_pur in update_pkg_purchase:
                        sessions.query(PackagePurchaseList).filter(PackagePurchaseList.user_id==userid, update_pkg_pur[1]==userid).update({PackagePurchaseList.user_id: update_pkg_pur[1], PackagePurchaseList.pkg_id: update_pkg_pur[2], PackagePurchaseList.product_id: update_pkg_pur[3], PackagePurchaseList.amount: update_pkg_pur[4],PackagePurchaseList.currency_type: update_pkg_pur[5], PackagePurchaseList.currency_symbol: update_pkg_pur[6],PackagePurchaseList.latest_entry: update_pkg_pur[7], PackagePurchaseList.payment_date: current_date, PackagePurchaseList.actual_amount: update_pkg_pur[9], PackagePurchaseList.discount: update_pkg_pur[10],PackagePurchaseList.renewal_date: pkg_renewal_datetime })
                    
                    sessions.query(AlertPackagePurchase).filter_by(user_id=userid).delete()
                    
                    # cursor.execute(f"Update package_purchase_list a set user_id=b.user_id,pkg_id=b.pkg_id,product_id=b.product_id,amount=b.amount,currency_type=b.currency_type,currency_symbol=b.currency_symbol,latest_entry=b.latest_entry,payment_date='{current_date}',actual_amount=b.actual_amount,discount=b.discount,renewal_date='{pkg_renewal_datetime}' from alert_package_purchase b where b.user_id={userid} and b.user_id=a.user_id ")

                    # cursor.execute(f"INSERT INTO package_purchase_history(pkg_pur_id, user_id,pkg_id,product_id,amount,currency_type,currency_symbol,latest_entry,payment_date,actual_amount,discount,renewal_date) SELECT pkg_pur_id,user_id,pkg_id,product_id,amount,currency_type,currency_symbol,latest_entry,payment_date,actual_amount,discount,renewal_date FROM package_purchase_list where user_id={userid} ;")

                    # cursor.execute(f"delete from alert_package_purchase where user_id={userid} ")

                select_pkg_purchase = sessions.query(PackagePurchaseList).with_entities(PackagePurchaseList.pkg_pur_id, PackagePurchaseList.user_id , PackagePurchaseList.pkg_id , PackagePurchaseList.product_id , PackagePurchaseList.amount , PackagePurchaseList.currency_type, PackagePurchaseList.currency_symbol , PackagePurchaseList.latest_entry , PackagePurchaseList.payment_date , PackagePurchaseList.actual_amount , PackagePurchaseList.discount , PackagePurchaseList.renewal_date) .filter(PackagePurchaseList.user_id==userid).all()

                for select_pkg_pur in select_pkg_purchase:
                    sessions.add(PackagePurchaseHistory(pkg_pur_id=select_pkg_pur[0], user_id=select_pkg_pur[1], pkg_id=select_pkg_pur[2], product_id=select_pkg_pur[3], amount=select_pkg_pur[4],currency_type=select_pkg_pur[5], currency_symbol=select_pkg_pur[6],latest_entry=select_pkg_pur[7], payment_date=select_usrselect_pkg_pur_pur[8], actual_amount=select_pkg_pur[9] ,discount=select_pkg_pur[10] ,renewal_date=select_pkg_pur[11]))
                    sessions.flush()

                if alert_user_annual_count != 0:
                    if alert_user_table_count == 0:
                        updated_user = sessions.query(UserPurchaseList).filter(UserPurchaseList.user_id == userid).update({ UserPurchaseList.payment_date:current_date, UserPurchaseList.renewal_date:pkg_renewal_datetime  })

                        # cursor.execute(f"update user_purchase_list set payment_date='{current_date}',renewal_date='{pkg_renewal_datetime}' where user_id={userid} ")

                        # cursor.execute(f"INSERT INTO user_purchase_history(user_pur_id, user_id,user_type_id,no_of_users,amount,currency_type,currency_symbol,latest_entry,payment_date,renewal_date,billing_frequency) SELECT user_pur_id,user_id,user_type_id,no_of_users,amount,currency_type,currency_symbol,latest_entry,payment_date,renewal_date,billing_frequency FROM user_purchase_list where user_id={userid};")
                        # connection.commit()

                    else:  # in alert table

                        update_usr_purchase = sessions.query(AlertUserPurchase).with_entities(AlertUserPurchase.user_pur_id, AlertUserPurchase.user_id , AlertUserPurchase.user_type_id , AlertUserPurchase.no_of_users , AlertUserPurchase.amount , AlertUserPurchase.currency_type, AlertUserPurchase.currency_symbol , AlertUserPurchase.latest_entry , AlertUserPurchase.payment_date , AlertUserPurchase.renewal_date , AlertUserPurchase.billing_frequency).filter(AlertUserPurchase.user_id==userid).all()

                        for update_usr_pur in update_usr_purchase:
                            sessions.query(UserPurchaseList).filter(UserPurchaseList.user_id==userid, update_usr_pur[1]==userid, UserPurchaseList.user_type_id == update_usr_pur[2]).update({UserPurchaseList.user_id: update_usr_pur[1], UserPurchaseList.user_type_id: update_usr_pur[2], UserPurchaseList.no_of_users: update_usr_pur[3], UserPurchaseList.amount: update_usr_pur[4],UserPurchaseList.currency_type: update_usr_pur[5], UserPurchaseList.currency_symbol: update_usr_pur[6],UserPurchaseList.latest_entry: update_usr_pur[7], UserPurchaseList.payment_date: current_date,UserPurchaseList.renewal_date: pkg_renewal_datetime, UserPurchaseList.billing_frequency: update_usr_pur[10] })

                        sessions.query(AlertUserPurchase).filter_by(user_id=userid).delete()

                        # cursor.execute(f"Update user_purchase_list a set user_id=b.user_id,user_type_id=b.user_type_id,no_of_users=b.no_of_users ,amount=b.amount,currency_type=b.currency_type,currency_symbol=b.currency_symbol,latest_entry=b.latest_entry,payment_date='{current_date}',renewal_date='{pkg_renewal_datetime}',billing_frequency=b.billing_frequency from alert_user_purchase b where b.user_id={userid} and a.user_id={userid} and a.user_type_id=b.user_type_id")

                        # cursor.execute(f"INSERT INTO user_purchase_history(user_pur_id, user_id,user_type_id,no_of_users,amount,currency_type,currency_symbol,latest_entry,payment_date,renewal_date,billing_frequency) SELECT user_pur_id,user_id,user_type_id,no_of_users,amount,currency_type,currency_symbol,latest_entry,payment_date,renewal_date,billing_frequency FROM user_purchase_list where user_id={userid};")

                        # cursor.execute(f"delete from alert_user_purchase where user_id={userid} ")

                    select_usr_purchase = sessions.query(UserPurchaseList).with_entities(UserPurchaseList.user_pur_id, UserPurchaseList.user_id , UserPurchaseList.user_type_id , UserPurchaseList.no_of_users , UserPurchaseList.amount , UserPurchaseList.currency_type, UserPurchaseList.currency_symbol , UserPurchaseList.latest_entry , UserPurchaseList.payment_date , UserPurchaseList.renewal_date , UserPurchaseList.billing_frequency).filter(UserPurchaseList.user_id==userid).all()

                    for select_usr_pur in select_usr_purchase:
                        sessions.add(UserPurchaseHistory(user_pur_id=select_usr_pur[0], user_id=select_usr_pur[1], user_type_id=select_usr_pur[2], no_of_users=select_usr_pur[3], amount=select_usr_pur[4],currency_type=select_usr_pur[5], currency_symbol=select_usr_pur[6],latest_entry=select_usr_pur[7], payment_date=select_usr_pur[8],renewal_date=select_usr_pur[9], billing_frequency=select_usr_pur[10] ))
                        sessions.flush()

                if alert_cloud_table_count == 0:
                    updated_cloud = sessions.query(CloudPurchaseList).filter(CloudPurchaseList.user_id == userid).update({ CloudPurchaseList.payment_date:current_date, CloudPurchaseList.renewal_date:pkg_renewal_datetime  })

                    # cursor.execute(f"update cloud_purchase_list set payment_date='{current_date}',renewal_date='{pkg_renewal_datetime}' where user_id={userid} ")

                    # cursor.execute(f"INSERT INTO cloud_purchase_history(cloud_pur_id, user_id,cloud_type_id,amount,currency_type,currency_symbol,latest_entry,payment_date,renewal_date) SELECT cloud_pur_id,user_id,cloud_type_id,amount,currency_type,currency_symbol,latest_entry,payment_date,renewal_date FROM cloud_purchase_list where user_id={userid};")
                    # connection.commit()

                else:  # in alert table
                    update_cloud_purchase = sessions.query(AlertCloudPurchase).with_entities(AlertCloudPurchase.cloud_pur_id, AlertCloudPurchase.user_id , AlertCloudPurchase.cloud_type_id, AlertCloudPurchase.amount , AlertCloudPurchase.currency_type, AlertCloudPurchase.currency_symbol , AlertCloudPurchase.latest_entry , AlertCloudPurchase.payment_date , AlertCloudPurchase.renewal_date).filter(AlertCloudPurchase.user_id==userid).all()

                    for update_cloud_pur in update_cloud_purchase:
                        sessions.query(CloudPurchaseList).filter(CloudPurchaseList.user_id==userid, update_cloud_pur[1]==userid).update({CloudPurchaseList.user_id: update_cloud_pur[1], CloudPurchaseList.cloud_type_id: update_cloud_pur[2], CloudPurchaseList.amount: update_cloud_pur[3],CloudPurchaseList.currency_type: update_cloud_pur[4], CloudPurchaseList.currency_symbol: update_cloud_pur[5],CloudPurchaseList.latest_entry: update_cloud_pur[6], CloudPurchaseList.payment_date: current_date, CloudPurchaseList.renewal_date: pkg_renewal_datetime })

                    sessions.query(AlertCloudPurchase).filter_by(user_id=userid).delete()

                select_cloud_purchase = sessions.query(CloudPurchaseList).with_entities(CloudPurchaseList.cloud_pur_id, CloudPurchaseList.user_id , CloudPurchaseList.cloud_type_id , CloudPurchaseList.amount , CloudPurchaseList.currency_type, CloudPurchaseList.currency_symbol , CloudPurchaseList.latest_entry , CloudPurchaseList.payment_date , CloudPurchaseList.renewal_date).filter(CloudPurchaseList.user_id==userid).all()

                for select_cld_pur in select_cloud_purchase:
                    sessions.add(CloudPurchaseHistory(cloud_pur_id=select_cld_pur[0], user_id=select_cld_pur[1], cloud_type_id=select_cld_pur[2],  amount=select_cld_pur[3],currency_type=select_cld_pur[4], currency_symbol=select_cld_pur[5],latest_entry=select_cld_pur[6], payment_date=select_cld_pur[7],renewal_date=select_cld_pur[8] ))
                    sessions.flush()


                    # cursor.execute(f"Update cloud_purchase_list a set user_id=b.user_id,cloud_type_id=b.cloud_type_id,amount=b.amount,currency_type=b.currency_type,currency_symbol=b.currency_symbol,latest_entry=b.latest_entry,payment_date='{current_date}',renewal_date='{pkg_renewal_datetime}' from alert_cloud_purchase b where b.user_id={userid} and b.user_id=a.user_id ")

                    # cursor.execute(f"INSERT INTO cloud_purchase_history(cloud_pur_id, user_id,cloud_type_id,amount,currency_type,currency_symbol,latest_entry,payment_date,renewal_date) SELECT cloud_pur_id,user_id,cloud_type_id,amount,currency_type,currency_symbol,latest_entry,payment_date,renewal_date FROM cloud_purchase_list where user_id={userid} ;")
                    # cursor.execute(f"delete from alert_cloud_purchase where user_id={userid} ")

                # cursor.execute(f"Insert into payment_history(payment_date,mode_of_payment,amount,transaction_details,user_id,status) values {(str(current_date),'credit_card',payment_amount_annual,'1246566',userid,1)} ")

                # card_no_val = '09764'
                # card_no = encryptdata(card_no_val)
                # cvv_no_val = '998'
                # cvv_no = encryptdata(cvv_no_val)
                # expiry_date_val = '04/20'
                # expiry_date = encryptdata(expiry_date_val)

                # cursor.execute(f"Insert into payment_mode(mode_of_payment,card_number,account_holder_name,cvv,expiry_date,user_id) values {('credit_card',card_no,'scopiq',cvv_no,expiry_date,userid)} ")
                # connection.commit()
                inserted_pay_his = PaymentHistory(payment_date=current_date, mode_of_payment='credit_card', amount=payment_amount_annual, transaction_details='1246566', user_id=userid, status=1)
                sessions.add(inserted_pay_his)
                sessions.flush()

                card_no_val = '09764'
                card_no = encryptdata(card_no_val)
                cvv_no_val = '998'
                cvv_no = encryptdata(cvv_no_val)
                expiry_date_val = '04/20'
                expiry_date = encryptdata(expiry_date_val)

                inserted_pay_his = PaymentMode(mode_of_payment='credit_card', card_number=card_no, account_holder_name='scopiq', cvv=cvv_no, expiry_date=expiry_date, user_id=userid)
                sessions.add(inserted_pay_his)
                sessions.flush()

                sessions.commit()
                msg = Message('Payment Information', sender='sneha.r@perpetua.co.in', recipients=[user_email])
                message = "Your payment was Successful"
                msg.body = message
                msg.html = render_template('emails/alert_mail_remainder.html', expiry_details=message)
                mail.send(msg)

            else:
                flash('Your Payment was failed')
        return redirect('/auto_renewal')

    return render_template('auto_renewal.html', count_values=count_values, userid=userid,failed_payment_details=failed_payment_details,pkg_amount=pkg_amount,cloud_amount=cloud_amount,user_amount=user_amount,exist_user_billing_freq=exist_user_billing_freq)



@app.route('/get_admin_slab', methods=['GET', 'POST'])
def get_admin_slab():
    
    currency_type = session['currency']
    currency = currency_type.lower()
    current_date = datetime.date(datetime.now())

    
    admin_effective_date = sessions.query(UserPricing.effective_date).filter_by(user_type_id=1).first()[0]

    if admin_effective_date <= current_date:
        admin_amount = sessions.query(UserPricing.inr).filter_by(user_type_id=1).first()[0]

        # cursor.execute(f"select lower as lower_value,upper as higher_value,{currency} as amount,user_pricing_id from user_pricing where user_type_id=1")
        # columns = [col[0] for col in cursor.description]
        # admin_user = [dict(zip(columns, row)) for row in cursor.fetchall()]

    else:
        admin_cnt = sessions.query(UserPricing).filter_by(user_type_id = 1).count()
        
        admin_user = sessions.query(UserPricingHistory).with_entities(UserPricingHistory.lower.label('lower_value'),UserPricingHistory.upper.label('higher_value'),getattr(UserPricingHistory,currency).label('amount'),UserPricingHistory.user_pricing_id.label('user_pricing_id')).filter_by(user_type_id=1).filter(UserPricingHistory.effective_date<=current_date).order_by(UserPricingHistory.user_pricing_his_id.desc()).limit(admin_cnt)


    admin_amount = admin_amount
    return admin_amount


@app.route('/get_general_slab', methods=['GET', 'POST'])
def get_general_slab():
    
    currency_type = session['currency']
    currency = currency_type.lower()
    current_date = datetime.date(datetime.now())

    
    admin_effective_date = sessions.query(UserPricing.effective_date).filter_by(user_type_id=1).first()[0]

    if admin_effective_date <= current_date:
        general_amount = sessions.query(UserPricing.inr).filter_by(user_type_id=2).first()[0]

        # cursor.execute(f"select lower as lower_value,upper as higher_value,{currency} as amount,user_pricing_id from user_pricing where user_type_id=1")
        # columns = [col[0] for col in cursor.description]
        # admin_user = [dict(zip(columns, row)) for row in cursor.fetchall()]

    else:
        admin_cnt = sessions.query(UserPricing).filter_by(user_type_id = 1).count()
        
        admin_user = sessions.query(UserPricingHistory).with_entities(UserPricingHistory.lower.label('lower_value'),UserPricingHistory.upper.label('higher_value'),getattr(UserPricingHistory,currency).label('amount'),UserPricingHistory.user_pricing_id.label('user_pricing_id')).filter_by(user_type_id=1).filter(UserPricingHistory.effective_date<=current_date).order_by(UserPricingHistory.user_pricing_his_id.desc()).limit(admin_cnt)


    general_amount = general_amount
    return general_amount



@app.route('/get_limited_slab', methods=['GET', 'POST'])
def get_limited_slab():
    
    currency_type = session['currency']
    currency = currency_type.lower()
    current_date = datetime.date(datetime.now())

    
    admin_effective_date = sessions.query(UserPricing.effective_date).filter_by(user_type_id=1).first()[0]

    if admin_effective_date <= current_date:
        limited_amount = sessions.query(UserPricing.inr).filter_by(user_type_id=3).first()[0]

        # cursor.execute(f"select lower as lower_value,upper as higher_value,{currency} as amount,user_pricing_id from user_pricing where user_type_id=1")
        # columns = [col[0] for col in cursor.description]
        # admin_user = [dict(zip(columns, row)) for row in cursor.fetchall()]

    else:
        admin_cnt = sessions.query(UserPricing).filter_by(user_type_id = 1).count()
        
        admin_user = sessions.query(UserPricingHistory).with_entities(UserPricingHistory.lower.label('lower_value'),UserPricingHistory.upper.label('higher_value'),getattr(UserPricingHistory,currency).label('amount'),UserPricingHistory.user_pricing_id.label('user_pricing_id')).filter_by(user_type_id=1).filter(UserPricingHistory.effective_date<=current_date).order_by(UserPricingHistory.user_pricing_his_id.desc()).limit(admin_cnt)


    limited_amount = limited_amount
    return limited_amount


@app.route('/get_bill_no', methods=['GET', 'POST'])
def get_bill_no():
    invoice_details=[]
    # check atleast one entry exists in PaymentHistory Table
    check_billing_count = sessions.query(PaymentHistory).count()
    print(check_billing_count,'check_billing_count')
    # First billing happening
    if check_billing_count == 0:
        new_bill_no = str(1)
        new_bill_no_val = new_bill_no.zfill(5)
        bill_num_val = str(bill_code)+str(new_bill_no_val)+"/"+str(financial_year)+"-"+str(nxt_fin_year)

        new_pur_no = str(1)
        new_pur_no_val = new_pur_no.zfill(5)
        pur_num_val = str(purchase_code)+str(new_pur_no_val)+"/"+str(financial_year)+"-"+str(nxt_fin_year)
    else:
        # fetch last bill series no and add 1 to it, generate bill no
        get_last_bill_no = sessions.query(PaymentHistory.bill_no).filter(PaymentHistory.amount != '0.0').order_by(PaymentHistory.payment_history_id.desc()).limit(1).first()[0] 
        print(get_last_bill_no,'get_last_bill_no')
        new_bill_no = int(get_last_bill_no)+1
        new_bill_no_val = str(new_bill_no).zfill(5)
        bill_num_val = str(bill_code)+str(new_bill_no_val)+"/"+str(financial_year)+"-"+str(nxt_fin_year)

        get_last_pur_no = sessions.query(PaymentHistory.purchase_no).order_by(PaymentHistory.payment_history_id.desc()).limit(1).first()[0]
        print(get_last_pur_no,'get_last_pur_no')
        new_pur_no = int(get_last_pur_no)+1
        new_pur_no_val = str(new_pur_no).zfill(5)
        pur_num_val = str(purchase_code)+str(new_pur_no_val)+"/"+str(financial_year)+"-"+str(nxt_fin_year)

        print(bill_num_val,'bill_num_val')
        print(pur_num_val,'pur_num_val')


    invoice_details.append({'bill_no':new_bill_no, 'pur_no':new_pur_no, 'bill_num_val':bill_num_val, 'pur_num_val':pur_num_val})

    print(invoice_details,'invoice_details')
    return invoice_details




if __name__ == '__main__':
    # app.jinja_env.auto_reload = True
    # app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SESSION_COOKIE_NAME'] = "azurewebsitesession"
    app.run(host=host, port=port,debug=True)
