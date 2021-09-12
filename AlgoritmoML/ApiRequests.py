import json
import csv
import pandas as pd
from tmdbv3api import TMDb, Movie
from tmdbv3api.exceptions import TMDbException


def read_data(filename, is_implicit):
    """
    Method that reads from a csv file and returns a list movies rated from the users
    :param filename: path where the csv file is located (this file must be in csv format and must contain
    the following columns: userId, movieTitle, rating)
    :type filename: string
    :param is_implicit: if the data is implicit or explicit (False = explicit data, True = implicit data)
    :type is_implicit: boolean
    :return: list of transactions with all users' items
    """
    with open(filename, encoding='utf-8') as fp:
        USERID, MOVIETITLE, RATING = 0, 1, 2
        reader = csv.reader(fp)
        next(reader, None)  # skip the headers
        ratings_dict = {}
        if is_implicit:
            for line in reader:
                if line[USERID] in ratings_dict.keys():
                    ratings_dict[line[USERID]].append((line[MOVIETITLE]))
                else:
                    ratings_dict[line[USERID]] = [(line[MOVIETITLE])]
        else:
            for line in reader:
                if float(line[RATING]) >= 3.0:
                    if line[USERID] in ratings_dict.keys():
                        ratings_dict[line[USERID]].append((line[MOVIETITLE]))
                    else:
                        ratings_dict[line[USERID]] = [(line[MOVIETITLE])]
    fp.close()

    return list(ratings_dict.values())


# print(json.dumps(read_data('datasets/userRatings5k.csv',isImplicit=False), ensure_ascii=False, indent=2))

def get_user_ratings_movies_dict(filename, is_implicit):
    """
    Method that returns a dictionary with the movies frequency in a certain csv file
    :param filename: path where the csv file is located (this file must be in csv format and must contain
    the following columns: userId, movieTitle, rating)
    :type filename: string
    :param is_implicit: if the data is implicit or explicit (False = explicit data, True = implicit data)
    :type is_implicit: boolean
    :return: dictionary that contains the movies frequency with the following format: { "MovieName": no. of ocorrences }
    """
    moviesListSet = read_data(filename, is_implicit)
    moviesFreqDict = {}
    for movies in moviesListSet:
        for movie in movies:
            if movie in moviesFreqDict.keys():
                moviesFreqDict[movie] += 1
            else:
                moviesFreqDict[movie] = 1

    return moviesFreqDict


# print(json.dumps(get_user_ratings_movies_dict('datasets/userRatings5k.csv', isImplicit=False), ensure_ascii=False,
#                  indent=2))

def get_movies_dict(filename):
    """
    Method that converts a csv file with the movies information (movieId, title, genres) into a dictionary ({ MovieId: { Title: ... } })
    :param filename: path where the csv file is located (this file must be in csv format and must contain
    the following columns: movieId, title, genres)
    :type filename: string
    :return: dictionary that contains the following format: { MovieId: { Title: ... }, ... }
    """
    with open(filename, encoding='utf-8') as fp:
        reader = csv.reader(fp)
        next(reader, None)  # skip the headers
        movies_dict = {}
        # moviesDict = { MovieId: { Title: ... }  }
        MOVIEID, TITLE = 0, 1
        for line in reader:
            if line[MOVIEID] in movies_dict.keys():
                movies_dict[line[MOVIEID]].append({"Title": line[TITLE]})
            else:
                movies_dict[line[MOVIEID]] = {"Title": line[TITLE]}
    fp.close()

    return movies_dict


# print(json.dumps(get_movies_dict('new_movies.csv'), ensure_ascii=False, indent=2))


# Number of unique movies in dataset
# df = pd.read_csv("datasets/userRatings5k.csv")
# print(df["movieTitle"].nunique())

