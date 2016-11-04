from datetime import date as Date
import csv 
import copy 

ATM = 'atm'
CASH = 'cash'

class Transaction:
    def __init__(self, input_line):
        self.id = int(input_line[0])
        self.name = input_line[1]
        self.amount = int(input_line[2])
        self.parent_id = None 
        time = input_line[3].split('-')
        year = int(time[0])
        month = int(time[1])
        day = int(time[2])
        self.date = Date(year, month, day)
        
        if (input_line[4] == 'True' and input_line[5] == 'False'):
            self.type = CASH 
        elif (input_line[4] == 'False' and input_line[5] == 'True'):
            self.type = ATM 
        else:
            raise Error('Provided transaction is neither cash nor atm.')
             

class Reconciler:
    
    def __init__(self, csv_file):
        self.csv_file = csv_file 
        self.purchases = []
        self.withdrawals = []
        self.output = []
        
    def digest(self):
        f = open(self.csv_file)
        csv_f = csv.reader(f)
        next(csv_f, None)
        for row in csv_f:
            transaction = Transaction(row)
            if transaction.type == ATM:
                self.withdrawals.append(transaction)
            else:
                self.purchases.append(transaction)
        '''
                Assumption here is that transaction with higher id 
                is definitely more recent than one with lower id. 
        '''
        self.purchases.sort(key=lambda x: x.id, reverse=True)
        self.withdrawals.sort(key=lambda x: x.id, reverse=True)
    
    def reconcile(self):
        current_atm = self.withdrawals.pop(0)
        current_cash = self.purchases.pop(0)
        amt_left = False 
        not_done = True
        while not_done: 
            if current_cash.amount == current_atm.amount:
                current_cash.parent_id = current_atm.id
                self.output.append(current_cash)
                if len(self.withdrawals) > 0:
                    current_atm = self.withdrawals.pop(0)
                if len(self.purchases) > 0:
                    current_cash = self.purchases.pop(0)
                else:
                    not_done = False 
            elif current_cash.amount < current_atm.amount:
                current_cash.parent_id = current_atm.id
                current_atm.amount -= current_cash.amount
                self.output.append(current_cash)
                if len(self.purchases) > 0:
                    current_cash = self.purchases.pop(0)
                else:
                    not_done = False
            elif current_cash.amount > current_atm.amount:
                temp = copy.deepcopy(current_cash)
                temp.amount = current_atm.amount
                temp.parent_id = current_atm.id
                current_cash.amount -= current_atm.amount
                self.output.append(temp)
                if len(self.withdrawals) > 0:
                    current_atm = self.withdrawals.pop(0)
                else:
                    self.output.append(current_cash)
                    if len(self.purchases) > 0:
                        for cash in self.purchases:
                            self.output.append(cash)
                    not_done = False
    
    def report(self): 
        with open('challenge_output.csv', 'w') as fp:
            a = csv.writer(fp, delimiter=',')
            a.writerow(['id'] + ['name'] + ['parent'] + ['amount'])
            for transaction in self.output:
                a.writerow([str(transaction.id)] + [transaction.name] + [str(transaction.parent_id)] + [str(transaction.amount)])
                
r = Reconciler('challenge_test.csv')
r.digest() 
r.reconcile()
r.report()