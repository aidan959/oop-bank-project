"""
Main bank module. Creates menus, and imports all classes.
"""
from datetime import datetime
import copy
import sys
import os
import re

import bank as b
import user_interaction as ui


# GLOBAL VARIABLE DECLARATION

CUSTOMER_FILE = "customers.txt"
ACCOUNTS_FILE = "accounts.txt"
TRANSACTION_FILE = "accountsTransactions.txt"
NON_DESTRUCT = False
# allows for non-destructive debugging and alternative file names
if sys.argv.__len__() > 1:
    # loops through arguments attached
    for i in range(1, sys.argv.__len__()):
        # checks if we found the debug variable
        if sys.argv[i] == "debug":
            # enables non destructive editing
            NON_DESTRUCT = True
        else:
            # creates a pattern recognition regex
            pattern = re.compile(r'^[\w\-. ]+$')
            # casts the argument to string
            sys.argv[i] = str(sys.argv[i])
            # splits the string by the equals sign
            FILE_INFO = sys.argv[i].split("=", maxsplit=2)
            # useful for debugging
            # print(str(sys.argv))
            if FILE_INFO[0] == "CUSTOMER_FILE":
                # checks if the file already exists
                if os.path.isfile(FILE_INFO[1]):
                    # sets the customer_file variable to file_info
                    CUSTOMER_FILE = FILE_INFO[1]
                else:
                    # file name not created yet
                    print(
                        f"TRANSACTION_FILE name {FILE_INFO[1]} entered could not be found.")
                    # uses regex pattern to determine if file is safe to write to os
                    if not pattern.match(FILE_INFO[1]):
                        # maintains aaults
                        print(
                            "File name not safe to create. Defaulting to temporary name.")
                    else:
                        print("File name safe to create.")
                        TRANSACTION_FILE = FILE_INFO[1]
            # comments above work identically
            elif FILE_INFO[0] == "ACCOUNTS_FILE":
                if os.path.isfile(FILE_INFO[1]):
                    ACCOUNTS_FILE = FILE_INFO[1]
                else:
                    print(
                        f"ACCOUNTS_FILE name {FILE_INFO[1]} entered could not be found.")
                    if not pattern.match(FILE_INFO[1]):
                        print(
                            "File name not safe to create. Defaulting to temporary name.")
                    else:
                        print("File name safe to create.")
                        ACCOUNTS_FILE = FILE_INFO[1]
            # comments above work identically
            elif FILE_INFO[0] == "TRANSACTION_FILE":
                if os.path.isfile(FILE_INFO[1]):
                    TRANSACTION_FILE = FILE_INFO[1]
                else:
                    print(
                        f"TRANSACTION_FILE name {FILE_INFO[1]} entered could not be found.")
                    if not pattern.match(FILE_INFO[1]):
                        print(
                            "File name not safe to create.  Defaulting to temporary name.")
                    else:
                        print("File name safe to create.")
                        TRANSACTION_FILE = FILE_INFO[1]
            else:
                # entered argument was not found
                print(f"{FILE_INFO[0]} argument not recognized..")
    if NON_DESTRUCT:
        # if the user did not specify a temporary file, the software will change it automatically
        if CUSTOMER_FILE == "customers.txt":
            CUSTOMER_FILE = "customers_tmp.txt"
        if ACCOUNTS_FILE == "accounts.txt":
            ACCOUNTS_FILE = "accounts_tmp.txt"
        if TRANSACTION_FILE == "accountsTransactions.txt":
            TRANSACTION_FILE = "accountsTransactions_tmp.txt"
# updates bank modules constants
b.CUSTOMER_FILE = CUSTOMER_FILE
b.ACCOUNTS_FILE = ACCOUNTS_FILE
b.TRANSACTION_FILE = TRANSACTION_FILE
b.NON_DESTRUCT = NON_DESTRUCT


