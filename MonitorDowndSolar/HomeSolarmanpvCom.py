import os
import time
import sys
import shutil
import csv
import warnings
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.action_chains import ActionChains
from subprocess import CREATE_NO_WINDOW
from datetime import datetime, timedelta


class HomeSolarmanpvCom:
    """docstring for HomeSolarmanpvCom"""
    def __init__(self, user, passw, loan, device_id, inverter_name, previous_date, current_directory):
        self.DOMAIN = 'https://home.solarmanpv.com/'
        self.user = user
        self.passw = passw
        self.loan = loan
        self.device_id = device_id
        self.inverter_name = inverter_name
        self.previous_date = previous_date
        self.current_directory = current_directory
        self.driver = None
        self.download_path = current_directory+r'\storage\temp\home.solarmanpv.com'
        self.newfolder = current_directory+r'\storage\rawdata\data_bytime\home.solarmanpv.com'
        self.newfolder_day = current_directory+r'\storage\rawdata\data_byday\home.solarmanpv.com'

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
        chrome_options.add_argument("--disable-blink-features=AutomationControlled") 
        # Exclude the collection of enable-automation switches 
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
        # Turn-off userAutomationExtension 
        chrome_options.add_experimental_option("useAutomationExtension", False)
        # Initialize the WebDriver with the options
        driver = webdriver.Chrome(service=chrome_service,options=chrome_options)
        # Navigate to the page with the file download link
        driver.get(self.DOMAIN)
        time.sleep(2)
        # input username and pass
        try:
            try:
                #agree //*[@id="app"]/div[3]/div[2]/div/div[3]/button[1]
                elementval = WebDriverWait(driver, 7).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div[2]/div/div[2]/div/div/div/button')))
                elementval.click()
                time.sleep(2)
            except Exception as e:
                print("not confirm agree!")
                time.sleep(1)

            try:
                #country //*[@id="areaList"]/div[1]/div[2]
                elementval = WebDriverWait(driver, 7).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div[2]/div/div[2]/div/div/div/span')))
                elementval.click()
                time.sleep(2)
                print("input Vietnam")
                #input country /html/body/div[3]/div/div/div/div[2]/div/div/div/span/input
                elementval = WebDriverWait(driver, 7).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div/div/div[2]/div/div/div/span/input')))
                elementval.send_keys('Vietnam')
                time.sleep(1)
                elementval = WebDriverWait(driver, 7).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div/div/div[2]/div/div/div/span/span')))
                elementval.click()
                time.sleep(1)
                #choise /html/body/div[4]/div/div/div/div[2]/div/div/div/div[2]
                elementval = WebDriverWait(driver, 7).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div/div/div[2]/div/div/div/div[2]')))
                elementval.click()
                time.sleep(2)
                #confirm /html/body/div[3]/div/div[2]/div/div[2]/div[2]/div[3]/button
                elementval = WebDriverWait(driver, 7).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div[2]/div/div[2]/div[2]/div[3]/button')))
                elementval.click()
                time.sleep(1)
            except Exception as e:
                print("not confirm country!")
                time.sleep(1)

            #verify Bar
            element_hold = driver.find_element('xpath','//*[@id="nc_1_n1z"]')
            action = ActionChains(driver)
            action.click_and_hold(element_hold).perform()
            action.move_by_offset(350,0).perform()
            time.sleep(2)
            action.release().perform()
            time.sleep(3.5)
            elementval = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="email"]')))
            elementval.send_keys(self.user)
            time.sleep(2)
            #//*[@id="password"]
            elementval = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="password"]')))
            elementval.send_keys(self.passw)
            time.sleep(1)
            #//*[@id="loginHolder"]/div/div[4]/button
            elementval = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="xmzd-login-btn"]')))
            elementval.click()
            time.sleep(1)
            try:
                #agree //*[@id="app"]/div[3]/div[2]/div/div[3]/button[1]
                elementval = WebDriverWait(driver, 8).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div[2]/div/div[2]/div/div/div/button')))
                elementval.click()
                time.sleep(2)
            except Exception as e:
                print("not agree!")
            self.driver = driver
        except Exception as e:
            self.driver = None

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

    def crawl_time(self):
        # Suppress the UserWarning from openpyxl
        warnings.simplefilter("ignore", category=UserWarning)
        # Get today's date
        today = datetime.now()
        # Subtract one day to get yesterday's date
        yesterday = today - timedelta(days=int(self.previous_date))
        # Format yesterday's date as "yyyy-mm-dd"
        formatted_date = yesterday.strftime("%Y-%m-%d")
        current_date = (today - timedelta(days=(int(self.previous_date)-1))).strftime("%Y-%m-%d")
        desired_file_name = yesterday.strftime("%Y%m%d_")+self.loan+'.xlsx'
        dateout = yesterday.strftime("%m/%d/%Y")
        datefilter = yesterday.strftime("%Y/%m/%d")
        # check login page
        if self.driver == None:
            fields=[self.loan,dateout,'Login Fail page (by min)!']
            with open(self.current_directory+r'\log_down.csv', 'a',newline='') as f:
                writer = csv.writer(f)
                writer.writerow(fields)
            return
        try:
            self.driver.get(self.DOMAIN+'plant/infos/exportdata')
            #click open layout device
            #click open calender
            elementval = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/section/main/div[1]/section/main/div/div/div/div/div/div/div/div/div[1]/div/div[6]/span')))
            elementval.click()
            time.sleep(3)
            #start date
            rate = [2,3]
            flag = True
            element_curdate =None
            while flag:
                try:
                    elmdiv = str(rate.pop())
                    elementval = WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div['+elmdiv+']/div/div/div/div/div[1]/div[1]/div[1]/div/input')))
                    time.sleep(1)
                    element_curdate = WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div['+elmdiv+']/div/div/div/div/div[1]/div[2]/div[1]/div/input')))
                    flag = False
                except Exception as e:
                    if len(rate)==0:
                        flag = False
                    print('click again time')
            # Remove the readonly attribute using JavaScript
            self.driver.execute_script("arguments[0].removeAttribute('readonly')", elementval)
            elementval.send_keys(Keys.CONTROL + "a")
            time.sleep(1)
            elementval.send_keys(Keys.DELETE)
            time.sleep(1)
            elementval.send_keys(formatted_date)
            time.sleep(1)
            #current date
            self.driver.execute_script("arguments[0].removeAttribute('readonly')", element_curdate)
            element_curdate.send_keys(Keys.CONTROL + "a")
            time.sleep(1)
            element_curdate.send_keys(Keys.DELETE)
            time.sleep(1)
            element_curdate.send_keys(current_date)
            time.sleep(1)
            #click other element and keep date
            elementval = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/section/header/div/div[2]/div')))
            elementval.click()
            time.sleep(1)
            elementval = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[2]/div[1]/div/div[2]/i')))
            elementval.click()
            time.sleep(1)
            #btn export 
            print('click Export')
            elementval = WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/section/main/div[1]/section/main/div/div/div/div/div/div/div/div/div[1]/div/button')))
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
            dataframe = pd.read_excel(os.path.join(self.newfolder, desired_file_name),engine = 'openpyxl',sheet_name=0)
            dataframe = dataframe[dataframe['Updated Time'].str.contains(datefilter)]
            dataframe.to_excel(os.path.join(self.newfolder, desired_file_name), index=False)
        except Exception as e:
            time.sleep(1)
            print("Erro",e)
            fields=[self.loan,dateout,'Fail crawl_min '+str(e)[:150]]
            with open(r'log_down.csv', 'a',newline='') as f:
                writer = csv.writer(f)
                writer.writerow(fields)
            self.driver = None

    def crawl_date(self):
        # Suppress the UserWarning from openpyxl
        warnings.simplefilter("ignore", category=UserWarning)
        # Get today's date
        today = datetime.now()
        # Subtract one day to get yesterday's date
        yesterday = today - timedelta(days=int(self.previous_date))
        # Format yesterday's date as "yyyy-mm-dd"
        formatted_date = yesterday.strftime("%Y-%m-%d")
        current_date = (today - timedelta(days=(int(self.previous_date)-1))).strftime("%Y-%m-%d")
        desired_file_name = yesterday.strftime("%Y%m%d_")+self.loan+'.xlsx'
        dateout = yesterday.strftime("%m/%d/%Y")
        datefilter = yesterday.strftime("%Y/%m/%d")
        # check login page
        if self.driver == None:
            fields=[self.loan,dateout,'Login Fail page (by date)!']
            with open(self.current_directory+r'\log_down.csv', 'a',newline='') as f:
                writer = csv.writer(f)
                writer.writerow(fields)
            return
        try:
            self.driver.get(self.DOMAIN+'plant/infos/exportdata')
            # change down date
            time.sleep(2)
            elementval = WebDriverWait(self.driver, 7).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/section/main/div[1]/section/main/div/div/div/div/div/div/div/div/div[1]/div/div[4]/div/span[2]')))
            elementval.click()
            time.sleep(1)
            #click open layout device
            #click open calender
            elementval = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/section/main/div[1]/section/main/div/div/div/div/div/div/div/div/div[1]/div/div[6]/span')))
            elementval.click()
            time.sleep(3)
            #start date
            rate = [2,3]
            flag = True
            element_curdate =None
            while flag:
                try:
                    elmdiv = str(rate.pop())
                    elementval = WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div['+elmdiv+']/div/div/div/div/div[1]/div[1]/div[1]/div/input')))
                    time.sleep(1)
                    element_curdate = WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div['+elmdiv+']/div/div/div/div/div[1]/div[2]/div[1]/div/input')))
                    flag = False
                except Exception as e:
                    if len(rate)==0:
                        flag = False
                    print('click again date')
            # Remove the readonly attribute using JavaScript
            self.driver.execute_script("arguments[0].removeAttribute('readonly')", elementval)
            elementval.send_keys(Keys.CONTROL + "a")
            time.sleep(1)
            elementval.send_keys(Keys.DELETE)
            time.sleep(1)
            elementval.send_keys(formatted_date)
            time.sleep(1)
            #current date
            self.driver.execute_script("arguments[0].removeAttribute('readonly')", element_curdate)
            element_curdate.send_keys(Keys.CONTROL + "a")
            time.sleep(1)
            element_curdate.send_keys(Keys.DELETE)
            time.sleep(1)
            element_curdate.send_keys(current_date)
            time.sleep(1)
            #click other element and keep date
            elementval = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/section/header/div/div[2]/div')))
            elementval.click()
            time.sleep(1)
            elementval = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[2]/div[1]/div/div[2]/i')))
            elementval.click()
            time.sleep(1)
            #btn export 
            elementval = WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/section/main/div[1]/section/main/div/div/div/div/div/div/div/div/div[1]/div/button')))
            elementval.click()
            time.sleep(6)
            # Rename the downloaded file
            for filename in os.listdir(self.download_path):
                if filename.endswith('.xlsx'):  # Adjust the file extension based on the actual file type
                    old_file_path = os.path.join(self.download_path, filename)
                    new_file_path = os.path.join(self.download_path, desired_file_name)
                    os.rename(old_file_path, new_file_path)
                    break
            shutil.move(new_file_path,os.path.join(self.newfolder_day, desired_file_name))
            dataframe = pd.read_excel(os.path.join(self.newfolder_day, desired_file_name),engine = 'openpyxl',sheet_name=0)
            dataframe = dataframe[dataframe['Updated Time'].str.contains(datefilter)]
            dataframe.to_excel(os.path.join(self.newfolder_day, desired_file_name), index=False)
        except Exception as e:
            time.sleep(1)
            print("Erro",e)
            fields=[self.loan,dateout,'Fail crawl_date '+str(e)[:150]]
            with open(r'log_down.csv', 'a',newline='') as f:
                writer = csv.writer(f)
                writer.writerow(fields)
            self.driver = None

if __name__ == "__main__":
    args = sys.argv
    current_directory = str(os.getcwd())
    # str(args[7]) 3 mode: day time both (day is data by day, time data by min, both data day&time) 
    # parameter func.exe HomeSolarmanpvCom(user, passw, loan, device_id, inverter_name, previous_date, current_directory)
    casedown = HomeSolarmanpvCom(user=str(args[1]), passw=str(args[2]), loan=str(args[3]), device_id=str(args[4]), inverter_name=str(args[5]), previous_date=str(args[6]), current_directory=current_directory)
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

