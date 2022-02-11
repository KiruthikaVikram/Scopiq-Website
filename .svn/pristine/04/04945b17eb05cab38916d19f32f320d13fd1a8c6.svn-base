from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Systemrole(db.Model):
    roleid = db.Column(db.Integer, primary_key=True)
    rolename = db.Column(db.String(50),nullable=False)

class RegUsers(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String, nullable=False)
    verification_code = db.Column(db.String(10), nullable=False)
    status = db.Column(db.Integer, nullable=False)
    referred_by = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_type = db.Column(db.String, nullable=False)


class CompanyDetails(db.Model):
    company_id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    company_code = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(255), nullable=False)
    site_name = db.Column(db.String, nullable=False)
    country_id = db.Column(db.Integer, nullable=False)
    state_id = db.Column(db.Integer, nullable=False)
    city_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())
    dynamic_table_name = db.Column(db.String, nullable=False)


class CompanyDetailsHistory(db.Model):
    company_his_id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    company_code = db.Column(db.String(100))
    address = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(255), nullable=False)
    site_name = db.Column(db.String, nullable=False)
    country_id = db.Column(db.Integer, nullable=False)
    state_id = db.Column(db.Integer, nullable=False)
    city_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())
    dynamic_table_name = db.Column(db.String, nullable=False)


class Location(db.Model):
    location_id = db.Column(db.Integer, primary_key=True)
    location_name = db.Column(db.String, nullable=False)
    company_id = db.Column(db.Integer, nullable=False)
    address = db.Column(db.Text, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())


class ProductList(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())


class BillingDetails(db.Model):
    bill_id = db.Column(db.Integer, primary_key=True)
    bill_no = db.Column(db.Integer, nullable=True)
    user_id = db.Column(db.Integer, nullable=False)
    invoice_company_name = db.Column(db.String, nullable=False)
    invoice_billing_address = db.Column(db.String, nullable=False)
    gst_no = db.Column(db.String, nullable=False)
    country_id = db.Column(db.Integer, nullable=False)
    state_id = db.Column(db.Integer, nullable=False)
    city_id = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())


class Referral(db.Model):
    referral_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())


class SuperadminLogin(db.Model):
    superadmin_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password_hash = db.Column(db.String, nullable=False)


class UserType(db.Model):
    user_type_id = db.Column(db.Integer, primary_key=True)
    user_type_name = db.Column(db.String(50), nullable=False)
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())


class UserPricing(db.Model):
    user_pricing_id = db.Column(db.Integer, primary_key=True)
    user_type_id = db.Column(db.Integer, nullable=False)
    lower = db.Column(db.String, nullable=False)
    upper = db.Column(db.String, nullable=False)
    inr = db.Column(db.String, nullable=False)
    usd = db.Column(db.String, nullable=False)
    eur = db.Column(db.String, nullable=False)
    gbp = db.Column(db.String, nullable=False)
    effective_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())


class Gst(db.Model):
    gst_id = db.Column(db.Integer, primary_key=True)
    country_id = db.Column(db.Integer, nullable=False)
    gst_per = db.Column(db.String, nullable=False)
    effective_from_date = db.Column(db.Date, nullable=False)
    effective_to_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())


class Country(db.Model):
    country_id = db.Column(db.Integer, primary_key=True)
    country_name = db.Column(db.String(50), nullable=False)
    country_code = db.Column(db.String(50), nullable=False)
    phone_code = db.Column(db.Integer, nullable=False)
    currency = db.Column(db.String(50), nullable=False)
    currency_symbol = db.Column(db.String(50), nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())


class State(db.Model):
    state_id = db.Column(db.Integer, primary_key=True)
    state_name = db.Column(db.String(50), nullable=False)
    state_code = db.Column(db.String(15), nullable=False)
    country_id = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())


class City(db.Model):
    city_id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(50), nullable=False)
    state_id = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())


class PackageList(db.Model):
    pkg_id = db.Column(db.Integer, primary_key=True)
    pkg_name = db.Column(db.String, nullable=False)
    product_id = db.Column(db.String, nullable=False)
    inr = db.Column(db.Integer, nullable=False)
    usd = db.Column(db.Integer, nullable=False)
    eur = db.Column(db.Integer, nullable=False)
    gbp = db.Column(db.Integer, nullable=False)
    effective_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())


class ProductSelectionList(db.Model):
    selc_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    pkg_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.String, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    actual_amount = db.Column(db.Integer, nullable=False)
    discount = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())


