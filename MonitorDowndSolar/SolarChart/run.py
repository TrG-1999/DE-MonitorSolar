from flask import render_template, url_for
from flask import redirect
from flask import request
from flask import send_from_directory
import pandas as pd
import json
import plotly
import plotly.express as px
import plotly.graph_objects as go
import os
from flask import Flask
import sys
import sqlite3
from datetime import datetime, timedelta


if getattr(sys,'frozen',False):
    template_folder = os.path.join(sys.executable,'..','templates')
    static_folder = os.path.join(sys.executable,'..','static')
    app = Flask(__name__,template_folder=template_folder,static_folder=static_folder)
else:
    app = Flask(__name__)

lsloanf1 = None
lsdatef1 = None
inverter1 = None
status1 = None
region1 = None
lsloanf2 = None
lsdatef2 = None
inverter2 = None

def format_as_percentage(number):
    return f'{number:.2%}'

def get_json_barchar(df,title="Chart by date"):
    fig1= go.Figure()
    # Add a bar trace for each column
    fig1.add_trace(go.Bar(x=df['Date'], y=df['Consumption(kW/h)'], name='Consumption(kW/h)', marker_color='blue',hovertemplate='Date: %{x}<br>Value: %{y}'))
    fig1.add_trace(go.Bar(x=df['Date'], y=df['Power(kW/h)'], name='Power(kW/h)', marker_color='green',hovertemplate='Date: %{x}<br>Value: %{y}'))
    fig1.add_trace(go.Bar(x=df['Date'], y=df['Grid power(kW/h)'], name='Grid power(kW/h)', marker_color='#Ffd400',hovertemplate='Date: %{x}<br>Value: %{y}'))
    fig1.add_trace(go.Bar(x=df['Date'], y=df['BatteryDisCharge(kW/h)'], name='BatteryDisCharge(kW/h)', marker_color='red',hovertemplate='Date: %{x}<br>Value: %{y}'))
    # fig1 = px.bar(df,x="Date", y = ['Power(Kw/h)', 'Consumption(Kw/h)','Grid Power(Kw/h)'])
    #list_names = df['loanid'].unique()
    # dropdown_menu = [{'label': name, 'method': 'update', 'args': [{'visible': [name == lsname for lsname in list_names]}]} for name in list_names]
    fig1.update_layout(
        # template='seaborn',
        title=title,
        xaxis_title="Date",
        yaxis_title="kW/h",
        xaxis_rangeslider_visible=True,
        barmode='group',
        hoverlabel=dict(
        font=dict(size=14),  # Increase hover label font size
        align='left',  # Adjust alignment to the left
        ),
    )
    graphBarDate = json.dumps(fig1, cls = plotly.utils.PlotlyJSONEncoder)
    return graphBarDate

def get_json_table(df):
    df['AvgPerformance%'] = df['AvgPerformance%'].fillna(0)
    highlight_condition = df['AvgPerformance%'] < 0.5
    df['AvgPerformance%'] = df['AvgPerformance%'].apply(format_as_percentage)
    highlight_color = [['yellow' if cond else 'white' for cond in highlight_condition]*len(df)]
    # Create a Plotly table
    fig = go.Figure(data=[go.Table(
        header=dict(values=["invertername", "loanid","Sum of power(kw/h)","Target (KW/h)","AvgPerformance%"],line_color='darkslategray'),
        cells=dict(values=[df['invertername'], df['loanid'], df['Sum of power(kw/h)'],df['Target (KW/h)'],df['AvgPerformance%']],line_color='darkslategray',
                fill=dict(color=highlight_color))
        )],
        layout=go.Layout(title="Target/Performance As of date (Total Loan: "+str(len(df['loanid']))+")",height=800))

    # Export the figure to JSON using PlotlyJSONEncoder
    figtable_json = json.dumps(fig, cls = plotly.utils.PlotlyJSONEncoder)
    return figtable_json

