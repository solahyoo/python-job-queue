from celery_config import app
import requests

@app.task
def fetch_data(url):
    """ Fetches and returns data from URL. """
    try:
        response = requests.get(url).text
    except:
        response = {"error": "unable to get url"}

    return response
