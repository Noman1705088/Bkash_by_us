from django.db import models
from datetime import date
from django.shortcuts import render, HttpResponse, redirect
# Create your models here.
from dashboard.models import execute_sql, USERS, hash_the_password


class UserProfile:
    def __init__(self, id):
        self.id = id

    def getProfile(self):
        sql = 'SELECT USER_NAME,USER_PHOTO,USER_MOBILE_NO FROM USERS WHERE USER_ID =: id'
        ans = execute_sql(sql, [self.id], False, True)[0]
        context = {'NAME': ans[0], 'PHOTO': 'media\\'+ans[1], 'MOBILE': ans[2]}

        return context


class AdminProfile:
    def __init__(self, id):
        self.id = id

    def getProfile(self):
        sql = 'SELECT ADMIN_NAME FROM ADMIN WHERE ADMIN_ID=: id'
        ans = execute_sql(sql, [self.id], False, True)[0]
        name = ans[0]

        sql = 'SELECT USER_NAME,USER_NID,USER_MOBILE_NO,USER_ID FROM USERS U JOIN CUSTOMER C\
             ON U.USER_ID=C.CUSTOMER_ID WHERE APPROVED_BY IS NULL'
        customer = execute_sql(sql, [], False, True)
        cont_cust = customer
        i = 0
        for x in customer:
            cont_cust[i] = {'cust_name': x[0], 'cust_nid': x[1], 'cust_mobile': x[2], 'cust_post': 'CUST'+str(x[3]),
                            'cust_val': x[3]}
            i = i+1

        sql = 'SELECT USER_NAME,USER_NID,USER_MOBILE_NO,AGENT_BANK_AC,USER_ID FROM USERS U JOIN AGENT A\
             ON U.USER_ID=A.AGENT_ID WHERE APPROVED_BY IS NULL'
        agent = execute_sql(sql, [], False, True)
        cont_agent = agent
        i = 0
        for x in agent:
            cont_agent[i] = {'agent_name': x[0], 'agent_nid': x[1], 'agent_mobile': x[2],
                             'agent_bank_ac': x[3], 'agent_post': 'AGENT'+str(x[4]), 'agent_val': x[4]}
            i = i+1

        sql = 'SELECT ADMIN_NAME,ADMIN_ID FROM ADMIN WHERE APPROVED_BY IS NULL'
        admin = execute_sql(sql, [], False, True)
        cont_admin = admin
        i = 0
        for x in admin:
            cont_admin[i] = {'admin_name': x[0], 'admin_post': 'ADMIN'+str(x[1]),
                             'admin_val': x[1]}
            i = i+1

        sql = 'SELECT MERCHANT_NAME,MERCHANT_ID,TRADE_LICENSE_NO,HEAD_OFFICE_LOCATION FROM MERCHANTS WHERE APPROVED_BY IS NULL'
        merchant = execute_sql(sql, [], False, True)
        cont_merchant = merchant
        i = 0
        for x in merchant:
            cont_merchant[i] = {'merchant_name': x[0], 'merchant_post': 'MERCHANT'+str(x[1]),
                                'merchant_val': x[1], 'trade_license_no': x[2], 'head_office_loc': x[3]}
            i = i+1

        sql='SELECT SERVICE_PHOTO,SERVICE_NAME,SERVICE_TYPE,SERVICE_BANK_AC_NO,\
            SERVICE_ID FROM UTILITY_SERVICE WHERE APPROVED_BY IS NULL'
        service = execute_sql(sql,[],False,True)
        cont_service = service
        i=0
        for x in service:
            cont_service[i] = {'service_photo':x[0],'service_name':x[1],'service_type':x[2]\
                ,'service_bank_ac':x[3],'service_post':'SERVICE'+str(x[4]),'service_val':x[4]}
            i=i+1

        context = {'NAME': name, 'CUSTOMER': cont_cust,
                   'AGENT': cont_agent, 'ADMIN': cont_admin, 'MERCHANT': cont_merchant, 'SERVICE':cont_service}

        return context


class MerchantProfile:
    def __init__(self, id):
        self.merchantid = id
        sql = 'SELECT MERCHANT_NAME,MERCHANT_LOGO_IMAGE,TRADE_LICENSE_NO,HEAD_OFFICE_LOCATION,OFFER_ID FROM MERCHANTS WHERE MERCHANT_ID =: merchantid'
        ans = execute_sql(sql, [self.merchantid], False, True)[0]
        self.merchantName = ans[0]
        self.img = ans[1]
        self.trade_license = ans[2]
        self.head_office = ans[3]
        if not ans[4]:
            self.offer_percent = 0;
        else :
            offer_id = ans[4]
            sql = 'SELECT DISCOUNT_PERCENT FROM OFFERS WHERE OFFER_ID =: offer_id';
            self.offer_percent = execute_sql(sql,[offer_id],False,True)[0][0]



    def getProfile(self):
        sql = 'SELECT BRANCH_NAME,BRANCH_MOBILE_NO,MERCHANT_BRANCH_BALANCE FROM BRANCH WHERE BRANCH_MERCHANT_ID =: merchant_id'
        list = [self.merchantid]
        branch = execute_sql(sql, list, False, True)
        cont_branch = branch
        i = 0
        for x in branch:
            cont_branch[i] = {'branch_name': x[0],
                              'branch_mobile_no': x[1], 'branch_balance': x[2]}
            i = i+1
        context = {'NAME': self.merchantName, 'PHOTO': '..\media\\'+self.img,
                   'TRADE_LICENSE_NO': self.trade_license, 'HEAD_OFFICE_LOCATION': self.head_office, 'BRANCH': cont_branch,'OFFER_PERCENT':self.offer_percent}
        return context


