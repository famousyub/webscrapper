import os
import sys

from flask import Flask, request
from flask_restful import Api
from werkzeug.utils import secure_filename
#import py_eureka_client.eureka_client as eureka_client
from flask import jsonify

sys.path.insert(1, '/parser/resumeparse.py')
sys.path.insert(1, '/matcher/candidate_matcher.py')
sys.path.insert(1,'/matcher/job_matcher.py')
from parserr.resumeparse import resumeparse
from matcher.candidate_matcher import recommend_candidates
from matcher.job_matcher import recommend_jobs
app = Flask(__name__)
api = Api(app)


@app.route('/api/users', methods=['POST', 'GET'])
def users():
    file = request.files["file"]
    if file.filename == "":
        return "No file selected"
    filename = secure_filename(file.filename)
    file.save("./" + filename)
    data = resumeparse.read_file(filename)
    os.remove(filename)
    return data


@app.route('/api/recommend/<int:job_id>/<int:number_of_candidates>', methods=['GET'])
def recommend_candidates_for_job(job_id, number_of_candidates):
    return jsonify(recommend_candidates(job_id, number_of_candidates))


@app.route('/api/recommend_job/<int:candidate_id>/<int:number_of_jobs>', methods=['GET'])
def recommend_jobs_for_candidates(candidate_id, number_of_jobs):
    return jsonify(recommend_jobs(candidate_id, number_of_jobs))


if __name__ == "__main__":
    app.run(port=6000, host='0.0.0.0')
