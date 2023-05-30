import os
import configparser
import csv
from amex_scraper import AmexScraper
from helpers import print_error, display_choices_prompt, print_success, print_msg, session, console
from models import Transaction
from datetime import datetime


class NfcuBudgetParser():
    def begin(self, budget_month, transaction_type, start_day, end_day):
        console.clear()
        try:
            config = configparser.ConfigParser()
            config.read('config.ini')
            categories = budget_month.categories

            # Read from config transactions csv directory
            directory_path = config['DEFAULT']['download_directory']
            csv_path = os.path.join(directory_path, 'transactions.csv')
            with open(csv_path, "r") as csv_file:
                csv_reader = csv.DictReader(csv_file)

                for row in csv_reader:
                    description = row["Description"]
                    amount = row["Debit"]
                    date_string = ""
                    if transaction_type == "NFCUCredit":
                        date_string = row["Transaction Date"]
                    else:    
                        date_string = row["Date"]
                    date = datetime.strptime(date_string, "%m/%d/%Y").date()

                    if date.day < start_day or date.day > end_day:
                        continue

                    category = display_choices_prompt([*categories.all(), "SKIP"], f'{row["Description"]} ${row["Debit"]}\nSelect a category for this transaction')
                    if category == "SKIP":
                        continue

                    transaction = Transaction(description=description, amount=amount, date=date, budget_category_id=category.id, transaction_type=transaction_type)
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
