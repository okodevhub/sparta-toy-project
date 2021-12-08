import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbspartatoyprojcet

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://movie.naver.com/movie/running/current.naver',headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

# 코딩 시작

lis = soup.select('#content > div.article > div:nth-child(1) > div.lst_wrap > ul > li')

db.currentmovies.delete_many({})

for li in lis :
    title = li.select_one('dl > dt > a').text  # 제목
    # movie_url = li.select_one('dl > dt > a')['href']  # 영화 주소
    code = li.select_one('dl > dt > a')['href'].split("=")[-1]  # 코드
    image_url = li.select_one('div > a > img')['src']  # 이미지 주소
    reservation = float(li.select_one('dl > dd.star > dl.info_exp > dd > div > span.num').text)  # 예매율

    print(code)

    doc = {
        'title': title ,
        'code' : code,
        'image': image_url ,
        'reservation': reservation
    }
    db.currentmovies.insert_one(doc)

top20movies = list( db.currentmovies.find({},{'_id':False}).sort('reservation', -1).limit(20) )

for i in top20movies :
    doc = {
        'title': i['title'],
        'code' : i['code'],
        'image_url': i['image'],
        'reservation': i['reservation'],
        'ranking': top20movies.index(i)+1
    }

    db.top20movies.insert_one(doc)

