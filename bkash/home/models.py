from django.db import models

# Create your models here.
from dashboard.models import execute_sql,USERS,hash_the_password

class UserProfile:
    def __init__(self,id):
        self.id = id

    def getProfile(self):
        sql = 'SELECT USER_NAME,USER_PHOTO,USER_MOBILE_NO FROM USERS WHERE USER_ID =: id'
        ans = execute_sql(sql,[self.id],False,True)[0]
        context = {'NAME':ans[0],'PHOTO':'media\\'+ans[1],'MOBILE':ans[2]}

        return context

class UpdateUser:
    def __init__(self,id):
        self.id = id
        sql = 'SELECT USER_ID,USER_NAME,USER_PHOTO,USER_FATHER_NAME\
        ,USER_MOTHER_NAME,USER_GENDER,USER_DOB,USER_NID,USER_MOBILE_NO,USER_PASSWORD \
        FROM USERS WHERE USER_ID=:id'
        ans = execute_sql(sql,[self.id],False,True)[0]
        self.img = ans[2]
        self.username= ans[1]
        self.father_name = ans[3]
        self.mother_name = ans[4]
        self.gender = ans[5]
        self.dob = ans[6]
        self.nid_no = ans[7]
        self.mobile_no = ans[8]
        self.password = ans[9]

    def showForUpdate(self):
        return {'PHOTO':'..\media\\'+self.img,'NAME':self.username,'MOTHER':self.mother_name,'FATHER':self.mother_name}

    def update(self,img,username,father_name,mother_name,Password):
        if img:
            self.img=img
        if username:
            self.username=username
        if father_name:
            self.father_name=father_name
        if mother_name:
            self.mother_name=mother_name
        if Password:
            self.password= hash_the_password(password)

        sql = 'UPDATE USERS\
        SET USER_NAME=:username,USER_FATHER_NAME=:father_name,USER_MOTHER_NAME=:mother_name,USER_PASSWORD=:password\
        WHERE USER_ID=:id'

        list = [self.username,self.img,self.father_name,self.mother_name,self.password]
        execute_sql(sql,list,True,False)


        
