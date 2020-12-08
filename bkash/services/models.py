from django.db import models
from dashboard.models import execute_sql, hash_the_password

# Create your models here.


class SendMoney:
    def __init__(self, sender_id, receiver_mobile, amount, password):
        self.sender_id = sender_id
        self.receiver_mobile = receiver_mobile
        self.amount = amount
        self.password = password

    def isCorrectPass(self):
        sql = 'SELECT USER_PASSWORD FROM USERS U JOIN CUSTOMER C ON U.USER_ID=C.CUSTOMER_ID WHERE CUSTOMER_ID=:CUST\
            AND APPROVED_BY IS NOT NULL'
        list = [self.sender_id]

        if not execute_sql(sql, list, False, True):
            return False
        elif execute_sql(sql, list, False, True)[0][0] == hash_the_password(self.password):
            return True
        else:
            return False

    def hasEnoughMoney(self):
        sql = 'SELECT CUSTOMER_BALANCE FROM CUSTOMER WHERE CUSTOMER_ID=: CUST_ID'
        list = [self.sender_id]
        sender_balance = execute_sql(sql, list, False, True)[0][0]

        if sender_balance >= self.amount:
            return True
        return False

    def validMobileNo(self):
        sql = 'SELECT CUSTOMER_ID FROM USERS U JOIN CUSTOMER C ON C.CUSTOMER_ID=U.USER_ID WHERE USER_MOBILE_NO =: receiver'
        list = [self.receiver_mobile]

        if execute_sql(sql, list, False, True):
            self.receiver_id = execute_sql(sql, list, False, True)[0][0]
            return True
        return False

    def doTransiction(self):
        sql = 'UPDATE CUSTOMER SET CUSTOMER_BALANCE = CUSTOMER_BALANCE+ :amount WHERE CUSTOMER_ID = :reciver'
        list = [self.amount, self.receiver_id]
        execute_sql(sql, list, True, False)

        sql = 'UPDATE CUSTOMER SET CUSTOMER_BALANCE = CUSTOMER_BALANCE- :amount WHERE CUSTOMER_ID = :sender'
        list = [self.amount, self.sender_id]
        execute_sql(sql, list, True, False)

        sql = 'INSERT INTO SEND_MONEY(FROM_CUSTOMER_ID,TO_CUSTOMER_ID,TRANSACTION_AMOUNT_S_M) VALUES(:sender,:receiver,:amount)'
        list = [self.sender_id, self.receiver_id, self.amount]
        execute_sql(sql, list, True, False)


class CashIn:
    def __init__(self, sender_id, receiver_mobile, amount, password):
        self.sender_id = sender_id
        self.receiver_mobile = receiver_mobile
        self.amount = amount
        self.password = password

    def isCorrectPass(self):
        sql = 'SELECT USER_PASSWORD FROM USERS U JOIN AGENT A ON U.USER_ID=A.AGENT_ID WHERE AGENT_ID=:AGENT\
            AND APPROVED_BY IS NOT NULL'
        list = [self.sender_id]

        if not execute_sql(sql, list, False, True):
            return False
        elif execute_sql(sql, list, False, True)[0][0] == hash_the_password(self.password):
            return True
        else:
            return False

    def hasEnoughMoney(self):
        sql = 'SELECT AGENT_BALANCE FROM AGENT WHERE AGENT_ID=: AGENT_ID'
        list = [self.sender_id]
        sender_balance = execute_sql(sql, list, False, True)[0][0]

        if sender_balance >= self.amount:
            return True
        return False

    def validMobileNo(self):
        sql = 'SELECT CUSTOMER_ID FROM USERS U JOIN CUSTOMER C ON C.CUSTOMER_ID=U.USER_ID\
             WHERE USER_MOBILE_NO =: receiver AND APPROVED_BY IS NOT NULL'
        list = [self.receiver_mobile]

        if execute_sql(sql, list, False, True):
            self.receiver_id = execute_sql(sql, list, False, True)[0][0]
            return True
        return False

    def doTransiction(self):
        sql = 'UPDATE CUSTOMER SET CUSTOMER_BALANCE = CUSTOMER_BALANCE+ :amount WHERE CUSTOMER_ID = :reciver'
        list = [self.amount, self.receiver_id]
        execute_sql(sql, list, True, False)

        sql = 'UPDATE AGENT SET AGENT_BALANCE = AGENT_BALANCE- :amount WHERE AGENT_ID = :sender'
        list = [self.amount, self.sender_id]
        execute_sql(sql, list, True, False)

        sql = 'INSERT INTO CASH_IN(CUSTOMER_ID,AGENT_ID,TRANSACTION_AMOUNT_C_I) VALUES(:receiver,:sender,:amount)'
        list = [self.receiver_id, self.sender_id, self.amount]
        execute_sql(sql, list, True, False)


