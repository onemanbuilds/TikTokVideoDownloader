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

    def PrintText(self,info_name,text,info_color:Fore,text_color:Fore):
        lock = Lock()
        lock.acquire()
        sys.stdout.flush()
        text = text.encode('ascii','replace').decode()
        sys.stdout.write(f'[{info_color+info_name+Fore.RESET}] '+text_color+f'{text}\n')
        lock.release()

    def __init__(self):
        self.SetTitle('One Man Builds TikTok Video Downloader Tool')
        self.clear()
        init()
        self.ua = UserAgent()
        self.use_proxy = int(input('[QUESTION] Would you like to use proxies [1] yes [0] no: '))
        self.method = int(input('[QUESTION] [1] Download 1 video [2] Download multiple videos from txt: '))
        print('')
        self.videos = self.ReadFile('videos.txt','r')
        self.header = headers = {'User-Agent':'okhttp','referer':'https://www.tiktok.com/'}

    def GetRandomProxy(self):
        proxies_file = ReadFile('proxies.txt','r')
        proxies = {
            "http":"http://{0}".format(random.choice(proxies_file)),
            "https":"https://{0}".format(random.choice(proxies_file))
            }
        return proxies

    def DownloadVideo(self):
        download_url = str(input('> TikTok Video URL: '))

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
        self.PrintText('DOWNLOADED','{0} -> {1}'.format(filename,download_url),Fore.GREEN,Fore.WHITE)

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
        self.PrintText('DOWNLOADED','{0} -> {1}'.format(filename,videos),Fore.GREEN,Fore.WHITE)

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
    