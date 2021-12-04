import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient # 파이몽고를 쓰겠습니다.
client = MongoClient('localhost', 27017) #내 컴퓨터에 돌아가고 있는 몽고디비에 접속할 겁니다.
db = client.dbspartatoyprojcet

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://movie.naver.com/movie/running/current.naver',headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

# 코딩 시작

lis = soup.select('#content > div.article > div:nth-child(1) > div.lst_wrap > ul > li')

db.currentmovies.delete_many({})

#content > div.article > div:nth-child(1) > div.lst_wrap > ul > li:nth-child(1) >

for li in lis :
    title = li.select_one('dl > dt > a').text  # 제목
    movie_url = li.select_one('dl > dt > a')['href']  # 영화 주소
    # age = li.select_one('dl > dt > span').text  # 관람가
    image_url = li.select_one('div > a > img')['src']  # 이미지 주소
    # grade = li.select_one('dl > dd.star > dl.info_star > dd > div > a > span.num').text  # 평점
    reservation = float(li.select_one('dl > dd.star > dl.info_exp > dd > div > span.num').text)  # 예매율

    # genress = li.select('dl > dd:nth-child(3) > dl > dd:nth-child(2) > span.link_txt > a')
    # genre = []  # 장르(리스트)
    # for g in genress:
    #     ge = g.text
    #     genre.append(ge)
    # genres = ", ".join(genre)  # 장르(나열)

    # time_and_release = li.select_one('dl > dd:nth-child(3) > dl > dd:nth-child(2)').text
    # time = time_and_release.split('분')[0].split('|')[-1].strip() + "분"  # 상영 시간
    # release = time_and_release.split('개봉')[0].split('|')[-1].strip()  # 개봉일

    # directorss = li.select('dl > dd:nth-child(3) > dl > dd:nth-child(4) > span > a')
    # director = []  # 감독(리스트)
    # for d in directorss:
    #     di = d.text
    #     director.append(di)
    # directors = ", ".join(director)  # 장르(나열)

    # actorss = li.select('dl > dd:nth-child(3) > dl > dd:nth-child(6) > span > a')
    # actor = []  # 출연(리스트)
    # for a in actorss:
    #     ac = a.text
    #     actor.append(ac)
    # actors = ", ".join(actor)  # 장르(나열)

    doc = {
        'title': title ,
        'movie_url': movie_url,
        'image': image_url ,
        'reservation': reservation
    }
    db.currentmovies.insert_one(doc)

top20movies = list( db.currentmovies.find({},{'_id':False}).sort('reservation', -1).limit(20) )

# t20movies = sorted(db.currentmovies.find({}), key=(lambda x:x['reservation']), reverse=True)[: 20]

for i in top20movies :
    doc = {
        'title': i['title'],
        'movie_url': i['movie_url'],
        'image_url': i['image'],
        'reservation': i['reservation'],
        'ranking': top20movies.index(i)+1
    }

    db.top20movies.insert_one(doc)

