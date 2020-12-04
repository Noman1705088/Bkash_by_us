from django.db import models
import cx_Oracle as db
from datetime import date
import hashlib
import os


def hash_the_password(password):
    salt = b''
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return str(key)


# Create your models here.

def execute_sql(sql, list, commit, is_select_st):
    try:
        with db.connect(
                user='bkash_db',
                password='123',
                dsn='localhost/orcl',
                encoding='UTF-8') as connection:
            with connection.cursor() as cursor:
                if list:
                    cursor.execute(sql, list)
                else:
                    cursor.execute(sql)

                if commit:
                    connection.commit()

                if is_select_st:
                    row = cursor.fetchall()
                    return row

    except db.Error as error:
        print(error)


class USERS:
    def __init__(self, img, username, father_name, mother_name, gender, dob, nid_no, mobile_no, Password):
        self.img = img
        self.username = username
        self.father_name = father_name
        self.mother_name = mother_name
        self.gender = gender
        self.dob = dob
        self.nid_no = nid_no
        self.mobile_no = mobile_no
        self.password = hash_the_password(Password)
        if not execute_sql('select max(user_id) from users', [], False, True)[0][0]:
            self.id = 1
        else:
            self.id = int(execute_sql(
                'select max(user_id) from users', [], False, True)[0][0]) + 1

    def insert(self):
        sql = 'INSERT INTO USERS VALUES(:id,:username,:img,:fater,:mother,:gender,:dob,\
        :nid_no,:mobile_no,:password)'
        list = [self.id, self.username, self.img, self.father_name, self.mother_name, self.gender, date.fromisoformat(self.dob),
                self.nid_no, self.mobile_no, self.password]
        execute_sql(sql, list, True, False)

    def is_a_new_user(self):
        sql1 = 'select count(*) from users where USER_MOBILE_NO=:mobile_no'
        sql2 = 'select count(*) from users where USER_NID=:nid'
        list1 = [self.mobile_no]
        list2 = [self.nid_no]
        if execute_sql(sql1, list1, False, True)[0][0] == 0 and execute_sql(sql2, list2, False, True)[0][0] == 0:
            return True
        else:
            return False

    def id(self):
        return self.id


class Agent:
    def __init__(self, AGENT_ID, AGENT_BANK_AC, AGENT_BALANCE):
        self.agent_id = AGENT_ID
        self.agent_bank_ac = AGENT_BANK_AC
        self.agent_balance = AGENT_BALANCE

    def insert(self):
        sql = 'INSERT INTO AGENT VALUES(:id,:agent_bank_ac,:agent_balance,:approved_by)'
        list = [self.agent_id, self.agent_bank_ac, self.agent_balance, None]
        execute_sql(sql, list, True, False)


class Customer:
    def __init__(self, cust_id, cust_balance):
        self.customer_id = cust_id
        self.customer_balance = cust_balance

    def insert(self):
        sql = 'INSERT INTO CUSTOMER VALUES(:id,:customer_balance,:approved_by)'
        list = [self.customer_id, self.customer_balance, None]
        execute_sql(sql, list, True, False)


class Login:
    def __init__(self, mobile_no, Password):
        self.id = id
        self.mobile_no = mobile_no
        self.password = Password

    def user_id(self):
        sql = 'select USER_ID from users where USER_MOBILE_NO=:mobile'
        list = [self.mobile_no]

        return execute_sql(sql, list, False, True)[0][0]


class LoginCustomer(Login):
    def __init__(self, mobile_no, Password):
        super().__init__(mobile_no, Password)

    def is_valid_user(self):
        sql = 'SELECT USER_PASSWORD FROM USERS U JOIN CUSTOMER C ON U.USER_ID=C.CUSTOMER_ID WHERE USER_MOBILE_NO=:mobile\
            AND APPROVED_BY IS NOT NULL'
        list = [self.mobile_no]

        if not execute_sql(sql, list, False, True):
            return False
        elif execute_sql(sql, list, False, True)[0][0] == hash_the_password(self.password):
            return True
        else:
            return False


