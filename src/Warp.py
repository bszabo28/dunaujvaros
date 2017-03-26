# -*- coding: utf-8 -*-
import osgeo.gdal as gdal
import subprocess
import psycopg2
import os

class Warp():

	def run(self,data,folder):
		p,f = os.path.split(data['path'])
		to = os.path.join(folder,self.subfolders[1],f)
		if(data['name'] in self.rows):
			command = "gdalwarp -overwrite -s_srs EPSG:3857 -t_srs EPSG:3857 -dstalpha  -cutline {} -csql {} -crop_to_cutline -of GTiff -dstnodata 0 -dstnodata 0 {} {}".format(
				'"PG:{}"'.format(self.db),
				'"SELECT ST_SETSRID(geom,3857) as geom FROM vagott.osszes_javitott WHERE name=\'{}\'"'.format(data['name']),
				data['path'],
				to
			)
			#if(os.path.exists(to) == False):
			os.popen(command)
			return to


        def __init__(self,subfolders,db):
                self.subfolders = subfolders
		self.db = db
		
		conn = psycopg2.connect(self.db)
                cur = conn.cursor()

                cur.execute("SELECT * FROM vagott.osszes")
                self.rows = [k[1] for k in cur.fetchall()]

                cur.close()
                conn.close()
