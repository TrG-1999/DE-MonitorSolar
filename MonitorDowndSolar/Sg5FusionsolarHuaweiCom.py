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


class Sg5FusionsolarHuaweiCom:
    
    def __init__(self, user, passw, loan, device_id, inverter_name, previous_date, current_directory):
        self.DOMAIN = 'https://sg5.fusionsolar.huawei.com/'
        self.user = user
        self.passw = passw
        self.loan = loan
        self.device_id = device_id
        self.inverter_name = inverter_name
        self.previous_date = previous_date
        self.current_directory = current_directory
        self.driver = None
        self.download_path = current_directory+r'\storage\temp\sg5.fusionsolar.huawei.com'
        self.newfolder = current_directory+r'\storage\rawdata\data_bytime\sg5.fusionsolar.huawei.com'
        self.newfolder_day = current_directory+r'\storage\rawdata\data_byday\sg5.fusionsolar.huawei.com'

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
        driver = webdriver.Chrome(service=chrome_service,options=chrome_options)
        # Navigate to the page with the file download link
        driver.get(self.DOMAIN)
        # input username and pass
        try:
            time.sleep(3)
            elementval = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="username"]/input')))
            elementval.send_keys(self.user)
            time.sleep(2)
            #//*[@id="password"]
            elementval = WebDriverWait(driver, 7).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="password"]/input')))
            elementval.send_keys(self.passw)
            time.sleep(1)
            #//*[@id="loginHolder"]/div/div[4]/button
            elementval = WebDriverWait(driver, 7).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="submitDataverify"]')))
            elementval.click()
            time.sleep(6)
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
        desired_file_name = yesterday.strftime("%Y%m%d_")+self.loan+'.xlsx'
        dateout = yesterday.strftime("%m/%d/%Y")
        # check login page
        if self.driver == None:
            fields=[self.loan,dateout,'Login Fail page! (by min)']
            with open(self.current_directory+r'\log_down.csv', 'a',newline='') as f:
                writer = csv.writer(f)
                writer.writerow(fields)
            return
        try:
            # Set browser options to specify the download location 
            elementval = WebDriverWait(self.driver, 7).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="dpFrameworkHeader"]/div/div[1]/div[1]/div/div/a[3]')))
            time.sleep(1)
            # search plan of divice Id //*[@id="searchName"]
            elementval = WebDriverWait(self.driver, 7).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="searchName"]')))
            elementval.send_keys(self.device_id)
            time.sleep(1)
            # click search 
            elementval = WebDriverWait(self.driver, 7).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div/div[2]/div/div/div[2]/div[1]/form/div[7]/div/div/div/button[1]')))
            elementval.click()
            time.sleep(2)
            #get https://sg5.fusionsolar.huawei.com/pvmswebsite/assets/build/index.html#/view/station/NE=33940121/overview
            # click plant 
            elementval = WebDriverWait(self.driver, 7).until(EC.element_to_be_clickable((By.XPATH, "//*[@class='ant-table-cell nco-cloumn-relative ant-table-cell-ellipsis']//a")))
            elementval.click()
            print('chose time')
            time.sleep(4)  # Adjust this wait time based on the website's loading time
            try:
                elementval = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[@class='nco-single-energy-header-datetime']//*[@class='ant-picker-input']/input")))
            except Exception as e:
                #//*[@class='ant-picker']//*[@class='ant-picker-input']/input
                elementval = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//*[@class='ant-picker']//*[@class='ant-picker-input']/input")))
            # Get the captured network logs
            print('find choise time done')
            time.sleep(1)
            elementval.send_keys(Keys.CONTROL + "a")
            time.sleep(2)
            elementval.send_keys(Keys.DELETE)
            time.sleep(1)
            elementval.send_keys(formatted_date)
            time.sleep(2)
            elementval.send_keys(Keys.ENTER)
            time.sleep(8)
            logs = self.driver.execute_script("return window.performance.getEntries();")
            for log in logs:
                if log['name'].startswith(self.DOMAIN+'rest/pvms/web/station/v1/overview/energy-balance'):  # Filter out browser's internal requests
                    url = log['name']
                    # response_time = log['responseEnd'] - log['responseStart']  # Response time
                    # Access more attributes from the log as needed
                    # print(f"URL: {url}")
                    # print(f"Response Time: {response_time} ms")
                    print(url)
                    if formatted_date in url:
                        print(formatted_date)
                        self.driver.get(url)
                        elementval = WebDriverWait(self.driver, 7).until(EC.element_to_be_clickable((By.XPATH, "/html/body/pre")))
                        data = json.loads(elementval.text)
                        # print(type(data))
                        break
                    else:
                        #&dateTime=2024-03-10%2000%3A00%3A00 unless datetime and add datetime
                        if '&dateTime=' not in url:
                            self.driver.get(url+'&dateTime='+formatted_date+r'%2000%3A00%3A00')
                            elementval = WebDriverWait(self.driver, 7).until(EC.element_to_be_clickable((By.XPATH, "/html/body/pre")))
                            data = json.loads(elementval.text)
                            # print(type(data))s
                            break

            df_final = pd.DataFrame(data['data'])
            df_final.to_excel(os.path.join(self.download_path,'tmp_huawei.xlsx'), index=False)
            print('Export done by time')
            # Rename the downloaded file
            for filename in os.listdir(self.download_path):
                if filename.endswith('.xlsx'):  # Adjust the file extension based on the actual file type
                    old_file_path = os.path.join(self.download_path, filename)
                    new_file_path = os.path.join(self.download_path, desired_file_name)
                    os.rename(old_file_path, new_file_path)
                    break
            shutil.move(new_file_path,os.path.join(self.newfolder, desired_file_name))
        except Exception as e:
            time.sleep(1)
            print("Erro",e)
            errs = str(e).replace(',',' ')
            errs = errs.replace('\n',' ')
            fields=[self.loan,dateout,'Fail crawl_min '+errs[:150]]
            with open(r'log_down.csv', 'a',newline='') as f:
                writer = csv.writer(f)
                writer.writerow(fields)

    def crawl_date(self):
        # Get today's date
        today = datetime.now()
        # Subtract one day to get yesterday's date
        yesterday = today - timedelta(days=int(self.previous_date))
        # Format yesterday's date as "yyyy-mm-dd"
        formatted_date = yesterday.strftime("%Y-%m")
        desired_file_name = yesterday.strftime("%Y%m_")+self.loan+'.xlsx'
        dateout = yesterday.strftime("%m/%d/%Y")
        # check login page
        if self.driver == None:
            fields=[self.loan,dateout,'Login Fail page! (by day)']
            with open(self.current_directory+r'\log_down.csv', 'a',newline='') as f:
                writer = csv.writer(f)
                writer.writerow(fields)
            return
        try:
            time.sleep(1)
            self.driver.get(self.DOMAIN)
            # Set browser options to specify the download location 
            elementval = WebDriverWait(self.driver, 7).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="dpFrameworkHeader"]/div/div[1]/div[1]/div/div/a[3]')))
            time.sleep(1)
            # search plan of divice Id //*[@id="searchName"]
            elementval = WebDriverWait(self.driver, 7).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="searchName"]')))
            elementval.send_keys(self.device_id)
            time.sleep(1)
            # click search 
            elementval = WebDriverWait(self.driver, 7).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div/div[2]/div/div/div[2]/div[1]/form/div[7]/div/div/div/button[1]')))
            elementval.click()
            time.sleep(2)
            # click plant 
            # elementval = WebDriverWait(self.driver, 7).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div/div[2]/div/div/div[2]/div[4]/div/div/div/div/div/div/div/table/tbody/tr/td[3]/div/a')))
            # elementval.click()
            elementval = WebDriverWait(self.driver, 7).until(EC.element_to_be_clickable((By.XPATH, "//*[@class='ant-table-cell nco-cloumn-relative ant-table-cell-ellipsis']//a")))
            elementval.click()
            time.sleep(1)
            # click report manager 
            elementval = WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div/div/div[3]/div[2]/div/div[1]/span[3]/a')))
            elementval.click()
            time.sleep(1)
            # click expand Month 
            elementval = WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div/div/div/div/div/div/div/div[3]/div[2]/div/div[2]/div/div/div/div/div[2]/div/div[1]/div/div/div[1]/div[1]/div/form/div[1]/div[2]/div/div/div/div[1]/span[2]')))
            elementval.click()
            time.sleep(1)
            elementval = WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div/div/div/div/div/div/div/div[3]/div[2]/div/div[2]/div/div/div/div/div[2]/div/div[1]/div/div/div[1]/div[1]/div/form/div[1]/div[2]/div/div/div/div[2]/div/div/div/div[2]/div/div/div/div[2]/div')))
            elementval.click()
            time.sleep(1)
            # change date 
            elementval = WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="statisticTime"]')))
            time.sleep(1)
            elementval.send_keys(Keys.CONTROL + "a")
            time.sleep(2)
            elementval.send_keys(Keys.DELETE)
            time.sleep(1)
            elementval.send_keys(formatted_date)
            time.sleep(2)
            elementval.send_keys(Keys.ENTER)
            time.sleep(1)
            #click export 
            elementval = WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div/div/div/div/div/div/div/div[3]/div[2]/div/div[2]/div/div/div/div/div[2]/div/div[1]/div/div/div[1]/div[2]/button[2]')))
            elementval.click()
            time.sleep(1)
            # click down
            elementval = WebDriverWait(self.driver, 7).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div[2]/div/div[2]/div[2]/div/div[2]/div/div[3]/div/a[1]')))
            elementval.click()
            time.sleep(1)
            #click remove 
            elementval = WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div[2]/div/div[2]/div[2]/div/div[2]/div/div[3]/div/a[2]')))
            elementval.click()
            time.sleep(1)
            #confirm 
            elementval = WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div/div[2]/div/div[2]/div/div/div[2]/button[2]')))
            elementval.click()
            time.sleep(1)
            # oke done
            elementval = WebDriverWait(self.driver, 4).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div/div[2]/div/div[2]/div/div/div[2]/button')))
            elementval.click()
            time.sleep(1)
            print('Download done by date')
            # Rename the downloaded file
            for filename in os.listdir(self.download_path):
                if filename.endswith('.xlsx'):  # Adjust the file extension based on the actual file type
                    old_file_path = os.path.join(self.download_path, filename)
                    new_file_path = os.path.join(self.download_path, desired_file_name)
                    os.rename(old_file_path, new_file_path)
                    break
            shutil.move(new_file_path,os.path.join(self.newfolder_day, desired_file_name))
        except Exception as e:
            time.sleep(1)
            print("Erro",e)
            errs = str(e).replace(',',' ')
            errs = errs.replace('\n',' ')
            fields=[self.loan,dateout,'Fail crawl_date '+errs[:150]]
            with open(r'log_down.csv', 'a',newline='') as f:
                writer = csv.writer(f)
                writer.writerow(fields)


if __name__ == "__main__":
    args = sys.argv
    current_directory = str(os.getcwd())
    # str(args[7]) 3 mode: day time both (day is data by day, time data by min, both data day&time) 
    # parameter func.exe Sg5FusionsolarHuaweiCom(user, passw, loan, device_id, inverter_name, previous_date, current_directory)
    casedown = Sg5FusionsolarHuaweiCom(user=str(args[1]), passw=str(args[2]), loan=str(args[3]), device_id=str(args[4]), inverter_name=str(args[5]), previous_date=str(args[6]), current_directory=current_directory)
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

