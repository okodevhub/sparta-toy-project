from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')

## API
@app.route('/moviedetails', methods=['GET'])
def moviedetails():
    moviedetails = list(db.MovieDetails.find({},{'_id':False}))
    return jsonify({"all_details": moviedetails})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
