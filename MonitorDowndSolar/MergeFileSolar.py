import os
import pandas as pd
import openpyxl
import csv
import warnings
import shutil
from datetime import datetime, timedelta


warnings.simplefilter("ignore")


class MergeFileSolar:
    def __init__(self, folder_merge, save_file, domain):
        self.folder_merge = folder_merge
        self.save_file = save_file
        self.current_directory = str(os.getcwd())
        self.domain = domain

    def merge_min_file(self):
        src_path = self.current_directory+self.folder_merge
        print('-'*30)
        print(src_path)
        all_frame = []
        today = datetime.now()
        yesterday = today - timedelta(days=1)
        dateout = yesterday.strftime("%d/%m/%y")
        try:
            for file in os.listdir(src_path):
                sig_file = os.path.join(src_path, file)
                if file.endswith('.xlsx'):
                    book = openpyxl.load_workbook(sig_file)
                    if self.domain == 'www.soliscloud.com':
                        sheet = book.worksheets[1]
                        sheet.delete_rows(0, 28)
                    else:
                        sheet = book.worksheets[0]
                    df_sig_file = pd.DataFrame(sheet.values)
                    df_sig_file = df_sig_file.rename(
                        columns=df_sig_file.iloc[0]).drop(df_sig_file.index[0], axis=0)
                    df_sig_file = df_sig_file.reset_index(
                        drop=True).fillna('None').assign(NameFile=file)
                    all_frame.append(df_sig_file)
                elif file.endswith('.xls'):
                    if self.domain == 'www.semsportal.com':
                        df_sig_file = pd.read_excel(
                            sig_file, engine='xlrd')
                        df_sig_file = df_sig_file.rename(columns=df_sig_file.iloc[1]).drop(df_sig_file.index[0:2], axis=0).reset_index(
                            drop=True).assign(NameFile=file)
                    else:
                        df_sig_file = pd.read_excel(
                            sig_file, engine='xlrd').assign(NameFile=file)
                    all_frame.append(df_sig_file)
            if all_frame:
                all_frame_final = pd.concat(all_frame, axis=0)
                all_frame_final.to_excel(
                    self.current_directory+self.save_file, index=False)
                print(self.domain, ' Merge done!')
            else:
                fields = [self.domain, dateout, 'Fail file min combine!']
                print(fields)
                # with open(self.current_directory+r'\log_down.csv', 'a', newline='') as f:
                #     writer = csv.writer(f)
                #     writer.writerow(fields)
        except Exception as e:
            fields = [self.domain, dateout, 'Fail merge min! '+str(e)[:150]]
            with open(self.current_directory+r'\log_down.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(fields)

    def tranf_date_file(self, link_file):
        data = None
        xls = pd.ExcelFile(link_file)
        sheet0 = xls.parse(0)
        if self.domain == 'home.solarmanpv.com':
            data = sheet0.fillna('None').assign(
                NameFile=os.path.basename(link_file).split('.')[0])
            data = data.assign(day=data['Updated Time'].str[-2:])
        elif self.domain == 'globalpro.solarmanpv.com':
            data = sheet0.fillna('None').assign(
                NameFile=os.path.basename(link_file).split('.')[0])
            data = data.assign(day=data['Time'].str[-2:])
        elif self.domain == 'pro.solarmanpv.com':
            data = sheet0.fillna('None').assign(
                NameFile=os.path.basename(link_file).split('.')[0])
            data = data.assign(day=data['Time'].str[-2:])
        elif self.domain == 'server.luxpowertek.com':
            pass
        elif self.domain == 'www.hyponportal.com':
            pass
        elif self.domain == 'www.isolarcloud.com':
            data = sheet0.fillna('None').assign(
                NameFile=os.path.basename(link_file).split('.')[0])
        elif self.domain == 'server.growatt.com':
            data = sheet0.fillna('None').drop(['Unnamed: 1', 'Unnamed: 2'], axis=1)
            # keep row 15 16 is normal and keep 27 28 Hybrid
            data = data.drop(data.index[0:15], axis=0).drop(
                [17, 18, 19, 22, 23, 26, 29, 32, 33])
            data = data.set_index(data.columns[0]).T
            data.columns.name = None
            data = data.reset_index(drop=True).drop('None',axis=1)
            data = data.drop(list(data.columns.values[2:4])+list(data.columns.values[5:]),axis=1)
            data = data.drop(data.index[-1], axis=0)
            data.columns.values[0] = 'day' 
            data.columns.values[1] = 'PV1kWh'
            if data.columns.size > 2:
                data.columns.values[2] = 'PV2kWh'
            data = data.assign(NameFile=os.path.basename(link_file).split('.')[0])

        elif self.domain == 'www.semsportal.com':
            data = sheet0.drop(sheet0.index[0:19], axis=0).fillna('None')
            data = data.rename(columns=data.iloc[0]).drop(data.index[0], axis=0).reset_index(
                drop=True).assign(NameFile=os.path.basename(link_file).split('.')[0])
        elif self.domain == 'sg5.fusionsolar.huawei.com':
            book = openpyxl.load_workbook(link_file)
            sheet = book['Sheet1']
            sheet.delete_rows(0, 1)
            data = pd.DataFrame(sheet.values)
            if data.columns.stop >= 22:
                data = data.fillna('None').drop(data.columns[22], axis=1)
            else:
                data = data.fillna('None')
            data = data.rename(columns=data.iloc[0]).drop([0]).reset_index(drop=True).assign(
                NameFile=os.path.basename(link_file).split('.')[0])
            #print(list(data.filter(regex='Revenue|Loss Due to Export')),link_file)
            data = data.drop(list(data.filter(regex='Revenue|Loss Due to Export')), axis=1)
        elif self.domain == 'www.soliscloud.com':
            data = sheet0.drop(sheet0.index[0:5], axis=0)
            data = data.rename(columns=data.iloc[0]).drop(data.index[0], axis=0)
            data = data.reset_index(drop=True).fillna('None').assign(NameFile=os.path.basename(link_file).split('.')[0])

        return data

    def merge_date_file(self):
        src_path = self.current_directory+self.folder_merge
        print('-'*30)
        print(src_path)
        all_frame = []
        name_file = ''
        today = datetime.now()
        yesterday = today - timedelta(days=1)
        dateout = yesterday.strftime("%d/%m/%y")
        try:
            for file in os.listdir(src_path):
                name_file = file
                sig_file = os.path.join(src_path, file)
                df_sig_file = self.tranf_date_file(link_file=sig_file)
                all_frame.append(df_sig_file)
            if all_frame:
                all_frame_final = pd.concat(all_frame, axis=0)
                all_frame_final.to_excel(
                    self.current_directory+self.save_file, index=False)
                print(self.domain, ' Merge done!')
            else:
                # fields = [self.domain, dateout, '(Merge)Error combine file!']
                # with open(self.current_directory+r'\log_down.csv', 'a', newline='') as f:
                #     writer = csv.writer(f)
                #     writer.writerow(fields)
                print('Have not file date combine, ', self.domain)
        except Exception as e:
            print(e)
            print(name_file)
            fields = [self.domain, dateout, 'Fail merge date! '+str(e)[:150]]
            with open(self.current_directory+r'\log_down.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(fields)


if __name__ == "__main__":
    # parameter func.exe __innit__(self, folder_merge, save_file, domain)
    dir_raw_date = r'\storage\rawdata\data_byday'
    #dir_raw_date = r'\storage\data_by_hand'
    dir_raw_min = r'\storage\rawdata\data_bytime'
    dir_merge_date = r'\storage\merge\data_byday'
    dir_merge_min = r'\storage\merge\data_bytime'
    #Folder, File
    lsmerge = [['globalpro.solarmanpv.com', 'globalprosolarmanpvcom.xlsx'],
               ['home.solarmanpv.com', 'homesolarmanpvcom.xlsx'],
               ['pro.solarmanpv.com', 'prosolarmanpvcom.xlsx'],
               ['server.luxpowertek.com', 'serverluxpowertekcom.xlsx'],
               ['www.hyponportal.com', 'wwwhyponportalcom.xlsx'],
               ['www.isolarcloud.com', 'wwwisolarcloudcom.xlsx'],
               ['server.growatt.com', 'servergrowattcom.xlsx'],
               ['www.semsportal.com', 'wwwsemsportalcom.xlsx'],
               ['sg5.fusionsolar.huawei.com', 'sg5fusionsolarhuaweicom.xlsx'],
               ['www.soliscloud.com', 'wwwsoliscloudcom.xlsx']]
    for item in lsmerge:
        folder_date = dir_raw_date+'\\'+item[0]
        file_merge_date = dir_merge_date+'\\'+item[1]
        folder_min = dir_raw_min+'\\'+item[0]
        file_merge_min = dir_merge_min+'\\'+item[1]
        # print(folder_date)
        # print(file_merge_date)
        ob_date = MergeFileSolar(
            folder_merge=folder_date, save_file=file_merge_date, domain=item[0])
        ob_date.merge_date_file()
        ob_min = MergeFileSolar(
            folder_merge=folder_min, save_file=file_merge_min, domain=item[0])
        ob_min.merge_min_file()


    #ob_import = MergeFileSolar(src_file=str(args[1]), functname=str(args[2]),table_name=str(args[3]),mode=str(args[4]))
    # ob_import.import_sqlite_fromfile()
