# streamlit_app.py
import streamlit as st
from Banking.account import SavingsAccount, CurrentAccount
from Banking.transactions import deposit, withdraw

# Initialize session state for accounts
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
    
    # Header
    st.subheader(f"👋 Welcome, {user_account.name}!")
    
    # Account info in columns
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Account Number", user_account.account_number)
    with col2:
        st.metric("Account Type", type(user_account).__name__)
    with col3:
        st.metric("Current Balance", f"₹{user_account.get_balance():.2f}")
    
    st.divider()
    
    # Action buttons in columns
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
        amount = st.number_input("Enter amount to deposit:", min_value=0.01, step=0.01)
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
    
    st.info(f"Current Balance: ₹{user_account.get_balance():.2f}")
    
    with st.form("withdraw_form"):
        amount = st.number_input("Enter amount to withdraw:", min_value=0.01, step=0.01)
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
        st.info(f"Current Balance: ₹{user_account.get_balance():.2f}")
        
        if st.button("Calculate Interest", type="primary"):
            try:
                old_balance = user_account.get_balance()
                user_account.calculate_interest()
                new_balance = user_account.get_balance()
                interest_earned = new_balance - old_balance
                
                st.success(f"✅ Interest calculated successfully!")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Interest Earned", f"₹{interest_earned:.2f}")
                with col2:
                    st.metric("New Balance", f"₹{new_balance:.2f}")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    if st.button("← Back to Dashboard"):
        st.session_state.current_page = 'dashboard'
        st.rerun()

def main():
    # Page config
    st.set_page_config(
        page_title="SBI Banking System",
        page_icon="🏦",
        layout="centered"
    )
    
    # Header
    st.title("🏦 SBI Banking System")
    st.markdown("**Nagpur SIT Branch**")
    st.markdown("---")
    
    # Navigation based on current page
    if st.session_state.current_page == 'main':
        if st.session_state.logged_in_user is None:
            # Main menu
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
    
    # Footer
    st.markdown("---")
    st.markdown("*Thank you for using SBI Banking System! 🙏*")
    st.markdown("*Made with ❤️ by Shreyas Kasture*")    

if __name__ == "__main__":
    main()
