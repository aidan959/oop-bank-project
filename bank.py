"""
    This module contains classes for a bank's inner workings Account,
    SavingAccount, CheckingAccount and Customer.
"""

from types import resolve_bases
from typing import List, Type
import datetime
import shutil
class CustomerOutOfRange(Exception):
    """Raised if the account being references has an id of an invalid customer"""
class FileCreationReadError(Exception):
    """Raised if the folder is inaccesible"""
# GLOBAL VARIABLE DECLARATION
CUSTOMER_FILE = "customers.txt"
ACCOUNTS_FILE = "accounts.txt"
TRANSACTION_FILE = "accountsTransactions.txt"
NON_DESTRUCT = False
def file_handler(filename : str) -> (list):
    """
    opens the file - and then returns a list of those lines, NOne if failed

        Args:
            filename (str): the file to return

        Returns:
            [List]: [list containing lines of file]
    """
    # file output
    output = []
    # reads out file lines
    try:
        # opens the file
        with open(filename, 'r+') as file:
            # appends lines to the output
            for line in file:
                output.append(line)
        # closes the file
        file.close()
        # returns the output
        return output
    # handles if the file does not exist
    except FileNotFoundError:
        # warn the user that the file didnt exist
        print("File not created ", filename)
        try:
            # attempt to create the file
            with open(filename, 'x') as f:
                # inform file was created
                print(f'{filename} created.')
                if NON_DESTRUCT:
                    try:
                        # 
                        shutil.copy('customers.txt', CUSTOMER_FILE)
                        shutil.copy('accounts.txt', ACCOUNTS_FILE)
                        shutil.copy('accountsTransactions.txt', TRANSACTION_FILE)
                    except Exception as e:
                        print(f"{e} occured. Could not find files to enable non-destructive debugging.")
                        print("Please check these exist befure using -debug flag.")
                f.close()
            return file_handler(filename)
        except FileExistsError:
            # How did we get here?
            raise FileCreationReadError
        except OSError:
            # no read write permissions

            raise FileCreationReadError
    except IOError:
        # prints out the issue of which file couldn't be read
        print("Could not read file:", filename)
        return None

def file_line_validator(object_type: type, line: str) -> (bool):
    """
    Valiates lines going into and coming out of the customers.txt and accounts.txt
    The entire line is passed and the object type being checked is also passed

        Args:
            object_type ([Account or Customer or Transaction type]): What object we're
                        validating
            line (str): the line to validate

        Returns:
            [bool]: wheter the line is valid
    """
    line = line.lstrip("\n")
    line = line.rstrip("\n")
    # checks if dealing with an account
    if object_type is Account:
        try:
            # makes sure it have valid ,'s etc
            if((line.count(",") == 3 or line.count(",") == 4) and line[0] != "#"):
                # splits the line into a row of columns
                row = line.split(",")
                # checks if the appropriate values are numeric after stripped
                try:
                    try:
                        float(row[2].strip())
                    except ValueError:
                        return False
                    if(row[1].strip().isnumeric()):
                        # checks if the account type is valid
                        acc_type = int(row[1].strip())
                        if(acc_type != 0 or acc_type != 1):
                            if(acc_type == 0):
                                datetime.datetime.strptime(row[4].strip(), '%b %d %Y %I:%M%p')
                            # Valid Line :)
                            return True
                        else:
                            # invalid line :()
                            return False
                    else:
                        # invalid line
                        return False
                # error occured? return false - prevent program from crashing
                except Exception as e:
                    # TODO: REMOVE LATER ON WHEN THIS HAS BEEN UPDATED
                    return False
            # checks if its a comment or empty line
            elif line[0] == "#" or line.count(",") == 0:
                # invalid line
                return False
            else:
                # invalid line
                return False
        except Exception as e:
            # TODO: REMOVE LATER ON WHEN THIS HAS BEEN UPDATED
            return False
    # checks if its dealing with a customer
    elif object_type is Customer:
        try:
            # checks count on required variables
            if(line.count(",") == 4 and
               line.count("[") == 1 and
               line.count("]") == 1 and
               line[0] != "#"):
                # splits line into row with columns
                row = line.split(",")
                # checks if the appropriate values are numeric
                try:
                    if row[0].strip().isnumeric() and row[2].strip().isnumeric():
                        # successfully found numbers
                        return True
                except AttributeError:
                    # validation failed
                    return False
            elif line[0] == "#":
                # validation failed
                return False
            else:
                # validation failed
                return False
        except AttributeError:
            return False
        except IndexError:
            return False
    # checks for transaction
    elif object_type is Transaction:
        # makes sure the line contains whats being looked for
        if(line.count(",") == 5 and line[0] != "#"):

            # splits the line into colums
            row = line.split(",")

            # checks that every item is numeric
            try:
                int(row[0].strip())
                int(row[1].strip())
                float(row[3].strip())
                int(row[2].strip())
                # datetime.datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
                datetime.datetime.strptime(row[5].strip(), '%b %d %Y %I:%M%p')
                # can only return true if the line is numeric
                return True
            except ValueError as e:
                # TODO: REMOVE LATER ON WHEN THIS HAS BEEN UPDATED
                print(e)
                return False
            except AttributeError as e:
                # TODO: REMOVE LATER ON WHEN THIS HAS BEEN UPDATED
                print(e)
                return False

        # line validation failed
        else:
            return False

