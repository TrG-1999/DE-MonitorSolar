import os
import time
import sys
import shutil
import csv
import pandas as pd
from functools import reduce
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from subprocess import CREATE_NO_WINDOW
from datetime import datetime, timedelta


class ServerGrowattCom:

    def __init__(self, user, passw, loan, device_id, inverter_name, previous_date, current_directory):
        self.DOMAIN = 'https://server.growatt.com/'
        self.user = user
        self.passw = passw
        self.loan = loan
        self.device_id = device_id
        self.inverter_name = inverter_name
        self.previous_date = previous_date
        self.current_directory = current_directory
        self.driver = None
        self.download_path = current_directory+r'\storage\temp\server.growatt.com'
        self.newfolder = current_directory+r'\storage\rawdata\data_bytime\server.growatt.com'
        self.newfolder_day = current_directory+r'\storage\rawdata\data_byday\server.growatt.com'

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
        try:
            time.sleep(3)
            elementval = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="val_loginAccount"]')))
            elementval.send_keys(self.user)
            time.sleep(2)
            elementval = WebDriverWait(driver, 7).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="val_loginPwd"]')))
            elementval.send_keys(self.passw)
            time.sleep(1)
            elementval = WebDriverWait(driver, 7).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="body"]/div[1]/div[2]/div[4]/div/div[2]/div[5]/button')))
            elementval.click()
            # End click btn login
            time.sleep(5)
            self.driver = driver
        except Exception as e:
            # IF Erro return None Value
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
        # Get date for downloads
        today = datetime.now()
        yesterday = today - timedelta(days=int(self.previous_date))
        formatted_date = yesterday.strftime("%Y-%m-%d")
        desired_file_name = yesterday.strftime("%Y%m%d_")+self.loan+'.xlsx'
        dateout = yesterday.strftime("%m/%d/%Y")
        # run crawl data
        # check login page
        if self.driver == None:
            fields=[self.loan,dateout,'Login Fail page! (by min)']
            with open(self.current_directory+r'\log_down.csv', 'a',newline='') as f:
                writer = csv.writer(f)
                writer.writerow(fields)
            return
        try:
            if self.inverter_name != 'None':
                # Search place
                elementval = WebDriverWait(self.driver, 7).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="plantSerch"]')))
                time.sleep(1)
                elementval.send_keys(self.inverter_name)
                time.sleep(1)
                elementval.send_keys(Keys.ENTER)
                time.sleep(5)
                #choise plane //*[@id="selectPlant-con"]/ul/li
                elementval = WebDriverWait(self.driver, 7).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="selectPlant-con"]/ul/li')))
                elementval.click()
                WebDriverWait(self.driver, 7).until(EC.number_of_windows_to_be(2))
                self.driver.switch_to.window(self.driver.window_handles[1])
                time.sleep(4)

            # Get element click date
            time.sleep(6)
            try:
                elementval = WebDriverWait(self.driver, 7).until(EC.element_to_be_clickable((By.XPATH, "(//*[@class='floatR timeSelDiv'])//*[@class='prevLeft prvTime']")))
            except Exception as e:
                elementval = WebDriverWait(self.driver, 7).until(EC.element_to_be_clickable((By.XPATH, "(//*[@class='timeSelDiv'])//*[@class='prevLeft prvTime']")))
            for x in range(1,int(self.previous_date)+1):
                elementval.click()
                time.sleep(10)
            if "Hybrid" in self.device_id:
                elementDate = ((int(self.previous_date)+1)*3)-1
            else:
                elementDate = self.previous_date

            inputjscript = """
                var chart = Highcharts.charts["""+str(elementDate)+"""];
                var output = []
                var datatime = [];
                var dataraw = [];
                var dictname = { };
                for (let i =0;i < chart.series.length; i++){
                    nametitle = 
                    chart.series[i].data.forEach(function (point) {
                        datatime.push(point.category);
                        dataraw.push(point.y);
                    });
                    dictname['time'] = datatime;
                    dictname[chart.series[i].name] = dataraw;
                    output.push(dictname);
                    datatime = [];
                    dataraw = [];
                    dictname = { };
                }

                return output;
                """
            lsdict = []
            outputjscript = self.driver.execute_script(inputjscript)
            for dct in outputjscript:
                lsdict.append(pd.DataFrame.from_dict(dct))

            df_final = reduce(lambda left, right: pd.merge(left, right, on='time', how='inner'), lsdict)
            df_final.to_excel(os.path.join(self.download_path,'tmp_growatt.xlsx'), index=False)
            # Rename the downloaded file
            for filename in os.listdir(self.download_path):
                if filename.endswith('.xlsx'):  # Adjust the file extension based on the actual file type
                    old_file_path = os.path.join(self.download_path, filename)
                    new_file_path = os.path.join(self.download_path, desired_file_name)
                    os.rename(old_file_path, new_file_path)
                    break
            shutil.move(new_file_path,os.path.join(self.newfolder, desired_file_name))
            print('Done Export '+self.loan)
        except Exception as e:
            time.sleep(1)
            errs = str(e).replace(',',' ')
            errs = errs.replace('\n',' ')
            fields=[self.loan,dateout,'Fail crawl_min '+errs[:150]]
            with open(r'log_down.csv', 'a',newline='') as f:
                writer = csv.writer(f)
                writer.writerow(fields)
            self.driver = None
        # Close the browser session
        # driver.switch_to.window(driver.window_handles[0])
        

    def crawl_date(self):
        try:
            # Get today's date
            today = datetime.now()
            # Subtract one day to get yesterday's date
            yesterday = today - timedelta(days=int(self.previous_date))
            # distance month
            dis_month = (today.year - yesterday.year) * \
                12 + (today.month - yesterday.month)
            # Format yesterday's date as "yyyy-mm-dd"
            desired_file_name = yesterday.strftime("%Y%m_")+self.loan+'.xls'
            dateout = yesterday.strftime("%m/%d/%Y")
            # check login page
            if self.driver == None:
                fields=[self.loan,dateout,'Login Fail page! (by date)']
                with open(self.current_directory+r'\log_down.csv', 'a',newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(fields)
                return
            self.driver.get(self.DOMAIN)
            #click to Energ
            time.sleep(7)
            elementval = WebDriverWait(self.driver, 7).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="bodyContent"]/div[1]/div[3]/div[3]/div[4]')))
            elementval.click()
            time.sleep(3)
            if self.device_id != 'None':
                # search device
                elementval = WebDriverWait(self.driver, 7).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="val_energy_compare_search"]')))
                elementval.send_keys(self.device_id)
                time.sleep(2)
                # choise device
                elementval = WebDriverWait(self.driver, 7).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="mCSB_1_container"]/div[1]/div/div')))
                elementval.click()
                time.sleep(2)
            # click to date
            elementval = WebDriverWait(self.driver, 7).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="div_pageContent"]/div[4]/div/div[2]/div[1]/div/div[2]/div[1]/div[1]/i[2]')))
            elementval.click()
            time.sleep(2)
            # click previus months
            for i in range(int(dis_month)):
                elementval = WebDriverWait(self.driver, 7).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="div_pageContent"]/div[4]/div/div[2]/div[1]/div/div[2]/div[1]/div[1]/div/i[1]')))
                elementval.click()
                time.sleep(2)

            # click to export
            elementval = WebDriverWait(self.driver, 7).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="div_pageContent"]/div[4]/div/div[2]/div[1]/div/div[2]/div[1]/div[2]/div/div/div/input')))
            elementval.click()
            time.sleep(1)
            # export
            elementval = WebDriverWait(self.driver, 7).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="div_pageContent"]/div[4]/div/div[2]/div[1]/div/div[2]/div[1]/div[2]/div/div/dl/dd[2]')))
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
    # parameter func.exe ServerGrowattCom(user, passw, loan, device_id, inverter_name, previous_date, current_directory)
    casedown = ServerGrowattCom(user=str(args[1]), passw=str(args[2]), loan=str(args[3]), device_id=str(args[4]), inverter_name=str(args[5]), previous_date=str(args[6]), current_directory=current_directory)
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

