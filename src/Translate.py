# -*- coding: utf-8 -*-
from osgeo import gdal, osr
import subprocess
import psycopg2
import os

class Translate:

        def run(self,arr,folder,a=True):
                path,gcps = arr
                if(a):
                        gcps = " ".join([ "-gcp {} {} {} {}".format(p[2],abs(p[3]),p[0],p[1]) for p in gcps if p[4] == 1])
                else:
                        gcps = " ".join([ "-gcp {} {} {} {}".format(p[2],p[3],p[0],p[1]) for p in gcps if p[4] == 1])

                p,f = os.path.split(path)
                n, ext = os.path.splitext(f)
                temp = os.path.join(folder,'temp.tif')
                to = os.path.join(folder,self.subfolders[0],n + '.tif')
                command = 'gdal_translate -of GTiff {} "{}" "{}"'.format(gcps,path,to)
                if(os.path.exists(to) == False or n in self.rows):
                        os.popen(command)
                return {
                        'path': to,
                        'name': n
                }

        def __init__(self,subfolders,db):
                self.subfolders = subfolders
                self.db = db

                conn = psycopg2.connect(self.db)
                cur = conn.cursor()

                cur.execute("SELECT * FROM nyers.valtozas")
                self.rows = [k[0] for k in cur.fetchall() if k[1] == False]

                cur.execute("UPDATE vagott.osszes SET last_modified = nyers.osszes.last_modified FROM nyers.osszes WHERE vagott.osszes.name = nyers.osszes.name")
                conn.commit()

                cur.close()
                conn.close()