class Menu():
    """
    Menu class which holds list of customers, accounts and transaction.
        Attributes:
            _customers : dict[Customer]
                contains a dictionary of Customers
            _accounts : dict[Account]
                contains a dictionary of Accounts
            _transactions : dict[Transaction]
                contains a dictionary of Transactions
            current_cust_id : int
                current highest customer id
            current_acc_id : int
                current highest account id
            current_trans_id : int
                current highest transaction id
            _current_user : Customer
                used to record currently logged in Customer
            _current_account : Account
                used to record currently actioned Account

        Methods:
            load_customers(customer_file):
                customer_file - the file
                Sets the clean output of the interaction - object requested
            ouput():
                returns output_value of Interaction class
            prompt_user():
                prompts user for input and does all validation.
    """
    # variable declaration
    # customers, accounts and transaction dictionaries
    _customers: dict[b.Customer] = {}
    _accounts: dict[b.Account] = {}
    _transactions: dict[b.Transaction] = {}

    #
    current_cust_id: int
    current_acc_id: int
    current_trans_id: int

    _current_user: b.Customer
    _current_account: b.Account

    def __init__(self):
        # sets user to none
        self._current_user = None
        # loads customers and accounts from file into object
        self.load_customers()
        self.load_accounts()
        self.load_transactions()
        # sets the current id to the highest id on the list
        try:
            self.current_cust_id = int(
                self._customers[list(self._customers)[-1]].id)
        # if some errors occur - set to zero
        except:
            self.current_cust_id = 0
        try:
            self.current_acc_id = int(
                self._accounts[list(self._accounts)[-1]].id)
        # if some errors occur - set to zero
        except:
            self.current_acc_id = 0
        try:
            self.current_trans_id = int(
                self._transactions[list(self._transactions)[-1]].id)
        # if some errors occur - set to zero
        except:
            self.current_trans_id = 0

    def load_customers(self, customer_file: str = b.CUSTOMER_FILE):
        """
        Loads customers from files

        Args:
            customer_file (str, optional): Picks file to update. Defaults to CUSTOMER_FILE

        Customer File Structure
            [0]Customer Id, [1]Customer Name, [2]Customer Age, [3]Customer Password, [4]Account IDs
        """
        # loads customers file from file handler
        customers_file_list = b.file_handler(customer_file)
        # checks if handler succeeded
        if customers_file_list != None:
            # loops lines of customer file
            for customer in customers_file_list:
                # makes sure line being read is valid before loading
                if b.file_line_validator(b.Customer, customer):
                    # strips \n from file
                    customer = customer.rstrip("\n")
                    # splits file by commass
                    row = customer.split(",")
                    # list of account ids owned by customer
                    id_list = []
                    # removes whitespace
                    row[4] = row[4].strip()
                    # removes the []s from account id list
                    row[4] = row[4].lstrip("[")
                    row[4] = row[4].rstrip("]")
                    # checks if no accounts found
                    if row[4] == "":
                        # leave list empty
                        pass
                    else:
                        # split by - s of file
                        id_list = row[4].split("-")
                        # casts all ids in final list to int - then converts to a list
                        # as maps when iterated seem to empty themselves
                        id_list = list(map(int, id_list))
                    # adds customer to customer dict of file
                    try:
                        self._customers[int(row[0].strip())] = b.Customer(int(row[0].strip()),
                                                                          row[1].strip(
                        ),
                            int(row[2].strip(
                            )),
                            row[3].strip(
                        ),
                            id_list)
                    except Exception as e:
                        # Problem when found from loading in file
                        e
                else:
                    continue

    def load_accounts(self, account_file=ACCOUNTS_FILE, level=0):
        """Loads customers from files
        Checks if customers have been loaded yet and attempts to load
        Level makes sure that the rerunning of load_accounts doesnt happen more than twice
        Args:
            account_file (str, optional): Picks file to update. Defaults to ACCOUNTS_FILE.
            level (int) : level used to detect recursion when opening file

        Account File Structure
        [0]Account ID, [1]Account Type, [3]Account Balance, [4]Credit Limit - optional

        Account Types
        [1] = 0 - savings account
        [1] = 1 - checking account
        """
        accounts_file_list = b.file_handler(account_file)
        # checks if the customers list is empty
        if not bool(self._customers) and level < 2:
            # indicate we have no customers
            print("No customers loaded.")
            # attempts to load customers
            self.load_customers()
            # reattempts to load account
            self.load_accounts(account_file=ACCOUNTS_FILE, level=level+1)
            return False
        elif level >= 2:
            # no customers found - no point loading accounts - exits recursive part
            pass
        else:
            # accounts file list file handler
            if accounts_file_list != None:
                # loops through account
                for account in accounts_file_list:
                    # checks if the line looks valid
                    if b.file_line_validator(b.Account, account):
                        # removes newline tag from line
                        account = account.rstrip("\n")

                        # splits variables by ,s
                        row = account.split(",")

                        # removes whitespace characters
                        acc_id = int(row[0].strip())
                        acc_type = int(row[1].strip())
                        acc_balance = float(row[2].strip())
                        if acc_type == 0:
                            # creates a savings account object and puts it
                            # into our account dictionary
                            self._accounts[acc_id] = b.SavingAccount(
                                acc_id, acc_balance, last_transfer=str(row[4].strip()))
                        elif acc_type == 1:
                            # creates a checking account objet and puts it
                            # into our account dictionary
                            self._accounts[acc_id] = b.CheckingAccount(acc_id,
                                                                       acc_balance,
                                                                       int(row[3].strip()))
                    else:
                        # skips this
                        continue

    def load_transactions(self, transaction_file=TRANSACTION_FILE):
        """Loads transactions from files
        Args:
            transaction_file (str, optional): Picks file to update. Defaults to TRANSACTION_FILE.

        Transaction File Structure
        [0]Transaction ID, [1]Transaction Type, [2]Account ID, [3]Amount, [4]Receiving Account
        """
        # loads transaction file
        transaction_file_list = b.file_handler(transaction_file)
        # checks if transaction file exists
        if transaction_file_list != None:
            # loops through transaction
            for transaction in transaction_file_list:
                # makes sure line is valid Transaction line
                if b.file_line_validator(b.Transaction, transaction):
                    # removes \n from line
                    transaction = transaction.rstrip("\n")
                    # splits transaction into items
                    row = transaction.split(",")
                    # removes whitespace and casts to int
                    trans_id = int(row[0].strip())
                    trans_type = int(row[1].strip())
                    trans_acc = int(row[2].strip())
                    time_stamp = str(row[5].strip())
                    # casts amount to float
                    trans_amount = float(row[3].strip())
                    trans_rec_acc = int(row[4].strip())
                    # adds new transaction to list
                    self._transactions[trans_id] = b.Transaction(trans_id,
                                                                 trans_type,
                                                                 trans_acc,
                                                                 trans_amount,
                                                                 trans_rec_acc,
                                                                 time_stamp)

    def get_user_from_account(self, account_id: int) -> (b.Customer):
        """ gets a user from their account id

        Args:
            account_id (int): account id to find user of

        Returns:
            Customer: customer owning account
                      None if not found
        """
        # checks if account actually exists
        if account_id in list(self._accounts):
            # loops through customers
            for i in self._customers:
                # loops through customers account ids
                for j in self._customers[i].account_ids:
                    # checks if the accounts match
                    if account_id == j:
                        # returns the customer
                        return self._customers[i]
            # no customer found
            return None

    def write_transaction(self, transaction_type: int, acc_id: int, amount: float,
                          rec_acc: int) -> (b.Transaction):
        """ wrtes a transaction to file

        Args:
            transaction_type (int) : type of transaction to write
            acc_id (int) : account id money taken from
            amount (float) : amount of money transferred
            recc_acc (int) : account id money going to

        Returns:
            Transaction : if transaction was succful

        Transaction File Structure
        [0]Transaction ID, [1]Transaction Type, [2]Account ID, [3]Amount, [4]Receiving Account
        """
        try:
            curr_time = datetime.now()
            format_time = curr_time.strftime('%b %d %Y %I:%M%p')
            # creates transaction line
            line = f"{self.current_trans_id}, {transaction_type}, {acc_id}, {amount}, {rec_acc}, {format_time}\n"
            # checks if line is valid
            if b.file_line_validator(b.Transaction, line):
                # appends line to file
                with open(TRANSACTION_FILE, "a") as myfile:
                    myfile.write(line)
                # creates a new transaction
                new_transaction = b.Transaction(self.current_trans_id,
                                                transaction_type,
                                                acc_id,
                                                amount,
                                                rec_acc,
                                                format_time)
                # increments transaction
                self.current_trans_id += 1
                # adds new transaction to list
                self._transactions[self.current_trans_id] = new_transaction
                # returns transaction
                return new_transaction
            else:
                # returns nothing
                return None
        except:
            # returns nothing
            return None

    def write_customer(self, user_name: str, user_age: int, user_password: str) -> (b.Customer):
        """ writes a customer to file and adds object

        Args:
            user_name (str) : name of user 
            user_age (int) : age of user
            user_password (str) : password of user

        Returns:
            Customer : if customer creation was succful
        """
        try:
            # increments customer id
            self.current_cust_id += 1
            # opens file and appends new customer
            with open(CUSTOMER_FILE, "a") as myfile:
                myfile.write(
                    f"{self.current_cust_id}, {user_name}, {user_age}, {user_password}, []\n")
                myfile.close()
            # makes a new Customer
            new_customer = b.Customer(
                self.current_cust_id, user_name, user_age, user_password, [])
            # adds customer to file
            self._customers[self.current_cust_id] = new_customer
            # returns new Customer
            return new_customer
        except:
            return None
    """used to create user"""

    def create_user(self) -> (b.Customer):
        """ Creates a new user

        Returns:
            Customer : if customer creation was successful
        """
        # checks for user inputs so the process is not frustrating
        cancel_interaction = False
        local_check = True
        # creates our user input handler for name interaction
        user_input_hd = ui.TextInteraction(
            "", ui.CANCEL_FLAG, input_prompt="Enter Name")
        input_state = ""
        # makes sure user has not cancelled yet
        while input_state != user_input_hd.cancelled:
            # checks if we have attempted to esacape this
            while local_check:
                # blank prompt
                user_input_hd.prompt = ""
                user_input_hd.input_prompt = "Enter Name"
                # prompt user for name
                input_state = user_input_hd.prompt_user()
                # checks if user cancelled
                if input_state == user_input_hd.cancelled:
                    # breaks from loop
                    break
                # checks if user input succeeded
                elif input_state == user_input_hd.succeed:
                    # makes sure the name is longer than 5
                    if user_input_hd.output().__len__() > 5:
                        # puts our username in the field
                        user_name = user_input_hd.output()
                        # we can exit this loop
                        local_check = False
                # checks if input failed
                elif input_state == user_input_hd.fail:
                    print("Your name must be longer than 5 characters.")
            # escapes the loop
            if input_state == user_input_hd.cancelled:
                cancel_interaction = True
                break
            # resets local check
            local_check = True
            # USER ENTERS AGE
            while local_check:
                # age input which takes Int
                age_input_hd = ui.IntInteraction(
                    "", ui.CANCEL_FLAG, "Enter Age")
                # prompts user
                age_state = age_input_hd.prompt_user()
                if age_state == age_input_hd.succeed:
                    # make sure output is above 0
                    if age_input_hd.output() > 0:
                        # inicates we can break
                        local_check = False
                        # sets output
                        user_age = age_input_hd.output()
                    else:
                        print("Age must be a number greater than 0.")
                elif age_state == age_input_hd.cancelled:
                    cancel_interaction = True
                    break
                elif age_state == age_input_hd.fail:
                    print("Please enter a valid number.")
            # escapes the loop
            if cancel_interaction:
                break
            local_check = True
            # keeps for a local check
            while local_check:
                # creates password interaction
                user_password_hd = ui.PasswordInteraction(
                    "", ui.CANCEL_FLAG, "Enter Password")
                # prompts user
                password_state = user_password_hd.prompt_user()
                if password_state == user_password_hd.succeed:
                    # ,,ales sure password is longer than 6 characters
                    if user_password_hd.output().__len__() > 6:
                        user_password = user_password_hd.output()
                    else:
                        # makes sure second if not reached
                        user_password_hd.set_output("")
                        print("Password must be longer than six characters")
                elif password_state == user_password_hd.cancelled:
                    cancel_interaction = True
                    break
                else:
                    print(
                        "Password must be alphanumeric and cannot contain \'s, \"s and \'s ")
                # checks if password was successfully entered
                if user_password_hd.output() != "":
                    # password confirmation interaction
                    user_conf_password_hd = ui.PasswordInteraction(prompt="",
                                                                   input_prompt="Confirm Password")
                    # prompts user for password
                    conf_state = user_conf_password_hd.prompt_user()
                    if conf_state == user_conf_password_hd.succeed:
                        # checks if passwords match
                        if user_conf_password_hd.output() == user_password:
                            local_check = False
                            break
                        else:
                            print("Passwords did not match.")
                    elif conf_state == user_conf_password_hd.cancelled:
                        cancel_interaction = True
                        break
                    elif conf_state == user_conf_password_hd.fail:
                        print(
                            "Password must be alphanumeric and cannot contain \'s, \"s and \'s ")
            # escapes the loop
            # checks if cancelled
            if local_check == False or cancel_interaction:
                break
        if input_state == user_input_hd.cancelled or cancel_interaction:
            print("User creation cancelled, returning to menu")
            return None

        else:
            # writes new customer to file and returns
            new_customer = self.write_customer(
                user_name, user_age, user_password)
            return new_customer

    def create_account(self) -> (int):
        """ Creates a new account

        Returns:
            int : status of account creation
                0 - fail
                1 - success
                2 - cancelled
        """
        # variable declaratation
        cancel_interaction = False
        local_check = True
        available_accounts = []
        # makes sure user has cancelled yet
        while cancel_interaction == False:
            # makes sure user is over 18
            if self._current_user._age < 14:
                print("User is too young to create account")
                return 0
            # makes sure user is over 14
            elif self._current_user._age >= 14:
                available_accounts.append("savings")
                # makes sure user is over 18
                if self._current_user._age >= 18:
                    available_accounts.append("checkings")

            # keeps the local check
            while local_check:
                # generates selection interaction with user
                user_input_hd = ui.SelectionInteraction("", "x", "Select account type", int, [
                                                        "Option", "Account Type"], available_accounts, [0, 1])
                input_state = user_input_hd.prompt_user()
                if input_state == user_input_hd.cancelled:
                    cancel_interaction = True
                    break
                # update account type variable with selection
                elif input_state == user_input_hd.succeed:
                    local_check = False
                    account_type = user_input_hd.output()
                    cancel_interaction = True
                    break
                elif input_state == user_input_hd.invalid_choice:
                    print("Input must be numeric.")
                elif input_state == user_input_hd.fail:
                    print("Please enter a valid number.")
            # cancels interaction
            if input_state == user_input_hd.cancelled:
                print("User creation cancelled, returning to menu")
                return None

        self.current_acc_id += 1
        # appends new account to file
        with open(ACCOUNTS_FILE, "a") as myfile:
            if account_type == 0:
                new_account = b.SavingAccount(
                    self.current_acc_id, 0, "Jan 1 2000 01:00AM")
                myfile.write(
                    f"{self.current_acc_id}, {account_type}, {0}, , Jan 1 2000 01:00AM\n")
            elif account_type == 1:
                new_account = b.CheckingAccount(self.current_acc_id, 0, 100)
                myfile.write(
                    f"{self.current_acc_id}, {account_type}, {0}, 100\n")
            myfile.close()
        self._accounts[self.current_acc_id] = new_account
        self._current_user.add_account(new_account)
        return new_account

    def remove_account(self, deleted_account: b.Account):
        b.remove_item(ACCOUNTS_FILE, deleted_account.id)
        self._accounts.pop(deleted_account.id)
        self._current_user.remove_account(deleted_account.id)

    def remove_user(self, deleted_customer: b.Customer):
        b.remove_item(CUSTOMER_FILE, deleted_customer.id)
        self._customers.pop(deleted_customer.id)
        self._current_user = None

    """
    Logs into account
    0 indicates incorrect password
    1 indicates success
    2 indicates user cancelled attempt
    """

    def login_account(self, user: b.Customer, acc_pass: str):
        if user.password == acc_pass:
            self._current_user = user
            print(f"Welcome to Python Bank, {self._current_user._name}.")
            return 1
        elif acc_pass == ui.CANCEL_FLAG:
            print("Cancelling account login.")
            return 2
        else:
            print("Incorrect password for ID submitted")
            return 0
    """[summary]
        Resets the current user variable to none
    """

    def logout_account(self):
        if self._current_user == None:
            print("Already logged out - should be unreachable")
        else:
            # re adds our customer to the customer list
            if self._current_user is not None:
                self._customers[self._current_user.id] = self._current_user
            self._current_user = None

    def display_accounts(self):
        for account in self._accounts:
            print(account)
    """Prints users in user list"""

    def display_users(self):
        print("id \t Name")
        for user in self._customers:
            print(
                f"{self._customers[user].id} \t {self._customers[user]._name}")

    def print_menu(self):
        print("""================================\n
            MENU\n
                ================================\n
                1 - Display Accounts\n
                2 - Create New Account\n
                3 - Send Money\n
                4 - Deposit Money\n
                5 - Withdraw Money\n
                6 - Display Transactions\n
                7 - Close Account\n
                8 - Close Overall Customer Account\n
                x - Log out\n
                ================================\n
                """)

    def display_login(self):
        user_input_hd = ui.MenuInteraction("",
                                           input_prompt="Enter a choice and press enter",
                                           cancel_flag="3",
                                           options=[1, 2, 3])
        while self.is_logged_in() == False and user_input_hd.output() != 3:
            # prints the login page
            print("""================================\n
            MENU\n
                ================================\n
                1 - Log in to Existing User\n
                2 - Create New User\n
                3 - Exit\n
                ================================\n
                """)
            input_state = user_input_hd.prompt_user()
            # verifies the Interaction succeeded

            if input_state == user_input_hd.succeed:
                # LOGIN OPTION 1
                if user_input_hd.output() == 1:
                    # while the user hasn't logged in and hasn't exited
                    id_selection = ui.SelectionInteraction("Select id from users",
                                                           ui.CANCEL_FLAG,
                                                           type_selection=b.Customer,
                                                           option_headers=[
                                                               "id", "Name"],
                                                           available_options=list(
                                                               self._customers),
                                                           list_objs=self._customers)
                    input_state = 0
                    while self.is_logged_in() == False and input_state != id_selection.cancelled:
                        # display available users to login
                        # TODO: Add pagination here
                        # self.display_users()
                        input_state = id_selection.prompt_user()
                        # user_input = input("Select id from users ('x' to exit):")
                        # allows cast to int
                        if input_state == id_selection.succeed:
                            # does this user exist?
                            pass_input_hd = ui.PasswordInteraction("",
                                                                   ui.CANCEL_FLAG,
                                                                   f"Enter password for account owned by {self._customers[id_selection.output()]._name}")
                            pass_state = pass_input_hd.prompt_user()
                            # user_input = input(f"Enter password for account owned by {self._customers[id_selection.output()]._name} ('x' to exit):")
                            # attempt login
                            if pass_state == pass_input_hd.succeed:
                                account_state = self.login_account(self._customers[id_selection.output()],
                                                                   pass_input_hd.output())
                            else:
                                account_state = 0
                            # state 1 means success - return success to parent call
                            if account_state == 1:
                                # exits loop
                                # user_input = 3
                                return 1

                            # user entered an incorrect password
                            elif account_state == 0:
                                pass

                            # user chose to exit process here
                            elif account_state == 2:
                                break
                        # user exited here
                        elif input_state == id_selection.cancelled:
                            # makes sure this variable doesnt interfere
                            user_input_hd.set_output(1)
                            break
                        elif input_state == id_selection.invalid_choice:
                            print(
                                "Please enter a number corrosponding to the ID of the account you want to access.")
                        elif input_state == id_selection.fail:
                            print("Please enter a valid number.")
                        #else#
                # LOGIN OPTION 2
                elif user_input_hd.output() == 2:
                    # creates a new user using the create_user method
                    tmp_usr = self.create_user()
                    if tmp_usr == None:
                        pass
                    # automatically logs into our new account
                    else:
                        self.login_account(tmp_usr, tmp_usr.password)
                    # checks if our account logged or was succesfully created
                    if self.is_logged_in() == False:
                        print("Failed to create account")
                    else:
                        print(f"Welcome {self._current_user._name}")
                        return 1
            elif input_state == user_input_hd.invalid_choice:
                print("Please enter a valid choice.")
            elif input_state == user_input_hd.cancelled:
                return 0
            else:
                print("Please enter a number.")
    """Allows a user to pick their account"""

    def select_account(self, user: b.Customer = None):
        if user == None:
            user = self._current_user
        if self.is_logged_in():
            # used to check that a user has permission to read account info
            # allowed_ids = user.display_accounts(self._accounts)
            # user_input = input("Select id from accounts ('x' to exit):")
            user_input_hd = ui.SelectionInteraction("",
                                                    ui.CANCEL_FLAG,
                                                    "Select id from accounts",
                                                    b.Account,
                                                    ["id", "Type", "Amount"],
                                                    user.account_ids,
                                                    self._accounts)
            input_state = user_input_hd.prompt_user()
            # if the input succeeded
            if input_state == user_input_hd.succeed:
                return self._accounts[user_input_hd.output()]
            elif input_state == user_input_hd.cancelled:
                print("Cancelling Interaction")
                return None
            elif input_state == user_input_hd.fail:
                print("Input must be a number.")
                return None

        else:
            print("Not logged in.")

    def is_logged_in(self):
        return self._current_user != None

    def delete_customer(self):
        confirm_delete = ui.ConfirmationInteraction("")
        print("ARE YOU SURE YOU WANT TO DELETE ACCOUNT?")
        confirm_delete_state = confirm_delete.prompt_user()
        # CONFIRMED THEY WANT TO DELETE
        if confirm_delete_state == confirm_delete.succeed:
            # gives user a captcha
            captcha_input = ui.CaptchaInteraction(
                "Please verify captcha here:")
            captcha_state = captcha_input.prompt_user()
            # CONFIRMED VIA CAPTHCA
            if captcha_state == captcha_input.succeed:
                empty_accounts = False
                print("Verification succeeded. Proceeding with delete.")
                # loops through accounts to find empty balances TRUE IF NOT ALL ACCOUNTS ARE EMPTY
                empty_accounts = self._current_user.can_delete(self._accounts)
                # we found non empty accont
                if empty_accounts:
                    # checks if there is an account with a transaction limit reached
                    if(self._current_user.transaction_block(self._accounts)):
                        # user has no transfer limits -> continue
                        print(
                            f"Would you like to transfer all money to another user?")
                        confirm = ui.ConfirmationInteraction("")
                        confirm_state = confirm.prompt_user()
                        if(confirm_state == confirm.succeed):
                            print("Please select another user to transfer to.")
                            # removes the current user from the list of options to prevent user sending to themselves
                            user_list_wout_current = copy.deepcopy(
                                self._customers)
                            user_list_wout_current.pop(self._current_user.id)
                            # creates user interaction
                            user_recipient_hd = ui.SelectionInteraction(
                                "",
                                ui.CANCEL_FLAG,
                                "Select id from users",
                                option_headers=["id", "name"],
                                available_options=list(
                                    user_list_wout_current),
                                list_objs=user_list_wout_current)
                            # prompts user
                            user_recipient_state = user_recipient_hd.prompt_user()
                            if user_recipient_state == user_recipient_hd.succeed:
                                # sets the recipient to the selected account
                                recipient: b.Customer = self._customers[user_recipient_hd.output(
                                )]
                                recipient_account = self.select_account(
                                    recipient)
                                if(recipient_account is None):
                                    print("Cancelling interaction.")
                                    return False
                                else:

                                    print("Transferring all money now.")
                                    # has to be used as self._current_user.account_ids is being iterated and changed.
                                    accounts_to_remove = []
                                    # loops through users ids
                                    for i in self._current_user.account_ids:
                                        # if the balance is 0 remove it
                                        if(self._accounts[i].balance == 0):
                                            accounts_to_remove.append(
                                                self._accounts[i].id)
                                        else:
                                            # otherwise empty the account to our lucky user
                                            print(
                                                f"Account id {i} is not empty.")
                                            balance_before = self._accounts[i].balance
                                            if self._current_user.send_money(
                                                    self._accounts[i].balance,
                                                    self._accounts[i],
                                                    self._accounts[recipient_account.id]):
                                                print(
                                                    f"€{balance_before} transferred from your account.")
                                                # prints transaction
                                                self.write_transaction(
                                                    2, self._accounts[i].id, balance_before, recipient_account.id)
                                                # DELETE ACCOUNT
                                                accounts_to_remove.append(
                                                    self._accounts[i].id)

                                            else:
                                                return False
                                    for i in accounts_to_remove:
                                        self.remove_account(self._accounts[i])
                                    return True

                            else:
                                print("Cancelling interaction.")
                                return False
                        else:
                            print("Cancelling interaction.")
                            return False
                    else:
                        # warn that user has surpasssed monthly limit
                        print(
                            f"Account/s has/have reached their monthly transaction limit.")
                        confirm = ui.ConfirmationInteraction("")
                        # offer to void the accounts without transferring any money
                        print("Remove acount/s without transferring?")
                        # prompt the user to confirm
                        confirm_state = confirm.prompt_user()
                        if(confirm_state == confirm.succeed):
                            # loops through accounts and then removes them

                            accounts_to_remove = []
                            for i in self._current_user.account_ids:
                                accounts_to_remove.append(self._accounts[i].id)
                            # this second list and for loop is used to prevent the list being accessed from being modified while removing
                            for i in accounts_to_remove:
                                self.remove_account(self._accounts[i])

                            return True
                        else:
                            print("Cancelling interaction.")
                            return False
                else:
                    # all accounts are empty - delete all and then delete user
                    for i in self._current_user.account_ids:
                        self.remove_account(self._accounts[i])
                    return True
            else:
                print("Cancelling interaction")
                return False
        else:
            print("Cancelling interaction.")
            return False

    def main_menu(self):

        # user_input = 0
        exit_program = False
        while exit_program != True:

            if self.display_login() == 1:
                main_input_hd = ui.MenuInteraction(
                    "", input_prompt="Enter a choice and press enter",
                    cancel_flag=ui.CANCEL_FLAG, options=[1, 2, 3, 4, 5, 6, 7, 8])
                # while user has not quit menu
                while self.is_logged_in():
                    self.print_menu()
                    # get user input
                    input_state = main_input_hd.prompt_user()
                    # makes sure our value was inputted safely
                    if input_state == main_input_hd.succeed:
                        # MENU OPTION 1 -- DISPLAY ACCOUNTS
                        if main_input_hd.output() == 1:
                            self._current_user.display_accounts(self._accounts)
                        # MENU OPTION 2 -- CREATE NEW ACCOUNT
                        elif main_input_hd.output() == 2:
                            self._current_account = self.create_account()
                            if self._current_account == None:
                                print("Failed to create account")
                            elif self._current_account is b.Account:
                                print(
                                    f"Created new account {self._current_account}")
                        # MENU OPTION 3 -- SEND MONEY
                        elif main_input_hd.output() == 3:
                            self._current_account = self.select_account()
                            if self._current_account == None:
                                print("Selecting account failed. Please try again.")
                            else:
                                if self._current_account.limit_reached is False:
                                    user_input_hd = ui.SelectionInteraction(
                                        "",
                                        ui.CANCEL_FLAG,
                                        "Select id from users",
                                        option_headers=["id", "name"],
                                        available_options=list(
                                            self._customers),
                                        list_objs=self._customers)
                                    input_state = user_input_hd.prompt_user()
                                    # checks if the MenuInteraction class succeeded
                                    if input_state == user_input_hd.succeed:
                                        # selects our recipient
                                        recipient: b.Customer = self._customers[user_input_hd.output(
                                        )]
                                        # selects our recipient account
                                        recipient_account = self.select_account(
                                            recipient)
                                        # check if selecting the account worked or not
                                        if recipient_account == None:
                                            print("Selecting account failed.")
                                        else:
                                            # how much would we like to send
                                            amount_input_hd = ui.NumberInteraction(
                                                "",
                                                ui.CANCEL_FLAG,
                                                "How much would you like to send")
                                            amount_state = amount_input_hd.prompt_user()
                                            if amount_state == amount_input_hd.succeed:
                                                if amount_input_hd.output() > 0:
                                                    if self._current_user.send_money(
                                                            amount_input_hd.output(),
                                                            self._current_account,
                                                            recipient_account):
                                                        print(
                                                            f"€{amount_input_hd.output()} transferred from your account.")
                                                        # prints transaction
                                                        self.write_transaction(
                                                            2, self._current_account.id, amount_input_hd.output(), recipient_account.id)
                                                    else:
                                                        print(
                                                            "Transfer Failed.")
                                            elif amount_state == amount_input_hd.cancelled:
                                                print("Cancelling interaction")
                                            elif amount_state == amount_input_hd.fail:
                                                print(
                                                    "Invalid number submitted. Please try again.")
                                    elif input_state == user_input_hd.invalid_choice:
                                        print("User does not exist.")
                                    elif input_state == user_input_hd.cancelled:
                                        print("Cancelling interaction.")
                                    elif input_state == user_input_hd.fail:
                                        print("Please enter a valid number.")
                                else:
                                    print(
                                        f"Account transaction limit reached. Please try again in {self._current_account.next_transfer()} days.")
                        # MENU OPTION 4 -- DEPOSIT MONEY
                        elif main_input_hd.output() == 4:
                            self._current_account = self.select_account()
                            if self._current_account == None:
                                print("Selecting account failed. Please try again.")
                            else:
                                deposit_input_hd = ui.NumberInteraction(
                                    f"Enter how much to deposit into account {self._current_account.id}", ui.CANCEL_FLAG)
                                deposit_state = deposit_input_hd.prompt_user()
                                if deposit_state == deposit_input_hd.succeed:
                                    if deposit_input_hd.output() > 0:
                                        self._current_account.deposit(
                                            deposit_input_hd.output())
                                        self.write_transaction(
                                            0, self._current_account.id, deposit_input_hd.output(), self._current_account.id)
                                        print(
                                            f"€{deposit_input_hd.output()} deposited into your account.")
                                elif deposit_state == deposit_input_hd.cancelled:
                                    print("Cancelling interaction")
                                elif deposit_state == deposit_input_hd.fail:
                                    print("Please enter a valid number")
                        # MENU OPTION 5 -- WITHDRAW MONEY
                        elif main_input_hd .output() == 5:
                            self._current_account = self.select_account()
                            if self._current_account == None:
                                print("Selecting account failed. Please try again.")
                            else:
                                if self._current_account.limit_reached is False:
                                    withdraw_input_hd = ui.NumberInteraction(
                                        "", ui.CANCEL_FLAG, f"How much would you like to withdraw (€{self._current_account.balance})")
                                    withdraw_state = withdraw_input_hd.prompt_user()
                                    if withdraw_state == withdraw_input_hd.succeed:
                                        if withdraw_input_hd.output() > 0:
                                            if self._current_account.withdraw(withdraw_input_hd.output()):
                                                self.write_transaction(
                                                    1,
                                                    self._current_account.id,
                                                    withdraw_input_hd.output(),
                                                    self._current_account.id)
                                                print(
                                                    f"€{withdraw_input_hd.output()} withdrawn from your account.")
                                            else:
                                                print("Insufficient funds.")
                                    elif withdraw_state == withdraw_input_hd.cancelled:
                                        print("Cancelling")
                                    elif withdraw_state == withdraw_input_hd.fail:
                                        print("Please enter a valid number")
                                else:
                                    print(
                                        f"Account transaction limit reached. Please try again in {self._current_account.next_transfer()} days.")
                            pass
                        # MENU OPTION 6 -- DISPLAY TRANSACTIONS
                        elif main_input_hd.output() == 6:
                            # generates transactions from our list of Transaction objects
                            deposit_list = []
                            withdraw_list = []
                            transfer_list = []
                            received_lsit = []
                            # loops through transactions
                            for transaction in self._transactions:
                                # checks if the account of a current transaction belongs to the current user
                                if self.get_user_from_account(self._transactions[transaction].acc_id) == self._current_user:
                                    # checks if the transaction was a deposit
                                    if self._transactions[transaction].transaction_type == 0:
                                        # appends to the list of deposits
                                        deposit_list.append(
                                            self._transactions[transaction])
                                    # checks if the transaction was a withdrawal
                                    elif self._transactions[transaction].transaction_type == 1:
                                        # appends to the list of withdrawals
                                        withdraw_list.append(
                                            self._transactions[transaction])
                                    # checks if the transaction was a transfer
                                    elif self._transactions[transaction].transaction_type == 2:
                                        # appends to the list of transfers
                                        transfer_list.append(
                                            self._transactions[transaction])
                                elif self.get_user_from_account(self._transactions[transaction].rec_acc) == self._current_user and self._transactions[transaction].transaction_type == 2:
                                    received_lsit.append(
                                        self._transactions[transaction])
                            # generates the headers
                            print("\nAccount Deposits")
                            print("id\tType\tAccount\tAmount\tTransaction Time")
                            # prints the list of deposits
                            for i in deposit_list:
                                print(i)
                            print("\nAccount Withdrawals")
                            print("id\tType\t\tAccount\tAmount\tTransaction Time")
                            # prints list of withdrawals
                            for i in withdraw_list:
                                print(i)
                            print("\nAccount Transfers")
                            print(
                                "id\tType\t\tAccount\tAmount\tReceiver\tTransaction Time")
                            # prints the list of transfers
                            for i in transfer_list:
                                print(i)
                            print("\nMoney Received")
                            print("id\tType\tFrom\tAmount")
                            for i in received_lsit:
                                print(
                                    f"{i.rec_acc}\tReceive\t{i.id}\t{i.amount}")
                            pass
                        # MENU OPTION 7 -- DELETE ACCOUNT
                        elif main_input_hd.output() == 7:
                            # Deletes account
                            print("Select account for deletion")
                            # prompts user for account to delete
                            deleted_account = self.select_account()
                            # checks if it was successful
                            if deleted_account is not None:
                                # checks if the balance of the account is zero
                                if deleted_account.balance == 0:
                                    # delete the account
                                    print(
                                        f"Account {deleted_account.id} being prepared for deletion.")
                                    self.remove_account(deleted_account)
                                    print("Account has been deleted.")
                                # checks if the balance of the account is greater than zero
                                elif deleted_account.balance > 0:
                                    print(
                                        "Account must be empty before it can be deleted.")
                                    # offer to transfer money
                                    print("Transfer to other account now?")
                                    confirm = ui.ConfirmationInteraction("")
                                    confirm_state = confirm.prompt_user()
                                    # user confirmed
                                    if(confirm_state == confirm.succeed):
                                        # choose account to trasnsfer too
                                        transfer_to = self.select_account()
                                        # check if it equals to deleted account
                                        if(transfer_to == deleted_account):
                                            print(
                                                "Cannot transfer money to account attempting to be deleted.")
                                        else:
                                            # gets the balance before to write the transaction
                                            balance_before = deleted_account.balance
                                            # checks if we can send the money
                                            if self._current_user.send_money(
                                                    deleted_account.balance,
                                                    self._accounts[deleted_account.id],
                                                    self._accounts[transfer_to.id]):
                                                print(
                                                    f"€{balance_before} transferred from your account.")
                                                # writes transaction
                                                self.write_transaction(
                                                    2, deleted_account.id, balance_before, transfer_to.id)
                                                # deletes account
                                                self.remove_account(
                                                    deleted_account)
                                            # this will only fail if the account has surpassed their monthly transfer limit
                                            else:
                                                #   checks if it was a savings account to verify error
                                                if isinstance(deleted_account, b.SavingAccount):
                                                    print(
                                                        f"Account transaction limit reached. Please try again in {deleted_account.next_transfer()} days.")
                                                else:
                                                    # otherwise inform user that something failed
                                                    print("Operation failed.")
                                    else:
                                        print("Cancelling interaction.")
                                elif deleted_account.balance < 0:
                                    print(
                                        "User must clear their credit before closing their account.")
                                    pass
                            else:
                                print("Returning to menu.")
                        # MENU OPTION 8 -- DELETE CUSTOMER
                        elif main_input_hd.output() == 8:
                            # allows customer to delete their entire account
                            if(self.delete_customer()):
                                # removes the current user
                                self.remove_user(self._current_user)
                                print(
                                    "Customer deleted successfully. Logging out forever :(.")
                                break
                            else:
                                print("Returning to menu.")
                    elif input_state == main_input_hd.cancelled:
                        self.logout_account()
                        break
                    elif input_state == main_input_hd.invalid_choice:
                        print("Input out of range.")
                    elif input_state == main_input_hd.fail:
                        print("Please enter a valid number.")
            else:
                exit_program = True
                print("Exiting program.")


# used to allow this to be imported as a module
if __name__ == "__main__":
    # creates our main menu object
    main_object = Menu()

    # executes our menu loop

    try:
        main_object.main_menu()
    except KeyboardInterrupt:
        print("Logged out and exiting program")
    if NON_DESTRUCT:
        # rempoves temporary files
        os.remove(CUSTOMER_FILE) if CUSTOMER_FILE != "customers.txt" else print(
            "Not removing default customers file.")
        os.remove(ACCOUNTS_FILE) if ACCOUNTS_FILE != "accounts.txt" else print(
            "Not removing default accounts file.")
        os.remove(TRANSACTION_FILE) if TRANSACTION_FILE != "accountsTransactions.txt" else print(
            "Not removing default transaction file.")
    sys.exit(0)
