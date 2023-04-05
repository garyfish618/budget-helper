import re
from enum import Enum
from rich.console import Console
from rich.prompt import IntPrompt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///budget.db')
console = Console()
Session = sessionmaker(bind=engine)
session = Session()

class Month(Enum):
    JANUARY = (1, "January")
    FEBRUAR = (2, "February")
    MARCH = (3, "March")
    APRIL = (4, "April")
    MAY = (5, "May")
    JUNE = (6, "June")
    JULY = (7, "July")
    AUGUST = (8, "August")
    SEPTEMBER = (9, "September")
    OCTOBER = (10, "October")
    NOVEMBER = (11, "November") 
    DECEMBER = (12, "December")

    def __new__(cls, value, name):
        member = object.__new__(cls)
        member._value_ = value
        member._name_ = name
        member.int_value, member.str_value = value, name
        return member

def display_choices_prompt(options, prompt_text, validator=None, validator_args=None, validator_error_msg=None):
    while True:
        for i in range(0, len(options)):
            print_msg(f'{i+1}. {options[i]}')

        selected = IntPrompt.ask(prompt_text, console=console)

        if selected > 0 and selected <= len(options):
            answer = options[selected - 1]
            if validator: 
                if not validator(answer, validator_args):
                    console.clear()
                    print_error(validator_error_msg)
                    continue
            
            return answer
            
        
        console.clear()
        print_error("Please select a valid option")

def display_binary_prompt(prompt_text):
    while True:
        answer = console.input(f'{prompt_text}?[Y/N]:')

        if answer == 'y' or answer == 'Y':
            return True
        
        if answer == 'n' or answer == 'N':
            return False
        
        print_error("Please select a valid option")

def display_validator_prompt(validator, prompt_text, error_message=None):
    while True:
        response = console.input(f'{prompt_text}:')

        if validator(response):
            return response

        console.clear()
        if error_message:
            print_error(error_message)

        else:
            print_error("Please enter a valid input")

def display_prompt(prompt_text):
    return console.input(f'{prompt_text}:')

def print_success(success_text):
    console.print(success_text, style="green")

def print_error(error_text):
    console.print(error_text, style="red")

def print_money(money_amt, message=None):
    output = ""
    if message != None:
        output += message + ": "
    
    if money_amt >= 0:
        output += f'[green]${money_amt:.2f}[/green]'
    else:
        output += f'[red]${money_amt:.2f}[/red]'

    console.print(output, highlight=False)

def print_msg(msg, style=None):
    console.print(msg, style=style)

def valid_year(year):
    try:
        year = int(year)
        return year >= 1 and year <= 9999

    except:
        return False

def valid_money(money):
    if re.match(r'^\d+(.\d{2})?$', money):
        return True
    
    return False

def valid_category_choice(category, categories):
    if categories != None and category not in categories:
        return True
    return False
