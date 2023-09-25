import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def lambda_handler(event, context):
    # Extract input from HTTP request
    body = json.loads(event.get('body', '{}'))
    playlist_title = body.get('playlist_title', 'Monthly Top 20')
    playlist_desc = body.get('playlist_description', 'My top 20 tracks from the last 4 weeks.')

    # Spotify setup
    scope = 'playlist-modify-public'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,
                                                   redirect_uri='YOUR_REDIRECT_URI_HERE'))

    # Create playlist
    user_id = sp.me()['id']
    sp.user_playlist_create(user=user_id, name=playlist_title, description=playlist_desc)

    # Change scope of sp to fetch top tracks
    scope = 'user-top-read'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,
                                                   redirect_uri='YOUR_REDIRECT_URI_HERE'))

    # Get top 20 tracks
    results = sp.current_user_top_tracks(time_range='short_term', limit=20)
    tids = [item['uri'] for item in results['items']]

    # Get latest playlist ID (should be the one just created)
    playlist_id = sp.current_user_playlists()['items'][0]['id']

    # Add tracks to the new playlist
    scope = 'playlist-modify-public'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,
                                                   redirect_uri='YOUR_REDIRECT_URI_HERE'))
    sp.playlist_add_items(playlist_id, tids)

    # Return a success response
    response = {
        'statusCode': 200,
        'body': json.dumps({'message': 'Playlist created successfully!'}),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'  # Allow CORS
        }
    }
    return response