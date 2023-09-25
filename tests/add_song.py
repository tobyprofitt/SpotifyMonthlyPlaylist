# Shows the top tracks for a user

import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = 'user-library-modify'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,
                                               redirect_uri='http://localhost:7777/callback'))

track_id = ['spotify:track:7wGNuuEBhDhSUOBFzsDvUs']
sp.current_user_saved_tracks_add(tracks=track_id)
print('Current user: ' + str(sp.current_user()))
print("Done")
