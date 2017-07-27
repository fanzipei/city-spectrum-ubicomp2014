#!/usr/bin/env python
# encoding: utf-8

import csv
import time

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


def main():
    with open('fukushima_coastal.csv', 'w') as f_out_fc:
        with open('fukushima_land.csv', 'w') as f_out_fl:
            for m in xrange(3, 5):
                for d in xrange(1, 32):
                    if m == 4 and d == 31:
                        continue
                    with open('/data/zdc/2010/2010{:02d}{:02d}.csv'.format(m, d), 'r') as f_in:
                        for uid_str, time_str, lat_str, lon_str, _, _, _ in csv.reader(f_in):
                            # cnt += 1
                            # print cnt
                            uid = int(uid_str[3:])
                            lat = float(lat_str) / 3600000.0
                            lon = float(lon_str) / 3600000.0
                            time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(time_str, '%Y%m%d%H%M%S'))
                            if lat > lat_min_f and lat < lat_max_f and lon > lon_min_f and lon < lon_max_f:
                                f_out_fc.write('{},{},{},{}\n'.format(uid, lat, lon, time_str))
                            elif lat > lat_min_n and lat < lat_max_n and lon > lon_min_n and lon < lon_max_n:
                                f_out_fl.write('{},{},{},{}\n'.format(uid, lat, lon, time_str))


if __name__ == '__main__':
    main()
