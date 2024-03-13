import os
import time
import sys
import shutil
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from subprocess import CREATE_NO_WINDOW
from datetime import datetime, timedelta
from selenium.webdriver.common.action_chains import ActionChains


class GlobalProsolarmanpvCom:

    def __init__(self, user, passw, loan, device_id, inverter_name, previous_date, current_directory):
        self.DOMAIN = 'https://globalpro.solarmanpv.com/'
        self.user = user
        self.passw = passw
        self.loan = loan
        self.device_id = device_id
        self.inverter_name = inverter_name
        self.previous_date = previous_date
        self.current_directory = current_directory
        self.driver = None
        self.download_path = current_directory+r'\storage\temp\globalpro.solarmanpv.com'
        self.newfolder = current_directory + \
            r'\storage\rawdata\data_bytime\globalpro.solarmanpv.com'
        self.newfolder_day = current_directory + \
            r'\storage\rawdata\data_byday\globalpro.solarmanpv.com'

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
        # input username and pass
        try:
            try:
                # agree //*[@id="app"]/div[3]/div[2]/div/div[3]/button[1]
                elementval = WebDriverWait(driver, 8).until(EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="app"]/div[3]/div[2]/div/div[3]/button[1]')))
                elementval.click()
                time.sleep(2)
            except Exception as e:
                print('Not have Popup!')

            try:
                # country //*[@id="areaList"]/div[1]/div[2]
                elementval = WebDriverWait(driver, 7).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="areaList"]/div[1]/div[2]')))
                elementval.click()
                time.sleep(2)
                # confirm //*[@id="app"]/div[3]/div[5]/div/div/div[1]/div/div/div[3]/button
                elementval = WebDriverWait(driver, 7).until(EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="app"]/div[3]/div[5]/div/div/div[1]/div/div/div[3]/button')))
                elementval.click()
                time.sleep(2)
            except Exception as e:
                print('Not have popup country!')

            # verify Bar
            print('navigator Bar')
            element_hold = driver.find_element(
                'xpath', '/html/body/div[2]/div[5]/div[3]/div[6]/section/div/div[2]/div[4]/div/div/div/div/span')

            action = ActionChains(driver)
            action.click_and_hold(element_hold).perform()
            action.move_by_offset(311, 0).perform()
            action.release().perform()
            time.sleep(2)
            print('done bar')
            # elementval = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div[3]/div[6]/section/div[2]/div[2]/div[2]/div/input')))
            elementval = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, '//input[@name="eMail"]')))
            elementval.send_keys(self.user)
            time.sleep(2)
            # //*[@id="password"]
            # elementval = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div[3]/div[6]/section/div[2]/div[2]/div[3]/input')))
            elementval = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//input[@name="password"]')))
            elementval.send_keys(self.passw)
            time.sleep(1)
            # //*[@id="loginHolder"]/div/div[4]/button
            # elementval = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div[3]/div[6]/section/div[2]/div[2]/button')))
            elementval = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//button[@name="login"]')))
            elementval.click()
            time.sleep(1)
            # know //*[@id="mainFrame"]/aside/div[3]/div[3]/div[2]/button[1]
            try:
                elementval = WebDriverWait(driver, 6).until(EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="mainFrame"]/aside/div[3]/div[3]/div[2]/button[1]')))
                elementval.click()
            except Exception as e:
                print('time 2 lick End')
                elementval = WebDriverWait(driver, 6).until(EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="app"]/div[3]/div[2]/aside/div[3]/div[3]/div[2]/button[1]')))
                elementval.click()
            time.sleep(3)
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
        # distance month
        dis_month = (today.year - yesterday.year) * \
            12 + (today.month - yesterday.month)
        # Format yesterday's date as "yyyy-mm-dd"
        formatted_date = yesterday.strftime("%Y/%m/%d")
        desired_file_name = yesterday.strftime("%Y%m%d_")+self.loan+'.xlsx'
        dateout = yesterday.strftime("%m/%d/%Y")
        if self.driver == None:
            fields = [self.loan, dateout, 'Login Fail page! (by min)']
            with open(self.current_directory+r'\log_down.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(fields)
            return
        try:
            time.sleep(1)
            self.driver.get(self.DOMAIN+'business/maintain/device')
            time.sleep(1)
            if self.device_id != 'None':
                # input device //input[@name="maintainSearchKey"]
                elementval = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, '//input[@name="maintainSearchKey"]')))
                elementval.send_keys(self.device_id)
                # search //div[@class="iconfont iconsearch"]
                time.sleep(1)
                elementval = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, '//div[@class="iconfont iconsearch"]')))
                elementval.click()
                time.sleep(4)
            # click table
            elementval = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(
                (By.XPATH, '//button[@title="System"]/div/div[@class="iconfont iconparentSystem"]')))
            elementval.click()
            time.sleep(2)
            WebDriverWait(self.driver, 5).until(EC.number_of_windows_to_be(2))
            self.driver.switch_to.window(self.driver.window_handles[1])
            time.sleep(6)
            # confirm
            flag_confirm = 0
            try:
                elementval = WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="mainFrame"]/aside/div[4]/div[3]/div[2]/button')))
                elementval.click()
            except Exception as e:
                print('time end 2')
                flag_confirm = 1
            try:
                if flag_confirm == 1:
                    elementval = WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable(
                        (By.XPATH, '//*[@id="app"]/div[3]/div[3]/aside/div[4]/div[3]/div[2]/button')))
                    elementval.click()
            except Exception as e:
                print('Not end button')
            # //*[@id="prev"]
            time.sleep(2)
            elementval = WebDriverWait(self.driver, 5).until(                     
                EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div[3]/div[3]/section/div/div/div[9]/div[1]/div[4]/div/div[1]/div[2]/div[3]/div[2]/input')))
            elementval.click()
            time.sleep(3)
            # find months
            elementval = WebDriverWait(self.driver, 3).until( 
                EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div[3]/div[3]/section/div/div/div[9]/div[1]/div[4]/div/div[1]/div[2]/div[3]/div[2]/div/div[2]/div[1]/a[3]')))
            for x in range(dis_month):
                elementval.click()
                time.sleep(1)
            print('step find moths done')
            time.sleep(1)
            for x in range(8, 50):
                elementval = WebDriverWait(self.driver, 50).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div[3]/div[3]/section/div/div/div[9]/div[1]/div[4]/div/div[1]/div[2]/div[3]/div[2]/div/div[2]/div[2]/div[1]/a['+str(x)+']')))
                if elementval.get_attribute('title') == formatted_date:
                    print(elementval.get_attribute('title'))
                    elementval.click()
                    time.sleep(3)
                    break
            print('step find date done')
            # //div[@class="posR"]/button[2]
            elementval = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@class="posR"]/button[2]')))
            elementval.click()
            time.sleep(6)
            print('Done download time file')
            self.driver.close()
            time.sleep(1)
            self.driver.switch_to.window(self.driver.window_handles[0])
            time.sleep(1)
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
            fields = [self.loan, dateout, 'Fail crawl_min '+str(e)[:150]]
            with open(r'log_down.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(fields)

    def crawl_date(self):
        # Get today's date
        today = datetime.now()
        # Subtract one day to get yesterday's date
        yesterday = today - timedelta(days=int(self.previous_date))
        # Format yesterday's date as "yyyy-mm-dd"
        # distance year
        dis_year = (today.year - yesterday.year)
        formatted_date = yesterday.strftime("%Y/%m")
        desired_file_name = yesterday.strftime("%Y%m_")+self.loan+'.xlsx'
        dateout = yesterday.strftime("%m/%d/%Y")
        if self.driver == None:
            fields = [self.loan, dateout, 'Login Fail page! (by date)']
            with open(self.current_directory+r'\log_down.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(fields)
            return
        try:
            time.sleep(1)
            self.driver.get(self.DOMAIN+'business/maintain/device')
            time.sleep(3)
            if self.device_id != 'None':
                # input device //input[@name="maintainSearchKey"]
                elementval = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, '//input[@name="maintainSearchKey"]')))
                elementval.send_keys(self.device_id)
                # search //div[@class="iconfont iconsearch"]
                time.sleep(1)
                elementval = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, '//div[@class="iconfont iconsearch"]')))
                elementval.click()
                time.sleep(4)
            # click table
            elementval = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(
                (By.XPATH, '//button[@title="System"]/div/div[@class="iconfont iconparentSystem"]')))
            elementval.click()
            time.sleep(2)
            #WebDriverWait(self.driver, 5).until(EC.number_of_windows_to_be(2))
            #original_window = self.driver.current_window_handle
            self.driver.switch_to.window(self.driver.window_handles[-1])
            time.sleep(6)
            # confirm
            flag_confirm = 0
            try:
                elementval = WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="mainFrame"]/aside/div[4]/div[3]/div[2]/button')))
                elementval.click()
            except Exception as e:
                print('time end 2')
                flag_confirm = 1
            try:
                if flag_confirm == 1:
                    elementval = WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable(
                        (By.XPATH, '//*[@id="app"]/div[3]/div[3]/aside/div[4]/div[3]/div[2]/button')))
                    elementval.click()
            except Exception as e:
                print('Not end button')
            # click to month
            time.sleep(2)
            elementval = WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div[3]/div[3]/section/div/div/div[9]/div[1]/div[4]/div/div[1]/div[2]/div[1]/button[2]')))
            elementval.click()
            time.sleep(1)
            # click input date
            elementval = WebDriverWait(self.driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div[3]/div[3]/section/div/div/div[9]/div[1]/div[4]/div/div[1]/div[2]/div[3]/div[2]/input')))
            elementval.click()
            time.sleep(1)
            # last year
            elementval = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div[3]/div[3]/section/div/div/div[9]/div[1]/div[4]/div/div[1]/div[2]/div[3]/div[2]/div/div[2]/div[1]/a[2]')))
            for x in range(int(dis_year)):
                elementval.click()
                time.sleep(1.5)
            print('step find year done')
            # find months
            elementval = WebDriverWait(self.driver, 50).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div[3]/div[3]/section/div/div/div[9]/div[1]/div[4]/div/div[1]/div[2]/div[3]/div[2]/div/div[2]/div[2]/div[2]/a['+str(yesterday.month)+']')))
            elementval.click()
            time.sleep(2)
            # //div[@class="posR"]/button[2]
            elementval = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@class="posR"]/button[2]')))
            elementval.click()
            time.sleep(6)
            print('Done download date file')
            self.driver.close()
            time.sleep(1)
            self.driver.switch_to.window(self.driver.window_handles[0])
            time.sleep(1)
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
            fields = [self.loan, dateout, 'Fail crawl_date '+str(e)[:150]]
            with open(r'log_down.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(fields)


if __name__ == "__main__":
    args = sys.argv
    current_directory = str(os.getcwd())
    # str(args[7]) 3 mode: day time both (day is data by day, time data by min, both data day&time)
    # parameter func.exe GlobalProsolarmanpvCom(user, passw, loan, device_id, inverter_name, previous_date, current_directory)
    casedown = GlobalProsolarmanpvCom(user=str(args[1]), passw=str(args[2]), loan=str(args[3]), device_id=str(
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
