# from tabulate import tabulate
# import os
# import json
# import numpy
# import plotext as plt

# def main() -> int:
#     print("Welcome to the Loan Repayment App!")
#     print("MENU --------")
#     print("1. Register")
#     print("2. Login")
#     print("3. Exit")

#     plt.xlabel("month")
#     plt.ylabel("$")
#     plt.theme("pro")
#     plt.plot_size(30, 15)

#     while True:
#         user_input = input("Enter your choice: ")
#         if user_input == '1':
#             os.system('clear')
#             register()
#             break
#         elif user_input == '2':
#             os.system('clear')
#             login()
#             break
#         elif user_input == '3':
#             print("Exiting...")
#             return 0
#         else:
#             print("Invalid input! Try again.")
#     return 0

# # def login():
#     data = get_users()

#     user_type = account_type()

#     users = {}

#     for user in data:
#         if data[user]["type"] == user_type:
#             users[data[user]['name']] = data[user]

#     print("Current Accounts:")
#     for user in users:
#         print("->", users[user]['name'])


#     while True:
#         user_input = input("Enter a username from the list: ").lower()
#         if (user_input in users):
#             os.system('clear')
#             user = users[user_input]
#             app(user, user_type)
#             break
#         else:
#             print("User does not exist! Try again.")

# def get_user(name):
#     with open('src/loan_app/data.json', 'r') as f:
#         data = json.load(f)

#     for user in data:
#         if name == data[user]['name']:
#             return data[user]

# # def get_users():
#     with open('src/loan_app/data.json', 'r') as f:
#         data = json.load(f)
#     return data

# # def account_type() -> str:
#     while True:
#         user_type = input("Choose account type (admin/user): ").lower()
#         if user_type == 'admin' or user_type == 'user' :
#             os.system('clear')
#             break
#         else:
#             print("Invalid user type!")
#     return user_type

# # def register() -> int:
#     name = input("Enter your name: ")
#     loan: float = float(input("Enter loan amount: $"))
#     rate: float = float(input("Enter interest rate in decimal: "))
#     compound = input("Compound Interest (yes/no)? ").lower()

#     user = {
#         "name": name,
#         "type": "user",
#         "loan": loan,
#         "rate": rate,
#         "compound": True if compound == 'yes' else False,
#         "balance": loan + (loan * rate),
#         "payments": [],
#         "current_month": 1,
#     }

#     save_user(user)
#     os.system('clear')

#     app(user, user['type'])
#     return 0

# # def save_user(user):
#     with open('src/loan_app/data.json', 'r') as f:
#         data = json.load(f)

#     with open('src/loan_app/data.json', 'w') as f:
#         data[user['name']] = user
#         json.dump(data, f, indent=4, sort_keys=True)

# # def app(user, user_type) -> int:
#     if user_type == 'user':
#         user_dash(user)
#     else:
#         admin_dash(user)

#     return 0

# # def draw_user_app(user):
#     print("Welcome,", user['name'], "!")
#     print("Month:", user['current_month'])
#     print("You owe", user['balance'], "out of a", user['loan'], "at", user['rate']*100, "% rate.")
#     print("---------------------------")

#     if user['payments'] != []:
#         print("Payment Reciepts")
#         print(tabulate(user['payments'], headers=['Month', 'Payment', 'Balance'], floatfmt=('.2f'), tablefmt='grid'))

#     print()
#     print("MENU --------")

#     balance = user['balance']

#     if balance > 0:
#         print("1. Make Payment")
#     else:
#         print("1. New Loan")

#     print("2. Advance Month")
#     print("3. Log out")
#     print("4. Exit App")


# def user_dash(user):
#     draw_user_app(user)
#     name = user['name']
#     balance = user['balance']

#     while True:
#         user_input = input("Enter option: ")

#             if user_input == '1':
#             if balance > 0:
#                 user = make_payment(user)
#                 save_user(user)
#                 os.system('clear')
#                 user_dash(user)
#                 # draw_user_app(user)
#                 break
#             else:
#                 os.system('clear')
#                 user = new_loan(user)
#                 os.system('clear')
#                 user_dash(user)
#         elif user_input == '2':
#             os.system('clear')
#             res = advance()
#             print(res)
#             user = get_user(name)
#             draw_user_app(user)
#         elif user_input == '3':
#             os.system('clear')
#             logout()
#             break
#         elif user_input == '4':
#             os.system('clear')
#             quit()
#             break
#         else:
#             print('Invalid option! Try again.')

