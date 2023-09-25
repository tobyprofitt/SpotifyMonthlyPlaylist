# Shows the top tracks for a user

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pprint as pp

scope = 'user-library-read'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, redirect_uri='http://localhost:7777/callback'))
token = SpotifyOAuth.get_access_token()


def main():
    res1 = sp.current_user_saved_albums(limit=50)
    res2 = sp.current_user_saved_albums(limit=50, offset=50)
    res3 = []
    res4 = []

    for i in range(50):
        artist = res1['items'][i]['album']['artists'][0]['name']
        album = res1['items'][i]['album']['name']
        aid = res1['items'][i]['album']['id']
        artist_id = res1['items'][i]['album']['artists'][0]['id']
        res3.append([artist, artist_id, album, aid])
        res4.append(artist_id)

    for i in range(50):
        artist = res2['items'][i]['album']['artists'][0]['name']
        album = res2['items'][i]['album']['name']
        aid = res2['items'][i]['album']['id']
        artist_id = res2['items'][i]['album']['artists'][0]['id']
        res3.append([artist, artist_id, album, aid])
        res4.append(artist_id)
    pp.pprint(res4)

    scope2 = 'user-follow-modify'
    sp2 = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope2, redirect_uri='http://localhost:7777/callback'))
    sp2.user_follow_artists(res4[0:50])
    sp2.user_follow_artists(res4[50:])


if __name__ == "__main__":
    main()
