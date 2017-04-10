from redis import Redis
from flask import Flask, request, render_template, jsonify
import rq
from rq.job import Job
from fetch_data import fetch_data
from celery_config import app
from celery.result import AsyncResult

# Initialize application
flask_app = Flask(__name__)

# Set up a Redis connection
redis = Redis()

# Initialize queue based on redis connection
queue = rq.Queue(connection=redis)

jobs = []

@flask_app.route('/status/<job_id>', methods=['GET'])
def get_status(job_id):
    """ Returns status of job with id of job_id.
        If job_id doesn't exist, status of it will be 'PENDING'
    """
    job = fetch_data.AsyncResult(job_id, app=app)
    return jsonify({'job_id': job_id, 'status': job.status})

@flask_app.route('/results/<job_id>', methods=['GET'])
def view_result(job_id):
    """ Returns the results of the job with id of job_id if the job was successful.
    """
    job = fetch_data.AsyncResult(job_id, app=app)
    if job.successful():
        result = job.result
        return jsonify({'job_id': job_id, 'result': job.result})
    else:
        result = 'job was not finished or was not successful'
    return jsonify({'job_id': job_id, 'result': result})

@flask_app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        job = fetch_data.delay(url)
        jobs.append(job.id)
    return render_template('index.html', jobs=jobs)

if __name__ == '__main__':
    flask_app.run(debug=True)
