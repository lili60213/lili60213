from ctypes import *
import os
import sys
import ftplib
import time
from os import listdir
from os.path import isfile, isdir, join
import shutil
import datetime

while True:
    timeout = 60
    port = 21
    host = '140.96.143.30'
    user = 'ftpuser'
    passwd = '890826'
    try:
        ftp = ftplib.FTP()
        ftp.connect(host, port, timeout)
        ftp.login(user, passwd)

        path = '/home/pi/Desktop/'
        file_list = listdir(f'{path}record/')
        current_date_and_time = datetime.datetime.now()
        for name in file_list:
            now_time = current_date_and_time.strftime("%H-%M")
            if '.csv' in name and name[19:24] != now_time:
                print(name)

                addr_name = name[:7]
                year = name[8:12]
                month = name[13:15]

            '''
                FTP classified folder
            '''
            '''    
                ftp.cwd('../../../')
                try:
                    ftp.mkd(f'./{addr_name}')
                    ftp.cwd(f'./{addr_name}')
                except:
                    ftp.cwd(f'./{addr_name}')
                try:
                    ftp.mkd(f'./{year}')
                    ftp.cwd(f'./{year}')
                except:
                    ftp.cwd(f'./{year}')
                try:
                    ftp.mkd(f'./{month}')
                    ftp.cwd(f'./{month}')
                except:
                    ftp.cwd(f'./{month}')
            '''

                upload_file = open(f'{path}record/{name}','rb')
                ftp.storbinary('STOR '+name, upload_file)
                upload_file.close()

                '''
                    Part 2: classify csv
                '''

                src_file = f'{path}record/{name}'
                des_year_path = f'{path}csv_backup/{year}'
                des_month_path=f'{des_year_path}/{month}'

                if not os.path.isdir(des_year_path):
                    os.mkdir(des_year_path)
                if not os.path.isdir(des_month_path):
                    os.mkdir(des_month_path)
                shutil.move(src_file, des_month_path)
        ftp.quit()
        
    except:
            print('ftp error')

    time.sleep(60)

