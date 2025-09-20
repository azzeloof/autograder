import requests

class Assignment:
    def __init__(self, name, url):
        self.name = name
        self.url = url

    def __getattr__(self, function):
        def method(*args, **kwargs):
            payload = {'assignment': self.name, 'function': function, 'args': args, 'kwargs': kwargs}
            response = requests.post(self.url, json=payload)
            result = response.json()['Result']
            return result
        return method

class Autograder:
    def __init__(self, url="http://localhost:8000/evaluate/"):
        self.url = url

    def __getattr__(self, name):
        return Assignment(name, self.url)
