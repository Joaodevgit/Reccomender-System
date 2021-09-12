from neo4j import GraphDatabase, basic_auth
from werkzeug.security import generate_password_hash, check_password_hash

driver = GraphDatabase.driver(
    "bolt://localhost:7687",
    auth=basic_auth("neo4j", "pf2021"))


def find_user(username):
    """
    Method that, given an username, will find an user in neo4j database
    :param username: user's username
    :type username: string
    :return: user node with the username
    """
    query_find_user = """
                      match (u:User {username: $username})
                      return u
                      """

    with driver.session(database="neo4j") as session:
        user = session.read_transaction(
            lambda tx: tx.run(query_find_user, username=username).data())

    driver.close()
    return user


# print(find_user("João")[0]['u'].get('userId'))

def find_user_by_id(user_id):
    """
    Method that, given an user id, will find an user in neo4j database
    :param user_id: user's id
    :type user_id: integer
    :return: user node with the user id
    """
    query_find_user = """
                      match (u:User {userId: $userID})
                      return u
                      """

    with driver.session(database="neo4j") as session:
        user = session.read_transaction(
            lambda tx: tx.run(query_find_user, userID=user_id).data())

    driver.close()
    return user


# print(type(find_user_by_id(5001)[0]['u'].get('username')))


def search_movies(search_result):
    """
    Method that, given a search result words, will find in neo4j database movies title that contains the search result
    words
    :param search_result: search result words
    :type search_result: string
    :return: if no movie contains the search result words it will be returned an empty array otherwise it will be
             returned an array of nodes with the movies searched (Returns a maximum of 3 movies)
    """
    query_search_movies = """
                        MATCH (m:Movie)
                        WHERE toLower(m.title) CONTAINS toLower($movieSearched)
                        RETURN m
                        LIMIT 3
                        """
    with driver.session(database="neo4j") as session:
        result_movies = session.read_transaction(
            lambda tx: tx.run(query_search_movies, movieSearched=search_result).data())
    driver.close()
    if len(result_movies) != 0:
        return result_movies
    else:
        return []


# print(search_movies("lord"))


def get_movie(movie_id):
    """
    Method that, given a movie id, will find in neo4j database for a specific movie
    :param movie_id: movie's id
    :type movie_id: integer
    :return: if the movie exists in the neo4j database it will return the movie node, otherwise it will return an empty
             array
    """
    query_get_movie = """
                    MATCH (m:Movie {movieId: $movieID})-[:IN_GENRE]->(g:Genre)
                    RETURN m, collect(g.genre) as movieGenres
                    """
    with driver.session(database="neo4j") as session:
        # movieId, title, genres, imdbId, tmdbId, released_date, year, poster, overview
        result_movie = session.read_transaction(
            lambda tx: tx.run(query_get_movie, movieID=movie_id).data()[0])
    driver.close()

    if len(result_movie) != 0:
        return result_movie

    return []


def create_user(username, password):
    """
    Method that, given an username and a password (that will be encrypted), will create the user node that contains the
    user id, username and password encrypted
    :param username: user's username
    :type username: string
    :param password: user's password
    :type password: string
    :return: True if the operation was successful, otherwise it will return False
    """
    query_get_last_user_id = """
                              MATCH (u:User)
                              RETURN max(u.userId) as maxId
                              """

    query_create_user = """
                        MERGE(u: User {userId: toInteger($userID),username: $username, password:$password})
                        """

    with driver.session(database="neo4j") as session:
        user = find_user(username)

        if len(user) == 0:
            last_user_id = session.read_transaction(
                lambda tx: tx.run(query_get_last_user_id).data())
            if len(last_user_id) == 0:
                new_user_id = 1
            else:
                new_user_id = last_user_id[0]['maxId'] + 1

            session.write_transaction(
                lambda tx: tx.run(query_create_user, userID=new_user_id, username=username,
                                  password=generate_password_hash(password, method='sha256')))
            driver.close()
            return True
        else:
            driver.close()
            return False
    driver.close()


# create_user("João", "testando")


