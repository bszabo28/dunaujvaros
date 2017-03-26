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
years = ["1949","1950","1951","1953","1954","1955"]
subfolders = ['georeferalt','vagott']
processedFolder = "feldolgozott"

# Segédek
W = Warp(subfolders,db)
T = Translate(subfolders)
F = FileFinder(folder)

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

	# Georeferálás
	v = F.year(y)
	georeferenced = [T.run(a,_year) for a in v]
	cut = [W.run(i,_year) for i in georeferenced]

def main():
	for y in years:
		process(y)

if __name__ == "__main__":
    main()