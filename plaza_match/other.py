# -*- coding: utf-8 -*-
#from ftplib import FTP
import time
import ftplib
import os

class test(object):
    def __init__(self):   
        self.ip = 'ip地址'
        self.port = '端口'
        self.user = '用户名'
        self.password = '密码'
        self.bufsize = 1024
        self.ftp = ftplib.FTP()
        #self.ftp.cwd('/PLAZA/')
        self.ftp.encoding = 'utf8'

    def ftp_connect(self):
        try:
            self.ftp.connect(self.ip, self.port)
            self.ftp.login(self.user,self.password)
            self.ftp.encoding = 'utf8'
            return self.ftp.getwelcome()
        except ftplib.error_perm:
            time.sleep(1)
            self.ftp_connect()

    def ls(self, path='/PLAZA/'):
        self.ftp.cwd(path)
        return self.ftp.dir()

    def ftp_delete(self, name):
        self.ftp.delete(name)
        print name+u' -- 已经删除'

    def ftp_download(self, path):
        self.ftp.cwd('/PLAZA/'+path)
        l = self.ftp.nlst()       
        for i in l:
            file_handle = open('/home/appuser/plaza_match/gc/'+i,"wb")
            self.ftp.retrbinary('RETR '+i, file_handle.write, self.bufsize)
            file_handle.close()
        self.ftp.cwd('/')

    def run(self):
        os.system('python /home/appuser/plaza_match/plaza_match.py')

    def ftp_upload(self,path):
        self.ftp.cwd('/PLAZA/')
        file_handle = open('/home/appuser/plaza_match/Plaza_Match.csv',"rb")
        self.ftp.storbinary('STOR '+'Plaza_Match_'+path+'.csv', file_handle, self.bufsize)
        file_handle.close()

if __name__=='__main__':
    t = test()
    t.ftp_connect()
    t.ls()
