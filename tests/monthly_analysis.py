# Shows the top tracks for a user

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pprint as pp

client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def get_playlist_ids(user):
    playlists = sp.user_playlists(user)
    pids = []
    for playlist in playlists['items']:
        name_list = playlist['name'].split(' ')
        if len(name_list) == 1:
            continue
        if name_list[-1] in '20202019':
            pids.append(playlist['id'])
    return pids


def get_playlist_tids(playlist):
    results = sp.playlist(playlist)
    n = results['tracks']['total']
    tids = []
    for i in range(n):
        tids.append(results['tracks']['items'][i]['track']['id'])
    return tids


def get_track_analysis(tid):
    return sp.audio_analysis(tid)


def main():
    user = '12102731566'
    pids = get_playlist_ids(user)
    all_tids = []
    for pid in pids:
        all_tids.append(get_playlist_tids(pid))
    res = get_track_analysis(all_tids[0][0])
    pp.pprint(res)
    

if __name__ == "__main__":
    main()
