from pymongo import MongoClient

client = MongoClient("localhost", 27017)
db = client.dbspartatoyprojcet

# 네이버의 지역정보
regions = [
    {
        "regionRootCode": "1",
        "regionRootName": "서울",
        "regionSubs": [
            {"regionSubCode": "53", "regionSubName": "강남구/서초구"},
            {"regionSubCode": "54", "regionSubName": "강동구/송파구/광진구"},
            {"regionSubCode": "55", "regionSubName": "강북구/노원구"},
            {"regionSubCode": "56", "regionSubName": "강서구/양천구"},
            {"regionSubCode": "57", "regionSubName": "관악구/동작구"},
            {"regionSubCode": "58", "regionSubName": "구로구/금천구/영등포구"},
            {"regionSubCode": "59", "regionSubName": "마포구/서대문구"},
            {"regionSubCode": "60", "regionSubName": "동대문구/성동구"},
            {"regionSubCode": "61", "regionSubName": "성북구/중랑구"},
            {"regionSubCode": "62", "regionSubName": "은평구"},
            {"regionSubCode": "63", "regionSubName": "종로구"},
            {"regionSubCode": "64", "regionSubName": "중구"},
            {"regionSubCode": "65", "regionSubName": "용산구"},
        ],
    },
    {
        "regionRootCode": "2",
        "regionRootName": "인천",
        "regionSubs": [{"regionSubCode": "54", "regionSubName": "인천"}],
    },
    {
        "regionRootCode": "3",
        "regionRootName": "경기",
        "regionSubs": [
            {"regionSubCode": "66", "regionSubName": "수원/화성"},
            {"regionSubCode": "67", "regionSubName": "시흥/안산"},
            {"regionSubCode": "70", "regionSubName": "고양/파주"},
            {"regionSubCode": "69", "regionSubName": "광명/부천"},
            {"regionSubCode": "71", "regionSubName": "성남/용인/하남"},
            {"regionSubCode": "68", "regionSubName": "안양/군포/의왕"},
            {"regionSubCode": "72", "regionSubName": "오산/안성/평택"},
            {"regionSubCode": "73", "regionSubName": "남양주/구리"},
            {"regionSubCode": "74", "regionSubName": "여주/이천"},
            {"regionSubCode": "75", "regionSubName": "의정부"},
            {"regionSubCode": "76", "regionSubName": "김포"},
            {"regionSubCode": "77", "regionSubName": "동두천/양주"},
            {"regionSubCode": "78", "regionSubName": "광주"},
        ],
    },
    {
        "regionRootCode": "4",
        "regionRootName": "대전",
        "regionSubs": [{"regionSubCode": "47", "regionSubName": "대전"}],
    },
    {
        "regionRootCode": "5",
        "regionRootName": "충청",
        "regionSubs": [{"regionSubCode": "48", "regionSubName": "충청"}],
    },
    {
        "regionRootCode": "6",
        "regionRootName": "강원",
        "regionSubs": [{"regionSubCode": "49", "regionSubName": "강원"}],
    },
    {
        "regionRootCode": "7",
        "regionRootName": "광주",
        "regionSubs": [{"regionSubCode": "50", "regionSubName": "광주"}],
    },
    {
        "regionRootCode": "8",
        "regionRootName": "전라",
        "regionSubs": [{"regionSubCode": "24", "regionSubName": "전라"}],
    },
    {
        "regionRootCode": "9",
        "regionRootName": "부산",
        "regionSubs": [
            {"regionSubCode": "26", "regionSubName": "금정구"},
            {"regionSubCode": "27", "regionSubName": "남구"},
            {"regionSubCode": "28", "regionSubName": "동래구"},
            {"regionSubCode": "29", "regionSubName": "부산진구"},
            {"regionSubCode": "30", "regionSubName": "북구"},
            {"regionSubCode": "31", "regionSubName": "사상구"},
            {"regionSubCode": "32", "regionSubName": "연제구"},
            {"regionSubCode": "33", "regionSubName": "중구"},
            {"regionSubCode": "34", "regionSubName": "해운대구"},
            {"regionSubCode": "79", "regionSubName": "기장군"},
            {"regionSubCode": "80", "regionSubName": "사하구"},
            {"regionSubCode": "81", "regionSubName": "강서구"},
        ],
    },
    {
        "regionRootCode": "10",
        "regionRootName": "대구",
        "regionSubs": [{"regionSubCode": "51", "regionSubName": "대구"}],
    },
    {
        "regionRootCode": "11",
        "regionRootName": "경상",
        "regionSubs": [
            {"regionSubCode": "35", "regionSubName": "거제/통영"},
            {"regionSubCode": "36", "regionSubName": "거창"},
            {"regionSubCode": "37", "regionSubName": "김해/양산"},
            {"regionSubCode": "38", "regionSubName": "창원/마산"},
            {"regionSubCode": "39", "regionSubName": "밀양"},
            {"regionSubCode": "40", "regionSubName": "진주"},
            {"regionSubCode": "41", "regionSubName": "경산"},
            {"regionSubCode": "42", "regionSubName": "경주/포항"},
            {"regionSubCode": "43", "regionSubName": "구미/김천"},
            {"regionSubCode": "44", "regionSubName": "안동"},
            {"regionSubCode": "45", "regionSubName": "울산"},
        ],
    },
    {
        "regionRootCode": "12",
        "regionRootName": "제주",
        "regionSubs": [{"regionSubCode": "52", "regionSubName": "제주"}],
    },
]

db.regions.delete_many({})

for region in regions:
    db.regions.insert_one(region)
