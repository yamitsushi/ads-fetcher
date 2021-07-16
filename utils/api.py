import requests

class Api:
    def get(self, uri, parameters):
        return requests.get(self.build(uri, parameters))
    
    def build(self, uri, parameters):
        return uri + "?" + "&".join(self.parse_parameters(parameters))

    def parse_parameters(self, parameters):
        keys = []
        for key, value in parameters.items():
            keys.append(key + "=" + value)
        return keys
