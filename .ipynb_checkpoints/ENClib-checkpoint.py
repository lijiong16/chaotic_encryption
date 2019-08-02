import numpy as np
import random
import pdb
import matplotlib.pyplot as plt
"""
first ？ num of quanternary shows some info
the leading 0 for binfile, 1 for txt, 2 for img
The second 0 means num of characters in the original list is even,1 for odd

"""
def num2quant(num,aimlist,places):
    while places!=0:
        tmp=int(num/pow(4,places-1))
        aimlist.append(tmp)
        num-=tmp*pow(4,places-1)
        places-=1
def quant2num(aimlist):
    places=len(aimlist)
    ans=0
    for i in range(places):
        ans+=aimlist[i]*pow(4,places-i-1)
    return ans
"""
num2quant(j,n,4) == 
                
            a1=int(j/64)
            a2=int((j-a1*64)/16)
            a3=int((j-a1*64-a2*16)/4)
            a4=int(j-a1*64-a2*16-a3*4)
            n.append(a1)
            n.append(a2)
            n.append(a3)
            n.append(a4)  
"""
      
def bin2quant(binfile):
    n=[]
    n.append(0)
    return n

def txt2quant(txt): 
    n=[]
    n.append(1)
    for i in txt:
        j=ord(i)
        num2quant(j,n,4)        
    return np.array(n)

def img2quant(img): 
    n=[]
    n.append(2)
    shape=img.shape
    if len(shape)==3:
        n.append(3)
    else:
        n.append(1)
    for i in shape[0:2]:
        num2quant(i,n,7)
    img=img.reshape(1,-1)
    for j in img[0]:
        num2quant(j,n,4) 
    return np.array(n)

def quant2txt(ql):
    arg=[1]
    txt=str(ql[0])
    if ql[0]==1:
        
        tmp=ql[1:].reshape(-1,4)
        for i in tmp:
            txt+=chr(64*i[0]+16*i[1]+4*i[2]+i[3])
    elif ql[0]==2:
        
        tmp=ql.reshape(-1,4)  #2+14+4*lens
        for i in tmp:
            txt+=chr(64*i[0]+16*i[1]+4*i[2]+i[3])
    return txt,arg

def quant2img(ql):
    img=[]
    arg=[2]
    m=quant2num(ql[2:9])
    n=quant2num(ql[9:16])
    if ql[1]==3:
        shape=[m,n,3]
    else:
        shape=[m,n]
    arg.append(shape)
    tmp=ql[16:].reshape(-1,4)
    for i in tmp:
        img.append(64*i[0]+16*i[1]+4*i[2]+i[3])
    return np.array(img).reshape(shape),arg

def enc2quant(enc):
    if enc[0]=='1':
        n=[]
        n.append(1)
        for i in enc[1:]:
            j=ord(i)
            num2quant(j,n,4)        
        return np.array(n)
    elif enc[0]=='2':
        n=[]         #different cuz we add '2' to enctxt of img
        for i in enc[1:]:
            j=ord(i)
            num2quant(j,n,4)        
        return np.array(n)
def gen_key(u,x,lens):
    a=0
    key_list=[]
    real_key=[]
    for i in range(50+lens):
        if i==0:
            key_list.append(x)
        else: 
            key_list.append(u*key_list[i-1]*(1-key_list[i-1]))
    for i in key_list[50:50+lens]:
        real_key.append(np.mod(round(i*100000000),10))
    real_key[0]=0
    return real_key
def encryp_quant(key,quant):
    """
    key is a tuple of 2
    """
    u,x=key
    lens=len(quant)
    key=gen_key(u,x,lens)
    return np.array([(quant[i]+key[i])%4 for i in range(len(quant))])
def decryp_quant(key,quant):
    """
    key is a tuple of 3
    """
    u,x=key
    lens=len(quant)
    key=gen_key(u,x,lens)
    return np.array([(quant[i]-key[i])%4 for i in range(len(quant))])

def decode_quant(ql):
    if ql[0]==1 :
        return quant2txt(ql)
    elif ql[0]==2:
        return quant2img(ql)
    
def save_ans(re_file,arg,filename):
    if arg[0]==1:
        ff=open(filename+".txt",'w',encoding='utf-8')
        ff.write(re_file[1:])
        ff.close()
    elif arg[0]==2:
        if len(arg[1])==2:
            cmap='gray'
        else:
            cmap=None
        plt.imsave(filename+'.jpg',re_file.astype('uint8'),cmap=cmap)