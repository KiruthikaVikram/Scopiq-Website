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
    
class Country(db.Model):
    country_id = db.Column(db.Integer, primary_key=True)
    country_name = db.Column(db.String(50), nullable=False)
    country_code = db.Column(db.String(50), nullable=False)
    phone_code = db.Column(db.Integer)
    currency = db.Column(db.String(50))
    currency_symbol = db.Column(db.String(50))
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())


class State(db.Model):
    state_id = db.Column(db.Integer, primary_key=True)
    state_name = db.Column(db.String(50), nullable=False)
    state_code = db.Column(db.String(15))
    country_id = db.Column(db.Integer, db.ForeignKey('country.country_id'))
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

    
class DateFormat(db.Model):
    date_format_id = db.Column(db.Integer, primary_key=True)
    date_format = db.Column(db.String(50),nullable=False)
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())
    
class Company(db.Model):
    company_id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100),nullable=False)
    company_code = db.Column(db.String(100))
    address =  db.Column(db.Text,nullable=False)
    email = db.Column(db.String(100),nullable=False)
    upload_files = db.Column(db.String(100))
    date_format = db.Column(db.Integer,nullable=False)
    login_type = db.Column(db.Integer,nullable=False)
    country_id = db.Column(db.Integer)
    state_id = db.Column(db.Integer)
    city_id = db.Column(db.Integer)
    financial_year = db.Column(db.Date)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime, default=func.now())
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime, default=func.now())
    dynamic_table_name = db.Column(db.String(50))
   
class Department(db.Model):
    department_id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String(50),nullable=False)
    department_code = db.Column(db.String(15),nullable=False)
    status = db.Column(db.Integer, nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.company_id'))
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())
    
class Roles(db.Model):
    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(50),nullable=False)
    status = db.Column(db.Integer, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.department_id'))
    company_id = db.Column(db.Integer, db.ForeignKey('company.company_id'))
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())
    
class LocationList(db.Model):
    location_id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.company_id'))
    location_name = db.Column(db.String(100),nullable=False)
    country_id = db.Column(db.Integer)
    state_id = db.Column(db.Integer)
    city_id = db.Column(db.Integer)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())
    phone_code = db.Column(db.String(15))
    login_type = db.Column(db.Integer, nullable=False)
        
class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id'))
    department_id = db.Column(db.Integer, db.ForeignKey('department.department_id'))
    employee_code = db.Column(db.String(100))
    gender = db.Column(db.String(100))
    personal_contact = db.Column(db.String(25))
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    blood_group = db.Column(db.String(100))
    dob = db.Column(db.Date)
    doj = db.Column(db.Date)
    sys_role = db.Column(db.String(100))
    country_id = db.Column(db.Integer)
    state_id = db.Column(db.Integer)
    city_id = db.Column(db.Integer)
    location_id = db.Column(db.Integer, nullable=False)
    company_id = db.Column(db.Integer, nullable=False)
    company_code = db.Column(db.String(100))
    filedata = db.Column(db.String(100))
    type_of_user = db.Column(db.String(100))
    initial_type_of_user = db.Column(db.String(100))
    user_image = db.Column(db.String(100))
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())
    login_sys_role = db.Column(db.Integer)
    phone_code = db.Column(db.Integer)
    reporting_manager_id = db.Column(db.Integer)
    old_emp_id = db.Column(db.Integer)
    reassign_status = db.Column(db.Integer)
    left_date = db.Column(db.Date)
    status = db.Column(db.Integer, nullable=False)


class CompanyHistory(db.Model):
    __bind_key__ = 'sql_siteadmin'
    company_history_id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer)
    company_name = db.Column(db.String(100))
    company_code = db.Column(db.String(100))
    address = db.Column(db.Text)
    email = db.Column(db.String(100))
    upload_files = db.Column(db.String(100))
    date_format = db.Column(db.Integer)
    login_type = db.Column(db.Integer)
    country_id = db.Column(db.Integer)
    state_id = db.Column(db.Integer)
    city_id = db.Column(db.Integer)
    financial_year = db.Column(db.Date)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now())
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())
    dynamic_table_name = db.Column(db.String(50))
    
class ProductList(db.Model):
    __bind_key__ = 'sql_siteadmin'
    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())

class Packages(db.Model):
    __bind_key__ = 'sql_siteadmin'
    pkg_list_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(100), nullable=False)
    renewal_date = db.Column(db.Date)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())
    
class UserList(db.Model):
    __bind_key__ = 'sql_siteadmin'
    user_list_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    no_of_users = db.Column(db.String(100), nullable=False)
    renewal_date = db.Column(db.Date)
    user_type_id = db.Column(db.String(100), nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())
    
class CloudList(db.Model):
    __bind_key__ = 'sql_siteadmin'
    cloud_list_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    cloud_type_id = db.Column(db.String(100), nullable=False)
    renewal_date = db.Column(db.Date)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())
    
class MenuRolesList(db.Model):
    __bind_key__ = 'sql_siteadmin'
    menu_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    role_ids = db.Column(db.String(100))
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())


class MenuRolesHistory(db.Model):
    __bind_key__ = 'sql_siteadmin'
    menu_roles_history_id = db.Column(db.Integer, primary_key=True)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu_roles_list.menu_id'))
    user_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    role_ids = db.Column(db.String(100))
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())


class UsersHistory(db.Model):
    __bind_key__ = 'sql_siteadmin'
    user_history_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    username = db.Column(db.String(100))
    email = db.Column(db.String(255))
    password_hash = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id'))
    department_id = db.Column(db.Integer, db.ForeignKey('department.department_id'))
    employee_code = db.Column(db.String(100))
    gender = db.Column(db.String(100))
    personal_contact = db.Column(db.String(25))
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    blood_group = db.Column(db.String(100))
    dob = db.Column(db.Date)
    doj = db.Column(db.Date)
    sys_role = db.Column(db.String(100))
    country_id = db.Column(db.Integer)
    state_id = db.Column(db.Integer)
    city_id = db.Column(db.Integer)
    location_id = db.Column(db.Integer, nullable=False)
    company_id = db.Column(db.Integer, nullable=False)
    filedata = db.Column(db.String(100))
    type_of_user = db.Column(db.String(100))
    initial_type_of_user = db.Column(db.String(100))
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())
    login_sys_role = db.Column(db.Integer)
    phone_code = db.Column(db.Integer)
    reporting_manager_id = db.Column(db.Integer)
    old_emp_id = db.Column(db.Integer)
    reassign_status = db.Column(db.Integer)
    left_date = db.Column(db.Date)
    status = db.Column(db.Integer, nullable=False)
    user_image = db.Column(db.String(100))
    

class UsersBulkupload(db.Model):
    __bind_key__ = 'sql_siteadmin'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password_hash = db.Column(db.String(255))
    role_id = db.Column(db.String(100))
    department_id = db.Column(db.String(100))
    employee_code = db.Column(db.String(100))
    phone_code = db.Column(db.String(100))
    gender = db.Column(db.String(100))
    personal_contact = db.Column(db.String(25))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    blood_group = db.Column(db.String(100))
    dob = db.Column(db.String(100))
    doj = db.Column(db.String(100))
    sys_role = db.Column(db.String(100))
    country_id = db.Column(db.Integer)
    state_id = db.Column(db.Integer)
    city_id = db.Column(db.Integer)
    location_id = db.Column(db.Integer)
    company_id = db.Column(db.Integer)
    filedata = db.Column(db.String(100))
    type_of_user = db.Column(db.String(100))
    initial_type_of_user = db.Column(db.String(100))
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())
    status = db.Column(db.String(100))
    error_message =  db.Column(db.Text)


class Alert_notify_list(db.Model):
    __bind_key__ = 'sql_siteadmin'
    alert_notify_id = db.Column(db.Integer, primary_key=True)
    module_name = db.Column(db.String(50))
    role_name = db.Column(db.String(50))
    type_id = db.Column(db.Integer)
    message = db.Column(db.Text)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())


class Alert_notify_history(db.Model):
    __bind_key__ = 'sql_siteadmin'
    alert_notify_his_id = db.Column(db.Integer, primary_key=True)
    alert_notify_id = db.Column(db.Integer)
    module_name = db.Column(db.String(50))
    role_name = db.Column(db.String(50))
    type_id = db.Column(db.Integer)
    message = db.Column(db.Text)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())

class ReassignRolesList(db.Model):
    __bind_key__ = 'sql_siteadmin'
    reassign_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
    role_id = db.Column(db.Integer)
    new_user_id = db.Column(db.Integer)
    status = db.Column(db.Integer)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())

class UsersStatusHistory(db.Model):
    __bind_key__ = 'sql_siteadmin'
    user_status_his_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    left_date = db.Column(db.Date)
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())


class JobVacancy(db.Model):
    __bind_key__ = 'sql_siteadmin'
    job_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    dept_id = db.Column(db.Integer)
    role_id = db.Column(db.Integer)
    new_user_id = db.Column(db.Integer)
    subordinate_id = db.Column(db.Text)
    filled_date = db.Column(db.Date)
    status = db.Column(db.Integer)
    created_date =db.Column(db.Date)


class Site(db.Model):
    __bind_key__ = 'sql_dms'
    site_id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255))
    port = db.Column(db.Integer)
    user_name = db.Column(db.String(50))
    hash_password = db.Column(db.String(100))
    site_status = db.Column(db.String(50))
    company_id = db.Column(db.Integer)
    location_id = db.Column(db.Integer)
    add_or_edit = db.Column(db.Integer)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())


class Server(db.Model):
    __bind_key__ = 'sql_dms'
    server_id = db.Column(db.Integer, primary_key=True)
    server_type = db.Column(db.Integer, nullable=False)
    server_url = db.Column(db.String(255))
    server_port = db.Column(db.Integer)
    server_uname = db.Column(db.String(50))
    server_pwd = db.Column(db.String(100))
    server_status = db.Column(db.String(50))
    company_id = db.Column(db.Integer)
    location_id = db.Column(db.Integer)
    add_or_edit = db.Column(db.Integer)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())


class Domain(db.Model):
    __bind_key__ = 'sql_dms'
    domain_id = db.Column(db.Integer, primary_key=True)
    domain_name = db.Column(db.String(50), nullable=False)
    status = db.Column(db.Integer, nullable=False)
    company_id = db.Column(db.Integer)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())


class Programservice(db.Model):
    __bind_key__ = 'sql_dms'
    program_service_id = db.Column(db.Integer, primary_key=True)
    program_name = db.Column(db.String(100), nullable = False)
    short_code = db.Column(db.String(15), nullable = False)
    scope = db.Column(db.Text, nullable = False)
    description = db.Column(db.Text, nullable = False)
    company_id = db.Column(db.Integer)
    approval_type = db.Column(db.Integer, nullable = False)
    index_type = db.Column(db.Integer, nullable = False)
    node_level = db.Column(db.Integer, nullable = False)
    continuous_numbering = db.Column(db.Integer)
    primary_document = db.Column(db.Integer, nullable = False)
    revision_history = db.Column(db.Integer, nullable = False)
    last_access = db.Column(db.Integer, nullable = False)
    print_option = db.Column(db.Integer, nullable = False)
    domain_id = db.Column(db.Integer)
    rule_id = db.Column(db.String(20))
    status = db.Column(db.Integer)
    location_id = db.Column(db.Integer)
    server_id = db.Column(db.Text)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())
    common_id = db.Column(db.Integer)
    continue_from_old = db.Column(db.Integer)
    document_rule = db.Column(db.Integer)
    pgm_old_rev_num = db.Column(db.String(15))
    pgm_level_number = db.Column(db.String(50))
    pgm_level_shortcode = db.Column(db.String(50))
    pgm_level_revsion_number = db.Column(db.String(50))
    pgm_level_revsion_number_initial = db.Column(db.String(10))
    program_type = db.Column(db.String(100))



