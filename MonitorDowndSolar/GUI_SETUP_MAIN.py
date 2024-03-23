import json 
import threading
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import requests
import os
import csv
from datetime import datetime, timedelta
import schedule
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import shutil
import smtplib
import subprocess
import sqlite3


class SendMail:
    def __init__(self, SERVER, PORT, USER, PASS, SUBJECT, FROM, TO, TEXT):
        self.SERVER = SERVER
        self.PORT = PORT
        self.USER = USER
        self.PASS = PASS
        self.SUBJECT = SUBJECT
        self.FROM = FROM
        self.TO = TO
        self.TEXT = TEXT
        
    def transport(self):
        msg = MIMEMultipart('alternative')
        msg['Subject'] = self.SUBJECT
        msg['From'] = self.FROM
        msg['To'] = ";".join(self.TO)
        html = """\
        <html xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:w="urn:schemas-microsoft-com:office:word" xmlns:x="urn:schemas-microsoft-com:office:excel" xmlns:m="http://schemas.microsoft.com/office/2004/12/omml" xmlns="http://www.w3.org/TR/REC-html40"><head><meta name=Generator content="Microsoft Word 15 (filtered medium)"><!--[if !mso]><style>v\:* {behavior:url(#default#VML);}
        o\\:* {behavior:url(#default#VML);}
        w\\:* {behavior:url(#default#VML);}
        .shape {behavior:url(#default#VML);}
        </style><![endif]--><style><!--
        /* Font Definitions */
        @font-face
            {font-family:"Cambria Math";
            panose-1:2 4 5 3 5 4 6 3 2 4;}
        @font-face
            {font-family:Calibri;
            panose-1:2 15 5 2 2 2 4 3 2 4;}
        /* Style Definitions */
        p.MsoNormal, li.MsoNormal, div.MsoNormal
            {margin:0in;
            font-size:11.0pt;
            font-family:"Calibri",sans-serif;}
        span.EmailStyle17
            {mso-style-type:personal-compose;
            font-family:"Calibri",sans-serif;
            color:windowtext;}
        .MsoChpDefault
            {mso-style-type:export-only;
            font-family:"Calibri",sans-serif;}
        @page WordSection1
            {size:8.5in 11.0in;
            margin:1.0in 1.0in 1.0in 1.0in;}
        div.WordSection1
            {page:WordSection1;}
        --></style><!--[if gte mso 9]><xml>
        <o:shapedefaults v:ext="edit" spidmax="1026" />
        </xml><![endif]--><!--[if gte mso 9]><xml>
        <o:shapelayout v:ext="edit">
        <o:idmap v:ext="edit" data="1" />
        </o:shapelayout></xml><![endif]--></head><body lang=EN-US link="#0563C1" vlink="#954F72" style='word-wrap:break-word'><div class=WordSection1><p class=MsoNormal> Dear All, <o:p></o:p></p>&nbsp;<p class=MsoNormal> %s <o:p></o:p></p><p class=MsoNormal><o:p>&nbsp;</o:p></p><p class=MsoNormal><span style='font-family:"Times New Roman",serif'>Many thanks and best regards,<o:p></o:p></span></p><p class=MsoNormal><b><span style='font-family:"Times New Roman",serif'>MIS</span></b><b><span lang=VI style='font-family:"Times New Roman",serif'> Team<o:p></o:p></span></b></p><p class=MsoNormal><span style='font-family:"Times New Roman",serif'>Collections Systems and MIS Analyst<o:p></o:p></span></p><p class=MsoNormal><span style='font-size:12.0pt;font-family:"Times New Roman",serif'>US Business Services (USBS)</span><b><span style='font-family:"Times New Roman",serif;color:#2F5496'><o:p></o:p></span></b></p><p class=MsoNormal><span lang=VI></span><o:p></o:p></p><p class=MsoNormal><o:p>&nbsp;</o:p></p></div></body></html>
        """ % (self.TEXT)
        part = MIMEText(html,'html')
        msg.attach(part)
        #setting server
        try:
            mailSmtp = smtplib.SMTP(self.SERVER,self.PORT)
        except Exception as e:
            print(e)
        mailSmtp.ehlo()
        mailSmtp.starttls()
        mailSmtp.login(self.USER,self.PASS)
        mailSmtp.sendmail(self.FROM,self.TO,msg.as_string())
        mailSmtp.quit()