def get_json_linechar(df,title="Chart by Time - ",xaxis_title="Time of date: "):
    fig3= go.Figure()
    # Add a bar trace for each column
    # fig3.add_trace(go.Scatter(x=df['Time'], y=df['Consumption(Kw/h)'], name='Consumption(Kw/h)', marker_color='blue',
    #     text = ['Consumption(Kw/h)']*len(df),hovertemplate='Time: %{x}<br>Value: %{y}<br>%{text}',mode='lines'))
    # fig3.add_trace(go.Scatter(x=df['Time'], y=df['Power(Kw/h)'], name='Power(Kw/h)', marker_color='green',
    #     text = ['Consumption(Kw/h)']*len(df),hovertemplate='Time: %{x}<br>Value: %{y}<br>%{text}',mode='lines'))
    # fig3.add_trace(go.Scatter(x=df['Time'], y=df['Grid Power(Kw/h)'], name='Grid Power(Kw/h)', marker_color='red',
    #     text = ['Consumption(Kw/h)']*len(df),hovertemplate='Time: %{x}<br>Value: %{y}<br>%{text}',mode='lines'))
    fig3.add_trace(go.Scatter(x=df['Time'], y=df['Consumption(kW/h)'], name='Consumption(kW/h)', marker_color='blue',
        hovertemplate='Time: %{x}<br>Value: %{y}',mode='lines'))
    fig3.add_trace(go.Scatter(x=df['Time'], y=df['Power(kW/h)'], name='Power(kW/h)', marker_color='green',
        hovertemplate='Time: %{x}<br>Value: %{y}',mode='lines'))
    fig3.add_trace(go.Scatter(x=df['Time'], y=df['Grid power(kW/h)'], name='Grid power(kW/h)', marker_color='#Ffd400',
        hovertemplate='Time: %{x}<br>Value: %{y}',mode='lines'))
    fig3.add_trace(go.Scatter(x=df['Time'], y=df['BatteryDisCharge(kW/h)'], name='BatteryDisCharge(kW/h)', marker_color='red',
        hovertemplate='Time: %{x}<br>Value: %{y}',mode='lines'))
    # dropdown_menu = [{'label': name, 'method': 'update', 'args': [{'visible': [name == lsname for lsname in list_names]}]} for name in list_names]    
    fig3.update_layout(
        # template='seaborn',
        title=title,
        xaxis_title=xaxis_title,
        yaxis_title="kW/h",
        xaxis_rangeslider_visible=True,
        barmode='group',
        hoverlabel=dict(
        font=dict(size=14),  # Increase hover label font size
        align='left',  # Adjust alignment to the left
        ),
    )
    graphLinesMin = json.dumps(fig3, cls = plotly.utils.PlotlyJSONEncoder)
    return graphLinesMin

def get_query_for_line(conn,fil_line):
    if fil_line['date'] == '%' and fil_line['loanid'] == '%' and fil_line['inverter'] != '%':
        query = '''SELECT a.LoanID,a.invertername,a.Date,a.Time,round(sum("power(kw/h)"),2) as "Power(kW/h)",round(sum("grid_power(kw/h)"),2) as "Grid power(kW/h)"
        ,round(sum("consumption(kw/h)"),2) as "Consumption(kW/h)",
        round(sum("batterydischarge(kw/h)"),2) as "BatteryDisCharge(kW/h)"
        FROM Monitor_Min a
        WHERE  a.invertername like "'''+fil_line['inverter']+'" group By a.LoanID,a.invertername,a.Date,a.Time order by a.Time asc'
    elif fil_line['date'] == '%' and fil_line['loanid'] == '%':
        cursor = conn.cursor()
        cursor.execute('SELECT  LoanID,Date FROM Monitor_Min order by LoanID,date desc LIMIT 1')
        dateofchart = cursor.fetchall()
        cursor.close()
        fil_line['loanid'] = dateofchart[0][0]
        fil_line['date'] = dateofchart[0][1]
        fil_line['inverter'] = '%'
        query = '''SELECT a.LoanID,a.invertername,a.Date,a.Time,round(sum("power(kw/h)"),2) as "Power(kW/h)",round(sum("grid_power(kw/h)"),2) as "Grid power(kW/h)"
        ,round(sum("consumption(kw/h)"),2) as "Consumption(kW/h)",
        round(sum("batterydischarge(kw/h)"),2) as "BatteryDisCharge(kW/h)"
        FROM Monitor_Min a
        WHERE a.LoanID = "'''+fil_line['loanid']+'"and a.Date = "'+fil_line['date']+'" group By a.LoanID,a.invertername,a.Date,a.Time'
    elif fil_line['loanid'] == '%':
        query = '''SELECT a.invertername,a.Date,a.Time,round(sum("power(kw/h)"),2) as "Power(kW/h)",round(sum("grid_power(kw/h)"),2) as "Grid power(kW/h)"
        ,round(sum("consumption(kw/h)"),2) as "Consumption(kW/h)",
        round(sum("batterydischarge(kw/h)"),2) as "BatteryDisCharge(kW/h)"
        FROM Monitor_Min a
        WHERE  a.Date like "'''+fil_line['date']+'" and invertername like "'+fil_line['inverter']+'" group By a.invertername,a.Date,a.Time order by a.Time asc'
    else:
        query = '''SELECT a.LoanID,a.invertername,a.Date,a.Time,round(sum("power(kw/h)"),2) as "Power(kW/h)",round(sum("grid_power(kw/h)"),2) as "Grid power(kW/h)"
        ,round(sum("consumption(kw/h)"),2) as "Consumption(kW/h)",
        round(sum("batterydischarge(kw/h)"),2) as "BatteryDisCharge(kW/h)"
        FROM Monitor_Min a
        WHERE a.LoanID like "'''+fil_line['loanid']+'"and a.Date like "'+fil_line['date']+'" and invertername like "'+fil_line['inverter']+'" group By a.LoanID,a.invertername,a.Date,a.Time'
    return query

