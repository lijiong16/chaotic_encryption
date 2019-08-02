import numpy as np
import random
import pdb
"""
first ？ num of quanternary shows some info
the leading 0 for binfile, 1 for txt, 2 for img
The second 0 means num of characters in the original list is even,1 for odd

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
        a1=int(j/64)
        a2=int((j-a1*64)/16)
        a3=int((j-a1*64-a2*16)/4)
        a4=int(j-a1*64-a2*16-a3*4)
        n.append(a1)
        n.append(a2)
        n.append(a3)
        n.append(a4)         
    return np.array(n)
def quant2txt(ql):
    txt=''
    
    tmp=ql[1:].reshape(-1,4)
    for i in tmp:
        txt+=chr(64*i[0]+16*i[1]+4*i[2]+i[3])
    return txt
def img2quant(img): 
    n=[]
    n.append(2)
    for i in img:
        for j in i:
            a1=int(j/64)
            a2=int((j-a1*64)/16)
            a3=int((j-a1*64-a2*16)/4)
            a4=int(j-a1*64-a2*16-a3*4)
            n.append(a1)
            n.append(a2)
            n.append(a3)
            n.append(a4)         
    return np.array(n)
def quant2img(ql):
    img=[]
    tmp=ql[1:].reshape(-1,4)
    for i in tmp:
        img.append(64*i[0]+16*i[1]+4*i[2]+i[3])
    return np.array(img)
def dna2quant(A):
    n=[]
    for i in range(len(A)):
        if A[i]=='A':
            n.append(0)
        elif A[i]=='T':
            n.append(1)
        elif A[i]=='G':
            n.append(2)
        else:
            n.append(3)
    return n
def quant2dna(n):
    A=''
    for i in range(len(n)):
        if np.mod(n[i],4)==0:
            A=A+'A'
        elif np.mod(n[i],4)==1:
            A=A+'T'
        elif np.mod(n[i],4)==2:
            A=A+'G'
        else:
            A=A+'C'
    return A
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
def deencryp_quant(key,quant):
    """
    key is a tuple of 3
    """
    u,x=key
    lens=len(quant)
    key=gen_key(u,x,lens)
    return np.array([(quant[i]-key[i])%4 for i in range(len(quant))])
def decode_quant(ql):
    if ql[0]==1:
        return quant2txt(ql)
    if ql[0]==2:
        return quant2img(ql)
