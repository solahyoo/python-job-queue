# Massdrop
### Task:
Create a job queue whose workers fetch data from a URL and store the results in a database.  The job queue should expose a REST API for adding jobs and checking their status / results.

Example:
User submits www.google.com to your endpoint.  The user gets back a job id. Your system fetches www.google.com (the result of which would be HTML) and stores the result.  The user asks for the status of the job id and if the job is complete, he gets a response that includes the HTML for www.google.com

### My Implementation
I decided to use Python 3.5 and its frameworks and libraries (Flask, Redis, and Celery) to implement the job queue.

(I ran this on Unix so I'm not sure if this will run the same on a Mac or Windows).

To run this program, make sure you have all the modules listed above installed. Then, on the terminal, start the Redis Server by running:
```
redis-server
```
And start the Celery worker and the program:
```
celery -A fetch_data worker --loglevel=info
python app.py
```
Finally, go to `http://localhost:5000/` on your browser and submit your URL.

Once you submit a URL, you can click on the job ids below "Recent Job Statuses" to view job status and job ids below "Recent Job Results" to view the response from the url.

If the url is invalid (ie. www.google.com vs https://www.google.com), the result will show the error message.

### Updated
When I first implemented it, I forgot the part about storing the results into the database so my first implementation did not do that. And the RQ jobs would expire after a certain amount of time had passed.

So instead, I decided to use Celery for the job queue because Celery automatically stores all results in the Redis server if you provide a backend argument for it. And it made the code a little cleaner, too.
