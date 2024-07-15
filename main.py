
#* Import dotenv
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

#* Import Flask
from flask import Flask, request, url_for, session, redirect, render_template
app = Flask(__name__)
app.config["SESSION_COOCKIE_NAME"] = os.getenv("SESSION_COOCKIE_NAME")
app.secret_key = os.getenv("SECRET_KEY")
TOKEN_INFO = os.getenv("TOKEN_INFO")

#* Import from local file
import spotify
import genius
from utility import is_null

#* Import other library
import time
import logging
logging.basicConfig(filename='file.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

page_name = ""
games = [
    "guessthelyrics",
]

#SECTION ------------------------------------ Routing static page ------------------------------------
#* - Home route
@app.route("/")
def home():
    """Inizialize the authentication for spotify API

    Returns:
        redirect(auth_url): Redirect to an external page for the spotify's login
    """
    
    return render_template("home.html", logon="false") 

@app.route("/guessthelyrics/login")
def gtl_login():
    """Inizialize the authentication for spotify API

    Returns:
        redirect(auth_url): Redirect to an external page for the spotify's login
    """

    return redirect(url_for("gtl_playing"))

@app.route("/guessthelyrics/playing", methods=['GET', 'POST'])
def guessthelyrics_playing():
    """Inizialize the authentication for spotify API

    Returns:
        redirect(auth_url): Redirect to an external page for the spotify's login
    """
    
    uri = request.form["uri"]
    is_playlist = spotify.check_if_playlist(uri)
    if (not is_playlist):
        return redirect("http://127.0.0.1:5000/"+page_name)
        
    token = get_token()
    if (token == "login"):
        return redirect(url_for(token))
        
    playlist = spotify.get_playlist(token, uri)
    
    return render_template("guessthelyrics_playing.html")

@app.route("/<page>")
def render_game(page):
    """Inizialize the authentication for spotify API

    Returns:
        redirect(auth_url): Redirect to an external page for the spotify's login
    """
        
    global page_name
    page_name = page.replace("/", "_")
    if (page in games):
        
        token = get_token()
        if (token == "login"):
            return redirect(url_for(token))   
        
        return render_template(page+".html")
    else:
        return redirect(url_for(page))
#!SECTION ------------------------------------ Routing static page ------------------------------------

#SECTION ------------------------------------ Login Spotify ------------------------------------
#* - Login route
@app.route("/login")
def login():
    """Inizialize the authentication for spotify API

    Returns:
        redirect(auth_url): Redirect to an external page for the spotify's login
    """
    auth_url = spotify.login()
    print(auth_url)
    
    return redirect(auth_url) 

#* - The external page then redirect us to this page after you complete the login
@app.route("/callback")
def callback():
    """Extraction of the access token, which was given by the login

    Returns:
        redirect(url_for("create_playlist", external = True)): Redirect to an internal page which will execute the main task of this code
    """
    session.clear()
    
    token_info = spotify.callback(request)
        
    session[TOKEN_INFO] = token_info
    
    return redirect("http://127.0.0.1:5000/"+page_name) 

#* - get_token
def get_token():
    """Extraction of the token from the session, 
       if there isn't or it is expired it will redirect to the login page,
       

    Returns:
        token_info: the access token
    """
    
    token_info = session.get(TOKEN_INFO, None)
    logging.debug("Token: " + str(token_info))
    if token_info==None:
        logging.warning("User is not logged in Spotify")
        token_info = "login"
        
    now = int(time.time())
    
    if token_info != "login":
        is_expired = token_info["expires_at"] - now < 60
        if(is_expired): 
            logging.warning("The token is expired")
            token_info = spotify.refresh_token(token_info)
            logging.info("The token was refreshed")
            session[TOKEN_INFO] = token_info
        
    return token_info
#!SECTION ------------------------------------ Login Spotify ------------------------------------

#* Flask app run     
app.run(port=5000, debug=True)