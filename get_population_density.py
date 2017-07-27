#!/usr/bin/env python
# encoding: utf-8

import csv
import time
import numpy as np

# Tokyo
lat_min_t = 35.5
lat_max_t = 35.796
lon_min_t = 139.4
lon_max_t = 139.9
# Osaka
lat_min_o = 34.45
lat_max_o = 34.85
lon_min_o = 135.3
lon_max_o = 135.7
# Fukuoka
lat_min_f = 33.48
lat_max_f = 33.76
lon_min_f = 130.25
lon_max_f = 130.7
# Nagoya
lat_min_n = 35.00
lat_max_n = 35.32
lon_min_n = 136.7
lon_max_n = 137.1
# Fukushima coastal
lat_min_fc = 36.97
lat_max_fc = 37.85
lon_min_fc = 140.85
lon_max_fc = 141.05
# Fukushima land
lat_min_fl = 37.29
lat_max_fl = 37.85
lon_min_fl = 140.28
lon_max_fl = 140.60

num_time = 48
num_days = 61
dt = 24 * 3600 / num_time

def get_loc_idx(lat, lon, lat_min, lon_min, lat_max, lon_max, num_dislat):
    dis_lat = int((lat - lat_min) / 0.008)
    dis_lon = int((lon - lon_min) / 0.010)

    return dis_lat + dis_lon * num_dislat

lat_min = lat_min_fc
lon_min = lon_min_fc
lat_max = lat_max_fc
lon_max = lon_max_fc
num_dislat = int((lat_max - lat_min + 1e-6) / 0.008)
num_dislon = int((lon_max - lon_min + 1e-6) / 0.010)

population_density = np.zeros([num_dislat * num_dislon, num_time * num_days])
init_time = time.mktime(time.strptime('2011-02-28 23:50:00','%Y-%m-%d %H:%M:%S'))

with open('fukushima_coastal.csv', 'r') as f:
    for uid_str, time_str, lat_str, lon_str in csv.reader(f):
        uid = int(uid_str)
        lat = float(lat_str)
        lon = float(lon_str)
        if lat < lat_min or lat >= lat_max or lon < lon_min or lon >= lon_max:
            continue
        lid = get_loc_idx(lat, lon, lat_min, lon_min, lat_max, lon_max, num_dislat)
        tstamp = time.mktime(time.strptime(time_str,'%Y-%m-%d %H:%M:%S'))
        tid = int((tstamp - init_time) / dt)
        if tid >= num_time * num_days or tid < 0:
            print time_str
            continue
        population_density[lid, tid] += 1.0

np.savetxt('fukushima_coastal_pd.csv', population_density, delimiter=',')

lat_min = lat_min_fl
lon_min = lon_min_fl
lat_max = lat_max_fl
lon_max = lon_max_fl
num_dislat = int((lat_max - lat_min + 1e-6) / 0.008)
num_dislon = int((lon_max - lon_min + 1e-6) / 0.010)

population_density = np.zeros([num_dislat * num_dislon, num_time * num_days])
init_time = time.mktime(time.strptime('2011-02-28 23:50:00','%Y-%m-%d %H:%M:%S'))

with open('fukushima_land.csv', 'r') as f:
    for uid_str, time_str, lat_str, lon_str in csv.reader(f):
        uid = int(uid_str)
        lat = float(lat_str)
        lon = float(lon_str)
        if lat < lat_min or lat >= lat_max or lon < lon_min or lon >= lon_max:
            continue
        lid = get_loc_idx(lat, lon, lat_min, lon_min, lat_max, lon_max, num_dislat)
        tstamp = time.mktime(time.strptime(time_str,'%Y-%m-%d %H:%M:%S'))
        tid = int((tstamp - init_time) / dt)
        if tid >= num_time * num_days or tid < 0:
            print time_str
            continue
        population_density[lid, tid] += 1.0

np.savetxt('fukushima_land_pd.csv', population_density, delimiter=',')
