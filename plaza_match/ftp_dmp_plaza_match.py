# -*- coding: utf-8 -*-
# python2.7
from ftplib import FTP
import ftplib
import os
import datetime
import time
from time import strftime

class Fuzzy_Match(object):
    def __init__(self):
        self.ip = 'ip地址'
        self.port = '端口'
        self.user = '用户名'
        self.password = '密码'
        self.bufsize = 1024
        self.ftp = FTP()

    def ftp_connect(self):
        try:
            self.ftp.connect(self.ip, self.port)
            self.ftp.login(self.user,self.password)
            self.ftp.encoding = 'utf8'
        except ftplib.error_perm:
            self.ftp_connect()

    def ls(self, path):
        self.ftp.cwd(path)
        ll = self.ftp.nlst()
        self.ftp.cwd('/')
        return ll

    def ftp_download(self, path):
        self.ftp.cwd('/PLAZA/'+path)
        l = self.ftp.nlst()       
        for i in l:
            file_handle = open('/home/appuser/plaza_match/gc/'+i,"wb")
            self.ftp.retrbinary('RETR '+i, file_handle.write, self.bufsize)
            file_handle.close()
        self.ftp.cwd('/')

    def ftp_upload(self,path):
        self.ftp.cwd('/PLAZA/')
        file_handle = open('/home/appuser/plaza_match/Plaza_Match.csv',"rb")
        self.ftp.storbinary('STOR '+'Plaza_Match_'+path+'.csv', file_handle, self.bufsize)
        file_handle.close()

if __name__ == '__main__':
    while True:
        fm = Fuzzy_Match()
        fm.ftp_connect()
        a = fm.ls('/PLAZA/')
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days = 1)
        yesterday = yesterday.strftime('%Y%m%d') 
        if yesterday in a:
            l = fm.ls('/PLAZA/'+yesterday)
            if ('Plaza_Match_'+yesterday+'.csv' not in a) & (len(l)==8):
                print '\n'+strftime("%Y-%m-%d %H:%M:%S"), 'download starting...'
                fm.ftp_download(yesterday)
                print('download complete, start model')
                os.system('python /home/appuser/plaza_match/plaza_match.py')
                print('model complete,upload starting...')
                fm.ftp_upload(yesterday)
                print strftime("%Y-%m-%d %H:%M:%S"), 'upload complete\n'
            else:
                fm.ftp.quit()
                time.sleep(600)
        else:
            fm.ftp.quit()
            time.sleep(3600)










