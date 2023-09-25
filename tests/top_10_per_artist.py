# Creates a playlist of the top 20 most played song from the last 4 weeks

import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Instantiate sp
scope = 'user-top-read'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, redirect_uri='http://localhost:7777/callback'))

# Get artist
artist_name = input("Enter artist name: ")
artist_id = str(sp.search(q='artist:' + artist_name, type='artist')['artists']['items'][0]['id'])

search_count = 0
tids = []
tnames = []

while (len(tids) < 10) and search_count < 1000:
    results = sp.current_user_top_tracks(time_range='long_term', limit=1, offset=search_count)
    current_artist_id = results['items'][0]['artists'][0]['id']
    print(search_count)
    if current_artist_id == artist_id:
        tids.append(results['items'][0]['uri'])
        tnames.append(results['items'][0]['name'])
        print(str(search_count + 1) + str(results['items'][0]['name']))
    search_count += 1

# Print all the song names
for i, song in enumerate(tnames):
    print((i+1), song)

# Change scope to playlist-modify-public
scope = 'playlist-modify-public'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,
                                               redirect_uri='http://localhost:7777/callback'))

# Create playlist
playlist_title = input("Enter the playlist title: ")
playlist_desc = input("Enter the playlist description: ")
user_id = sp.me()['id']
print()
sp.user_playlist_create(user=user_id, name=playlist_title, description=playlist_desc)

# Add songs to playlist
playlist_id = sp.current_user_playlists()['items'][0]['id']
sp.playlist_add_items(playlist_id, tids)

print("\nCheck out your new playlist on Spotify now!\n")