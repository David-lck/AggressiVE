import pandas as pd
import os
import time

def main(file=r'C:\AggressiVE_GITHUB\AggressiVE\input_parameters.xlsx'):
    n=1
    while n < 5:
        try:
            os.makedirs('Ags'+str(n))
        except:
            n += 1
            continue
        break
    os.chdir(r'C:\Users\limchink\PythonSv\Ags'+str(n))
    current_time = str(time.ctime().replace(" ","_").replace(":",""))
    print(current_time)
    logfile_name = 'logfile_'+str(current_time)+'.log'
    df = open(logfile_name,'w')
    df.write('test'+str(n))
    df.close()

