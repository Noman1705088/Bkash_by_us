from django.db import models
from datetime import date
from django.shortcuts import render, HttpResponse, redirect
# Create your models here.
from dashboard.models import execute_sql, USERS, hash_the_password, execute_sql_func


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

        sql = 'SELECT SERVICE_PHOTO,SERVICE_NAME,SERVICE_TYPE,SERVICE_BANK_AC_NO,\
            SERVICE_ID FROM UTILITY_SERVICE WHERE APPROVED_BY IS NULL'
        service = execute_sql(sql, [], False, True)
        cont_service = service
        i = 0
        for x in service:
            cont_service[i] = {'service_photo': x[0], 'service_name': x[1], 'service_type': x[2],
                               'service_bank_ac': x[3], 'service_post': 'SERVICE'+str(x[4]), 'service_val': x[4]}
            i = i+1

        sql = 'SELECT OPERATOR_ID,OPERATOR_NAME,OPERATOR_DIGIT,OPERATOR_BANK_AC_NO FROM MOBILE_OPERATOR WHERE APPROVED_BY IS NULL'
        operator = execute_sql(sql, [], False, True)
        cont_operator = operator
        i = 0
        for x in operator:
            cont_operator[i] = {'operator_post': 'OPERATOR'+str(
                x[0]), 'operator_val': x[0], 'operator_name': x[1], 'operator_digit': x[2], 'operator_bank_ac': x[3]}
            i = i+1

        context = {'NAME': name, 'CUSTOMER': cont_cust,
                   'AGENT': cont_agent, 'ADMIN': cont_admin, 'MERCHANT': cont_merchant, 'SERVICE': cont_service, 'OPERATOR': cont_operator}

        return context
    def addMoney(self,receiver_mobile_no,amount):
        sql = """SELECT AGENT_ID
                FROM AGENT A,USERS U
                WHERE A.AGENT_ID = U.USER_ID AND U.USER_MOBILE_NO =: receiver_id"""
        if execute_sql(sql,[receiver_mobile_no],False,True):
            receiver_id = execute_sql(sql,[receiver_mobile_no],False,True)[0][0]
            
            sql = 'UPDATE AGENT SET AGENT_BALANCE = AGENT_BALANCE+ :add_money_amount WHERE AGENT_ID =:receiver_id'
            list = [amount,receiver_id]
            execute_sql(sql,list,True,False)
            sql = 'INSERT INTO ADD_MONEY(SENDER_ID,RECEIVER_ID,ADD_MONEY_AMOUNT) VALUES(:sender_id,:receiver_id,:add_amount)'
            list = [self.id,receiver_id,amount]
            execute_sql(sql,list,True,False)
            return True
        else:
            return False


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
            self.offer_percent = 0
        else:
            offer_id = ans[4]
            sql = 'SELECT DISCOUNT_PERCENT FROM OFFERS WHERE OFFER_ID =: offer_id'
            self.offer_percent = execute_sql(
                sql, [offer_id], False, True)[0][0]

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
        context = {'NAME': self.merchantName, 'PHOTO': '\media\\'+self.img,
                   'TRADE_LICENSE_NO': self.trade_license, 'HEAD_OFFICE_LOCATION': self.head_office, 'BRANCH': cont_branch, 'OFFER_PERCENT': self.offer_percent}
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
    def __init__(self, discount_percentage):

        sql = 'SELECT OFFER_ID FROM OFFERS WHERE DISCOUNT_PERCENT =: discount_percent'
        list = [discount_percentage]
        if not execute_sql(sql, list, False, True):
            if not execute_sql('select max(OFFER_ID) from OFFERS', [], False, True)[0][0]:
                self.offer_id = 1
            else:
                self.offer_id = int(execute_sql(
                    'select max(OFFER_ID) from OFFERS', [], False, True)[0][0]) + 1
            self.discount_percent = discount_percentage

            sql_insert = 'INSERT INTO OFFERS VALUES(:offer_id,:discount_percent)'
            execute_sql(sql_insert, [self.offer_id,
                                     self.discount_percent], True, False)

        else:
            self.offer_id = execute_sql(
                'SELECT OFFER_ID FROM OFFERS WHERE DISCOUNT_PERCENT =: discount_percent', [discount_percentage], False, True)[0][0]
            self.discount_percent = discount_percentage

    def getOfferId(self):
        return self.offer_id


class AllAgentInfo:
    def __init__(self):
        pass

    def getInfo(self):

        sql = 'SELECT USER_ID,USER_NAME,USER_PHOTO,USER_MOBILE_NO,USER_NID,AGENT_BALANCE,AGENT_BANK_AC FROM USERS U,AGENT A WHERE U.USER_ID = A.AGENT_ID AND APPROVED_BY IS NOT NULL ORDER BY USER_ID ASC'

        if execute_sql(sql, [], False, True):
            agent = execute_sql(sql, [], False, True)
            i = 0
            cont_agent = agent
            for x in agent:
                cont_agent[i] = {'agent_name': x[1], 'agent_photo': x[2],
                                 'agent_mobile_no': x[3], 'agent_nid': x[4], 'agent_balance': x[5], 'agent_bank_ac': x[6]}
                agent_id = x[0]
                transaction = execute_sql_func(
                    'GET_TRANSACTION_COUNT_AGENT', [agent_id], False, True)
                tran = transaction.split()

                cont_agent[i]['cash_in'] = tran[0]
                cont_agent[i]['cash_out_used'] = tran[1]
                cont_agent[i]['merchant_payment'] = tran[2]
                cont_agent[i]['mobile_recharge'] = tran[3]
                cont_agent[i]['service_payment'] = tran[4]
                cont_agent[i]['add_money_count'] = tran[5]

                i = i+1

            context = {'AGENT': cont_agent}
            return context
        else:
            context = {'AGENT': False}
            return context


