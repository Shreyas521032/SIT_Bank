import streamlit as st

class Account:
    account_counter = 1000
    
    def __init__(self, name, initial_balance=0):
        Account.account_counter += 1
        self.account_number = Account.account_counter
        self.name = name
        self.balance = initial_balance
    
    def get_balance(self):
        return self.balance
    
    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount
    
    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount

class SavingsAccount(Account):
    def __init__(self, name, initial_balance=0, interest_rate=0.04):
        super().__init__(name, initial_balance)
        self.interest_rate = interest_rate
    
    def calculate_interest(self):
        """Calculate and add interest to the account"""
        # Fixed: Allow interest calculation on any positive balance
        if self.balance <= 0:
            raise ValueError("Balance must be positive for interest calculation")
        
        interest = self.balance * self.interest_rate
        self.balance += interest
        return interest

class CurrentAccount(Account):
    def __init__(self, name, initial_balance=0, overdraft_limit=1000):
        super().__init__(name, initial_balance)
        self.overdraft_limit = overdraft_limit
    
    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > (self.balance + self.overdraft_limit):
            raise ValueError(f"Exceeds overdraft limit of ₹{self.overdraft_limit}")
        self.balance -= amount

def deposit(account, amount):
    account.deposit(amount)

def withdraw(account, amount):
    account.withdraw(amount)

# Initialize session state
if 'accounts' not in st.session_state:
    st.session_state.accounts = {}
if 'logged_in_user' not in st.session_state:
    st.session_state.logged_in_user = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'main'

def create_account():
    st.subheader("🆕 Create New Account")
    
    with st.form("create_account_form"):
        name = st.text_input("Enter the account holder's name:")
        account_type = st.selectbox("Select account type:", ["savings", "current"])
        initial_balance = st.number_input("Enter the initial balance:", min_value=0.0, step=0.01)
        
        submitted = st.form_submit_button("Create Account")
        
        if submitted:
            if name.strip():
                try:
                    if account_type == "savings":
                        acc = SavingsAccount(name.strip(), initial_balance)
                    else:
                        acc = CurrentAccount(name.strip(), initial_balance)
                    
                    st.session_state.accounts[acc.account_number] = acc
                    st.success(f"✅ Account created successfully for {name}!")
                    st.info(f"📋 Your Account Number: **{acc.account_number}**")
                    st.balloons()
                except Exception as e:
                    st.error(f"Error creating account: {str(e)}")
            else:
                st.error("Please enter a valid name.")

def login_page():
    st.subheader("🔐 Login to Your Account")
    
    with st.form("login_form"):
        account_number = st.number_input("Enter your account number:", min_value=1, step=1)
        submitted = st.form_submit_button("Login")
        
        if submitted:
            if account_number in st.session_state.accounts:
                st.session_state.logged_in_user = st.session_state.accounts[account_number]
                st.session_state.current_page = 'dashboard'
                st.rerun()
            else:
                st.error("❌ Invalid account number. Please try again.")

def dashboard():
    user_account = st.session_state.logged_in_user
    
    st.subheader(f"👋 Welcome, {user_account.name}!")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Account Number", user_account.account_number)
    with col2:
        st.metric("Account Type", type(user_account).__name__)
    with col3:
        st.metric("Current Balance", f"₹{user_account.get_balance():.2f}")
    
    if isinstance(user_account, SavingsAccount):
        st.info(f"💡 Interest Rate: {user_account.interest_rate * 100:.1f}% per calculation")
    elif isinstance(user_account, CurrentAccount):
        st.info(f"💼 Overdraft Limit: ₹{user_account.overdraft_limit:.2f}")
    
    st.divider()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("💰 Deposit", use_container_width=True):
            st.session_state.current_page = 'deposit'
            st.rerun()
    
    with col2:
        if st.button("💸 Withdraw", use_container_width=True):
            st.session_state.current_page = 'withdraw'
            st.rerun()
    
    with col3:
        if isinstance(user_account, SavingsAccount):
            if st.button("📈 Calculate Interest", use_container_width=True):
                st.session_state.current_page = 'interest'
                st.rerun()
        else:
            st.empty()  # Maintain column structure
    
    with col4:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in_user = None
            st.session_state.current_page = 'main'
            st.rerun()

def deposit_page():
    st.subheader("💰 Deposit Money")
    user_account = st.session_state.logged_in_user
    
    st.info(f"Current Balance: ₹{user_account.get_balance():.2f}")
    
    with st.form("deposit_form"):
        amount = st.number_input("Enter amount to deposit:", min_value=0.01, step=0.01, value=100.0)
        submitted = st.form_submit_button("Deposit")
        
        if submitted:
            try:
                deposit(user_account, amount)
                st.success(f"✅ Successfully deposited ₹{amount:.2f}")
                st.info(f"New Balance: ₹{user_account.get_balance():.2f}")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    if st.button("← Back to Dashboard"):
        st.session_state.current_page = 'dashboard'
        st.rerun()