class Nodes(db.Model):
    __bind_key__ = 'sql_dms'
    node_id = db.Column(db.Integer, primary_key=True)
    node_name = db.Column(db.String(100), nullable=False)
    node_type = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    printable_by = db.Column(db.Integer, nullable=False)
    revision_control = db.Column(db.Integer, nullable=False)
    continuous_numbering = db.Column(db.Integer, nullable=False)
    document_rule = db.Column(db.Integer, nullable=False)
    parent_node = db.Column(db.Integer)
    rule_id = db.Column(db.Integer)
    status = db.Column(db.Integer)
    program_id = db.Column(db.Integer)
    short_code = db.Column(db.String(50), nullable=False)
    location_id = db.Column(db.Integer)
    company_id = db.Column(db.Integer)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())
    created_by_first = db.Column(db.Integer)
    node_revision_number = db.Column(db.String(10))
    doc_number_shortcode = db.Column(db.Integer)
    revision_number = db.Column(db.String(15))
    revision_rule = db.Column(db.String(15))
    node_template = db.Column(db.Integer)
    printpage_continues_number = db.Column(db.Integer)
    node_old_rev_num = db.Column(db.String(15))
    node_level_number = db.Column(db.String(50))
    node_level_shortcode = db.Column(db.String(50))
    node_level_revsion_number = db.Column(db.String(50))
    approval_type = db.Column(db.Integer)
    node_level_revsion_number_initial = db.Column(db.String(10))


class Revisionrule(db.Model):
    __bind_key__ = 'sql_dms'
    revision_rule_id = db.Column(db.Integer, primary_key=True)
    rules = db.Column(db.String(50), nullable=False)
    minor_addend = db.Column(db.String(50))
    major_addend = db.Column(db.String(50))
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())
    starting_number = db.Column(db.String(50))
    rule_id_example = db.Column(db.String(50))


class Documentstructure(db.Model):
    __bind_key__ = 'sql_dms'
    document_structure_id = db.Column(db.Integer, primary_key=True)
    program_service_id = db.Column(db.Integer, nullable=False)
    node_id = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    old_document = db.Column(db.String(50), nullable=False)
    old_revision_number = db.Column(db.String(15), nullable=False)
    doc_number = db.Column(db.String(50), nullable=False)
    doc_rule = db.Column(db.Integer)
    document_name = db.Column(db.String)
    status = db.Column(db.Integer)
    sort_order = db.Column(db.String(10))
    revision_rule_id = db.Column(db.Integer)
    user_view_status = db.Column(db.Integer)
    company_id = db.Column(db.Integer)
    location_id = db.Column(db.Integer)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())
    created_by_first = db.Column(db.Integer)
    revision_rule = db.Column(db.Integer)
    approval_type = db.Column(db.Integer)
    old_document_structure = db.Column(db.Integer)


class Documentrevision(db.Model):
    __bind_key__ = 'sql_dms'
    document_id = db.Column(db.Integer, primary_key=True)
    document = db.Column(db.String)
    document_name_id = db.Column(db.Integer)
    comments = db.Column(db.String)
    add_or_edit_status = db.Column(db.Integer)
    inherit = db.Column(db.Integer)
    status = db.Column(db.Integer)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())
    revision_number = db.Column(db.String(50))
    file_content = db.Column(db.Text)
    doc_revision_name = db.Column(db.String(50))
    save_status = db.Column(db.Integer)
    saveandinherit = db.Column(db.Integer,default=0, nullable=False)
    logo_name = db.Column(db.String(100))


class DocumentrevisionHistory(db.Model):
    __bind_key__ = 'sql_dms'
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer)
    document_file_name = db.Column(db.String)
    comments = db.Column(db.String)
    company_id = db.Column(db.Integer)
    status = db.Column(db.Integer)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    created_date_history = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    file_content = db.Column(db.Text)
    doc_revision_name = db.Column(db.String(50))
    document_structure_id = db.Column(db.Integer)
    revision_number = db.Column(db.String(50))
    doc_level_name = db.Column(db.String(50))
    doc_current_status = db.Column(db.String(50))

class Documentlevel(db.Model):   
    __bind_key__ = 'sql_dms'  
    level_id = db.Column(db.Integer, primary_key=True)
    level_name = db.Column(db.String)
    parent_level_id = db.Column(db.Integer)
    program_id = db.Column(db.Integer, nullable = False)
    node_id = db.Column(db.Integer)
    document_id = db.Column(db.Integer)
    level_type = db.Column(db.String)
    status = db.Column(db.Integer)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    created_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())
    updated_by = db.Column(db.BigInteger)
    next_existing_level = db.Column(db.Integer)
    final_level = db.Column(db.Integer)
    level_name_type = db.Column(db.String(50))
    manager_name_type = db.Column(db.String(50))
    original_level = db.Column(db.Integer)
    created_by_first = db.Column(db.Integer)


class Approver(db.Model):
    __bind_key__ = 'sql_dms'
    approver_id = db.Column(db.Integer, primary_key=True)
    level_id = db.Column(db.Integer)
    appr_user_id = db.Column(db.Integer)
    status = db.Column(db.Integer)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())


class Documentapproval(db.Model):
    __bind_key__ = 'sql_dms'
    approval_id = db.Column(db.Integer, primary_key=True)
    approver_id = db.Column(db.Integer)
    approver_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    approver_comments = db.Column(db.String)
    level_id = db.Column(db.Integer)
    document_id = db.Column(db.Integer)
    revision_id = db.Column(db.Integer)
    status = db.Column(db.Integer)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())
    level_type = db.Column(db.String)


class Companysettings(db.Model):
    __bind_key__ = 'sql_dms'
    setting_id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(50))
    admin_count = db.Column(db.Integer)
    manager_count = db.Column(db.Integer)
    approver_count = db.Column(db.Integer)
    format_count = db.Column(db.Integer)
    program_count = db.Column(db.Integer)
    company_type = db.Column(db.Integer)
    print = db.Column(db.Integer)
    program_service = db.Column(db.Integer)
    document_service = db.Column(db.Integer)
    format = db.Column(db.Integer)
    approval_service = db.Column(db.Integer)
    company_logo = db.Column(db.String)
    company_id = db.Column(db.Integer)
    status = db.Column(db.Integer)


class FormatTemplates(db.Model):
    __bind_key__ = 'sql_dms'
    id = db.Column(db.Integer, primary_key=True)
    media = db.Column(db.String)
    template_code = db.Column(db.String(50))
    description = db.Column(db.Text, nullable = False)
    status = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    company_id = db.Column(db.Integer)
    template_name = db.Column(db.String(50))


class CompanyFormatService(db.Model):
    __bind_key__ = 'sql_dms'
    id = db.Column(db.Integer, primary_key=True)
    files = db.Column(db.String)
    company_format_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    file_id = db.Column(db.Integer)
    location_id = db.Column(db.Integer)


class ProgramFormatService(db.Model):
    __bind_key__ = 'sql_dms'
    id = db.Column(db.Integer, primary_key=True)
    program_file_id = db.Column(db.Integer)
    program_format_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    company_id = db.Column(db.Integer)
    file_id = db.Column(db.Integer)
    default_template = db.Column(db.Integer)


class Master(db.Model):
    __bind_key__ = 'sql_dms'
    feature_id = db.Column(db.Integer, primary_key=True)
    feature_name = db.Column(db.String(50))
    name = db.Column(db.String(50))


class Parentchild(db.Model):
    __bind_key__ = 'sql_dms'
    id = db.Column(db.Integer, primary_key=True)
    feature_name_id = db.Column(db.Integer, db.ForeignKey('master.feature_id'))
    parent_id = db.Column(db.Integer)


class ProgramAdminAllocation(db.Model):
    __bind_key__ = 'sql_dms'
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer)
    program_id = db.Column(db.Integer)
    company_id = db.Column(db.Integer)
    status = db.Column(db.Integer)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())
    common_id = db.Column(db.Integer)
    created_by_first = db.Column(db.Integer)


class ExternalDocumentApproval(db.Model):
    __bind_key__ = 'sql_dms'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    external_approver_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    external_approver_comments = db.Column(db.String)
    revision_id = db.Column(db.Integer)
    upload_files = db.Column(db.String)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())

    
class LocationDepartmentMapping(db.Model):
    __bind_key__ = 'sql_dms'
    location_department_mapping_id = db.Column(db.Integer, primary_key=True)
    common_id = db.Column(db.Integer)
    company_id = db.Column(db.Integer)
    location_id = db.Column(db.Integer)
    department_id = db.Column(db.Integer)
    type = db.Column(db.String)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())


class DocumentManagerAllocation(db.Model):
    __bind_key__ = 'sql_dms'
    id = db.Column(db.Integer, primary_key=True)
    manager_id = db.Column(db.Integer)
    program_id = db.Column(db.Integer)
    node_id = db.Column(db.Integer)
    document_id = db.Column(db.Integer)
    location_id = db.Column(db.Integer)
    company_id = db.Column(db.Integer)
    status = db.Column(db.Integer)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())
    created_by_first = db.Column(db.Integer)
    common_id = db.Column(db.Integer)


class DocumentManagerAllocationHistory(db.Model):
    __bind_key__ = 'sql_dms'
    id = db.Column(db.Integer, primary_key=True)
    old_id = db.Column(db.Integer)
    manager_id = db.Column(db.Integer)
    program_id = db.Column(db.Integer)
    node_id = db.Column(db.Integer)
    document_id = db.Column(db.Integer)
    location_id = db.Column(db.Integer)
    company_id = db.Column(db.Integer)
    status = db.Column(db.Integer)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())
    created_by_first = db.Column(db.Integer)
    common_id = db.Column(db.Integer)


class UserDocumentMapping(db.Model):
    __bind_key__ = 'sql_dms'
    user_document_mapping = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    document_id = db.Column(db.Integer)
    status = db.Column(db.Integer)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())
    department_id = db.Column(db.Integer)
    role_id = db.Column(db.Integer)
    access_type = db.Column(db.String(10))


class Oldrevision(db.Model):
    __bind_key__ = 'sql_dms'
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer)
    oldrevision_number = db.Column(db.String)
    change_comments = db.Column(db.Text)
    file_name = db.Column(db.String)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())
    status = db.Column(db.Integer)



class ChangeRequestApproval(db.Model):
    __bind_key__ = 'sql_dms'
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer)
    oldrevision_number = db.Column(db.Integer)
    change_comments = db.Column(db.Text)
    file_name = db.Column(db.String)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())


class ChangeRequestApprovalLevel(db.Model):
    __bind_key__ = 'sql_dms'
    level_id = db.Column(db.Integer, primary_key=True)
    level_name = db.Column(db.String)
    parent_level_id = db.Column(db.Integer)
    program_id = db.Column(db.Integer, nullable = False)
    node_id = db.Column(db.Integer)
    document_id = db.Column(db.Integer)
    level_type = db.Column(db.String)
    status = db.Column(db.Integer)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    created_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())
    updated_by = db.Column(db.BigInteger)
    next_existing_level = db.Column(db.Integer)
    final_level = db.Column(db.Integer)
    level_name_type = db.Column(db.String(50))
    manager_name_type = db.Column(db.String(50))
    original_level = db.Column(db.Integer)
    manager_id = db.Column(db.Text)
    created_by_first = db.Column(db.Integer)
    

class ApprovalpendingtableHistory(db.Model):
    __bind_key__ = 'sql_dms'
    pending_id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer)
    level_id = db.Column(db.Integer)
    appr_user_id = db.Column(db.Integer)
    status = db.Column(db.Integer)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())
    level_type = db.Column(db.String)
    change_req_level = db.Column(db.Integer)


class Approvalpendingtable(db.Model):
    __bind_key__ = 'sql_dms'
    pending_id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer)
    level_id = db.Column(db.Integer)
    appr_user_id = db.Column(db.Integer)
    status = db.Column(db.Integer)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())
    level_type = db.Column(db.String)
    change_req_level = db.Column(db.Integer)