class AllCustomerInfo:
    def __init__(self):
        pass

    def getInfo(self):
        sql = 'SELECT USER_ID,USER_NAME,USER_PHOTO,USER_MOBILE_NO,USER_NID,CUSTOMER_BALANCE FROM USERS U,CUSTOMER C WHERE U.USER_ID = C.CUSTOMER_ID AND APPROVED_BY IS NOT NULL ORDER BY USER_ID ASC'
        if execute_sql(sql, [], False, True):
            customer = execute_sql(sql, [], False, True)
            i = 0
            cont_customer = customer
            for x in customer:
                cont_customer[i] = {'customer_name': x[1], 'customer_photo': x[2],
                                    'customer_mobile_no': x[3], 'customer_nid': x[4], 'customer_balance': x[5]}
                customer_id = x[0]
                transaction = execute_sql_func('GET_TRANSACTION_COUNT_CUSTOMER', [
                    customer_id], False, True)
                tran = transaction.split()

                cont_customer[i]['cash_in_to'] = tran[0]
                cont_customer[i]['cash_out_from'] = tran[1]
                cont_customer[i]['merchant_payment'] = tran[2]
                cont_customer[i]['mobile_recharge'] = tran[3]
                cont_customer[i]['service_payment'] = tran[4]
                cont_customer[i]['send_money_from'] = tran[5]
                cont_customer[i]['received_money_to'] = tran[6]
                i = i+1

            context = {'CUSTOMER': cont_customer}
            return context
        else:
            context = {'CUSTOMER': False}
            return context


class AllMerchantInfo:
    def __init__(self):
        pass

    def getInfo(self):
        sql = """SELECT MERCHANT_ID,MERCHANT_NAME,MERCHANT_LOGO_IMAGE,TRADE_LICENSE_NO,HEAD_OFFICE_LOCATION,NVL(O.DISCOUNT_PERCENT,0)
                FROM MERCHANTS M,OFFERS O
                WHERE M.OFFER_ID = O.OFFER_ID (+)
                ORDER BY MERCHANT_ID ASC"""
        merchant = execute_sql(sql, [], False, True)
        cont_merchant = merchant
        i = 0
        for x in merchant:
            cont_merchant[i] = {'merchant_name': x[1], 'merchant_photo': x[2], 'trade_license': x[3],
                                'head_office': x[4], 'offer': x[5]}
            merchant_id = x[0]
            merchant_info = execute_sql_func(
                'GET_MERCHANT_INFO', [merchant_id], False, True)
            info = merchant_info.split()
            cont_merchant[i]['total_branch'] = info[0]
            cont_merchant[i]['mer_balance'] = info[1]
            cont_merchant[i]['total_transaction'] = info[2]

            i = i+1
        context = {'MERCHANT': cont_merchant}
        return context


class AllOperatorInfo:
    def __init__(self):
        pass

    def getInfo(self):

        sql = """SELECT M.OPERATOR_ID,M.OPERATOR_NAME,M.OPERATOR_DIGIT,M.OPERATOR_BANK_AC_NO,M.OPERATOR_BALANCE,NVL(COUNT(MR.OPERATOR_ID),0) TOTAL
                FROM MOBILE_OPERATOR M,MOBILE_RECHARGE MR,HISTORY H
                WHERE M.OPERATOR_ID = MR.OPERATOR_ID (+) AND MR.HISTORY_ID = H.HISTORY_ID AND M.APPROVED_BY IS NOT NULL
                GROUP BY M.OPERATOR_ID,M.OPERATOR_NAME,M.OPERATOR_DIGIT,M.OPERATOR_BANK_AC_NO,M.OPERATOR_BALANCE
                ORDER BY M.OPERATOR_ID ASC"""
        operator = execute_sql(sql, [], False, True)
        cont_operator = operator
        i = 0
        for x in operator:
            cont_operator[i] = {'operator_name': x[1], 'operator_3rd_digit': x[2],
                                'operator_bank_ac_no': x[3], 'operator_balance': x[4], 'transaction': x[5]}
            i = i+1
        context = {'OPERATOR': cont_operator}
        return context


class AllServiceProviderInfo:
    def __init__(self):
        pass

    def getInfo(self):

        sql = """SELECT S.SERVICE_NAME,S.SERVICE_PHOTO,S.SERVICE_TYPE,S.SERVICE_BANK_AC_NO,S.BALANCE,COUNT(PUB.SERVICE_ID) TOTAL
                FROM UTILITY_SERVICE S,PAY_UTILITY_BILL PUB,HISTORY H
                WHERE S.SERVICE_ID = PUB.SERVICE_ID (+) AND PUB.HISTORY_ID = H.HISTORY_ID AND APPROVED_BY IS NOT NULL
                GROUP BY S.SERVICE_ID,S.SERVICE_NAME,S.SERVICE_PHOTO,S.SERVICE_TYPE,S.SERVICE_BANK_AC_NO,S.BALANCE
                ORDER BY S.SERVICE_TYPE ASC"""
        service_provider = execute_sql(sql, [], False, True)
        cont_service = service_provider
        i = 0
        for x in service_provider:
            cont_service[i] = {'service_name': x[0],
                               'service_photo': x[1],
                               'service_type': x[2],
                               'service_bank_ac': x[3],
                               'service_balance': x[4],
                               'service_transaction': x[5]}
            i = i+1
        context = {'SERVICE': cont_service}
        return context
