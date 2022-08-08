import os
import time
import shutil
import pymysql
import pandas as pd
from datetime import datetime, timedelta

while True:
    #connect to database
    mydb = pymysql.connect(host='140.96.143.30',
                        port=3306,
                        user='itri',
                        passwd='itri',
                        charset='utf8',
                        db='itri_database')

    path = 'C:/Users/460428/Desktop/CSV/temp_csv'
    file_name = [name for name in os.listdir(path) if name[-4:] == '.csv']
    #file_name = ['300-001-2021-09-22-17-22-20.csv']

    with mydb.cursor() as cursor:
        now_time = datetime.now()
        pre_time = now_time + timedelta(minutes=-1)
        for name in file_name:
            p_time = pre_time.strftime("%H-%M")
            if '.csv' in name and name[19:24] != p_time:
                #load csv
                df = pd.read_csv(path + '/' + name)
                print('Load ' + name)

                table_name = 'DB_' + name[:7].replace('-', '_')
                file_date = name[8:18]
                file_start_time = df.values[0][2]
                file_end_time = df.values[-1][2]
                print(table_name)
                print(file_date)
                print(file_start_time)
                print(file_end_time)
                '''
                Part 1: csv to sql
                '''
                
                '''print(f'Checking table \'{table_name}\' exists...')'''
                #if table isn't exists create it
                sql = f"""CREATE TABLE IF NOT EXISTS {table_name}(
                            Status varchar(20),
                            Date date,
                            Time time(3),
                            Set_p int(10),
                            Real_f float,
                            Cal_f float,
                            Delta float)"""
                cursor.execute(sql)
                print(f'>>Table {table_name} created')

                #truncate table
                '''sql = f"""TRUNCATE TABLE {table_name}"""
                cursor.execute(sql)'''

                print(f'Preparing data...')
                #select time data by date
                sql = f"""SELECT Time FROM {table_name} WHERE Date = '{file_date}'
                            AND Time BETWEEN '{file_start_time}' AND '{file_end_time}'"""
                cursor.execute(sql)
                temp_col_time = cursor.fetchall()
                '''temp_col_time = 1'''
                
                #convert datetime datatype to string
                col_time = []
                for t in temp_col_time:
                    dt = datetime.datetime.strptime(file_date, '%Y-%m-%d')
                    dt += t[0]
                    col_time.append(dt.strftime('%H:%M:%S.%f')[:-3])
                #classify data to insert_data or update_data
                insert_data, update_data = [], []
                i = 0
                for row in df.values:
                    if row[2] not in col_time:
                        insert_data.append(row)
                    else:
                        update_data.append(row)
                    i += 1
                print(f'>>Done')
                
                #insert and update data
                print(f'Inserting data...')
                t_start = time.time()
                for data in insert_data:
                    sql = f"""INSERT INTO {table_name}(Status, Date, Time, Set_p, Real_f, Cal_f, Delta)
                                VALUES {tuple(data)}"""
                    cursor.execute(sql)
                t_end = time.time()
                print(f'>> {str(len(insert_data))} data inserted (cost time: {t_end-t_start:.3f}s)')
                
                print(f'Updating data...')
                t_start = time.time()
                if update_data:
                    case_sta, case_set, case_rea, case_cal, case_del = f'', f'', f'', f'', f''
                    for data in update_data:
                        case_sta += f"""WHEN '{data[2]}' THEN '{data[0]}' """
                        case_set += f"""WHEN '{data[2]}' THEN {data[3]} """
                        case_rea += f"""WHEN '{data[2]}' THEN {data[4]} """
                        case_cal += f"""WHEN '{data[2]}' THEN {data[5]} """
                        case_del += f"""WHEN '{data[2]}' THEN {data[6]} """
                        
                    sql = f"""UPDATE {table_name} SET
                                Status = CASE Time {case_sta} ELSE Status END,
                                Set_p = CASE Time {case_set} ELSE Set_p END,
                                Real_f = CASE Time {case_rea} ELSE Real_f END,
                                Cal_f = CASE Time {case_cal} ELSE Cal_f END,
                                Delta = CASE Time {case_del} ELSE Delta END
                                WHERE Date = '{file_date}' AND
                                Time BETWEEN '{file_start_time}' AND '{file_end_time}'"""
                    cursor.execute(sql)
                t_end = time.time()
                print(f'>> {str(len(update_data))} data updated (cost time: {t_end-t_start:.3f}s)')

                print('Upload ' + name + ' completed')
                
                '''
                    Part 2: classify csv
                '''
                

                src_file = f'{path}/{name}'
                des_addr_path = f'C:/Users/460428/Desktop/CSV/csv_file/{name[:7]}'
                des_date_path = f'{des_addr_path}/{file_date}'

                print(f'Checking destination folder \'{des_date_path}\' exists...')
                if not os.path.isdir(des_addr_path):
                    os.mkdir(des_addr_path)
                if not os.path.isdir(des_date_path):
                    os.mkdir(des_date_path)
                shutil.move(src_file, des_date_path)
                print(f'>>Moving \'{name}\' successfully')
                
                print()
                
            mydb.commit()

    mydb.close()

