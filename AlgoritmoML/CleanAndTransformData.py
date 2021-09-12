import csv
import json
import pandas as pd
import ast


def read_data(filename, qty_users):
    """
    Method that reads from a csv file and returns a list movies rated from the users
    :param filename: csv file path where all user ratings are is located (this file must be in csv format and must
                     contain the following columns: userId, movieId, rating)
    :type filename: string
    :param qty_users: quantity of users id's who rated movies
    :type qty_users: integer (between 1 and 200000)
    :return: list of transactions with all users' movies
    """
    with open(filename, encoding='utf-8') as fp:
        reader = csv.reader(fp)
        next(reader, None)  # skip the headers
        USERID, MOVIETITLE, RATING = 0, 1, 2
        ratings_list = []
        tot_users = str(qty_users + 1)
        for line in reader:
            if line[USERID] == tot_users:
                break
            new_line = [line[USERID], line[MOVIETITLE], line[RATING]]
            ratings_list.append(new_line)

    return ratings_list


# print(read_data('datasets/movies.csv', qtyUsers))

def get_movies_dict(filename):
    """
    Method that converts a csv file with the movies information (movieId, title, genres) into a dictionary
    :param filename: path where the csv file is located (this file must be in csv format and must contain
                     the following columns: movieId, title, genres)
    :type filename: string
    :return: dictionary that contains the following format: { MovieId: { Title: ..., Genres = [] }, ... }
    """
    with open(filename, encoding='utf-8') as fp:
        reader = csv.reader(fp)
        next(reader, None)  # skip the headers
        movies_dict = {}
        # moviesDict = { MovieId: { Title: ... , Genres = [] }  }
        MOVIEID, TITLE, GENRES = 0, 1, 2
        for line in reader:
            genres = line[GENRES].split('|')
            if line[MOVIEID] in movies_dict.keys():
                movies_dict[line[MOVIEID]].append({"Title": line[TITLE], "Genres": genres})
            else:
                movies_dict[line[MOVIEID]] = {"Title": line[TITLE], "Genres": genres}

    return movies_dict


# print(json.dumps(get_movies_dict('movies.csv'), ensure_ascii=False, indent=2))

def write_new_mov_csv_files(old_filename, new_filename, qty_users):
    """
    Method that, from the csv file of original movielens user ratings (userId, movieId, rating, timestamp), will write
    to a new csv file (userId, movieTitle, rating)
    :param old_filename: path where the csv file is located (this file must be in csv format and must contain
                        the following columns: userId, movieId, rating, timestamp)
    :type old_filename string
    :param new_filename: path where the new file will be located (this file must be in csv format)
    :type new_filename: string
    :param qty_users: quantity of users id's who rated movies
    :type qty_users: integer (between 1 and 200000)
    """
    with open(new_filename, 'w', newline='', encoding='utf-8') as new_fp:
        items = read_data(old_filename, qty_users)
        write = csv.writer(new_fp)
        for line in items:
            write.writerow(line)
    new_fp.close()


# 1º Descomentar esta linha
# write_new_mov_csv_files('original_ratings.csv', 'new_ratings.csv')


def write_sample_movies(original_filename, sampled_movies_filename, number_movies):
    """
    Method that, from csv file of the original movielens movies  (movieId, title, genres), will write to a new csv file
    containing sampled movies (reduced to a certain number of movies)
    :param original_filename: path where the csv file is located (this file must be in csv format and must contain
                             the following columns: movieId, title, genres)
    :type original_filename: string
    :param sampled_movies_filename: path where the new file will be located (this file must be in csv format)
    :type sampled_movies_filename: string
    :param number_movies: number of movies to be sampled (reduced)
    :type number_movies: integer
    """
    items = pd.read_csv(original_filename).sample(n=number_movies)
    items.to_csv(sampled_movies_filename, index=False)


# write_sample_movies('movies.csv','movies_sampled.csv', 10000)


