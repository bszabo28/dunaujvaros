# -*- coding: utf-8 -*-
import osgeo.gdal as gdal
import subprocess
import psycopg2
import os

class Warp():

	def run(self,data,folder):
		
		p,f = os.path.split(data['path'])
		to = os.path.join(folder,self.subfolders[1],f)
		
		if(data['name'] in self.names):
			command = "gdalwarp -overwrite -s_srs EPSG:3857 -t_srs EPSG:3857 -dstalpha  -cutline {} -csql {} -crop_to_cutline -of GTiff -dstnodata 0 -dstnodata 0 {} {}".format(
				'"PG:{}"'.format(self.db),
				'"SELECT * FROM osszes WHERE kepnev=\'{}\'"'.format(data['name']),
				data['path'],
				to
			)
			if(os.path.exists(to) == False):
				os.popen(command)
		return to


        def __init__(self,subfolders,db):
                self.subfolders = subfolders
		self.db = db
		conn = psycopg2.connect(db)
		cur = conn.cursor()
		cur.execute("SELECT kepnev FROM nyers_osszes;")
		self.names = [i[0] for i in cur.fetchall()]
		cur.close()
		conn.close()

"""
gdalwarp -overwrite -s_srs EPSG:3857 -t_srs EPSG:3857 -crop_to_cutline -cutline "PG:host=127.0.0.1 port=5432 user='homestead' password='secret' dbname='szakdolgozat'" -csql "SELECT * FROM public.osszes WHERE (id=2);" -dstnodata 0 -of GTiff /home/vagrant/Code/Szakdolgozat/Feldolgozas/feldolgozott/1949/georeferalt/0029_002.tif /home/vagrant/Code/Szakdolgozat/Feldolgozas/feldolgozott/1949/vagott/0029_002.tif
gdalwarp -q -cutline /Users/balazs/Code/Szakdolgozat/Feldolgozas/fedveny/osszes.shp -dstalpha -tr 1.0 1.0 -of GTiff -cwhere "kepnev='0029_002'" /Users/balazs/Code/Szakdolgozat/Feldolgozas/feldolgozott/1949/georeferalt/0029_002.tif /Users/balazs/Code/Szakdolgozat/Feldolgozas/feldolgozott/1949/georeferalt/Névtelen.tif

gdalwarp -overwrite -s_srs EPSG:3857 -t_srs EPSG:3857 -of GTiff /home/vagrant/Code/Szakdolgozat/Feldolgozas/feldolgozott/1949/georeferalt/0029_002.tif /home/vagrant/Code/Szakdolgozat/Feldolgozas/feldolgozott/1949/vagott/0029_002.tif

gdalwarp -overwrite  -cutline fedveny/osszes.shp -dstalpha -tr 1.0 1.0 -of GTiff -cwhere 'kepnev="0029_002"' feldolgozott/1949/georeferalt/0029_002.tif feldolgozott/1949/georeferalt/a.tif
"""