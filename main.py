from helpers import _clear,_setTitle,_printText,_readFile,_getCurrentTime,_getRandomUserAgent,_getRandomProxy,colors
from threading import Thread,active_count
from time import sleep
from random import choice
import requests

class Downloader:
    def __init__(self) -> None:
        _setTitle('[TiktokVideoDownloader] ^| [NoWatermark]')
        _clear()
        title = colors['yellow']+"""
                                   ╔════════════════════════════════════════════════╗
                                     @@@@@@@ @@@ @@@  @@@ @@@@@@@  @@@@@@  @@@  @@@
                                       @@!   @@! @@!  !@@   @@!   @@!  @@@ @@!  !@@
                                       @!!   !!@ @!@@!@!    @!!   @!@  !@! @!@@!@! 
                                       !!:   !!: !!: :!!    !!:   !!:  !!! !!: :!! 
                                        :    :    :   :::    :     : :. :   :   :::
                                   ╚════════════════════════════════════════════════╝
        """
        print(title)

        self.downloaded = 0
        self.retries = 0

        self.use_proxy = int(input(f'{colors["white"]}[>] {colors["yellow"]}[1]Proxy [2]Proxyless:{colors["white"]} '))
        self.proxy_type = None
        if self.use_proxy != 2:
            self.proxy_type = int(input(f'{colors["white"]}[>] {colors["yellow"]}[1]Https [2]Socks4 [3]Socks5:{colors["white"]} '))

        self.session = requests.Session()
        print('')

    def _titleUpdate(self):
        while True:
            _setTitle(f'[TiktokVideoDownloader] ^| [NoWatermark] ^| DOWNLOADED: {self.downloaded} ^| RETRIES: {self.retries}')
            sleep(0.4)

    def _download(self,url):
        useragent = _getRandomUserAgent('useragents.txt')
        headers = {'User-Agent':useragent}
        proxy = _getRandomProxy(self.use_proxy,self.proxy_type,'proxies.txt')
        try:
            response = self.session.get(f'https://hamod.ga/api/tiktokWithoutWaterMark.php?u={url}',proxies=proxy,headers=headers)
            if 'link' in response.text:
                link = response.json()['link']
                _printText(colors['green'],colors['white'],'FOUND',link)
                video_content = self.session.get(link,proxies=proxy,headers=headers).content
                with open(f'[Downloads]/{_getCurrentTime()+"".join(choice("0123456789") for _ in range(6))}.mp4','wb') as f:
                    f.write(video_content)
                self.downloaded += 1
            else:
                _printText(colors['green'],colors['white'],'RETRY',url)
                self.retries += 1
                self._download(url)
        except Exception:
            self.retries += 1
            self._download(url)
        

    def _start(self):
        _setTitle('[TiktokVideoDownloader] ^| [Setup]')
        _clear()
        title = colors['yellow']+"""
                                   ╔════════════════════════════════════════════════╗
                                     @@@@@@@ @@@ @@@  @@@ @@@@@@@  @@@@@@  @@@  @@@
                                       @@!   @@! @@!  !@@   @@!   @@!  @@@ @@!  !@@
                                       @!!   !!@ @!@@!@!    @!!   @!@  !@! @!@@!@! 
                                       !!:   !!: !!: :!!    !!:   !!:  !!! !!: :!! 
                                        :    :    :   :::    :     : :. :   :   :::
                                   ╚════════════════════════════════════════════════╝
        """
        print(title)
        option = int(input(f'{colors["white"]}[>] {colors["yellow"]}[1]Just one video [2]Multiple videos from txt:{colors["white"]} '))
        Thread(target=self._titleUpdate).start()
        threads = []

        if option == 1:
            url = str(input(f'{colors["white"]}[>] {colors["yellow"]}Video URL:{colors["white"]} '))
            print('')
            self._download(url)
        else:
            video_urls = _readFile('video_urls.txt','r')
            thread_num = int(input(f'{colors["white"]}[>] {colors["yellow"]}Threads:{colors["white"]} '))
            print('')
            for video_url in video_urls:
                run = True
                while run:
                    if active_count() <= thread_num:
                        thread = Thread(target=self._download,args=(video_url,))
                        threads.append(thread)
                        thread.start()
                        run = False

            for x in threads:
                x.join()
        
        _printText(colors['yellow'],colors['white'],'FINISHED','Process done!')

if __name__ == '__main__':
    Downloader()._start()