def remove_item(object_file, deleted_id):
    file_to_change = file_handler(object_file)
    if file_to_change is not None:
        # loops through file
        for i in range(0, file_to_change.__len__()):
            # loads the line from the file
            line = file_to_change[i]
            # checks if the line is validated
            if int(line.split(",", maxsplit=1)[0].strip()) == deleted_id:
                # updates the line to remove current info
                line = f""
                file_to_change[i] = line 
                break
            else:
                pass
        # recreates the accounts file
        with open(object_file, "w") as myfile:
            myfile.write("".join(file_to_change))
    pass
class BalanceTooLow(Exception):
    """Raised if the balance of the account goes too low"""

class Account():
    """
    A class to represent an account.

        Attributes:
            id : int
                id of this account
            type : str
                text representation of current type
            balance : float
                float containing the balance
            limit_reached : bool
                bool containing if transfer limit reached 
        Methods:
            deposit(amount):
                Deposits money into the account.
            transfer(amount, receiver):
                Transfers from current account to other user
            withdraw(amount):
                Safely withdraws from account with out direspecting limits.
            update_account_file():
                Updates the account file with the current accounts

    """
    # defines our account types
    type = "Generic Account"
    id = 0
    limit_reached = False
    def __init__(self, id: int,  balance: float):
        """Account initializer - nothing too interesting"""
        self._balance = balance
        self.id = id

    def __str__(self):
        """ Returns, when requested, a string representing this class"""
        return f"{type(self).__name__} {self.id} with €{self._balance}"

    @property
    def balance(self) -> (float):
        """ Returns the balance - property  setter and getter allows yout to treat
            _balance like a variable controlled via function """
        return self._balance

    @balance.setter
    def balance(self, value: float):
        """
        Sets the balance

            Args:
                value (float) : change value of balance
        """
        if value < 0:
            # Balance went too low
            raise BalanceTooLow
        self._balance = value
        self.update_account_file(0)

    def deposit(self, amount: float):
        '''
        Deposits money.

            Args:
                amount (float): Float containing deposit amount
        '''
        # references above set methods
        self.balance = self.balance + amount

    def transfer(self, amount: float, receiver) -> (bool):
        '''
        Transfers money and returns wheter the transaction was succesful.

            Args:
                    amount (float): A float
                    receiver (Account): The account receiving the money

            Returns:
                    (Bool): True - successful
                            False - unsuccessful
        '''
        # if we don't have enough money - cancel the transaction
        if not self.withdraw(amount):
            return False
        else:
            # deposits into receiver account
            receiver.deposit(amount)
            # informs success
            return True

    def withdraw(self, amount: float) -> (bool):
        '''
        Withdraws money from account.

            Args:
                amount (float): A float

            Returns:
                (Bool): True - successful
                        False - unsuccessful
        '''
        # checks if account has enough money before transacting
        if (self.balance - amount) >= 0:
            # reduces money from account
            self.balance = self.balance - amount
            return True
        else:
            # user is too poor
            return False

    def update_account_file(self, acc_type: int, credit=None, timestamp=None):
        '''
        Updates the accounts file with class info.

            Args:
                acc_type (int): A decimal integer containing account types
                credit (int): Another decimal integer containing  credit

            Returns:
                binary_sum (str): Binary string of the sum of a and b
        '''
        # loads the file into memory
        account_file = file_handler(ACCOUNTS_FILE)
        if account_file is not None:
            # loops through file
            for i in range(0, account_file.__len__()):
                # loads the line from the file
                line = account_file[i]
                # checks if the line is validated
                if file_line_validator(Account, line):
                    # checks if the int of the line scanned matches this objects id
                    if int(line.split(",", maxsplit=1)[0].strip()) == self.id:
                        # updates the line with current info
                        line = f"{self.id}, {acc_type}, {self._balance}"
                        # checks if we add the credit value
                        if credit == None:
                            line = f"{line}, ,{timestamp}\n"
                        # adds credit
                        else:
                            line = f"{line}, {credit}\n"
                        account_file[i] = line
                        break
                else:
                    pass
            # recreates the accounts file
            with open(ACCOUNTS_FILE, "w") as myfile:
                myfile.write("".join(account_file))

