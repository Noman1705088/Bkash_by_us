from django.db import models
import cx_Oracle as db
from datetime import date
# Create your models here.

def execute_sql(sql,list,commit,is_select_st):
    try:
        with db.connect(        
            user = 'bkash_db',
            password = '123',
            dsn = 'localhost/orcl',
            encoding = 'UTF-8') as connection:
            with connection.cursor() as cursor:
                if list:
                    cursor.execute(sql,list)
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
    def __init__(self,img,username,father_name,mother_name,gender,dob,nid_no,mobile_no,Password):
        self.img = img
        self.username = username
        self.father_name = father_name
        self.mother_name = mother_name
        self.gender = gender
        self.dob = dob
        self.nid_no = nid_no
        self.mobile_no = mobile_no
        self.password = Password
        self.id = int(execute_sql('select max(user_id) from users',[],False,True)[0][0]) + 1

    def insert(self):
        sql = 'INSERT INTO USERS VALUES(:id,:username,:img,:fater,:mother,:gender,:dob,\
        :nid_no,:mobile_no,:password)'
        list = [self.id,self.username,self.img,self.father_name,self.mother_name,self.gender,date.fromisoformat(self.dob),\
            self.nid_no,self.mobile_no,self.password]
        execute_sql(sql,list,True,False)

    def is_a_new_user(self):
        sql1 = 'select count(*) from users where USER_MOBILE_NO=:mobile_no'
        sql2 = 'select count(*) from users where USER_NID=:nid'
        list1 = [self.mobile_no]
        list2 = [self.nid_no]
        if execute_sql(sql1,list1,False,True)[0][0] == 0 and execute_sql(sql2,list2,False,True)[0][0] == 0:
            return True
        else:
            return False

    def id(self):
        return self.id


class Login:
    def __init__(self,mobile_no,Password):
        self.mobile_no=mobile_no
        self.password=Password

    def is_valid_user(self):
        sql= 'select USER_PASSWORD from users where USER_MOBILE_NO=:mobile'
        list= [self.mobile_no]

        if not execute_sql(sql,list,False,True):
            return False
        elif execute_sql(sql,list,False,True)[0][0] == self.password:
            return True
        else:
            return False

    def user_id(self,logged_in):
        sql= 'select USER_ID from users where USER_MOBILE_NO=:mobile'
        list= [self.mobile_no]

        return execute_sql(sql,list,False,True)[0][0]
