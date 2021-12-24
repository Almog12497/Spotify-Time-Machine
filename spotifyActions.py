import spotipy
from pprint import pprint
import os
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv("CLIENT_ID"),
                                                client_secret=os.getenv("CLIENT_SECRET"),
                                                redirect_uri=os.getenv("URI"),
                                                scope="playlist-modify-public,playlist-modify-private"))

class SpotifyMachine():

    def __init__(self,songs,date):
        self.songs = songs
        self.songs_ids = []
        self.date = date

    #Gets user's id
    def me(self):
        return sp.me()["id"]

    #Finds all the songs's ids
    def search(self):
        for song in self.songs:
            track = sp.search(f'track:{song} year:{self.date.split("-")[0]}', limit=1,type="track")["tracks"]["items"]
            if track != [] : self.songs_ids.append(track[0]["id"])
        return self.songs_ids

    #Gets users playlists
    def get_playlists(self):
        return sp.current_user_playlists()

    #Gets an id of a playlist
    def get_playlist_id(self,playlist_name):
        playlists_json = self.get_playlists()["items"]
        for playlist in playlists_json:
            if playlist_name == playlist['name']:
                return playlist['id']
    
    #Adds songs to playlist
    def add_songs(self,playlist_id,tracks):
        sp.user_playlist_add_tracks(self.me(),playlist_id,tracks)

    #Creates a new playlist
    def create_playlist(self):
        try:
            if self.songs_ids == []:
                raise BaseException("invalid list")
            self.playlist_name =  f'{self.date} Top 100'
            sp.user_playlist_create(self.me(),self.playlist_name, public=True, description="Top songs from said time period!")
            return self.playlist_name
            
        except BaseException:
            print("Please use the search method before attempting to create a playlist.")

    #Creates a top 100 songs playlist.
    def create_top_100(self):
        songs_ids = self.search()
        playlist_name = self.create_playlist()
        playlist_id = self.get_playlist_id(playlist_name)
        self.add_songs(playlist_id,songs_ids)

if __name__ == '__main__':
    machine = SpotifyMachine(['Incomplete', 'Bent', "It's Gonna Be Me"],"2000-08-12")
    machine.create_top_100()