class CashOut:
    def __init__(self, sender_id, receiver_mobile, amount, password):
        self.sender_id = sender_id
        self.receiver_mobile = receiver_mobile
        self.amount = amount
        self.password = password

    def isCorrectPass(self):
        sql = 'SELECT USER_PASSWORD FROM USERS U JOIN CUSTOMER C ON U.USER_ID=C.CUSTOMER_ID WHERE CUSTOMER_ID=:CUST\
            AND APPROVED_BY IS NOT NULL'
        list = [self.sender_id]

        if not execute_sql(sql, list, False, True):
            return False
        elif execute_sql(sql, list, False, True)[0][0] == hash_the_password(self.password):
            return True
        else:
            return False

    def hasEnoughMoney(self):
        sql = 'SELECT CUSTOMER_BALANCE FROM CUSTOMER WHERE CUSTOMER_ID=: CUST_ID'
        list = [self.sender_id]
        sender_balance = execute_sql(sql, list, False, True)[0][0]

        if sender_balance >= self.amount:
            return True
        return False

    def validMobileNo(self):
        sql = 'SELECT AGENT_ID FROM USERS U JOIN AGENT A ON U.USER_ID=A.AGENT_ID\
             WHERE USER_MOBILE_NO=: receiver AND APPROVED_BY IS NOT NULL'
        list = [self.receiver_mobile]

        if execute_sql(sql, list, False, True):
            self.receiver_id = execute_sql(sql, list, False, True)[0][0]
            return True
        return False

    def doTransiction(self):
        sql = 'UPDATE AGENT SET AGENT_BALANCE = AGENT_BALANCE+ :amount WHERE AGENT_ID = :receiver'
        list = [self.amount, self.receiver_id]
        execute_sql(sql, list, True, False)

        sql = 'UPDATE CUSTOMER SET CUSTOMER_BALANCE = CUSTOMER_BALANCE- :amount WHERE CUSTOMER_ID = :reciver'
        list = [self.amount, self.sender_id]
        execute_sql(sql, list, True, False)

        sql = 'INSERT INTO CASH_OUT(AGENT_ID,CUSTOMER_ID,TRANSACTION_AMOUNT_C_O) VALUES(:receiver,:sender,:amount)'
        list = [self.receiver_id, self.sender_id, self.amount]
        execute_sql(sql, list, True, False)


