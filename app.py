# Library Imports
import requests
from flask import Flask, redirect, url_for, jsonify, render_template, request
from flask_cors import CORS
import base64
from flask_sqlalchemy import SQLAlchemy

# Get Config variables
from config import configs


"""
========================================================================================
                Flask Setup
========================================================================================
"""
# Instantiate the Flask class into the app object
app = Flask(__name__)
#Initiate SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test3.db'
db = SQLAlchemy(app)


# Handle Cross Origin Resource Sharing issues
CORS(app)
#Define the database tables
class user_genres(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    genre = db.Column(db.String(80), nullable=True)
    spotify_user_id = db.Column(db.String(120), nullable=True)

    @property
    def serialize(self):
       """Return object data in easily serializable format"""
       return {
           'spotify_user_id':self.spotify_user_id,
           'genre':self.genre
       }
#Create the DB
db.create_all()
"""
========================================================================================
                Spotify Authorization Setup
========================================================================================
"""
# Encode client_id:client_secret
base_encode = base64.b64encode(f"{configs['id']}:{configs['secret']}".encode("utf-8"))
base_string = str(base_encode, "utf-8")

# Define some URLs
BASE_URL = "https://api.spotify.com"
AUTH_URL = "https://accounts.spotify.com"

#Variable containing User ID across the app
uid=''


"""
========================================================================================
                Front end Routes
========================================================================================
"""


@app.route('/')
def index():
    """
    This is the default front facing home route
    :return:
    """
    return render_template('home.html', uid=uid)



"""
========================================================================================
                Authorization Routes
========================================================================================
"""

@app.route('/auth')
def authorization():
    """
    This route initiates the Authorization to the spotify API by redirecting the user to the
    accounts.spotify.com/authorize endpoint with the client_id for our app and the redirect_uri
    included in the url parameters. We can also include a state parameter to make sure there wasn't
    an interception of our data. The spotify API then redirects after login to the redirect_uri which
    we have set to our /api endpoint.
​
    This is STEP 1)
​
    :return: redirect
    """
    print("Getting Token")

    scopes = "user-top-read"

    return redirect(f"{AUTH_URL}/authorize?client_id={configs['id']}&scope={scopes}&redirect_uri={configs['redirect']}&response_type=code&show_dialog=true")


@app.route('/api/auth')
def spotify_redirect():
    """
    This route is defined in the Spotify API application settings as the redirect_uri. After authorizing the Spotify API
    the api will redirect to this url with a code parameter in the url. We can use this code in a new request to the
    spotify API to exchange the code for a token by making a request to the accounts.spotify.com/api/token endpoint and
    including the code and the redirect_uri in a post body and including the client_id and client_secret in the
    request headers.
​
    STEP 2
    :return:
    """
    # Print statement to show history in the terminal
    print("***** Detected a redirect *****")

    # Get the response from the Spotify API.
    # The user should be redirected by the spotify service to this endpoint after they login and accept permissions
    # The url will include the "code" parameter which is an Authorization code
    print(request.args['code'])
    code = request.args['code']

    # Use that authorization code in the post request to the Spotify service we are also including
    # the redirect uri as required by the API
    token_params = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": configs["redirect"]
    }

    headers = {
        "Authorization": f"Basic {base_string}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # Make the request to the API
    response = requests.post(f"{AUTH_URL}/api/token", params=token_params, headers=headers)

    # Debug the response
    print(response.text)

    # Get the access_token out of the response
    data = response.json()
    token = data["access_token"]

    """
    ========================================================================================
        STEP 3
    ========================================================================================
    """
    offset_val = 0

    # Define request parameters here
    query_params = {
        "time_range": "long_term",
        "offset": offset_val,
        "limit": 50
    }

    # Define authorization headers here. Note the token from before is used in this request
    # with the Bearer text included.
    req_headers = {
        "Authorization": f"Bearer {token}"
    }
    #Get the users profile ID
    user_resp = requests.get(f"{BASE_URL}/v1/me", headers=req_headers)
    # Get the response from the spotify API using the correct token in the headers. This should return user information
    final_resp = requests.get(f"{BASE_URL}/v1/me/top/artists", params=query_params, headers=req_headers)

    # Debug the final response

    print("================================================")
    print(final_resp)
    print("================================================")
    # print("================================================")
    # print(user_resp)
    # print("================================================")
    # Utilize the data
    data = final_resp.json()
    user_id_reponse = user_resp.json()
    print(data)

    for artist in data['items']:
        print(artist['genres'])
        for genre in artist['genres']:
            genre_data = user_genres(genre=genre, spotify_user_id=user_id_reponse['id'])
            db.session.add(genre_data)
            db.session.commit()
            
    uid=user_id_reponse['id']
    print(user_id_reponse['id'])

    # Get playlist information
    #playlist_resp = requests.get(f"{BASE_URL}/v1/me/playlists", headers=req_headers)

    # pdata = playlist_resp.json()

    # final_data = {
    #     "first": data,
    #     "last": pdata
    # }

    #return jsonify(final_data)
    return redirect(url_for('index',uid=uid))


"""
========================================================================================
                Data Routes
========================================================================================
"""


# @app.route('/api/playlists')
# def playlists():
#     return "debug"

@app.route('/api/genres')
def genres():
    uid = request.args.get('uid')
    genres = user_genres.query.filter_by(spotify_user_id=uid).all()
    #figure out how to turn genre into json from sqlalchemy object (list comprehension)
    # return jsonify(json_list=[i.serialize for i in genres.all()])
    return jsonify(json_list=[i.serialize for i in genres.all()])


"""
========================================================================================
        Flask Run Statement
========================================================================================
"""
# Conditional and run the Flask app
if __name__ == "__main__":
    app.run(port=5000, debug=True)