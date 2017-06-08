import pickle
import numpy as np
import neurolab as nl
def main():
    N = open('Ndata_pickle','r')
    P = open('Pdata_pickle','r')
    Pdata = pickle.load(P)
    Ndata = pickle.load(N)
    return Ndata,Pdata
    
    

def n_Relief():
    Ndata,Pdata = main()
    
    n_data = []
    x = len(Ndata)
    y = len(Ndata[0])
    o = len(Pdata)
    p = len(Pdata[0])
    for i in range(x): #N file number
        for j in range(y):#channel number here is 8
            d = 0
            for l in range(x): #N file number 
                for m in range(y):#channel number here is 8
                    a = np.linalg.norm(np.array(Ndata[i][j])-np.array(Ndata[l][m]))
                    if a>d:
                        d = a
                    else:
                        pass
                       
            v = 0
            for s in range(o): #P file number
                for t in range(p):#channel number here is 8
                    b = np.linalg.norm(np.array(Ndata[i][j])-np.array(Pdata[s][t]))
                    if b>v:
                        v = b
                    else:
                        pass
            
            total = (-1)*d**2 + v**2
            n_data.append(total)
    n_data = list(n_data)
    sort_data = sorted(n_data,reverse=True)
    
    n_location = []
    for i in range(25):
        temp = n_data.index(sort_data[i])
        n_location.append(temp)
    print n_location

    
    nn_data = []
    for i in n_location:
        l,m = divmod(i,8)
        if m==0:
            nn_data.append(Ndata[l-1][7])
        else:
            nn_data.append(Ndata[l-1][m-1])
    return nn_data

    

def p_Relief():
    Ndata,Pdata = main()
    
    p_data = []
    x = len(Ndata)
    y = len(Ndata[0])
    o = len(Pdata)
    p = len(Pdata[0])
    for i in range(o): #P file number
        for j in range(p):#channel number here is 8
            d = 0
            for l in range(o): #P file number 
                for m in range(p):#channel number here is 8
                    a = np.linalg.norm(np.array(Pdata[i][j])-np.array(Pdata[l][m]))
                    if a>d:
                        d = a
                    else:
                        pass
                       
            v = 0
            for s in range(x): #P file number
                for t in range(y):#channel number here is 8
                    b = np.linalg.norm(np.array(Pdata[i][j])-np.array(Ndata[s][t]))
                    if b>v:
                        v = b
                    else:
                        pass
            
            total = (-1)*d**2 + v**2
            p_data.append(total)
    p_data = list(p_data)
    sort_data = sorted(p_data,reverse=True)
    p_location = []
    for i in range(25):
        temp = p_data.index(sort_data[i])
        p_location.append(temp)
    print p_location
    
    pp_data = []
    for i in p_location:
        l,m = divmod(i,8)
        if m==0:
            pp_data.append(Pdata[l-1][7])
        else:
            pp_data.append(Pdata[l-1][m-1])
    return pp_data
        

def neuro():
    nn_data = n_Relief()
    pp_data = p_Relief()
    total_data = np.array(nn_data + pp_data)
    
    target = np.array([[1] for i in range(25)] + [[0] for i in range(25)])
    target = target.reshape(len(target),1)
    
    bpnet = nl.net.newff([[0,1] for i in range(10)],[10,1])
    err = bpnet.train(total_data,target,epochs=3000,show=100,goal=0.02)
    bpnet.save('relief_hurst.net')
    answer = bpnet.sim(nn_data)
    answer2 = bpnet.sim(pp_data)
    #print nn_data
    print nn_data
    print answer2

neuro()   
