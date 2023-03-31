from helpers import display_prompt, display_validator_prompt, display_binary_prompt, print_success, print_error, valid_money, session, console
from models import CategoryTemplate

class CategoryCreator:
    def begin(self):
        console.clear()

        while True:
            name = display_prompt("Enter a name for this new category")
            
            if session.query(CategoryTemplate).filter_by(name=name).first():
                print_error("This category already exists")
                continue
            
            amount_budgeted = display_validator_prompt(valid_money, "Enter an amount to budget for this category", "Enter a valid amount for this category")

            budget_category = CategoryTemplate(name=name, amount_budgeted=amount_budgeted)
            session.add(budget_category)
            session.commit()

            print_success(f'Successfully created the {name} category with ${amount_budgeted} budgeted')

            if not display_binary_prompt("Create another category"):
                break