class UserApprover(db.Model):
    __bind_key__ = 'sql_dms'
    user_approver_id = db.Column(db.Integer, primary_key=True)
    level_id = db.Column(db.Integer)
    appr_user_id = db.Column(db.Integer)
    status = db.Column(db.Integer)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())


class ChangeRequest(db.Model):
    __bind_key__ = 'sql_dms'
    change_request_id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer)
    change = db.Column(db.String)
    reason = db.Column(db.String)
    company_id = db.Column(db.Integer)
    location_id = db.Column(db.Integer)
    status = db.Column(db.Integer)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())
    document_revision_name = db.Column(db.String(50))


class ChangeRequestHistory(db.Model):
    __bind_key__ = 'sql_dms'
    change_request_history_id = db.Column(db.Integer, primary_key=True)
    change_request_id = db.Column(db.Integer)
    document_id = db.Column(db.Integer)
    change = db.Column(db.String)
    reason = db.Column(db.String)
    company_id = db.Column(db.Integer)
    location_id = db.Column(db.Integer)
    status = db.Column(db.Integer)
    users_id = db.Column(db.Integer)
    approval_type = db.Column(db.String)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())
    document_revision_name = db.Column(db.String(50))  
    level_name = db.Column(db.String(50))  
    comments = db.Column(db.String) 


class CompanyImages(db.Model):
    __bind_key__ = 'sql_dms'
    id = db.Column(db.Integer, primary_key=True)
    contents = db.Column(db.String(600))
    status = db.Column(db.Integer)
    typeofcontents = db.Column(db.String(100))
    company_id = db.Column(db.Integer)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())


class UserDocumentApproval(db.Model):
    __bind_key__ = 'sql_dms'
    approval_id = db.Column(db.Integer, primary_key=True)
    approver_id = db.Column(db.Integer)
    approver_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    approver_comments = db.Column(db.String)
    level_id = db.Column(db.Integer)
    document_id = db.Column(db.Integer)
    revision_id = db.Column(db.Integer)
    status = db.Column(db.Integer)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())
    level_type = db.Column(db.String)


class ProgramAndNodeRevisionHistory(db.Model):
    __bind_key__ = 'sql_dms'
    pn_id = db.Column(db.Integer, primary_key=True)
    revision_type = db.Column(db.String(5), nullable = False)
    revision_type_id = db.Column(db.Integer, nullable = False)
    revision_type_name = db.Column(db.String(10), nullable = False)
    old_revision_type_name = db.Column(db.String(10), nullable = False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())
    document_list = db.Column(db.Text,nullable=False)
    approval_type = db.Column(db.Integer, nullable = False)
    view_status = db.Column(db.Integer)
    

class DupUserDocumentMapping(db.Model):
    __bind_key__ = 'sql_dms'
    user_document_mapping = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    document_id = db.Column(db.Integer)
    status = db.Column(db.Integer)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())


class UserViewDocument(db.Model):
    __bind_key__ = 'sql_dms'
    view_doc_id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, nullable = False)
    user_id = db.Column(db.Integer, nullable = False)
    status = db.Column(db.Integer)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())


class ReleaserLevel(db.Model): 
    __bind_key__ = 'sql_dms'    
    level_id = db.Column(db.Integer, primary_key=True)
    level_name = db.Column(db.String)
    parent_level_id = db.Column(db.Integer)
    program_id = db.Column(db.Integer, nullable = False)
    node_id = db.Column(db.Integer)
    document_id = db.Column(db.Integer)
    level_type = db.Column(db.String)
    status = db.Column(db.Integer)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    created_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())
    updated_by = db.Column(db.BigInteger)
    approval_list = db.Column(db.Text)
    final_level = db.Column(db.Integer)



class ReleaserApprover(db.Model):
    __bind_key__ = 'sql_dms'
    releaser_approver_id = db.Column(db.Integer, primary_key=True)
    level_id = db.Column(db.Integer)
    appr_user_id = db.Column(db.Integer)
    status = db.Column(db.Integer)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())



class Releaserapprovalpendingtable(db.Model):
    __bind_key__ = 'sql_dms'
    pending_id = db.Column(db.Integer, primary_key=True)
    pgm_node_document_id = db.Column(db.Integer)
    level_id = db.Column(db.Integer)
    appr_user_id = db.Column(db.Integer)
    status = db.Column(db.Integer)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    level_type = db.Column(db.String(20)) 


class ReassignAdminHistory(db.Model):
    __bind_key__ = 'sql_dms'
    id = db.Column(db.Integer, primary_key=True)
    program_id = db.Column(db.Integer)
    node_id = db.Column(db.Integer)
    document_id = db.Column(db.Integer)
    role_id  = db.Column(db.Integer)
    deactvie_user_id = db.Column(db.Integer)
    new_assign_user_id = db.Column(db.Integer)
    assign_status = db.Column(db.Integer)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.Integer)  

class SuggestionTemplateUseDetails(db.Model):
    __bind_key__ = 'sql_dms'
    sugg_id = db.Column(db.Integer, primary_key=True)
    scope_id = db.Column(db.Integer)
    created_by = db.Column(db.Integer)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)


class Type(db.Model):
    __bind_key__ = 'sql_cms'
    type_id = db.Column(db.Integer, primary_key=True)
    typename = db.Column(db.String(255), nullable=False)
    indiv_comp = db.Column(db.Integer, nullable=False)   

class GroupList(db.Model):
    __bind_key__ = 'sql_cms'
    group_id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(255), nullable=False)    
    type_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now()) 

class CertificateMaster(db.Model):
    __bind_key__ = 'sql_cms'

    certif_id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer, nullable=False)
    scopes = db.Column(db.String(255), nullable=False)    
    group_id = db.Column(db.Integer, nullable=False)
    code_std_reg = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    alert_period = db.Column(db.Integer, nullable=False)    
    cont_record = db.Column(db.String(255), nullable=False)  
    cont_freq = db.Column(db.String(255), nullable=False)  
    cont_notif = db.Column(db.String(255), nullable=False)    
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())        

class CertificationAgency(db.Model):
    __bind_key__ = 'sql_cms'
    agency_id = db.Column(db.Integer, primary_key=True)
    agency_name = db.Column(db.String(255), nullable=False)    
    address = db.Column(db.Text, nullable=False)
    country_id = db.Column(db.Integer, nullable=False)
    state_id = db.Column(db.Integer, nullable=False)
    city_id = db.Column(db.Integer, nullable=False) 
    gst = db.Column(db.String(255), nullable=False)
    contact = db.Column(db.String(255), nullable=False) 
    email = db.Column(db.String(255), nullable=False)  
    phone = db.Column(db.String(255), nullable=False)    
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())

class CodeStdRegulation(db.Model):
    __bind_key__ = 'sql_cms'
    code_id = db.Column(db.Integer, primary_key=True)
    code_std = db.Column(db.String(255), nullable=False)   
    type_id = db.Column(db.Integer, nullable=False)   
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())


class ApproverAllocation(db.Model):
    __bind_key__ = 'sql_cms'
    alloc_id = db.Column(db.Integer, primary_key=True)
    common_id = db.Column(db.Integer)
    type_id = db.Column(db.Integer)
    group_id = db.Column(db.Integer)
    certificate_id = db.Column(db.Integer)
    department_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)    
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now()) 


class ManageEmpCertif(db.Model):
    __bind_key__ = 'sql_cms'
    manage_id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer)
    group_id = db.Column(db.Integer)
    certificate_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)    
    agency_id = db.Column(db.Integer) 
    mail_status = db.Column(db.Integer) 
    del_cert = db.Column(db.Integer) 
    certif_no = db.Column(db.String(255), nullable=False)
    comments = db.Column(db.Text) 
    upload_file = db.Column(db.String(255), nullable=False)
    issue_date = db.Column(db.Date)
    valid_upto = db.Column(db.Date)
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())      



class ManageEmpContinuity(db.Model):
    __bind_key__ = 'sql_cms'
    cont_id = db.Column(db.Integer, primary_key=True)
    certificate_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)    
    reviewed_by = db.Column(db.Integer)
    manage_id = db.Column(db.Integer)    
    upload_file = db.Column(db.String(255), nullable=False)
    schedule_date = db.Column(db.Date)
    actual_date = db.Column(db.Date)
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())   

class AuthUserAllocation(db.Model):
    __bind_key__ = 'sql_cms'
    
    alloc_id = db.Column(db.Integer, primary_key=True)
    common_id = db.Column(db.Integer)
    type_id = db.Column(db.Integer)
    group_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)    
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())         

class ManageCompCertif(db.Model):
    __bind_key__ = 'sql_cms'
    
    manage_id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer)
    group_id = db.Column(db.Integer)
    certificate_id = db.Column(db.Integer)
    agency_id = db.Column(db.Integer) 
    del_cert = db.Column(db.Integer) 
    mail_status = db.Column(db.Integer) 
    upload_file = db.Column(db.String(255), nullable=False)
    issue_date = db.Column(db.Date)
    valid_upto = db.Column(db.Date)
    fees = db.Column(db.String(255))
    certif_no = db.Column(db.String(255))
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())       

class ManageCompContinuity(db.Model):
    __bind_key__ = 'sql_cms'

    cont_id = db.Column(db.Integer, primary_key=True)
    certificate_id = db.Column(db.Integer)
    reviewed_by = db.Column(db.Integer)
    manage_id = db.Column(db.Integer) 
    upload_file = db.Column(db.String(255), nullable=False)
    schedule_date = db.Column(db.Date)
    actual_date = db.Column(db.Date)
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())

# AMS

class AuditObservationList(db.Model):
    __bind_key__ = 'sql_ams'
    observation_id = db.Column(db.Integer, primary_key=True)
    observation_name = db.Column(db.String(255))
    observation_type = db.Column(db.Integer)
    display_name = db.Column(db.String(255))
    parent_id = db.Column(db.Integer)
    status =  db.Column(db.Integer)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())
    created_by = db.Column(db.BigInteger)


class AuditSettings(db.Model):
    __bind_key__ = 'sql_ams'
    setting_id = db.Column(db.Integer, primary_key=True)
    audit_hours = db.Column(db.String(255), nullable=False)
    audit_days = db.Column(db.String(255), nullable=False)
    full_month_hours = db.Column(db.String(255), nullable=False)
    full_year_hours = db.Column(db.String(255), nullable=False)
    part_month_hours = db.Column(db.String(255), nullable=False)
    part_year_hours = db.Column(db.String(255), nullable=False)
    status =  db.Column(db.Integer, nullable=False)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())
    created_by = db.Column(db.BigInteger)
    
class AuditType(db.Model):
    __bind_key__ = 'sql_ams'
    type_id = db.Column(db.Integer, primary_key=True)
    typename = db.Column(db.String(255), nullable=False)
    typecode = db.Column(db.String(255), nullable=False)
    status =  db.Column(db.Integer, nullable=False)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())
    created_by = db.Column(db.BigInteger)



class AssignAuditorList(db.Model):
    __bind_key__ = 'sql_ams'
    assign_auditor_id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    full_time_auditor = db.Column(db.Integer)  
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())



class AdminAllocationMaster(db.Model):
    __bind_key__ = 'sql_ams'
    admin_allocation_id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer, db.ForeignKey('audit_type.type_id'))
    user_id = db.Column(db.Integer)    
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())


class AllocationMaster(db.Model):
    __bind_key__ = 'sql_ams'
    allocation_id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer, db.ForeignKey('audit_type.type_id'))
    user_id = db.Column(db.Integer)    
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())  