class UserSelectionList(db.Model):
    user_selc_id = db.Column(db.Integer, primary_key=True)
    admin_user_count = db.Column(db.Integer, nullable=False)
    admin_user_amount = db.Column(db.String, nullable=False)
    general_user_count = db.Column(db.Integer, nullable=False)
    general_user_amount = db.Column(db.String, nullable=False)
    limited_user_count = db.Column(db.Integer, nullable=False)
    limited_user_amount = db.Column(db.String, nullable=False)
    amount = db.Column(db.String, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())
    billing_frequency = db.Column(db.String, nullable=False)
    actual_amount = db.Column(db.String, nullable=False)
    discount = db.Column(db.String, nullable=False)


class CloudType(db.Model):
    cl_type_id = db.Column(db.Integer, primary_key=True)
    cl_type_name = db.Column(db.String(50), nullable=False)
    cloud_type = db.Column(db.String, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())


class CloudPricing(db.Model):
    cloud_pricing_id = db.Column(db.Integer, primary_key=True)
    cl_type_id = db.Column(db.Integer, nullable=False)
    features = db.Column(db.Text, nullable=False)
    inr = db.Column(db.String, nullable=False)
    usd = db.Column(db.String, nullable=False)
    eur = db.Column(db.String, nullable=False)
    gbp = db.Column(db.String, nullable=False)
    effective_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())


class CloudSelection(db.Model):
    cloud_id = db.Column(db.Integer, primary_key=True)
    cl_type_id = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())


class AlertIntervalList(db.Model):
    renewal_alert_id = db.Column(db.Integer, primary_key=True)
    renewal_type = db.Column(db.String, nullable=False)
    alert_start_days = db.Column(db.Integer, nullable=False)
    renewal_alert_days = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())


class PackagePurchaseList(db.Model):
    pkg_pur_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    pkg_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.String, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    currency_type = db.Column(db.String, nullable=False)
    currency_symbol = db.Column(db.String, nullable=False)
    latest_entry = db.Column(db.Integer, nullable=True)
    payment_date = db.Column(db.Date, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())
    actual_amount = db.Column(db.Integer, nullable=False)
    discount = db.Column(db.Integer, nullable=False)
    renewal_date = db.Column(db.Date, nullable=False)
    product_amount = db.Column(db.Integer, nullable=False)


class AlertPackagePurchase(db.Model):
    pkg_pur_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    pkg_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.String, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    currency_type = db.Column(db.String, nullable=False)
    currency_symbol = db.Column(db.String, nullable=False)
    latest_entry = db.Column(db.Integer, nullable=True)
    payment_date = db.Column(db.Date, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())
    actual_amount = db.Column(db.Integer, nullable=False)
    discount = db.Column(db.Integer, nullable=False)
    renewal_date = db.Column(db.Date, nullable=False)


class UserPurchaseList(db.Model):
    user_pur_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    user_type_id = db.Column(db.Integer, nullable=False)
    no_of_users = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.String, nullable=False)
    currency_type = db.Column(db.String, nullable=False)
    currency_symbol = db.Column(db.String, nullable=False)
    latest_entry = db.Column(db.Integer, nullable=True)
    payment_date = db.Column(db.Date, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())
    billing_frequency = db.Column(db.String(10), nullable=False)
    renewal_date = db.Column(db.Date, nullable=False)
    actual_no_of_users = db.Column(db.Integer, nullable=False)
    actual_amount = db.Column(db.String, nullable=False)


class AlertUserPurchase(db.Model):
    user_pur_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    user_type_id = db.Column(db.Integer, nullable=False)
    no_of_users = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.String, nullable=False)
    currency_type = db.Column(db.String, nullable=False)
    currency_symbol = db.Column(db.String, nullable=False)
    latest_entry = db.Column(db.Integer, nullable=True)
    payment_date = db.Column(db.Date, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())
    billing_frequency = db.Column(db.String(10), nullable=False)
    renewal_date = db.Column(db.Date, nullable=False)


class CloudPurchaseList(db.Model):
    cloud_pur_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    cloud_type_id = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    currency_type = db.Column(db.String, nullable=False)
    currency_symbol = db.Column(db.String, nullable=False)
    latest_entry = db.Column(db.Integer, nullable=True)
    payment_date = db.Column(db.Date, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())
    renewal_date = db.Column(db.Date, nullable=False)
    actual_amount = db.Column(db.Integer, nullable=False)


class AlertCloudPurchase(db.Model):
    cloud_pur_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    cloud_type_id = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    currency_type = db.Column(db.String, nullable=False)
    currency_symbol = db.Column(db.String, nullable=False)
    latest_entry = db.Column(db.Integer, nullable=True)
    payment_date = db.Column(db.Date, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())
    renewal_date = db.Column(db.Date, nullable=False)


class Settings(db.Model):
    setting_id = db.Column(db.Integer, primary_key=True)
    user_dis_price = db.Column(db.String, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())


