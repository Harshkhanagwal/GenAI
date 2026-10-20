# Bank Account Management System
import json
import random
import string
from pathlib import Path

class Bank:
    database = 'data.json'
    data = []

    # Safe file loading block (Runs when the class is initially evaluated)
    try:
        path = Path(database)
        if path.exists():
            if path.stat().st_size > 0:
                with open(database, "r") as fs:
                    # FIX: Explicitly bind the loaded data to Bank.data so all methods can see it
                    Bank.data = json.loads(fs.read())
            else:
                Bank.data = [] 
        else:
            # If database doesn't exist, start fresh and create it
            Bank.data = []
    except Exception as err:
        print(f"An exception occurred as: {err}")

    @staticmethod
    def update(info=None):
        with open(Bank.database, "w") as fs:
            fs.write(json.dumps(Bank.data, indent=4)) 

    @classmethod
    def __accountGen(cls):
        alpha = random.choices(string.ascii_letters, k=3)
        num = random.choices(string.digits, k=3)
        spchar = random.choices("!@#$%^&*", k=1)

        id_list = alpha + num + spchar
        random.shuffle(id_list)
        return "".join(id_list)

    def createaccount(self):
        print("\n--- CREATE ACCOUNT ---")
        info = {
            "name" : input("Tell Your name :- "),
            "age" : int(input("Tell your age :- ")),
            "email" : input("Tell your email :- "),
            "pin" : int(input("Create 4 digit pin :- ")),
            "accountNo." : Bank.__accountGen(),
            "balance" : 0
        }

        if info['age'] < 13:
            print("Sorry, can't create account for user with age less than 13.")
        elif len(str(info["pin"])) != 4: 
            print("PIN should be exactly 4 digits.")
        else:
            print("\nAccount has been created successfully!")
            for key in info:
                print(f"{key} : {info[key]}")
            print("Please note down your account number safely.")

            Bank.data.append(info)
            Bank.update(info)

    def depositmoney(self):
        print("\n--- DEPOSIT MONEY ---")
        accnumber = input("Enter your acc no. : ")
        try:
            pin = int(input("Enter your 4 digit pin : "))
        except ValueError:
            print("Invalid PIN format!")
            return

        # FIX: Check using 'if not userdata:' instead of '== False'
        userdata = [i for i in Bank.data if i['accountNo.'] == accnumber and i['pin'] == pin]

        if not userdata:
            print("Sorry, no data found or Wrong pin.")
        else:
            amount = int(input("Enter value to be Deposited : "))

            if amount > 100000 or amount <= 0:
                print("Sorry, amounts between 1 and 100,000 can be deposited.")
            else:
                userdata[0]['balance'] += amount
                Bank.update()
                print(f"Amount has been deposited successfully. New Balance: {userdata[0]['balance']}")

    def withdrawmoney(self):
        print("\n--- WITHDRAW MONEY ---")
        accnumber = input("Enter your acc no. : ")
        try:
            pin = int(input("Enter your 4 digit pin : "))
        except ValueError:
            print("Invalid PIN format!")
            return

        userdata = [i for i in Bank.data if i['accountNo.'] == accnumber and i['pin'] == pin]

        if not userdata:
            print("Sorry, no data found or Wrong pin.")
        else:
            amount = int(input("Enter value to be Withdrawn : "))

            if amount > userdata[0]['balance']:
                print("Sorry, you don't have that much money in your account.")
            elif amount <= 0:
                print("Invalid withdrawal amount.")
            else:
                userdata[0]['balance'] -= amount
                Bank.update()
                print(f"Amount has been withdrawn. New Balance: {userdata[0]['balance']}")

    def showdetails(self):
        print("\n--- ACCOUNT DETAILS ---")
        accnumber = input("Enter your acc no. : ")
        try:
            pin = int(input("Enter your 4 digit pin : "))
        except ValueError:
            print("Invalid PIN format!")
            return
    
        userdata = [i for i in Bank.data if i['accountNo.'] == accnumber and i['pin'] == pin]
    
        if not userdata:
            print("Sorry, no data found or Wrong pin.")
        else:
            # FIX: Used single quotes internally to prevent breaking Python's f-string parsing
            print(f"Account No. : {userdata[0]['accountNo.']}")
            print(f"User name   : {userdata[0]['name']}")
            print(f"User email  : {userdata[0]['email']}")
            print(f"User Age    : {userdata[0]['age']}")
            print(f"Balance     : {userdata[0]['balance']}")

    def updatedetails(self):
        print("\n--- UPDATE DETAILS ---")
        accnumber = input("Enter your acc no. : ")
        try:
            pin = int(input("Enter your 4 digit pin : "))
        except ValueError:
            print("Invalid PIN format!")
            return
            
        userdata = [i for i in Bank.data if i['accountNo.'] == accnumber and i['pin'] == pin]

        if not userdata:
            print("Sorry, no data found or Wrong pin.")
        else:
            print("You can't change your age, account number, or balance.")
            print("Fill details to modify them, or press Enter/leave blank to keep current setup.")

            new_name = input("Please tell your New Name (Leave blank to skip): ")
            new_email = input("Please tell your New Email (Leave blank to skip): ")
            raw_pin = input("Please enter your New 4-digit PIN (Leave blank to skip): ")

            # FIX: Perform in-place updates on the verified database record directly
            if new_name != "":
                userdata[0]["name"] = new_name
 
            if new_email != "":
                userdata[0]["email"] = new_email
 
            if raw_pin != "":
                if len(raw_pin) == 4 and raw_pin.isdigit():
                    userdata[0]["pin"] = int(raw_pin)
                else:
                    print("Warning: PIN modification skipped (Invalid input framework: must be 4 digits).")

            Bank.update()
            print("Profile specifications altered smoothly.")

    def deleteUser(self):
        print("\n--- DELETE ACCOUNT ---")
        accnumber = input("Enter your acc no. : ")
        try:
            pin = int(input("Enter your 4 digit pin : "))
        except ValueError:
            print("Invalid PIN format!")
            return
                    
        userdata = [i for i in Bank.data if i['accountNo.'] == accnumber and i['pin'] == pin]
        
        if not userdata:
            print("Sorry, no data found or Wrong pin.")
        else:
            check = input("Press Y if you want to permanently delete your Account or N for No: ")

            if check.lower() == 'y':
                index = Bank.data.index(userdata[0])
                Bank.data.pop(index)
                print("Account deleted successfully.")
                Bank.update()
            else:
                print("Deletion cancelled by user.")

# --- CONSOLE INTERFACE ---
user = Bank()

print("==============================")
print("Welcome to Basic Bank Management System")
print("==============================")
print("1 : Create account")
print("2 : Deposit money")
print("3 : Withdraw money")
print("4 : Account details")
print("5 : Update details")
print("6 : Delete account")
print("==============================")

try:
    check = int(input("Choose your option (1 - 6) : "))
    if check == 1: user.createaccount()
    elif check == 2: user.depositmoney()
    elif check == 3: user.withdrawmoney()
    elif check == 4: user.showdetails()
    elif check == 5: user.updatedetails()
    elif check == 6: user.deleteUser()
    else: print("Error: Option must be between 1 and 6.")
except ValueError:
    print("Invalid option. Please input an integer numeric value.")