def get_query_for_bar(fil_bar):
    query = r'''SELECT Date,round(sum("power(kw/h)"),2) as "Power(kW/h)",
    round(sum("grid_power(kw/h)"),2) as "Grid power(kW/h)" ,
    round(sum("consumption(kw/h)"),2) as "Consumption(kW/h)",
    round(sum("batterydischarge(kw/h)"),2) as "BatteryDisCharge(kW/h)"  
    FROM Monitor_Date '''+'WHERE loanid like "'+fil_bar['loanid']+'" and Date like "'+fil_bar['date']+'" and invertername like "'+fil_bar['inverter']+'" and region like "'+fil_bar['region']+'" group By Date'
    return query

def get_query_for_table():
    query = r'''SELECT invertername,loanid,round(sum("power(kw/h)"),2) as "Sum of power(kw/h)",round(sum("Target"),2) as "Target (KW/h)",
        round(avg(Performance),4) as "AvgPerformance%"
        from (SELECT invertername,date,loanid,sum("power(kw/h)") as "power(kw/h)" ,sum("installed_capacity"*3.5) as "Target",
        (sum("power(kw/h)")/sum("installed_capacity"*3.5)) as Performance
        FROM Monitor_Date   
        GROUP by invertername,date,loanid )
        GROUP by invertername,loanid ORDER by "AvgPerformance%" ASC'''
    return query

def get_query_fail_case():
    query = r'''SELECT Domain,LoanID,Date,Status_down 
    FROM Statusdown 
    WHERE  substr(Date,1,7) = strftime('%Y/%m', DATE('now', '-1 day'), 'localtime') order by Date DESC'''

    return query


