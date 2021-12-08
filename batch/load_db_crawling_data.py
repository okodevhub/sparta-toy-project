import requests
import crawling_data as crawling_data
from pymongo import MongoClient
from datetime import datetime

client = MongoClient("localhost", 27017)
# client = MongoClient("mongodb://test:test@localhost", 27017)
db = client.dbmoviemoa

# TOP20영화 데이터 DB에 담기
top20_movies = crawling_data.get_top20_movies()
db.top20movies.delete_many({})
db.top20movies.insert_many(top20_movies)
db.top20movies.update_many({}, {"$currentDate": {"created_dt": {"$type": "date"}}})
print(f"{datetime.now()} [top20movies] 총{len(top20_movies)}건 INSERT 완료")

# DB지역정보
regions = list(db.regions.find({}, {"_id": False}))

db.running_time_table.delete_many({})
for movie in top20_movies:
    detail_info = crawling_data.get_movie_detail(movie["code"])
    db.top20movies.update_one(
        {"code": movie["code"]}, {"$set": {"detail_info": detail_info}}
    )
    db.top20movies.update_one(
        {"code": movie["code"]}, {"$currentDate": {"updated_dt": {"$type": "date"}}}
    )
    print(f"{datetime.now()} [top20movies] 영화({movie['code']}) 업데이트 완료")

    for region in regions:
        for region_sub in region["regionSubs"]:
            time_tables = crawling_data.get_movie_time_table(
                movie["code"], region["regionRootCode"], region_sub["regionSubCode"]
            )
            if time_tables is not None and time_tables:

                db.running_time_table.insert_many(time_tables)
                print(
                    f"{datetime.now()} [running_time_table] 영화({movie['code']}) 지역({region['regionRootCode']}, {region_sub['regionSubCode']}) {len(time_tables)}건 INSERT 완료"
                )

    db.running_time_table.update_many(
        {}, {"$currentDate": {"created_dt": {"$type": "date"}}}
    )
