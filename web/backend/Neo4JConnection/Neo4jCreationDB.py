import ast
import csv

from neo4j import GraphDatabase, basic_auth

# from CleanAndTransformData import *

database_username = "YOUR_DATABASE_USERNAME"
database_password = "YOUR_DATABASE_PASSWORD"

driver = GraphDatabase.driver(
    "bolt://localhost:7687",
    auth=basic_auth(database_username, database_password))


def write_to_neo4j(query):
    """
    Method that, given a query, writes to neo4j database
    """
    with driver.session(database="neo4j") as session:
        session.write_transaction(
            lambda tx: tx.run(query))
    driver.close()


def write_association_rules_to_neo4j(query):
    """
    Method that, given a query, writes to neo4j database
    """
    with driver.session(database="neo4j") as session:
        session.write_transaction(
            lambda tx: tx.run(query))
    driver.close()


query_create_genre_index = """
CREATE CONSTRAINT ON (g:Genre) ASSERT g.genreId IS UNIQUE;
"""

query_create_movie_index = """
CREATE CONSTRAINT ON (m:Movie) ASSERT m.movieId IS UNIQUE;
"""

query_create_user_index = """
CREATE CONSTRAINT ON (u:User) ASSERT u.userId IS UNIQUE;
"""

query_create_nodes_genres = """
  LOAD CSV WITH HEADERS FROM 'file:///Path_to_movies_genres.csv' AS row
  WITH row WHERE row.genre IS NOT NULL
  MERGE (g:Genre {
                genreId: toInteger(row.genreId),
                genre:row.genre
                })
"""

query_create_nodes_movies = """
LOAD CSV WITH HEADERS FROM 'file:///Path_to_movies.csv' AS row
WITH row WHERE row.title IS NOT NULL and row.tmdbId IS NOT NULL and row.released_date IS NOT NULL and row.overview IS NOT NULL
MERGE (m:Movie {
                movieId: toInteger(row.movieId),
                title:row.title,
                imdbId:toInteger(row.imdbId),
                tmdbId:toInteger(row.tmdbId),
                released_date:row.released_date,
                year:row.year,
                poster:row.poster,
                overview: row.overview
                })
"""

query_create_nodes_users = """
LOAD CSV WITH HEADERS FROM 'file:///Path_to_userRatings5k.csv' AS row
MERGE (u:User {
                userId: toInteger(row.userId)
                })
"""

query_add_movie_data = """
LOAD CSV WITH HEADERS FROM 'file:///Path_to_new_movies_data.csv' AS row
    MATCH (m:Movie {movieId:toInteger(row.movieId)})
    SET m.overview = row.overview
"""


def create_movies_genres_relationships(movies_filename):
    """
    Method that will write in Neo4j all the relationships between movies and genres (movie-[:IN_GENRE]->genre)
    :param movies_filename: path where the csv file is located (this file must be in csv format and must contain
                            the following columns: movieId, title, genres, imdbId, tmdbId, released_date, year, poster)
    :type movies_filename: string
    """
    query = """
    MATCH (m:Movie {movieId: $movieId, title: $movieName})
    MATCH (g:Genre {genre: $genreName})
    MERGE (m)-[:IN_GENRE]->(g)
    """
    with driver.session(database="neo4j") as session:
        with open(movies_filename, encoding='utf-8') as fp:
            reader = csv.reader(fp)
            next(reader, None)  # skip the headers
            MOVIEID, TITLE, GENRES, IMDBID, TMDBID, RELEASEDDATE, YEAR, POSTER = 0, 1, 2, 3, 4, 5, 6, 7
            for line in reader:
                genres = line[GENRES].split('|')
                for genre in genres:
                    session.write_transaction(
                        lambda tx: tx.run(query,
                                          {"movieId": int(line[MOVIEID]), "movieName": line[TITLE],
                                           "genreName": genre}))
        driver.close()


def create_users_movies_relationships(user_ratings_filename):
    """
    Method that will write in Neo4j all the relationships between movies and genres (user-[:WATCHED]->movie)
    (user-[:RATED {rating}]->movie)
    :param user_ratings_filename: path where the csv file is located (this file must be in csv format and must contain
                            the following columns: userId, movieTitle, rating)
    :type user_ratings_filename: string
    """
    query = """
    MATCH (u:User {userId: $userId})
    MATCH (m:Movie {title: $movieName})
    MERGE (u)-[:WATCHED]->(m)
    MERGE (u)-[:RATED {rating: $ratingValue}]->(m)
    """
    with driver.session(database="neo4j") as session:
        with open(user_ratings_filename, encoding='utf-8') as fp:
            reader = csv.reader(fp)
            next(reader, None)  # skip the headers
            USERID, MOVIETITLE, RATING = 0, 1, 2
            for line in reader:
                session.write_transaction(
                    lambda tx: tx.run(query,
                                      {"userId": int(line[USERID]), "movieName": line[MOVIETITLE],
                                       "ratingValue": float(line[RATING])}))
        driver.close()


