import requests
from bs4 import BeautifulSoup

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://movie.naver.com/movie/running/current.naver',headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbhomework

lis = soup.select('#content > div.article > div:nth-child(1) > div.lst_wrap > ul > li')

for li in lis:
    links = li.select_one('.tit a')
    link = links['href']
    moviecode = link.split('=')[1]
    movietitle = links.text
    #print(movietitle, moviecode)
    doc = {
        'code': moviecode,
        'title': movietitle
    }
    db.movie_details.insert_one(doc)

