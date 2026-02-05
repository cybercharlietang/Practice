"""
All your implementation code for the bank system simulation goes here.
"""
from collections import defaultdict
from this import d

class Simulation:

    def __init__(self):
        self.accounts=defaultdict(dict)
        self.cashbacks=defaultdict(list)
        self.payments=defaultdict(list)
        self.total=0

    def create_account(self, timestamp: int, account_id: str) -> bool | None:
        if account_id in self.accounts:
            return False
        self.accounts[account_id]={"timestamp":timestamp, "balance":0, "outgoing":0, "withdrawals":0}
        return True

    def deposit(self, timestamp: int, account_id: str, amount: int) -> int | None:
        if account_id not in self.accounts:
            return None
        self.accounts[account_id]["balance"]+=amount
        for cashbacks in self.cashbacks[account_id]:
            if cashbacks["status"]==False:
                if timestamp>=cashbacks["time_cb"]:
                    self.accounts[account_id]["balance"]+=cashbacks["amount"]
                    cashbacks["status"]=True
                    self.payments[cashbacks["payment_id"]]["status"]=True
        return self.accounts[account_id]["balance"]

    def transfer(self, timestamp: int, source_account_id: str, target_account_id: str, amount: int) -> int | None:
        if source_account_id not in self.accounts:
            return None
        if target_account_id not in self.accounts:
            return None
        if target_account_id==source_account_id:
            return None
        for cashbacks in self.cashbacks[source_account_id]:
            if cashbacks["status"]==False:
                if timestamp>=cashbacks["time_cb"]:
                    self.accounts[source_account_id]["balance"]+=cashbacks["amount"]
                    cashbacks["status"]=True
                    self.payments[cashbacks["payment_id"]]["status"]=True
        if self.accounts[source_account_id]["balance"]<amount:
            return None
        self.accounts[source_account_id]["balance"]-=amount
        self.accounts[target_account_id]["balance"]+=amount
        self.accounts[source_account_id]["outgoing"]+=amount
        return self.accounts[source_account_id]["balance"]
        

    def top_spenders(self, timestamp: int, n: int) -> list[str] | None:
        res = [(sid, self.accounts[sid]) for sid in self.accounts]
        sorted_res = sorted(res, key= lambda k: (-k[1]["outgoing"], k[0]))
        filter_res = sorted_res[:n]
        return [str(acc[0])+"("+str(acc[1]["outgoing"])+")" for acc in filter_res]

    def pay(self, timestamp: int, account_id: str, amount: int) -> str | None:
        if account_id not in self.accounts:
            return None
        if self.accounts[account_id]["balance"]<amount:
            return None
        self.accounts[account_id]["balance"]-=amount
        self.accounts[account_id]["outgoing"]+=amount
        self.accounts[account_id]["withdrawals"]+=1
        self.total+=1
        self.payments["payment"+str(self.total)]={"account_id": account_id, "time_cb":timestamp+86400000, "amount":0.02*amount, "status": False}
        self.cashbacks[account_id].append({"payment_id": "payment"+str(self.total), "time_cb":timestamp+86400000, "amount":0.02*amount, "status": False})
        return "payment"+str(self.total)
        

    def get_payment_status(self, timestamp: int, account_id: str, payment: str) -> str | None:
        if account_id not in self.accounts:
            return None
        if payment not in self.payments:
            return None
        if self.payments[payment]["account_id"]!=account_id:
            return None
        for cashbacks in self.cashbacks[account_id]:
            if cashbacks["status"]==False:
                if timestamp>=cashbacks["time_cb"]:
                    self.accounts[account_id]["balance"]+=cashbacks["amount"]
                    cashbacks["status"]=True
                    self.payments[cashbacks["payment_id"]]["status"]=True
        if timestamp<self.payments[payment]["time_cb"]:
            return "IN_PROGRESS"
        
        return "CASHBACK_RECEIVED"

    def merge_accounts(self, timestamp: int, account_id_1: str, account_id_2: str) -> bool | None:
        if account_id_1 not in self.accounts:
            return False
        if account_id_2 not in self.accounts:
            return False
        if account_id_1==account_id_2:
            return False
        self.cashbacks[account_id_1]=self.cashbacks[account_id_1]+self.cashbacks[account_id_2]
        self.accounts[account_id_1]["balance"]+=self.accounts[account_id_2]["balance"]
        self.accounts[account_id_1]["outgoing"]+=self.accounts[account_id_2]["outgoing"]
        self.accounts[account_id_1]["withdrawals"]+=self.accounts[account_id_2]["withdrawals"]
        for payments in self.payments.values():
            if payments["account_id"]==account_id_2:
                payments["account_id"]=account_id_1
        self.accounts.pop(account_id_2)
        self.cashbacks.pop(account_id_2)
        return True

    def get_balance(self, timestamp: int, account_id: str, time_at: int) -> int | None:
        if time_at < self.accounts[account_id]["timestamp"]:
            return None
        return self.account[account_id]["balance"]