flagprocess = 0
def executeProgram(user,passmail):
    global flagprocess
    flagprocess = 1
    try:
        curpatch = str(os.getcwd())
        print("Task executed at:", time.strftime("%Y-%m-%d %H:%M:%S"))
        subprocess.Popen(r'py controller.py', cwd=curpatch).wait()
        time.sleep(4)
        print("Done controller")
        with open(curpatch+'\\configSendMail.json','r',encoding="utf-8") as json_file:
            configData = json.load(json_file)
        today = datetime.now()
        # Subtract one day to get yesterday's date
        yesterday = today - timedelta(days=1)
        dateout = yesterday.strftime("%Y%m%d")
        conn = sqlite3.connect(curpatch+configData["dblog"])
        query = "select LOAN,DATE,STATUS_DOWN from status_down where STATUS_DOWN in ('Fail','Redownload') and DATE = '"+dateout+"';"
        df = pd.read_sql_query(query, conn)
        lsError = ['Name - RunForDate - Result']
        for index, row in df.iterrows():
            lsError.append('\n '+' - '.join(row))
        
        if len(lsError) > 1:
            TEXT = "---------------- Result Download MonitorSolar ---------------------------<br><br>"+"\n <br>".join(lsError)
            objMail = SendMail(configData["SERVER"],configData["PORT"],user,passmail,configData["SUBJECT"],user[3:]+configData["FROM"],configData["TO"],TEXT)
            objMail.transport()
        else:
            TEXT = "---------------- Result Download MonitorSolar ---------------------------<br><br>"+"\n <br> Not Error Case Fail Download."
            objMail = SendMail(configData["SERVER"],configData["PORT"],user,passmail,configData["SUBJECT"],user[3:]+configData["FROM"],configData["TO"],TEXT)
            objMail.transport()
    except Exception as e:
        print('Error system GUI SETUP - Func executeProgram',e)
        flagprocess = 0

def schedule_task():
    global flagprocess
    user = username.get()
    passmail = passw.get()
    settimer = timer.get()
    print('timer: ',settimer)
    schedule.every().day.at(str(settimer)).do(executeProgram,user,passmail)
    # Run the scheduled tasks
    flagprocess = 1
    while True:
        schedule.run_pending()
        time.sleep(1)

def threading_main():
    if flagprocess == 0:
        user = username.get()
        passmail = passw.get()
        settimer = timer.get()
        if user == '' or passmail == '' or settimer == '':
            messagebox.showwarning("warning", "Info not type null")
        else:
            #print(user,passmail,settimer)
            print('exec threading')
            th = threading.Thread(target=schedule_task)
            th.start()
    else:
        print("Program are working!")
        messagebox.showwarning("warning", "Program are working!")




#window
tkWindow = Tk()
tkWindow.geometry('300x100')
tkWindow.title('Setup')
tkWindow.resizable(False, False)
# apply the grid layout

lbusername = Label(tkWindow,text="email: ").grid(row=1,column=0)
username = StringVar()
usernameString = Entry(tkWindow,textvariable=username,width=30).grid(row=1,column=1)
#pass
lbpassw = Label(tkWindow,text="Password email: ").grid(row=2,column=0)
passw = StringVar()
passwString = Entry(tkWindow,textvariable=passw,width=30,show="*").grid(row=2,column=1)
#timer
lbtimer = Label(tkWindow,text="Timer for run: ").grid(row=3,column=0)
timer = StringVar()
timerString = Entry(tkWindow,textvariable=timer,width=30).grid(row=3,column=1)
#submit
btnEncrypt = Button(tkWindow,text="Start",command = threading_main).grid(row=4,column=1)
tkWindow.mainloop()