class PayBill:
    def servicesOfType(self,service_type):
        sql = 'SELECT SERVICE_NAME,SERVICE_TYPE,SERVICE_PHOTO,SERVICE_ID FROM UTILITY_SERVICE\
             WHERE UPPER(SERVICE_TYPE) = UPPER(:type) AND APPROVED_BY IS NOT NULL'

        list = [service_type]
        services = execute_sql(sql,list,False,True)
        cont_service = services

        i=0
        for x in services:
            cont_service[i] = {'servie_name':x[0],'service_type':x[1],'service_photo':x[2],'service_id':x[3]}
            i=i+1

        context = {'type_services':cont_service}
        return context

    def serviceOfID(self,service_id):
        sql = 'SELECT SERVICE_NAME,SERVICE_TYPE,SERVICE_PHOTO FROM UTILITY_SERVICE\
             WHERE SERVICE_ID=:service_id AND APPROVED_BY IS NOT NULL'

        list = [service_id]
        x = execute_sql(sql,list,False,True)

        context = {'service_name':x[0][0],'service_type':x[0][1],'service_photo':x[0][2]}
        return context        

    def doTransictionCustomer(self,service_id,user_id,amount,billing_id):
        sql = 'UPDATE CUSTOMER SET CUSTOMER_BALANCE = CUSTOMER_BALANCE- :amount WHERE CUSTOMER_ID = :sender'
        list = [amount,user_id]
        execute_sql(sql,list,True,False) 

        sql = 'INSERT INTO PAY_UTILITY_BILL(SERVICE_ID,USER_ID,TRANSACTION_AMOUNT_P_U_B,BILLING_ID)\
             VALUES(:ser_id,:user_id,:amount,:billing_id)'
        list = [service_id,user_id,amount,billing_id]
        execute_sql(sql,list,True,False)

    def doTransictionAgent(self,service_id,user_id,amount,billing_id):
        sql = 'UPDATE AGENT SET AGENT_BALANCE = AGENT_BALANCE- :amount WHERE AGENT_ID = :sender' 
        list = [amount,user_id]
        execute_sql(sql,list,True,False) 

        sql = 'INSERT INTO PAY_UTILITY_BILL(SERVICE_ID,USER_ID,TRANSACTION_AMOUNT_P_U_B,BILLING_ID) VALUES \
            (:ser_id,:user_id,:amount,:billing_id)'
        list = [service_id,user_id,amount,billing_id]
        execute_sql(sql,list,True,False)

    def isCorrectPass(self,isCustomer,user_id,password):
        if isCustomer:
            sql= 'SELECT USER_PASSWORD FROM USERS U JOIN CUSTOMER C ON U.USER_ID=C.CUSTOMER_ID WHERE CUSTOMER_ID=:CUST\
                AND APPROVED_BY IS NOT NULL'
        elif not isCustomer:
            sql= 'SELECT USER_PASSWORD FROM USERS U JOIN AGENT A ON U.USER_ID=A.AGENT_ID WHERE AGENT_ID=:AGENT\
                AND APPROVED_BY IS NOT NULL'

        list= [user_id]
        passwordIs = execute_sql(sql, list, False, True)

        if not passwordIs:
            return False
        elif passwordIs[0][0] == hash_the_password(password):
            return True
        else:
            return False

    def hasEnoughMoney(self,isCustomer,user_id,amount):
        if isCustomer:
            sql = 'SELECT CUSTOMER_BALANCE FROM CUSTOMER WHERE CUSTOMER_ID=: CUST_ID'
        elif not isCustomer:
            sql = 'SELECT AGENT_BALANCE FROM AGENT WHERE AGENT_ID=: AGENT_ID'  

        list = [user_id]
        sender_balance = execute_sql(sql,list,False,True)[0][0]

        if int(sender_balance)>=int(amount):
            return True
        return False    