def write_ratings_with_sampled_movies(original_ratings_filename, sampled_movies_filename, new_ratings_filename,
                                      qty_users):
    """
    Method that, from csv file of the original movielens user ratings, will write user ratings made only in sampled
    movies
    :param original_ratings_filename: csv file path where all user ratings are is located (this file must be in csv
                                      format and must contain the following columns: userId, movieId, rating)
    :type original_ratings_filename: strin
    :param sampled_movies_filename: path where the csv file with sampled movies is located (this file must be in csv
                                  format and must contain the following columns: movieId, title, genres)
    :type sampled_movies_filename: string
    :param new_ratings_filename: path where the user ratings in sampled movies csv file will be located (this file must
                                 be in csv format)
    :type new_ratings_filename: string
    :param qty_users: quantity of users id's who rated movies
    :type qty_users: integer (between 1 and 200000)
    """
    with open(new_ratings_filename, 'w', newline='', encoding='utf-8') as new_fp:
        USERID, MOVIEID, RATING = 0, 1, 2
        movies_dict = get_movies_dict(sampled_movies_filename)
        items = read_data(original_ratings_filename, qty_users)
        write = csv.writer(new_fp)
        write.writerow(["userId", "movieTitle", "rating"])
        for line in items:
            if line[MOVIEID] in movies_dict.keys():
                movieTitle = movies_dict[line[MOVIEID]]["Title"]
                new_line = [line[USERID], movieTitle, line[RATING]]
                write.writerow(new_line)
    new_fp.close()


# write_ratings_with_sampled_movies('new_ratings.csv', 'movies_sampled.csv', 'ratings_sampled.csv')


def write_limited_users_ratings(filename, qty_users):
    """
    Method that will write to a new csv file a certain number of user ratings (userRatings5k, 10k,...)
    :param filename: path where the new csv file with a certain quantity of users who rated movies will be located (this
                     file must be in csv format)
    :type filename: string
    :param qty_users: quantity of users id's who rated movies
    :type qty_users: integer (between 1 and 200000)
    """
    with open(filename, 'w', newline='', encoding='utf-8') as new_fp:
        USERID, MOVIEID, RATING = 0, 1, 2
        movies_dict = get_movies_dict('movies.csv')
        items = read_data('../new_ratings.csv', qty_users)
        write = csv.writer(new_fp)
        write.writerow(["userId", "movieTitle", "rating"])
        for line in items:
            movieTitle = movies_dict[line[MOVIEID]]["Title"]
            new_line = [line[USERID], movieTitle, line[RATING]]
            write.writerow(new_line)
    new_fp.close()


# 2º Descomentar esta linha
# write_data('../datasets/userRatings5k.csv')

def write_modified_movies(user_ratings_filename, sampled_movies_filename, new_user_rating_genre_filename, qty_users):
    """
    Method that, from the csv file where all user ratings are, will write a certain quantity of users who made only
    ratings in sampled movies
    :param user_ratings_filename: csv file path where all user ratings are is located (this file must be in csv format
                                  and must contain the following columns: userId, movieId, rating)
    :type user_ratings_filename: string
    :param sampled_movies_filename: path where the csv file with sampled movies is located (this file must be in csv
                                  format and must contain the following columns: movieId, title, genres)
    :type sampled_movies_filename: string
    :param new_user_rating_genre_filename: path where the user ratings with movies genre csv file will be located (this
                                           file must be in csv format and must contain the following columns: userId,
                                           movieTitle, genre,rating)
    :type new_user_rating_genre_filename: string
    :param qty_users: quantity of users id's who rated movies
    :type qty_users: integer (between 1 and 200000)
    """
    with open(new_user_rating_genre_filename, 'w', newline='', encoding='utf-8') as new_fp:
        USERID, MOVIEID, RATING = 0, 1, 2
        movies_dict = get_movies_dict(sampled_movies_filename)
        items = read_data(user_ratings_filename, qty_users)
        write = csv.writer(new_fp)
        write.writerow(["userId", "movieTitle", "genre", "rating"])
        for line in items:
            if line[MOVIEID] in movies_dict.keys():
                movie_title = movies_dict[line[MOVIEID]]["Title"]
                for i in range(len(movies_dict[line[MOVIEID]]["Genres"])):
                    genre = movies_dict[line[MOVIEID]]["Genres"][i]
                    new_line = [line[USERID], movie_title, genre, line[RATING]]
                    write.writerow(new_line)
    new_fp.close()


