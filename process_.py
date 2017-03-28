# -*- coding: utf-8 -*-
import os
from string import Template

class PointsReader():

        def gcp(self):
                return self.values

        def valid(self):
                return len(self.values) > 3

        def parameters(self,a=True):

                if(a):
                        return " ".join([ "-gcp {} {} {} {}".format(p[2],abs(p[3]),p[0],p[1]) for p in self.gcp() if p[4] == 1])
                else:
                        return " ".join([ "-gcp {} {} {} {}".format(p[2],p[3],p[0],p[1]) for p in self.gcp() if p[4] == 1])

        def __init__(self,path):
                lines = open(path).readlines()
                self.header = lines[0].replace('\n','').split(',')
                self.values = [[float(k) for k in l.replace('\n','').split(',')] for l in lines[1:]]


class FileFinder():

        forced = True

        db = "filefinder.txt"

        jpg = []
        files = []
        points = []
        raw = []
        georeferred = []
        loaded = []

        def save(self):

                f = open(self.db,'w')
                [
                        f.write("{};{}\n".format(
                                data['path'],
                                data['last_modified']
                        ))
                        for data in self.georeferred
                ]

                f.close()

        def load(self):

                if(os.path.exists(self.db) == False):
                        return
                
                f = open(self.db,'r')
                self.loaded = []

                for line in f.readlines():
                        path,last = line.replace('\n','').split(';')
                        self.loaded.append({
                                'path': path,
                                'last_modified': round(float(last),0)
                        })

        def changes(self):

                toReturn = []

                for i in self.georeferred:
                        temp = False
                        for j in self.loaded:
                                # Ha az útvonal egyezik és a módosítás ideje sem változott
                                if(j['path'] == i['path'] and j['last_modified'] == i['last_modified']):
                                        temp = True
                        
                        if(temp == False):
                                toReturn.append(i)
                return toReturn
                                

        def search(self):
                for r,d,f in os.walk(self.currentFolder):
                        self.files += ['{}/{}'.format(r,fi) for fi in f]
        
        def hasPair(self,path):
                n, ext = os.path.splitext(path)

                if(ext == '.points'):
                        return os.path.exists(path.replace('.points',''))
                else:
                        return os.path.exists(path + '.points')

        def separate(self):

                for path in self.files:
                        n, ext = os.path.splitext(path)
                        ext = ext.lower()

                        if(ext == '.jpg' or ext == '.jpeg'):
                                self.jpg.append(path)
                        elif(ext == '.points'):
                                self.points.append(path)
                
                self.georeferred = [{
                        "path": f,
                        "world": f + ".points",
                        "last_modified": round(os.stat(f).st_mtime,0),
                        "year": int(os.path.split(f)[0][-4:])
                } 
                for f in self.jpg if self.hasPair(f)]

                self.raw = [{
                        "path": f
                }
                for f in self.jpg if self.hasPair(f) == False]
        
        def byYear(self,year):

                if(self.forced):
                        return [i for i in self.georeferred if str(i['year']) == str(year)]
                else:
                        return [i for i in self.changes() if str(i['year']) == str(year)]

        def __init__(self,path):
                self.currentFolder = path
                self.db = os.path.join(self.currentFolder,self.db)
                self.load()
                self.search()
                self.separate()
                self.save()

class CommandFactory():

        autoreate = True
        autorun = False

        def createPath(self,path):
                if(os.path.exists(path) == False):
                        os.makedirs(path)


        def create(self,command,path,year,ext,subfolder):
                p,f = os.path.split(path)
                n,e = os.path.splitext(f)
                year = str(year)

                p = os.path.join(self.folder,year,subfolder,"{}.{}".format(n,ext))

                if(self.autoreate):
                        self.createPath(os.path.join(self.folder,year,subfolder))
                
                if(self.autorun):
                        if(os.path.exists(p)):
                                os.remove(p)

                        os.popen(Template(command).substitute(src=path, dst=p))

                return {
                        "commands": {
                                subfolder: {
                                        "path": p,
                                        "command": Template(command).substitute(src=path, dst=p)
                                }
                        }
                }

        def __init__(self,folder):
                self.folder = folder



############################################################
folder = os.path.dirname(os.path.realpath(__file__))
years = ["1953"]#,"1950","1951","1953","1954","1955"]
subfolders = ['modositott','georeferalt','vagott']
processedFolder = "feldolgozott"
origFolder = "eredeti"
############################################################
F = FileFinder(os.path.join(folder,origFolder))
C = CommandFactory(os.path.join(folder,processedFolder))
C.autorun = True

############################################################
command_convert = "convert $src -set colorspace Gray -separate -average $dst"
command_georeferencing = "gdal_translate -ot Byte -a_srs '+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +wktext  +no_defs' -of GTiff {} $src $dst"
command_cut = "gdalwarp -override $src $dst -s_srs '+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +wktext  +no_defs' -t_srs '+proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +wktext  +no_defs'"
#############################################################

for o in F.byYear(1949):

        # Kép módosítása
        modified = C.create(
                command_convert,
                o['path'],
                o['year'],
                'png',
                subfolders[0]
        )
        o.update(modified)
        
        # Kép georeferálása
        gcp = PointsReader(o['world']).parameters()
        partial_command = command_georeferencing.format(gcp)
        georeferenced = C.create(
                partial_command,
                o['commands'][subfolders[0]]['path'],
                o['year'],
                'tiff',
                subfolders[1]
        )
        o.update(georeferenced)

        # Kép megvágása
        C.create(
                partial_command,
                o['commands'][subfolders[1]]['path'],
                o['year'],
                'tiff',
                subfolders[2]
        )