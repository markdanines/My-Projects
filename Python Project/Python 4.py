import tkinter
from tkinter import messagebox
import pickle


##############################################################
# USER OBJECTS
##############################################################

# Class for all Users including admin
class User:

    def __init__(self, name, user_name, user_pin, adminstat):
        self.__name = name
        self.__user_name = user_name
        self.__user_pin = user_pin
        self.__balance = 0
        self.__is_admin = adminstat

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_user_name(self):
        return self.__user_name

    def set_user_name(self, user):
        self.__user_name = user

    def get_pin(self):
        return self.__user_pin

    def set_pin(self, pin):
        self.__user_pin = pin

    def add_bal(self, amount):
        self.__balance += amount

    def sub_bal(self, amount):
        self.__balance -= amount

    def get_bal(self):
        return self.__balance

    def get_admin_status(self):
        return self.__is_admin


# Class for administrator which inherits from the user class
class Admin(User):

    def __init__(self, name, user_name, user_pin, adminstat):
        super().__init__(name, user_name, user_pin, adminstat)


##############################################################
# ATM OBJECT
##############################################################

# Class for the atm machine
class Atm:

    # Initialization Function
    def __init__(self):
        self.admin = Admin('daniel', 'dan', '1234', True)
        self.__user_list = self.load_users()
        self.__current_user = None
        self.current_screen = self.create_login()

    # Load User List from file
    def load_users(self):
        f = open('/Users/daniel/desktop/accounts.dat', 'rb')
        accounts = pickle.load(f)
        f.close()
        return accounts

    # Get List of Users
    def get_users(self):
        return self.__user_list

    # Set Current List
    def add_users(self, user):
        self.__user_list.append(user)

    def set_users_list(self, lst):
        self.__user_list = lst

    # Get the current user
    def get_current_user(self):
        return self.__current_user

    # Set the Current User
    def set_current_user(self, user):
        self.__current_user = user

    def create_login(self):
        self.current_screen = LoginScreen('Log-In', self)


##############################################################
# SCREEN OBJECTS
##############################################################


# Screen objects that will be in the atm object, each screen will have its own set of available methods
class Screens:

    #   Screen Object Initialization
    def __init__(self, title, obj):
        self.root = tkinter.Tk()
        self.root.title = title
        self.root.geometry('400x300')
        self.obj = obj

    #   Method that exits/quits
    def quit_screen(self):
        self.root.destroy()

    def save_file(self):
        f = open('/Users/daniel/desktop/accounts.dat', 'wb')
        pickle.dump(self.obj.get_users(), f)
        f.close()


# Log-In Screen Object
class LoginScreen(Screens):

    def __init__(self, title, obj):
        super().__init__(title, obj)

        self.admin_menu = None
        self.user_menu = None

        #   Counter variable for login attempts
        self.counter = 0

        #######################################################
        # Screen Contents
        # Add labels, and boxes for username and PIN
        self.login_user_label = tkinter.Label(self.root, text='Username: ')
        self.login_user_label.pack()
        self.login_username = tkinter.Entry(self.root)
        self.login_username.pack()

        self.login_pin_label = tkinter.Label(self.root, text='PIN: ')
        self.login_pin_label.pack()
        self.login_pin = tkinter.Entry(self.root)
        self.login_pin.pack()

        # The alert label that shows up is entered username/ password is wrong
        self.alert_value = tkinter.StringVar()
        self.alert_label = tkinter.Label(self.root, textvariable=self.alert_value)
        self.alert_label.pack()

        # Add Login Button and Quit Button and associate with functions
        self.login_btn = tkinter.Button(self.root, text='Log-In', command=self.log_in)
        self.login_btn.pack()
        self.quit_btn = tkinter.Button(self.root, text='Quit', command=self.quit_screen)
        self.quit_btn.pack()

        self.root.mainloop()

    def log_in(self):
        success = False

        # Go through each array in the list to check if login is right
        for i in self.obj.get_users():

            if self.login_username.get() == i.get_user_name() and self.login_pin.get() == i.get_pin():
                user_index = i
                self.quit_screen()
                success = True

                if i.get_admin_status():
                    # Assigns logged in user object to the current_user variable in the screen class
                    self.obj.set_current_user(i)
                    self.obj.current_screen = AdminMenuScreen('Admin Menu', self.obj)
                else:
                    self.obj.set_current_user(i)
                    print(i.get_name())
                    self.obj.current_screen = UserMenuScreen('User Menu', self.obj)

                break

        # If attempt is wrong, add to counter
        if not success:
            self.counter += 1
            self.alert_value.set(f'Wrong Username and/or password. {3 - self.counter} try left')

            if self.counter >= 3:
                messagebox.showinfo('MAX ATTEMPTS REACHED', 'Maximum number of login attempts have been reached!')
                self.root.quit()


