# metaxe.api - communicates with the meta XE API

import requests

class Error(Exception):
    """API error base class"""

class AuthError(Error):
    """Not authorized"""

class NotFoundError(Error):
    """Entry not found"""

class Client(object):
    def __init__(self, app):
        self.client_id = app.config['CLIENT_ID']
        self.client_secret = app.config['CLIENT_SECRET']

        self.api_endpoint = app.config['API_ENDPOINT']
        self.token_endpoint = app.config['TOKEN_ENDPOINT']

    def search(self, q="", version="", instance="", page=1):
        """Get the value corresponding to a given SSN.

        Exceptions:
            api.Error
            api.AuthError
            api.NotFoundError
            requests.exceptions.RequestException
        """

        access_token = self._get_access_token()
        payload = {
            'q': q,
            'version': version,
            'instance': instance,
            'page[number]': page,
            'page[size]': 20,
        }
        headers = {'Authorization': "Bearer "+access_token}
        response = requests.get(self.api_endpoint, params=payload, headers=headers)

        if response.status_code == 401:
            raise AuthError('not authorized')
        elif response.status_code == 404:
            raise NotFoundError('entry not found')
        elif response.status_code != 200:
            raise Error('HTTP error')

        try:
            obj = response.json()
        except (ValueError, KeyError):
            raise Error("couldn't decode json")

        return obj

    def _get_access_token(self):
        if self.token_endpoint is None:
            return ''
        payload = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'client_credentials',
        }
        response = requests.post(self.token_endpoint, data=payload)
        if response.status_code == 401:
            raise AuthError("couldn't get access token")
        elif response.status_code != 200:
            raise Error('HTTP error')

        try:
            obj = response.json()
            obj['token_type']
            obj['access_token']
        except (ValueError, KeyError):
            raise Error("couldn't decode json")

        # FIXME: Remove BearerToken when apigee correctly returns Bearer
        if obj['token_type'] not in( 'Bearer', 'BearerToken' ):
            raise AuthError('invalid token type')

        return obj['access_token']
