from utils.api import Api

class Facebook:
    """Helper class for easier access to facebook"""

    def __init__(self, graph_url="https://graph.facebook.com", graph_version="v10.0", api=Api):
        if type(graph_url) is not str:
            raise TypeError("The url must be a string")
        self._graph_url = graph_url
        if type(graph_version) is not str:
            raise TypeError("The version must be a string")
        self._graph_version = graph_version
        if api is not Api:
            raise TypeError("The api must be valid Api")
        self._api = api()

    def set_token(self, token):
        """Setting the token of the Facebook"""
        if type(token) is not str:
            raise TypeError("Token must be a string") 
        if token == "":
            raise ValueError("Token must not be empty")
        self._token = token

    def set_account(self, account):
        """Setting the account of the Facebook API"""
        if type(account) is not str:
            raise TypeError("Account must be a string") 
        if account == "":
            raise ValueError("Account must not be empty")
        self._account = account

    def set_field(self, field):
        if type(field) is not str:
            raise TypeError("Field must be a string")
        if field == "":
            raise ValueError("Field must not be empty")
        self._field = field

    def set_level(self, level):
        if type(level) is not str:
            raise TypeError("Field must be a string")
        if level == "":
            raise ValueError("Field must not be empty")
        self._level = level
    
    def set_range(self, range):
        if type(range) is not dict:
            raise TypeError("Field must be a dictionary")
        if "since" not in range or "until" not in range:
            raise ValueError("Must have the key since and until")
        if type(range['since']) is not str:
            raise TypeError("Key Since must be a string")
        if type(range['until']) is not str:
            raise TypeError("Key Until must be a string")
        self._range = range
    
    def is_token_valid(self):
        if not hasattr(self, "_token"):
            raise ValueError("Token is not set")
        url = "/".join([self._graph_url, self._graph_version, "me"])
        validity = self._api.get(link=url, parameters={"access_token": self._token})
        if validity.status_code == 200:
            return True
        return False
            