def get_popular_movies_by_genre(movie_genre):
    """
    Method that, given a movie genre, will return the top 5 popular movies with that genre
    :param movie_genre: movie's genre
    :type movie_genre: string
    :return: if the genre is valid it will return list of top 5 popular movies based on genre, otherwise it will return
             an empty array
    """
    verify_genre = """
            MATCH (g:Genre {genre:$movieGenre})
            RETURN g
    """
    query_popular_movies = """
                    MATCH (:User)-[w:WATCHED]->(m:Movie)-[:IN_GENRE]->(:Genre {genre:$movieGenre})
                    RETURN m, count(w) as tot ORDER BY tot DESC
                    LIMIT 5
                    """

    with driver.session(database="neo4j") as session:
        genre_existence = session.read_transaction(
            lambda tx: tx.run(verify_genre, movieGenre=movie_genre).data())
        if genre_existence is not None:
            popular_movies = session.read_transaction(
                lambda tx: tx.run(query_popular_movies, movieGenre=movie_genre).data())
            driver.close()
            # for i in range(len(popular_movies)):
            #     print(popular_movies[i]['m'].get('title'))

            return popular_movies
        else:
            driver.close()
            return []
    driver.close()


# print(get_popular_movies_by_genre("Comedy"))

def get_user_watched_movies(user_id):
    """
    Method that, given an user id, will find in neo4j database for a maximum of 5 movies nodes that contains the
    relationship "WATCHED" with the user node
    :param user_id: user's id
    :type user_id: integer
    :return: A maximum of 5 movie's nodes that the user node has watched
    """
    query_user_watched_movies = """
                        MATCH (:User {userId:$userID})-[:WATCHED]->(m:Movie)
                        RETURN DISTINCT m
                        LIMIT 5
                        """
    with driver.session(database="neo4j") as session:
        user_watched_movies = session.read_transaction(
            lambda tx: tx.run(query_user_watched_movies, userID=user_id).data())

        # for i in range(len(user_watched_movies)):
        #     print(user_watched_movies[i]['m'].get('title'))
    driver.close()
    return user_watched_movies


# print(get_user_watched_movies(5000))

def get_user_rated_movies(user_id):
    """
    Method that, given an user id, will find in neo4j database for a maximum of 5 movies nodes that contains the
    relationship "RATED" with the user node
    :param user_id: user's id
    :type user_id: integer
    :return: A maximum of 5 movie's nodes that the user has rated
    """
    query_user_rated_movies = """
                        MATCH (:User {userId:$userID})-[:RATED]->(m:Movie)
                        RETURN DISTINCT m
                        LIMIT 5
                        """
    with driver.session(database="neo4j") as session:
        user_rated_movies = session.read_transaction(
            lambda tx: tx.run(query_user_rated_movies, userID=user_id).data())

        # for i in range(len(user_rated_movies)):
        #     print(user_rated_movies[i]['m'].get('title'))
    driver.close()
    return user_rated_movies


# print(get_user_rated_movies(5000))


def create_user_rated_movie(user_id, rating_value, movie_id):
    """
    Method that, given an user id, movie id and a rating value, will create the relationship "RATED", with the property
    rating containing the rating_value parameter, between the user and the movie nodes
    :param user_id: user's id
    :type user_id: integer
    :param rating_value: user's rating value given to the movie
    :type rating_value: integer
    :param movie_id: movie's id
    :type movie_id: integer
    """
    query_user_rated_movie = """
                    MATCH (u:User {userId: $userID})
                    MATCH (m:Movie {movieId: $movieID})
                    MERGE (u)-[:RATED {rating:$ratingValue} ]->(m)
                    """

    with driver.session(database="neo4j") as session:
        session.write_transaction(
            lambda tx: tx.run(query_user_rated_movie, userID=user_id, movieID=movie_id,
                              ratingValue=rating_value).data())
    driver.close()
    create_user_watched_movie(user_id, movie_id)


# create_user_rated_movie(5001, 3.0, 1)


def create_user_watched_movie(user_id, movie_id):
    """
    Method that, given an user id, movie id and a rating value, will create the relationship "WATCHED" between the
    user and the movie nodes
    :param user_id: user's id
    :type user_id: integer
    :param movie_id: movie's id
    :type movie_id: integer
    """
    query_user_watched_movie = """
                    MATCH (u:User {userId: $userID})
                    MATCH (m:Movie {movieId: $movieID})
                    MERGE (u)-[:WATCHED]->(m)
                    """
    with driver.session(database="neo4j") as session:
        session.write_transaction(
            lambda tx: tx.run(query_user_watched_movie, userID=user_id, movieID=movie_id).data())
    driver.close()


