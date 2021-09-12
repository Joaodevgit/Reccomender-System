from flask import Flask, make_response, request, jsonify, send_from_directory
from flask_cors import CORS
from neo4j_operations import *
from flask_swagger_ui import get_swaggerui_blueprint
from dotenv import load_dotenv, find_dotenv
import jwt
import datetime

load_dotenv(find_dotenv())

# Setup Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisissecret'

CORS(app)


# Path where swagger.json file will be
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


SWAGGER_URL = '/swagger'  # swagger's url
API_URL = '/static/swagger.json'  # Path where swagger.json file is
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Estgflix API"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)


def serialize_movie(movie):
    return {
        'movieId': movie['m']['movieId'],
        'imdbId': movie['m']['imdbId'],
        'tmdbId': movie['m']['tmdbId'],
        'title': movie['m']['title'],
        'released_date': movie['m']['released_date'],
        'year': movie['m']['year'],
        'overview': movie['m']['overview'],
        'poster': movie['m']['poster'],
    }


@app.route('/api/mainMenu')
def get_movies():
    user_logged_in_id = request.args.get('userID')
    popular_action_movies = get_popular_movies_by_genre("Action")
    popular_comedy_movies = get_popular_movies_by_genre("Comedy")
    user_recommended_movies = get_user_recommended_movies(int(user_logged_in_id))
    output_action = []
    output_comedy = []
    for movie in popular_action_movies:
        output_action.append(serialize_movie(movie))
    for movie in popular_comedy_movies:
        output_comedy.append(serialize_movie(movie))

    return {"popularActionMovies": output_action,
            "popularComedyMovies": output_comedy,
            "recommendedUserMovies": user_recommended_movies}


@app.route('/api/userProfile')
def get_user_movies():
    user_logged_in_id = int(request.args.get('userID'))
    watched_movies = get_user_watched_movies(user_logged_in_id)
    rated_movies = get_user_rated_movies(user_logged_in_id)
    output_watched = []
    output_rated = []
    for movie in watched_movies:
        output_watched.append(serialize_movie(movie))
    for movie in rated_movies:
        output_rated.append(serialize_movie(movie))

    return {"userWatchedMovies": output_watched,
            "userRatedMovies": output_rated}


@app.route('/api/movieDetails/<int:movie_id>', methods=["GET"])
def get_movie_by_id(movie_id):
    user_logged_in_id = request.args.get('userID', type=int)
    # get_user_movie_rating(user_id, movie_id)
    movie_info = get_movie(movie_id)
    return {"movieInfo": serialize_movie(movie_info),
            "genres": movie_info['movieGenres'],
            "hasWatched": is_a_watched_movie(user_logged_in_id, movie_id),
            "movieRating": get_user_movie_rating(user_logged_in_id, movie_id)}


@app.route('/api/movieDetails/<int:movie_id>/<int:user_id>', methods=["POST"])
def create_user_watched_relationship(movie_id, user_id):
    create_user_watched_movie(user_id, movie_id)
    return {"message": "Movie added to your watched movies list"}


@app.route('/api/movieDetails/rate/<int:movie_id>/<int:user_id>', methods=["POST"])
def create_user_rated_relationship(movie_id, user_id):
    rating = request.get_json()
    # print(rating['rating'])
    if get_user_movie_rating(user_id, movie_id) != rating['rating']:
        remove_user_relationship_rated_movie(user_id, movie_id)
        create_user_rated_movie(user_id, rating['rating'], movie_id)
        return {"message": "Movie rated added to your rated and watched movies list"}
    return {"message": "You already rated this movie with this value"}


@app.route('/api/searchResults/<string:search_words>')
def getSearchResults(search_words):
    moviesSearched = search_movies(search_words)
    output_movies_searched = []
    for movie in moviesSearched:
        output_movies_searched.append(serialize_movie(movie))

    return {"moviesSearched": output_movies_searched}


@app.route('/api/me')
def token_required():
    # const authHeader = req.headers["authorization"];
    # var token = authHeader && authHeader.split(" ")[1];
    token = request.headers["Authorization"]
    # print(token)
    if not token:
        return jsonify({'mensagem': 'Token is missing'}), 401

    try:
        data = jwt.decode(
            token.split(' ')[1], app.config['SECRET_KEY'], algorithms=["HS256"])
        current_user = find_user_by_id(data["user_id"])
        return {"user_id": current_user[0]['u'].get('userId'), "username": current_user[0]['u'].get('username')}
    except:
        return jsonify({'mensagem': 'Invalid token'}), 401


@app.route('/api/login', methods=['POST'])
def login_user():
    data = request.get_json()
    # print(data)
    user = find_user(data['user']["username"])
    if check_password_hash(user[0]['u']['password'], data['user']["password"]):
        token = jwt.encode(
            {'user_id': user[0]['u']['userId'], 'exp': datetime.datetime.utcnow() +
                                                       datetime.timedelta(minutes=30)},
            app.config['SECRET_KEY'], algorithm="HS256")
        # print(token)
        return jsonify({'token': token})
    else:
        return make_response('Não foi possível verificar', 401, {'WWW-Authenticate': 'Basic realm ="Login required!"'})


@app.route('/api/register', methods=['POST'])
def register_user():
    data = request.get_json()
    res = create_user(data['user']["username"], data['user']["password"])
    if res:
        msg = "User successfully created"
    else:
        msg = "User already exists"
    return jsonify({'message': msg})


if __name__ == '__main__':
    app.run(debug=True)