#######################################################

# Admin Screens
class AdminMenuScreen(Screens):

    def __init__(self, title, obj):
        super().__init__(title, obj)

        self.add_btn = tkinter.Button(self.root, text='Add User', command=self.add_user)
        self.add_btn.pack()

        self.delete_btn = tkinter.Button(self.root, text='Delete User', command=self.delete_user)
        self.delete_btn.pack()

        self.plot_btn = tkinter.Button(self.root, text='Plot Info')
        self.plot_btn.pack()

        self.return_btn = tkinter.Button(self.root, text='Log-Out', command=self.return_exit)
        self.return_btn.pack()

        self.root.mainloop()

    def add_user(self):
        self.quit_screen()
        self.obj.current_screen = AdminAddScreen('Add Account', self.obj)

    def delete_user(self):
        self.quit_screen()
        self.obj.current_screen = AdminDeleteScreen('Delete Account', self.obj)

    def return_exit(self):
        self.quit_screen()
        self.obj.current_screen = self.obj.create_login()


class AdminAddScreen(Screens):

    def __init__(self, title, obj):
        super().__init__(title, obj)

        self.name_label = tkinter.Label(self.root, text='Name: ')
        self.name_label.pack()
        self.name_entry = tkinter.Entry(self.root, width=10)
        self.name_entry.pack()

        self.username_label = tkinter.Label(self.root, text='Username: ')
        self.username_label.pack()
        self.username_entry = tkinter.Entry(self.root, width=10)
        self.username_entry.pack()

        self.userpin_label = tkinter.Label(self.root, text='PIN: ')
        self.userpin_label.pack()
        self.userpin_entry = tkinter.Entry(self.root, width=10)
        self.userpin_entry.pack()

        self.admin_var = tkinter.IntVar()
        self.admin_label = tkinter.Label(self.root, text='Admin')
        self.admin_check = tkinter.Checkbutton(self.root, variable=self.admin_var)

        self.submit = tkinter.Button(self.root, text='Add User', command=self.enter_user)
        self.submit.pack()

        self.root.mainloop()

    # Enter User into system and save to separate file
    def enter_user(self):
        name = self.name_entry.get()
        username = self.username_entry.get()
        pin = self.userpin_entry.get()

        if self.admin_var.get() == 1:
            admin_stat = True
        else:
            admin_stat = False

        self.obj.add_users(User(name, username, pin, admin_stat))

        f = open('/Users/daniel/desktop/accounts.dat', 'wb')
        pickle.dump(self.obj.get_users(), f)
        f.close()

        self.quit_screen()
        self.obj.current_screen = AdminMenuScreen('Admin Menu', self.obj)


class AdminDeleteScreen(Screens):

    def __init__(self, title, obj):
        super().__init__(title, obj)

        self.name_label = tkinter.Label(self.root, text='Name: ')
        self.name_label.pack()
        self.name_entry = tkinter.Entry(self.root, width=10)
        self.name_entry.pack()
        self.newstring = ''

        for i in self.obj.get_users():
            self.newstring += i.get_name() + ', '

        self.val = tkinter.StringVar()
        self.val.set(self.newstring)
        self.list_label = tkinter.Label(self.root, textvariable=self.val)
        self.list_label.pack()

        self.delete_btn = tkinter.Button(self.root, text='Delete User', command=self.delete_user)
        self.delete_btn.pack()

        self.root.mainloop()

    def delete_user(self):
        name = self.name_entry.get()
        count = 0
        found = False

        for i in self.obj.get_users():
            if i.get_name() == name:
                user_list = self.obj.get_users()
                user_list.pop(count)
                self.obj.set_users_list(user_list)
                found = True

            if not found:
                count += 1

        f = open('/Users/daniel/desktop/accounts.dat', 'wb')
        pickle.dump(self.obj.get_users(), f)
        f.close()


#######################################################
# User Screens

