import psycopg2,json,sys
from datetime import datetime
import pandas as pd
import pandas.io.sql as psql
import sqlite3


try:
    argument = sys.argv
    print("#export data from sql to excel")
    with open(argument[1]+'\\sqlconf.json',encoding = 'utf-8') as fjson:
        conf = json.load(fjson)
    conn = psycopg2.connect(database= conf["database"],user= conf["user"],password= conf["password"],
                            host= conf["host"],port= conf["port"])

    fbydate = psql.read_sql(conf["sql_by_date"], conn)
    fbymin = psql.read_sql(conf["sql_by_min"], conn)
    conn.close()

    conn = sqlite3.connect(argument[1]+'\\data_chart.db')
    fbydate.columns=['LoanID','Date','Power(Kw/h)','Grid_Power(Kw/h)','Consumption(Kw/h)','BatteryCharge(Kw/h)','BatteryDisCharge(Kw/h)','InverterName','Status','Region','installed_capacity']
    table_name = 'Monitor_Date'
    fbydate['Date'] = pd.to_datetime(fbydate['Date'], format='%Y%m%d')
    fbydate['Date']  = fbydate['Date'].dt.strftime('%Y/%m/%d')
    # Save the DataFrame to the SQLite database
    fbydate.to_sql(table_name, conn, if_exists='replace', index=False)

    fbymin.columns=['LoanID', 'Date','Time','Power(Kw/h)', 'Grid_Power(Kw/h)', 'Consumption(Kw/h)', 'BatteryCharge(Kw/h)', 'BatteryDisCharge(Kw/h)', 'InverterName']
    table_name = 'Monitor_Min'
    fbymin['Date'] = pd.to_datetime(fbymin['Date'], format='%Y%m%d')
    fbymin['Date']  = fbymin['Date'].dt.strftime('%Y/%m/%d')
    # Save the DataFrame to the SQLite database
    fbymin.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()

except Exception as err:
    #get current time
    now = datetime.now()
    date_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
    with open(argument[1]+"\\log_getvardb.txt","a",encoding="utf-8") as wlog:
        wlog.write("["+date_time_str+"] "+str(err))
        wlog.write("\n")
        wlog.write("\n")
        
        
