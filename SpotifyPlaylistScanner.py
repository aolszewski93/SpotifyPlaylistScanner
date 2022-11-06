#import useful libraries
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
from pprint import pprint
import pandas as pd

scope = "playlist-modify-public"
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
        # print("track_number: %d --- track_name: %s --- track_artist: %s --- track_id: %s" % (i,track_name,track_artist,track_uri))
    return df_pl

#the following function takes a user and returns dataframe with playlist information from newest to oldest
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
                                                                'playlist_length':pl_length,
                                                                'uri':pl_uri}])])
        # print("pl_number: %d --- pl_name:%s --- pl_id:%s --- pl_length:%s" % (pl_number, pl_name, pl_uri,pl_length))
    return df_pls

#this function will take a dataframe of playlist data and return data frame with playlists containing an input word
def playlist_containing(df_pls, word = ''):
    new_df = df_pls[df_pls['playlist_name'].str.contains(word, case=False, na=False)]
    return new_df

#this function will find duplicates from old playlists to new and remove the track from the newest playlists
def compile_pl_tracks(df_pls, newest=True):
    # pl_uris = df_pls['uri']
    #create a dataframe with a compiled track list of all the playlists_from_user
    df_pl_tracks = pd.DataFrame(columns = ['playlist_number','playlist_name','playlist_uri','track_name','track_artists','track_uri'])
    for i,row_pl in df_pls.iterrows():
        df_tracks = tracks_in_playlist(row_pl['uri'])
        for i, row_track in df_tracks.iterrows():
            df_pl_tracks = pd.concat([df_pl_tracks, pd.DataFrame.from_records([{'playlist_number': row_pl['playlist_number'],
                                                                            'playlist_name': row_pl['playlist_name'],
                                                                            'playlist_uri': row_pl['uri'],
                                                                            'track_name': row_track['track_name'],
                                                                            'track_artists': row_track['track_artists'],
                                                                            'track_uri': row_track['uri']}])])
    return df_pl_tracks

def remove_duplicate_tracks(sp, df_pl_tr):
    #reverse the order of playlists so that the oldest playlist apears first in the dataframe
    df_pl_tr.sort_values(by=['playlist_number'], ascending=False, inplace = True)
    #add column that states if the track was previously found in the dataframe
    df_pl_tr['duplicate'] = df_pl_tr['track_uri'].duplicated()

    if all(item is False for item in df_pl_tr['duplicate']):
        print('There are no duplicates in playlists...')
    else:
        #make a subset of the data frame that contains infor of all duplicate tracks_in_playlist
        df_rm = df_pl_tr[df_pl_tr['duplicate']==True]
        print(df_rm)
        #remove all duplicate tracks_in_playlist
        for i, row in df_rm.iterrows():
            remove_track = [row['track_uri'].split(':')[-1]]
            from_pl = row['playlist_uri'].split(':')[-1]
            print(remove_track, from_pl)
            sp.playlist_remove_all_occurrences_of_items(playlist_id = from_pl, items = remove_track)
            print("%s by %s was removed from %s" % (row['track_name'], row['track_artists'], row['playlist_name']))

# # to see the structure of the dict
# one_playlist = sp.current_user_playlists(limit=3)
# pretty = json.dumps(one_playlist, indent=4, sort_keys=True)
# print(pretty)

#get playlists_from_user
df_user_playlists = playlists_from_user(sp)

#grab all playlists containing the word leah
df_leah = playlist_containing(df_user_playlists, word = 'Leah')

df_compiled = compile_pl_tracks(df_leah)

remove_duplicate_tracks(sp, df_compiled)