@app.route("/")
def index():
    global lsloanf1
    global lsdatef1
    global inverter1
    global status1
    global region1
    global lsloanf2
    global lsdatef2
    global inverter2
    curpatch = str(os.getcwd())
    #graph Bar
    conn = sqlite3.connect(curpatch+'\\tool\\data_chart.db')
    query = r'''SELECT Date,round(sum("power(kw/h)"),2) as "Power(kW/h)",
    round(sum("grid_power(kw/h)"),2) as "Grid power(kW/h)" ,
    round(sum("consumption(kw/h)"),2) as "Consumption(kW/h)",
    round(sum("batterydischarge(kw/h)"),2) as "BatteryDisCharge(kW/h)"  
    FROM Monitor_Date group By Date'''
    df = pd.read_sql_query(query, conn)
    dfdate = pd.read_sql_query('select LoanID,Date,InverterName,Status,Region from Monitor_Date order by LoanID,Date Desc', conn)
    conn.close()
    #'LoanID','Date','Power(Kw/h),'Grid Power(Kw/h)','Consumption(Kw/h)','BatteryCharge(Kw/h)','BatteryDisCharge(Kw/h)','InverterName','Status','Region','installed_capacity'
    #df.columns=['loanid', 'Date', 'Power(Kw/h)', 'Grid Power(Kw/h)', 'Consumption(Kw/h)', 'BatteryCharge(Kw/h)', 'BatteryDisCharge(Kw/h)', 'InverterName', 'Status', 'Region', 'installed_capacity']
    # df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d')
    # df['Date']    =df['Date'].dt.strftime('%Y/%m/%d')
    df.sort_values("Date",inplace=True)
    lsloanf1 = dfdate['LoanID'].unique()
    lsdatef1 = dfdate['Date'].unique()
    inverter1 = dfdate['InverterName'].unique()
    status1 = dfdate['Status'].unique()
    region1 = dfdate['Region'].unique()
    #filter
    #df = df[df['LoanID']=='LN000001']
    graphBarDate = get_json_barchar(df,title="Chart by date")

    #Graph Lines
    conn = sqlite3.connect(curpatch+'\\tool\\data_chart.db')
    # df["Date"] =  pd.to_datetime(df["Date"], format="%Y/%m/%d")
    # df = pd.read_excel(curpatch+"\\data\\sql_by_min.xlsx")
    # df.columns=['loanid', 'Date','Time','Power(Kw/h)', 'Grid Power(Kw/h)', 'Consumption(Kw/h)', 'BatteryCharge(Kw/h)', 'BatteryDisCharge(Kw/h)', 'InverterName']
    # df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d')
    # df['Date']    =df['Date'].dt.strftime('%Y/%m/%d')
    # df.sort_values("Time",inplace=True)
    # lsloanf3 = df['loanid'].unique()
    # df = df[(df['loanid']=='LN000001') & (df['Date']=='2023/09/10')]
    cursor = conn.cursor()
    cursor.execute('SELECT  LoanID,Date FROM Monitor_Min order by LoanID,date desc LIMIT 1')
    dateofchart = cursor.fetchall()
    cursor.close()
    query = '''SELECT a.LoanID,a.invertername,a.Date,a.Time,round(sum("power(kw/h)"),2) as "Power(kW/h)",round(sum("grid_power(kw/h)"),2) as "Grid power(kW/h)"
    ,round(sum("consumption(kw/h)"),2) as "Consumption(kW/h)",
    round(sum("batterydischarge(kw/h)"),2) as "BatteryDisCharge(kW/h)"
    FROM Monitor_Min a
    WHERE a.LoanID = "'''+dateofchart[0][0]+'"and a.Date = "'+dateofchart[0][1]+'" group By a.Date,a.Time,a.LoanID,a.invertername'
    df = pd.read_sql_query(query, conn)
    dfdate = pd.read_sql_query('select LoanID,Date,InverterName from Monitor_Min order by LoanID,Date Desc', conn)
    lsloanf2 = dfdate['LoanID'].unique()
    lsdatef2 = dfdate['Date'].unique()
    inverter2 = dfdate['InverterName'].unique()
    conn.close()
    graphLinesMin = get_json_linechar(df,title="Chart by Time - "+dateofchart[0][0],xaxis_title="Time of date: "+dateofchart[0][1])

    #add table perfomance/target
    conn = sqlite3.connect(curpatch+'\\tool\\data_chart.db')
    query = get_query_for_table()
    df = pd.read_sql_query(query, conn)
    conn.close()
    figtable_json = get_json_table(df)

    return render_template("index.html", title = "Home",graphBarDate = graphBarDate,graphLinesMin=graphLinesMin,lsloanf1=lsloanf1,lsdatef1=lsdatef1,
        inverter1=inverter1,region1=region1,lsloanf2=lsloanf2,inverter2=inverter2,lsdatef2=lsdatef2,figtable_json=figtable_json)

