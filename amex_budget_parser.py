import os
import configparser
import csv
from amex_scraper import AmexScraper
from helpers import print_error, display_choices_prompt, print_success, print_msg, session, console
from models import Transaction
from datetime import datetime


class AmexBudgetParser():
    def begin(self, budget_month):
        console.clear()
        print_msg("Running AMEX scraper please wait...")

        try:
            config = configparser.ConfigParser()
            config.read('config.ini')

            # Read from config username/password 
            if AmexScraper.run(config['DEFAULT']['amex_username'], config['DEFAULT']['amex_password']):
                categories = budget_month.categories


                # Read from config activity csv directory
                directory_path = config['DEFAULT']['download_directory']
                csv_path = os.path.join(directory_path, 'activity.csv')


                with open(csv_path, "r") as csv_file:
                    csv_reader = csv.DictReader(csv_file)

                    for row in csv_reader:
                        description = row["Description"]
                        amount = row["Amount"]
                        date = datetime.strptime(row["Date"], "%m/%d/%Y").date()
                        category = display_choices_prompt(categories.all(), f'{row["Description"]}\nSelect a category for this transaction')
                        transaction = Transaction(description=description, amount=row["Amount"], date=date, budget_category_id=category.id)
                        session.add(transaction)

                    session.commit()
                    print_success("Successfully added all transactions")
                
                try:
                    # Once done processing csv, delete it
                    os.remove(csv_path)
                
                except:
                    return
                
            else:
                print_error("Error downloading AMEX transaction history")

        except KeyError:
            print_error("Config.ini is missing information. Please update it")
