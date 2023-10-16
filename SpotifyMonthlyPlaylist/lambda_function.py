import json
import spotipy
import requests
from spotipy.oauth2 import SpotifyOAuth
import os

SPOTIPY_CLIENT_ID =     os.environ['SPOTIPY_CLIENT_ID']
SPOTIPY_CLIENT_SECRET = os.environ['SPOTIPY_CLIENT_SECRET']
SPOTIPY_REDIRECT_URI =  os.environ['SPOTIPY_REDIRECT_URI']

def lambda_handler(event, context):

    # Spotify setup
    scope = 'playlist-modify-public'

    # Parse the body from the event into a Python dictionary
    body = json.loads(event['body'])
    playlist_title = body.get('playlist_title', 'Monthly Top 20')
    playlist_desc = body.get('playlist_description', 'My top 20 tracks from the last 4 weeks.')

    # Extract the authorization code from the parsed body
    code = body['code']

    # Exchange the authorization code for an access token
    token_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': SPOTIPY_REDIRECT_URI,
        'client_id': SPOTIPY_CLIENT_ID,
        'client_secret': SPOTIPY_CLIENT_SECRET
    }

    response = requests.post('https://accounts.spotify.com/api/token', data=token_data)

    print(f'Response: {response.json()}')

    token_info = response.json()

    # Check if the response contains an error or if the access_token key is missing
    if 'error' in token_info or 'access_token' not in token_info:
        print(f"Error during token exchange: {token_info}")
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Error during token exchange.'})
        }
    
    access_token = token_info['access_token']

    # Use the access token to create an authenticated Spotipy client
    sp = spotipy.Spotify(auth=access_token)

    # Create playlist
    user_id = sp.me()['id']
    print(1)
    playlist = sp.user_playlist_create(user=user_id, name=playlist_title, description=playlist_desc)

    # Get top 20 tracks
    print(2)
    results = sp.current_user_top_tracks(time_range='short_term', limit=20)
    print(3)
    tids = [item['uri'] for item in results['items']]
    print(4)
    for item in results['items']:
        print(item)
    print(5)

    # Add tracks to the playlist
    sp.user_playlist_add_tracks(user=user_id, playlist_id=playlist['id'], tracks=tids)
    print(6)

    # Return the playlist URL and top 20 songs
    response_body = {
        'songs': results['items'],
        'playlist_link': playlist['external_urls']['spotify']
    }

    return {
    'statusCode': 200,
    'headers': {
        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
    },
    'body': json.dumps(response_body)
}

