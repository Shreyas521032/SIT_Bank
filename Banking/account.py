class BankAccount:
    account_counter=1000
    def __init__(self,name,balance=0.0):
        self.name=name
        self.__balance=balance
        self.account_number=BankAccount.account_counter
        BankAccount.account_counter+=1
        
    def get_balance(self):
        return self.__balance
    
    def withdraw(self,amount):
        if amount>0:
            self.__balance-=amount
            print(f"Withdrawl of {amount} successful. New balance: {self.__balance}")
            return True
        else:
            print("Withdrawl amount must be positive")
            return False
        
    def deposit(self,amount):
        if amount>0:
            self.__balance+=amount
            print(f"Deposit of {amount} successful. New balance: {self.__balance}")
            return True
        else:
            print("Deposit amount must be positive")
            return False
        
    def display_balance(self):
        print(f"Account number: {self.account_number}, Holder: {self.name}, Balance: {self.__balance}")

class SavingsAccount(BankAccount):
    def __init__(self,name,balance=0.0,interest_rate=0.05):
        super().__init__(name,balance)
        self.__interest_rate=interest_rate
    def calculate_interest(self):
        months = int(input("How many months to calculate interest for: "))
        interest=self.get_balance() * self.__interest_rate * months
        self.deposit(interest)
        print(f"Interest applied. New balance: {self.get_balance()}")


class CurrentAccount(BankAccount):
    def __init__(self,name,balance=0.0,overdraft_limit=100000.0):
        super().__init__(name,balance)
        self.overdraft_limit=overdraft_limit