class PackagePurchaseHistory(db.Model):
    pkg_history_id = db.Column(db.Integer, primary_key=True)
    pkg_pur_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    pkg_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.String, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    currency_type = db.Column(db.String, nullable=False)
    currency_symbol = db.Column(db.String, nullable=False)
    latest_entry = db.Column(db.Integer, nullable=True)
    payment_date = db.Column(db.Date, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())
    actual_amount = db.Column(db.Integer, nullable=False)
    discount = db.Column(db.Integer, nullable=False)
    renewal_date = db.Column(db.Date, nullable=False)
    product_amount = db.Column(db.Integer, nullable=False)


class UserPurchaseHistory(db.Model):
    user_history_id = db.Column(db.Integer, primary_key=True)
    user_pur_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    user_type_id = db.Column(db.Integer, nullable=False)
    no_of_users = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.String, nullable=False)
    currency_type = db.Column(db.String, nullable=False)
    currency_symbol = db.Column(db.String, nullable=False)
    latest_entry = db.Column(db.Integer, nullable=True)
    payment_date = db.Column(db.Date, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())
    billing_frequency = db.Column(db.String(10), nullable=False)
    renewal_date = db.Column(db.Date, nullable=False)
    actual_no_of_users = db.Column(db.Integer, nullable=False)
    actual_amount = db.Column(db.String, nullable=False)


class CloudPurchaseHistory(db.Model):
    cloud_history_id = db.Column(db.Integer, primary_key=True)
    cloud_pur_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    cloud_type_id = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    currency_type = db.Column(db.String, nullable=False)
    currency_symbol = db.Column(db.String, nullable=False)
    latest_entry = db.Column(db.Integer, nullable=True)
    payment_date = db.Column(db.Date, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())
    renewal_date = db.Column(db.Date, nullable=False)
    actual_amount = db.Column(db.Integer, nullable=False)


class PaymentHistory(db.Model):
    payment_history_id = db.Column(db.Integer, primary_key=True)
    bill_no = db.Column(db.Integer, nullable=True)
    purchase_no = db.Column(db.Integer, nullable=True)
    bill_series_no = db.Column(db.String(255), nullable=True)
    purchase_series_no = db.Column(db.String(255), nullable=True)
    payment_date = db.Column(db.Date, nullable=False)
    mode_of_payment = db.Column(db.String, nullable=False)
    amount = db.Column(db.String, nullable=False)
    transaction_details = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    pkg_pur_his_id = db.Column(db.Integer, nullable=False)
    user_pur_his_id = db.Column(db.String, nullable=False)
    cld_pur_his_id = db.Column(db.Integer, nullable=False)
    payment_type = db.Column(db.String(10), nullable=False)


class PaymentMode(db.Model):
    mode_id = db.Column(db.Integer, primary_key=True)
    mode_of_payment = db.Column(db.String, nullable=False)
    card_number = db.Column(db.String, nullable=False)
    account_holder_name = db.Column(db.String, nullable=False)
    cvv = db.Column(db.String, nullable=False)
    expiry_date = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)


class PackageListHistory(db.Model):
    pkg_his_id = db.Column(db.Integer, primary_key=True)
    pkg_id = db.Column(db.Integer, nullable=False)
    pkg_name = db.Column(db.String, nullable=False)
    product_id = db.Column(db.String, nullable=False)
    inr = db.Column(db.Integer, nullable=False)
    usd = db.Column(db.Integer, nullable=False)
    eur = db.Column(db.Integer, nullable=False)
    gbp = db.Column(db.Integer, nullable=False)
    effective_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())


class UserPricingHistory(db.Model):
    user_pricing_his_id = db.Column(db.Integer, primary_key=True)
    user_pricing_id = db.Column(db.Integer, nullable=False)
    user_type_id = db.Column(db.Integer, nullable=False)
    lower = db.Column(db.String, nullable=False)
    upper = db.Column(db.String, nullable=False)
    inr = db.Column(db.String, nullable=False)
    usd = db.Column(db.String, nullable=False)
    eur = db.Column(db.String, nullable=False)
    gbp = db.Column(db.String, nullable=False)
    effective_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())


class CloudPricingHistory(db.Model):
    cloud_pricing_his_id = db.Column(db.Integer, primary_key=True)
    cloud_pricing_id = db.Column(db.Integer, nullable=False)
    cl_type_id = db.Column(db.Integer, nullable=False)
    features = db.Column(db.Text, nullable=False)
    inr = db.Column(db.String, nullable=False)
    usd = db.Column(db.String, nullable=False)
    eur = db.Column(db.String, nullable=False)
    gbp = db.Column(db.String, nullable=False)
    effective_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())