class CheckingAccount(Account):
    """
    A class to represent a Checking Account (extends Account).
    Contains ability to use credit.

        Attributes:
            id : int
                id of this account
            type : str
                text representation of current type
            balance : float
                float containing the balance
            credit_limit : float
                float containing the credit limit of the account

        Methods:
            deposit(amount):
                Deposits money into the account.
            transfer(amount, receiver):
                Transfers from current account to other user
            withdraw(amount):
                Safely withdraws from account with out direspecting limits.
            update_account_file():
                Updates the account file with the current accounts

    """
    type = "Checking Account"
    credit_limit = 100

    def __init__(self, id: int,  balance: float, credit_lim: float = 100):
        """Initializes checking account"""
        self.credit_limit = credit_lim
        # supers to Account class
        super().__init__(id, balance)

    def __str__(self):
        """Prints a string with the id, account type and balance, tabbed"""
        return f"{self.id}\tChecking\t{self.balance}"

    @property
    def balance(self) -> (float):
        """Balance getter"""
        return super().balance

    @balance.setter
    def balance(self, value):
        """Balance Setter"""
        if value >= - (self.credit_limit):
            self._balance = value
            self.update_account_file()
        else:
            # balance went below credit limit
            raise BalanceTooLow

    def update_account_file(self, acc_type=1):
        """Updates the account file with this account"""
        super().update_account_file(acc_type, self.credit_limit)
        
    def withdraw(self, amount: float) -> (bool):
        """Withdraws money from account"""
        if (self.balance - amount) >= -(self.credit_limit):
            self.balance = self.balance - amount
            return True
        else:
            return False

class SavingAccount(Account):
    """
    A class to represent a Savings Account (extends Account).

        Attributes:
            id : int
                id of this account
            type : str
                text representation of current type
            balance : float
                float containing the balance

        Methods:
            deposit(amount):
                Deposits money into the account.
            transfer(amount, receiver):
                Transfers from current account to other user
            withdraw(amount):
                Safely withdraws from account with out direspecting limits.
            update_account_file():
                Updates the account file with the current accounts 

    """
    type = "Savings Account"
    limit_reached = False
    # days
    reset_time = 30
    def __init__(self, id: int,  balance: float, last_transfer):
        if(last_transfer is None):
            self._last_transfer = datetime.datetime.strptime(last_transfer, '%b %d %Y %I:%M%p')
            self.limit_reached = False
        else:
            self.last_transfer = datetime.datetime.strptime(last_transfer, '%b %d %Y %I:%M%p')
            delta = datetime.datetime.now().date() - self._last_transfer.date()
            if(delta.days >= self.reset_time ):
                self.limit_reached = False
            else:
                self.limit_reached = True
        super().__init__(id, balance)

    def __str__(self):
        return f"{self.id}\tSavings \t{self.balance}"
    """_balance getter"""
    @property
    def balance(self) -> (float):
        return super().balance
        
    """_balance setter"""
    @balance.setter
    def balance(self, value):
        if value == self._balance:
            pass
        elif value > self._balance:
            self._balance = value
        elif value < self._balance:
            self._balance = value
            self.last_transfer = datetime.datetime.now()
        self.update_account_file(0, credit=None, timestamp=self.last_transfer.strftime('%b %d %Y %I:%M%p'))
    @property
    def last_transfer(self):
        return self._last_transfer
    @last_transfer.setter
    def last_transfer(self, value):
        trans =  value
        delta = datetime.datetime.now().date() - trans.date()
        if(delta.days >= 30 ):
            self.limit_reached = False
        else:
            self.limit_reached = True
        self._last_transfer = trans
    def update_account_file(self, acc_type: int, credit=None, timestamp=None):
        """trans_type is transaction type
        0 = deposit
        1 = withdraw / transfer"""
        return super().update_account_file(acc_type, credit=credit, timestamp=timestamp)
    def withdraw(self, amount: float) -> (bool):
        if self.limit_reached is False:
            return super().withdraw(amount)
        else:
            return None
    def deposit(self, amount: float):
        return super().deposit(amount)
    def next_transfer(self) -> (int):
        """
            updates to check if limit was reached and returns the number of days if not
        """
        delta = datetime.datetime.now().date() - self._last_transfer.date()
        if(delta.days >= self.reset_time ):
            self.limit_reached = False
        else:
            self.limit_reached = True
            return self.reset_time - delta.days