class HistoryOf:
    def __init__(self, user):
        self.user = user

    def getHistory(self):
        sql = 'SELECT SENDER,RECEIVER,AMOUNT,TRANSACTION_ID,TRANSACTION_TIME,TYPE_NAME,H.HISTORY_ID FROM \
            ((SELECT \'USER_\' || AGENT_ID SENDER,\'USER_\'||CUSTOMER_ID RECEIVER,HISTORY_ID,TRANSACTION_AMOUNT_C_I AMOUNT FROM CASH_IN)\
                UNION (SELECT \'USER_\'||CUSTOMER_ID,\'USER_\'||AGENT_ID,HISTORY_ID,TRANSACTION_AMOUNT_C_O FROM CASH_OUT)\
                    UNION (SELECT \'USER_\'||FROM_CUSTOMER_ID,\'USER_\'||TO_CUSTOMER_ID,HISTORY_ID,TRANSACTION_AMOUNT_S_M FROM SEND_MONEY)\
                        UNION (SELECT \'USER_\'||USER_ID,\'SERV_\'||SERVICE_ID,HISTORY_ID,TRANSACTION_AMOUNT_P_U_B FROM PAY_UTILITY_BILL)\
                            UNION (SELECT \'USER_\'||USER_ID,\'OPER_\'||OPERATOR_ID,HISTORY_ID,TRANSACTION_AMOUNT_M_R FROM MOBILE_RECHARGE))\
                        S JOIN HISTORY H ON S.HISTORY_ID=H.HISTORY_ID JOIN HISTORY_TYPE HT ON H.TYPE_ID=HT.TYPE_ID\
                            WHERE SENDER =: SENDER OR RECEIVER =: RECEIVER\
                                ORDER BY TRANSACTION_TIME DESC'

        ans = execute_sql(sql, [self.user, self.user], False, True)
        cont_history = ans

        i = 0
        for x in ans:
            sender= x[0]
            receiver=x[1]

            if sender[:5] == 'USER_':
                sql1 = 'SELECT USER_MOBILE_NO FROM USERS WHERE USER_ID=: id'
                sender = execute_sql(sql1,[sender[5:]],False,True)[0][0]
            if receiver[:5] == 'USER_' :
                sql2 = 'SELECT USER_MOBILE_NO FROM USERS WHERE USER_ID=: id'
                receiver = execute_sql(sql2,[receiver[5:]],False,True)[0][0]
            elif receiver[:5] == 'SERV_' :
                sql2 = 'SELECT SERVICE_NAME,SERVICE_TYPE FROM UTILITY_SERVICE WHERE SERVICE_ID=: id'
                receiver = execute_sql(sql2,[receiver[5:]],False,True)[0][0] +'('+execute_sql(sql2,[receiver[5:]],False,True)[0][1]+')'
            elif receiver[:5] == 'OPER_':
                sql2 = 'SELECT TO_MOBILE_NUMBER_RECHARGE,OPERATOR_NAME\
                    FROM MOBILE_OPERATOR O,MOBILE_RECHARGE M\
                        WHERE O.OPERATOR_ID = M.OPERATOR_ID AND HISTORY_ID = :hist_id'
                receiver_first = execute_sql(sql2,[x[6]],False,True)[0]
                receiver = receiver_first[0] +'(' + receiver_first[1] +')'
            
            billing_id = None
            if x[5] == 'Pay Utility Bill':
                sql3= 'SELECT BILLING_ID FROM PAY_UTILITY_BILL WHERE HISTORY_ID=:id'
                billing_id = execute_sql(sql3,[x[6]],False,True)[0][0]

            cont_history[i] = {'SENDER':sender,'RECEIVER':receiver,'AMOUNT':x[2],'TXID':x[3],\
                'TIME':x[4],'HIS_TYPE':x[5],'Billing_Id':billing_id}
            i = i+1

        return cont_history