def get_movies_id_dict(filename):
    """
    Method that converts a csv file (link.csv) (movieId, imdbId, tmdbId) into a dictionary with the following format:
    { MovieId: { IMDBID: ..., TMDBID: ... } }
    :param filename: path where the csv file is located (this file must be in csv format and must contain
    the following columns: movieId, imdbId, tmdbId)
    :type filename: string
    :return: dictionary that contains the following format: { MovieId: { IMDBID: ..., TMDBID: ... } }
    """
    with open(filename, encoding='utf-8') as fp:
        reader = csv.reader(fp)
        next(reader, None)  # skip the headers
        movies_id_dict = {}
        # moviesDict = { MovieId: { IMDBID: ..., TMDBID: ... } }
        MOVIEID, IMDBID, TMDBID = 0, 1, 2
        for line in reader:
            imdb_id = ""
            if len(line[IMDBID]) < 7:
                nZeros = 7 - len(line[IMDBID])
                for zero in range(nZeros):
                    imdb_id += "0"
                imdb_id += line[IMDBID]
            else:
                imdb_id = line[IMDBID]
            if line[MOVIEID] in movies_id_dict.keys():

                movies_id_dict[line[MOVIEID]].append({"IMDBID": imdb_id, "TMDBID": line[TMDBID]})
            else:
                movies_id_dict[line[MOVIEID]] = {"IMDBID": imdb_id, "TMDBID": line[TMDBID]}
    fp.close()

    return movies_id_dict


def get_modified_movies_dict(filename):
    """
    Method that converts a csv file (movies_modi.csv.csv) (movieId, title, genres, imdbId) into a dictionary with the following format:
    { MovieId: { Title: ... , IMDBID: ... } }
    :param filename: path where the csv file is located (this file must be in csv format and must contain
    the following columns: movieId, title, genres, imdbId)
    :type filename: string
    :return: dictionary that contains the following format: { MovieId: { Title: ... , IMDBID: ... } }
    """
    MOVIEID, MOVIETITLE, GENRES, IMDBID = 0, 1, 2, 3
    with open(filename, encoding='utf-8') as fp:
        reader = csv.reader(fp)
        next(reader, None)  # skip the headers
        modified_movies_dict = {}
        # moviesModiDict = { MovieId: { Title: ... , IMDBID: ... } }
        for line in reader:
            if line[MOVIEID] in modified_movies_dict.keys():
                modified_movies_dict[line[MOVIEID]].append({"Title": line[MOVIETITLE], "IMDBID": line[IMDBID]})
            else:
                modified_movies_dict[line[MOVIEID]] = {"Title": line[MOVIETITLE], "IMDBID": line[IMDBID]}
    fp.close()

    return modified_movies_dict


# print(json.dumps(get_movies_modi_dict('movies_modi.csv'), ensure_ascii=False, indent=2))

