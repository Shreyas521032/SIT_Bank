# 🏦 SBI Banking System

A modern web-based banking application built with Python and Streamlit, featuring account management, transactions, and interest calculations.

## 🌐 Live Demo

**🚀 Try the app live:** [https://shreyas-sitbank.streamlit.app/](https://shreyas-sitbank.streamlit.app/)

## ✨ Features

### 🔐 Account Management
- **Create Account**: Set up new Savings or Current accounts
- **Secure Login**: Access accounts using unique account numbers
- **Account Types**: 
  - 💰 **Savings Account**: Includes interest calculation feature
  - 🏢 **Current Account**: Standard business account functionality

### 💸 Transaction Operations
- **Deposit Money**: Add funds to your account
- **Withdraw Money**: Remove funds with balance validation
- **Balance Inquiry**: View current account balance in real-time
- **Interest Calculation**: Automatic interest computation for savings accounts

### 🎨 User Experience
- **Modern UI**: Clean, intuitive Streamlit interface
- **Real-time Updates**: Instant balance updates after transactions
- **Visual Feedback**: Success/error messages with emojis
- **Responsive Design**: Works seamlessly on desktop and mobile

## 🛠️ Technology Stack

- **Backend**: Python 3.x
- **Frontend**: Streamlit
- **Architecture**: Object-Oriented Programming (OOP)
- **Deployment**: Streamlit Cloud

## 📁 Project Structure

```
shreyas-sitbank/
├── streamlit_app.py          # Main Streamlit application
├── requirements.txt          # Python dependencies
├── Banking/                  # Core banking modules
│   ├── __init__.py
│   ├── account.py           # Account classes (Savings/Current)
│   └── transactions.py      # Transaction functions
└── README.md               # This file
```

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd shreyas-sitbank
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run streamlit_app.py
   ```

4. **Access the app**
   Open your browser and go to `http://localhost:8501`

## 📖 How to Use

### 1️⃣ **Create Account**
- Navigate to the "Create Account" tab
- Enter your name and select account type
- Set initial balance
- Note down your auto-generated account number

### 2️⃣ **Login**
- Use the "Login" tab
- Enter your account number
- Access your dashboard

### 3️⃣ **Perform Transactions**
- **Deposit**: Add money to your account
- **Withdraw**: Remove money (subject to balance availability)
- **Check Balance**: View current balance
- **Calculate Interest**: (Savings accounts only) Compute and add interest

## 🏗️ Architecture

### Core Classes
- **`SavingsAccount`**: Savings account with interest calculation
- **`CurrentAccount`**: Standard current account functionality
- **`Transaction Functions`**: Deposit and withdrawal operations

### Key Features
- **Session Management**: Maintains user state across pages
- **Input Validation**: Ensures data integrity
- **Error Handling**: Graceful error management
- **Security**: Account number-based authentication

## 🌟 Branch Information

**SBI Nagpur SIT Branch**
- Modern banking solutions
- Student-friendly interface
- Secure transaction processing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

**🏦 Experience modern banking with SBI Digital Banking System!**
