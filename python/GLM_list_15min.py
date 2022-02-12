import numpy as np
import pandas as pd
import clima_anom as ca
import pandas as pd
import argparse
import os
import cartopy
import cartopy.feature as feature
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from netCDF4 import Dataset

parser = argparse.ArgumentParser()
parser.add_argument("-yr", "--year", type=str, required=True)
parser.add_argument("-mo", "--month", type=str, required=True)

args = vars(parser.parse_args())
year = vars(parser.parse_args())['year']
month = vars(parser.parse_args())['month']

Num_dias = ca.days_number(year,month)

print()
print(f'YEAR : {year}')
print(f'MONTH: {month}')
print(f'Days : {Num_dias}')
print()

for mm in range(Num_dias):

    Dia = ("{:02d}".format(mm+1))
    print(f'Dia: {Dia}')

    filename='/media/arturo/Seagate Expansion Drive/GLM/Data/'+year+'/'+month+'/basic/'+Dia+'/Data_GOES_'+Dia+'.txt'
    Total_list = pd.read_csv(filename,header=None,delimiter=';')
    GLM_list = Total_list[1]

    for h in range(24):
        Hora = ("{:02d}".format(h))
        # print(f'  Hora: {Hora}')

        test_00_14 = []
        test_15_29 = []
        test_30_44 = []
        test_45_59 = []

        for t in range(len(GLM_list)):
            name_out = GLM_list[t].split('/')[4]

            start_time = GLM_list[t].split('_')[3]
            hour_s = start_time[8:10]
            minu_s = start_time[10:12]
            segu_s = start_time[12:14]

            end_time = GLM_list[t].split('_')[4]
            hour_e = end_time[8:10]
            minu_e = end_time[10:12]
            segu_e = end_time[12:14]

            if hour_s == Hora:
                if int(minu_s) >= 0 and int(minu_s) < 15:
                    tmp = 'GLM/Data/'+year+'/'+month+'/basic/'+Dia+'/'+name_out
                    test_00_14.append(tmp)
                elif int(minu_s) >= 15 and int(minu_s) < 30:
                    tmp = 'GLM/Data/'+year+'/'+month+'/basic/'+Dia+'/'+name_out
                    test_15_29.append(tmp)
                elif int(minu_s) >= 30 and int(minu_s) < 45:
                    tmp = 'GLM/Data/'+year+'/'+month+'/basic/'+Dia+'/'+name_out
                    test_30_44.append(tmp)
                elif int(minu_s) >= 45 and int(minu_s) < 60:
                    tmp = 'GLM/Data/'+year+'/'+month+'/basic/'+Dia+'/'+name_out
                    test_45_59.append(tmp)

        dir_base = '/mnt/Data/Data/GLM/SA/List/List_15min/'+year+'/'+month

        if not os.path.exists(dir_base):
            os.makedirs(dir_base)

        export_00_14 = pd.DataFrame({'File':test_00_14})
        salida_00_14 = dir_base + '/List_15min_'+year+'_'+month+'_'+Dia+'_'+Hora+'_'+'00_14.csv'
        export_00_14.to_csv(salida_00_14, index = None, header=True)

        export_15_29 = pd.DataFrame({'File':test_15_29})
        salida_15_29 = dir_base + '/List_15min_'+year+'_'+month+'_'+Dia+'_'+Hora+'_'+'15_29.csv'
        export_15_29.to_csv(salida_15_29, index = None, header=True)

        export_30_44 = pd.DataFrame({'File':test_30_44})
        salida_30_44 = dir_base + '/List_15min_'+year+'_'+month+'_'+Dia+'_'+Hora+'_'+'30_44.csv'
        export_30_44.to_csv(salida_30_44, index = None, header=True)

        export_45_59 = pd.DataFrame({'File':test_45_59})
        salida_45_59 = dir_base + '/List_15min_'+year+'_'+month+'_'+Dia+'_'+Hora+'_'+'45_59.csv'
        export_45_59.to_csv(salida_45_59, index = None, header=True)

