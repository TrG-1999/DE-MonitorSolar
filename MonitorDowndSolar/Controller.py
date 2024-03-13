import pandas as pd
import time
import subprocess
import os
import shutil
import sqlite3
from datetime import datetime, timedelta


class Controller:
    def __init__(self, file_template, current_directory):
        self.file_template = file_template
        self.current_directory = current_directory
        self.dataframe = None
        self.dict_tool = {
            'globalpro.solarmanpv.com': 'py GlobalProsolarmanpvCom.py ',
            'home.solarmanpv.com': 'py HomeSolarmanpvCom.py ',
            'pro.solarmanpv.com': 'py ProSolarmanpvCom.py ',
            'server.luxpowertek.com': 'py ServerLuxpowertekCom.py ',
            'www.hyponportal.com': 'wwwhyponportalcom.exe ',
            'www.isolarcloud.com': 'py IsolarcloudCom.py ',
            'server.growatt.com': 'py ServerGrowattCom.py ',
            'www.semsportal.com': 'py SemsportalCom.py ',
            'www.hyponportal.com': 'py wwwhyponportalcom.py ',
            'sg5.fusionsolar.huawei.com': 'py Sg5FusionsolarHuaweiCom.py ',
            'www.soliscloud.com': 'py SoliscloudCom.py '
        }
        self.dir_merge_date = r'\storage\merge\data_byday'
        self.dir_merge_min = r'\storage\merge\data_bytime'
        self.dir_raw_min = r'\storage\rawdata\data_bytime'
        self.dir_raw_date = r'\storage\rawdata\data_byday'
        self.prefix_date = 'tmp_date_'
        self.prefix_min = 'tmp_min_'
        self.tool_merge_file = 'py MergeFileSolar.py '
        self.str_merge_sqlite = 'py ImportDB.py '
        self.yesterday = datetime.now() - timedelta(days=1)
        self.dateout = self.yesterday.strftime("%d/%m/%y")

    def archive_file(self,old_folder,new_folder):
        lst_dir_old = os.listdir(old_folder)
        lst_dir_new = os.listdir(new_folder)
        for dirc in lst_dir_old:
            path_new = os.path.join(new_folder, dirc)
            path_old = os.path.join(old_folder, dirc)
            if dirc not in lst_dir_new:
                os.mkdir(path_new) 
                print("Directory '% s' created dst folder" % path_new)
            
            for file in os.listdir(path_old):
                shutil.move(os.path.join(path_old,file), os.path.join(path_new,file))

        print('Archve Done!')

    def run_archive(self):
        self.archive_file(self.current_directory+self.dir_raw_min,self.current_directory+r'\storage\Archive\data_bytime')
        self.archive_file(self.current_directory+self.dir_raw_date,self.current_directory+r'\storage\Archive\data_byday')

    def read_dataframe_template(self):
        try:
            dataframe = pd.read_excel(
                self.file_template, engine='openpyxl', sheet_name='Sheet1', dtype={'PASSWORD': object})
            self.dataframe = dataframe.fillna('None')
            # print(self.dataframe)
        except Exception as e:
            print('Error Read Template: ', e)
            self.dataframe = None

    def call_download(self, domain, mode, item):
        # mode: both - data - time
        if self.dict_tool.get(str(domain), 'None') == 'None':
            print('Check again Domain for Tool')
            print('-'*20)
        else:
            subprocess.Popen(self.dict_tool.get(str(domain), 'None')+'"'+str(item['USERNAME'])+'"'+' '+str(item['PASSWORD'])+' '+str(item['LOAN'])+' '+'"'+str(
                item['DEVICE_ID'])+'"'+' '+'"'+str(item['INVERTER TYPE'])+'"'+' '+str(item['LAST_DATE'])+' '+str(mode), cwd=self.current_directory).wait()
            time.sleep(2)

    def run_download(self):
        for index, row in self.dataframe.iterrows():
            print('index run ', int(index)+1)
            self.call_download(domain=row['DOMAIN'], mode='both', item=row)

    def merge_raw_sqlite(self):
        # agrs1: src_file(Excel) | args2: functioname | args3: tablename | args4: mode(1 create/0 exist) | args5: dbname
        # (src_file=r'template_solar_all.xlsx', functname='import_sqlite_fromfile',table_name='template_solar_all',mode='1', dbname='rawdb.db')
        src_merge_date = self.current_directory+self.dir_merge_date
        src_merge_min = self.current_directory+self.dir_merge_min
        try:
            # import sqlite date
            for file in os.listdir(src_merge_date):
                link_file = src_merge_date+'\\'+file
                subprocess.Popen(self.str_merge_sqlite+link_file+' '+'import_sqlite_fromfile'+' ' +
                                 self.prefix_date+str(file.split('.')[0])+' 1 '+'rawdb.db', cwd=self.current_directory).wait()
                time.sleep(2)
            # import sqlite min
            for file in os.listdir(src_merge_min):
                link_file = src_merge_min+'\\'+file
                subprocess.Popen(self.str_merge_sqlite+link_file+' '+'import_sqlite_fromfile'+' ' +
                                 self.prefix_min+str(file.split('.')[0])+' 1 '+'rawdb.db', cwd=self.current_directory).wait()
                time.sleep(2)

        except Exception as e:
            print('Fail run funct merge_raw_sqlite', e)

    def merge_file_all(self):
        subprocess.Popen(self.tool_merge_file,
                         cwd=self.current_directory).wait()
        time.sleep(2)

    def run_sql_file(self):
        subprocess.Popen(self.str_merge_sqlite+' None'+' '+'run_file_sql' +
                         ' None'+' 1 '+'rawdb.db', cwd=self.current_directory).wait()
        time.sleep(2)

    def export_data_for_webchart(self):
        subprocess.Popen(self.str_merge_sqlite+' None'+' '+'export_for_webchart' +
                         ' None'+' 0 '+'rawdb.db', cwd=self.current_directory).wait()
        time.sleep(2)

    def recheck_download(self, status_fail):
        lsredownload = []
        lsfinish = []
        allstatus = []
        flag = 0
        # get user for check
        dfuser_check = self.dataframe
        # Get today's date
        today = datetime.now()
        col = list(self.dataframe)
        col.append('DATE')
        for index, row in dfuser_check.iterrows():
            yesterday = today - timedelta(days=int(row['LAST_DATE']))
            name_check = yesterday.strftime("%Y%m%d_")+row['LOAN']
            flag = 1
            for subfile in os.listdir(self.current_directory+self.dir_raw_min+'\\'+row['DOMAIN']):
                if name_check in subfile:
                    lsrow = list(row)
                    lsrow.append(yesterday.strftime("%Y%m%d"))
                    lsfinish.append(lsrow)
                    flag = 0
                    break

            if flag:
                lsrow = list(row)
                lsrow.append(yesterday.strftime("%Y%m%d"))
                lsredownload.append(lsrow)

        dfredown = pd.DataFrame(lsredownload, columns=col)
        self.dataframe = dfredown[['DOMAIN','LOAN','USERNAME','PASSWORD','INVERTER TYPE','DEVICE_ID','LAST_DATE']]
        print('-'*50,'Redownload ','-'*50)
        print(self.dataframe)
        allstatus.append(pd.DataFrame(
            lsfinish, columns=col).assign(STATUS_DOWN='Success'))
        allstatus.append(dfredown.assign(STATUS_DOWN=str(status_fail)))
        df_all_status = pd.concat(allstatus, axis=0)[['DOMAIN','LOAN','LAST_DATE','DATE','STATUS_DOWN']]
        df_all_status.to_excel(
            self.current_directory+r'\status_down.xlsx', index=False)

        subprocess.Popen(self.str_merge_sqlite+self.current_directory+r'\status_down.xlsx'+' '+'import_sqlite_fromfile' +
                         ' status_down 0 '+'rawdb.db', cwd=self.current_directory).wait()
        time.sleep(2)


if __name__ == "__main__":
    current_directory = str(os.getcwd())
    control = Controller(file_template=current_directory +
                         r'\template_solar.xlsx', current_directory=current_directory)
    # #load data for template
    control.read_dataframe_template()
    #run download data
    control.run_download()
    #Check fail and filter data for run again
    control.recheck_download(status_fail='Redownload')
    #run download data again
    control.run_download()
    #check fail and add status fail
    control.recheck_download(status_fail='Fail')
    #merge file and process data
    control.merge_file_all()
    control.merge_raw_sqlite()
    control.run_sql_file()
    #archive file from raw data
    control.run_archive()
    #export for webchart
    control.export_data_for_webchart()
