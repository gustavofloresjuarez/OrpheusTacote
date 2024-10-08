import time
from utils.utils import hash_string, create_requests_session

class Qobuz:
    def __init__(self, app_id: str, app_secret: str, auth_with_token: bool, exception):
        self.api_base = 'https://www.qobuz.com/api.json/0.2/'
        self.app_id = app_id
        self.app_secret = app_secret
        self.auth_token = None
        self.exception = exception
        self.s = create_requests_session()
        self.auth_with_token = auth_with_token

    def headers(self):
        headers = {
            'X-Device-Platform': 'Android',
            'X-Device-Model': 'Pixel 7',
            'X-Device-Os-Version': '13',
            'X-User-Auth-Token': self.auth_token if self.auth_token else None,
            'X-Device-Manufacturer-Id': '482D8CB7-015D-402F-A93B-5EEF0E0996F3',
            'X-App-Version': '7.4.0.0',
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 13; Pixel 7 Build/TQ2A.230505.002.A1)) QobuzMobileAndroid/7.4.0.0'
        }
        return headers

    def _get(self, url: str, params=None):
        if params is None:
            params = {}

        response = self.s.get(f'{self.api_base}{url}', params=params, headers=self.headers())

        if response.status_code not in [200, 201, 202]:
            raise self.exception(response.text)

        return response.json()

    def _prepare_login_params(self, username_or_UserID: str, password_or_Token: str):
        if not username_or_UserID or not password_or_Token:
            raise self.exception('Invalid username_or_UserID/password_or_Token')

        if self.auth_with_token:
            return {
                'user_id': username_or_UserID,
                'user_auth_token': password_or_Token,
                'extra': 'partner',
                'app_id': self.app_id
            }
        else:
            return {
                'username': username_or_UserID,
                'password': password_or_Token,
                'extra': 'partner',
                'app_id': self.app_id
            }

    def login(self, username_or_UserID: str, password_or_Token: str):
        params = self._prepare_login_params(username_or_UserID, password_or_Token)

        signature = self.create_signature('user/login', params)
        params.update({
            'request_ts': signature[0],
            'request_sig': signature[1]
        })

        response = self._get('user/login', params)

        if 'user_auth_token' in response and 'credential' in response['user']:
            self.auth_token = response['user_auth_token']
            credential_params = response['user']['credential'].get('parameters')
            if credential_params:
                print('Account Plan:', credential_params['label'])
            else:
                print('Account Plan:', response['user']['credential']['description'])
                raise self.exception("Free accounts are not eligible for downloading")
            
            print('Country:', response['user']['country'])
            print('Periodicity:', response['user']['subscription']['periodicity'])
            print('Expiration:', response['user']['subscription']['end_date'])
            print('Renewal:', not response['user']['subscription']['is_canceled'])
        else:
            raise self.exception('Invalid username_or_UserID/password_or_Token')

        return response['user_auth_token']

    def check_subscription(self, username_or_UserID: str, password_or_Token: str):
        params = self._prepare_login_params(username_or_UserID, password_or_Token)

        signature = self.create_signature('user/login', params)
        params.update({
            'request_ts': signature[0],
            'request_sig': signature[1]
        })

        response = self._get('user/login', params)

        if 'user_auth_token' in response and 'credential' in response['user']:
            credential_params = response['user']['credential'].get('parameters')
            if credential_params:
                print('Account Plan:', credential_params['label'])
            else:
                print('Account Plan:', response['user']['credential']['description'])
                raise self.exception("Free accounts are not eligible for downloading")
            
            print('Country:', response['user']['country'])
            print('Periodicity:', response['user']['subscription']['periodicity'])
            print('Expiration:', response['user']['subscription']['end_date'])
            print('Renewal:', not response['user']['subscription']['is_canceled'])
        else:
            raise self.exception('Invalid username_or_UserID/password_or_Token')

    def create_signature(self, method: str, parameters: dict):
        timestamp = str(int(time.time()))
        to_hash = method.replace('/', '')

        for key in sorted(parameters.keys()):
            if key not in ['app_id', 'user_auth_token']:
                to_hash += key + parameters[key]

        to_hash += timestamp + self.app_secret
        signature = hash_string(to_hash, 'MD5')
        return timestamp, signature

    def search(self, query_type: str, query: str, limit: int = 10):
        return self._get('catalog/search', {
            'query': query,
            'type': query_type + 's',
            'limit': limit,
            'app_id': self.app_id
        })

    def get_file_url(self, track_id: str, quality_id=27):
        params = {
            'track_id': track_id,
            'format_id': str(quality_id),
            'intent': 'stream',
            'sample': 'false',
            'app_id': self.app_id,
            'user_auth_token': self.auth_token
        }

        signature = self.create_signature('track/getFileUrl', params)
        params.update({
            'request_ts': signature[0],
            'request_sig': signature[1]
        })

        return self._get('track/getFileUrl', params)

    def get_track(self, track_id: str):
        return self._get('track/get', params={
            'track_id': track_id,
            'app_id': self.app_id
        })

    def get_playlist(self, playlist_id: str):
        return self._get('playlist/get', params={
            'playlist_id': playlist_id,
            'app_id': self.app_id,
            'limit': '2000',
            'offset': '0',
            'extra': 'tracks,subscribers,focusAll'
        })

    def get_album(self, album_id: str):
        return self._get('album/get', params={
            'album_id': album_id,
            'app_id': self.app_id,
            'extra': 'albumsFromSameArtist,focusAll'
        })

    def get_artist(self, artist_id: str):
        return self._get('artist/get', params={
            'artist_id': artist_id,
            'app_id': self.app_id,
            'extra': 'albums,playlists,tracks_appears_on,albums_with_last_release,focusAll',
            'limit': '1000',
            'offset': '0'
        })