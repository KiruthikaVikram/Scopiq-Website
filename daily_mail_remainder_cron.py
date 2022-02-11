from flask import Flask, request, render_template, flash, redirect, url_for, session, abort

from datetime import datetime

from flask_mail import *

from db_configuration import app, se, mail, host, port
import db_configuration

from dateutil import relativedelta
from dateutil.relativedelta import relativedelta

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


def index():
   cursor.execute(f"select alert_start_days,renewal_alert_days from alert_interval_list where renewal_type='A' ")
   alert_interval_annual_list = cursor.fetchone()

   alert_start_days_annual = alert_interval_annual_list[0]
   alert_interval_annual = - + alert_interval_annual_list[1] # for decrementing values

   cursor.execute(f"select * from package_purchase_list")
   columns = [col[0] for col in cursor.description]
   package_details = [dict(zip(columns, row)) for row in cursor.fetchall()]

   for pkg_det in package_details:
      pkg_renewal_date = pkg_det['renewal_date']
      cond1 = "1!=1"

      for alerts in range (alert_start_days_annual, 0, alert_interval_annual): # range(start,stop,step)
         alert_period = alerts
         current_date = datetime.date(datetime.now())
         payment_date = current_date + relativedelta(days=alert_period)
         cond1 = str(cond1) + " OR " + str(payment_date) + "=" + str(pkg_renewal_date)

   cursor.execute(f"select alert_start_days,renewal_alert_days from alert_interval_list where renewal_type='M' ")
   alert_interval_monthly_list = cursor.fetchone()

   alert_start_days_monthly = alert_interval_monthly_list[0]
   alert_interval_monthly = - + alert_interval_monthly_list[1] # for decrementing values

   cursor.execute(f"select Distinct user_id,renewal_date from user_purchase_list where billing_frequency = 'M' ")
   columns = [col[0] for col in cursor.description]
   user_pkg_details = [dict(zip(columns, row)) for row in cursor.fetchall()]

   for user_det in user_pkg_details:
      user_renewal_date = user_det['renewal_date']
      cond2 = "1!=1"

      for alerts in range (alert_start_days_monthly, 0, alert_interval_monthly): # range(start,stop,step)
         alert_period = alerts
         current_date = datetime.date(datetime.now())
         payment_date = current_date + relativedelta(days=alert_period)
         cond2 = str(cond2) + " OR " + str(payment_date) + "=" + str(user_renewal_date)

   print(f"select a.user_id,b.email,a.renewal_date from package_purchase_list a left join users b on a.user_id = b.user_id where {cond1} UNION select c.user_id,d.email,c.renewal_date from user_purchase_list c left join users d on c.user_id = d.user_id where {cond2} and  c.billing_frequency = 'M'")

   cursor.execute(f"select a.user_id,b.email,a.renewal_date from package_purchase_list a left join users b on a.user_id = b.user_id where {cond1} UNION select c.user_id,d.email,c.renewal_date from user_purchase_list c left join users d on c.user_id = d.user_id where {cond2} and  c.billing_frequency = 'M'")
   user_details = cursor.fetchall()

   for user_det in user_details:

      user_email = user_det[1]
      renewal_date = (user_det[2].strftime('%d-%m-%Y'))
      with app.app_context():
         msg = Message('Expire', sender='username@gmail.com', recipients=[user_email])
         expiry_details = "Your Pack will expire on " + str(renewal_date)
         msg.body = expiry_details

         msg.html = render_template('emails/alert_mail_remainder.html', expiry_details = expiry_details)
         mail.send(msg)

index()

if __name__ == '__main__':
   app.run(debug=True)