class ChecklistMaster(db.Model):
    __bind_key__ = 'sql_ams'
    checklist_id = db.Column(db.Integer, primary_key=True)
    checklist_name = db.Column(db.String(255), nullable=False)
    checklist_series_no = db.Column(db.String(25), nullable=False)
    checklist_no = db.Column(db.Integer, nullable=False)
    checklist_option = db.Column(db.Integer, nullable=False)
    checklist_code = db.Column(db.String(25), nullable=False)    
    type_id = db.Column(db.Integer, db.ForeignKey('audit_type.type_id')) 
    status = db.Column(db.Integer, nullable=False)
    current_rev_no = db.Column(db.Integer, nullable=False)
    approval_status = db.Column(db.Integer, nullable=False)
    checklist_date = db.Column(db.Date, nullable=False)
    effective_date = db.Column(db.Date)
    replace_cl_id = db.Column(db.Integer)
    created_by = db.Column(db.BigInteger)
    created_role_id = db.Column(db.BigInteger, nullable=False)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())        


class ChecklistItemsMaster(db.Model):
    __bind_key__ = 'sql_ams'
    checkitem_id = db.Column(db.Integer, primary_key=True)
    checklist_id = db.Column(db.Integer, db.ForeignKey('checklist_master.checklist_id'))
    checkitem_name = db.Column(db.Text, nullable=False)
    checkitem_division = db.Column(db.String(25), nullable=False)
    checkitem_division_id = db.Column(db.Integer)
    checkitem_duplicate_id = db.Column(db.Integer)
    clause_no = db.Column(db.String(100))
    procedure_ref_no = db.Column(db.String(100))
    parent_id = db.Column(db.Integer)
    sort_order = db.Column(db.Integer)
    s_no = db.Column(db.String(100))
    status = db.Column(db.Integer, nullable=False) 
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())


class ChecklistObservationList(db.Model):
    __bind_key__ = 'sql_ams'
    co_id = db.Column(db.Integer, primary_key=True)
    audit_id = db.Column(db.Integer)
    checklist_id = db.Column(db.Integer)
    checkitem_id = db.Column(db.Integer)
    s_no = db.Column(db.Integer)
    observation_id = db.Column(db.Integer)
    suggestion_id = db.Column(db.Integer)
    observation_comments = db.Column(db.Text)
    suggestion_comments = db.Column(db.Text)
    upload_files = db.Column(db.Text)
    status =  db.Column(db.Integer)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())
    created_by = db.Column(db.BigInteger)


class ChecklistObservationReviewList(db.Model):
    __bind_key__ = 'sql_ams'
    co_review_id = db.Column(db.Integer, primary_key=True)
    co_id = db.Column(db.Integer)
    audit_id = db.Column(db.Integer)
    checklist_id = db.Column(db.Integer)
    checkitem_id = db.Column(db.Integer)
    s_no = db.Column(db.Integer)
    observation_id = db.Column(db.Integer)
    suggestion_id = db.Column(db.Integer)
    observation_comments = db.Column(db.Text)
    suggestion_comments = db.Column(db.Text)
    upload_files = db.Column(db.Text)
    status =  db.Column(db.Integer)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())
    created_by = db.Column(db.BigInteger)


class UploadFilesList(db.Model):
    __bind_key__ = 'sql_ams'
    upload_id = db.Column(db.Integer, primary_key=True)
    co_id = db.Column(db.Integer)
    file_name = db.Column(db.Text)
    status =  db.Column(db.Integer)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())
    created_by = db.Column(db.BigInteger)

class UploadFilesReviewList(db.Model):
    __bind_key__ = 'sql_ams'
    upload_review_id = db.Column(db.Integer, primary_key=True)
    co_review_id = db.Column(db.Integer)
    co_id = db.Column(db.Integer)
    file_name = db.Column(db.Text)
    status =  db.Column(db.Integer)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())
    created_by = db.Column(db.BigInteger)


class ChecklistApproval(db.Model):
    __bind_key__ = 'sql_ams'
    checklist_approval_id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer, db.ForeignKey('audit_type.type_id'))
    checklist_id = db.Column(db.Integer, db.ForeignKey('checklist_master.checklist_id'))
    user_id = db.Column(db.Integer)
    approver_id = db.Column(db.Integer)    
    status = db.Column(db.Integer, nullable=False)
    comments = db.Column(db.Text, nullable=False)
    approver_comments = db.Column(db.Text)
    added_date = db.Column(db.Date, nullable=False)
    approval_date = db.Column(db.Date)
    created_role_id = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())


class ChecklistRevision(db.Model):
    __bind_key__ = 'sql_ams'
    checklist_revision_id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer, db.ForeignKey('audit_type.type_id'))
    checklist_id = db.Column(db.Integer, db.ForeignKey('checklist_master.checklist_id'))
    user_id = db.Column(db.Integer)
    revision_number = db.Column(db.Integer)
    status = db.Column(db.Integer)
    modified_date = db.Column(db.Date)
    approved_date = db.Column(db.Date)
    modified_by = db.Column(db.Integer)
    approved_by = db.Column(db.Integer)
    modified_comments = db.Column(db.Text)
    approved_comments = db.Column(db.Text)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())


class ChecklistHistory(db.Model):
    __bind_key__ = 'sql_ams'
    checklist_history_id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer, db.ForeignKey('audit_type.type_id'))
    checklist_id = db.Column(db.Integer, db.ForeignKey('checklist_master.checklist_id'))
    checklist_name = db.Column(db.String(255), nullable=False)
    checklist_code = db.Column(db.String(25), nullable=False)
    checkitem_id = db.Column(db.Integer)
    checkitem_name = db.Column(db.Text, nullable=False)
    checkitem_division = db.Column(db.String(25), nullable=False)
    checkitem_division_id = db.Column(db.Integer)
    clause_no = db.Column(db.String(100))
    procedure_ref_no = db.Column(db.String(100))
    parent_id = db.Column(db.Integer)
    revision_number = db.Column(db.Integer)
    sort_order = db.Column(db.Integer)
    s_no = db.Column(db.String(100))
    user_id = db.Column(db.Integer)  
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())


class AuditorAllocationMaster(db.Model):
    __bind_key__ = 'sql_ams'
    auditor_allocation_id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer, db.ForeignKey('audit_type.type_id'))
    user_id = db.Column(db.Integer)
    lead_auditor_id = db.Column(db.Integer)   
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())


class AuditeeAllocationMaster(db.Model):
    __bind_key__ = 'sql_ams'
    auditee_allocation_id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer, db.ForeignKey('audit_type.type_id'))
    user_id = db.Column(db.Integer)
    lead_auditor_id = db.Column(db.Integer)   
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())


class AuditList(db.Model):
    __bind_key__ = 'sql_ams'
    audit_id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer, db.ForeignKey('audit_type.type_id'))
    department_id = db.Column(db.Integer)
    title = db.Column(db.String(255), nullable=False)
    frequency = db.Column(db.Integer, nullable=False)
    notification = db.Column(db.Integer, nullable=False)
    alert_interval = db.Column(db.Integer, nullable=False)
    plan_hrs = db.Column(db.Integer, nullable=False)
    indiv_plan_hrs = db.Column(db.Integer, nullable=False)
    team_size = db.Column(db.Integer, nullable=False)
    audit_date = db.Column(db.Date, nullable=False)
    audit_start_date = db.Column(db.Date)
    audit_start_time = db.Column(db.String(255))
    audit_close_date = db.Column(db.Date)
    actual_close_date = db.Column(db.Date)
    audit_close_time = db.Column(db.String(255))
    actual_plan_hrs = db.Column(db.Integer)
    checklist_id = db.Column(db.Integer, db.ForeignKey('checklist_master.checklist_id'))
    rev_no = db.Column(db.Integer)
    lead_auditor_id = db.Column(db.Integer, nullable=False)
    auditors_id = db.Column(db.String(255))
    auditee_id = db.Column(db.String(255))
    reviewer_id = db.Column(db.Integer)
    review_comments = db.Column(db.Text)
    old_audit_id = db.Column(db.Integer)
    temp_assign = db.Column(db.Integer)
    re_audit = db.Column(db.Integer)
    re_audit_id = db.Column(db.Integer)
    workload_assign = db.Column(db.Integer)
    replace_assign = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
    days = db.Column(db.Integer)
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())



class AuditScheduleList(db.Model):
    __bind_key__ = 'sql_ams'
    audit_schedule_id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer, db.ForeignKey('audit_type.type_id'))
    department_id = db.Column(db.Integer)
    audit_id = db.Column(db.Integer, db.ForeignKey('audit_list.audit_id'))
    checklist_id = db.Column(db.Integer, db.ForeignKey('checklist_master.checklist_id'))
    rev_no = db.Column(db.Integer)
    title = db.Column(db.String(255), nullable=False)
    frequency = db.Column(db.Integer, nullable=False)
    audit_date = db.Column(db.Date, nullable=False)
    audit_close_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    next_frequency = db.Column(db.Integer, nullable=False)
    lead_auditor_id = db.Column(db.Integer, nullable=False)
    auditors_id = db.Column(db.String(255))
    auditee_id = db.Column(db.String(255))
    total_plan_hrs = db.Column(db.Integer, nullable=False)
    plan_hrs = db.Column(db.Integer, nullable=False)
    days = db.Column(db.Integer)
    team_size = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())


class AuditNcList(db.Model):
    __bind_key__ = 'sql_ams'
    nc_id = db.Column(db.Integer, primary_key=True)
    co_review_id = db.Column(db.Integer)
    co_id = db.Column(db.Integer)
    audit_id = db.Column(db.Integer)
    checklist_id = db.Column(db.Integer)
    checkitem_id = db.Column(db.Integer)
    checkitem_subheading_id = db.Column(db.Integer)
    checkitem_heading_id = db.Column(db.Integer)
    s_no = db.Column(db.Integer)
    status = db.Column(db.Integer)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())



class AuditImpList(db.Model):
    __bind_key__ = 'sql_ams'
    imp_id = db.Column(db.Integer, primary_key=True)
    co_review_id = db.Column(db.Integer)
    co_id = db.Column(db.Integer)
    audit_id = db.Column(db.Integer)
    checklist_id = db.Column(db.Integer)
    checkitem_id = db.Column(db.Integer)
    checkitem_subheading_id = db.Column(db.Integer)
    checkitem_heading_id = db.Column(db.Integer)
    s_no = db.Column(db.Integer)
    status = db.Column(db.Integer)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())


class AuditAllocationList(db.Model):
    __bind_key__ = 'sql_ams'
    audit_allocation_id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer, db.ForeignKey('audit_type.type_id'))
    checklist_id = db.Column(db.Integer, db.ForeignKey('checklist_master.checklist_id'))
    user_id = db.Column(db.Integer)
    audit_id = db.Column(db.Integer, db.ForeignKey('audit_list.audit_id'))
    audit_date = db.Column(db.Date, nullable=False)
    total_plan_hrs = db.Column(db.Integer, nullable=False)
    plan_hrs = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())


class AuditScheduleAllocationList(db.Model):
    __bind_key__ = 'sql_ams'
    audit_schedule_allocation_id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer)
    checklist_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    audit_id = db.Column(db.Integer)
    audit_schedule_id = db.Column(db.Integer)
    audit_date = db.Column(db.Date, nullable=False)
    total_plan_hrs = db.Column(db.Integer, nullable=False)
    plan_hrs = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())


class TemporaryAllocationList(db.Model):
    __bind_key__ = 'sql_ams'
    temp_allocation_id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer, db.ForeignKey('audit_type.type_id'))
    checklist_id = db.Column(db.Integer, db.ForeignKey('checklist_master.checklist_id'))
    user_id = db.Column(db.Integer)
    replace_user_id = db.Column(db.Integer)
    audit_id = db.Column(db.Integer, db.ForeignKey('audit_list.audit_id'))
    audit_date = db.Column(db.Date, nullable=False)
    total_plan_hrs = db.Column(db.Integer, nullable=False)
    plan_hrs = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())



class ReplaceAllocationList(db.Model):
    __bind_key__ = 'sql_ams'
    replace_allocation_id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer, db.ForeignKey('audit_type.type_id'))
    checklist_id = db.Column(db.Integer, db.ForeignKey('checklist_master.checklist_id'))
    user_id = db.Column(db.Integer)
    replace_user_id = db.Column(db.Integer)
    audit_id = db.Column(db.Integer, db.ForeignKey('audit_list.audit_id'))
    audit_date = db.Column(db.Date, nullable=False)
    total_plan_hrs = db.Column(db.Integer, nullable=False)
    plan_hrs = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())


