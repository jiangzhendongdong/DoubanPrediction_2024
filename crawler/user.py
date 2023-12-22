import re
from bs4 import BeautifulSoup
from crawler.downloader import download

def UserInfo(url):
    soup = download(url)
    soup = BeautifulSoup(soup, 'lxml')
    INFO = soup.find_all('div', attrs={'class': 'user-info'})
    if len(INFO) > 0:
        info = str(INFO[0].find_all('div', attrs={'class': 'pl'})[0])
    else:
        return '-1'
    date = re.findall(r"\d+-\d+-\d+", info)[0]
    print(date)
    return date