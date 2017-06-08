import os
import scipy.io as sio
import numpy as np
import re
import random
from sklearn.decomposition import FastICA, PCA
import numpy as np
from scipy import signal
import nolds
import pickle
def get_file():
        N = re.compile('N')
        P = re.compile('P')
        path = 'F:\data2'
        a = list(os.walk(path))
        a = a[0]
        a = a[2]
        array_1 = []
        array_2 = []
        n = 0
        d = []
        d2 = []
        for i in a:
            x = i.split('.',1)
            try:
                    if x[1]=='mat':
                                if bool(N.match(x[0]))==True:
                                        
                                        i = str(i)
                                        print i
                                        try:
                                                a = main(i)
                                                if a is None:
                                                        continue
                                                else:
                                                        array_1.append(a)
                                        except:
                                                continue
                                                        
                                else:
                                    pass
                                if bool(P.match(x[0]))==True:
                                        i = str(i)
                                        print i
                                        try:
                                                a = main(i)
                                                if a is None:
                                                        continue
                                                else:
                                                        array_2.append(a)
                                        except:
                                                continue
            except:
                continue
        print array_1
        print array_2
        Ndata = open('Ndata_pickle','w')
        pickle.dump(array_1,Ndata)
        Ndata.close()
        Pdata = open('Pdata_pickle','w')
        pickle.dump(array_2,Pdata)
        Pdata.close()
def get_array(name):
    channel_num = 16
    array = []
    array_value = 0
    array_1 = []
    s = 0
    n = sio.loadmat(name)
    egMatrix = (n["dataStruct"][["data"]])[0][0][0]
    egMatrix = egMatrix.T
    egSamplingRate = list(n["dataStruct"][["iEEGsamplingRate"]])[0][0][0][0][0]
    egDataLength = list(n["dataStruct"][["nSamplesSegment"]])[0][0][0][0][0]
    egChannels = list(n["dataStruct"][["channelIndices"]])[0][0][0][0]
    return egMatrix.T
            
def main(name):    
    egMatrix = get_array(name)

    pca = PCA(n_components=8,whiten=True)

    H = pca.fit_transform(egMatrix)


    ica = FastICA(whiten=False)

    S = ica.fit_transform(H)
    c = []
    for i in range(8):
        c.append(sparate(H[:,i]))
    return c
def sparate(a_column):
        a = int(len(a_column)/10)
        b = []
        for i in range(10):
                c = []
                for j in range(a):
                        c.append(a_column[i*a+j])
                d = nolds.hurst_rs(c)
                b.append(d)
        return b
get_file()