class Branch:
    def __init__(self, branch_name, branch_mobile_no, branch_merchant_id):
        # super.__init__(id)
        if not execute_sql('select max(BRANCH_ID) from BRANCH', [], False, True)[0][0]:
            self.branch_id = 1
        else:
            self.branch_id = int(execute_sql(
                'select max(BRANCH_ID) from BRANCH', [], False, True)[0][0]) + 1
        self.branchname = branch_name
        self.mobile_no = branch_mobile_no
        self.balance = 0
        self.branch_merchant_id = branch_merchant_id

    def is_a_new_branch(self):
        sql1 = 'select count(*) from BRANCH where BRANCH_MOBILE_NO=:mobile_no'
        sql2 = 'select count(*) from USERS  where USER_MOBILE_NO=:mobile_no'
        sql3 = 'select count(*) from BRANCH where BRANCH_MERCHANT_ID=:merchant_id and BRANCH_NAME=:branch_name'
        list1 = [self.mobile_no]
        list2 = [self.mobile_no]
        list3 = [self.branch_merchant_id, self.branchname]
        if execute_sql(sql1, list1, False, True)[0][0] == 0 and execute_sql(sql2, list2, False, True)[0][0] == 0 and execute_sql(sql3, list3, False, True)[0][0] == 0:
            return True
        else:
            return False

    def insert(self):
        sql = 'INSERT INTO BRANCH VALUES(:branch_id,:branch_name,:branch_mobile_no,:balance,:branch_merchant_id)'
        list = [self.branch_id, self.branchname, self.mobile_no,
                self.balance, self.branch_merchant_id]
        execute_sql(sql, list, True, False)


class UpdateUser:
    def __init__(self, id):
        self.id = id
        sql = 'SELECT USER_ID,USER_NAME,USER_PHOTO,USER_FATHER_NAME\
        ,USER_MOTHER_NAME,USER_GENDER,USER_DOB,USER_NID,USER_MOBILE_NO,USER_PASSWORD \
        FROM USERS WHERE USER_ID=:id'
        ans = execute_sql(sql, [self.id], False, True)[0]
        self.img = ans[2]
        self.username = ans[1]
        self.father_name = ans[3]
        self.mother_name = ans[4]
        self.gender = ans[5]
        self.dob = ans[6]
        self.nid_no = ans[7]
        self.mobile_no = ans[8]
        self.password = ans[9]

    def showForUpdate(self):
        return {'PHOTO': '..\media\\'+self.img, 'NAME': self.username, 'MOTHER': self.mother_name,
                'FATHER': self.father_name, 'GENDER': self.gender, 'DOB': self.dob,
                'NID': self.nid_no, 'MOBILE': self.mobile_no}

    def update(self, username, father_name, mother_name, gender, dob, nid, mobile, Password):
        if username:
            self.username = username
        if father_name:
            self.father_name = father_name
        if mother_name:
            self.mother_name = mother_name
        if Password:
            self.password = hash_the_password(Password)
        if gender:
            self.gender = gender
        if dob:
            self.dob = date.fromisoformat(dob)
        if nid:
            self.nid_no = nid
        if mobile:
            self.mobile_no = mobile

        sql = 'UPDATE USERS\
        SET USER_NAME=:username,USER_FATHER_NAME=:father_name,USER_MOTHER_NAME=:mother_name,USER_PASSWORD=:password\
            ,USER_GENDER=:gender,USER_DOB=:dob,USER_NID=:nid,USER_MOBILE_NO=:mobile\
            WHERE USER_ID=:id'

        list = [self.username, self.father_name, self.mother_name, self.password, self.gender, self.dob,
                self.nid_no, self.mobile_no, self.id]
        execute_sql(sql, list, True, False)

        resp = redirect('home:home')
        resp.set_cookie('NAME', str(self.username))
        resp.set_cookie('MOBILE', str(self.mobile_no))
        return resp

class Offer:
    def __init__(self,discount_percentage):

        sql = 'SELECT OFFER_ID FROM OFFERS WHERE DISCOUNT_PERCENT =: discount_percent'
        list = [discount_percentage]
        if not execute_sql(sql,list,False,True):
            if not execute_sql('select max(OFFER_ID) from OFFERS', [], False, True)[0][0]:
                self.offer_id = 1
            else:
                self.offer_id = int(execute_sql(
                    'select max(OFFER_ID) from OFFERS', [], False, True)[0][0]) + 1
            self.discount_percent = discount_percentage

            sql_insert = 'INSERT INTO OFFERS VALUES(:offer_id,:discount_percent)'
            execute_sql(sql_insert,[self.offer_id,self.discount_percent],True,False)
        
        else :
            self.offer_id = execute_sql(
                                'SELECT OFFER_ID FROM OFFERS WHERE DISCOUNT_PERCENT =: discount_percent',[discount_percentage],False,True)[0][0]
            self.discount_percent = discount_percentage
    
    def getOfferId(self):
        return self.offer_id
