from helpers import display_validator_prompt, display_choices_prompt, print_error, valid_year, session, console
from models import BudgetMonth
from amex_budget_parser import AmexBudgetParser

class BudgetViewer:
    def begin(self):
        console.clear()
        
        while True:
            year = display_validator_prompt(valid_year, "What year would you like to view budgets for", "Please enter a valid year")
            
            budgets = session.query(BudgetMonth).filter_by(year=year).all()
            
            if not budgets:
                print_error("No budgets exist for that year")

            else:
                budget = display_choices_prompt(budgets, "Select a budget you would like to view")
                # Display table here
                choices = ["Import AMEX transactions", "Exit"]
                choice = display_choices_prompt(choices, "Please select an action")

                if choice == choices[0]:
                    AmexBudgetParser().begin(budget)

                else:
                    return
                    

