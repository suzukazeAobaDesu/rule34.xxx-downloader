# coding=utf-8

from bs4 import BeautifulSoup
import requests
import urllib.request
import string,os,sys
from time import sleep
from datetime import datetime

def Connect(url):
    requests.adapters.DEFAULT_RETRIES = 5
    s = requests.session()
    s.keep_alive = False

    t=1
    while (not 'r' in locals().keys()) and t<=10:  
        try:
            r = requests.get(url)
        except:
            print('reconnecting..'+str(t))
            t+=1
            sleep(3)
            continue
    if(t>30):
        print('After trying to reconnect 30 times, the program still cannot connect to the server,program ends by itself.')    
        sys.exit(0)

    s = BeautifulSoup(r.content,"html.parser")
    return s


#Get the high-resolution or low-resolution version of the picture address in the picture page
def GetPicAdress(z,high_res):
    if high_res==1:
        for image in z.find_all("a",string="Original image"):
            t=str(image)
            t=t[t.find('href="')+len('href="'):]
            t=t[:t.find('" ')]
            img=t[t.rfind('/')+1:]

    elif high_res==0:
        for image in z.find_all(attrs={'id':'image'}):
            t=str(image)
            t=t[t.find('src="')+len('src="'):]
            t=t[:t.find('" ')]

            suffix=t[:t.find('?')]
            suffix=suffix[suffix.rfind('.'):]
            img=t[t.find('?')+1:]+suffix

    return t,img

def download(t,img):
    c=0
    while (not os.path.exists(img)) and c<=10:
        try:
            urllib.request.urlretrieve(t, img)
        except:
            print('\r',end='')
            print('redownloading...'+str(c))
            sleep(3)
            c+=1
        if(c>30):
            print('After trying to reconnect 30 times, the program still cannot connect to the server,program ends by itself.')    
            sys.exit(0)



def direct_download(link):
    z = Connect(link)
    if len(z.find_all(attrs={'id':'image'}))!=0:
        t,img=GetPicAdress(z,high_res)
        img=path+'\\'+img
        print(link)
        download(t,img)
    elif len(z.find_all(attrs={'type':'video/mp4'}))!=0:
        for image in z.find_all(attrs={'type':'video/mp4'}):
            t=str(image)
            t=t[t.find('src="')+len('src="'):]
            t=t[:t.find('" type=')]
            img=t[t.rfind('/')+1:]
            img=path+'\\'+img
            print(link)
            download(t,img)


def start():
    with open(txtpath, "r") as f:
        l=1
        for line in f.readlines():
            line = line.strip('\n')
            if len(line) >= 10:
                print('line  '+str(l),end=',  ')
                direct_download(line)
            l+=1
    print('compeleted!')

high_res=1
path = r"G:\DownLoad\rule34"
txtpath=r'C:\Users\admin\Desktop\rule34.txt'
start()


