import numpy as np
import pandas as pd
import clima_anom as ca
import pandas as pd
import argparse
import os
import glob
import cartopy
import cartopy.feature as feature
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

from shapely.geometry import Polygon, Point
import rtree as rt

from netCDF4 import Dataset

parser = argparse.ArgumentParser()
parser.add_argument("-yr", "--year", type=str, required=True)
parser.add_argument("-mo", "--month", type=str, required=True)
parser.add_argument("-re", "--region", type=str, required=True)

args = vars(parser.parse_args())
year = vars(parser.parse_args())['year']
month = vars(parser.parse_args())['month']
region = vars(parser.parse_args())['region']

Num_dias, ds, de, month_name = ca.days_number(year,month)

if region == 'SA':
    resolution = 0.5
    grid_r = '05x05'
    data_dir = '/mnt/Data/Data/GLM/SA/Point/'+year+'/'+month+'/*.csv'
    file_name_out = '/mnt/Data/Data/GLM/SA/Grid/GLM_'+year+'_'+month+'_15min_'+grid_r+'.nc'
    var_unit = 'flash/0.5x0.5'
    lon_new = np.arange(-85,-30,resolution)
    lat_new = np.arange(-45,10,resolution)
    lons = np.arange(-85,-30+resolution,resolution)
    lats = np.arange(-45,10+resolution,resolution)

elif region == 'SP':
    resolution = 14/111
    grid_r = '14kmx14km'
    data_dir = '/mnt/Data/Data/GLM/SP/Point/'+year+'/'+month+'/*.csv'
    file_name_out = '/mnt/Data/Data/GLM/SP/Grid/GLM_'+year+'_'+month+'_15min_'+grid_r+'.nc'
    var_unit = 'flash/14kmx14km'
    lon_new = np.arange(-49,-45,resolution)
    lat_new = np.arange(-25,-21,resolution)
    lons = np.arange(-49,-45+resolution,resolution)
    lats = np.arange(-25,-21+resolution,resolution)

elif region == 'test':
    resolution = 0.5
    grid_r = '05x05'
    data_dir = '/mnt/Data/Data/GLM/SA/Point/'+year+'/'+month+'/*.csv'
    file_name_out = '/mnt/Data/Data/GLM/SA/Grid/Test_'+year+'_'+month+'_15min_'+grid_r+'.nc'
    var_unit = 'flash/0.5x0.5'
    lon_new = np.arange(-60,-50,resolution)
    lat_new = np.arange(-20,0,resolution)
    lons = np.arange(-60,-50+resolution,resolution)
    lats = np.arange(-20,0+resolution,resolution)

else:
    print(f'Region {region} dind\'t exist')
    exit()

print()
print(f'YEAR      : {year}')
print(f'MONTH     : {month}')
print(f'REGION    : {region}')
print(f'RESOLUTION: {grid_r}')
print()

grids = list()
for lat in range(lats.size-1):
    for lon in range(lons.size-1):
        lu = Point(lons[lon], lats[lat])
        ru = Point(lons[lon+1], lats[lat])
        rb = Point(lons[lon+1], lats[lat+1])
        lb = Point(lons[lon], lats[lat+1])
        poly = Polygon((lu, ru, rb, lb, lu))
        grids.append(poly)

grid = np.reshape(grids, (lats.size-1, lons.size-1))

lista = glob.glob(data_dir)
lista = sorted(lista)
tempos = len(lista)

Densidad = np.zeros([tempos,len(lat_new),len(lon_new)])
count = 0
for i in range(tempos): 

    if os.path.exists(lista[i]):

        if i % 100 == 0 or i == tempos-1:
            print(i+1,'de',tempos,' ',lista[i])

        data_in = pd.read_csv(lista[i])
        data = pd.DataFrame({'Lat':data_in['Lat'],'Lon':data_in['Lon']})

        tree = rt.index.Index()

        for i, row in data.iloc[:,:].iterrows():
            tree.insert(i, Point(row.Lon, row.Lat).bounds)

        mapping = list()

        for g in grids:
            matches = list(tree.intersection(g.bounds))
            mapping.append(len(matches))

        density = np.reshape(mapping, (lats.size-1, lons.size-1))

    else:
        print('   ',lista[i],'No Existe')
        density = np.zeros([len(lat_new),len(lon_new)])

    Densidad[count,:,:] = densityvar_unit = 'flash/0.5x0.5'
    count = count + 1

print()
print(f'EXPORT TO : {file_name_out}')

info = {'file': file_name_out,
        'title': 'GLM flash 0.5x0.5', 
        'year_start':int(year),'month_start':int(month),'day_start':ds,'hour_start':0,'minute_start':0,
        'year_end':int(year),'month_end':int(month),'day_end':de,'hour_end':23,'minute_end':59,
        'time_frequency': 'minutely', 
        'time_interval': 15,
        'var_name': 'flash', 
        'var_units': var_unit}

ca.create_netcdf(info,Densidad,lat_new,lon_new)