class AuditActionList(db.Model):
    __bind_key__ = 'sql_ams'
    action_id = db.Column(db.Integer, primary_key=True)
    audit_id = db.Column(db.Integer)
    nc_id = db.Column(db.Integer)
    checklist_id = db.Column(db.Integer)
    root_cause_comments = db.Column(db.Text)
    root_cause_evidence = db.Column(db.Text)
    co_action_comments = db.Column(db.Text)
    co_action_evidence = db.Column(db.Text)
    review_rc_comments = db.Column(db.Text)
    review_rc_evidence = db.Column(db.Text)
    review_ca_comments = db.Column(db.Text)
    review_ca_evidence = db.Column(db.Text)
    status = db.Column(db.Integer)
    action_status = db.Column(db.Integer)
    review_status = db.Column(db.Integer)
    verify_status = db.Column(db.Integer)
    verification_req = db.Column(db.Integer)
    action_by = db.Column(db.Integer)
    review_by = db.Column(db.Integer)
    verify_by = db.Column(db.Integer)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())


#### New Changes In Program Service 12.3.2021

class ProgramMadmin(db.Model):
    __bind_key__ = 'sql_dms'
    program_service_id = db.Column(db.Integer, primary_key=True)
    program_name = db.Column(db.String(100), nullable = False)
    program_short_code = db.Column(db.String(15), nullable = False)
    program_type = db.Column(db.String(100), nullable = False)
    company_id = db.Column(db.Integer)
    status = db.Column(db.Integer)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())
    template_id = db.Column(db.Integer)
    

class ProgramMadminHistory(db.Model):
    __bind_key__ = 'sql_dms'
    program_history_id = db.Column(db.Integer, primary_key=True)
    program_service_id = db.Column(db.Integer) 
    program_name = db.Column(db.String(100), nullable = False)
    program_short_code = db.Column(db.String(15), nullable = False)
    program_type = db.Column(db.String(100), nullable = False)
    company_id = db.Column(db.Integer)
    status = db.Column(db.Integer)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())
    

class ProgramService(db.Model):
    __bind_key__ = 'sql_dms'
    program_id = db.Column(db.Integer, primary_key=True)
    program_service_id = db.Column(db.Integer)
    company_id = db.Column(db.Integer)
    approval_type = db.Column(db.Integer, nullable = False)
    revision_history = db.Column(db.Integer, nullable = False)
    revision_history_row_count = db.Column(db.Integer, nullable = False)
    pgm_revision_rule_id = db.Column(db.String(20))
    pgm_manual_number = db.Column(db.String(50))
    continue_from_old = db.Column(db.Integer)
    document_numbering_rule = db.Column(db.Integer)
    program_revision = db.Column(db.Integer, nullable = False)
    print_continuous_numbering = db.Column(db.Integer)
    pgm_old_rev_num = db.Column(db.String(15))
    pgm_level_number = db.Column(db.String(50))
    pgm_level_shortcode = db.Column(db.String(50))
    pgm_level_revsion_number = db.Column(db.String(50))
    pgm_level_revsion_number_initial = db.Column(db.String(10))
    status = db.Column(db.Integer)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())
    
    
class ProgramServiceHistory(db.Model):
    __bind_key__ = 'sql_dms'
    program_history_id = db.Column(db.Integer, primary_key=True)
    program_id = db.Column(db.Integer)
    program_service_id = db.Column(db.Integer)
    company_id = db.Column(db.Integer)
    approval_type = db.Column(db.Integer, nullable = False)
    revision_history = db.Column(db.Integer, nullable = False)
    revision_history_row_count = db.Column(db.Integer, nullable = False)
    pgm_revision_rule_id = db.Column(db.String(20))
    pgm_manual_number = db.Column(db.String(50))
    continue_from_old = db.Column(db.Integer)
    document_numbering_rule = db.Column(db.Integer)
    program_revision = db.Column(db.Integer, nullable = False)
    print_continuous_numbering = db.Column(db.Integer)
    pgm_old_rev_num = db.Column(db.String(15))
    pgm_level_number = db.Column(db.String(50))
    pgm_level_shortcode = db.Column(db.String(50))
    pgm_level_revsion_number = db.Column(db.String(50))
    pgm_level_revsion_number_initial = db.Column(db.String(10))
    status = db.Column(db.Integer)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now()) 


class TemporaryTemplateDetails(db.Model):
    __bind_key__ = 'sql_dms'
    t_id = db.Column(db.Integer, primary_key=True)
    temp_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    steps_id = db.Column(db.Integer, nullable=False) 


class MultiTemplateDetails(db.Model):
    __bind_key__ = 'sql_dms'
    temp_id = db.Column(db.Integer, primary_key=True)
    temp_name = db.Column(db.String(255),nullable=False)
    pagewise_template = db.Column(db.Text,nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())   
    temp_first_page = db.Column(db.Integer) 
    temp_revision_details = db.Column(db.Integer)

class TemplateDetails(db.Model):
    __bind_key__ = 'sql_dms'
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



class PassPercentage(db.Model):
    __bind_key__ = 'sql_kms'
    passper_id = db.Column(db.Integer, primary_key=True)
    department_id = db.Column(db.Integer, nullable=False)  
    pass_per = db.Column(db.String(255), nullable=False)    
     
class PassPercentageHistory(db.Model):
    __bind_key__ = 'sql_kms'
    hist_id = db.Column(db.Integer, primary_key=True)
    department_id = db.Column(db.Integer, nullable=False)  
    old_pass_per = db.Column(db.String(255), nullable=False)  
    pass_per = db.Column(db.String(255), nullable=False)     
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)

class UserGroupAllocation(db.Model):
    __bind_key__ = 'sql_kms'
    alloc_id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)    
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())   

class CourseStream(db.Model):
    __bind_key__ = 'sql_kms'
    crse_strm_id = db.Column(db.Integer, primary_key=True)
    crse_strm_name = db.Column(db.String(255), nullable=False)  
    crse_strm_short = db.Column(db.String(255), nullable=False)  
    status = db.Column(db.Integer)
    seq_num = db.Column(db.Integer)    
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)

class CourseModule(db.Model):
    __bind_key__ = 'sql_kms'
    module_id = db.Column(db.Integer, primary_key=True)
    crse_strm_id = db.Column(db.Integer)
    module_name = db.Column(db.String(255), nullable=False)  
    module_short = db.Column(db.String(5), nullable=False) 
    exam_duration = db.Column(db.String(255), nullable=False)
    is_chapter = db.Column(db.Integer) 
    no_of_ques = db.Column(db.Integer)
    scope = db.Column(db.Text)  
    status = db.Column(db.Integer)
    seq_num = db.Column(db.Integer)    
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)    
          
class Chapter(db.Model):
    __bind_key__ = 'sql_kms'
    chapter_id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer)
    crse_strm_id = db.Column(db.Integer)
    chapter_num = db.Column(db.String(255), nullable=False)
    chapter_title = db.Column(db.String(255), nullable=False)  
    chapter_identifier = db.Column(db.String(50), nullable=False)  
    material = db.Column(db.String(255), nullable=False)  
    duration_hours = db.Column(db.String(255), nullable=False)
    chapter_scope = db.Column(db.Text)  
    status = db.Column(db.Integer)
    seq_num = db.Column(db.Integer)    
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)  

class QuestionType(db.Model):
    __bind_key__ = 'sql_kms'
    ques_type_id = db.Column(db.Integer, primary_key=True)
    type_short = db.Column(db.String(255), nullable=False)  
    ques_type_name = db.Column(db.String(255), nullable=False)  
    ques_type_desc = db.Column(db.Text)  
    status = db.Column(db.Integer)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)

class FinYear(db.Model):
    __bind_key__ = 'sql_kms'
    fin_id = db.Column(db.Integer, primary_key=True)
    fin_year = db.Column(db.String(20), nullable=False)  
    curr_year_flag = db.Column(db.Integer)
    status = db.Column(db.Integer)
    from_date = db.Column(db.Date)
    to_date = db.Column(db.Date)

class ModuleAllocation(db.Model):
    __bind_key__ = 'sql_kms'
    alloc_id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer) 
    module_id = db.Column(db.Integer)
    fin_year = db.Column(db.String(20), nullable=False)  
    status = db.Column(db.Integer)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False) 

class IpIndocAllocation(db.Model):
    __bind_key__ = 'sql_kms'
    alloc_id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer)
    type_id = db.Column(db.Integer)
    chapter_id= db.Column(db.Integer)  
    module_id= db.Column(db.Integer)  
    view_status= db.Column(db.Integer)  
    fin_year = db.Column(db.String(20), nullable=False)   
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)

class IndividualAllocation(db.Model):
    __bind_key__ = 'sql_kms'
    alloc_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer) 
    module_id = db.Column(db.Integer)
    chapter_id = db.Column(db.Integer)
    type_id = db.Column(db.Integer)
    dept_id = db.Column(db.Integer)
    fin_year = db.Column(db.String(20), nullable=False)  
    status = db.Column(db.Integer)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False) 

class ModuleAllocationUser(db.Model):
    __bind_key__ = 'sql_kms'
    alloc_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    module_id = db.Column(db.Integer)
    transfer_id = db.Column(db.Integer)
    user_status= db.Column(db.String(50), nullable=False)   
    fin_year = db.Column(db.String(20), nullable=False)   
    status = db.Column(db.String(50), nullable=False)   
    date_of_complete = db.Column(db.DateTime(timezone=False))
    trans_id = db.Column(db.Integer)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False) 

class ChapterAllocationUser(db.Model):
    __bind_key__ = 'sql_kms'
    alloc_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    module_id = db.Column(db.Integer)
    chapter_id = db.Column(db.Integer)
    transfer_id = db.Column(db.Integer)
    view_count = db.Column(db.Integer)
    user_status= db.Column(db.String(50), nullable=False)   
    fin_year = db.Column(db.String(20), nullable=False)   
    status = db.Column(db.String(50), nullable=False)  
    chapter_duration= db.Column(db.String(50), nullable=False)   
    seq_num = db.Column(db.String(50), nullable=False)   
    date_of_complete = db.Column(db.DateTime(timezone=False))
    trans_id = db.Column(db.Integer)
    feedback = db.Column(db.String(20))   
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)         

class UserStatus(db.Model):
    __bind_key__ = 'sql_kms'
    status_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    user_transfer = db.Column(db.Integer)
    trans_id = db.Column(db.Integer)
    fin_year = db.Column(db.String(20), nullable=False)   
    status = db.Column(db.String(50), nullable=False)  
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)    

class QuestionBank(db.Model):
    __bind_key__ = 'sql_kms'
    ques_id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text)
    question_image = db.Column(db.Text)
    ques_type = db.Column(db.Integer)
    answer_type = db.Column(db.Integer)
    multi_option = db.Column(db.Integer)
    status = db.Column(db.Integer)
    ques_uid = db.Column(db.String(20), nullable=False)   
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False) 
    created_by = db.Column(db.BigInteger)  

class QuestionBankRelation(db.Model):
    __bind_key__ = 'sql_kms'
    relate_ques_id = db.Column(db.Integer, primary_key=True)
    ques_id = db.Column(db.Integer)
    answers = db.Column(db.Text)
    answer_image = db.Column(db.Text)
    is_correct = db.Column(db.Integer)
    
    
class QuestionBankAllocation(db.Model):
    __bind_key__ = 'sql_kms'
    alloc_id = db.Column(db.Integer, primary_key=True)
    ques_id = db.Column(db.Integer)
    module_id = db.Column(db.Integer)


