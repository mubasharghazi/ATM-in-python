import sqlite3

# Connect to SQLite database (creates a new file if it doesn't exist)
db = sqlite3.connect("atm_simulator.db")

# Create a cursor object to interact with the database
cursor = db.cursor()

# Create a table to store account information if it doesn't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS accounts (
        account_number INTEGER PRIMARY KEY,
        pin INTEGER,
        balance REAL
    )
""")

# Function to fetch account info
def fetch_account_info(account_number):
    cursor.execute("SELECT * FROM accounts WHERE account_number = ?", (account_number,))
    return cursor.fetchone()

# Function to handle login
def login():
    account_number = input("Enter your account number: ")
    pin = input("Enter your PIN: ")

    # Check if account exists
    cursor.execute("SELECT * FROM accounts WHERE account_number = ? AND pin = ?", (account_number, pin))
    account_info = cursor.fetchone()

    if account_info:
        print("Logged in successfully.")
        return account_info
    else:
        print("Invalid account number or PIN.")
        return None

# Function to handle account creation
def create():
    account_number = input("Enter a new account number: ")
    pin = input("Enter a new PIN: ")

    # Check if account number already exists
    cursor.execute("SELECT * FROM accounts WHERE account_number = ?", (account_number,))
    if cursor.fetchone():
        print("Account number already exists.")
        return

    cursor.execute("INSERT INTO accounts (account_number, pin, balance) VALUES (?, ?, ?)",
                   (account_number, pin, 0.0))
    db.commit()
    print("Account created successfully.")

# Function to handle deposit
def deposit(account_info):
    amount = input("Enter the amount to deposit: ")

    # Check if amount is a valid number
    try:
        amount = float(amount)
    except ValueError:
        print("Invalid amount.")
        return

    new_balance = account_info[2] + amount
    cursor.execute("UPDATE accounts SET balance = ? WHERE account_number = ?", (new_balance, account_info[0]))
    db.commit()
    print(f"Deposited successfully. Your new balance is {new_balance}.")
    return fetch_account_info(account_info[0])

# Function to handle withdrawal
def withdraw(account_info):
    amount = input("Enter the amount to withdraw: ")

    # Check if amount is a valid number
    try:
        amount = float(amount)
    except ValueError:
        print("Invalid amount.")
        return

    if account_info[2] >= amount:
        new_balance = account_info[2] - amount
        cursor.execute("UPDATE accounts SET balance = ? WHERE account_number = ?", (new_balance, account_info[0]))
        db.commit()
        print(f"Withdrew successfully. Your new balance is {new_balance}.")
        return fetch_account_info(account_info[0])
    else:
        print("Insufficient balance.")
        return account_info

# Function to check balance
def check_balance(account_info):
    cursor.execute("SELECT balance FROM accounts WHERE account_number = ?", (account_info[0],))
    balance = cursor.fetchone()[0]
    print(f"Your current balance is {balance}.")

# Main program loop
account_info = None
while True:
    print("\n1. Login")
    print("2. Create account")
    print("3. Deposit")
    print("4. Withdraw")
    print("5. Check Balance")
    print("6. Exit")
    choice = input("Enter your choice: ")

    if choice == '1':
        account_info = login()
    elif choice == '2':
        create()
    elif choice == '3':
        if account_info:
            account_info = deposit(account_info)
        else:
            print("You need to login first.")
    elif choice == '4':
        if account_info:
            account_info = withdraw(account_info)
        else:
            print("You need to login first.")
    elif choice == '5':
        if account_info:
            check_balance(account_info)
        else:
            print("You need to login first.")
    elif choice == '6':
        print("Thank you for using our ATM. Goodbye!")
        break
    else:
        print("Invalid choice.")

# Close database connection when the program exits
cursor.close()
db.close()