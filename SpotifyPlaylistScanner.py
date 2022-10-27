#import useful libraries
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
from pprint import pprint

scope = "user-library-read"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

#grab user playlist data. return type dict
user_playlists = sp.current_user_playlists()
#print list of user_playlists
for i, item in enumerate(user_playlists['items']):
    print("number: %d --- name:%s --- id:%s --- length:%s" % (i, item['name'], item['uri'],item['tracks']['total']))

one_playlist = sp.current_user_playlists(limit=1)
#to see the structure of the dict
# pretty = json.dumps(one_playlist, indent=4, sort_keys=True)
# print(pretty)

#get tracks
pl_id = 'spotify:playlist:5OTsR8IJOfnRxZOsOvo4SC'
playlist = sp.playlist_items(pl_id)
for i,item in enumerate(playlist['items']):
    #still need to grab all the artists right now I only grab the first listed on the track
    print("%d - %s by %s" % (i,item['track']['name'],item['track']['artists'][0]['name']))