class QuestionAnswer(db.Model):
    __bind_key__ = 'sql_kms'
    seq_id = db.Column(db.Integer, primary_key=True)
    ques_id = db.Column(db.Integer)
    ans_id = db.Column(db.Integer)
    module_id = db.Column(db.Integer)
    ans_status = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    test_id = db.Column(db.Integer)
    dept_id = db.Column(db.Integer)
    ques_type_id = db.Column(db.Integer)
    fin_year = db.Column(db.String(20), nullable=False)   
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    
class TestResult(db.Model):
    __bind_key__ = 'sql_kms'
    test_id = db.Column(db.Integer, primary_key=True)
    ques_id = db.Column(db.Text)
    module_id = db.Column(db.Integer)
    tot_score = db.Column(db.Integer)
    alloc_score = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    dept_id = db.Column(db.Integer)
    pass_status = db.Column(db.String(20), nullable=False)   
    tot_ques = db.Column(db.Integer)
    tot_ans_correct = db.Column(db.Integer)
    tot_ans_wrong = db.Column(db.Integer)
    fin_year = db.Column(db.String(20), nullable=False)   
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)

class TempQues(db.Model):
    __bind_key__ = 'sql_kms'
    temp_id = db.Column(db.Integer, primary_key=True)
    alloc_id = db.Column(db.Integer)
    ques_id = db.Column(db.String(255), nullable=False)   
    status = db.Column(db.Integer)


class ExternalTraining(db.Model):
    __bind_key__ = 'sql_kms'
    ext_id = db.Column(db.Integer, primary_key=True)
    course_title = db.Column(db.Text)
    instructor = db.Column(db.Text)
    com_inst_name = db.Column(db.Text)
    ext_type = db.Column(db.String(20), nullable=False)  
    location = db.Column(db.String(200), nullable=False)   
    training_hours = db.Column(db.String(20), nullable=False)   
    course_stream = db.Column(db.Integer)
    course_module = db.Column(db.Integer)
    status = db.Column(db.Integer)
    training_date = db.Column(db.Date)
    description = db.Column(db.Text)
    material_upload = db.Column(db.Text)
    fin_year = db.Column(db.String(20), nullable=False)  
    created_by = db.Column(db.BigInteger)   
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)    


class ExternalTrainingUser(db.Model):
    __bind_key__ = 'sql_kms'
    extuser_id = db.Column(db.Integer, primary_key=True)
    ext_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    dept_id = db.Column(db.Integer)
    status = db.Column(db.Integer)
    training_hours = db.Column(db.String(20), nullable=False)   
    marks = db.Column(db.String(20))
    upload_file = db.Column(db.Text)
    fin_year = db.Column(db.String(20), nullable=False)   
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)     

class FeedbackQues(db.Model):
    __bind_key__ = 'sql_kms'
    ques_id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text)
    status = db.Column(db.Integer)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)      

class FeedbackAns(db.Model):
    __bind_key__ = 'sql_kms'
    ans_id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Integer)
    ans_name = db.Column(db.String(20))   

class FeedbackAllocation(db.Model):
    __bind_key__ = 'sql_kms'
    alloc_id = db.Column(db.Integer, primary_key=True)
    crse_strm_id = db.Column(db.Integer)
    module_id = db.Column(db.Integer)
    chapter_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    ques_id = db.Column(db.Integer)
    ans_id = db.Column(db.Integer)
    comments = db.Column(db.Text)
    fin_year = db.Column(db.String(20))  
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)     

class KmsType(db.Model):
    __bind_key__ = 'sql_kms'
    type_id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.Text)  
    new_user_status = db.Column(db.String(5))  
    trans_user_status = db.Column(db.String(5))  
    exam_yes_no = db.Column(db.String(5))  
    feedback_yes_no = db.Column(db.String(5))  
    existing_user_mod_alloc = db.Column(db.String(5)) 
    repeat_study = db.Column(db.String(5)) 
    status = db.Column(db.Integer)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)

class ExternalIndivAllocation(db.Model):
    __bind_key__ = 'sql_kms'
    alloc_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer) 
    module_id = db.Column(db.Integer)
    crse_strm_id = db.Column(db.Integer)
    fin_year = db.Column(db.String(20), nullable=False)  
    status = db.Column(db.Integer)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)

    
class UserViewDocumentReport(db.Model):
    __bind_key__ = 'sql_dms'
    report_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    document_structure_id = db.Column(db.Integer, nullable=False)
    document_rev_id = db.Column(db.Integer, nullable=False)
    rev_no = db.Column(db.String(255), nullable=False)
    view_count = db.Column(db.BigInteger, nullable=False)
    first_view_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    last_view_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    
class AgencyDetails(db.Model):
    __bind_key__ = 'sql_dsm'
    agency_id = db.Column(db.Integer, primary_key=True)
    agency_name = db.Column(db.String(255), nullable=False)    
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now()) 


class ManageCompCertifDetails(db.Model):
    __bind_key__ = 'sql_dsm'
    manage_id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer)
    sub_group_id = db.Column(db.Integer)
    sub_grouptwo_id = db.Column(db.Integer)
    certificate_id = db.Column(db.Integer)
    agency_id = db.Column(db.Integer) 
    del_cert = db.Column(db.Integer) 
    certif_no = db.Column(db.String(255), nullable=False)
    fees = db.Column(db.String(255), nullable=False)
    entry_date = db.Column(db.Date)
    bill_date = db.Column(db.Date)
    payment_date = db.Column(db.Date)
    validity = db.Column(db.Integer) 
    issue_date = db.Column(db.Date)
    valid_upto = db.Column(db.Date)
    notification_reminder = db.Column(db.Integer) 
    alert = db.Column(db.Integer) 
    description = db.Column(db.String(255))
    upload_file = db.Column(db.String(255))
    bill_no = db.Column(db.String(200))
    mail_status = db.Column(db.Integer) 
    status = db.Column(db.Integer, nullable=False)
    comments = db.Column(db.Text) 
    user_id = db.Column(db.Integer)
    agency_fees = db.Column(db.String(255))
    consulting_fees = db.Column(db.String(255))
    holder_name = db.Column(db.String(255))
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())       

class GroupLists(db.Model):
    __bind_key__ = 'sql_dsm'
    group_id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(255), nullable=False)    
    status = db.Column(db.Integer, nullable=False)
    sub_group_status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now()) 
    
class CertificateMasters(db.Model):
    __bind_key__ = 'sql_dsm'
    certif_id = db.Column(db.Integer, primary_key=True)
    scopes = db.Column(db.String(255))    
    group_id = db.Column(db.Integer, nullable=False)
    sub_group_id = db.Column(db.Integer)
    sub_grouptwo_id = db.Column(db.Integer)
    description = db.Column(db.String(255), nullable=False)
    alert_period = db.Column(db.Integer, nullable=False)  
    cont_record = db.Column(db.String(255), nullable=False)  
    cont_freq = db.Column(db.Integer, nullable=False)  
    cont_notif = db.Column(db.String(255), nullable=False)    
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())        
    
class DsmAlertIntervalList(db.Model):
    __bind_key__ = 'sql_dsm'
    dsm_renewal_alert_id = db.Column(db.Integer, primary_key=True)
    frequency = db.Column(db.String)
    alert = db.Column(db.String)
    notification = db.Column(db.String)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())    
    
class AuthUserAllocations(db.Model):
    __bind_key__ = 'sql_dsm'
    alloc_id = db.Column(db.Integer, primary_key=True)
    common_id = db.Column(db.Integer)
    group_id = db.Column(db.Integer)
    sub_group_id = db.Column(db.Integer)
    sub_grouptwo_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)    
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now()) 

class ApproverAllocations(db.Model):
    __bind_key__ = 'sql_dsm'
    alloc_id = db.Column(db.Integer, primary_key=True)
    common_id = db.Column(db.Integer)
    group_id = db.Column(db.Integer)
    sub_group_id = db.Column(db.Integer)
    sub_grouptwo_id = db.Column(db.Integer)
    certificate_id = db.Column(db.Integer)
    department_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)    
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())   

class SubGroupLists(db.Model):
    __bind_key__ = 'sql_dsm'
    sub_group_id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer)
    sub_group_name = db.Column(db.String(255), nullable=False)    
    status = db.Column(db.Integer, nullable=False)
    sub_grouptwo_status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now()) 

class SubGrouptwoLists(db.Model):
    __bind_key__ = 'sql_dsm'
    sub_grouptwo_id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer)
    sub_group_id = db.Column(db.Integer)
    sub_grouptwo_name = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())          

# SMS models

class SmsApproverAllocation(db.Model):
    __bind_key__ = 'sql_sms'
    alloc_id = db.Column(db.Integer, primary_key=True)
    common_id = db.Column(db.Integer)
    certificate_id = db.Column(db.Integer)
    v_type_id = db.Column(db.Integer)
    v_group_id = db.Column(db.Integer)
    v_ref_id = db.Column(db.Integer)
    department_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)    
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())  

class SmsCertificateMaster(db.Model):
    __bind_key__ = 'sql_sms'
    certif_id = db.Column(db.Integer, primary_key=True)
    v_type_id = db.Column(db.Integer, nullable=False)
    v_group_id = db.Column(db.Integer, nullable=False)
    v_reference = db.Column(db.Integer, nullable=False)
    certificate_name = db.Column(db.String(255), nullable=False)
    alert_period = db.Column(db.Integer, nullable=False)  
    cont_record = db.Column(db.String(255), nullable=False)  
    cont_freq = db.Column(db.Integer, nullable=False)  
    cont_notif = db.Column(db.String(255), nullable=False)    
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())  

class SmsManageEmpCertif(db.Model):
    __bind_key__ = 'sql_sms'
    manage_id = db.Column(db.Integer, primary_key=True)
    v_type_id = db.Column(db.Integer)
    v_group_id = db.Column(db.Integer)
    v_reference_id = db.Column(db.Integer)
    certificate_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)    
    company_id = db.Column(db.Integer) 
    mail_status = db.Column(db.Integer) 
    del_cert = db.Column(db.Integer) 
    certif_no = db.Column(db.String(255), nullable=False)
    comments = db.Column(db.Text) 
    upload_file = db.Column(db.String(255), nullable=False)
    issue_date = db.Column(db.Date)
    valid_upto = db.Column(db.Date)
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())     

class SmsManageEmpContinuity(db.Model):
    __bind_key__ = 'sql_sms'
    cont_id = db.Column(db.Integer, primary_key=True)
    certificate_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)    
    reviewed_by = db.Column(db.Integer)
    manage_id = db.Column(db.Integer)    
    upload_file = db.Column(db.String(255), nullable=False)
    schedule_date = db.Column(db.Date)
    actual_date = db.Column(db.Date)
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())   

# class Systemrole(db.Model):
#     __bind_key__ = 'sql_sms'
#     roleid = db.Column(db.Integer, primary_key=True)
#     rolename = db.Column(db.String(50), nullable=False)
    
# class Department(db.Model):
#     __bind_key__ = 'sql_sms'
#     department_id = db.Column(db.Integer, primary_key=True)
#     department_name = db.Column(db.String(50), nullable=False)
#     department_code = db.Column(db.String(15), nullable=False)
#     status = db.Column(db.Integer, nullable=False)
#     company_id = db.Column(db.Integer, db.ForeignKey('company.company_id'))
#     created_by = db.Column(db.BigInteger)
#     created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
#     updated_by = db.Column(db.BigInteger)
#     updated_date = db.Column(db.DateTime(timezone=True), default=func.now())


# class Roles(db.Model):
#     __bind_key__ = 'sql_sms'
#     role_id = db.Column(db.Integer, primary_key=True)
#     role_name = db.Column(db.String(50), nullable=False)
#     status = db.Column(db.Integer, nullable=False)
#     department_id = db.Column(db.Integer, db.ForeignKey('department.department_id'))
#     company_id = db.Column(db.Integer, db.ForeignKey('company.company_id'))
#     created_by = db.Column(db.BigInteger)
#     created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
#     updated_by = db.Column(db.BigInteger)
#     updated_date = db.Column(db.DateTime(timezone=True), default=func.now())

