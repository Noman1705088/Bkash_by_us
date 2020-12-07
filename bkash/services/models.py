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


class HistoryOf:
    def __init__(self, user):
        self.user = user

    def getHistory(self):
        sql = 'SELECT SENDER,RECEIVER,AMOUNT,TRANSACTION_ID,TRANSACTION_TIME,TYPE_NAME FROM \
            ((SELECT \'AGEN_\' || AGENT_ID SENDER,\'CUST_\'||CUSTOMER_ID RECEIVER,HISTORY_ID,TRANSACTION_AMOUNT_C_I AMOUNT FROM CASH_IN)\
                UNION (SELECT \'CUST_\'||CUSTOMER_ID,\'AGEN_\'||AGENT_ID,HISTORY_ID,TRANSACTION_AMOUNT_C_O FROM CASH_OUT)\
                    UNION (SELECT \'CUST_\'||FROM_CUSTOMER_ID,\'CUST_\'||TO_CUSTOMER_ID,HISTORY_ID,TRANSACTION_AMOUNT_S_M FROM SEND_MONEY))\
                        S JOIN HISTORY H ON S.HISTORY_ID=H.HISTORY_ID JOIN HISTORY_TYPE HT ON H.TYPE_ID=HT.TYPE_ID\
                            WHERE SENDER =: SENDER OR RECEIVER =: RECEIVER\
                                ORDER BY TRANSACTION_TIME DESC'

        ans = execute_sql(sql, [self.user, self.user], False, True)
        cont_history = ans

        i = 0
        for x in ans:
            sender = x[0]
            receiver = x[1]
            sql = 'SELECT USER_MOBILE_NO FROM USERS WHERE USER_ID=: id'

            sender = execute_sql(sql, [sender[5:]], False, True)[0][0]
            receiver = execute_sql(sql, [receiver[5:]], False, True)[0][0]
            cont_history[i] = {'SENDER': sender, 'RECEIVER': receiver,
                               'AMOUNT': x[2], 'TXID': x[3], 'TIME': x[4], 'HIS_TYPE': x[5]}
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
            sql = 'SELECT AGENT_BALANCE FROM AGENTS WHERE AGENT_ID=: AGNT_ID'
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

        if disc_percent > 0:
            disc_amount = (self.amount*disc_percent)/100.0
            if self.sender_type == "customer":
                sql = 'UPDATE CUSTOMER SET CUSTOMER_BALANCE = CUSTOMER_BALANCE+ :cashback_amount WHERE CUSTOMER_ID =:sender_id'
                list = [disc_amount, self.sender_id]
            elif self.sender_type == "agent":
                sql = 'UPDATE AGENT SET AGENT_BALANCE = AGENT_BALANCE+ :cashback_amount WHERE AGENT_ID =:sender_id'
                list = [disc_amount, self.sender_id]
            execute_sql(sql, list, True, False)

            sql = 'INSERT INTO PAYMENT(MERCHANT_BRANCH_ID,USER_ID,TRANSACTION_AMOUNT_PAYMENT) VALUES(:receiver,:sender,:amount)'
            list = [self.merchant_branch_id, self.sender_id, self.amount]
            execute_sql(sql, list, True, False)

            sql = 'INSERT INTO CASHBACK(USER_ID,MERCHANT_BRANCH_ID,CASHBACK_AMOUNT) VALUES(:sender,:merchant,:amount)'
            list = [self.sender_id, self.merchant_branch_id, disc_amount]
            execute_sql(sql, list, True, False)
