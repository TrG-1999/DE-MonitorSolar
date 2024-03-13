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


class SoliscloudCom:
    
    def __init__(self, user, passw, loan, device_id, inverter_name, previous_date, current_directory):
        self.DOMAIN = 'https://www.soliscloud.com/'
        self.user = user
        self.passw = passw
        self.loan = loan
        self.device_id = device_id
        self.inverter_name = inverter_name
        self.previous_date = previous_date
        self.current_directory = current_directory
        self.driver = None
        self.download_path = current_directory+r'\storage\temp\www.soliscloud.com'
        self.newfolder = current_directory+r'\storage\rawdata\data_bytime\www.soliscloud.com'
        self.newfolder_day = current_directory+r'\storage\rawdata\data_byday\www.soliscloud.com'

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
        # Adding argument to disable the AutomationControlled flag
        chrome_options.add_argument(
            "--disable-blink-features=AutomationControlled")
        # Exclude the collection of enable-automation switches
        chrome_options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])
        # Turn-off userAutomationExtension
        chrome_options.add_experimental_option("useAutomationExtension", False)
        # Initialize the WebDriver with the options
        driver = webdriver.Chrome(
            service=chrome_service, options=chrome_options)
        driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        # Navigate to the page with the file download link
        driver.get(self.DOMAIN)
        try:
            #Unremenber user
            elementval = WebDriverWait(driver, 8).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[1]/div[2]/div/div/div[2]/div/div[5]/div/div/div[1]/label')))
            elementval.click()
            time.sleep(1)
            #agree policy
            elementval = WebDriverWait(driver, 8).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[1]/div[2]/div/div/div[2]/div/div[1]/div[2]/div[4]/div[1]/span[1]/label/span/span')))
            elementval.click()
            time.sleep(1)
            #username
            elementval = WebDriverWait(driver, 8).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[1]/div[2]/div/div/div[2]/div/div[1]/div[2]/form/div[1]/div/div/div[1]/input')))
            elementval.send_keys(self.user)
            time.sleep(1)
            #pass
            elementval = WebDriverWait(driver, 8).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[1]/div[2]/div/div/div[2]/div/div[1]/div[2]/form/div[2]/div/div/input')))
            elementval.send_keys(self.passw)
            time.sleep(1)
            #btn login
            elementval = WebDriverWait(driver, 8).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[1]/div[2]/div/div/div[2]/div/div[1]/div[2]/div[4]/div[2]/button')))
            elementval.click()
            time.sleep(5)
            try:
                elementval = WebDriverWait(driver, 8).until(
                        EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div[1]/button')))
                elementval.click()
                time.sleep(1)
            except Exception as e:
                print('pass question')
            self.driver = driver
        except Exception as e:
            # IF Erro return None Value
            print(e)
            self.driver = None

    def crawl_time(self):
        # Get today's date
        today = datetime.now()
        # Subtract one day to get yesterday's date
        yesterday = today - timedelta(days=int(self.previous_date))
        # Format yesterday's date as "dd-mm-yyyy"
        formatted_date = yesterday.strftime("%d/%m/%Y")
        desired_file_name = yesterday.strftime("%Y%m%d_")+self.loan+'.xlsx'
        dateout = yesterday.strftime("%m/%d/%Y")
        if self.driver == None:
            fields = [self.loan, dateout, 'Login Fail page! (by min)']
            with open(self.current_directory+r'\log_down.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(fields)
            return
        try:
            self.driver.get(self.DOMAIN+'#/station/device')
            if self.device_id != 'None':
                #seach 
                elementval = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, '//*[@id="equipment"]/div[1]/div[1]/div[1]/div[2]/div/div[1]/input')))
                elementval.send_keys(self.device_id)
                time.sleep(1)
                elementval = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, '//*[@id="equipment"]/div[1]/div[1]/div[1]/div[2]/div/div[1]/div/button')))
                elementval.click()
                time.sleep(3)
            #click device 
            elementval = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="equipment"]/div[1]/div[1]/div[2]/div[3]/div[1]/div[4]/div[2]/table/tbody/tr/td[2]/div/a')))
            elementval.click()
            time.sleep(3)
            WebDriverWait(self.driver, 5).until(EC.number_of_windows_to_be(2))
            self.driver.switch_to.window(self.driver.window_handles[1])
            time.sleep(6)
            #input date 
            elementval = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="inverterdetail"]/div/div[2]/div/div[1]/div[4]/div[1]/div/div[1]/div[1]/input')))
            # Remove the readonly attribute using JavaScript
            self.driver.execute_script("arguments[0].removeAttribute('readonly')", elementval)
            elementval.send_keys(Keys.CONTROL + "a")
            time.sleep(1)
            elementval.send_keys(Keys.DELETE)
            time.sleep(1)
            elementval.send_keys(formatted_date)
            time.sleep(1)
            elementval.send_keys(Keys.ENTER)
            time.sleep(3)
            elementval = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@class="el-collapse-item is-active"]/div/div/div/div[7]/div[1]/span[2]')))
            elementval = self.driver.find_elements(By.XPATH, '//*[@class="el-collapse-item is-active"]/div/div/div/div[7]/div[1]/span[2]')
            #click choise
            for el in elementval:
                if 'Grid Total Active Power' in el.get_attribute('innerHTML'):
                    el.click()
                    time.sleep(3)
                    break
            elementval = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@class="el-collapse-item is-active"]/div/div/div/div[1]/div/span[2]')))
            elementval = self.driver.find_elements(By.XPATH, '//*[@class="el-collapse-item is-active"]/div/div/div/div[1]/div/span[2]')
            for el in elementval:
                if 'Total Consumption Power' in el.get_attribute('innerHTML'):
                    el.click()
                    time.sleep(3)
                    break
            #battery 
            elementval = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@class="el-collapse-item is-active"]/div/div/div/div[3]/div[1]/span[2]')))
            elementval = self.driver.find_elements(By.XPATH, '//*[@class="el-collapse-item is-active"]/div/div/div/div[3]/div[1]/span[2]')
            for el in elementval:
                if 'Battery Power' in el.get_attribute('innerHTML'):
                    el.click()
                    time.sleep(3)
                    break
            #click export
            elementval = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="inverterdetail"]/div/div[2]/div/div[1]/div[4]/div[1]/div/button[5]/span/span')))
            elementval.click()
            time.sleep(6)
            # Rename the downloaded file
            for filename in os.listdir(self.download_path):
                if filename.endswith('.xlsx'):  # Adjust the file extension based on the actual file type
                    old_file_path = os.path.join(self.download_path, filename)
                    new_file_path = os.path.join(self.download_path, desired_file_name)
                    os.rename(old_file_path, new_file_path)
                    break
            shutil.move(new_file_path,os.path.join(self.newfolder, desired_file_name))
            self.driver.close()
            time.sleep(1)
            self.driver.switch_to.window(self.driver.window_handles[0])
            time.sleep(1)
            print('Done Export min'+self.loan)
        except Exception as e:
            time.sleep(1)
            errs = str(e).replace(',',' ')
            errs = errs.replace('\n',' ')
            fields=[self.loan,dateout,'Fail crawl_min '+errs[:150]]
            with open(r'log_down.csv', 'a',newline='') as f:
                writer = csv.writer(f)
                writer.writerow(fields)
            self.driver = None


    def crawl_date(self):
        # Get today's date
        today = datetime.now()
        # Subtract one day to get yesterday's date
        yesterday = today - timedelta(days=int(self.previous_date))
        # Format yesterday's date as "dd-mm-yyyy"
        formatted_date = yesterday.strftime("%m/%Y")
        desired_file_name = yesterday.strftime("%Y%m_")+self.loan+'.xls'
        dateout = yesterday.strftime("%m/%d/%Y")
        print('crawl_date ',formatted_date)
        if self.driver == None:
            fields = [self.loan, dateout, 'Login Fail page! (by date)']
            with open(self.current_directory+r'\log_down.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(fields)
            return
        try:
            self.driver.get(self.DOMAIN+'#/station/device')
            if self.device_id != 'None':
                #seach 
                elementval = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, '//*[@id="equipment"]/div[1]/div[1]/div[1]/div[2]/div/div[1]/input')))
                elementval.send_keys(self.device_id)
                time.sleep(1)
                elementval = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, '//*[@id="equipment"]/div[1]/div[1]/div[1]/div[2]/div/div[1]/div/button')))
                elementval.click()
                time.sleep(3)
            #click device 
            elementval = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="equipment"]/div[1]/div[1]/div[2]/div[3]/div[1]/div[4]/div[2]/table/tbody/tr/td[2]/div/a')))
            elementval.click()
            time.sleep(3)
            WebDriverWait(self.driver, 5).until(EC.number_of_windows_to_be(2))
            self.driver.switch_to.window(self.driver.window_handles[-1])
            time.sleep(6)
            #click months
            elementval = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="inverterdetail"]/div/div[2]/div/div[1]/div[4]/div[1]/div/button[2]')))
            elementval.click()
            time.sleep(3)
            #input date 
            elementval = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="inverterdetail"]/div/div[2]/div/div[1]/div[4]/div[1]/div/div[1]/div[2]/input')))
            # Remove the readonly attribute using JavaScript
            self.driver.execute_script("arguments[0].removeAttribute('readonly')", elementval)
            elementval.send_keys(Keys.CONTROL + "a")
            time.sleep(1)
            elementval.send_keys(Keys.DELETE)
            time.sleep(1)
            elementval.send_keys(formatted_date)
            time.sleep(1)
            elementval.send_keys(Keys.ENTER)
            time.sleep(3)
            #click export
            elementval = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="inverterdetail"]/div/div[2]/div/div[1]/div[4]/div[1]/div/button[5]/span/span')))
            elementval.click()
            time.sleep(6)
            # Rename the downloaded file
            for filename in os.listdir(self.download_path):
                if filename.endswith('.xls'):  # Adjust the file extension based on the actual file type
                    old_file_path = os.path.join(self.download_path, filename)
                    new_file_path = os.path.join(self.download_path, desired_file_name)
                    os.rename(old_file_path, new_file_path)
                    break
            shutil.move(new_file_path,os.path.join(self.newfolder_day, desired_file_name))
            self.driver.close()
            time.sleep(1)
            self.driver.switch_to.window(self.driver.window_handles[0])
            time.sleep(1)
            print('Done Export date'+self.loan)
        except Exception as e:
            time.sleep(1)
            errs = str(e).replace(',',' ')
            errs = errs.replace('\n',' ')
            fields=[self.loan,dateout,'Fail crawl_date '+errs[:150]]
            with open(r'log_down.csv', 'a',newline='') as f:
                writer = csv.writer(f)
                writer.writerow(fields)
            self.driver = None


if __name__ == "__main__":
    args = sys.argv
    current_directory = str(os.getcwd())
    # str(args[7]) 3 mode: day time both (day is data by day, time data by min, both data day&time) 
    # parameter func.exe SoliscloudCom(user, passw, loan, device_id, inverter_name, previous_date, current_directory)
    casedown = SoliscloudCom(user=str(args[1]), passw=str(args[2]), loan=str(args[3]), device_id=str(args[4]), inverter_name=str(args[5]), previous_date=str(args[6]), current_directory=current_directory)
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