class Customer():
    """
    A class to represent a Customer.

        Attributes:
            id : int
                id of this customer.
            account_ids : list[int]
                List of account ids owned by customer.
            account_obs : list[Account]
                List of account objects owned by customer.
            _name : str
                Name of customer.
            _age : int
                Age of customer.

        Methods:
            name : str
                return name of customer
            age : int
                returns age of customer
            load_account_ids(accounts_list:dict)
                Loops through accounts in user an receives them from list of accounts obj
            display_accounts(accounts_list:dict)
                Loops through accounts and displays them from list of account obj
            send_money(transfera_amount, from_account, to_account)
                Transfers money from accounts of user
            add_account(new_acc)
                new_acc - account to be added
                attaches account to customer and updates file
            remove_account(account_id)
                account_id - id of the account to remove
                removes account from user based on id and regens file
            update_customer_file(file)
                file - customer file being used
                Regenerates the customer file with current info
            can_delete(acc_objs)
                acc_objs - list of account objects
                checks if the current user can be deleted without needing to clear
                user accounts
            transaction_block(acc_objs)
                acc_objs - list of account objects
                Returns true if noaccounts with limits were found, False otherwise


    """
    account_ids = []
    account_objs = []
    _name = ""
    _age = 0
    id = 0
    """Customer initializer"""

    def __init__(self, id: int, cust_name: str, age: int, password: str, ids: List[int]):
        self._name = cust_name
        self._age = age
        self.id = id
        self.password = password
        self.account_ids = ids

    """"Returns, when requested, a string representing this class"""
    def __str__(self):
        return f"{self.id}\t{self._name}"

    @property
    def name(self):
        """Returns _name variable of Customer.

        Returns:
            str: Name of account
        """
        return self._name
    @name.setter
    def name(self, name : str):
        """Sets _name variable of Customer.

        Args:
            name (str): takes name as input.
        """
        # this basically verifies that any set name only has alphabetic and space characters
        self._name = ''.join([i for i in name if i.isalpha() or i.isspace()])
    
    @property
    def age(self):
        """Returns _age variable of Customer

        Returns:
            int: _age variable of Customer
        """
        return self._age
    @age.setter
    def age(self, age : int):
        """Sets _age variable of Customer

        Args:
            age (int): variable to set to
        """
        self._age = age

    def load_account_ids(self, accounts_list : dict):
        """Loads account objs from IDs

        Args:
            accounts_list (dict): dict of account list (taken from Menu class)                 
        """
        for i in self.account_ids:
            # appends to Customer's account list
            self.account_objs.append(accounts_list[i])

    def display_accounts(self, accounts_list : dict):
        """Display account objs from IDs

        Args:
            accounts_list (dict): dict of account list (taken from Menu class)             
        """
        print("id \t Account Type \t Balance")
        # runs through account ids
        for i in self.account_ids:
            print(accounts_list[i])

    def send_money(self, transfer_amount : float, from_account: Account, to_account: Account) -> (bool):
        """

        Args:
            transfer_amount (float): Amount to transfer
            from_account (Account): Account to transfer from
            to_account (Account): Account to transfer to

        Returns:
            bool: whether transfer function of from account worked.
        """
        return from_account.transfer(transfer_amount, to_account)

    def add_account(self, new_acc: Account):
        """Attaches account to Customer

        Args:
            acc_obj (Account): The Account to append
        """
        self.account_ids.append(new_acc.id)
        self.account_objs.append(new_acc)
        self.update_customer_file()

    def remove_account(self, account_id):
        # removes account from object
        self.account_ids.remove(account_id)
        try:
            self.account_objs.pop(account_id)
        except IndexError:
            # this object wont be used but is here for future development
            pass 
        # regenerates customer file
        self.update_customer_file()
    """Updates the customer file"""
    def update_customer_file(self, file : str = CUSTOMER_FILE):
        """Updates the customer file

        Args:
            file (str): The file to read and write from 
        """
        # loads file from file handler
        customer_file = file_handler(file)
        # checks if file handler failed
        if(customer_file != None):
            # error flag
            error_encountered = False
            # loops through customer file
            for i in range(0, customer_file.__len__()):
                # selects the line
                line = customer_file[i]
                # makes sure the line isnt just a text block or comment
                if file_line_validator(Customer, line):
                    # This gets the first value from the line and sees if its the current customer id
                    if int(line.split(",", maxsplit=1)[0].strip()) == self.id:
                        # converts account ids to string so it can be joined by "-"s
                        account_ids = "-".join(map(str, self.account_ids))
                        # recreates the line from the file
                        line = f"{self.id}, {self._name}, {self._age}, {self.password}, [{account_ids}]\n"
                        # runs the line validator to make sure it is a valid customer
                        if file_line_validator(Customer, line):
                            # updates the line
                            customer_file[i] = line
                        else:
                            # we encountered an error - flag it and print output
                            error_encountered = True
                            # TODO: REMOVE THIS WHEN SUCCESSFULLY NO LONGER GETS PRINTED
                            print(f"Line \"{line}\" failed validation.")
                        break
                else:
                    # we skip the line
                    continue
            # no error encountered? Re-generate file
            if error_encountered == False:
                # opens the customer file and rewrites all of the lines
                with open(file, "w") as myfile:
                    myfile.write("".join(customer_file))
    def can_delete(self, acc_objs : dict):
        """
        Returns True if the account can't be deleted without clearing accounts, False otherwise
        Args:
            acc_objs (dit[Accounts]): list of all account objects 
        """
        can_delete = False
        for i in self.account_ids:
            if acc_objs[i].balance == 0 and not acc_objs[i].balance < 0:
                pass
            else:
                can_delete = True  
        return can_delete
    def transaction_block(self, acc_objs :dict):
        """
        Returns True if there are no accounts with limits - otherwise false
        Args:
            acc_objs (dit[Accounts]): list of all account objects
        """
        can_delete = True
        for i in self.account_ids:
            if not acc_objs[i].limit_reached:
                pass
            else:
                can_delete = False
        return can_delete