# def advance():
#     data = get_users()

#     for user in data:
#         data[user]['current_month'] += 1
#         if 'balance' in data[user]:
#             if data[user]['compound'] == True:
#                 data[user]['balance'] *= (1 + data[user]['rate'])
#             else:
#                 data[user]['balance'] += data[user]['loan'] * data[user]['rate']
#         save_user(data[user])

#     return "Success!"

# def new_loan(user):
#     loan: float = float(input("Enter loan amount: $"))
#     rate: float = float(input("Enter interest rate in decimal: "))
#     compound = input("Compound Interest (yes/no)? ").lower()

#     new_user = {
#         "name": user['name'],
#         "type": "user",
#         "loan": loan,
#         "rate": rate,
#         "compound": True if compound == 'yes' else False,
#         "balance": loan + (loan * rate),
#         "payments":  user['payments'],
#         "current_month": user['current_month'],
#     }

#     save_user(new_user)
#     return new_user

# def logout():
#     main()

# def draw_admin_app(user):
#     print("Welcome,", user['name'], "!")
#     print("Current Month:", user['current_month'])
#     print("---------------------------")
#     print("MENU --------")
#     print("1. View Payment Stats")
#     print("2. View Payment Prediction")
#     print("3. Advance Month")
#     print("4. Log out")
#     print("5. Exit App")

# def admin_dash(user):
#     draw_admin_app(user)
#     name = user['name']

#     while True:
#         user_input = input("Enter option: ")
#         if user_input == '1':
#             os.system('clear')
#             admin_payment_stats(user)
#         elif user_input == '2':
#             os.system('clear')
#             admin_payment_prediction(user)
#         elif user_input == '3':
#             os.system('clear')
#             res = advance()
#             user = get_user(name)
#             draw_admin_app(user)
#             print(res)
#         elif user_input == '4':
#             os.system('clear')
#             logout()
#             break
#         elif user_input == '5':
#             os.system('clear')
#             quit()
#             break
#         else:
#             print('Invalid option! Try again.')

# def admin_payment_prediction(user):
#     max_month = user['current_month'] -1
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

# def admin_payment_stats(user):
#     total = 0

#     for payment in user['payments']:
#         total += payment[1]

#     print("Total loan repayments for month", user['current_month'], "is $", total )

#     if user['payments'] != []:
#         print("Payment Reciepts")
#         print(tabulate(user['payments'], headers=['Month', 'Payment'], floatfmt=('.2f'), tablefmt='grid'))

#     print("MENU --------")
#     print("1.Go back to Main Menu")
#     print("2. View Payment Prediction")

#     while True:
#         user_input = input("Enter Option: ")

#         if user_input == '1':
#             os.system('clear')
#             admin_dash(user)
#             break
#         elif user_input == '2':
#             os.system('clear')
#             admin_payment_prediction(user)
#             break
#         else:
#             print('Invalid option! Try again.')


# def make_payment(user):
#     month = user['current_month']
#     payments = user['payments']
#     balance = user['balance']

#     data = get_users()
#     admin = data['admin']

#     admin_payments = admin['payments']

#     payment: float = float(input("Enter payment amount: $"))

#     if payment >= balance:
#         payment = balance
#         balance = 0
#     else:
#         balance -= payment
#         if user['compound'] == True:
#             balance *= (1 + user['rate'])
#         else:
#             balance += user['loan'] * user['rate']

#     payments.append([month, payment, balance])

#     current_id = 0
#     if admin['payments'] == []:
#         admin['payments'].append([month, payment])
#     else:
#         if len([entry for entry in admin['payments'] if entry[0] == month]) == 1:
#             admin['payments'][month - 1][1] += payment
#         else:
#             admin_payments.append([month, payment])

#     save_user(admin)
#     user['payments'] = payments

#     return user