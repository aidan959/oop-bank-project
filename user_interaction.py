"""
    Used when user interaction is required - contains classes to handle different input
    types and return safe values
"""
import random
import string


class Account():
    pass


class Customer():
    pass


class Transaction():
    pass


CANCEL_FLAG = "x"


class UserInteraction():
    """
    Handles user interactions in a clear and consistent way.
    (I'm pretty proud of this idea and implementation).

        Attributes:
            fail : int
                input validation failed value
            succeed : int
                input validation succeeded value
            cancelled : int
                input cancelled value
            invalid_choice : int
                input was out of range value

        Methods:
            set_output(value):
                Sets the clean output of the interaction
            ouput():
                returns output_value of Interaction class
            prompt_user():
                prompts user for input and does all validation.
    """
    fail = 0
    succeed = 1
    cancelled = 2
    invalid_choice = 3

    def __init__(self, prompt, cancel_flag=CANCEL_FLAG, input_prompt="Enter value"):
        self.prompt = prompt
        self.input_prompt = input_prompt
        self.cancel_flag = cancel_flag
        self.output_value = None

    def set_output(self, value):
        """Sets clean output of this function

        Args:
            value (str): value to set output_value to
        """
        self.output_value = value

    def output(self):
        """returns clean output

        Returns:
            str: value output
        """
        return self.output_value

    def prompt_user(self) -> (int):
        """Prompts user for information

        Returns:
            int: success state of prompt
        """
        # checks if prompt text is empty
        if(self.prompt != ""):
            print(self.prompt)
        # takes the user input
        user_input = input(
            f"{self.input_prompt} (\"{self.cancel_flag}\" to cancel): ")
        # checks if user cancelled
        if user_input == self.cancel_flag:
            # returns cancel state
            return self.cancelled
        # makes sure input is not empty
        elif user_input != "":
            try:
                # casts to int
                user_input = str(user_input)
                # sets output to value
                self.set_output(user_input)
                # returns success state
                return self.succeed
            except Exception as e:
                # TODO: REMOVE WHEN BUGS SORTED
                e
                return self.fail
        else:
            # returns fail state
            return self.fail


class NumberInteraction(UserInteraction):
    """
    Handles user interaction where numbers are required.

        Attributes:
            fail : int
                input validation failed value
            succeed : int
                input validation succeeded value
            cancelled : int
                input cancelled value
            invalid_choice : int
                input was out of range value

        Methods:
            set_output(value):
                Sets the clean output of the interaction
            ouput():
                returns output_value of Interaction class
            prompt_user():
                prompts user for input and does all validation.
    """

    def __init__(self, prompt, cancel_flag=CANCEL_FLAG, input_prompt="Enter value"):
        super().__init__(prompt, cancel_flag, input_prompt)

    def prompt_user(self):
        """Prompts user for float input

        Returns:
            int: success state of prompt
        """
        if(self.prompt != ""):
            print(self.prompt)
        user_input = input(
            f"{self.input_prompt} (\"{self.cancel_flag}\" to cancel): ")
        # checks if user cancelled
        if user_input == self.cancel_flag:
            return self.cancelled

        # attempts to cast to float
        try:
            user_input = float(user_input)
            # updates output
            self.set_output(user_input)
            # indicate successs
            return self.succeed
        except Exception as e:
            # TODO REMOVE WHEN BUGS SQUASHED
            e
            return self.fail


class IntInteraction(UserInteraction):
    """
    Handles user interaction where numbers are required.

        Attributes:
            fail : int
                input validation failed value
            succeed : int
                input validation succeeded value
            cancelled : int
                input cancelled value
            invalid_choice : int
                input was out of range value

        Methods:
            set_output(value):
                Sets the clean output of the interaction
            ouput():
                returns output_value of Interaction class
            prompt_user():
                prompts user for input and does all validation.
    """

    def __init__(self, prompt, cancel_flag=CANCEL_FLAG, input_prompt="Enter value"):
        super().__init__(prompt, cancel_flag, input_prompt)

    def prompt_user(self):
        """Prompts user for float input

        Returns:
            int: success state of prompt
        """
        if(self.prompt != ""):
            print(self.prompt)
        user_input = input(
            f"{self.input_prompt} (\"{self.cancel_flag}\" to cancel): ")
        # checks if user cancelled
        if user_input == self.cancel_flag:
            return self.cancelled

        # attempts to cast to int
        try:
            user_input = int(user_input)
            # updates output
            self.set_output(user_input)
            # indicate successs
            return self.succeed
        except Exception as e:
            # TODO REMOVE WHEN BUGS SQUASHED
            e
            return self.fail