@app.route("/filter_bar",methods=['POST'])
def filter_bar():
    global lsloanf1
    global lsdatef1
    global inverter1
    global status1
    global region1
    global lsloanf2
    global lsdatef2
    global inverter2
    curpatch = str(os.getcwd())
    fil_bar = {'loanid': '','date': '','inverter': '','region': ''}
    fil_bar['loanid'] = request.form.get('loanid1','')
    fil_bar['date'] = request.form.get('dateid1','')
    fil_bar['inverter'] = request.form.get('inverter1','')
    fil_bar['region'] = request.form.get('region1','')
    print(fil_bar)
    fil_line = {'loanid': '','date': '','inverter': ''}
    fil_line['loanid'] = request.form.get('filloanid2','')
    fil_line['date'] = request.form.get('fildate2','')
    fil_line['inverter'] = request.form.get('filinverter2','')

    if fil_bar['loanid'] == '' or fil_bar['loanid'] == 'All':
        fil_bar['loanid'] = '%'
    if fil_bar['date'] == '' or fil_bar['date'] == 'All':
        fil_bar['date'] = '%'
    if fil_bar['inverter'] == '' or fil_bar['inverter'] == 'All':
        fil_bar['inverter'] = '%'
    if fil_bar['region'] == '' or fil_bar['region'] == 'All':
        fil_bar['region'] = '%'
    #graph Bar
    conn = sqlite3.connect(curpatch+'\\tool\\data_chart.db')

    query = get_query_for_bar(fil_bar)

    df = pd.read_sql_query(query, conn)
    conn.close()

    graphBarDate = get_json_barchar(df,title="Chart by date - Filter: "+fil_bar['loanid'].replace('%','')+' '+fil_bar['inverter'].replace('%','')+' '+fil_bar['region'].replace('%','')+' '+fil_bar['date'].replace('%',''))

    #fil_line = {'loanid': '','date': '','inverter': ''}
    #Graph Lines
    conn = sqlite3.connect(curpatch+'\\tool\\data_chart.db')

    if fil_line['loanid'] == '' or fil_line['loanid'] == 'All':
        fil_line['loanid'] = '%'
    if fil_line['date'] == '' or fil_line['date'] == 'All':
        fil_line['date'] = '%'
    if fil_line['inverter'] == '' or fil_line['inverter'] == 'All':
        fil_line['inverter'] = '%'

    query =    get_query_for_line(conn,fil_line)

    df = pd.read_sql_query(query, conn)
    conn.close()

    graphLinesMin = get_json_linechar(df,title="Chart by Time - Filter: "+fil_line['loanid'].replace('%','')+' '+fil_line['inverter'].replace('%',''),xaxis_title="Time of date: "+fil_line['date'].replace('%',''))

    fil_line['loanid'] = fil_line['loanid'].replace('%','')
    fil_line['date'] = fil_line['date'].replace('%','')
    fil_line['inverter'] = fil_line['inverter'].replace('%','')
    fil_bar['loanid'] = fil_bar['loanid'].replace('%','')
    fil_bar['date'] = fil_bar['date'].replace('%','')
    fil_bar['inverter'] = fil_bar['inverter'].replace('%','')
    fil_bar['region'] = fil_bar['region'].replace('%','')

    #add table perfomance/target
    conn = sqlite3.connect(curpatch+'\\tool\\data_chart.db')
    query = get_query_for_table()
    df = pd.read_sql_query(query, conn)
    conn.close()
    figtable_json = get_json_table(df)

    return render_template("filterpage.html", title = "Filter",graphBarDate = graphBarDate,graphLinesMin=graphLinesMin,lsloanf1=lsloanf1,lsdatef1=lsdatef1,
        inverter1=inverter1,region1=region1,lsloanf2=lsloanf2,inverter2=inverter2,lsdatef2=lsdatef2,fil_line=fil_line,fil_bar=fil_bar,figtable_json=figtable_json)

