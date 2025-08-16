import os

USERS_FILE = "users.txt"

def check_users_file():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as _:
            pass

def login(username, password):
    ensure_users_file()
    with open(USERS_FILE, "r") as file:
        for line in file:
            parts = line.strip().split(",")
            if len(parts) < 2:
                continue
            stored_username, stored_password = parts[0], parts[1]
            stored_balance = float(parts[2]) if len(parts) >= 3 else 0.0
            if stored_username == username and stored_password == password:
                return True, stored_balance
    return False, 0.0

def register(username, password, initial_balance):
    check_users_file()
    with open(USERS_FILE, "a") as file:
        file.write(f"{username},{password},{initial_balance:.2f}\n")

def update_balance(username, new_balance):
    check_users_file()
    lines = []
    with open(USERS_FILE, "r") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) >= 2 and parts[0] == username:
                if len(parts) == 2:
                    parts.append(f"{new_balance:.2f}")
                else:
                    parts[2] = f"{new_balance:.2f}"
                lines.append(",".join(parts) + "\n")
            else:
                lines.append(line)
    with open(USERS_FILE, "w") as f:
        f.writelines(lines)

def show_balance(balance):
    print(f"Your balance is ${balance:.2f}")

def get_amount(prompt):
    while True:
        user_input = input(prompt).strip()
        try:
            amount = float(user_input)
            if amount < 0:
                print("Amount must be non-negative.")
                continue
            return amount
        except ValueError:
            print("Invalid input. Please enter a number (e.g., 25 or 25.50).")

def make_deposit():
    return get_amount("How much would you like to deposit? ")

def withdrawal(balance):
    amt = get_amount("How much would you like to withdraw? ")
    if amt > balance:
        print("Insufficient funds.")
        return 0.0
    return amt

def main():
    check_users_file()
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
        print("D. Quit")
        choice = input("Enter a letter: ").strip().upper()

        if choice == "A":
            show_balance(balance)
        elif choice == "B":
            balance += make_deposit()
            show_balance(balance)
        elif choice == "C":
            balance -= withdrawal(balance)
            show_balance(balance)
        elif choice == "D":
            is_running = False
        else:
            print("Invalid input.")

    update_balance(current_user, balance)
    print("Balance saved. Thank you. Goodbye.")

if __name__ == "__main__":
    main()
