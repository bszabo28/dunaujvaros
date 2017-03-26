# -*- coding: utf-8 -*-
import os
import sys
import psycopg2
import datetime

sys.path.append(os.path.dirname(__file__))
from PointsReader import PointsReader

class FileFinder:

        jpg = []
        files = []
        points = []

        raw = []
        georeferred = []

        def updatedb(self):
                conn = psycopg2.connect(self.db)
                conn.autocommit = True
                cur = conn.cursor()

                data = [
                        {  
                                "name": os.path.split(filename)[1].replace(".jpg.points",""),
                                "time": datetime.date.fromtimestamp(os.stat(filename).st_mtime)
                                
                        }                        
                        for filename in self.points
                ]

                cur.execute("TRUNCATE nyers.osszes;")

                for d in data:
                        cur.execute("INSERT INTO nyers.osszes (name,last_modified) VALUES ('{}','{}')".format(d['name'],d['time']))
                cur.close()
		conn.close()

        def year(self,y):
                return self.gcps([p for p in self.georeferred if p.find(str(y)) != -1])
                

        def hasPair(self,path):
                n, ext = os.path.splitext(path)

                if(ext == '.points'):
                        return os.path.exists(path.replace('.points',''))
                else:
                        return os.path.exists(path + '.points')
        
        def gcps(self,arr=[]):
                if(len(arr) == 0):
                        arr= self.georeferred
                return [[path,PointsReader(path + '.points').gcp()] for path in arr]
        
        def georeferenced(self):
                self.georeferred = [f for f in self.jpg if self.hasPair(f)]
                self.raw = [f for f in self.jpg if self.hasPair(f) == False]

        def separate(self):

                for path in self.files:
                        n, ext = os.path.splitext(path)
                        ext = ext.lower()

                        if(ext == '.jpg' or ext == '.jpeg'):
                                self.jpg.append(path)
                        elif(ext == '.points'):
                                self.points.append(path)

        def search(self):
                for r,d,f in os.walk(self.currentFolder):
                        self.files += ['{}/{}'.format(r,fi) for fi in f]

        def __init__(self,path,db):
                self.db = db
                self.currentFolder = path
                self.search()
                self.separate()
                self.georeferenced()
                self.updatedb()