class MerchantPayment:
    def __init__(self, sender_id, merchant_mobile_no, amount, password, sender_type):
        self.sender_id = sender_id
        self.merchant_mobile_no = merchant_mobile_no
        self.amount = amount
        self.password = password
        self.sender_type = sender_type

    def is_correct_password(self):
        if self.sender_type == "customer":
            sql = 'SELECT USER_PASSWORD FROM USERS U JOIN CUSTOMER C ON U.USER_ID=C.CUSTOMER_ID WHERE CUSTOMER_ID=:CUST\
                AND APPROVED_BY IS NOT NULL'
        elif self.sender_type == "agent":
            sql = 'SELECT USER_PASSWORD FROM USERS U JOIN AGENT A ON U.USER_ID=A.AGENT_ID WHERE AGENT_ID=:AGNT\
                AND APPROVED_BY IS NOT NULL'
        list = [self.sender_id]

        if not execute_sql(sql, list, False, True):
            return False
        elif execute_sql(sql, list, False, True)[0][0] == hash_the_password(self.password):
            return True
        else:
            return False

    def valid_merchant_mobile_no(self):
        sql = 'SELECT BRANCH_ID,BRANCH_MERCHANT_ID FROM BRANCH B,MERCHANTS M WHERE B.BRANCH_MERCHANT_ID = M.MERCHANT_ID AND B.BRANCH_MOBILE_NO =: BR_MOB'
        list = [self.merchant_mobile_no]

        if execute_sql(sql, list, False, True):
            ans = execute_sql(sql, list, False, True)[0]
            self.merchant_branch_id = ans[0]
            self.merchant_id = ans[1]
            return True
        else:
            return False

    def hasEnoughMoney(self):
        if self.sender_type == "customer":
            sql = 'SELECT CUSTOMER_BALANCE FROM CUSTOMER WHERE CUSTOMER_ID=: CUST_ID'
        elif self.sender_type == "agent":
            sql = 'SELECT AGENT_BALANCE FROM AGENT WHERE AGENT_ID=: AGNT_ID'
        list = [self.sender_id]
        sender_balance = execute_sql(sql, list, False, True)[0][0]

        if sender_balance >= self.amount:
            return True
        return False

    def do_payment_transaction(self):
        sql = 'SELECT DISCOUNT_PERCENT FROM OFFERS O,MERCHANTS M WHERE M.OFFER_ID = O.OFFER_ID  AND MERCHANT_ID =: MERC_ID'
        list = [self.merchant_id]

        if execute_sql(sql, list, False, True)[0][0]:
            disc_percent = int(execute_sql(sql, list, False, True)[0][0])
        else:
            disc_percent = 0

        if self.sender_type == "customer":
            sql = 'UPDATE CUSTOMER SET CUSTOMER_BALANCE = CUSTOMER_BALANCE- :amount WHERE CUSTOMER_ID =:sender_id'
            list = [self.amount, self.sender_id]
        elif self.sender_type == "agent":
            sql = 'UPDATE AGENT SET AGENT_BALANCE = AGENT_BALANCE- :amount WHERE AGENT_ID =:sender_id'
            list = [self.amount, self.sender_id]

        execute_sql(sql, list, True, False)

        sql = 'UPDATE BRANCH SET MERCHANT_BRANCH_BALANCE = MERCHANT_BRANCH_BALANCE+ :amount WHERE BRANCH_ID =: merchant_branch_id'
        list = [self.amount, self.merchant_branch_id]
        execute_sql(sql, list, True, False)

        sql = 'INSERT INTO PAYMENT(MERCHANT_BRANCH_ID,USER_ID,TRANSACTION_AMOUNT_PAYMENT) VALUES(:receiver,:sender,:amount)'
        list = [self.merchant_branch_id, self.sender_id, self.amount]
        execute_sql(sql, list, True, False)

        if disc_percent > 0:
            disc_amount = (self.amount*disc_percent)/100.0
            if self.sender_type == "customer":
                sql = 'UPDATE CUSTOMER SET CUSTOMER_BALANCE = CUSTOMER_BALANCE+ :cashback_amount WHERE CUSTOMER_ID =:sender_id'
                list = [disc_amount, self.sender_id]
            elif self.sender_type == "agent":
                sql = 'UPDATE AGENT SET AGENT_BALANCE = AGENT_BALANCE+ :cashback_amount WHERE AGENT_ID =:sender_id'
                list = [disc_amount, self.sender_id]
            execute_sql(sql, list, True, False)

            sql = 'INSERT INTO CASHBACK(USER_ID,MERCHANT_BRANCH_ID,CASHBACK_AMOUNT) VALUES(:sender,:merchant,:amount)'
            list = [self.sender_id, self.merchant_branch_id, disc_amount]
            execute_sql(sql, list, True, False)


