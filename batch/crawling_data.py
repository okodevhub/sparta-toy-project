import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome import options
from datetime import datetime

# Header 유저정보
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
}

# Chrome Driver 위치 (AWS로 옮길 경우 수정 필요)
# chrome_driver_dir = "/opt/homebrew/bin/chromedriver"
chrome_driver_dir = "/home/ubuntu/chromedriver"

# 현재상영영화중 예매율20위 영화 가져오기
def get_top20_movies():
    data = requests.get(
        "https://movie.naver.com/movie/running/current.naver?view=list&order=reserve",
        headers=headers,
    )
    soup = BeautifulSoup(data.text, "html.parser")

    movies = soup.select(
        "#content > div.article > div:nth-child(1) > div.lst_wrap > ul > li"
    )

    current_movies = []

    for movie in movies:
        # 영화코드
        code = movie.select_one("dl > dt > a")["href"].split("=")[-1]
        # 영화제목
        title = movie.select_one("dl > dt > a").text
        # 포스터URl
        image_url = movie.select_one("div > a > img")["src"].split("?")[0]
        # 예매율
        reservation = float(
            movie.select_one("dl > dd.star > dl.info_exp > dd > div > span.num").text
        )

        doc = {
            "title": title,
            "code": code,
            "image": image_url,
            "reservation": reservation,
        }
        current_movies.append(doc)

    top20movies = sorted(
        current_movies, key=(lambda x: x["reservation"]), reverse=True
    )[:20]
    top20_movies = []

    for i in top20movies:
        doc = {
            "title": i["title"],
            "code": i["code"],
            "image_url": i["image"],
            "advanced_rate": i["reservation"],
            "ranking": top20movies.index(i) + 1,
        }
        top20_movies.append(doc)
    return top20_movies


# 영화 상세 정보
def get_movie_detail(code):
    url = f"https://movie.naver.com/movie/bi/mi/basic.naver?code={code}"

    # 옵션 생성
    options = webdriver.ChromeOptions()

    # 창 숨기는 옵션 추가
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(
        "--user-agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'"
    )

    # chrome driver 실행
    driver = webdriver.Chrome(chrome_driver_dir, options=options)
    driver.get(url)

    # 영화기본정보
    mv_info_elem = driver.find_element_by_xpath(
        "//*[@id='content']/div[1]/div[2]/div[1]"
    )

    # 영화제목(영문), 제작연도 가져오기
    title_en = ""
    prdt_year = ""
    h_movie2_elem = (
        mv_info_elem.find_element_by_xpath("strong[@class='h_movie2']")
        .get_attribute("title")
        .split(",")
    )
    if len(h_movie2_elem) == 2:
        # 영화제목(영문)
        title_en = h_movie2_elem[0].strip()
        # 제작연도
        prdt_year = h_movie2_elem[1].strip()
    elif len(h_movie2_elem) == 3:
        # 영화제목(영문)
        title_en = h_movie2_elem[1].strip()
        # 제작연도
        prdt_year = h_movie2_elem[2].strip()
    elif len(h_movie2_elem) == 1:
        # 제작연도
        prdt_year = h_movie2_elem[0].strip()

    # 관람객 평점 가져오기
    actual_pt_elems = mv_info_elem.find_elements_by_xpath(
        "//*[@id='actualPointPersentBasic']/div/em"
    )
    # 관람객 평점
    audience_point = ""
    for actual_pt_elem in actual_pt_elems:
        audience_point += actual_pt_elem.text

    # 평론가 평점 가져오기
    spc_score_elems = mv_info_elem.find_elements_by_xpath("div[1]/div[2]/div/a/div/em")
    # 평론가 평점
    critic_point = ""
    for spc_score_elem in spc_score_elems:
        critic_point += spc_score_elem.text

    # 네티즌 평점 가져오기
    netizen_score_elems = mv_info_elem.find_elements_by_xpath(
        "//*[@id='pointNetizenPersentBasic']/em"
    )
    # 네티즌 평점
    netizen_point = ""
    for netizen_score_elem in netizen_score_elems:
        netizen_point += netizen_score_elem.text

    info_spec_elems_cnt = len(
        mv_info_elem.find_elements_by_xpath("dl[@class='info_spec']/dt")
    )

    genre = ""
    nation = ""
    running_time = ""
    open_date = ""
    directors = []
    actors = []
    film_rating = ""
    audience_accum = ""

    for i in range(1, info_spec_elems_cnt + 1):
        info_spec_elem = mv_info_elem.find_element_by_xpath(
            f"dl[@class='info_spec']/dt[{i}]"
        )

        # 개요정보 가져오기
        if info_spec_elem.get_attribute("class") == "step1":
            # 장르 가져오기
            genre = mv_info_elem.find_element_by_xpath(f"dl/dd[{i}]/p/span[1]/a").text
            # 국가 가져오기
            nation = mv_info_elem.find_element_by_xpath(f"dl/dd[{i}]/p/span[2]/a").text
            # 상영시간 가져오기
            running_time = mv_info_elem.find_element_by_xpath(
                f"dl/dd[{i}]/p/span[3]"
            ).text
            # 개봉일 가져오기
            open_date_elems = mv_info_elem.find_elements_by_xpath(
                f"dl/dd[{i}]/p/span[4]/a"
            )
            for open_date_elem in open_date_elems:
                open_date += open_date_elem.text.strip()

        # 감독 정보 가져오기
        elif info_spec_elem.get_attribute("class") == "step2":
            direct_elems = mv_info_elem.find_elements_by_xpath(f"dl/dd[{i}]/p/a")
            for direct_elem in direct_elems:
                directors.append(direct_elem.text)

        # 출연 정보 가져오기
        elif info_spec_elem.get_attribute("class") == "step3":
            actor_elems = mv_info_elem.find_elements_by_xpath(f"dl/dd[{i}]/p/a")
            for actor_elem in actor_elems:
                actors.append(actor_elem.text)

        # 등급 정보 가져오기
        elif info_spec_elem.get_attribute("class") == "step4":
            film_rating = mv_info_elem.find_element_by_xpath(f"dl/dd[{i}]/p/a").text

        # 흥행 정보 가져오기
        elif info_spec_elem.get_attribute("class") == "step9":
            hit_info_elems = mv_info_elem.find_elements_by_xpath(f"dl/dd[{i}]/div/p")
            for hit_info_elem in hit_info_elems:
                if hit_info_elem.get_attribute("class") == "count":
                    audience_accum = hit_info_elem.text

    # 줄거리 가져오기
    story = driver.find_element_by_xpath(
        "//*[@id='content']/div[1]/div[4]/div[1]/div/div[1]/p"
    ).text

    # driver 종료
    driver.quit()

    detail_info = {
        "title_en": title_en,
        "prdt_year": prdt_year,
        "audience_point": audience_point,
        "critic_point": critic_point,
        "netizen_point": netizen_point,
        "genre": genre,
        "nation": nation,
        "running_time": running_time,
        "open_date": open_date,
        "directors": directors,
        "actors": actors,
        "film_rating": film_rating,
        "audience_accum": audience_accum,
        "story": story,
    }

    return detail_info


