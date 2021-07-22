import requests
import validators

class Api:
    def get(self, link=None, parameters=None):
        link = self.check_url(link)

        if parameters is None:
            return requests.get(link)

        if type(parameters) is not dict:
            raise TypeError("The parameter must be a dictionary")

        return requests.get(link, parameters)
    
    def build(self, link = None, parameters = None):
        link = self.check_url(link)

        if parameters is None:
            return link

        return link + "?" + self.parse_parameters(parameters)

    def parse_parameters(self, parameters):
        if type(parameters) is not dict:
            raise TypeError("The parameter must be a dictionary")

        keys = []
        for key, value in parameters.items():
            keys.append(key + "=" + value)

        return "&".join(keys)

    def check_url(self, link):
        if type(link) is not str:
            raise TypeError("The link must be a string")
        if not validators.url(link):
            raise ValueError("The link must be a valid URL")

        return link
