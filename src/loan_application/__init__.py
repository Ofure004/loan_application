from tabulate import tabulate
import plotext as plt
import numpy
import json
import os


# class person:
#     def __init__(self, name, loanamount, interestrate, balance, start_month, compound):
#         self.name = name
#         self.loanamount = loanamount
#         self.interestrate = interestrate
#         self.balance = balance
#         self.start_month = start_month
#         self.compound = compound


# people: list[person] = []



def main():
    plt.xlabel("month")
    plt.ylabel("$")
    plt.theme("pro")
    plt.plot_size(30, 15)
    login()
    return 0


def login():

    with open('src/loan_application/users.json', 'r') as f:
        data = json.load(f)

    users = {}

    print("Are you an admin or a user?: ")
    role = input("> ").lower()

    if role == "admin":
        user = data['admin']
        user_type = "admin"
        app(user ,user_type)
    else:
        user_type = 'user'
        print("Are you a new user?(y/n)")
        new = input("> ").lower()
        if new in ["y", "yes"]:
            register()
        elif new in ["n", "no"]:
            with open('src/loan_application/users.json', 'r') as f:
                data = json.load(f)
                for user in data:
                    if data[user]["type"] == 'user':
                        users[data[user]['name']] = data[user]

                print("Current Accounts:")
                for user in users:
                    print("->", users[user]['name'])
            while True:
                user_input = input("Choose your username from the ones listed above: ").lower()
                if (user_input in users):
                    os.system('clear')
                    user = users[user_input]
                    app(user,user_type)
                    break
                else:
                    print("User does not exist! Try again.")
                # name = input("> ").lower()
                # for i in [p.name for p in people]:
                #     if name == i:
                #         print("matches!!")
            print("Invalid option")




def iscompound(comp: str) -> str:
    option = ""
    if comp == "y" or comp == "yes":
        option = "compound"
    elif comp == "n" or comp == "no":
        option = "simple"
    else:
        print("The option picked is invalid")
    return option


def register():
    print("Do you want to get a loan? (y/n): ")
    user_input = input("> ").lower() 

    if user_input == "y":
        print("What is your name?: ")
        name = input("> ").lower()

        print("Indicate if you want to use compound interest (y/n):")
        comp = input("> ").lower()
        compound = iscompound(comp)

        print("What month did you start? eg. january: ")
        mth = input("> ")
        loanamount: float = float(input("Enter loan amount: $"))
        interestrate: float = float(input("Enter interest rate in decimal: "))
        balance = loanamount
        users = {
                "name": name,
                "type": "user",
                "loan": loanamount,
                "rate": interestrate,
                "compound": compound,
                "balance": balance,
                "payments": [],
                "start_month": mth,
                "current_month": 1
        }

        save_user(users)
        redirect = input("Redirecting you to the main page to login as an existing user, type okay to confirm: ").lower()
        if redirect == 'okay' or redirect == 'ok':
            main()
            os.system('clear')
        else:
            print("No valid answer chosen")
        


    elif user_input == "n":
        quit()


def save_user(user):
    with open('src/loan_application/users.json', 'r') as f:
        data = json.load(f)

    with open('src/loan_application/users.json', 'w') as f:
        data[user['name']] = user
        json.dump(data, f, indent=4, sort_keys=True)

def app(user, user_type):
    if user_type == 'user': 
        print("Hello there",user['name'], "here are your details for this session")
        print("You initially borrowed", user['loan'])
        print(
            "You currently have",user['balance'],
            "to pay out of the",
            user['loan'],
            "you took",
            "since you're paying at a rate of",
            user['rate'],
            "since the month of",
            user['start_month'],
        )
        print("Since you have chosen the", user['compound'], "interest option")
        
        increase = input("new month? (y/n)").lower()
        if increase == 'y':
            advance()
        
        loans = input("Please type 'pay' if you want to make payments in your already existing loan and 'new' for a new loan: ").lower()

        
        if loans == 'pay':
            loan_repayment(user)
        else:
            createloan(user)

        option = input("type back to go back to main menu or exit to quit: ").lower()
        
        if option == 'back':
            os.system('clear')
            main()
        elif option == 'exit':
            os.system('clear')
            quit()
        
    elif user_type == "admin":
        admin_stuff(user)
    else:
        print("Invalid role")

def admin_stuff(user):
    print("Hello", user['name'], "these are your stats")
    total = 0

    for payment in user['payments']:
        total += payment[1]

    print("Total loan repayments are $", total )

    if len(user['payments']) != 0:
        print("Payment Reciepts")
        print(tabulate(user['payments'], headers=['Month', 'Payment'], floatfmt=('.2f'), tablefmt='grid'))

    option = input("Do you want payment predictions?(y/n): ").lower()
    if option == 'y' or option == 'yes':
        prediction(user)
    elif option == 'n' or 'no':
        redirect = input("Redirecting you back to the login page, type okay to confirm").lower()
        if redirect == 'okay':
            login()
        else:
            print("Invalid option")


