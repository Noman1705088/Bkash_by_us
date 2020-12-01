from django.db import models
from dashboard.models import execute_sql

# Create your models here.

class SendMoney:
    def __init__(self,sender_id,receiver_mobile,amount):
        self.sender_id= sender_id
        self.receiver_mobile= receiver_mobile
        self.amount= amount

    def hasEnoughMoney(self):
        sql = 'SELECT CUSTOMER_BALANCE FROM CUSTOMER WHERE CUSTOMER_ID=: CUST_ID'
        list = [self.sender_id]
        sender_balance = execute_sql(sql,list,False,True)[0][0]

        if sender_balance>=self.amount:
            return True
        return False

    def validMobileNo(self):
        sql = 'SELECT CUSTOMER_ID FROM USERS U JOIN CUSTOMER C ON C.CUSTOMER_ID=U.USER_ID WHERE USER_MOBILE_NO =: receiver'
        list = [self.receiver_mobile]

        if execute_sql(sql,list,False,True):
            self.receiver_id = execute_sql(sql,list,False,True)[0][0]
            return True
        return False

    def doTransiction(self):
        sql = 'UPDATE CUSTOMER SET CUSTOMER_BALANCE = CUSTOMER_BALANCE+ :amount WHERE CUSTOMER_ID = :reciver' 
        list = [self.amount,self.receiver_id]
        execute_sql(sql,list,True,False)

        sql = 'UPDATE CUSTOMER SET CUSTOMER_BALANCE = CUSTOMER_BALANCE- :amount WHERE CUSTOMER_ID = :sender' 
        list = [self.amount,self.sender_id]
        execute_sql(sql,list,True,False) 

        sql = 'INSERT INTO SEND_MONEY(FROM_CUSTOMER_ID,TO_CUSTOMER_ID,TRANSACTION_AMOUNT_S_M) VALUES(:sender,:receiver,:amount)'
        list = [self.sender_id,self.receiver_id,self.amount]
        execute_sql(sql,list,True,False)


class CashIn:
    def __init__(self,sender_id,receiver_mobile,amount):
        self.sender_id= sender_id
        self.receiver_mobile= receiver_mobile
        self.amount= amount

    def hasEnoughMoney(self):
        sql = 'SELECT AGENT_BALANCE FROM AGENT WHERE AGENT_ID=: AGENT_ID'
        list = [self.sender_id]
        sender_balance = execute_sql(sql,list,False,True)[0][0]

        if sender_balance>=self.amount:
            return True
        return False

    def validMobileNo(self):
        sql = 'SELECT CUSTOMER_ID FROM USERS U JOIN CUSTOMER C ON C.CUSTOMER_ID=U.USER_ID\
             WHERE USER_MOBILE_NO =: receiver AND APPROVED_BY IS NOT NULL'
        list = [self.receiver_mobile]

        if execute_sql(sql,list,False,True):
            self.receiver_id = execute_sql(sql,list,False,True)[0][0]
            return True
        return False

    def doTransiction(self):
        sql = 'UPDATE CUSTOMER SET CUSTOMER_BALANCE = CUSTOMER_BALANCE+ :amount WHERE CUSTOMER_ID = :reciver' 
        list = [self.amount,self.receiver_id]
        execute_sql(sql,list,True,False)

        sql = 'UPDATE AGENT SET AGENT_BALANCE = AGENT_BALANCE- :amount WHERE AGENT_ID = :sender' 
        list = [self.amount,self.sender_id]
        execute_sql(sql,list,True,False) 

        sql = 'INSERT INTO CASH_IN(CUSTOMER_ID,AGENT_ID,TRANSACTION_AMOUNT_C_I) VALUES(:receiver,:sender,:amount)'
        list = [self.receiver_id,self.sender_id,self.amount]
        execute_sql(sql,list,True,False)

class CashOut:
    def __init__(self,sender_id,receiver_mobile,amount):
        self.sender_id= sender_id
        self.receiver_mobile= receiver_mobile
        self.amount= amount

    def hasEnoughMoney(self):
        sql = 'SELECT CUSTOMER_BALANCE FROM CUSTOMER WHERE CUSTOMER_ID=: CUST_ID'
        list = [self.sender_id]
        sender_balance = execute_sql(sql,list,False,True)[0][0]

        if sender_balance>=self.amount:
            return True
        return False

    def validMobileNo(self):
        sql = 'SELECT AGENT_ID FROM USERS U JOIN AGENT A ON U.USER_ID=A.AGENT_ID\
             WHERE USER_MOBILE_NO=: receiver AND APPROVED_BY IS NOT NULL'
        list = [self.receiver_mobile]

        if execute_sql(sql,list,False,True):
            self.receiver_id = execute_sql(sql,list,False,True)[0][0]
            return True
        return False

    def doTransiction(self):
        sql = 'UPDATE AGENT SET AGENT_BALANCE = AGENT_BALANCE+ :amount WHERE AGENT_ID = :receiver' 
        list = [self.amount,self.receiver_id]
        execute_sql(sql,list,True,False)

        sql = 'UPDATE CUSTOMER SET CUSTOMER_BALANCE = CUSTOMER_BALANCE- :amount WHERE CUSTOMER_ID = :reciver'
        list = [self.amount,self.sender_id]
        execute_sql(sql,list,True,False) 

        sql = 'INSERT INTO CASH_OUT(AGENT_ID,CUSTOMER_ID,TRANSACTION_AMOUNT_C_O) VALUES(:receiver,:sender,:amount)'
        list = [self.receiver_id,self.sender_id,self.amount]
        execute_sql(sql,list,True,False)

class HistoryOf:
    def __init__(self,user):
        self.user = user

    def getHistory(self):
        sql = 'SELECT SENDER,RECEIVER,AMOUNT,TRANSACTION_ID,TRANSACTION_TIME,TYPE_NAME FROM \
            ((SELECT \'CUST_\'||CUSTOMER_ID SENDER,\'AGEN_\' || AGENT_ID RECEIVER,HISTORY_ID,TRANSACTION_AMOUNT_C_I AMOUNT FROM CASH_IN)\
                UNION (SELECT \'AGEN_\'||AGENT_ID,\'CUST_\'||CUSTOMER_ID,HISTORY_ID,TRANSACTION_AMOUNT_C_O FROM CASH_OUT)\
                    UNION (SELECT \'CUST_\'||FROM_CUSTOMER_ID,\'CUST_\'||TO_CUSTOMER_ID,HISTORY_ID,TRANSACTION_AMOUNT_S_M FROM SEND_MONEY))\
                        S JOIN HISTORY H ON S.HISTORY_ID=H.HISTORY_ID JOIN HISTORY_TYPE HT ON H.TYPE_ID=HT.TYPE_ID\
                            WHERE SENDER =: SENDER OR RECEIVER =: RECEIVER\
                                ORDER BY TRANSACTION_TIME DESC'
        
        ans = execute_sql(sql,[self.user,self.user],False,True)
        cont_history = ans
        
        i = 0
        for x in ans:
            sender= x[0]
            receiver=x[1]
            sql = 'SELECT USER_MOBILE_NO FROM USERS WHERE USER_ID=: id'

            sender = execute_sql(sql,[sender[5:]],False,True)[0][0]
            receiver = execute_sql(sql,[receiver[5:]],False,True)[0][0]
            cont_history[i] = {'SENDER':sender,'RECEIVER':receiver,'AMOUNT':x[2],'TXID':x[3],'TIME':x[4],'HIS_TYPE':x[5]}
            i = i+1

        return cont_history
               