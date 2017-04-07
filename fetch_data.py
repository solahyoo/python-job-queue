import json
import requests

def fetch_data(url):
    """ Fetches and returns data from URL. """
    try:
        response = requests.get(url)
    except:
        return {"error": "unable to get url"}

    return response.text
