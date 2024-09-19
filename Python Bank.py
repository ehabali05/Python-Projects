def show_balance(balance):
    print(f"Your balance is ${balance:.2f}")

def make_deposit():
    amount = float(input("How much would you like to deposit? "))
    if amount < 0:
        print("Invalid number")
    else:
        return amount

def withdrawal(balance):
    withdrawn = float(input("How much would you like to withdraw? "))
    if withdrawn>balance:
        print("Insufficient funds.")
        return 0
    elif withdrawn<0:
        print("Amount must be greater than 0")
        return 0
    else:
        return withdrawn

def main():
    balance = 0
    is_running = True

    while is_running == True:
        print("Python Bank")
        print("A. Show Balance")
        print("B. Deposit")
        print("C. Withdraw")
        print("D. Quit")

        choice = input("Enter a Letter: ")

        if choice == 'A':
            show_balance(balance)
        elif choice == 'B':
           balance += make_deposit()
        elif choice == 'C':
            balance -= withdrawal(balance)
        elif choice == 'D':
            is_running = False
        else:
            print("Invalid input")

            
    print("Thank you. Goodbye.")

if __name__ == '__main__':
    main()       