class MobileRecharge:
    def __init__(self,sender_id,receiver_mobile_no,recharge_amount,password,sender_type):
        self.sender_id = sender_id
        self.receiver_mobile_no = receiver_mobile_no
        self.recharge_amount = recharge_amount
        self.password =password
        self.sender_type = sender_type
    
    def is_correct_password(self):
        if self.sender_type == "customer":
            sql = 'SELECT USER_PASSWORD FROM USERS U JOIN CUSTOMER C ON U.USER_ID=C.CUSTOMER_ID WHERE CUSTOMER_ID=:CUST\
                AND APPROVED_BY IS NOT NULL'
        elif self.sender_type == "agent":
            sql = 'SELECT USER_PASSWORD FROM USERS U JOIN AGENT A ON U.USER_ID=A.AGENT_ID WHERE AGENT_ID=:AGNT\
                AND APPROVED_BY IS NOT NULL'
        list = [self.sender_id]

        if not execute_sql(sql, list, False, True):
            return False
        elif execute_sql(sql, list, False, True)[0][0] == hash_the_password(self.password):
            return True
        else:
            return False
    
    def hasEnoughMoney(self):
        if self.sender_type == "customer":
            sql = 'SELECT CUSTOMER_BALANCE FROM CUSTOMER WHERE CUSTOMER_ID=: CUST_ID'
        elif self.sender_type == "agent":
            sql = 'SELECT AGENT_BALANCE FROM AGENT WHERE AGENT_ID=: AGNT_ID'
        list = [self.sender_id]
        sender_balance = execute_sql(sql, list, False, True)[0][0]

        if sender_balance >= self.recharge_amount:
            return True
        return False

    def isOperatorAvailable(self):
        digit = int(self.receiver_mobile_no[2])

        sql = 'SELECT COUNT(OPERATOR_ID) FROM MOBILE_OPERATOR WHERE OPERATOR_DIGIT =: digit AND APPROVED_BY IS NOT NULL'
        list = [digit]

        if execute_sql(sql,list,False,True)[0][0] == 0:
            return False
        else:
            return True
    
    def make_recharge(self):
        digit = int(self.receiver_mobile_no[2])

        sql = 'SELECT OPERATOR_ID FROM MOBILE_OPERATOR WHERE OPERATOR_DIGIT =: digit'
        list = [digit]
        operator_id = execute_sql(sql,list,False,True)[0][0]

        if self.sender_type == "customer":
            sql = 'UPDATE CUSTOMER SET CUSTOMER_BALANCE = CUSTOMER_BALANCE- :amount WHERE CUSTOMER_ID =:sender_id'
            list = [self.recharge_amount, self.sender_id]
        elif self.sender_type == "agent":
            sql = 'UPDATE AGENT SET AGENT_BALANCE = AGENT_BALANCE- :amount WHERE AGENT_ID =:sender_id'
            list = [self.recharge_amount, self.sender_id]
        execute_sql(sql, list, True, False)
        
        sql ='UPDATE MOBILE_OPERATOR SET OPERATOR_BALANCE = OPERATOR_BALANCE+ :amount WHERE OPERATOR_ID =: operator'
        list = [self.recharge_amount,operator_id]
        execute_sql(sql,list,True,False)

        sql = 'INSERT INTO MOBILE_RECHARGE(OPERATOR_ID,USER_ID,TRANSACTION_AMOUNT_M_R,TO_MOBILE_NUMBER_RECHARGE) VALUES(:operator_id,:user_id,:recharge_amount,:receiver_mobile_no)'
        list = [operator_id,self.sender_id,self.recharge_amount,self.receiver_mobile_no]
        execute_sql(sql,list,True,False)