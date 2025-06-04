from Banking.account import SavingsAccount,CurrentAccount
from Banking.transactions import deposit,withdraw

accounts={}

def create_account():
    name=input("Enter the account holder's name: ").strip()
    account_type=input("Enter the account type (savings/current): ").strip().lower()
    initial_balance=float(input("Enter the initial balance: "))
    if account_type=="savings":
        acc = SavingsAccount(name,initial_balance)
    elif account_type=="current":
        acc = CurrentAccount(name,initial_balance)
    else:
        print("Invalid account type. Please enter 'savings' or 'current'.")
        return None
    accounts[acc.account_number]=acc
    print(f"Account created successfully for {name}. Account number: {acc.account_number}")
    
def login():
    account_number=int(input("Enter your account number: "))
    if account_number in accounts:
        user_account=accounts[account_number]
        print(f"Welcome, {user_account.name}!")
        while True:
            print("\n1. Deposit")
            print("\n2. Withdraw")
            print("\n3. Display Balance")
            if isinstance(user_account,SavingsAccount):
                print("\n4. Calculate Interest")
            print("\n5. Logout")
            
            choice=int(input("Enter your choice: "))
            if choice==1:
                amount=float(input("Enter the amount to deposit: "))
                deposit(user_account,amount)
            elif choice==2:
                amount=float(input("Enter the amount to withdraw: "))
                withdraw(user_account,amount)
            elif choice==3:
                print(f"Current balance: {user_account.get_balance()}")
            elif choice==4 and isinstance(user_account,SavingsAccount):
                user_account.calculate_interest()
            elif choice==5:
                print("Thank you for using the banking system! Logging out...")
                break
            else:
                print("Invalid choice. Please try again.")
    else:
        print("Invalid account number. Please try again.")

def main():
    print("\nWelcome to the SBI banking system!\nNagpur SIT Branch")
    print("="*50)
    while True:
        print("\n1. Create Account")
        print("\n2. Login")
        print("\n3. Exit")
        choice=input("Choose an option: ")
        if choice == '1':
            create_account()
        elif choice == '2':
            login()
        elif choice == '3':
            print("Thank you for using SBI Bank. Goodbye!")
            break
        else:
            print("Invalid choice. Please choose a valid option.")

if __name__ == "__main__":
    main()
        
