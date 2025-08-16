import os
from datetime import datetime

USERS_FILE = "users.txt"
TRANSACTIONS_FOLDER = "transactions"

def check_files():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as _:
            pass
    if not os.path.exists(TRANSACTIONS_FOLDER):
        os.makedirs(TRANSACTIONS_FOLDER)

def get_transaction_file(username):
    return os.path.join(TRANSACTIONS_FOLDER, f"{username}_transactions.txt")

def login(username, password):
    check_files()
    with open(USERS_FILE, "r") as file:
        for line in file:
            parts = line.strip().split(",")
            if len(parts) >= 3:
                stored_username, stored_password, stored_balance = parts[0], parts[1], float(parts[2])
                if stored_username == username and stored_password == password:
                    return True, stored_balance
    return False, 0.0

def register(username, password, initial_balance):
    check_files()
    with open(USERS_FILE, "a") as file:
        file.write(f"{username},{password},{initial_balance:.2f}\n")
    with open(get_transaction_file(username), "w") as tfile:
        tfile.write(f"{datetime.now()} - Account created with ${initial_balance:.2f}\n")

def update_balance(username, new_balance):
    lines = []
    with open(USERS_FILE, "r") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) >= 2 and parts[0] == username:
                parts[2] = f"{new_balance:.2f}"
                lines.append(",".join(parts) + "\n")
            else:
                lines.append(line)
    with open(USERS_FILE, "w") as f:
        f.writelines(lines)

def record_transaction(username, action, amount, balance):
    with open(get_transaction_file(username), "a") as tfile:
        tfile.write(f"{datetime.now()} - {action} ${amount:.2f} | Balance: ${balance:.2f}\n")

def show_transactions(username):
    path = get_transaction_file(username)
    if os.path.exists(path):
        with open(path, "r") as tfile:
            print("\nTransaction History:")
            print(tfile.read())
    else:
        print("No transactions found.")

def show_balance(balance):
    print(f"Your balance is ${balance:.2f}")

def get_amount(prompt):
    while True:
        try:
            amount = float(input(prompt).strip())
            if amount < 0:
                print("Amount must be non-negative.")
                continue
            return amount
        except ValueError:
            print("Invalid input.")

def make_deposit(username, balance):
    amt = get_amount("How much would you like to deposit? ")
    balance += amt
    record_transaction(username, "Deposited", amt, balance)
    return balance

def withdrawal(username, balance):
    amt = get_amount("How much would you like to withdraw? ")
    if amt > balance:
        print("Insufficient funds.")
        return balance
    balance -= amt
    record_transaction(username, "Withdrew", amt, balance)
    return balance

def main():
    check_files()
    logged_in = False
    current_user = None
    balance = 0.0

    while not logged_in:
        print("\nPython Bank")
        print("A. Register")
        print("B. Log In")
        choice = input("Enter a letter: ").strip().upper()

        if choice == "A":
            user = input("Choose a username: ").strip()
            password = input("Choose a password: ").strip()
            depchoice = input("Initial deposit? (Y/N): ").strip().upper()
            initial = 0.0
            if depchoice == "Y":
                initial = get_amount("How much to deposit? ")
            register(user, password, initial)
            print("Registration successful.")
        elif choice == "B":
            user = input("Enter your username: ").strip()
            password = input("Enter your password: ").strip()
            ok, bal = login(user, password)
            if ok:
                logged_in = True
                current_user = user
                balance = bal
                print(f"Login successful. Loaded balance: ${balance:.2f}")
            else:
                print("Incorrect. Try again.")
        else:
            print("Invalid input.")

    is_running = True
    while is_running:
        print("\nPython Bank")
        print("A. Show Balance")
        print("B. Deposit")
        print("C. Withdraw")
        print("D. Transactions")
        print("E. Quit")
        choice = input("Enter a letter: ").strip().upper()

        if choice == "A":
            show_balance(balance)
        elif choice == "B":
            balance = make_deposit(current_user, balance)
            show_balance(balance)
        elif choice == "C":
            balance = withdrawal(current_user, balance)
            show_balance(balance)
        elif choice == "D":
            show_transactions(current_user)
        elif choice == "E":
            is_running = False
        else:
            print("Invalid input.")

    update_balance(current_user, balance)
    print("Balance saved. Thank you. Goodbye.")

if __name__ == "__main__":
    main()
