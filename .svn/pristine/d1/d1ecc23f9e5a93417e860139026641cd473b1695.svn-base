from flask import Flask, request, render_template, flash, redirect, url_for, session, abort

from datetime import datetime
from crontab import CronTab

from flask_mail import *

from db_configuration import app, se, mail, host, port
import db_configuration

from dateutil import relativedelta
from dateutil.relativedelta import relativedelta


import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Protocol.KDF import PBKDF2

import urllib
import urllib.parse


app = Flask(__name__)

connection = db_configuration.connection()
cursor = connection.cursor()

# Flask mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'sneha.r@perpetua.co.in'
app.config['MAIL_PASSWORD'] = 'snehasneha'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['SECRET_KEY'] = "random string"
# #instantiate the Mail class
mail = Mail(app)

BLOCK_SIZE = 16
bs = 16
# pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]
passcr="thisisdemo"
def _pad(s):
      return s + (bs - len(s) % bs) * chr(bs - len(s) % bs)


def get_private_key(passcr):
    salt = b"this is a salt"
    kdf = PBKDF2(passcr, salt, 64, 1000)
    key = kdf[:32]
    return key

@app.template_filter('encryptdata')
def encryptdata(raw):
    private_key = get_private_key(passcr)
    raw = _pad(str(raw))
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(raw))



def decrypt(enc, passcr):
    private_key = get_private_key(passcr)
   #  enc = base64.b32decode(enc)
    enc = base64.b64decode(enc + '=' * (-len(enc) % 4))
    iv = enc[:16]
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc[16:]))


def index():
   cursor.execute(f"select a.expiry_date,a.user_id,b.email from payment_mode a left join users b on a.user_id = b.user_id ")
   payment_mode_details = cursor.fetchall()

   for payment_mode_det in payment_mode_details:
      email = payment_mode_det[2]
      expiry_date = payment_mode_det[0]

      expiry_date_decrypt = decrypt(expiry_date, passcr)

      decrypted_expiry_date=str(expiry_date_decrypt).replace("'",'').replace('b','')

      expdate = "01/" + str(decrypted_expiry_date)

      exp = str(expdate).replace('/', '-')

      expiry_date_format = datetime.strptime(exp, '%d-%m-%y').date()

      expiry_format = expiry_date_format + relativedelta(months=-1)

      current_date = datetime.date(datetime.now())

      if current_date == expiry_format:

         with app.app_context():
            msg = Message('Expire', sender='username@gmail.com', recipients=[email])
            expiry_details = "Your Card will expire in " + str(payment_mode_det[0])
            msg.body = expiry_details
            mail.send(msg)

index()

if __name__ == '__main__':
   app.run(debug=True)