class TextInteraction(UserInteraction):
    """
    Handles user interaction where text is required.

        Attributes:
            fail : int
                input validation failed value
            succeed : int
                input validation succeeded value
            cancelled : int
                input cancelled value
            invalid_choice : int
                input was out of range value

        Methods:
            set_output(value):
                Sets the clean output of the interaction
            ouput():
                returns output_value of Interaction class
            prompt_user():
                prompts user for input and does all validation.
    """

    def __init__(self, prompt, cancel_flag=CANCEL_FLAG, input_prompt="Enter value"):
        super().__init__(prompt, cancel_flag, input_prompt)

    def prompt_user(self) -> (int):
        """Prompts user for text input

        Returns:
            int: success state of prompt
        """
        print(self.prompt)
        user_input = input(
            f"{self.input_prompt} (\"{self.cancel_flag}\" to cancel): ")
        # check if user cancelled
        if user_input == self.cancel_flag:
            return self.cancelled

        # checks if user inputted alphabetic characters (ignores spacing)
        elif user_input.replace(' ', '').isalpha():
            self.set_output(user_input)
            # indicates success
            return self.succeed

        # checks if user inputted non alphabetic characters
        elif user_input.replace(' ', '').isalpha() == False:
            return self.invalid_choice

        else:
            return self.fail


"""Selection interaction - used when selecting from list
   of objects or ids
   option headers is used to print out the object headers
   type_selection is which type is being asked for
   available options are the ids the user is allowed pick
   list_objs is the list of type_selection"""


class SelectionInteraction(UserInteraction):
    """
    Handles user interaction where selection of item is required -
    used when selecting from list of objects or ids.

    (My favourite aspect of this code) - spent a while on it
    (I do apologize that my code is so long and complex)
        Attributes:
            fail : int
                input validation failed value
            succeed : int
                input validation succeeded value
            cancelled : int
                input cancelled value
            invalid_choice : int
                input was out of range value
            option_headers : list
                used to print out object headers
            type_selection : type
                used to indicate type of return
            available_options : list
                list of acceptable choices
            list_obs : list
                list (type_selection type) of items to choose from

        Methods:
            set_output(value):
                Sets the clean output of the interaction - object requested
            ouput():
                returns output_value of Interaction class
            prompt_user():
                prompts user for input and does all validation.
    """

    def __init__(self,
                 prompt,
                 cancel_flag=CANCEL_FLAG,
                 input_prompt="Enter value",
                 type_selection=Customer,
                 option_headers: list = None,
                 available_options: list = None,
                 list_objs: dict = None):
        # updates variables
        self.option_headers = option_headers
        self.available_options = available_options
        self.list_objs = list_objs
        self.type_selection = type_selection
        super().__init__(prompt, cancel_flag, input_prompt)
    """Prompts the user and updates the output"""

    def prompt_user(self) -> (int):
        """Prompts user for selection input

        Returns:
            int: success state of prompt
        """
        # makes sure its a  list before we check if its empty - helps with debugging
        if isinstance(self.available_options, list):
            # makes sure we have options on prompt
            if self.available_options != [] and self.option_headers != []:
                header = ""
                # runs through headers
                for i in self.option_headers:
                    header += f"{i}\t"
                # runs through available options
                options = ""
                if self.type_selection == int:
                    for i in range(0, self.available_options.__len__()):
                        options += f"{str(self.list_objs[i])}\t{self.available_options[i]}\n"
                else:
                    for i in self.available_options:
                        # converts objects to string (accesses their __str__ magic method)
                        options += f"{str(self.list_objs[i])}\n"
                # prints headers
                print(f"{header}\n{options}")
                # displays the input - shows user selection limits of their options
                user_input = input(
                    f"{self.input_prompt} ({self.available_options[0]}-{self.available_options[-1]}) (\"{self.cancel_flag}\" to cancel): ")
                # checks if user cancels
                if user_input == self.cancel_flag:
                    return self.cancelled
                # checks if the choice was numeric
                elif user_input.isnumeric():
                    # casts choice to int
                    user_input = int(user_input)
                    # checks if the user selected a safe option
                    if user_input in self.list_objs:
                        # sets output to that selection
                        self.set_output(user_input)

                        # indicates success
                        return self.succeed
                    else:
                        # indicates invalid choice was selected
                        return self.invalid_choice
                else:
                    # indicates failure
                    return self.fail
            else:
                # none of type in list - warn user
                print(f"No {self.type_selection}s created, please create one.")
                # indicates cancel
                return self.cancelled
        else:
            # indicates failure
            return self.fail


