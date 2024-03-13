import pandas as pd
import psycopg2
import os
import sys
import csv
import json
import sqlite3
import pandas.io.sql as psql
from datetime import datetime, timedelta

"""
parameter for call exe src_file functname mode
"""
class ImportDB:
    def __init__(self, src_file, table_name, mode, dbname):
        self.src_file = src_file
        self.mode = mode
        self.table_name = table_name
        self.current_directory = str(os.getcwd())
        self.conf_db_postgres = r'config_postgres.json'
        self.sqlitedb = r'\storage\dbsql'+'\\'+dbname
        self.path_run_sql = r'\sql_run'
        self.today = datetime.now()
        self.yesterday = self.today - timedelta(days=1)
        self.dateout = self.yesterday.strftime("%d/%m/%y")

    def remove_special_characters(self, input_string):
        allowed_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_,"
        cleaned_string = ''.join(
            char for char in input_string if char in allowed_chars)
        return cleaned_string

    def import_postgres(self):
        with open(self.current_directory+self.conf_db_postgres, 'r', encoding='utf-8') as json_file:
            conf = json.load(json_file)
        try:
            conn = psycopg2.connect(database=conf['postgres']['database'], user=conf['postgres']['user'],
                                    passw=confconf['postgres']['passw'], host=conf['postgres']['host'], port=conf['postgres']['port'])

            """ Get data from DB sql other to dataframe pandas
                 mode 1 is Creater new table;
                 mode 0 exist table and add data 
            """
            df = """Read Sql from pandas funct"""
            df = df[df['NameFile'].str.contains('LN')].fillna('')
            cursor = conn.cursor()
            # Generate the column
            columns = ", ".join(df.columns)
            columns = self.remove_special_characters(input_string=columns)
            lscolumns = columns.split(',')
            if self.mode == '1':
                query = f"drop table if exists {self.table_name}"
                cursor.execute(query)
                connt.commit()
                create_table = f"create table {self.table_name} ("+",".join([f"{column} TEXT" for column in lscolumns])+"}"
                cursor.execute(create_table)
                connt.commit()
                insert_table = f"INSERT INTO {self.table_name} ({columns}) VALUES ({', '.join(['%s']*len(df.columns))})"
                cursor.executemany(
                    insert_table, df.astype(str).values.tolist())
                conn.commit()
                conn.close()
        except Exception as e:
            field = ['ErrorSqlPostgres', self.dateout,
                     'Fail '+str(e).replace(',', ' ')]
            with open(r'log_down.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(field)

    def import_sqlite_fromfile(self):
        conn = sqlite3.connect(self.current_directory+self.sqlitedb)
        df = pd.read_excel(self.src_file)
        cursor = conn.cursor()
        # Generate the column
        columns = ", ".join(df.columns)
        columns = self.remove_special_characters(input_string=columns)
        lscolumns = columns.split(',')
        try:
            if self.mode == '1':
                query = f"drop table if exists {self.table_name}"
                cursor.execute(query)
                conn.commit()
                create_table = f"create table {self.table_name} ("+",".join([f"{column} TEXT" for column in lscolumns])+")"
                #print(create_table)
                cursor.execute(create_table)
                conn.commit()
                insert_table = f"INSERT INTO {self.table_name} ({columns}) VALUES ({', '.join(['?']*len(df.columns))})"
                #print(insert_table)
                cursor.executemany(
                    insert_table, df.astype(str).values.tolist())
                conn.commit()
                conn.close()
                print('import Sqlite done, ',self.table_name)
            else:
                create_table = f"CREATE TABLE IF NOT EXISTS {self.table_name} ("+",".join([f"{column} TEXT" for column in lscolumns])+")"
                #print(create_table)
                cursor.execute(create_table)
                conn.commit()
                insert_table = f"INSERT INTO {self.table_name} ({columns}) VALUES ({', '.join(['?']*len(df.columns))})"
                cursor.executemany(
                    insert_table, df.astype(str).values.tolist())
                conn.commit()
                conn.close()
        except Exception as e:
            conn.close()
            field = ['ErrorSqlite', self.dateout,
                     'Fail '+str(e).replace(',', ' ')]
            with open(r'log_down.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(field)


    def run_file_sql(self):
        db = sqlite3.connect(self.current_directory+self.sqlitedb)
        try:
            cursor = db.cursor()
            for file in os.listdir(self.current_directory+self.path_run_sql):
                print('SQL FILE RUN ',self.current_directory+self.path_run_sql+'\\'+file)
                with open(self.current_directory+self.path_run_sql+'\\'+file, 'r') as sql_file:
                    sql_script = sql_file.read()
                cursor.executescript(sql_script)
                db.commit()
            db.close()
        except Exception as e:
           db.close()

    def export_for_webchart(self):
        try:
            with open(self.current_directory+'\\config_webchart.json',encoding = 'utf-8') as fjson:
                conf = json.load(fjson)

            src_conn = sqlite3.connect(self.current_directory+conf['src_database'])
            fbydate = psql.read_sql(conf["sql_by_date"], src_conn).fillna('NoneData')
            fbymin = psql.read_sql(conf["sql_by_min"], src_conn).fillna('NoneData')
            src_conn.close()
            #export sqlite for webchart
            dest_conn = sqlite3.connect(self.current_directory+conf['dest_database'])
            table_name = 'Monitor_Date'
            fbydate.columns=['LoanID','Date','Power(Kw/h)','Grid_Power(Kw/h)','Consumption(Kw/h)','BatteryCharge(Kw/h)','BatteryDisCharge(Kw/h)','InverterName','Status','Region','installed_capacity']
            fbydate['Date'] = pd.to_datetime(fbydate['Date'], format='%Y%m%d')
            fbydate['Date']  = fbydate['Date'].dt.strftime('%Y/%m/%d')
            fbydate.to_sql(table_name, dest_conn, if_exists='replace', index=False)
            table_name = 'Monitor_Min'
            fbymin.columns=['LoanID', 'Date','Time','Power(Kw/h)', 'Grid_Power(Kw/h)', 'Consumption(Kw/h)', 'BatteryCharge(Kw/h)', 'BatteryDisCharge(Kw/h)', 'InverterName']
            fbymin['Date'] = pd.to_datetime(fbymin['Date'], format='%Y%m%d')
            fbymin['Date']  = fbymin['Date'].dt.strftime('%Y/%m/%d')
            # Save the DataFrame to the SQLite database
            fbymin.to_sql(table_name, dest_conn, if_exists='replace', index=False)
            dest_conn.close()
            #Remove file Excel in folder export
            for file in os.listdir(self.current_directory+conf['dir_export_perf']):
                os.remove(self.current_directory+conf['dir_export_perf']+'\\'+file)

        except Exception as e:
            src_conn.close()
            dest_conn.close()
            field = ['ErrorExportForWebchart', self.dateout,
                     'Fail '+str(e).replace(',', ' ')]
            with open(r'log_down.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(field)


if __name__ == "__main__":
    #agrs1: src_file(Excel) | args2: functioname | args3: tablename | args4: mode(1 create/0 exist) | args5: dbname
    args = sys.argv
    # parameter func.exe __innit__(self, src_file, functname, table_name, mode)
    #ob_import = ImportDB(src_file=r'template_solar_all.xlsx', functname='import_sqlite_fromfile',table_name='template_solar_all',mode='1', dbname='rawdb.db')
    ob_import = ImportDB(src_file=str(args[1]), table_name=str(args[3]), mode=str(args[4]), dbname=str(args[5]))
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    dateout = yesterday.strftime("%d/%m/%y")
    if str(args[2]) == 'import_sqlite_fromfile':
        ob_import.import_sqlite_fromfile()
    elif str(args[2]) == 'run_file_sql':
        try:
            ob_import.run_file_sql()
        except Exception as e:
            field = ['Error run_file_sql ', dateout,'Fail '+str(e).replace(',', ' ')]
            with open(r'log_down.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(field)
    elif str(args[2]) == 'export_for_webchart':
        ob_import.export_for_webchart()


