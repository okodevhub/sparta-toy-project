from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from pymongo.collation import Collation

app = Flask(__name__)

# client = MongoClient("localhost", 27017)
client = MongoClient("mongodb://test:test@localhost", 27017)
db = client.dbmoviemoa


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/result", methods=["GET"])
def search():
    return render_template("result.html")


@app.route("/test", methods=["GET"])
def test():
    return render_template("test.html")


# 지역정보전체를 가져오는 API
@app.route("/regions", methods=["GET"])
def get_all_reions():
    regionRoots = list(
        db.regions.find({}, {"_id": False})
        .sort("regionRootCode", 1)
        .collation(Collation(locale="en_US", numericOrdering=True))
    )
    return jsonify({"regions": regionRoots})


# 특정 상위지역과 그 하위지역을 가져오는 API
@app.route("/regions/<regionRootCode>", methods=["GET"])
def get_region(regionRootCode):
    region = db.regions.find_one(
        {"regionRootCode": str(regionRootCode)},
        {"_id": False},
        sort=[("regionSub.regionSubCode", 1)],
    )

    return jsonify({"region": region})


# top20영화 가져오는 API
@app.route("/top20movies", methods=["GET"])
def get_all_top20movies():
    movies = list(
        db.top20movies.find({}, {"detail_info": False, "_id": False}).sort("ranking", 1)
    )

    return jsonify({"movies": movies})


# 특정영화 가져오는 API
# @app.route("/top20movies/<code>", methods=["GET"])
# def get_movie(code):
#     movie = db.top20movies.find_one({"code": str(code)}, {"_id": False})
#     return jsonify({"movie": movie})


# 영화정보와 상영테이블 가져오는 API
@app.route("/api/result", methods=["GET"])
def get_timetable():
    region_root = request.args.get("region_root")
    region_sub = request.args.get("region_sub")
    code = request.args.get("code")
    hour = request.args.get("hour")

    # 영화정보 가져오기
    movie = db.top20movies.find_one({"code": str(code)}, {"_id": False})

    cgv_tables = []
    mega_tables = []
    lotte_tables = []

    timetables = list(
        db.running_time_table.find(
            {
                "code": str(code),
                "regionRootCode": str(region_root),
                "regionSubCode": str(region_sub),
            },
            {"_id": False},
        ).sort("show_time", 1)
    )

    for timetable in timetables:
        if timetable["show_time"].split(":")[0] >= hour:
            if timetable["brand"] in ("CGV"):
                cgv_tables.append(timetable)
            elif timetable["brand"] in ("메가박스"):
                mega_tables.append(timetable)
            elif timetable["brand"] in ("롯데시네마"):
                lotte_tables.append(timetable)

    return jsonify(
        {
            "movie": movie,
            "cgv_tables": cgv_tables,
            "mega_tables": mega_tables,
            "lotte_tables": lotte_tables,
        }
    )


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)
