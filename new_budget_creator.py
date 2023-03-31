from helpers import console, display_choices_prompt, display_validator_prompt, display_binary_prompt, valid_year, session, print_error, print_success, valid_category_choice, Month
from models import BudgetMonth, BudgetMonthCategory, CategoryTemplate
import time

class BudgetCreator:

    def __init__(self):
        return

    def begin(self):
        console.clear()
        
        while True:
            month = display_choices_prompt( [month.str_value for month in Month], "Choose the month this budget is for")
            year = display_validator_prompt(valid_year, "Choose the year this budget is for", "Please enter a valid year")

            budget_month = BudgetMonth(month=month, year=year)
            
            
            existing_budget = session.query(BudgetMonth).filter_by(month=month, year=year).first()

            if existing_budget:
                print_error("Budget for this month alredady exists. Please specify a new one")
                continue
            
            category_templates = self.get_budget_categories()
            session.add(budget_month)
            session.commit()

            # Create budget categories from templates
            for category_template in category_templates:
                budget_category = BudgetMonthCategory(name=category_template.name, amount_left=category_template.amount_budgeted, budget_month_id=budget_month.id)
                session.add(budget_category)
            
            session.commit()
            print_success(f'Successfully created a budget for {month} {year}')
            time.sleep(3)
            break     

    
    def get_budget_categories(self):
        category_templates = session.query(CategoryTemplate).all()
        category_template_names = [category_template.name for category_template in session.query(CategoryTemplate).all()]

        categories = []
        while True:

            category = display_choices_prompt(category_template_names, "Choose a category to add to this budget", validator=valid_category_choice, validator_args=categories, validator_error_msg="This category was already selected. Select a different one")
            categories.append(category)

            if not display_binary_prompt("Add another category"):
                result = []
                for category in categories:
                    for template in category_templates:
                        if template.name == category:
                            result.append(template)
                
                return result



        
        

        








