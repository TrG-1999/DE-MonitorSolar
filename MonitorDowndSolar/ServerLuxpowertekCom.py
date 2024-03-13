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


class ServerLuxpowertekCom:
    
    def __init__(self, user, passw, loan, device_id, inverter_name, previous_date, current_directory):
        self.DOMAIN = 'https://server.luxpowertek.com/'
        self.user = user
        self.passw = passw
        self.loan = loan
        self.device_id = device_id
        self.inverter_name = inverter_name
        self.previous_date = previous_date
        self.current_directory = current_directory
        self.driver = None
        self.download_path = current_directory+r'\storage\temp\server.luxpowertek.com'
        self.newfolder = current_directory+r'\storage\rawdata\data_bytime\server.luxpowertek.com'
        self.newfolder_day = current_directory+r'\storage\rawdata\data_byday\server.luxpowertek.com'

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
        with open(self.current_directory+r'\LinkChrome.txt') as fchrome:
            linkdriver = fchrome.read()
        chrome_service = ChromeService(linkdriver)
        chrome_service.creationflags = CREATE_NO_WINDOW  
        chrome_options = webdriver.ChromeOptions()
        prefs = {"download.default_directory": self.download_path}
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument("--start-maximized")

        # Initialize the WebDriver with the options
        driver = webdriver.Chrome(service=chrome_service,options=chrome_options)

        # Navigate to the page with the file download link
        driver.get(self.DOMAIN)
        try:
            elementval = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="account"]')))
            elementval.send_keys(self.user)
            time.sleep(1)
            #//*[@id="password"]
            elementval = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="password"]')))
            elementval.send_keys(self.passw)
            time.sleep(1)
            #//*[@id="loginHolder"]/div/div[4]/button
            elementval = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="loginHolder"]/div/div[4]/button')))
            elementval.click()
            time.sleep(2)
            driver.get(self.DOMAIN)
            print('check login ',driver.title)
            if str(driver.title)=='Login page':
                elementval = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="account"]')))
                elementval.send_keys(self.user)
                time.sleep(1)
                #//*[@id="password"]
                elementval = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="password"]')))
                elementval.send_keys(self.passw)
                time.sleep(1)
                #//*[@id="loginHolder"]/div/div[4]/button
                elementval = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="loginHolder"]/div/div[4]/button')))
                elementval.click()
                time.sleep(1)
                #check login success  //*[@id="companyLogoTopLeftImg"]
                elementval = WebDriverWait(driver, 8).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="companyLogoTopLeftImg"]')))
                self.DOMAIN =  'https://eu.luxpowertek.com/'
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
        formatted_date = yesterday.strftime("%Y-%m-%d")
        desired_file_name = yesterday.strftime("%Y%m%d_")+self.loan+'.xls'
        dateout = yesterday.strftime("%m/%d/%Y")
        # check login page
        if self.driver == None:
            fields=[self.loan,dateout,'Login Fail page! (by min)']
            with open(self.current_directory+r'\log_down.csv', 'a',newline='') as f:
                writer = csv.writer(f)
                writer.writerow(fields)
            return

        try:
            url = self.DOMAIN+r'WManage/web/analyze/data/export/'+self.device_id+'/'+formatted_date
            self.driver.get(url)
            time.sleep(10)
            for filename in os.listdir(self.download_path):
                if filename.endswith('.xls'):  # Adjust the file extension based on the actual file type
                    old_file_path = os.path.join(self.download_path, filename)
                    new_file_path = os.path.join(self.download_path, desired_file_name)
                    os.rename(old_file_path, new_file_path)
                    break
            shutil.move(new_file_path,os.path.join(self.newfolder, desired_file_name))            
        except Exception as e:
            time.sleep(1)
            print("Erro",e)
            fields=[self.loan,dateout,'Fail crawl_min '+str(e)[:150]]
            with open(r'log_down.csv', 'a',newline='') as f:
                writer = csv.writer(f)
                writer.writerow(fields)

    def crawl_date(self):
        pass


if __name__ == "__main__":
    args = sys.argv
    current_directory = str(os.getcwd())
    # str(args[7]) 3 mode: day time both (day is data by day, time data by min, both data day&time) 
    # parameter func.exe ServerLuxpowertekCom(user, passw, loan, device_id, inverter_name, previous_date, current_directory)
    casedown = ServerLuxpowertekCom(user=str(args[1]), passw=str(args[2]), loan=str(args[3]), device_id=str(args[4]), inverter_name=str(args[5]), previous_date=str(args[6]), current_directory=current_directory)
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