class UserMenuScreen(Screens):

    def __init__(self, title, obj):
        super().__init__(title, obj)

        self.deposit_btn = tkinter.Button(self.root, text='Deposit', command=self.deposit)
        self.deposit_btn.pack()

        self.withdraw_btn = tkinter.Button(self.root, text='Withdrawal', command=self.withdraw)
        self.withdraw_btn.pack()

        self.change_btn = tkinter.Button(self.root, text='Change Pin', command=self.change_pin)
        self.change_btn.pack()

        self.balance_btn = tkinter.Button(self.root, text='Check Balance', command=self.check_balance)
        self.balance_btn.pack()

        self.return_btn = tkinter.Button(self.root, text='Log-Out', command=self.return_exit)
        self.return_btn.pack()

        self.root.mainloop()

    def deposit(self):
        self.quit_screen()
        self.obj.current_screen = UserDepositScreen('Deposit', self.obj)

    def withdraw(self):
        self.quit_screen()
        self.obj.current_screen = UserWithdrawalScreen('Withdrawal', self.obj)

    def change_pin(self):
        self.quit_screen()
        self.obj.current_screen = UserPinScreen('Change Pin', self.obj)

    def check_balance(self):
        self.quit_screen()
        self.obj.current_screen = UserBalanceScreen('Balance', self.obj)

    def return_exit(self):
        self.quit_screen()
        self.obj.current_screen = self.obj.create_login()


class UserDepositScreen(Screens):

    def __init__(self, title, obj):
        super().__init__(title, obj)

        self.amount_label = tkinter.Label(self.root, text='Enter Amount to Deposit')
        self.amount_label.pack()
        self.amount_entry = tkinter.Entry(self.root, width=10)
        self.amount_entry.pack()

        self.deposit_btn = tkinter.Button(self.root, text='Deposit', command=self.deposit)
        self.deposit_btn.pack()

        self.root.mainloop()

    def deposit(self):
        amount = self.amount_entry.get()
        user = self.obj.get_current_user()
        user.add_bal(float(amount))

        #Saves file after deposit
        self.save_file()
        self.quit_screen()
        self.obj.current_screen = UserMenuScreen('User Menu', self.obj)


class UserWithdrawalScreen(Screens):

    def __init__(self, title, obj):
        super().__init__(title, obj)

        self.amount_label = tkinter.Label(self.root, text='Enter Amount to Withdrawal')
        self.amount_label.pack()
        self.amount_entry = tkinter.Entry(self.root, width=10)
        self.amount_entry.pack()

        self.withdrawal_btn = tkinter.Button(self.root, text='Withdrawal', command=self.withdraw)
        self.withdrawal_btn.pack()

        self.root.mainloop()

    def withdraw(self):
        amount = self.amount_entry.get()
        user = self.obj.get_current_user()
        user.sub_bal(float(amount))

        #Saves files after withdrawal
        self.save_file()
        self.quit_screen()
        self.obj.current_screen = UserMenuScreen('User Menu', self.obj)


class UserBalanceScreen(Screens):

    def __init__(self, title, obj):
        super().__init__(title, obj)

        self.amount_label = tkinter.Label(self.root, text='Balance:')
        self.amount_label.pack()

        self.val = tkinter.StringVar()
        self.amount_label2 = tkinter.Label(self.root, textvariable=self.val)
        self.amount_label2.pack()

        self.val.set(self.obj.get_current_user().get_bal())

        self.return_btn = tkinter.Button(self.root, text='Return to Main Menu', command=self.return_menu)
        self.return_btn.pack()

        self.root.mainloop()

    def return_menu(self):

        self.quit_screen()
        self.obj.current_screen = UserMenuScreen('User Menu', self.obj)


class UserPinScreen(Screens):

    def __init__(self, title, obj):
        super().__init__(title, obj)

        self.label1 = tkinter.Label(self.root, text='Enter Old Pin')
        self.label1.pack()
        self.old_entry = tkinter.Entry(self.root, width=10)
        self.old_entry.pack()

        self.label2 = tkinter.Label(self.root, text='Enter New Pin')
        self.label2.pack()
        self.new_entry = tkinter.Entry(self.root, width=10)
        self.new_entry.pack()

        self.val = tkinter.StringVar()
        self.label3 = tkinter.Label(self.root, textvariable=self.val)
        self.label3.pack()

        self.change_btn = tkinter.Button(self.root, text='Change', command=self.change_pin)
        self.change_btn.pack()

        self.root.mainloop()

    def change_pin(self):
        self.val.set('')
        old_pin = self.old_entry.get()
        new_pin = self.new_entry.get()

        if self.obj.get_current_user().get_pin() == old_pin:
            self.obj.get_current_user().set_pin(new_pin)

            # Make sure to save File after changing pin
            self.save_file()

            messagebox.showinfo('Success', 'Pin was successfully changed!')
            self.quit_screen()
            self.obj.current_screen = UserMenuScreen('User Menu', self.obj)
        else:
            self.val.set('Please enter the right pin to change')


atm = Atm()