# class Users(db.Model):
#     __bind_key__ = 'sql_sms'
#     user_id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(100), unique=True)
#     email = db.Column(db.String(100), unique=True)
#     password_hash = db.Column(db.String(100), nullable=False)
#     role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id'))
#     department_id = db.Column(db.Integer, db.ForeignKey('department.department_id'))
#     employee_code = db.Column(db.String(100), nullable=False)
#     gender = db.Column(db.String(100), nullable=False)
#     personal_contact = db.Column(db.String(25), nullable=False)
#     first_name = db.Column(db.String(100), nullable=False)
#     last_name = db.Column(db.String(100), nullable=False)
#     blood_group = db.Column(db.String(100), nullable=False)
#     dob = db.Column(db.Date)
#     doj = db.Column(db.Date)
#     sys_role = db.Column(db.String(100), nullable=False)
#     country_id = db.Column(db.Integer, nullable=False)
#     state_id = db.Column(db.Integer, nullable=False)
#     city_id = db.Column(db.Integer, nullable=False)
#     location_id = db.Column(db.Integer, nullable=False)
#     company_id = db.Column(db.Integer, nullable=False)
#     filedata = db.Column(db.String(100), nullable=False)
#     type_of_user = db.Column(db.String(100), nullable=False)
#     initial_type_of_user = db.Column(db.String(100))
#     created_by = db.Column(db.BigInteger)
#     created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
#     updated_by = db.Column(db.BigInteger)
#     updated_date = db.Column(db.DateTime(timezone=True), default=func.now())
#     login_sys_role = db.Column(db.Integer)
#     phone_code = db.Column(db.Integer)
#     reporting_manager_id = db.Column(db.Integer)
#     old_emp_id = db.Column(db.Integer)
#     reassign_status = db.Column(db.Integer)
#     left_date = db.Column(db.Date)
#     status = db.Column(db.String(100), nullable=False)

class VendorCompany(db.Model):
    __bind_key__ = 'sql_sms'
    v_com_id = db.Column(db.Integer, primary_key=True)
    v_company_name = db.Column(db.String(255), nullable=False)    
    address = db.Column(db.Text, nullable=False)
    country_id = db.Column(db.Integer, nullable=False)
    state_id = db.Column(db.Integer, nullable=False)
    city_id = db.Column(db.Integer, nullable=False) 
    gst = db.Column(db.String(255), nullable=False)
    contact = db.Column(db.String(255), nullable=False) 
    email = db.Column(db.String(255), nullable=False)  
    phone = db.Column(db.String(255), nullable=False)    
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())

class VendorGroup(db.Model):
    __bind_key__ = 'sql_sms'
    vendor_group_id = db.Column(db.Integer, primary_key=True)
    vendor_type_id = db.Column(db.Integer, nullable=False)
    vendor_group_name = db.Column(db.String(255), nullable=False)   
    vendor_group_audit_req = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now()) 

class VendorReference(db.Model):
    __bind_key__ = 'sql_sms'
    vendor_reference_id = db.Column(db.Integer, primary_key=True)
    vendor_type_id = db.Column(db.Integer, nullable=False)
    vendor_reference_name = db.Column(db.String(255), nullable=False)    
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now()) 

class VendorType(db.Model):
    __bind_key__ = 'sql_sms'
    vendor_type_id = db.Column(db.Integer, primary_key=True)
    vendor_type_name = db.Column(db.String(255), nullable=False)    
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())

class VendorUserAllocation(db.Model):
    __bind_key__ = 'sql_sms'
    vendor_allocation_id = db.Column(db.Integer, primary_key=True)
    common_id = db.Column(db.Integer)
    vendor_type_id = db.Column(db.Integer)
    vendor_group_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)    
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now()) 

# class Country(db.Model):
#     __bind_key__ = 'sql_sms'
#     country_id = db.Column(db.Integer, primary_key=True)
#     country_name = db.Column(db.String(50), nullable=False)
#     country_code = db.Column(db.String(50), nullable=False)
#     phone_code = db.Column(db.Integer)
#     currency = db.Column(db.String(50))
#     currency_symbol = db.Column(db.String(50))
#     created_by = db.Column(db.BigInteger)
#     created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
#     updated_by = db.Column(db.BigInteger)
#     updated_date = db.Column(db.DateTime(timezone=True), default=func.now())

# class LocationList(db.Model):
#     __bind_key__ = 'sql_sms'
#     location_id = db.Column(db.Integer, primary_key=True)
#     company_id = db.Column(db.Integer, db.ForeignKey('company.company_id'))
#     location_name = db.Column(db.String(100), nullable=False)
#     country_id = db.Column(db.Integer, db.ForeignKey('country.country_id'))
#     state_id = db.Column(db.Integer, db.ForeignKey('state.state_id'))
#     city_id = db.Column(db.Integer, db.ForeignKey('city.city_id'))
#     created_by = db.Column(db.BigInteger)
#     created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
#     updated_by = db.Column(db.BigInteger)
#     updated_date = db.Column(db.DateTime(timezone=True), default=func.now())
#     phone_code = db.Column(db.String(15))
#     login_type = db.Column(db.Integer, nullable=False)

class SupplierCertificateDetails(db.Model):
    __bind_key__ = 'sql_sms'
    supplier_certificate_id = db.Column(db.Integer, primary_key=True)
    supplier_certificate_name = db.Column(db.String(255), nullable=False) 
    alert_period = db.Column(db.Integer, nullable=False)       
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now()) 

class VendorCertificateAllocation(db.Model):
    __bind_key__ = 'sql_sms'
    vendor_certificate_id = db.Column(db.Integer, primary_key=True)
    common_id = db.Column(db.Integer)
    vendor_type_id = db.Column(db.Integer)
    vendor_group_id = db.Column(db.Integer)
    certificatename_id = db.Column(db.Integer)    
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now()) 

class VendorSupplierCompany(db.Model):
    __bind_key__ = 'sql_sms'
    v_com_id = db.Column(db.Integer, primary_key=True)
    v_company_name = db.Column(db.String(255), nullable=False) 
    email = db.Column(db.String(255), nullable=False)
    erp_supplier_id = db.Column(db.String(255), nullable=False) 
    gst = db.Column(db.String(255), nullable=False)
    country_id = db.Column(db.Integer, nullable=False)   
    contact_name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.Text, nullable=False)   
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())
    certificate_yesno = db.Column(db.String(5))

class SupplierScopeMapping(db.Model):
    __bind_key__ = 'sql_sms'
    ss_map_id = db.Column(db.Integer, primary_key=True)
    v_sup_com_id = db.Column(db.Integer, nullable=False) 
    v_type_id = db.Column(db.Integer, nullable=False) 
    v_group_id = db.Column(db.Integer, nullable=False) 
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())

class SmsSupplierCertificateDetails(db.Model):
    __bind_key__ = 'sql_sms'
    certifcate_manage_id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer)
    v_type_id = db.Column(db.Integer)
    v_group_id = db.Column(db.Integer)
    certificate_id = db.Column(db.Integer)
    certif_no = db.Column(db.String(255), nullable=False)
    issue_date = db.Column(db.Date)
    valid_upto = db.Column(db.Date) 
    upload_file = db.Column(db.String(255), nullable=False)
    mail_status = db.Column(db.Integer) 
    del_cert = db.Column(db.Integer) 
    status = db.Column(db.Integer, nullable=False)
    total_upload = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())     

class SmsSupplierCertificateDetailsHistory(db.Model):
    __bind_key__ = 'sql_sms'
    certifcate__hist_manage_id = db.Column(db.Integer, primary_key=True)
    certifcate_manage_id = db.Column(db.Integer)
    supplier_id = db.Column(db.Integer)
    v_type_id = db.Column(db.Integer)
    v_group_id = db.Column(db.Integer)
    certificate_id = db.Column(db.Integer)
    certif_no = db.Column(db.String(255), nullable=False)
    issue_date = db.Column(db.Date)
    valid_upto = db.Column(db.Date) 
    upload_file = db.Column(db.String(255), nullable=False)
    mail_status = db.Column(db.Integer) 
    del_cert = db.Column(db.Integer) 
    status = db.Column(db.Integer, nullable=False)
    total_upload = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())     

class ProjectVendorDetailsList(db.Model):
    __bind_key__ = 'sql_sms'
    pro_ven_id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(255), nullable=False) 
    customer_name = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())    
    
class ProjectVendorList(db.Model):
    __bind_key__ = 'sql_sms'
    pro_ven_id_list = db.Column(db.Integer, primary_key=True)
    pro_ven_id = db.Column(db.Integer) 
    v_type_id = db.Column(db.Integer)
    v_group_id = db.Column(db.Integer)
    supplier_id = db.Column(db.Integer)
    certificate_id = db.Column(db.Integer)
    certifcate_manage_id = db.Column(db.Integer)
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())   
# End of sms table
 
     
class CamsGroupList(db.Model):
    __bind_key__ = 'sql_cams'
    group_id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(255), nullable=False)    
    short_code = db.Column(db.String(10), nullable=False) 
    status = db.Column(db.Integer, nullable=False)
    sub_group_status = db.Column(db.Integer, nullable=False)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    
    
class CamsSubGroup1(db.Model):
    __bind_key__ = 'sql_cams'
    sub_group_id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer)
    sub_group_name = db.Column(db.String(255), nullable=False)    
    grp1_short_code = db.Column(db.String(10))
    sub_group_auto_num = db.Column(db.String(20), nullable=False)
    status = db.Column(db.Integer, nullable=False)
    sub_grouptwo_status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now()) 

class CamsSubGroup2(db.Model):
    __bind_key__ = 'sql_cams'
    sub_grouptwo_id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer)
    sub_group_id = db.Column(db.Integer)
    sub_grouptwo_name = db.Column(db.String(255), nullable=False)
    grp2_short_code = db.Column(db.String(10))
    sub_group2_auto_num = db.Column(db.String(20), nullable=False)
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())              


class AssetList(db.Model):
    __bind_key__ = 'sql_cams'
    asset_id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer)
    sub_group_id = db.Column(db.Integer)
    sub_grouptwo_id = db.Column(db.Integer)
    asset_name = db.Column(db.String(255), nullable=False)
    asset_id_code = db.Column(db.String(50), nullable=False)
    asset_cost = db.Column(db.Integer)
    range_val = db.Column(db.Text)
    reference = db.Column(db.Text)
    tolerance = db.Column(db.Text)
    unit_of_measure = db.Column(db.Text)
    product_weight = db.Column(db.String(25))
    frequency = db.Column(db.String(25))
    alert_interval = db.Column(db.Integer)
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())              

class InstrumentList(db.Model):
    __bind_key__ = 'sql_cams'
    instrument_id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer)
    sub_group_id = db.Column(db.Integer)
    sub_grouptwo_id = db.Column(db.Integer)
    asset_id = db.Column(db.Integer, nullable=False)
    asset_id_code = db.Column(db.String(50), nullable=False)
    process_manager = db.Column(db.Text) 
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())              

class PlantMachineList(db.Model):
    __bind_key__ = 'sql_cams'
    plant_id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer)
    sub_group_id = db.Column(db.Integer)
    sub_grouptwo_id = db.Column(db.Integer)
    asset_id = db.Column(db.Integer, nullable=False)
    asset_id_code = db.Column(db.String(50), nullable=False)
    process_manager = db.Column(db.Text) 
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())              