def remove_user_relationship_rated_movie(user_id, movie_id):
    """
    Method that, given an user id and a movie id, will delete the relationship "RATED" between the user and the movie
    nodes
    :param user_id: user's id
    :type user_id: integer
    :param movie_id: movie's id
    :type movie_id: integer
    """
    query_delete_relationship = """
                                  MATCH (:User {userId:$userID})-[r:RATED]-(:Movie{movieId: $movieID})
                                  DELETE r
          """
    with driver.session(database="neo4j") as session:
        session.write_transaction(
            lambda tx: tx.run(query_delete_relationship, userID=user_id, movieID=movie_id).data())
    driver.close()


# create_user_watched_movie(5001, 2)

def is_a_watched_movie(user_id, movie_id):
    """
    Method that, given an user id and a movie id, will verify if an user has watched a certain movie or not
    :param user_id: user's id
    :type user_id: integer
    :param movie_id: movie's id
    :type movie_id: integer
    :return: True if the user has watched the movie, otherwise will return False
    """
    query_user_watched_movie = """
                    MATCH (u:User {userId: $userID})-[w:WATCHED]->(m:Movie {movieId: $movieID})
                    RETURN w
                    """
    with driver.session(database="neo4j") as session:
        movie_watched = session.read_transaction(
            lambda tx: tx.run(query_user_watched_movie, userID=user_id, movieID=movie_id).data())
    driver.close()
    if len(movie_watched) == 0:
        return False
    else:
        return True


# print(is_a_watched_movie(5003, 318))

def get_user_movie_rating(user_id, movie_id):
    """
    Method that, given an user id and a movie id, will get the rating value given rating given by a user to a certain
    movie
    :param user_id: user's id
    :type user_id: integer
    :param movie_id: movie's id
    :type movie_id: integer
    :return: 0 if the user hasn't rated the movie, otherwise it will return the user's rating value given to  the movie
    """
    query_get_user_rating_value_movie = """
                    MATCH (u:User {userId: $userID})-[r:RATED]->(m:Movie {movieId: $movieID})
                    RETURN r.rating
                    """
    with driver.session(database="neo4j") as session:
        rating_movie_value = session.read_transaction(
            lambda tx: tx.run(query_get_user_rating_value_movie, userID=user_id, movieID=movie_id).data())
        if len(rating_movie_value) == 0:
            rating_value = 0
        else:
            rating_value = rating_movie_value[0]['r.rating']
    driver.close()
    return rating_value


# print(get_user_movie_rating(5001, 2))