class MenuInteraction(UserInteraction):
    """
    Handles user interaction where menu items are chosen
        Attributes:
            fail : int
                input validation failed value
            succeed : int
                input validation succeeded value
            cancelled : int
                input cancelled value
            invalid_choice : int
                input was out of range value
            options : list
                list of acceptable choices

        Methods:
            set_output(value):
                Sets the clean output of the interaction - object requested
            ouput():
                returns output_value of Interaction class
            prompt_user():
                prompts user for input and does all validation.
    """

    def __init__(self, prompt, cancel_flag=CANCEL_FLAG, input_prompt="Enter value", options: list = None):
        self.options = options
        super().__init__(prompt, cancel_flag=cancel_flag, input_prompt=input_prompt)

    def prompt_user(self) -> (int):
        """Prompts user for selection input

            Returns:
                int: success state of prompt
        """
        # makes sure its a  list before we check if its empty - helps with debugging
        if isinstance(self.options, list):
            # makes sure we have options on prompt
            if self.options != []:
                if(self.prompt != ""):
                    print(self.prompt)
                # lists inputs available
                user_input = input(
                    f"{self.input_prompt} ({self.options[0]}-{self.options[-1]}) (\"{self.cancel_flag}\" to cancel): ")
                # checks if cancelled
                if user_input == self.cancel_flag:
                    return self.cancelled
                # checks if input was numeric
                elif user_input.isnumeric():
                    # casts input to int
                    user_input = int(user_input)

                    # checks if option was in options
                    if user_input in self.options:
                        # update output
                        self.set_output(user_input)
                        return self.succeed
                    else:
                        # indicate invalid choice
                        return self.invalid_choice
                else:
                    return self.fail
            else:
                return self.fail
        else:
            return self.fail


class PasswordInteraction(UserInteraction):
    """
    Handles user interaction where password is inputted
        Attributes:
            fail : int
                input validation failed value
            succeed : int
                input validation succeeded value
            cancelled : int
                input cancelled value
            invalid_choice : int
                input was out of range value

        Methods:
            set_output(value):
                Sets the clean output of the interaction - object requested
            ouput():
                returns output_value of Interaction class
            prompt_user():
                prompts user for input and does all validation.
    """

    def __init__(self, prompt, cancel_flag=CANCEL_FLAG, input_prompt="Enter Password"):
        super().__init__(prompt, cancel_flag=cancel_flag, input_prompt=input_prompt)

    def prompt_user(self):
        # user input
        user_input = input(
            f"{self.input_prompt} (\"{self.cancel_flag}\" to cancel): ")
        if user_input == self.cancel_flag:
            return self.cancelled
        # makes sure nothing dodgy is detected on password set
        elif user_input.count(',') == 0 and user_input.count('\'') == 0 and user_input.count('\"') == 0:
            self.set_output(user_input)
            return self.succeed
        else:
            return self.fail


class ConfirmationInteraction(UserInteraction):
    """
    Handles user interaction where confirmation(y/n) is inputted
        Attributes:
            fail : int
                input validation failed value
            succeed : int
                input validation succeeded value
            cancelled : int
                input cancelled value
            invalid_choice : int
                input was out of range value

        Methods:
            set_output(value):
                Sets the clean output of the interaction - object requested
            ouput():
                returns output_value of Interaction class
            prompt_user():
                prompts user for input and does all validation.
    """

    def __init__(self, prompt, cancel_flag=CANCEL_FLAG, input_prompt="Confirm"):
        super().__init__(prompt, cancel_flag=cancel_flag, input_prompt=input_prompt)

    def prompt_user(self):
        confirm_inputs = ["y", "yes", "ye", "yeah"]
        deny_inputs = ["n", "no", "nah", "none"]
        # user input
        user_input = input(
            f"{self.input_prompt}(Y/n) (\"{self.cancel_flag}\" to cancel): ")
        if user_input == self.cancel_flag:
            return self.cancelled
        # makes sure nothing dodgy is detected on password set
        elif user_input.lower() in confirm_inputs:
            self.set_output(user_input)
            return self.succeed
        elif user_input.lower() in deny_inputs:
            return self.cancelled
        else:
            return self.fail


class CaptchaInteraction(UserInteraction):
    """
    Handles user interaction where we want to verify intent
        Attributes:
            fail : int
                input validation failed value
            succeed : int
                input validation succeeded value
            cancelled : int
                input cancelled value
            invalid_choice : int
                input was out of range value

        Methods:
            set_output(value):
                Sets the clean output of the interaction - object requested
            ouput():
                returns output_value of Interaction class
            prompt_user():
                prompts user for input and does all validation.
    """

    def __init__(self, prompt, cancel_flag=CANCEL_FLAG, input_prompt="Confirm code", complexity=5):
        self.complexity = complexity
        super().__init__(prompt, cancel_flag=cancel_flag, input_prompt=input_prompt)

    def prompt_user(self):
        guess_string = ""
        for _ in range(0, self.complexity):
            guess_string += random.choice(string.ascii_letters)
        # user input
        if(self.prompt != ""):
            print(self.prompt)
        user_input = input(
            f"{self.input_prompt}: ({guess_string}) (\"{self.cancel_flag}\" to cancel): ")
        if user_input == self.cancel_flag:
            return self.cancelled
        # makes sure nothing dodgy is detected on password set
        elif user_input == guess_string:
            self.set_output(user_input)
            return self.succeed
        else:
            return self.fail
