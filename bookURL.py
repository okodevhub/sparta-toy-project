import requests
from bs4 import BeautifulSoup

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://movie.naver.com/movie/bi/mi/running.naver?code=182362',headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')


## 상영관 장소/ 몇관 가져오기
bookingListBox = soup.select_one('#runningLayer')
lis = bookingListBox.select('li')
for li in lis:
    cine_title = li.select_one('strong').text
    cine_info_list = li.select('.no_cine_info')
    for no_cine_infos in cine_info_list:
        no_cine_info = no_cine_infos.text
        alist = li.select('.rsv_time a')
        for a_tag in alist:
            url = a_tag.get('href')
            showtime = a_tag.text.split('종료')[0]
            print(cine_title, no_cine_info, showtime, url)

