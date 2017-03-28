

class PointsReader:

        def gcp(self):
                return self.values

        def valid(self):
                return len(self.values) > 3

        def parameters(self):

                if(a):
                        return " ".join([ "-gcp {} {} {} {}".format(p[2],abs(p[3]),p[0],p[1]) for p in gcp() if p[4] == 1])
                else:
                        return " ".join([ "-gcp {} {} {} {}".format(p[2],p[3],p[0],p[1]) for p in gcp() if p[4] == 1])

        def __init__(self,path):
                lines = open(path).readlines()
                self.header = lines[0].replace('\n','').split(',')
                self.values = [[float(k) for k in l.replace('\n','').split(',')] for l in lines[1:]]