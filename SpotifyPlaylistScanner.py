#import useful libraries
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
from pprint import pprint
import pandas as pd

scope = "user-library-read"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

#define functions
#the following function takes a playlist id and returns a dataframe with essential information
def tracks_in_playlist(playlist_id):
    df_pl = pd.DataFrame(columns = ['track_number','track_name','track_artists','uri'])
    playlist = sp.playlist_items(playlist_id)
    for i,item in enumerate(playlist['items']):
        #still need to grab all the artists right now I only grab the first listed on the track
        track_number = i
        track_name = item['track']['name']
        track_artist = item['track']['artists'][0]['name']
        track_uri = item['track']['uri']

        df_pl = pd.concat([df_pl,pd.DataFrame.from_records([{'track_number':track_number,
                        'track_name':track_name,
                        'track_artists':track_artist,
                        'uri':track_uri}])])
        # df_pl.iloc[i]['track_number'] = track_number
        # df_pl.iloc[i]['track_name'] = track_name
        # df_pl.iloc[i]['track_artists'] = track_artist
        # df_pl.iloc[i]['uri'] = track_uri

        # print("track_number: %d --- track_name: %s --- track_artist: %s --- track_id: %s" % (i,track_name,track_artist,track_uri))
    return df_pl

#the following function takes a user and returns dataframe with playlist information
def playlists_from_user(sp):
    df_pls = pd.DataFrame(columns = ['playlist_number','playlist_name','playlist_length','uri'])
    #grab user playlist data. return type dict
    user_playlists = sp.current_user_playlists()
    #print list of user_playlists
    for i, item in enumerate(user_playlists['items']):
        pl_number = i
        pl_name = item['name']
        pl_length = item['tracks']['total']
        pl_uri = item['uri']

        #add to dataframe
        df_pls = pd.concat([df_pls, pd.DataFrame.from_records([{'playlist_number':pl_number,
                                                                'playlist_name':pl_name,
                                                                'playlist_length':i,
                                                                'uri':pl_uri}])])
        # print("pl_number: %d --- pl_name:%s --- pl_id:%s --- pl_length:%s" % (pl_number, pl_name, pl_uri,pl_length))
    return df_pls

#this function will take a dataframe of playlist data and return data frame with playlists containing an input word
def playlist_containing(df_pls, word = ''):
    new_df = df_pls[df_pls['playlist_name'].str.contains(word, case=False, na=False)]
    return new_df



#to see the structure of the dict
# one_playlist = sp.current_user_playlists(limit=1)
# pretty = json.dumps(one_playlist, indent=4, sort_keys=True)
# print(pretty)

#get playlists_from_user
df_user_playlists = playlists_from_user(sp)
print(df_user_playlists)
# #get tracks
# pl_id = 'spotify:playlist:5OTsR8IJOfnRxZOsOvo4SC'
# df_playlist_tracks = tracks_in_playlist(pl_id)
# print(df_playlist_tracks.head())

#grab all playlists containing the word leah
df_leah = playlist_containing(df_user_playlists, word = 'Leah')
print(df_leah)
