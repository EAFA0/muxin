from urllib.parse import urlparse

def id_from_url(url: str) -> str:
    '''
    获取 url 中 /*.(ext) 前面 * 匹配的部分
    '''
    path = urlparse(url).path
    return path.split('/')[-1].partition('.')[0]