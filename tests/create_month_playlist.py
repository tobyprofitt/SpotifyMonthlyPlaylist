# Creates a playlist of the top 20 most played song from the last 4 weeks

import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Instantiate sp
scope = 'playlist-modify-public'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,
                                               redirect_uri='http://localhost:7777/callback'))

# Create playlist
playlist_title = input("Enter the playlist title: ")
playlist_desc = input("Enter the playlist description: ")
user_id = sp.me()['id']
print()

sp.user_playlist_create(user=user_id, name=playlist_title, description=playlist_desc)

# Change scope of sp
scope = 'user-top-read'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,
                                               redirect_uri='http://localhost:7777/callback'))

# Get tracks
results = sp.current_user_top_tracks(time_range='short_term', limit=20)
tids = []

# Print out song artist//names and get track IDs in an array
for i, item in enumerate(results['items']):
    tids.append(item['uri'])
    print((i+1), item['name'], '//', item['artists'][0]['name'])

# Get latest playlist ID (should be the one just created)
playlist_id = sp.current_user_playlists()['items'][0]['id']

# Add tracks to playlist
scope = 'playlist-modify-public'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,
                                               redirect_uri='http://localhost:7777/callback'))
sp.playlist_add_items(playlist_id, tids)
print('\nHappy listening, see you next month!\n')
