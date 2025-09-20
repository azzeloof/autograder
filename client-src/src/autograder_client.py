import requests
import logging

log = logging.getLogger(__name__)

class Assignment:
    def __init__(self, name, url):
        self.name = name
        self.url = url

    def __getattr__(self, function):
        def method(*args, **kwargs):
            payload = {'assignment': self.name, 'function': function, 'args': args, 'kwargs': kwargs}
            response = requests.post(self.url, json=payload)
            try:
                result = response.json()
                return result['Result']
            except Exception as e:
                log.error(f"Error: {e}")
        return method

class Autograder:
    def __init__(self, url="http://localhost/evaluate"):
        self.url = url

    def __getattr__(self, name):
        return Assignment(name, self.url)
