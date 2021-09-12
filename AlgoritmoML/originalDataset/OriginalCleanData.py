import csv
import json
import pandas as pd


def read_data(filename):
    """
    Method that reads from a csv file and returns a list of transactions with all users' items
    :param filename: path where the file is located (this file must be in csv)
    :type filename: string
    :return: list of transactions with all users' items
    """
    # Open the file
    with open(filename, encoding='utf-8') as fp:
        reader = csv.reader(fp)
        next(reader, None)  # skip the headers
        i = 0
        ratingsList = []
        for line in reader:
            if line[0] == '5001':
                break
            new_line = [line[0], line[1], line[2]]
            ratingsList.append(new_line)

    return ratingsList


# print(read_data('movies.csv'))

# Converte um ficheiro csv com as colunas (movieId,title,genres) no dicionário ({ MovieId: { Title: ... , Genres = [] } })
def get_movies_dict(filename):
    # Open the file
    with open(filename, encoding='utf-8') as fp:
        reader = csv.reader(fp)
        next(reader, None)  # skip the headers
        moviesDict = {}
        # moviesDict = { MovieId: { Title: ... , Genres = [] }  }
        MOVIEID, TITLE, GENRES = 0, 1, 2
        for line in reader:
            # print(line_content[3])
            genres = line[GENRES].split('|')
            if line[MOVIEID] in moviesDict.keys():
                moviesDict[line[MOVIEID]].append({"Title": line[TITLE], "Genres": genres})
            else:
                moviesDict[line[MOVIEID]] = {"Title": line[TITLE], "Genres": genres}

    return moviesDict


# print(json.dumps(get_movies_dict('movies.csv'), ensure_ascii=False, indent=2))

# Escreve um ficheiro csv para
def write_new_mov_csv_files(oldFilename, newFilename):
    with open(newFilename, 'w', newline='', encoding='utf-8') as new_fp:
        items = read_data(oldFilename)
        write = csv.writer(new_fp)
        for line in items:
            write.writerow(line)
    new_fp.close()


# Escreve, a partir do ficheiro original (movies.csv), um ficheiro csv com o conteúdo do ficheiro original reduzido a um
# determinado nº de filmes
def write_sample_movies(filename, originalFilename, numberMovies):
    items = pd.read_csv(originalFilename).sample(n=numberMovies)
    items.to_csv(filename, index=False)


# write_sample_movies('movies_sampled.csv', 'movies.csv', 10000)

# Escreve para um ficheiro csv, o conteúdo do ficheiro "new_ratings.csv", os ratings os utilizadores num determinado
# grupo de filmes
def write_ratings_with_sampled_movies(originalFilename, newFilename, sampledFilename):
    with open(newFilename, 'w', newline='', encoding='utf-8') as new_fp:
        USERID, MOVIEID, RATING = 0, 1, 2
        moviesDict = get_movies_dict(sampledFilename)
        items = read_data(originalFilename)
        write = csv.writer(new_fp)
        write.writerow(["userId", "movieTitle", "rating"])
        for line in items:
            if line[MOVIEID] in moviesDict.keys():
                movieTitle = moviesDict[line[MOVIEID]]["Title"]
                new_line = [line[USERID], movieTitle, line[RATING]]
                write.writerow(new_line)
    new_fp.close()


# write_ratings_with_sampled_movies('new_ratings.csv', 'ratings_sampled.csv', 'movies_sampled.csv')


# 1º Descomentar esta linha
# write_new_mov_csv_files('original_ratings.csv', 'new_ratings.csv')

# Escreve para um ficheiro csv com as colunas (userId,movieTitle,rating) (userRatings5k, 10k,...)
def write_data(filename):
    with open(filename, 'w', newline='', encoding='utf-8') as new_fp:
        USERID, MOVIEID, RATING = 0, 1, 2
        moviesDict = get_movies_dict('movies.csv')
        items = read_data('../datasets/new_ratings.csv')
        write = csv.writer(new_fp)
        write.writerow(["userId", "movieTitle", "rating"])
        for line in items:
            movieTitle = moviesDict[line[MOVIEID]]["Title"]
            new_line = [line[USERID], movieTitle, line[RATING]]
            write.writerow(new_line)
    new_fp.close()

# 2º Descomentar esta linha
# write_data('../datasets/userRatings5k.csv')
