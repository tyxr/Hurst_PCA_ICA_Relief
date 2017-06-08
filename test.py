import pickle
import numpy as np
import neurolab as nl
def main():
    N = open('Ndata_pickle','r')
    P = open('Pdata_pickle','r')
    Pdata = pickle.load(P)
    Ndata = pickle.load(N)
    return Ndata,Pdata
def test_neuro():
    Ndata,Pdata = main()

    
    p_data = []
    x = len(Ndata)#N file number
    y = len(Ndata[0])#channel number here is 8
    o = len(Pdata)#P file number
    p = len(Pdata[0])#channel number here is 8

    bpnet=nl.load('relief_hurst.net')
    answer = bpnet.sim(Ndata[7])
    print answer
    for i in range(o):
        n_answer = bpnet.sim(Pdata[i])
        print n_answer
test_neuro()      
    
