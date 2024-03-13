import os
import time
import sys
import shutil
import csv
import pandas as pd
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from subprocess import CREATE_NO_WINDOW
from datetime import datetime, timedelta


class IsolarcloudCom:

    def __init__(self, user, passw, loan, device_id, inverter_name, previous_date, current_directory):
        self.DOMAIN = 'https://www.isolarcloud.com/'
        self.user = user
        self.passw = passw
        self.loan = loan
        self.device_id = device_id
        self.inverter_name = inverter_name
        self.previous_date = previous_date
        self.current_directory = current_directory
        self.driver = None
        self.download_path = current_directory+r'\storage\temp\www.isolarcloud.com'
        self.newfolder = current_directory + \
            r'\storage\rawdata\data_bytime\www.isolarcloud.com'
        self.newfolder_day = current_directory + \
            r'\storage\rawdata\data_byday\www.isolarcloud.com'

    def close_driver(self):
        if self.driver != None:
            self.driver.quit()

    def check_driver(self):
        if self.driver == None:
            return False
        else:
            return True

    def clear_file(self):
        # clear file temp
        for root, dirs, files in os.walk(self.download_path):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))

    def login_page(self):
        # Set browser options to specify the download location
        with open(self.current_directory+r'\LinkChrome.txt') as fchrome:
            linkdriver = fchrome.read()
        chrome_service = ChromeService(linkdriver)
        chrome_service.creationflags = CREATE_NO_WINDOW
        chrome_options = webdriver.ChromeOptions()
        prefs = {"download.default_directory": self.download_path}
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument("--start-maximized")
        # Initialize the WebDriver with the options
        driver = webdriver.Chrome(
            service=chrome_service, options=chrome_options)
        driver.get(self.DOMAIN)
        # input username and pass
        try:
            time.sleep(3)
            elementval = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="userAcct"]')))
            elementval.send_keys(self.user)
            time.sleep(2)
            # //*[@id="password"]
            elementval = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="userPswd"]')))
            elementval.send_keys(self.passw)
            time.sleep(1)
            # //*[@id="loginHolder"]/div/div[4]/button
            elementval = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="login-btn"]')))
            elementval.click()
            time.sleep(2)
            #know /html/body/div[1]/div/div[2]/span[1]
            try:
                elementval = WebDriverWait(driver, 4).until(EC.element_to_be_clickable(
                    (By.XPATH, '/html/body/div[1]/div/div[2]/span[1]')))
                elementval.click()
                time.sleep(3)
            except Exception as e:
                print('not have know button')

            print('Done mainFrame')
            # close prompt /html/body/div[2]/div/div[1]/button/i
            try:
                elementval = WebDriverWait(driver, 4).until(EC.element_to_be_clickable(
                    (By.XPATH, '/html/body/div[2]/div/div[1]/button/i')))
                elementval.click()
                time.sleep(1)
            except Exception as e:
                print('not have promt')

            try:
                #close popup IsolarCloud Web Upgrade
                #/html/body/div[2]/div/div[2]/div[2]/button[1]
                elementval = WebDriverWait(driver, 4).until(EC.element_to_be_clickable(
                    (By.XPATH, '/html/body/div[2]/div/div[2]/div[1]/i')))
                elementval.click()
                time.sleep(1)
            except Exception as e:
                print('not have close upgrade')

            self.driver = driver
        except Exception as e:
            # IF Erro return None Value
            self.driver = None

    def crawl_time(self):
        # Get today's date
        today = datetime.now()
        # Subtract one day to get yesterday's date
        yesterday = today - timedelta(days=int(self.previous_date))
        # Format yesterday's date as "yyyy-mm-dd"
        formatted_date = yesterday.strftime("%Y/%m/%d")
        dateout = yesterday.strftime("%m/%d/%Y")
        desired_file_name = yesterday.strftime("%Y%m%d_")+self.loan+'.xlsx'
        # check login page
        if self.driver == None:
            fields = [self.loan, dateout, 'Login Fail page! (by min)']
            with open(self.current_directory+r'\log_down.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(fields)
            return

        try:
            if self.inverter_name != 'None':
                #search plant unless None
                elementval = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="app"]/div[1]/div[1]/section/div/div[1]/div/div[1]/div[2]/div/input')))
                elementval.send_keys(self.inverter_name)
                time.sleep(1)
                #click search 
                elementval = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="app"]/div[1]/div[1]/section/div/div[1]/div/div[1]/button')))
                elementval.click()
                time.sleep(2)
            # popup //*[@id="app"]/div[1]/div[1]/section/div/div[2]/div/div[2]/div[1]
            elementval = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="app"]/div[1]/div[1]/section/div/div[2]/div/div[2]/div[1]')))
            elementval.click()
            time.sleep(1)
            # input date //*[@id="overview-container"]/div[3]/div[1]/div[2]/div/input
            elementval = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="overview-container"]/div[3]/div[1]/div[2]/div/input')))
            elementval.send_keys(Keys.CONTROL + "a")
            time.sleep(1)
            elementval.send_keys(Keys.DELETE)
            time.sleep(1)
            elementval.send_keys(formatted_date)
            time.sleep(1)
            elementval.send_keys(Keys.ENTER)
            time.sleep(1)
            # btn export //*[@id="overview-container"]/div[3]/div[3]/div[1]/div[1]/div/button //*[@id="overview-container"]/div[3]/div[2]/div[1]/div[1]/div/button
            try:
                elementval = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="overview-container"]/div[3]/div[3]/div[1]/div[1]/div/button')))
                elementval.click()
                time.sleep(1)
            except Exception as e:
                print('swap click btn export 2')
                elementval = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="overview-container"]/div[3]/div[2]/div[1]/div[1]/div/button')))
                elementval.click()
                time.sleep(1)
            # click export /html/body/ul/li[1]
            elementval = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/ul/li[1]')))
            time.sleep(1)
            elementval.click()
            time.sleep(4)
            print('click Export min')
            # Rename the downloaded file
            for filename in os.listdir(self.download_path):
                # Adjust the file extension based on the actual file type
                if filename.endswith('.xlsx'):
                    old_file_path = os.path.join(self.download_path, filename)
                    new_file_path = os.path.join(
                        self.download_path, desired_file_name)
                    os.rename(old_file_path, new_file_path)
                    break
            shutil.move(new_file_path, os.path.join(
                self.newfolder, desired_file_name))
        except Exception as e:
            time.sleep(1)
            print("Erro", e)
            errs = str(e).replace(',', ' ')
            errs = errs.replace('\n', ' ')
            fields = [self.loan, dateout, 'Fail crawl_min '+errs[:150]]
            with open(r'log_down.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(fields)

    def crawl_date(self):
        # Get today's date
        today = datetime.now()
        # Subtract one day to get yesterday's date
        yesterday = today - timedelta(days=int(self.previous_date))
        # Format yesterday's date as "yyyy-mm-dd"
        formatted_date = yesterday.strftime("%Y/%m")
        dateout = yesterday.strftime("%m/%d/%Y")
        desired_file_name = yesterday.strftime("%Y%m_")+self.loan+'.xlsx'
        # check login page
        if self.driver == None:
            fields = [self.loan, dateout, 'Login Fail page! (by date)']
            with open(self.current_directory+r'\log_down.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(fields)
            return

        try:
            elementval = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="app"]/div[1]/div[1]/div/div[2]/div/div[1]/div/ul[1]/li[1]')))
            elementval.click()
            time.sleep(2)
            if self.inverter_name != 'None':
                #search plant unless None
                elementval = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="app"]/div[1]/div[1]/section/div/div[1]/div/div[1]/div[2]/div/input')))
                elementval.send_keys(self.inverter_name)
                time.sleep(1)
                #click search 
                elementval = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="app"]/div[1]/div[1]/section/div/div[1]/div/div[1]/button')))
                elementval.click()
                time.sleep(2)
            # popup //*[@id="app"]/div[1]/div[1]/section/div/div[2]/div/div[2]/div[1]
            elementval = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="app"]/div[1]/div[1]/section/div/div[2]/div/div[2]/div[1]')))
            elementval.click()
            time.sleep(1)
            #click Months report 
            elementval = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="overview-container"]/div[3]/div[1]/div[1]/button[2]')))
            elementval.click()
            time.sleep(1)
            #input date months 
            elementval = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="overview-container"]/div[3]/div[1]/div[2]/div/input')))
            elementval.send_keys(Keys.CONTROL + "a")
            time.sleep(1)
            elementval.send_keys(Keys.DELETE)
            time.sleep(1)
            elementval.send_keys(formatted_date)
            time.sleep(2)
            elementval.send_keys(Keys.ENTER)
            time.sleep(1)
            try:
                elementval = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="overview-container"]/div[3]/div[3]/div[1]/div[1]/div/button')))
                elementval.click()
                time.sleep(1)
            except Exception as e:
                print('swap click btn export 2')
                elementval = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="overview-container"]/div[3]/div[2]/div[1]/div[1]/div/button')))
                elementval.click()
                time.sleep(1)
            # click export /html/body/ul/li[1]
            elementval = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/ul/li[1]')))
            time.sleep(1)
            elementval.click()
            time.sleep(4)
            print('click Export date')
            # Rename the downloaded file
            for filename in os.listdir(self.download_path):
                # Adjust the file extension based on the actual file type
                if filename.endswith('.xlsx'):
                    old_file_path = os.path.join(self.download_path, filename)
                    new_file_path = os.path.join(
                        self.download_path, desired_file_name)
                    os.rename(old_file_path, new_file_path)
                    break
            shutil.move(new_file_path, os.path.join(
                self.newfolder_day, desired_file_name))
        except Exception as e:
            time.sleep(1)
            print("Erro", e)
            errs = str(e).replace(',', ' ')
            errs = errs.replace('\n', ' ')
            fields = [self.loan, dateout,'Fail crawl_date '+ errs[:150]]
            with open(r'log_down.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(fields)


if __name__ == "__main__":
    args = sys.argv
    current_directory = str(os.getcwd())
    # str(args[7]) 3 mode: day time both (day is data by day, time data by min, both data day&time)
    # parameter func.exe IsolarcloudCom(user, passw, loan, device_id, inverter_name, previous_date, current_directory)
    casedown = IsolarcloudCom(user=str(args[1]), passw=str(args[2]), loan=str(args[3]), device_id=str(
        args[4]), inverter_name=str(args[5]), previous_date=str(args[6]), current_directory=current_directory)
    casedown.login_page()
    if str(args[7]) == "both":
        casedown.crawl_time()
        casedown.clear_file()
        if not casedown.check_driver:
            casedown.login_page()
        casedown.crawl_date()
        casedown.clear_file()
        casedown.close_driver()
    elif str(args[7]) == "date":
        casedown.crawl_date()
        casedown.clear_file()
        casedown.close_driver()
    else:
        casedown.crawl_time()
        casedown.clear_file()
        casedown.close_driver()

