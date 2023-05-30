import os
import configparser
import csv
from amex_scraper import AmexScraper
from helpers import print_error, display_choices_prompt, print_success, print_msg, session, console
from models import Transaction
from datetime import datetime


class AmexBudgetParser():
    def begin(self, budget_month, start_day, end_day):
        console.clear()
        scraper_choice = display_choices_prompt(["Use AMEX Scraper", "Download manually"], "Use AMEX scraper or grab from directory?")
        try:
            config = configparser.ConfigParser()
            config.read('config.ini')
            if scraper_choice == "Use AMEX Scraper":
                print_msg("Running AMEX scraper please wait...")
                if not AmexScraper.run(config['DEFAULT']['amex_username'], config['DEFAULT']['amex_password']):
                    print_error("Error downloading AMEX transaction history")
                    return

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

                    if date.day < start_day or date.day > end_day:
                        continue

                    category = display_choices_prompt([*categories.all(), "SKIP"], f'{row["Description"]} ${row["Amount"]}\nSelect a category for this transaction')
                    if category == "SKIP":
                        continue

                    transaction = Transaction(description=description, amount=amount, date=date, budget_category_id=category.id, transaction_type="AMEX")
                    session.add(transaction)
                    console.clear()

                session.commit()
                print_success("Successfully added all transactions")
                
                try:
                    # Once done processing csv, delete it
                    os.remove(csv_path)
                
                except:
                    return
                
        except KeyError:
            print_error("Config.ini is missing information. Please update it")