class PaymentStatus(db.Model):
    status_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    mode_of_payment = db.Column(db.String, nullable=False)
    card_number = db.Column(db.String, nullable=False)
    account_holder_name = db.Column(db.String, nullable=False)
    amount = db.Column(db.String, nullable=False)
    from_date = db.Column(db.Date, nullable=False)
    to_date = db.Column(db.Date, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    payment_type = db.Column(db.String, nullable=False)
    
class PortList(db.Model):
    port_id = db.Column(db.Integer, primary_key=True)
    port_no = db.Column(db.Integer)
    company_id = db.Column(db.Integer)
    status = db.Column(db.Integer)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())


class GlobalProgramType(db.Model):
    gpt_id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(100))
    status = db.Column(db.Integer)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)


class GlobalProgramTypeApproval(db.Model):
    gpt_id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(100))
    program_name = db.Column(db.String(100))
    company_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)


class GlobalRecommandTable(db.Model):
    grt_id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(100))
    program_name = db.Column(db.String(100))
    template_id = db.Column(db.Integer)
    type_count = db.Column(db.BigInteger)
    company_id = db.Column(db.Integer)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)


class GlobalRecommandTableHistory(db.Model):
    grth_id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(100))
    template_id = db.Column(db.Integer)
    company_id = db.Column(db.Integer)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)

class GlobalTemplateLists(db.Model):
    global_temp_id = db.Column(db.Integer, primary_key=True)
    global_type_name = db.Column(db.String(100))
    global_template_name =  db.Column(db.String(100))
    global_pagewise_template = db.Column(db.Text)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)


class GlobalMultiTemplateDetails(db.Model):
    temp_id = db.Column(db.Integer, primary_key=True)
    temp_name = db.Column(db.String(255))
    pagewise_template =  db.Column(db.Text)
    program_type_id = db.Column(db.Integer)
    status = db.Column(db.Integer)
    temp_first_page = db.Column(db.Integer)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date =  db.Column(db.DateTime(timezone=True), default=func.now())

class GlobalMultiTemplateDetailsApproval(db.Model):
    temp_id = db.Column(db.Integer, primary_key=True)
    temp_name = db.Column(db.String(255))
    pagewise_template =  db.Column(db.Text)
    user_id = db.Column(db.Integer)
    status = db.Column(db.Integer)
    temp_first_page = db.Column(db.Integer)
    company_id = db.Column(db.Integer)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date =  db.Column(db.DateTime(timezone=True), default=func.now())

class TemplateDetails(db.Model):
    temp_det_id = db.Column(db.Integer, primary_key=True)
    temp_id = db.Column(db.Integer)
    temp_file_name = db.Column(db.String(255),nullable=False)
    temp_image_name = db.Column(db.String(255),nullable=False)
    temp_type = db.Column(db.String(10),nullable=False)
    temp_rev_check = db.Column(db.String(10), nullable=False)
    prepared_count = db.Column(db.Integer, nullable=False)
    reviewed_count = db.Column(db.Integer, nullable=False)
    approved_count = db.Column(db.Integer, nullable=False)
    released_count = db.Column(db.Integer, nullable=False)
    temp_source = db.Column(db.Text)


class GlobalTemplateDetails(db.Model):
    temp_id = db.Column(db.Integer, primary_key=True)
    temp_file_name = db.Column(db.String(255),nullable=False)
    temp_image_name = db.Column(db.String(255),nullable=False)
    temp_type = db.Column(db.String(10),nullable=False)
    temp_rev_check = db.Column(db.String(10), nullable=False)
    prepared_count = db.Column(db.Integer, nullable=False)
    reviewed_count = db.Column(db.Integer, nullable=False)
    approved_count = db.Column(db.Integer, nullable=False)
    released_count = db.Column(db.Integer, nullable=False)
    temp_source = db.Column(db.Text, nullable=False)
    page_name = db.Column(db.String(100))


class DsmAlertIntervalList(db.Model):
    dsm_renewal_alert_id = db.Column(db.Integer, primary_key=True)
    frequency = db.Column(db.String)
    alert = db.Column(db.String)
    notification = db.Column(db.String)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())


class HolidayList(db.Model):
    holiday_id = db.Column(db.Integer, primary_key=True)
    country_id = db.Column(db.Integer, nullable=False)
    holiday_dates = db.Column(db.String(255))
    status = db.Column(db.Integer)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())


class DbList(db.Model):
    pdb_id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, nullable=False)
    company_code = db.Column(db.String(100), nullable=False)
    pdb_name = db.Column(db.String(255))
    status = db.Column(db.Integer)
    sort_order = db.Column(db.Integer)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())

    