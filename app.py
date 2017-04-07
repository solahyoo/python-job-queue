import json
from redis import Redis
from flask import Flask, request, render_template, jsonify
import rq
from rq.job import Job
from fetch_data import fetch_data

# Initialize application
app = Flask(__name__)

# Set up a Redis connection
redis = Redis()

# Initialize queue based on redis connection
queue = rq.Queue(connection=redis)

jobs = []

@app.route('/status/<job_id>', methods=['GET'])
def get_status(job_id):
    try:
        job = Job.fetch(job_id, connection=redis)
    except rq.exceptions.NoSuchJobError:
        return jsonify({'job_id': job_id, 'status': 'no such jobs'})
    if job.is_finished:
        ret = {'job_id': job_id, 'status':'finished'}
    elif job.is_started:
        ret = {'job_id': job_id, 'status':'waiting'}
    elif job.is_failed:
        ret = {'job_id': job_id, 'status': 'failed'}
    elif job.is_queued:
        ret = {'job_id': job_id, 'status': 'queued'}
    return jsonify(ret)

@app.route('/results/<job_id>', methods=['GET'])
def view_result(job_id):
    try:
        job = Job.fetch(job_id, connection=redis)
    except rq.exceptions.NoSuchJobError:
        return jsonify({'result': 'no such jobs: ' + job_id})
    if job.is_finished:
        return jsonify({'result': job.return_value})
    else:
        return jsonify({'result': 'job not finished'})

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        job = queue.enqueue(fetch_data, args=(url,))
        jobs.append(job.get_id())
    return render_template('index.html', jobs=jobs)

if __name__ == '__main__':
    app.run(debug=True)
