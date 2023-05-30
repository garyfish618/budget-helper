from helpers import display_validator_prompt, display_choices_prompt, print_error, print_msg, print_money, valid_year, valid_money, valid_day, session, console
from models import BudgetMonth
from amex_budget_parser import AmexBudgetParser
from nfcu_budget_parser import NfcuBudgetParser
from rich.table import Table

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
                console.clear()
                while True:
                    table = Table(title=str(budget))
                    table.add_column("Date", justify="right")
                    table.add_column("Description")
                    table.add_column("Category", justify="right")
                    table.add_column("Amount", justify="right")

                    total_nfcu_credit = 0.0
                    total_amex_credit = 0.0
                    category_totals = {}
                    for category in budget.categories.all():
                        category_total = float(category.amount_budgeted)
                        for transaction in category.transactions:
                            if transaction.transaction_type == "AMEX":
                                total_amex_credit += float(transaction.amount)
                            elif transaction.transaction_type == "NFCUCredit":
                                total_nfcu_credit += float(transaction.amount)
                            category_total -= float(transaction.amount)
                            table.add_row(transaction.date.strftime('%m-%d-%Y'), transaction.description, category.name, f'${transaction.amount}')

                        category_totals[category.name] = category_total

                    console.clear()
                    print_msg(table)

                    for total in category_totals.keys():
                        console.print(f'{total}')
                        
                        amount = category_totals[total]
                        print_money(amount)

                    print_money(float(budget.extra_income), 'Extra income')
                    print_money(total_nfcu_credit, 'NFCU credit due')
                    print_money(total_amex_credit, "AMEX credit due")
                    print_money(sum([value for value in category_totals.values()]) + float(budget.extra_income), 'Total Debt')

                    choices = ["Import AMEX transactions", "Import NFCU Transactions", "Import NFCU Credit Transactions", "Add additional income for this month", "Exit"]
                    choice = display_choices_prompt(choices, "Please select an action")

                        

                    if choice == choices[0]:
                        days = BudgetViewer.get_day_range()
                        AmexBudgetParser().begin(budget, int(days[0]), int(days[1]))

                    elif choice == choices[1]:
                        days = BudgetViewer.get_day_range()
                        NfcuBudgetParser().begin(budget, "NFCUDebit", int(days[0]), int(days[1]))

                    elif choice == choices[2]:
                        days = BudgetViewer.get_day_range()
                        NfcuBudgetParser().begin(budget, "NFCUCredit", int(days[0]), int(days[1]))

                    elif choice == choices[3]:
                        money = display_validator_prompt(valid_money, "Enter amount of extra income", "Please enter a valid amount of money")
                        budget.extra_income = money
                        session.add(budget)
                        session.commit()
                    else:
                        return

    @staticmethod                
    def get_day_range():
        start_day = display_validator_prompt(valid_day, "Enter a start day for the transactions (Inclusive)", "Please enter a day from 1 - 31")
        end_day = display_validator_prompt(valid_day, "Enter a end day for the transactions (Inclusive)", "Please enter a day from 1 - 31")
        return start_day, end_day

