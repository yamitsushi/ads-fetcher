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
    
    def is_token_valid(self):
        if not hasattr(self, "_token"):
            raise ValueError("Token is not set")
        url = "/".join([self._graph_url, self._graph_version, "me"])
        validity = self._api.get(link=url, parameters={"access_token": self._token})
        if validity.status_code == 200:
            return True
        return False

    def get_insight(self, since=None, until=None):
        if not hasattr(self, "_account"):
            raise ValueError("Account is not set")
        if not hasattr(self, "_level"):
            raise ValueError("Level is not set")
        if not hasattr(self, "_token"):
            raise ValueError("Token is not set")
        if not hasattr(self, "_field"):
            raise ValueError("Field is not set")
        if since is None or until is None:
            raise ValueError("Must have the Key since and until")
        if type(since) is not str or type(until) is not str:
            raise TypeError("Key since and until must be a string")
        url = "/".join([self._graph_url, self._graph_version, self._account, "insights"])
        return self._api.get(link=url, parameters={
        "access_token": self._token, 
        "fields": self._field,
        "time_range": str({"since": since, "until": until}),
        "level": self._level
        })
