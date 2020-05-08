# coding=utf-8

from bs4 import BeautifulSoup
import requests
import urllib.request
import string,os,sys,time
from time import sleep
from datetime import datetime


dat=datetime.now()
g_total_size=0
def speed():
    t=datetime.now()-dat
    spd=g_total_size/t.total_seconds()/1000
    return str(int(spd))+' kb/s'

def GetHours():
    t=int(time.strftime("%H", time.localtime()))
    return t

def Connect(url):
    requests.adapters.DEFAULT_RETRIES = 5
    s = requests.session()
    s.keep_alive = False

    t=1
    while (not 'r' in locals().keys()) and t<=20:  
        try:
            header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'}
            r = requests.get(url,headers = header)
        except:
            print('reconnecting..'+str(t))
            t+=1
            sleep(3)
            continue
    if(t>20):
        print('After trying to reconnect 20 times, the program still cannot connect to the server.') 
        
    s = BeautifulSoup(r.content,"html.parser")
    return s

def GetLast(url):
    s = Connect(url+"&pid=0")
    last = 0
    if len(s.find_all("a", string=">>"))!=0:
        for a in s.find_all("a", string=">>"):
            b=str(a)
            last=int(b[b.find('pid=')+len('pid='):b.find('">')])

    s = Connect(url+"&pid="+str(last))
    #print('URL of the last page is : '+str(url+"&pid="+str(last)))
    pages = last
    for a in s.find_all(attrs={'class':'thumb'}):
        pages += 1
    return last,pages
    #last=the last page nuber
    #pages=total pic numbers

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

def record(t):
    with open(path+'record.txt',"a") as f:
        f.write(t+'\n')
    print('ERROR URL has been wirting in '+path+'record.txt')



def download(t,img):
    c=1
    while (not os.path.exists(img)) and c<=10:
        try:
            opener=urllib.request.build_opener()
            opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(t, img)
        except:
            print('redownloading...'+str(c))
            sleep(2)
            c+=1
        if(c>10):
            print('After trying to redownload 10 times, the program still cannot connect to the server,program ends by itself.')
            record(t)
            

def GetPages(url):
    last,pages = GetLast(url)
    p=int(last/42+1)
    print(str(pages)+' pictures , ',end='')
    print(str(p)+' pages')


    for n in range(p):
        k=n*42
        print('='*80+'\n'+'page: '+str(n+1)+'/'+str(p)+'      url : '+str(url+"&pid="+str(k)))
        s = Connect(url+"&pid="+str(k))

        
        count=0
        for a in s.find_all(attrs={'class':'thumb'}):

            h=str(a)
            h=h[h.find('<a href="')+len('<a href="'):]
            h=h[:h.find('" id=')]
            h=h.replace('&amp;','&')
            
            count+=1
            print('post: '+str(k+count)+'/'+str(pages),end='')
            print(' , url : https://rule34.xxx/'+h)
            z = Connect('https://rule34.xxx/'+h)

            if len(z.find_all(attrs={'id':'image'}))!=0:

                t,img=GetPicAdress(z,high_res)
                img=path+'\\'+img
                download(t,img)

            elif len(z.find_all(attrs={'type':'video/mp4'}))!=0:
                for image in z.find_all(attrs={'type':'video/mp4'}):
                    t=str(image)
                    t=t[t.find('src="')+len('src="'):]
                    t=t[:t.find('" type=')]

                    img=t[t.rfind('/')+1:]
                    img=path+'\\'+img
                    download(t,img)

            elif len(z.find_all(attrs={'type':'video/mp4'}))==0:
                print('ERROR:can not find picture and video in this page:'+'https://rule34.xxx/'+h)


def MultipleTask(taglist):
    count=0
    for tag in taglist:
        count+=1
        print('task '+str(count)+' in progress...\n'+'='*130)
        Main(tag)


def Main(tag):
    global path
    path = r"D:\1myword\download"
    path=path+'\\'+tag.replace(' ','-').replace('\\','').replace(':','').replace('*','')
    if not os.path.exists(path):
        os.makedirs(path)
    print('Save path =  '+path)
    url =  "https://rule34.xxx/index.php?page=post&s=list&tags="+tag
    GetPages(url)



###################################################################################################

#If you want to disable some code, add # before the code


#file save path
#You can modify the following line of code to customize the download path
path = r"G:\DownLoad"

#The default download path is the 'test' folder under the folder where the program is located
#Delete the line below, or prefix the line with # to use a custom path


#high_res=0 lower resolution,Lower hard drive footprint
#high_res=1 higher resolution,higher hard drive footprint
high_res=1


#timer to run subsequent code after 200 seconds,remove the # before the code to make the timer take effect
#sleep(200)


#the tag can be written in advance, or written when the program is running,only one effect at a time
tag='buckethead_ero sound'
#tag = input("Please enter tag: ")
#Main(tag)  



#MultipleTask function will download multiple tags at once in the order of taglist
#When using Main (downloading one tag at a time) or MultipleTask (downloading multiple tags at one time),
#please add # before one of the lines of code, and do not add the other.
taglist = ['buckethead_ero sound']
MultipleTask(taglist)


#Queue_downloader can download the pictures and videos in the page 
#pointed by the address in turn according to the address given by download_link
# .txt.
#Queue_downloader.start()



if GetHours()<=6:
    os.system("shutdown -s -t  300")