class LoginAgent(Login):
    def __init__(self, mobile_no, Password):
        super().__init__(mobile_no, Password)

    def is_valid_user(self):
        sql = 'SELECT USER_PASSWORD FROM USERS U JOIN AGENT A ON U.USER_ID=A.AGENT_ID WHERE USER_MOBILE_NO=:mobile\
            AND APPROVED_BY IS NOT NULL'
        list = [self.mobile_no]

        if not execute_sql(sql, list, False, True):
            return False
        elif execute_sql(sql, list, False, True)[0][0] == hash_the_password(self.password):
            return True
        else:
            return False


class Admin:
    def __init__(self, name, Password):
        if not execute_sql('select max(admin_id) from admin', [], False, True)[0][0]:
            self.id = 1
        else:
            self.id = int(execute_sql(
                'select max(admin_id) from admin', [], False, True)[0][0]) + 1
        self.name = name
        self.password = hash_the_password(Password)

    def insert(self):
        sql = 'INSERT INTO ADMIN VALUES(:id,:name,:pass,:approved_by)'
        list = [self.id, self.name, self.password, None]
        execute_sql(sql, list, True, False)

    def uniqueName(self):
        sql = 'SELECT ADMIN_NAME FROM ADMIN WHERE ADMIN_NAME=:name'
        list = [self.name]
        if not execute_sql(sql, list, False, True):
            return True
        else:
            return False


class LoginAdmin:
    def __init__(self, name, Password):
        self.name = name
        self.password = Password

    def is_valid_user(self):
        sql = 'SELECT ADMIN_PASSWORD FROM ADMIN WHERE APPROVED_BY IS NOT NULL AND ADMIN_NAME=:name'
        list = [self.name]

        if not execute_sql(sql, list, False, True):
            return False
        elif execute_sql(sql, list, False, True)[0][0] == hash_the_password(self.password):
            return True
        else:
            return False

    def user_id(self):
        sql = 'select ADMIN_ID from ADMIN where ADMIN_NAME=:name'
        list = [self.name]

        return execute_sql(sql, list, False, True)[0][0]


class Merchant:
    def __init__(self, merchant_id,image, name,trade_license,head_office,Password):
        self.id = merchant_id
        self.img = image
        self.name = name
        self.trade_license = trade_license
        self.head_office_loc = head_office
        self.password = hash_the_password(Password)

    def insert(self):
        sql = 'INSERT INTO MERCHANTS(MERCHANT_ID,MERCHANT_NAME,MERCHANT_LOGO_IMAGE,TRADE_LICENSE_NO,HEAD_OFFICE_LOCATION,MERCHANT_PASSWORD,OFFER_ID,APPROVED_BY) VALUES (:id,:name,:img,:trade_license,:head_office,:password,:offer_id,:approved_by)'
        list = [self.id, self.name, self.img,self.trade_license,self.head_office_loc,self.password, None, None]
        execute_sql(sql, list, True, False)

    def uniqueMerchantName(self):
        sql = 'SELECT MERCHANT_NAME FROM MERCHANTS WHERE MERCHANT_NAME=:name'
        list = [self.name]
        if not execute_sql(sql, list, False, True):
            return True
        else:
            return False


class LoginMerchant:
    def __init__(self,name,Password):
        self.name = name
        self.password = Password
    
    def is_a_valid_Merchant(self):
        sql = 'SELECT MERCHANT_PASSWORD FROM MERCHANTS WHERE APPROVED_BY IS NOT NULL AND MERCHANT_NAME=:name'
        list = [self.name]

        if not execute_sql(sql, list, False, True):
            return False
        elif execute_sql(sql, list, False, True)[0][0] == hash_the_password(self.password):
            return True
        else:
            return False
    
    def merchant_id(self):
        sql = 'select MERCHANT_ID from MERCHANTS where MERCHANT_NAME=:name'
        list = [self.name]

        return execute_sql(sql, list, False, True)[0][0]