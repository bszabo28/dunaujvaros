

class PointsReader:

        def gcp(self):
                return self.values

        def valid(self):
                return len(self.values) > 3

        def __init__(self,path):
                lines = open(path).readlines()
                self.header = lines[0].replace('\n','').split(',')
                self.values = [[float(k) for k in l.replace('\n','').split(',')] for l in lines[1:]]