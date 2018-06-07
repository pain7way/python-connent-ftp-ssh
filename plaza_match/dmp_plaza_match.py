# -*- coding: utf-8 -*-
import os
import datetime
import paramiko
import time
from time import strftime

def ls(path):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname='ip地址', 
                port='端口', 
                username='用户名', 
                password='密码')    
    stdin, stdout, stderr = ssh.exec_command('ls '+path)
    b = stdout.read()
    a = bytes.decode(b)
    a = a.split('\n')
    a = a[0:-1]
    ssh.close()
    return a

def scp_download(path):
    transport = paramiko.Transport(('10.199.207.5', 22))
    transport.connect(username='jqr', password='Jqr@123' )
    sftp = paramiko.SFTPClient.from_transport(transport)
    ll = ls('PLAZA/'+path)
    for n in ll:
        sftp.get(remotepath='/hdfsftp/DM/JQR/PLAZA/'+path+'/'+n, 
                 localpath='/home/appuser/plaza_match/gc/'+n)

def scp_upload(path):
    transport = paramiko.Transport(('10.199.207.5', 22))
    transport.connect(username='jqr', password='Jqr@123' )
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.put(localpath='/home/appuser/plaza_match/Plaza_Match.csv', 
             remotepath='/hdfsftp/DM/JQR/PLAZA/'+path+'/Plaza_Match.csv')

while True:
    a = ls('PLAZA/')
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days = 1)
    yesterday = yesterday.strftime('%Y%m%d') 
    if yesterday in a:
        l = ls('PLAZA/'+yesterday)
        if ('Plaza_Match.csv' not in l) & (len(l)==8):
            print '\n'+strftime("%Y-%m-%d %H:%M:%S"), 'download starting...'
            scp_download(yesterday)
            print('download complete, start model')
            os.system('python /home/appuser/plaza_match/plaza_match.py')
            print('model complete,upload starting...')
            scp_upload(yesterday)
            print strftime("%Y-%m-%d %H:%M:%S"), 'upload complete\n'
        else:
            time.sleep(600)
    else:
        time.sleep(3600)

