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

    def id(self):
        return self.id