def withdraw_page():
    st.subheader("💸 Withdraw Money")
    user_account = st.session_state.logged_in_user
    
    current_balance = user_account.get_balance()
    st.info(f"Current Balance: ₹{current_balance:.2f}")
    
    if isinstance(user_account, CurrentAccount):
        available_amount = current_balance + user_account.overdraft_limit
        st.info(f"Available Amount (with overdraft): ₹{available_amount:.2f}")
    
    with st.form("withdraw_form"):
        max_amount = current_balance if isinstance(user_account, SavingsAccount) else current_balance + user_account.overdraft_limit
        amount = st.number_input("Enter amount to withdraw:", min_value=0.01, step=0.01, value=50.0)
        
        if amount > max_amount:
            st.warning(f"⚠️ Amount exceeds available funds (₹{max_amount:.2f})")
        
        submitted = st.form_submit_button("Withdraw")
        
        if submitted:
            try:
                withdraw(user_account, amount)
                st.success(f"✅ Successfully withdrew ₹{amount:.2f}")
                st.info(f"New Balance: ₹{user_account.get_balance():.2f}")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    if st.button("← Back to Dashboard"):
        st.session_state.current_page = 'dashboard'
        st.rerun()

def interest_page():
    st.subheader("📈 Calculate Interest")
    user_account = st.session_state.logged_in_user
    
    if isinstance(user_account, SavingsAccount):
        current_balance = user_account.get_balance()
        
        # Display current account info
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Current Balance", f"₹{current_balance:.2f}")
        with col2:
            st.metric("Interest Rate", f"{user_account.interest_rate * 100:.1f}%")
        
        st.divider()
        
        # Check if interest can be calculated
        if current_balance > 0:
            potential_interest = current_balance * user_account.interest_rate
            potential_new_balance = current_balance + potential_interest
            
            st.success("✅ Ready to calculate interest!")
            
            # Show potential earnings
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"💰 Interest to be earned: **₹{potential_interest:.2f}**")
            with col2:
                st.info(f"🏦 New balance will be: **₹{potential_new_balance:.2f}**")
            
            st.divider()
            
            # Calculate interest button
            if st.button("🎯 Calculate & Add Interest", type="primary", use_container_width=True):
                try:
                    old_balance = user_account.get_balance()
                    interest_earned = user_account.calculate_interest()
                    new_balance = user_account.get_balance()
                    
                    st.success(f"🎉 Interest calculated and added successfully!")
                    
                    # Show results in a nice format
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Previous Balance", f"₹{old_balance:.2f}")
                    with col2:
                        st.metric("Interest Earned", f"₹{interest_earned:.2f}", delta=f"+{interest_earned:.2f}")
                    with col3:
                        st.metric("New Balance", f"₹{new_balance:.2f}", delta=f"+{interest_earned:.2f}")
                        
                    st.balloons()
                    
                except ValueError as e:
                    st.error(f"❌ Error: {str(e)}")
                except Exception as e:
                    st.error(f"❌ Unexpected error: {str(e)}")
        else:
            st.warning("⚠️ Cannot calculate interest on zero or negative balance.")
            st.info("💡 Please deposit some money first to earn interest!")
            
            if st.button("💰 Go to Deposit", type="secondary"):
                st.session_state.current_page = 'deposit'
                st.rerun()
    else:
        st.error("❌ Interest calculation is only available for Savings Accounts.")
        st.info("💡 Current accounts do not earn interest but have overdraft facilities.")
    
    st.divider()
    if st.button("← Back to Dashboard", use_container_width=True):
        st.session_state.current_page = 'dashboard'
        st.rerun()

def main():
    st.set_page_config(
        page_title="SBI Banking System",
        page_icon="🏦",
        layout="centered"
    )
    
    st.title("🏦 SBI Banking System")
    st.markdown("**Nagpur SIT Branch**")
    st.markdown("---")
    
    if st.session_state.current_page == 'main':
        if st.session_state.logged_in_user is None:
            tab1, tab2 = st.tabs(["🔐 Login", "🆕 Create Account"])
            
            with tab1:
                login_page()
            
            with tab2:
                create_account()
        else:
            st.session_state.current_page = 'dashboard'
            st.rerun()
    
    elif st.session_state.current_page == 'dashboard':
        dashboard()
    
    elif st.session_state.current_page == 'deposit':
        deposit_page()
    
    elif st.session_state.current_page == 'withdraw':
        withdraw_page()
    
    elif st.session_state.current_page == 'interest':
        interest_page()
    
    st.markdown("---")
    st.markdown("*Thank you for using SBI Banking System! 🙏*")
    st.markdown("**CRAFTED WITH ❤️ BY SHREYAS KASTURE**")

if __name__ == "__main__":
    main()