def write_movies_with_more_data(new_movies_filename, old_movies_filename, api_key):
    """
    Method that writes to a new csv file (movieID, title, genres, imdbid, tmdbid, released_date, year, poster), where
    the attributes "released_date" and "poster" are obtained from the TMDB api with the help of the library tmdbv3api
    If a movie doesnt have a poster url it will be assigned a default poster url
    :param new_movies_filename: path where the new file will be located (this file must be in csv format)
    :type new_movies_filename: string
    :param old_movies_filename: path where the csv file is located (this file must be in csv format and must contain
                                the following columns: movieId, title, genres, imdbId, tmdbId)
    :type old_movies_filename: string
    :param api_key: TMDB api key
    :type api_key: string
    """
    # Movie url default: https://user-images.githubusercontent.com/44362304/120392750-d5529780-c328-11eb-82b5-568eb31b9145.jpg
    with open(new_movies_filename, 'w', newline='', encoding='utf-8') as movies_modified:
        # movieId, title, genres, imdbId, tmdbId, released_date, year, poster, overview
        with open(old_movies_filename, encoding='utf-8') as new_movies_modified:
            i = 0
            MOVIEID, MOVIETITLE, GENRES, IMDBID, TMDBID = 0, 1, 2, 3, 4
            reader_modified_movies = csv.reader(new_movies_modified)
            tmdb = TMDb()
            tmdb.api_key = api_key
            movie = Movie()
            write = csv.writer(movies_modified)
            write.writerow(
                ["movieId", "title", "genres", "imdbId", "tmdbId", "released_date", "year", "poster", "overview"])
            next(reader_modified_movies, None)  # skip the headers
            not_found_arr = ['12773', '17882', '68149', '24549', '14980', '164721', '140207', '192936', '876', '2413',
                             '82205', '149645', '8677', '13057', '119324', '2670', '215993', '47350', '13519', '152426',
                             '30983', '7096', '15738', '11944', '110147', '15024', '206216', '19341', '2518', '36763',
                             '64699', '69234', '13716', '11343', '185441', '18976', '10700', '24019', '37525', '15594',
                             '24269', '41758', '58923', '17266', '17919', '253768', '78057', '34573', '27138', '49870',
                             '244797', '21847', '31653', '14305', '13541', '118309', '225130', '114796', '17800',
                             '13905',
                             '12224', '9795', '18884', '14301', '38870', '168643', '19350', '18901', '67479', '67463',
                             '19422', '200039', '65990', '17632', '61872', '113879', '58589', '202855', '45988',
                             '25950',
                             '200664', '141714', '61917', '61919', '61920', '211877', '37106', '31261', '41522',
                             '47477',
                             '96451', '59572', '24219', '133252', '11788', '183894', '110639', '367647', '202241',
                             '20881', '15533', '71982', '67636', '51765', '75375', '69487', '58423', '94174', '262475',
                             '60364', '20892', '192695', '62582', '99254', '26397', '168210', '46813', '147269',
                             '206997',
                             '284694', '170359', '200157', '168332', '378452', '208988', '57346', '83191', '193976',
                             '233984', '53803', '118013', '202043', '216035', '263946', '263947', '215999', '117408',
                             '172538', '119431', '232005', '142051', '51982', '193380', '147538', '57290', '69372',
                             '62403', '101517', '273740', '95571', '156078', '166918', '162806', '134481', '56508',
                             '89049', '2966', '281788', '355551', '194668', '114049', '114761', '155055', '4548',
                             '241340', '136991', '64820', '63383', '124531', '51452', '166986', '129405', '253941',
                             '176297', '18231', '252995', '252993', '239471', '211779', '230657', '40593', '245170',
                             '54102', '110414', '313289', '169224', '370353', '218277', '257155', '64047', '222481',
                             '38626', '267795', '106938', '239163', '30146', '21680', '53870', '86997', '297167',
                             '67493',
                             '264330', '298573', '31446', '103081', '12450', '178446', '97414', '159140', '289314',
                             '36597', '203766', '82400', '276690', '29133', '144114', '248785', '24486', '2699',
                             '312497',
                             '65821', '301231', '62836', '151153', '62653', '74309', '125458', '289394', '101660',
                             '18729', '140161', '31183', '63039', '133365', '77172', '18202', '51768', '136867',
                             '69234',
                             '150004', '266314', '108716', '67866', '76162', '197592', '25093', '13535', '57622',
                             '162864', '67456', '53285', '189197', '317384', '238386', '252063', '64123', '278468',
                             '22211', '138394', '122023', '315010', '160874', '264321', '30496', '80527', '56771']
            for line in reader_modified_movies:
                i += 1
                if line[TMDBID] not in not_found_arr and line[TMDBID] != '':
                    m = movie.details(int(line[TMDBID]))
                    print("TMDBID:" + line[TMDBID])
                    if m.release_date is not None and m.release_date != "":
                        if m.poster_path is not None:
                            poster = "https://image.tmdb.org/t/p/original" + str(m.poster_path)
                        else:
                            poster = "https://user-images.githubusercontent.com/44362304/120392750-d5529780-c328-11eb-82b5-568eb31b9145.jpg"
                        if m.overview is not None or m.overview != "":
                            overview = m.overview
                        else:
                            overview = "Movie's overview not available"
                        releaseDate = m.release_date
                        new_released_date = releaseDate.split('-')[2] + "/" + releaseDate.split('-')[1] + "/" + \
                                            releaseDate.split('-')[0]
                        year = releaseDate.split('-')[0]

                        new_line = [line[MOVIEID], line[MOVIETITLE], line[GENRES], line[IMDBID], line[TMDBID],
                                    new_released_date,
                                    year, poster, overview]
                        write.writerow(new_line)
                print(str(i))
        new_movies_modified.close()
    movies_modified.close()


write_movies_with_more_data('datasets/new_movies_data.csv', 'datasets/modified_movies.csv',
                            '416556d32aa949c4738c5d43067c3293')


def get_not_found_movies_api(new_modified_movies_filename, api_key):
    """
    Method that returns a list with all movie's tmdbids that weren't found in the tmdb api
    :param new_modified_movies_filename: path where the csv file is located (this file must be in csv format and must contain
                                         the following columns: movieID, title, genres, imdbid, tmdbid)
    :type new_modified_movies_filename: string
    :param api_key: TMDB api key
    :type api_key: string
    :return: list of movie's tmdbids that weren't found in the tmdb api
    """
    with open(new_modified_movies_filename, encoding='utf-8') as new_movies_modi:
        i = 0
        noTMDBID = 0
        MOVIEID, MOVIETITLE, GENRES, IMDBID, TMDBID = 0, 1, 2, 3, 4
        readerMoviesMovi = csv.reader(new_movies_modi)
        next(readerMoviesMovi, None)  # skip the headers
        tmdb = TMDb()
        tmdb.api_key = api_key
        movie = Movie()
        notFoundArr = []
        for line in readerMoviesMovi:
            try:
                i += 1
                if line[TMDBID] != '':
                    movie.details(int(line[TMDBID]))
                else:
                    noTMDBID += 1
            except TMDbException:
                notFoundArr.append(line[TMDBID])
            print(str(i))
        print("Nº de filmes que não tinham TMDBID: " + noTMDBID)
        print("Nº de filmes não econtrados na API: " + str(len(notFoundArr)))
    new_movies_modi.close()
    return notFoundArr