# write_modified_movies('../new_ratings.csv', '../movies_sampled.csv', 'userRatingsGenre.csv')

def get_movies_genres_list(filename):
    """
    Method that converts a csv file with the movies information (movieId, title, genres) into a list of strings
    :param filename: path where the csv file is located (this file must be in csv format and must contain
                     the following columns: movieId, title, genres)
    :type filename: string
    :return: list of strings that contains all the movies genres
    """
    with open(filename, encoding='utf-8') as fp:
        reader = csv.reader(fp)
        next(reader, None)  # skip the headers
        genres_list = []
        MOVIEID, TITLE, GENRES = 0, 1, 2
        for line in reader:
            genres = line[GENRES].split('|')
            for genre in genres:
                if genre not in genres_list:
                    genres_list.append(genre)

    return genres_list


# print(get_movies_genres_list('datasets/movies.csv'))

def write_movie_genres_files(movies_filename, genres_filename):
    """
    Method that, from the csv file with the movies information (movieId, title, genres), will write to a new csv file
    (genreId, genre)
    :param movies_filename: path where the csv file is located (this file must be in csv format and must contain
                        the following columns: movieId, title, genres)
    :type movies_filename string
    :param genres_filename: path where the new file will be located (this file must be in csv format)
    :type genres_filename: string
    """
    with open(genres_filename, 'w', newline='', encoding='utf-8') as new_fp:
        items = get_movies_genres_list(movies_filename)
        write = csv.writer(new_fp)
        write.writerow(["genreId", "genre"])
        i = 1
        for item in items:
            write.writerow([i, item])
            i += 1
    new_fp.close()


# write_movie_genres_files('datasets/movies.csv', 'datasets/movies_genres.csv')

def get_users_id_list(filename):
    """
    Method that converts a csv file with the movies information (userId, movieTitle, rating) into a list of strings
    :param filename: path where the csv file is located (this file must be in csv format and must contain
                     the following columns: userId, movieTitle, rating)
    :type filename: string
    :return: list of strings that contains all the users id's
    """
    with open(filename, encoding='utf-8') as fp:
        reader = csv.reader(fp)
        next(reader, None)  # skip the headers
        users_list = []
        USERID, MOVIETITLE, RATING = 0, 1, 2
        for line in reader:
            if line[USERID] not in users_list:
                users_list.append(line[USERID])

    return users_list


# print(get_users_id_list('datasets/userRatings5k.csv'))

def get_rules_movies(filename, has_id):
    with open(filename, encoding='utf-8') as fp:
        reader = csv.reader(fp)
        next(reader, None)  # skip the headers
        ant_movies_list = []
        cons_movies_list = []
        if has_id:
            ID, ANTECEDENTS, CONSEQUENTS, ANTECEDENTSUPPORT, CONSEQUENTSUPPORT, SUPPORT, CONFIDENCE, KULC, IBRATIO = 0, 1, 2, 3, 4, 5, 6, 7, 8
        else:
            ANTECEDENTS, CONSEQUENTS, ANTECEDENTSUPPORT, CONSEQUENTSUPPORT, SUPPORT, CONFIDENCE, KULC, IBRATIO = 0, 1, 2, 3, 4, 5, 6, 7

        for line in reader:
            antecedents = ast.literal_eval(line[ANTECEDENTS])
            consequents = ast.literal_eval(line[CONSEQUENTS])
            for antecedent in antecedents:
                if antecedent not in ant_movies_list:
                    ant_movies_list.append(antecedent)
            for consequent in consequents:
                if consequent not in cons_movies_list and consequent not in ant_movies_list:
                    cons_movies_list.append(consequent)

    print("Antecedents no: " + str(len(ant_movies_list)))
    print(ant_movies_list)
    print("Consequents no: " + str(len(cons_movies_list)))
    print(cons_movies_list)
    print()


# get_rules_movies('rulesCsv/rules5kUsersConfImp.csv', True)
# get_rules_movies('rulesCsv/rules5kUsersConfExp.csv', False)
