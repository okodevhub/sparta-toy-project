import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbspartamc

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
# 추출항목 : code, title, title_en, prdt_year, audience_point, critic_point, netizen_point,genre,nations,running_time,open_date,directors,actors,film_rating,audience_accum, story

# code, ranking 추출
data = requests.get('https://movie.naver.com/movie/running/current.naver',headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')
# ranking=[]
code=[]
comments = soup.find_all(string = lambda text: isinstance(text, Comment))
for c in comments:
  if "N=a:nol.img,r:" in c:
    code.append(c.split(",")[2][2:])   
# ranking=ranking[:19]
code=code[:19]

# 나머지 추출
for i in code:
  code_data={'code':int(i)}
  req= requests.get("https://movie.naver.com/movie/bi/mi/basic.naver",params=code_data,headers=headers)
  soup=BeautifulSoup(req.text,'html.parser')
  infos=soup.select("#content > div.article > div.mv_info_area > div.mv_info")
  
  for info in infos:
    # 제목
    title = info.select_one("h3 > a:nth-of-type(1)").text 
    # 영문 제목
    title_en = info.select_one("strong")['title'].split(",")[0]
    # production year(?)
    prdt_year = info.select_one("strong")['title'].split(",")[1]
    # 관람객 평점
    audience_point = float(info.select_one("div.main_score > div:nth-of-type(1) > a > div > span > span")['style'][6:-1])*0.1
    # 평론가 평점
    critic_point = float(info.select_one("div.main_score > div:nth-of-type(2) > div > a > div > span > span")['style'][6:-1])*0.1
    # 네티즌 평점
    netizen_point = float(info.select_one("div.main_score > div:nth-of-type(3) > div:nth-of-type(2) > a > span > span")['style'][6:-1])*0.1
    # 장르
    genre = info.select_one("dl > dd > p > span:nth-of-type(1) > a").text 
    # 국가
    nations = info.select_one("dl > dd > p > span:nth-of-type(2) > a").text 
    # 상영 시간
    running_time = info.select_one("dl > dd > p > span:nth-of-type(3)").text 
    # 개봉일자
    o_year = info.select_one("dl > dd > p > span:nth-of-type(4) > a:nth-of-type(1)").text[1:] #개봉년도
    o_date = info.select_one("dl > dd > p > span:nth-of-type(4) > a:nth-of-type(2)").text #개봉월일
    open_date=o_year+o_date
    # 감독
    directors = info.select_one("dl > dd:nth-of-type(2)").text
    # 배우
    actors = info.select_one("dl > dd:nth-of-type(3)").text
    # 상영 등급
    film_rating = info.select_one("dl > dd:nth-of-type(4) > p > a").text
    # 누적 관객
    audience_accum = info.select_one("dl > dd:nth-of-type(5)> div > p:nth-of-type(2)").text

  # 줄거리 : 전체가 아니라 부분만 추출되네요...
  story = soup.select_one("#content > div.article > div.section_group.section_group_frst > div:nth-of-type(1) > div > div.story_area p.con_tx").text
  doc = {'code':i,
         'title':title, 
         'title_en':title_en, 
         'prdt_year':prdt_year, 
         'audience_point':audience_point, 
         'critic_point':critic_point, 
         'netizen_point':netizen_point,
         'genre':genre,
         'nations':nations,
         'running_time':running_time,
         'open_date':open_date,
         'directors':directors,
         'actors':actors,
         'film_rating':film_rating,
         'audience_accum':audience_accum,
         'story':story}
  db.MovieDetails.insert_one(doc)
  

