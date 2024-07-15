
#* Import dotenv
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

#* Import Spotify API
import spotipy
from spotipy.oauth2 import SpotifyOAuth
# Setting for spotify API
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")


#* Import other library
from flask import url_for
import time
import logging
logging.basicConfig(filename='file.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
# logging.basicConfig(filename='filter_spotify.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

#* login route
def login():
    """Inizialize the authentication for spotify API

    Returns:
        redirect(auth_url): Redirect to an external page for the spotify's login
    """
    logging.info("Start login")
    auth_url = spotify_oauth().get_authorize_url()
    logging.debug("Link to spotify login page: " + str(auth_url))
    return auth_url 


#* The external page then redirect us to this page after you complete the login
def callback(request):
    """Extraction of the access token, which was given by the login

    Returns:
        redirect(url_for("create_playlist", external = True)): Redirect to an internal page which will execute the main task of this code
    """
    logging.info("Start callback")
    
    code = request.args.get("code")
    logging.debug("Code received from login page: " + str(code))
    
    token_info = spotify_oauth().get_access_token(code)
    logging.debug("Token info in callback: " + str(token_info))
    
    return token_info
    
#* spotify_oauth
def spotify_oauth():
    """Create an object to allow us to login into spotify and use the logged session to save the access token

    Returns:
        SpotifyOAuth(...): An object of the library "spotipy", composed by 
                           the client id;
                           the "password" (client secret);
                           the redirect uri, which is where the external authorize url will redirect us after the login;
                           the scope, which is the action we can perform with the logged spotify account 
    """
    return SpotifyOAuth(
        client_id = CLIENT_ID,
        client_secret = CLIENT_SECRET,
        # redirect_uri = url_for("callback", _external=True),
        redirect_uri = "http://127.0.0.1:5000/callback",
        scope = "playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public"
    )
    
def check_if_playlist(uri):
    uri_splitted = uri.split(":")
    logging.debug("Uri passato dal giocatore: " + str(uri_splitted))
    
    if (uri_splitted[0]=="spotify" and (uri_splitted[1]=="playlist" or uri_splitted[1]=="album")):
        return True
    else:
        return False
            
        
def get_playlist(token, uri):
    uri_splitted = uri.split(":")
    logging.debug("Uri passato dal giocatore: " + str(uri_splitted))
    
    type = uri_splitted[1]
    id = uri_splitted[2]
    
    spotify = spotipy.Spotify(auth=token["access_token"])
    if (type=="playlist"):
        filter = "next, items.track.artists.name, items.track.name"
        playlist = spotify.playlist_items(id, fields=filter)
        
        while True:
            items = playlist["items"]
            
            songs = playlist_to_list(items)
                    
            next = {"next": playlist["next"]}
            logging.debug("Next: " + str(next))
            if(next["next"] == None):
                logging.info("No more pages")
                break
            else:
                logging.info("Another page found")
                playlist = None
                playlist = spotify.next(next)
    else:
        album = spotify.album_tracks(id, market="IT")
        
        while True:
            items = album["items"]
            
            songs = album_to_list(items)
                    
            next = {"next": album["next"]}
            logging.debug("Next: " + str(next))
            if(next["next"] == None):
                logging.info("No more pages")
                break
            else:
                logging.info("Another page found")
                playlist = None
                playlist = spotify.next(next) 
        
    logging.debug("Playlist estratta: " + str(songs))
    
# def get_song():

def refresh_token(token):
    refreshed_oauth = spotify_oauth()
    token_info = refreshed_oauth.refresh_access_token(token["refresh_token"])
    
    return token_info

def playlist_to_list(playlist):
    songs = []
    for song in playlist:
        song_name = song["track"]["name"]
        artist = song["track"]["artists"][0]["name"]
        logging.debug((song_name, artist))
        songs.append((song_name, artist))
    
    return songs

def album_to_list(album):
    songs = []
    for song in album:
        song_name = song["name"]
        artist = song["artists"][0]["name"]
        logging.debug((song_name, artist))
        songs.append((song_name, artist))
    
    return songs