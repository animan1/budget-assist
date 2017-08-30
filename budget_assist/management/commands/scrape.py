from django.core.management.base import BaseCommand
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait


class Command(BaseCommand):
    help = 'Scrape Data'

    def handle(self, *args, **options):
        driver = webdriver.Chrome()
        try:
            driver.get('https://mint.intuit.com/transaction.event')
            ec = expected_conditions.presence_of_all_elements_located((By.ID, "account-0"))
            WebDriverWait(driver, 60).until(ec)
            account_elements = driver.find_elements_by_css_selector("#localnav-acounts ul li")
            account_service_ids = {a.get_property('id').split('-')[-1] for a in account_elements} - {'0'}
        finally:
            driver.quit()
