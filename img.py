import requests
import sqlite3
from bs4 import BeautifulSoup
import re

# index_url = "https://movie.douban.com/people/49583935/collect"



    
def spider(url, url_list):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser', from_encoding='utf-8')
    imgs = soup.find_all('img', src=re.compile(r'movie_poster_cover'))
    urls = []
    next_url = False
    for img in imgs:
        urls.append(img['src'])
    next_link = soup.find('link', rel='next')
    if next_link:
        next_url = next_link['href']
    for url in urls:
        url_list.append(url + '\n')
    
    return next_url

def main(index_url = "https://movie.douban.com/people/49583935/collect"):
    url_list = []   
    while index_url:
        print(index_url)
        index_url = spider(index_url, url_list)
    f = open('img_urls.txt','w')
    f.writelines(url_list)
    f.close()


if __name__  == "__main__":
    main()
    
