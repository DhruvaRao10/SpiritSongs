from flask import Flask, request, url_for, session, redirect
from spotipy.oauth2 import SpotifyOAuth
import spotipy
import time

app = Flask(__name__)

app.secret_key = "Ohellofriend2024"
app.config['SESSION_COOKIE_NAME'] = 'Dr Cookie'
TOKEN_INFO = "token_info"

@app.route('/')
def login():
    sp_oauth = spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/redirect')
def redirectPage():
    sp_oauth = spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('getTracks', _external=True))

@app.route('/getTracks')
def getTracks():
    try:
        token_info = get_token()
    except:
        print("user not logged in")
        return redirect('/')
    
    sp = spotipy.Spotify(auth=token_info['access_token'])
    all_songs = []
    iter = 0
    while True:
        items = sp.current_user_saved_tracks(limit=50,offset=iter*50)['items']
        iter+=1 
        all_songs += items
        if(len(items) < 50):
            break
    return str(len(all_songs))
        

def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        raise Exception("Token not available")
    
    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if is_expired:
        sp_oauth = spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    return token_info

def spotify_oauth():
    return SpotifyOAuth(
        client_id="533142914f93486298556d73fff14ccc",
        client_secret="58bb0f3a4e4b4b1fae8eaa210b410a14",
        redirect_uri=url_for("redirectPage", _external=True),
        scope='user-library-read'
    )

if __name__ == '__main__':
    app.run(debug=True)
