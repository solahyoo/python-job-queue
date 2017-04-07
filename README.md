# Massdrop
### Task:
Create a job queue whose workers fetch data from a URL and store the results in a database.  The job queue should expose a REST API for adding jobs and checking their status / results.

Example:
User submits www.google.com to your endpoint.  The user gets back a job id. Your system fetches www.google.com (the result of which would be HTML) and stores the result.  The user asks for the status of the job id and if the job is complete, he gets a response that includes the HTML for www.google.com

### My Implementation
I decided to use Python 2.7 and its frameworks and libraries (Flask, Redis, and RQ) to implement the job queue.
(I ran this on Unix so I'm not sure if this will run the same on a Mac or Windows).
To run this program, make sure you have all the modules installed. Then, on the terminal, start the Redis Server by running:
```
redis-server
```
And start the RQ worker and the program:
```
rq worker
python app.py
```
Finally, go to `http://localhost:5000/` on your browser and submit your URL.

Once you submit a URL, you can click on the job ids below "Job Status" to view job status and job ids below "Job Results" to view the response from the url.

If the url is invalid (ie. www.google.com vs https://www.google.com), the result will show the error message. 
