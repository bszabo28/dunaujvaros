# -*- coding: utf-8 -*-
from osgeo import gdal, osr
import subprocess
import os

class Translate:

        def run(self,arr,folder):
                path,gcps = arr
                gcps = " ".join([ "-gcp {} {} {} {}".format(p[2],abs(p[3]),p[0],p[1]) for p in gcps])
                p,f = os.path.split(path)
                n, ext = os.path.splitext(f)
                temp = os.path.join(folder,'temp.tif')
                to = os.path.join(folder,self.subfolders[0],n + '.tif')
                command = 'gdal_translate -of GTiff {} "{}" "{}"'.format(gcps,path,to)
                if(os.path.exists(to) == False):
                        os.popen(command)
                return {
                        'path': to,
                        'name': n
                }

                #gdal_translate -of GTiff -gcp 726.687 952.335 2.09829e+06 5.94194e+06 -gcp 2532.58 1261.87 2.10164e+06 5.94167e+06 -gcp 3124.14 2477.76 2.10296e+06 5.93954e+06 -gcp 1223.62 3293.5 2.09956e+06 5.93777e+06 -gcp 3041.5 1317.91 2.10261e+06 5.94163e+06 "/Users/balazs/Code/Szakdolgozat/Feldolgozas/L-34-38-B-b/1949/0029_002.jpg" "/var/folders/tf/6yqpbty1297ckb7hhzjd2hfm0000gn/T/0029_002.jpg"
                #gdal_translate -of GTiff -gcp 726.687327824 -952.334710744 2098291.32701 5941935.96182 -gcp 2532.58264463 -1261.87258953 2101641.97872 5941668.29348 -gcp 3124.13705234 -2477.75964187 2102963.44637 5939543.48996 -gcp 1223.6177686 -3293.50482094 2099562.17259 5937770.06316 -gcp 3041.49548262 -1317.90686542 2102608.76101 5941634.54543 "/home/vagrant/Code/Szakdolgozat/Feldolgozas/L-34-38-B-b/1949/0029_002.jpg" "/home/vagrant/Code/Szakdolgozat/Feldolgozas/feldolgozott/1949/temp.tif"
                #gdalwarp -r cubic -tps -co COMPRESS=NONE  "/var/folders/tf/6yqpbty1297ckb7hhzjd2hfm0000gn/T/0029_002.jpg" "/Users/balazs/Code/Szakdolgozat/Feldolgozas/L-34-38-B-b/1949/0029_002.tif"


        def __init__(self,subfolders):
                self.subfolders = subfolders
                