# 상영 테이블 정보
def get_movie_time_table(code, regionRootCode, regionSubCode):

    # 오늘 날짜 가져오기
    reserveDate = datetime.today().strftime("%Y-%m-%d")

    data = {
        "code": f"{code}",
        "regionRootCode": f"{regionRootCode}",
        "regionSubCode": f"{regionSubCode}",
        "reserveDate": reserveDate,
        "sort": 0,
    }

    url = "https://movie.naver.com//movie/bi/mi/runningJson.naver"

    response = requests.post(url, headers=headers, data=data).json()

    # 영화코드, 지역정보, 예약일자가 일치하지 않을 경우 빠져나옴
    if (
        str(response["regionSub"]["regionCode"]) != regionRootCode
        and str(response["regionSub"]["subRegionCode"]) != regionSubCode
    ):
        print(
            f"{datetime.now()} 영화({code}) 지역({regionRootCode}, {regionSubCode})에 상영시간표가 없습니다"
        )
        return

    elif response["reserveDate"] != reserveDate:
        print(
            f"{datetime.now()} 영화({code}) 지역({regionRootCode}, {regionSubCode})의 {reserveDate}일자 상영시간표가 없습니다"
        )
        return

    # 전체페이지 수 확인
    totalPages = response["pagerInfo"]["totalPages"]
    time_tables = []
    for i in range(1, totalPages + 1):
        if i == 1:
            time_tables += get_group_schedule(
                code, regionRootCode, regionSubCode, response["groupScheduleList"]
            )

        else:
            data["page"] = i
            response = requests.post(url, headers=headers, data=data).json()
            time_tables += get_group_schedule(
                code, regionRootCode, regionSubCode, response["groupScheduleList"]
            )

    return time_tables


def get_group_schedule(code, regionRootCode, regionSubCode, groupScheduleList):
    time_tables = []

    for group_schedule in groupScheduleList:
        theater = group_schedule["gname"]
        brand = theater.split(" ")[0]

        # CGV, 메가박스, 롯데시네마가 아닐 경우 다음으로 넘어감
        if brand not in ("CGV", "메가박스", "롯데시네마"):
            print(
                f"{datetime.now()} 영화({code}) 지역({regionRootCode}, {regionSubCode})의 상영관은 CGV, 메가박스, 롯데시네마가 아닙니다"
            )
            continue

        for theater_schedule in group_schedule["theaterScheduleList"]:
            for time_table in theater_schedule["timetableList"]:
                auditorium = time_table["tname"]
                show_time = time_table["rtime"]
                reservation_url = time_table["ticketPcUrl"]
                reserveDate = time_table["rdate"]
                t_table = {
                    "regionRootCode": regionRootCode,
                    "regionSubCode": regionSubCode,
                    "code": code,
                    "brand": brand,
                    "theater": theater,
                    "auditorium": auditorium,
                    "reserveDate": reserveDate,
                    "show_time": show_time,
                    "reservation_url": reservation_url,
                }
                time_tables.append(t_table)

    return time_tables
