import pandas as pd
import os
import csv
''' git test '''
path = 'Data'
file_name = [name for name in os.listdir(path) if name[-4:] == '.csv']
'''
        Search CSV file in the folder
                                        '''
for name in file_name:
        df = pd.read_csv('./Data/' + name, encoding='latin1', dtype='unicode')
        #print(name)
        column = list(df.values[1]) #Data title
        rows = df.shape[0] #file row count
        #print(column)
        #print(rows)
        file1, file2 = [], []
        count = 1
        for i in range(2, rows):
                if count % 2 == 1:
                #print(i)
                        file1.append(list(df.values[i]))
                else:
                        file2.append(list(df.values[i]))
                count += 1

        file1 = pd.DataFrame(file1, columns=column)
        #print(file1)
        file2 = pd.DataFrame(file2, columns=column)
        #print(file2)

        '''
                Check Power Station status
                                                '''
        if int(float(file1.iat[1, 40])) > 0:
                print("Starting")
                print(file1.iat[1,40])
                file1.to_csv(f'./Splited/{name[:-4]}_1.1.csv', index = False)
        else:
                print("Not Starting")
                file1.to_csv(f'./Splited/{name[:-4]}_1.csv', index = False)
        
        file2.to_csv(f'./Splited/{name[:-4]}_2.csv', index = False)
