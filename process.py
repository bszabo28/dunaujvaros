# -*- coding: utf-8 -*-
import shutil
import sys
import os

# Saját könyvtárak 
sys.path.append('src')
from Warp import Warp
from Translate import Translate
from FileFinder import FileFinder

# Beállítások
db = "host=127.0.0.1 port=5432 user='homestead' password='secret' dbname='szakdolgozat'"
folder = os.path.dirname(os.path.realpath(__file__))
years = ["1953"]#,"1950","1951","1953","1954","1955"]
subfolders = ['georeferalt','vagott']
processedFolder = "feldolgozott"

# Segédek
W = Warp(subfolders,db)
T = Translate(subfolders,db)
F = FileFinder(folder,db)

# 1 év feldolgozásának a folyamata
def process(y):
	_year = os.path.join(folder,processedFolder,str(y))
	
	# Könyvtárak létrehozása
        #if(os.path.exists(_year)):
		#shutil.rmtree(_year)
        if(os.path.exists(_year) == False):
		os.makedirs(_year)
		# Alkönyvtárak létrehozása
		for p in subfolders:
			os.makedirs(os.path.join(_year,p))
	# Alapinformációk
	print("--------")
	print("| {} |".format(y))
	print("--------")
	print("Képek száma: {}, Georeferált képek száma: {}, Arány: {}%".format(
		len(F.jpg),
		len(F.points),
		float(len(F.points)) / float(len(F.jpg)) * 100
	))
	# Georeferálás
	v = F.year(y)
	georeferenced = [T.run(a,_year,True if y=="1953" else False ) for a in v]
	cut = [W.run(i,_year) for i in georeferenced]
	print("Megvágott képek száma: {}, Arány: {}%".format(
		len(cut),
		float(len(cut)) / float(len(F.jpg)) * 100))
	print("---------------------------------------------")

def main():
	for y in years:
		process(y)

if __name__ == "__main__":
    main()