@app.route("/filter_line",methods=['POST'])
def filter_line():
    global lsloanf1
    global lsdatef1
    global inverter1
    global status1
    global region1
    global lsloanf2
    global lsdatef2
    global inverter2
    curpatch = str(os.getcwd())
    fil_bar = {'loanid': '','date': '','inverter': '','region': ''}
    fil_bar['loanid'] = request.form.get('filloanid1','')
    fil_bar['date'] = request.form.get('fildate1','')
    fil_bar['inverter'] = request.form.get('filinverter1','')
    fil_bar['region'] = request.form.get('filregion1','')

    fil_line = {'loanid': '','date': '','inverter': ''}
    fil_line['loanid'] = request.form.get('lsloanf2','')
    fil_line['date'] = request.form.get('lsdatef2','')
    fil_line['inverter'] = request.form.get('inverter2','')

    if fil_bar['loanid'] == '' or fil_bar['loanid'] == 'All':
        fil_bar['loanid'] = '%'
    if fil_bar['date'] == '' or fil_bar['date'] == 'All':
        fil_bar['date'] = '%'
    if fil_bar['inverter'] == '' or fil_bar['inverter'] == 'All':
        fil_bar['inverter'] = '%'
    if fil_bar['region'] == '' or fil_bar['region'] == 'All':
        fil_bar['region'] = '%'
    #graph Bar
    conn = sqlite3.connect(curpatch+'\\tool\\data_chart.db')

    query = get_query_for_bar(fil_bar)

    df = pd.read_sql_query(query, conn)
    conn.close()

    graphBarDate = get_json_barchar(df,title="Chart by date - Filter: "+fil_bar['loanid'].replace('%','')+' '+fil_bar['inverter'].replace('%','')+' '+fil_bar['region'].replace('%','')+' '+fil_bar['date'].replace('%',''))

    #fil_line = {'loanid': '','date': '','inverter': ''}
    #Graph Lines
    conn = sqlite3.connect(curpatch+'\\tool\\data_chart.db')

    if fil_line['loanid'] == '' or fil_line['loanid'] == 'All':
        fil_line['loanid'] = '%'
    if fil_line['date'] == '' or fil_line['date'] == 'All':
        fil_line['date'] = '%'
    if fil_line['inverter'] == '' or fil_line['inverter'] == 'All':
        fil_line['inverter'] = '%'

    query =    get_query_for_line(conn,fil_line)

    df = pd.read_sql_query(query, conn)
    conn.close()

    graphLinesMin = get_json_linechar(df,title="Chart by Time - Filter: "+fil_line['loanid'].replace('%','')+' '+fil_line['inverter'].replace('%',''),xaxis_title=fil_line['date'].replace('%',''))

    fil_line['loanid'] = fil_line['loanid'].replace('%','')
    fil_line['date'] = fil_line['date'].replace('%','')
    fil_line['inverter'] = fil_line['inverter'].replace('%','')
    fil_bar['loanid'] = fil_bar['loanid'].replace('%','')
    fil_bar['date'] = fil_bar['date'].replace('%','')
    fil_bar['inverter'] = fil_bar['inverter'].replace('%','')
    fil_bar['region'] = fil_bar['region'].replace('%','')

    #add table perfomance/target
    conn = sqlite3.connect(curpatch+'\\tool\\data_chart.db')
    query = get_query_for_table()
    df = pd.read_sql_query(query, conn)
    conn.close()
    figtable_json = get_json_table(df)

    return render_template("filterpage.html", title = "Filter",graphBarDate = graphBarDate,graphLinesMin=graphLinesMin,lsloanf1=lsloanf1,lsdatef1=lsdatef1,
        inverter1=inverter1,region1=region1,lsloanf2=lsloanf2,inverter2=inverter2,lsdatef2=lsdatef2,fil_line=fil_line,fil_bar=fil_bar,figtable_json=figtable_json)

@app.route("/Downloads_target",methods=['POST','GET'])
def downloads_target():
    folderexport = '\\tool\\ExportTarget'
    curpatch = str(os.getcwd())
    conn = sqlite3.connect(curpatch+'\\tool\\data_chart.db')
    query = get_query_for_table()
    df = pd.read_sql_query(query, conn)
    conn.close()
    today = datetime.now()
    dateout = today.strftime("%d%m%y%H%M%S")
    direct = curpatch+folderexport
    filesave = 'Export_Targe_Perf_'+dateout+'.xlsx'
    df.to_excel(direct+'\\'+filesave, index=False)

    return send_from_directory(direct,filesave)

@app.route("/Downloads_fails",methods=['POST','GET'])
def Downloads_fails():
    folderexport = '\\tool\\ExportTarget'
    curpatch = str(os.getcwd())
    conn = sqlite3.connect(curpatch+'\\tool\\data_chart.db')
    query = get_query_fail_case()
    df = pd.read_sql_query(query, conn)
    conn.close()
    today = datetime.now()
    timeout = today.strftime("%H%M%S")
    dateout = today.strftime("%m%Y")
    direct = curpatch+folderexport
    filesave = 'Export_FailCase_'+dateout+'_'+timeout+'.xlsx'
    df.to_excel(direct+'\\'+filesave, index=False)

    return send_from_directory(direct,filesave)

if __name__ == "__main__":
    # app.run(debug=True)
    app.run(debug=False,port=5000,host="0.0.0.0")