def create_movie_recommends_movie_relationships(rules_filename):
    """
    Method that will write in Neo4j all the relationships between movies (movieA-[:RECOMMENDS]->movieB)
    Method that reads from a csv file containing association rules and create relationships
    :param rules_filename: csv file path where all user ratings are is located (this file must be in csv format and must
                           contain the following columns: id, antecedents, consequents, antecedent_support,
                           consequent_support, support, confidence, kulczynski, imbalance_ratio)
    :type rules_filename: string
    """
    query_get_movie_relationship = """
    MATCH (:Movie {movieId: $movieAntID})-[r:RECOMMENDS]->(:Movie {movieId: $movieConsID})
    RETURN r.confidence
    """
    query_get_movie_id = """
    MATCH (m:Movie {title: $movieTitle})
    RETURN m.movieId
    """
    query_delete_rule_relationship = """
    MATCH (:Movie {movieId: $movieAntID})-[r:RECOMMENDS]->(:Movie {movieId: $movieConsID})
    DELETE r
    """
    query_connect_movies = """
    MATCH (mA:Movie {movieId: $movieAntID})
    MATCH (mB:Movie {movieId: $movieConsID})
    MERGE (mA)-[:RECOMMENDS {confidence: $newConfidence}]->(mB)
    """
    with driver.session(database="neo4j") as session:
        with open(rules_filename, encoding='utf-8') as fp:
            reader = csv.reader(fp)
            next(reader, None)  # skip the headers
            ID, ANTECEDENTS, CONSEQUENTS, ANTECEDENTSUPPORT, CONSEQUENTSUPPORT, SUPPORT, CONFIDENCE, KULC, IBRATIO = 0, 1, 2, 3, 4, 5, 6, 7, 8
            for line in reader:
                rule_antecedent = ast.literal_eval(line[ANTECEDENTS])
                rule_consequent = ast.literal_eval(line[CONSEQUENTS])
                for antecedent in rule_antecedent:
                    antecedent_id = session.read_transaction(lambda tx: tx.run(query_get_movie_id,
                                                                               {"movieTitle": antecedent}).data()[0][
                        'm.movieId'])
                    for consequent in rule_consequent:
                        consequent_id = session.read_transaction(lambda tx: tx.run(query_get_movie_id,
                                                                                   {"movieTitle": consequent}).data()[
                            0]['m.movieId'])

                        relationship_exists = session.read_transaction(lambda tx: tx.run(query_get_movie_relationship,
                                                                                         {"movieAntID": antecedent_id,
                                                                                          "movieConsID": consequent_id}).data())

                        if len(relationship_exists) != 0:
                            # print(relationship_exists[0]['r.confidence'])
                            if float(line[CONFIDENCE]) > relationship_exists[0]['r.confidence']:
                                session.write_transaction(lambda tx: tx.run(query_delete_rule_relationship,
                                                                            {"movieAntID": antecedent_id,
                                                                             "movieConsID": consequent_id}))
                                session.write_transaction(lambda tx: tx.run(query_connect_movies,
                                                                            {"movieAntID": antecedent_id,
                                                                             "movieConsID": consequent_id,
                                                                             "newConfidence": float(line[CONFIDENCE])}))
                        else:
                            session.write_transaction(lambda tx: tx.run(query_connect_movies,
                                                                        {"movieAntID": antecedent_id,
                                                                         "movieConsID": consequent_id,
                                                                         "newConfidence": float(line[CONFIDENCE])}))
    driver.close()

# CREATION OF INDEXES

# write_to_neo4j(query_create_genre_index)
# write_to_neo4j(query_create_movie_index)
# write_to_neo4j(query_create_user_index)

# CREATION OF NODES (Dont forget to comment dbms.directories.import=import in database's settings!)

# Nodes Genres
# write_to_neo4j(query_create_nodes_genres)

# Nodes Movies
# write_to_neo4j(query_create_nodes_movies)

# Nodes Users
# write_to_neo4j(query_create_nodes_users)

# CREATION OF RELATIONSHIPS

# Movie -[:IN_GENRE]-> Genre
# create_movies_genres_relationships('../datasets/movies.csv')

# User -[:WATCHED]-> Movie | User -[:RATED {rating}]-> Movie
# create_users_movies_relationships('../datasets/userRatings5k.csv')

# MovieA -[:RECOMMENDS]-> MovieA
# create_movie_recommends_movie_relationships('../rulesCsv/rules5kUsersImp.csv')