class InstrumentAssetList(db.Model):
    __bind_key__ = 'sql_cams'
    instrument_assetid = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer)
    sub_group_id = db.Column(db.Integer)
    sub_grouptwo_id = db.Column(db.Integer)
    asset_id = db.Column(db.Integer, nullable=False)
    instrument_id = db.Column(db.Integer)
    asset_id_code = db.Column(db.String(50), nullable=False)
    frequency = db.Column(db.String(25))
    alert_interval = db.Column(db.Integer)
    system_current_id = db.Column(db.Integer, nullable=False)
    instrument_asset_idcode = db.Column(db.String(50), nullable=False)
    manufacture_make = db.Column(db.String(225), nullable=False)
    modal_number = db.Column(db.String(225), nullable=False)
    machine_serial_id = db.Column(db.String(225), nullable=False)
    supplier = db.Column(db.String(225), nullable=False)
    calib_scope = db.Column(db.String(50), nullable=False)
    # calib_scope_name = db.Column(db.String(50), nullable=False)
    calib_department = db.Column(db.String(225), nullable=False)
    agency =  db.Column(db.String(225), nullable=False)
    calibration_date = db.Column(db.Date)
    calib_due_date = db.Column(db.Date)
    process_manager = db.Column(db.Text) 
    upload_certificate = db.Column(db.String(255))
    plant_machine_id = db.Column(db.Integer)
    service_status = db.Column(db.String(255))
    service_registered = db.Column(db.String(255))
    service_supplier = db.Column(db.String(255))
    service_disposition = db.Column(db.String(255))
    service_cost = db.Column(db.Integer)
    final_status = db.Column(db.String(255))
    mail_status = db.Column(db.Integer) 
    entry_status = db.Column(db.Integer)
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())              

class PlantMachineAssetList(db.Model):
    __bind_key__ = 'sql_cams'
    plant_machine_assetid = db.Column(db.Integer, primary_key=True)
    plant_group_id = db.Column(db.Integer)
    plant_sub_group_id = db.Column(db.Integer)
    plant_sub_grouptwo_id = db.Column(db.Integer)
    plant_asset_id = db.Column(db.Integer)
    plant_id = db.Column(db.Integer)
    plant_asset_id_code = db.Column(db.String(50), nullable=False)
    plant_frequency = db.Column(db.String(25))
    plant_alert_interval = db.Column(db.Integer)
    plant_system_current_id = db.Column(db.Integer, nullable=False)
    plant_instrument_asset_idcode = db.Column(db.String(50), nullable=False) 
    plant_manufacture_make = db.Column(db.String(225), nullable=False)
    plant_machine_serial_id = db.Column(db.String(225), nullable=False)
    plant_supplier = db.Column(db.String(225), nullable=False)
    plant_calib_scope = db.Column(db.String(50), nullable=False)
    # calib_scope_name = db.Column(db.String(50), nullable=False)
    plant_calib_department = db.Column(db.String(225), nullable=False)
    plant_agency =  db.Column(db.String(225), nullable=False)
    plant_calibration_date = db.Column(db.Date)
    plant_calib_due_date = db.Column(db.Date)
    plant_process_manager = db.Column(db.Text) 
    plant_upload_certificate = db.Column(db.String(255))
    plant_model_number = db.Column(db.String(255))
    instrument_ids = db.Column(db.Text)
    plant_status = db.Column(db.Integer, nullable=False)
    plant_service_status = db.Column(db.String(255))
    plant_service_registered = db.Column(db.String(255))
    plant_service_supplier = db.Column(db.String(255))
    plant_service_disposition = db.Column(db.String(255))
    plant_service_cost = db.Column(db.Integer)
    plant_final_status = db.Column(db.String(255))
    mail_status = db.Column(db.Integer) 
    entry_status = db.Column(db.Integer)
    status = db.Column(db.Integer)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())              

class CamsServiceOrderEmail(db.Model):
    __bind_key__ = 'sql_cams'
    service_order_id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer)
    sub_group_id = db.Column(db.Integer)
    sub_grouptwo_id = db.Column(db.Integer)
    asset_id  = db.Column(db.Integer)
    instrument_id = db.Column(db.Integer)
    plant_machine_id = db.Column(db.Integer)
    emails =  db.Column(db.Text)
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())              

class FrequencyAlertIntervalList(db.Model):
    __bind_key__ = 'sql_cams'
    renewal_alert_id = db.Column(db.Integer, primary_key=True)
    frequency = db.Column(db.String)
    alert = db.Column(db.String)
    notification = db.Column(db.String)
    no_of_days = db.Column(db.Integer)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())

class MachineMake(db.Model):
    __bind_key__ = 'sql_cams'
    machine_make_id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer)
    sub_group_id = db.Column(db.Integer)
    sub_grouptwo_id = db.Column(db.Integer)
    instrument_asset_id = db.Column(db.BigInteger)
    plant_asset_id = db.Column(db.BigInteger)
    machine_make_name =  db.Column(db.String(225), nullable=False)
    status = db.Column(db.Integer)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    
class MachineSupplier(db.Model):
    __bind_key__ = 'sql_cams'
    machine_supplier_id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer)
    sub_group_id = db.Column(db.Integer)
    sub_grouptwo_id = db.Column(db.Integer)
    instrument_asset_id = db.Column(db.Integer)
    plant_asset_id = db.Column(db.Integer)
    machine_serial_id = db.Column(db.String(225), nullable=False)
    machine_supplier_name =  db.Column(db.String(225), nullable=False)
    status = db.Column(db.Integer)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
        
class AssetScopes(db.Model):
    __bind_key__ = 'sql_cams'
    asset_scopes_id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer)
    sub_group_id = db.Column(db.Integer)
    sub_grouptwo_id = db.Column(db.Integer)
    instrument_asset_id = db.Column(db.Integer)
    plant_asset_id = db.Column(db.Integer)
    machine_serial_id = db.Column(db.String(225), nullable=False)
    asset_scope_name =  db.Column(db.String(225), nullable=False)
    status = db.Column(db.Integer)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)

class CalibAgency(db.Model):
    __bind_key__ = 'sql_cams'
    asset_agency_id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer)
    sub_group_id = db.Column(db.Integer)
    sub_grouptwo_id = db.Column(db.Integer)
    asset_id = db.Column(db.Integer)
    asset_agency_name =  db.Column(db.String(225), nullable=False)
    address = db.Column(db.Text, nullable=False)
    gst = db.Column(db.String(255), nullable=False)
    contact_name = db.Column(db.String(255), nullable=False) 
    email = db.Column(db.String(255), nullable=False)  
    phone = db.Column(db.String(255), nullable=False)    
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)

class AgencyAllocation(db.Model):
    __bind_key__ = 'sql_cams'
    alloc_id  = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer)
    sub_group_id = db.Column(db.Integer)
    sub_grouptwo_id = db.Column(db.Integer)
    asset_id = db.Column(db.Integer)
    agency_id = db.Column(db.Integer)
    status = db.Column(db.Integer, nullable=False)
    created_by  = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by  = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)

class CalibDepartment(db.Model):
    __bind_key__ = 'sql_cams'
    asset_dep_id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer)
    sub_group_id = db.Column(db.Integer)
    sub_grouptwo_id = db.Column(db.Integer)
    instrument_asset_id = db.Column(db.Integer)
    plant_asset_id = db.Column(db.Integer)
    asset_department_name =  db.Column(db.String(225), nullable=False)
    status = db.Column(db.Integer)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)

class ProcessManagerAllocations(db.Model):
    __bind_key__ = 'sql_cams'
    process_manager_id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer)
    sub_group_id = db.Column(db.Integer)
    sub_grouptwo_id = db.Column(db.Integer)
    asset_id = db.Column(db.Integer)
    instrument_asset_id = db.Column(db.Integer)
    plant_asset_id = db.Column(db.Integer)
    user_id =  db.Column(db.Integer)
    status = db.Column(db.Integer)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)


class CapaNcType(db.Model):
    __bind_key__ = 'sql_capa'
    nc_type_id = db.Column(db.Integer, primary_key=True)
    nc_typename = db.Column(db.String(255), nullable=False)
    nc_typecode = db.Column(db.String(255), nullable=False)
    status =  db.Column(db.Integer, nullable=False)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())
    created_by = db.Column(db.BigInteger)



class CapaWorkFlowType(db.Model):
    __bind_key__ = 'sql_capa'
    wf_type_id = db.Column(db.Integer, primary_key=True)
    wf_typename = db.Column(db.String(255), nullable=False)
    wf_typecode = db.Column(db.String(255), nullable=False)
    status =  db.Column(db.Integer, nullable=False)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())
    created_by = db.Column(db.BigInteger)



class NcRiskLevelName(db.Model):
    __bind_key__ = 'sql_capa'
    nc_risk_id = db.Column(db.Integer, primary_key=True)
    nc_riskname = db.Column(db.String(255), nullable=False)
    status =  db.Column(db.Integer, nullable=False)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())
    created_by = db.Column(db.BigInteger)

class NcRiskLevel(db.Model):
    __bind_key__ = 'sql_capa'
    nc_riskid = db.Column(db.Integer, primary_key=True)
    nc_riskname_id = db.Column(db.Integer, nullable=False)
    nc_risk_number = db.Column(db.Integer, nullable=False)
    nc_risk_value = db.Column(db.String(255), nullable=False)
    status =  db.Column(db.Integer, nullable=False)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())
    created_by = db.Column(db.BigInteger)

class NcDummySetup(db.Model):
    __bind_key__ = 'sql_capa'
    dum_id = db.Column(db.Integer, primary_key=True)
    nctype_id = db.Column(db.Integer)
    wftype_id = db.Column(db.Integer)
    ncauth = db.Column(db.Text)
    vfauth = db.Column(db.Text)
    dep = db.Column(db.Text)
    dep_res = db.Column(db.Text)
    risk_level = db.Column(db.Text)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())
    created_by = db.Column(db.BigInteger)


class NcSetup(db.Model):
    __bind_key__ = 'sql_capa'
    nc_setup_id = db.Column(db.Integer, primary_key=True)
    nctype_id = db.Column(db.Integer)
    wftype_id = db.Column(db.Integer)
    ncauth = db.Column(db.Text)
    vfauth = db.Column(db.Text)
    dep = db.Column(db.Text)
    dep_res = db.Column(db.Text)
    risk_level_id = db.Column(db.Integer)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())
    created_by = db.Column(db.BigInteger)


class NcAuthUserAllocations(db.Model):
    __bind_key__ = 'sql_capa'
    alloc_id = db.Column(db.Integer, primary_key=True)
    nctype_id = db.Column(db.Integer)
    nc_setup_id = db.Column(db.Integer)
    user_type_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)    
    status = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())         


class NCList(db.Model):
    __bind_key__ = 'sql_capa'
    nc_id = db.Column(db.Integer, primary_key=True)
    nc_typeid = db.Column(db.Integer)
    nc_risklevel_id = db.Column(db.Integer)
    nc_description = db.Column(db.Text)
    nc_customer = db.Column(db.String(225))
    nc_upload_file = db.Column(db.Text)
    status =  db.Column(db.Integer, nullable=False)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())
    created_by = db.Column(db.BigInteger)
    


class NCActionList(db.Model):
    __bind_key__ = 'sql_capa'
    action_id = db.Column(db.Integer, primary_key=True)
    nctype_id = db.Column(db.Integer)
    nc_id = db.Column(db.Integer)
    root_cause_comments = db.Column(db.Text)
    root_cause_evidence = db.Column(db.Text)
    co_action_comments = db.Column(db.Text)
    co_action_evidence = db.Column(db.Text)
    review_rc_comments = db.Column(db.Text)
    review_rc_evidence = db.Column(db.Text)
    review_ca_comments = db.Column(db.Text)
    review_ca_evidence = db.Column(db.Text)
    status = db.Column(db.Integer)
    action_status = db.Column(db.Integer)
    review_status = db.Column(db.Integer)
    verify_status = db.Column(db.Integer)
    verification_req = db.Column(db.Integer)
    action_by = db.Column(db.Integer)
    review_by = db.Column(db.Integer)
    verify_by = db.Column(db.Integer)
    verify_nc = db.Column(db.Integer)
    created_by = db.Column(db.BigInteger)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    updated_by = db.Column(db.BigInteger)
    updated_date = db.Column(db.DateTime(timezone=True), default=func.now())

    

                   