def prediction(user):
    max_month = user['current_month'] -1
    months = []
    payments = []

    for payment in user['payments']:
         months.append(payment[0])
         payments.append(payment[1])

    reg = numpy.polynomial.Polynomial.fit(
        months,
        payments,
      1
    )

    plt.cld()
    plt.plot(months, payments, marker="braille")
    plt.plot(
        [max_month, max_month + 1, max_month + 2, max_month + 3],
        [payments[-1], reg(max_month + 1), reg(max_month + 2), reg(max_month + 3)],
        marker="braille"
    )

    xticks= months
    xticks.extend([max_month + 1, max_month + 2, max_month + 3])

    plt.xticks(xticks, xticks)

    plt.yticks([x for x in payments], [format(x, ".2f") for x in payments])

    payment_graph = plt.build()
    print("Loan repayment graph")
    print("Predictions for future payments in green")
    print(payment_graph)




def createloan(user):
    loanamount: float = float(input("Enter loan amount: $"))
    interestrate: float = float(input("Enter interest rate in decimal: "))
    print("Indicate if you want to use compound interest (y/n):")
    comp = input("> ").lower()
    compound = iscompound(comp)

    updated_user ={
        "name": user['name'],
        "type": "user",
        "loan": loanamount,
        "rate": interestrate,
        "compound": compound,
        "balance": loanamount + (loanamount * interestrate),
        "payments":  user['payments'],
        "start_month": user['start_month'],
        "current_month": user['current_month'],
    }
    save_user(updated_user)
    os.system('clear')
    print("Hello there",updated_user['name'], "here are your details for this session")
    print("You initially borrowed", updated_user['loan'])
    print(
        "You currently have",updated_user['balance'],
        "to pay out of the",
        updated_user['loan'],
        "you took",
        "since you're paying at a rate of",
        updated_user['rate'],
        "since the month of",
        updated_user['start_month'],
    )
    print("Since you have chosen the", updated_user['compound'], "interest option")




# def admin_payment_prediction(user):
#     print("Hello there")
#    max_month = user['current_month'] -1
#     months = []
#     payments = []

#     for payment in user['payments']:
#          months.append(payment[0])
#          payments.append(payment[1])

#     reg = numpy.polynomial.Polynomial.fit(
#         months,
#         payments,
#       1
#     )

#     plt.cld()
#     plt.plot(months, payments, marker="braille")
#     plt.plot(
#         [max_month, max_month + 1, max_month + 2, max_month + 3],
#         [payments[-1], reg(max_month + 1), reg(max_month + 2), reg(max_month + 3)],
#         marker="braille",
#     )

#     xticks= months
#     xticks.extend([max_month + 1, max_month + 2, max_month + 3])

#     plt.xticks(xticks, xticks)

#     plt.yticks([x for x in payments], [format(x, ".2f") for x in payments])

#     payment_graph = plt.build()
#     print("Loan repayment graph")
#     print("Predictions for future payments in green")
#     print(payment_graph)

#     print("MENU --------")
#     print("1.Go back to Main Menu")
#     print("2. View Payment Stats")

#     while True:
#         user_input = input("Enter Option: ")
#         if user_input == '1':
#             os.system('clear')
#             admin_dash(user)
#             break
#         elif user_input == '2':
#             os.system('clear')
#             admin_payment_stats(user)
#             break
#         else:
#             print('Invalid option! Try again.')

# 

def advance():
    with open('src/loan_application/users.json', 'r') as f:
            data = json.load(f)

    for user in data:
        data[user]['current_month'] += 1
        if 'balance' in data[user]:
            if data[user]['compound'] == 'compound':
                data[user]['balance'] *= (1 + data[user]['rate'])
            else:
                data[user]['balance'] += data[user]['loan'] * data[user]['rate']
        save_user(data[user])

    return "New Month!!"




def loan_repayment(user):

    print("This is to make payments on your loan")
    payment: float = float(input("Enter payment amount: $"))
    
    with open('src/loan_application/users.json', 'r') as f:
            data = json.load(f)
    admin = data['admin']
    admin_payments = admin['payments']

    month = user['current_month']
    payments = user['payments']
    balance = user['balance']
    admin = data['admin']

    admin_payments = admin['payments']

    if payment >= balance:
        payment = balance
        balance = 0
    else:
        balance -= payment
        if user['compound'] == 'compound':
            balance *= (1 + user['rate'])
        else:
            balance += user['loan'] * user['rate']

    payments.append([month, payment, balance])

    if admin['payments'] == []:
        admin['payments'].append([month, payment])
    else:
        if len([entry for entry in admin['payments'] if entry[0] == month]) == 1:
            admin['payments'][month - 1][1] += payment
        else:
            admin_payments.append([month, payment])

    save_user(admin)
    user['payments'] = payments
    user['balance'] = balance

    save_user(user)
    os.system('clear')
    
    app(user, user['type'])
