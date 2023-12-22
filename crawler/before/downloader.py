import requests
from time import sleep

HEADERS_douban = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
    'Cookie': 'll="108288"; bid=up0rofOlT4o; __yadk_uid=6Piu6D9gQlgkP4gC3hgArFi0RunP6k5T; push_noty_num=0; push_doumail_num=0; _vwo_uuid_v2=DDF215CC01DBBE41F222EC90538FB2D8A|49272204d8258e96190df0b4354e4dd2; __utma=30149280.1436538775.1618204010.1618204010.1618721534.2; __utmz=30149280.1618721534.2.2.utmcsr=qdan.me|utmccn=(not set)|utmcmd=(not set)|utmctr=(not provided); __utma=223695111.1097268048.1618204010.1618204010.1618721534.2; __utmz=223695111.1618721534.2.2.utmcsr=qdan.me|utmccn=(not set)|utmcmd=(not set)|utmctr=(not provided); _pk_ref.100001.4cf6=["","",1619498308,"https://m.douban.com/"]; _pk_ses.100001.4cf6=*; __gads=ID=711c888999a2e5f0-22dfaadf9dc7003c:T=1619498309:RT=1619498309:S=ALNI_MZFOiKjGCpwqqIx_9KalMsBejTvlA; _pk_id.100001.4cf6=144675c5bcfcfa6a.1618198911.4.1619498357.1618722649.; dbcl2="226186082:B5H3Q7prE2E"'
}


def download(url, web='douban'):
    HEADERS = {}
    if web == 'douban':
        HEADERS = HEADERS_douban
    else:
        HEADERS = HEADERS_douban
    try:
        # 如果不登录抓取的数据可能会很有限（未证实），这里简化处理认证部分逻辑，直接把我的cookie信息复制过来
        resp = requests.get(url,
                            headers=HEADERS,
                            timeout=30.0)
        resp.raise_for_status()
        # print(resp.text)
        return resp.text  # .encode('utf-8')
    except requests.RequestException as e:
        print("下载错误1，进入休眠")
        print(e)
        # sleep(600)
    except Exception as e:
        print(e)
        print("下载错误1，进入休眠")
        # sleep(600)


def download2(url, web='douban'):
    HEADERS = {}
    # url = "https://www.baidu.com/s?wd=%09%E5%A4%A9%E6%B0%94%E4%B9%8B%E5%AD%90%09%09%09%09%09%09%09%09%09%09%09%09%09%09%09%09%09%09%09%09%E8%B1%86%E7%93%A3"
    if web == 'douban':
        HEADERS = HEADERS_douban
    else:
        HEADERS = HEADERS_douban
    try:
        print(HEADERS['Cookie'])
        # 如果不登录抓取的数据可能会很有限（未证实），这里简化处理认证部分逻辑，直接把我的cookie信息复制过来
        resp = requests.get(url,
                            headers=HEADERS,
                            timeout=30.0)
        resp.raise_for_status()
        # print(resp.text)
        return resp.text  # .encode('utf-8')
    except requests.RequestException as e:
        print("下载错误2，进入休眠")
        # sleep(600)
    except Exception as e:
        print("下载错误2，进入休眠")
        # sleep(600)
