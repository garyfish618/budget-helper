from rich.console import Console
from rich.prompt import IntPrompt
from new_budget_creator import BudgetCreator
from budget_viewer import BudgetViewer
from category_creator import CategoryCreator
from helpers import console, display_choices_prompt

while True:
    console.clear()

    options = {
        "Create a new months budget" : BudgetCreator(), 
        "View a months budget" : BudgetViewer(),
        "Create a budget category" : CategoryCreator(), 
        "Import transactions for month": None, 
        "Make income/savings adjustments": None

    }

    options[display_choices_prompt(list(options.keys()), "Select an option")].begin()



