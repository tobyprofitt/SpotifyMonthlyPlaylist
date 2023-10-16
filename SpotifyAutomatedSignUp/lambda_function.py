import boto3
import requests
import json
import os
import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('SpotifyUsers')

SPOTIPY_CLIENT_ID =     os.environ['SPOTIPY_CLIENT_ID']
SPOTIPY_CLIENT_SECRET = os.environ['SPOTIPY_CLIENT_SECRET']
SPOTIPY_REDIRECT_URI =  os.environ['SPOTIPY_REDIRECT_URI']

SPOTIFY_TOKEN_ENDPOINT = 'https://accounts.spotify.com/api/token'
SPOTIFY_PROFILE_ENDPOINT = 'https://api.spotify.com/v1/me'

def lambda_handler(event, context):
    auth_code = event['body']['code']
    
    # Request refresh token from Spotify
    response = requests.post(SPOTIFY_TOKEN_ENDPOINT, data={
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': SPOTIPY_REDIRECT_URI,
        'client_id': SPOTIPY_CLIENT_ID,
        'client_secret': SPOTIPY_CLIENT_SECRET
    })
    token_data = response.json()
    refresh_token = token_data['refresh_token']
    
    # Fetch the user's Spotify email (you'd use the access token to call Spotify's API and get the user's profile data)
    user_email = get_spotify_email(token_data['access_token'])
    
    # Store the refresh token and email in DynamoDB
    table.put_item(
        Item={
            'email': user_email,
            'refresh_token': refresh_token, 
            'is_valid': True,
            'last_updated': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Successfully signed up for monthly playlists!'})
    }

def get_spotify_email(access_token):
    headers = {'Authorization': 'Bearer ' + access_token}
    response = requests.get(SPOTIFY_PROFILE_ENDPOINT, headers=headers)
    user_data = response.json()
    return user_data['email']
