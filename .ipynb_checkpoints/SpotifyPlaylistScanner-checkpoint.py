#import useful libraries
import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = "user-library-read"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

user_playlists = sp.current_user_playlists()
print(user_playlists)