def get_user_recommended_movies(user_id):
    """
    Method, that given an user id, will recommend movies to the user based on ratings, with a minimum value of 3,
    assigned by the user to the movies. If there are no movies to be recommended to the user, it will be recommended the
    top 5 of popular movies that the user hasn't seen yet
    :param user_id: user's id
    :type user_id: integer
    :return: returns a maximum of 5 movies, ordered by the "RECOMMENDS" relationship confidence property in a descending
             order (the greater the confidence is the greater the relevance of the movie's recommendation will be),
             otherwise it will return the top 5 of popular movies that the user hasn't seen yet
    """
    # query_recommend_movies = """
    #                 MATCH (u:User {userId: $userID})-[ra:RATED]->(m:Movie)-[r:RECOMMENDS]->(m2:Movie)
    #                 WHERE NOT ((u)-[:WATCHED]->(m2)) and ra.rating >= 3.0
    #                 WITH collect(DISTINCT m2) AS recommMovies, r ORDER BY r.confidence DESC
    #                 RETURN DISTINCT recommMovies
    #                 LIMIT 5
    #                 """

    # Recommendation query, based on the movies that the user liked (rated >= 3) and hasn't seen yet
    query_recommend_movies = """
                    MATCH (u:User {userId: $userID})-[ra:RATED]->(m:Movie)-[r:RECOMMENDS]->(m2:Movie)
                    WHERE NOT ((u)-[:WATCHED]->(m2)) and ra.rating >= 3.0
                    RETURN collect(DISTINCT m2)[0..5] as recommMovies
                    """

    # query_get_top_n_popular_movies = """
    #                     MATCH (u:User {userId:$userID})-[ra:RATED]->(m:Movie)
    #                     WHERE ra.rating >= 3.0
    #                     WITH collect(m.imdbId) as userWatchedMovies
    #                     MATCH (:User)-[r:RATED]->(t:Movie)
    #                     WHERE NOT (t.imdbId IN userWatchedMovies) and r.rating >= 3.0
    #                     RETURN t, count(r) as tot ORDER BY tot DESC
    #                     LIMIT 5
    #                 """

    # Recommendation query based on the movies that the user hasn't seen yetand the movies that the other users have
    # rated >= 3.0
    query_get_top_n_popular_movies = """
                        MATCH (u:User {userId:$userID})-[w:WATCHED]->(m:Movie)
                        WITH collect(m.imdbId) as userWatchedMovies
                        MATCH (:User)-[r:RATED]->(t:Movie) 
                        WHERE NOT (t.imdbId IN userWatchedMovies) and r.rating >= 3.0
                        RETURN t, count(r) as tot ORDER BY tot DESC
                        LIMIT 5
                    """
    with driver.session(database="neo4j") as session:
        recommended_movies = session.read_transaction(
            lambda tx: tx.run(query_recommend_movies, userID=user_id).data())
        # for i in range(len(recommended_movies)):
        #     print(recommended_movies[i]['recommMovies'][0])
        # if len(recommended_movies) == 0:
        if len(recommended_movies[0]["recommMovies"]) == 0:
            popular_recommended_movies = session.read_transaction(
                lambda tx: tx.run(query_get_top_n_popular_movies, userID=user_id).data())
            pop_recomm_movies_list = []
            for i in range(len(popular_recommended_movies)):
                new_pop_recomm_movie = {'movieId': popular_recommended_movies[i]['t']['movieId'],
                                        'imdbId': popular_recommended_movies[i]['t']['imdbId'],
                                        'tmdbId': popular_recommended_movies[i]['t']['tmdbId'],
                                        'title': popular_recommended_movies[i]['t']['title'],
                                        'released_date': popular_recommended_movies[i]['t']['released_date'],
                                        'year': popular_recommended_movies[i]['t']['year'],
                                        'overview': popular_recommended_movies[i]['t']['overview'],
                                        'poster': popular_recommended_movies[i]['t']['poster']}
                pop_recomm_movies_list.append(new_pop_recomm_movie)
            driver.close()
            return pop_recomm_movies_list
        else:
            driver.close()
            recomm_movies_list = []
            for i in range(len(recommended_movies[0]["recommMovies"])):
                new_movie = {'movieId': recommended_movies[0]['recommMovies'][i]['movieId'],
                             'imdbId': recommended_movies[0]['recommMovies'][i]['imdbId'],
                             'tmdbId': recommended_movies[0]['recommMovies'][i]['tmdbId'],
                             'title': recommended_movies[0]['recommMovies'][i]['title'],
                             'released_date': recommended_movies[0]['recommMovies'][i]['released_date'],
                             'year': recommended_movies[0]['recommMovies'][i]['year'],
                             'overview': recommended_movies[0]['recommMovies'][i]['overview'],
                             'poster': recommended_movies[0]['recommMovies'][i]['poster']}
                recomm_movies_list.append(new_movie)
            # Old way (ordered by confidence)
            # for i in range(len(recommended_movies)):
            #     new_movie = {'movieId': recommended_movies[i]['recommMovies'][0]['movieId'],
            #                  'imdbId': recommended_movies[i]['recommMovies'][0]['imdbId'],
            #                  'tmdbId': recommended_movies[i]['recommMovies'][0]['tmdbId'],
            #                  'title': recommended_movies[i]['recommMovies'][0]['title'],
            #                  'released_date': recommended_movies[i]['recommMovies'][0]['released_date'],
            #                  'year': recommended_movies[i]['recommMovies'][0]['year'],
            #                  'overview': recommended_movies[i]['recommMovies'][0]['overview'],
            #                  'poster': recommended_movies[i]['recommMovies'][0]['poster']}
            #     recomm_movies_list.append(new_movie)

            return recomm_movies_list
    driver.close()

# get_user_recommended_movies(5005)
# print(get_user_recommended_movies(5005))
