from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from pymongo.collation import Collation

app = Flask(__name__)

client = MongoClient("localhost", 27017)
db = client.dbspartatoyprojcet


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


# 지역정보전체를 가져오는 API
@app.route("/regionRoots", methods=["GET"])
def get_all_reionRoots():
    regionRoots = list(
        db.regions.find({}, {"_id": False})
        .sort("regionRootCode", 1)
        .collation(Collation(locale="en_US", numericOrdering=True))
    )
    return jsonify({"regionRoots": regionRoots})


# 특정 상위지역과 그 하위지역을 가져오는 API
@app.route("/regionRoots/<regionRootCode>", methods=["GET"])
def get_regionRoot(regionRootCode):
    region_root = db.regions.find_one(
        {"regionRootCode": str(regionRootCode)},
        {"_id": False},
        sort=[("regionSub.regionSubCode", 1)],
    )

    return jsonify({"regionRoot": region_root})


@app.route("/test", methods=["GET"])
def test_get():
    title_receive = request.args.get("title_give")
    print(title_receive)
    return jsonify({"result": "success", "msg": "이 요청은 GET!"})


@app.route("/test", methods=["POST"])
def test_post():
    title_receive = request.form["title_give"]
    print(title_receive)
    return jsonify({"result": "success", "msg": "이 요청은 POST!"})


if __name__ == "__main__":
    app.run("0.0.0.0", port=5001, debug=True)
