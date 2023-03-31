from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

class AmexScraper:
    def run(amex_username, amex_password):
        try:
            # Set up Chrome WebDriver and go to American Express login page
            driver = webdriver.Chrome()
            driver.get("https://www.americanexpress.com/en-us/account/login")

            # Wait for the page to load
            time.sleep(5)

            # Find the email input field and enter your email address
            email_field = driver.find_element(By.ID, "eliloUserID")
            email_field.send_keys(amex_username)

            # Find the password input field and enter your password
            password_field = driver.find_element(By.ID, "eliloPassword")
            password_field.send_keys(amex_password)

            # Submit the form
            password_field.send_keys(Keys.RETURN)

            # Wait for the page to load
            time.sleep(10)

            view_recent_transactions = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[3]/div/div/div/div[3]/div[1]/div[1]/div/div/div/div/div[1]/div/div[2]/p/a')
            view_recent_transactions.click()
            time.sleep(10)

            download_recent_transactions = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[3]/div/div/div/div/div[2]/div/div[4]/div/div/table/thead/div/tr[1]/td[2]/div/div[2]/button')
            download_recent_transactions.click()
            time.sleep(10)

            csv_selection = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[3]/div/div/div/div/div[2]/div/div[4]/div/div/div[2]/div/div/div/div/div/div[1]/div/div/div[1]/div/fieldset/div[1]/label')
            csv_selection.click()
            confirm = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[3]/div/div/div/div/div[2]/div/div[4]/div/div/div[2]/div/div/div/div/div/div[2]/div/a')
            confirm.click()
            time.sleep(10)

            # Close the browser
            driver.close()
            driver.quit()
            return True
        
        except:
            return False



