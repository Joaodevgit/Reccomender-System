from neo4j import GraphDatabase, basic_auth

database_username = "YOUR_DATABASE_USERNAME"
database_password = "YOUR_DATABASE_PASSWORD"

driver = GraphDatabase.driver(
    "bolt://localhost:7687",
    auth=basic_auth(database_username, database_password))


def read_to_neo4j(query):
    """
    Method that, given a query, reads from neo4j database
    """
    with driver.session(database="neo4j") as session:
        result = session.read_transaction(
            lambda tx: tx.run(query).data())
    driver.close()
    return result


def get_popular_movies_recommended(user_id, top_n):
    """
    Method that, given a query and a number, reads from neo4j database and returns a list of popular movies
    :param query: neo4j query responsible to get all popular movies in descending order
    :type query: string
    :param user_id: user id
    :type user_id: integer
    :param top_n: number of popular movies to be returned
    :type top_n: integer
    :return list of top_nn popular movies that the user hasn't seen yet
    """
    query_get_top_n_popular_movies = """
    MATCH (u:User {userId:$userID})-[ra:RATED]->(m:Movie)
    WHERE ra.rating >=3.0 
    WITH collect(m.imdbId) as userMovies
    MATCH (:User)-[r:RATED]->(t:Movie) 
    WHERE NOT (t.imdbId IN userMovies) and r.rating >= 3.0
    RETURN t.imdbId,t.title, count(r) as tot ORDER BY tot DESC
    LIMIT 5
    """
    with driver.session(database="neo4j") as session:
        result_neo4j = session.read_transaction(
            lambda tx: tx.run(query_get_top_n_popular_movies, {"userID": user_id}).data())
        results = []
        for i in range(len(result_neo4j)):
            results.append(result_neo4j[i]['t.title'])
    driver.close()
    return results


# print(get_popular_movies_recommended(user_id=124, top_n=5))


def recommend_movies_to_user(user_id, top_n):
    """
    Method that, given a query, user id and a number, reads from neo4j database and returns a list of movies recommended
    movies
    :param user_id: user id
    :type user_id: integer
    :param top_n: number of popular movies to be returned
    :type top_n: integer
    :return list of recommended movies that the user hasn't seen yet, if there isn't any recommended movie it's returned
            the top_n popular movies ordered by
    """
    query_recommendation_with_top_n = """
    MATCH (u:User {userId: $userID})-[ra:RATED]->(m:Movie)-[r:RECOMMENDS]->(m2:Movie)
    WHERE NOT ((u)-[:WATCHED]->(m2)) and ra.rating >= 3.0
    WITH collect(DISTINCT m2.title) AS recommMovies, r ORDER BY r.confidence DESC
    RETURN DISTINCT recommMovies
    LIMIT $topN
    """
    with driver.session(database="neo4j") as session:
        recommended_movies = session.read_transaction(
            lambda tx: tx.run(query_recommendation_with_top_n, {"userID": user_id, "topN": top_n}).data())
        results = []
        for i in range(len(recommended_movies)):
            results.append(recommended_movies[i]['recommMovies'][0])
        if len(results) == 0:
            print("Não foi possível recomendar items, items populares:")
            results = get_popular_movies_recommended(user_id=user_id, top_n=top_n)
    driver.close()
    return results

# print("Neo4j: ")
# print(recommend_movies_to_user(user_id=13, top_n=5))
