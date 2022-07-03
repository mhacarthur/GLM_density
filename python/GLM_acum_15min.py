import glob
import numpy as np
import pandas as pd
import clima_anom as ca
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
parser.add_argument("-ac", "--acumm", type=str, required=True)
parser.add_argument("-re", "--region", type=str, required=True)

args = vars(parser.parse_args())
year = vars(parser.parse_args())['year']
month = vars(parser.parse_args())['month']
acumm = vars(parser.parse_args())['acumm']
region = vars(parser.parse_args())['region']

# data_dir = '/mnt/Data/Data/GLM/SA/List/List_'+ acumm + '/'+year+'/'+month+'/*.csv'
data_dir = '/mnt/Data/Data/GLM/SA/List/List_'+ acumm + '/'+year+'/'+month+'/*.csv'
lista_GLM = glob.glob(data_dir)
lista_GLM = sorted(lista_GLM)

print(f'Files: {len(lista_GLM)}')
print()

for t in range(len(lista_GLM)): #len(lista_GLM)

    name = lista_GLM[t]
    name_out = lista_GLM[t].split('/')[10].replace("List", "Flash")
    Dia = name_out.split('_')[4]
    Hora = name_out.split('_')[5]
    Minu_s_s = name_out.split('_')[6]

    lista_files = pd.read_csv(name)

    GLM_dia = []
    GLM_hora = []
    GLM_min = []
    GLM_lon = []
    GLM_lat = []

    salida = '/mnt/Data/Data/GLM/SA/Point/'+year+'/'+month+'/' + name_out

    for n in range(len(lista_files)):

        # name_v1 = '/media/arturo/Seagate Expansion Drive/' + lista_files['File'][n]
        name_v1 = '/mnt/Data/' + lista_files['File'][n]
        data = Dataset(name_v1,mode = 'r')

        lat = data['flash_lat']
        lon = data['flash_lon']

        GLM_lat = np.concatenate(([GLM_lat,lat]), axis=0)
        GLM_lon = np.concatenate(([GLM_lon,lon]), axis=0)

        GLM_flash = pd.DataFrame({'dia':Dia,'hora':Hora,'minuto':Minu_s_s,'Lat':GLM_lat,'Lon':GLM_lon})

        if region == 'SA':
            out1 = GLM_flash[(GLM_flash['Lon'] > -85) & (GLM_flash['Lon'] < -30 )]
            out2 = out1[(out1['Lat'] > -45) & (out1['Lat'] < 10 )]

        elif region == 'SaoPaulo':
            out1 = GLM_flash[(GLM_flash['Lon'] > -50) & (GLM_flash['Lon'] < -44 )]
            out2 = out1[(out1['Lat'] > -25) & (out1['Lat'] < -20 )]

        else:
            print(f'Region {region} dind\'t exist')
            exit()

    dir_base = '/mnt/Data/Data/GLM/SA/Point/'+year+'/'+month+'/'

    if not os.path.exists(dir_base):
        os.makedirs(dir_base)

    salida = dir_base + name_out
    export_csv = out2.to_csv(salida, index = None, header=True)
    print(salida)
