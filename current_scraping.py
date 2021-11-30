import requests
from bs4 import BeautifulSoup

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://movie.naver.com/movie/running/current.naver',headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

# 코딩 시작

lis = soup.select('#content > div.article > div:nth-child(1) > div.lst_wrap > ul > li')

for li in lis:
    title = li.select_one('dl > dt > a').text # 제목
    age = li.select_one('dl > dt > span').text # 관람가
    grade = li.select_one('dl > dd.star > dl.info_star > dd > div > a > span.num').text # 평점
    reservation = li.select_one('dl > dd.star > dl.info_exp > dd > div > span.num').text + "%" # 예매율

    genres = li.select('dl > dd:nth-child(3) > dl > dd:nth-child(2) > span.link_txt > a')
    genre = [] # 장르(리스트)
    for g in genres:
        ge = g.text
        genre.append(ge)


    time_and_release = li.select_one('dl > dd:nth-child(3) > dl > dd:nth-child(2)').text
    time = time_and_release.split('분')[0].split('|')[-1].strip() + "분" # 상영 시간
    release = time_and_release.split('개봉')[0].split('|')[-1].strip() # 개봉일

    directors = li.select('dl > dd:nth-child(3) > dl > dd:nth-child(4) > span > a')
    director = [] # 감독(리스트)
    for d in directors:
        di = d.text
        director.append(di)

    actors = li.select('dl > dd:nth-child(3) > dl > dd:nth-child(6) > span > a')
    actor = [] # 출연(리스트)
    for a in actors:
        ac = a.text
        actor.append(ac)

    print(title, actor)




