import spotipy.util as util


scope = 'user-read-recently-played'
redirect_uri = 'http://localhost:7777/callback'

token = util.prompt_for_user_token(scope=scope,
                                   redirect_uri=redirect_uri)
print(token)