class Transaction():
    """
    Transaction records between accounts
        Attributes:
            id : int
                transaction id
            transaction_type : int
                determines transaction type
                    0 - deposit
                    1 - withdraw
                    2 - transfer
            acc_id : int
                id of account taken from
            amount : float
                amount of money transacted
            rec_acc : int
                id of account receiving (same of deposit / withdrawal)
    """
    id: int
    transaction_type: int
    acc_id: int
    amount: float
    rec_acc: int

    def __init__(self, id : int, transaction_type : int, acc_id : int, amount : float, rec_acc : int, time_stamp):
        self.id = id
        self.transaction_type = transaction_type
        self.acc_id = acc_id
        self.amount = amount
        self.rec_acc = rec_acc
        self.timestamp = datetime.datetime.strptime(time_stamp, '%b %d %Y %I:%M%p')

    def __str__(self):
        # checks if deposit
        if self.transaction_type == 0:
            return f"{self.id}\tDeposit\t{self.acc_id}\t{self.amount}\t{self.timestamp}"
        # checks if withdraw
        elif self.transaction_type == 1:
            return f"{self.id}\tWithdraw\t{self.acc_id}\t{self.amount}\t{self.timestamp}"
        # checks if transfer
        elif self.transaction_type == 2:
            return f"{self.id}\tTransfer\t{self.acc_id}\t{self.amount}\t{self.rec_acc}\t{self.timestamp}"