def verify_api(new_modified_movies_filename, api_key):
    """
    Method that verifies if it doesn't exists any problem about all movies requests made to the api
    :param new_modified_movies_filename: path where the csv file is located (this file must be in csv format and must
                                         contain the following columns: movieID, title, genres, imdbid, tmdbid)
    :type new_modified_movies_filename: string
    :param api_key: TMDB api key
    :type api_key: string
    :return:
    """
    with open(new_modified_movies_filename, encoding='utf-8') as new_movies_modified:
        MOVIEID, MOVIETITLE, GENRES, IMDBID, TMDBID = 0, 1, 2, 3, 4
        reader_modified_movies = csv.reader(new_movies_modified)
        next(reader_modified_movies, None)  # skip the headers
        tmdb = TMDb()
        tmdb.api_key = api_key
        movie = Movie()
        none_arr = []
        not_found_arr = []
        no_tmdbid_arr = []
        i = 0
        for line in reader_modified_movies:
            try:
                i += 1
                if line[TMDBID] != '':
                    m = movie.details(int(line[TMDBID]))
                    if m.release_date is None:
                        none_arr.append(line[TMDBID])
                else:
                    no_tmdbid_arr.append(line[TMDBID])
            except TMDbException:
                not_found_arr.append(line[TMDBID])
            print(str(i))
        print("Nº de filmes que a release_date foi null: " + str(len(none_arr)))
        # Output: Nº de filmes que a release_date foi null: 0
        print(none_arr)
        print("Nº de filmes que não tinham TMDBID: " + str(len(no_tmdbid_arr)))
        # Output: Nº de filmes que não tinham TMDBID: 249
        print(no_tmdbid_arr)
        # Output: Nº de filmes não econtrados na API: 266
        print("Nº de filmes não econtrados na API: " + str(len(not_found_arr)))
        print(not_found_arr)
    new_movies_modified.close()


# verify_api('movies_modi.csv', '416556d32aa949c4738c5d43067c3293')


def write_movies_imdbId_modified(original_movies_filename, movies_id_filename, new_movies_filename):
    """
    Method that joins the csv files movies.csv and link.csv into a new csv file with the following columns:
    movieId, title, genres, imdbId, tmdbId
    :param original_movies_filename: path where the csv file is located (this file must be in csv format and must
                                     contain the following columns: movieId, title, genres)
    :type original_movies_filename: string
    :param movies_id_filename: path where the csv file is located (this file must be in csv format and must contain
                               the following columns: movieId, imdbId, tmdbId)
    :type movies_id_filename: string
    :param new_movies_filename: path where the new file will be located (this file must be in csv format)
    :type new_movies_filename: string
    """
    with open(new_movies_filename, 'w', newline='', encoding='utf-8') as write_fp:
        with open(original_movies_filename, encoding='utf-8') as read_old_movies:
            reader_old_movies = csv.reader(read_old_movies)
            next(reader_old_movies, None)  # skip the headers
            movies_id_dict = get_movies_id_dict(movies_id_filename)
            write = csv.writer(write_fp)
            write.writerow(["movieId", "title", "genres", "imdbId", "tmdbId"])
            MOVIEID, TITLE, GENRES = 0, 1, 2
            for line in reader_old_movies:
                if line[MOVIEID] in movies_id_dict.keys():
                    new_line = [line[MOVIEID], line[TITLE], line[GENRES], movies_id_dict[line[MOVIEID]]["IMDBID"],
                                movies_id_dict[line[MOVIEID]]["TMDBID"]]
                    # print(new_line)
                    write.writerow(new_line)
        read_old_movies.close()
    write_fp.close()

# write_movies_imdbId_modified('new_movies.csv', 'link.csv', 'movies_modi.csv')
