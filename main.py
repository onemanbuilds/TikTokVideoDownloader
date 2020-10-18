import os
import requests
import json
import time
import random
import sys
import substring
from colorama import init,Fore
from datetime import datetime
from multiprocessing.dummy import Pool as ThreadPool
from threading import Thread, Lock
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

class Main:
    def clear(self):
        if os.name == 'posix':
            os.system('clear')
        elif os.name in ('ce', 'nt', 'dos'):
            os.system('cls')
        else:
            print("\n") * 120

    def SetTitle(self,title_name:str):
        os.system("title {0}".format(title_name))

    def ReadFile(self,filename,method):
        with open(filename,method) as f:
            content = [line.strip('\n') for line in f]
            return content

    def __init__(self):
        self.SetTitle('One Man Builds TikTok Video Downloader Tool')
        self.clear()
        init(convert=True)
        title = Fore.YELLOW+"""
                             ___ _ _  _ ___ ____ _  _    _  _ _ ___  ____ ____  
                              |  | |_/   |  |  | |_/     |  | | |  \ |___ |  |  
                              |  | | \_  |  |__| | \_     \/  | |__/ |___ |__|  
                                                                            
                             ___  ____ _ _ _ _  _ _    ____ ____ ___  ____ ____ 
                             |  \ |  | | | | |\ | |    |  | |__| |  \ |___ |__/ 
                             |__/ |__| |_|_| | \| |___ |__| |  | |__/ |___ |  \ 
                                                                                
        """
        print(title)
        self.ua = UserAgent()
        self.use_proxy = int(input(Fore.YELLOW+'['+Fore.WHITE+'>'+Fore.YELLOW+'] Would you like to use proxies [1] yes [0] no: '))
        self.method = int(input(Fore.YELLOW+'['+Fore.WHITE+'>'+Fore.YELLOW+'] [1] Download 1 video [2] Download multiple videos from txt: '))
        print('')
        self.videos = self.ReadFile('videos.txt','r')
        self.header = headers = {'User-Agent':'okhttp','referer':'https://www.tiktok.com/'}

    def GetRandomProxy(self):
        proxies_file = self.ReadFile('proxies.txt','r')
        proxies = {
            "http":"http://{0}".format(random.choice(proxies_file)),
            "https":"https://{0}".format(random.choice(proxies_file))
            }
        return proxies

    def DownloadVideo(self):
        download_url = str(input(Fore.YELLOW+'['+Fore.WHITE+'>'+Fore.YELLOW+'] TikTok Video URL: '))

        if 'https://' not in download_url:
            download_url = 'https://{0}'.format(download_url)

        response = requests.get(download_url,headers=self.header).text

        soup = BeautifulSoup(response,'html.parser')
        script = soup.find('script',{'id':'__NEXT_DATA__'})

        while script == None:
            try:
                if self.use_proxy == 1:
                    response = requests.get(download_url,headers=self.header,proxies=self.GetRandomProxy()).text
                    soup = BeautifulSoup(response,'html.parser')
                    script = soup.find('script',{'id':'__NEXT_DATA__'})
                else:
                    response = requests.get(download_url,headers=self.header).text
                    soup = BeautifulSoup(response,'html.parser')
                    script = soup.find('script',{'id':'__NEXT_DATA__'})
                
                time.sleep(2)
            except:
                pass
            
        json_data = json.loads(script.string)
        full_url = json_data['props']['pageProps']['videoData']['itemInfos']['video']['urls'][0]

        download_req = requests.get(full_url,headers=self.header)
        filename = substring.substringByChar(download_url,'@','/')
        filename = filename.replace('/','')
       
        with open('Downloads/{0}'.format(filename+''.join(random.choice('0123456789') for _ in range(6))+'.mp4'), 'wb') as f:
            f.write(download_req.content)
        print('')
        print(Fore.GREEN+'['+Fore.WHITE+'!'+Fore.GREEN+'] DOWNLOADED | {0} | {1}'.format(filename,download_url))

    def DownloadVideos(self,videos):

        if 'https://' not in videos:
            videos = 'https://{0}'.format(videos)

        response = requests.get(videos,headers=self.header).text

        soup = BeautifulSoup(response,'html.parser')
        script = soup.find('script',{'id':'__NEXT_DATA__'})

        while script == None:
            try:
                if self.use_proxy == 1:
                    response = requests.get(videos,headers=self.header,proxies=self.GetRandomProxy()).text
                    soup = BeautifulSoup(response,'html.parser')
                    script = soup.find('script',{'id':'__NEXT_DATA__'})
                else:
                    response = requests.get(videos,headers=self.header).text
                    soup = BeautifulSoup(response,'html.parser')
                    script = soup.find('script',{'id':'__NEXT_DATA__'})
            except:
                pass
            
        json_data = json.loads(script.string)
        full_url = json_data['props']['pageProps']['videoData']['itemInfos']['video']['urls'][0]

        download_req = requests.get(full_url,headers=self.header)
        filename = substring.substringByChar(videos,'@','/')
        filename = filename.replace('/','')
       
        with open('Downloads/{0}'.format(filename+''.join(random.choice('0123456789') for _ in range(6))+'.mp4'), 'wb') as f:
            f.write(download_req.content)
        print(Fore.GREEN+'['+Fore.WHITE+'!'+Fore.GREEN+'] DOWNLOADED | {0} | {1}'.format(filename,videos))

    def Start(self):
        if self.method == 2:
            pool = ThreadPool()
            results = pool.map(self.DownloadVideos,self.videos)
            pool.close()
            pool.join()
        else:
            self.DownloadVideo()

        
if __name__ == "__main__":
    main = Main()
    main.Start()
    