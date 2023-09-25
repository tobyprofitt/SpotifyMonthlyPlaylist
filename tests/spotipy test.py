import spotipy
import argparse
import logging

from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

"""
gizz_uri = 'spotify:artist:6XYvaoDGE0VmRt83Jss9Sn'
lz_uri = 'spotify:artist:36QJpDe2go2KgaRleHCDTp'
honey_uri = 'spotify:track:01IuTsgAlgKlgrvPhZ2c95'

print(spotify.recommendation_genre_seeds())
results = spotify.recommendations(seed_genres=('psych-rock', 'alt-rock'))
for track in results['tracks']:
    if 'AU' in track['available_markets']:
        print(track['album']['external_urls'])
        for item in track:
            print(item)
        print('-'*30)

results = spotify.artist_top_tracks(gizz_uri, country='NZ')

for track in results['tracks']:
    if not track['preview_url']:
        continue
    print('track    : ' + track['name'])
    print('audio    : ' + track['preview_url'])
    print('cover art: ' + track['album']['images'][0]['url'])
    print()
"""

logger = logging.getLogger('examples.artist_recommendations')
logging.basicConfig(level='INFO')


def get_args():
    parser = argparse.ArgumentParser(description='Recommendations for the '
                                     'given artist')
    parser.add_argument('-a', '--artist', required=True, help='Name of Artist')
    return parser.parse_args()


def get_artist(name):
    results = sp.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        return items[0]
    else:
        return None


def show_recommendations_for_artist(artist, genre):
    if not genre:
        results = sp.recommendations(seed_artists=[artist['id']])
    else:
        results = sp.recommendations(seed_artists=[artist['id']], seed_genres=[genre])
    for track in results['tracks']:
        print('Recommendation: {} - {}'.format(track['name'], track['artists'][0]['name']), end='\n')
        print('Link = ' + str(track['external_urls']['spotify']))


def show_artist_tags(name):
    artist = sp.search(q='artist:' + name, type='artist')
    print(artist['artists']['items'][0]['genres'])


def main():
    in_type = input("Do you want song recommendations or artist tags? (type 'tags' or 'genres' for the latter) ")
    if in_type.lower() in ('tags', 'genres', 'tag'):
        print("You have chosen tags")
        artist = input("What artist? ")
        show_artist_tags(artist)

    else:
        print("You have chose recommendations")
        print('Available genres:', sp.recommendation_genre_seeds())
        artist = input('What artist would you like to use as a search seed? ')
        genre = input('What genre? ')
        artist = get_artist(artist)
        if artist:
            show_recommendations_for_artist(artist, genre)
        else:
            logger.error("Can't find that artist", artist)


if __name__ == '__main__':
    main()
