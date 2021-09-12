import json
import csv
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import association_rules, fpgrowth
from matplotlib import pyplot as plt


def get_csv_headers(filename):
    """
    Method that returns a list with all headers of a csv file
    :param filename: path where the csv file is located (this file must be in csv format)
    :type filename: string
    :return: list with all headers of a csv file
    """
    # reading the csv file using read_csv
    # storing the data frame in variable called df
    df = pd.read_csv(filename)

    # creating a list of column names by
    # calling the .columns
    list_of_column_names = list(df.columns)

    return list_of_column_names


# print(get_csv_headers('new_movies.csv'))

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


def generate_frequent_items_dataset(filename, is_implicit, top_n):
    """
    Method that returns the top X, X is the number of movies defined by the user, of most frequent movies in the dataset
    :param filename: path where the csv file is located (this file must be in csv format and must contain
    the following columns: userId, movieTitle, rating)
    :type filename: string
    :param is_implicit: if the data is implicit or explicit (False = explicit data, True = implicit data)
    :type is_implicit: boolean
    :param top_n: number that define the top of frequent movies in the dataset
    :type top_n: integer
    :return: frequent itemsets in dataset
    """
    movies_list_set = read_data(filename, is_implicit)
    movies_freq_dict = {}
    for movies in movies_list_set:
        for movie in movies:
            if movie in movies_freq_dict.keys():
                movies_freq_dict[movie] += 1
            else:
                movies_freq_dict[movie] = 1

    dfMoviesFreqDict = pd.DataFrame(list(movies_freq_dict.items()),
                                    columns=['Movie', 'Absolute Count']).sort_values('Absolute Count',
                                                                                     ascending=False)[0:top_n]
    return dfMoviesFreqDict


print(generate_frequent_items_dataset('datasets/userRatings5k.csv', True, 50).to_string())


# print(json.dumps(generate_frequent_items_dataset('datasets/userRatings5k.csv'), ensure_ascii=False, indent=2))


def generate_frequent_itemsets(filename, min_support, is_implicit):
    """
    Method that generates frequent itemsets using fp-growth algorithm
    :param filename: path where the csv file is located (this file must be in csv format and must contain
    the following columns: userId, movieTitle, rating)
    :type filename: string
    :param min_support: minimum support for the frequent itemsets
    :type min_support: float
    :param is_implicit: if the data is implicit or explicit (False = explicit data, True = implicit data)
    :type is_implicit: boolean
    :return: frequent itemsets in DataFrame type
    """
    trans_full = read_data(filename, is_implicit)
    # print(transFull)  # Output of transfull (list of lists of items)
    # Encoding transactions (Representation of the items in the list in 0's and 1's)

    # Initialize one hot encoding transactions
    one_hot_encoding = TransactionEncoder()

    # Data is transformed into one hot encoding format
    one_hot_trans = one_hot_encoding.fit(trans_full).transform(trans_full)

    # Converted into dataframe
    one_hot_trans_df = pd.DataFrame(one_hot_trans, columns=one_hot_encoding.columns_)
    # Output of items dataframe transformed into a binary data (one hot encoding)
    # print(one_hot_trans_df.head(5))
    # print('Number of columns :', one_hot_trans_df.shape[1])

    # Generating association rules
    freq_prod = fpgrowth(one_hot_trans_df, min_support=min_support, use_colnames=True)
    # print(freq_prod.to_string())  # Output of frequent products rules

    return freq_prod


# print(generate_frequent_itemsets(filename="datasets/userRatings5k.csv", min_support=0.1).sort_values('support',
#                                                                                                      ascending=False)[
#       0:50].to_string())


def group_itemsets(filename, min_support, is_implicit):
    """
    Method that forms groups of itemsets and stores it into a dictionary with the following format:
    { "Grupos de X":[ "Itemset", ... ] }
    :param filename: path where the csv file is located (this file must be in csv format and must contain
    the following columns: userId, movieTitle, rating)
    :type filename: string
    :param min_support: minimum support for the frequent itemsets
    :type min_support: float
    :param is_implicit: if the data is implicit or explicit (False = explicit data, True = implicit data)
    :type is_implicit: boolean
    :return: dictionary with the following format: { "Grupos de X":[ "Itemset", ... ] }
    """
    freq_items = generate_frequent_itemsets(filename, min_support, is_implicit)
    freq_items_dict = {}

    for item in freq_items['itemsets']:
        itemsets_key = "Grupos de " + str(len(list(item)))
        itemset = ",".join(list(item))
        if itemsets_key in freq_items_dict.keys():
            freq_items_dict[itemsets_key].append(itemset)
        else:
            freq_items_dict[itemsets_key] = [itemset]

    return freq_items_dict


# print(json.dumps(group_itemsets('datasets/userRatings5k.csv', 0.2, False), ensure_ascii=False, indent=2))


def generate_bar_plot_frequent_items(filename, is_implicit, top_n):
    """
    Method that generates a frequent itemsets bar plot
    :param filename: path where the csv file is located (this file must be in csv format and must contain
    the following columns: userId, movieTitle, rating)
    :type filename: string
    :param is_implicit: if the data is implicit or explicit (False = explicit data, True = implicit data)
    :type is_implicit: boolean
    :param top_n: number that will defines the top of frequent movies in the dataset
    :type top_n: integer
    :return: frequent itemsets bar plot
    """
    df = generate_frequent_items_dataset(filename, is_implicit, top_n)

    movies = df["Movie"]
    abscounts = df["Absolute Count"]

    # plt.rc('axes', labelsize=13)  # fontsize of the x and y labels
    # plt.rc('xtick', labelsize=13)  # fontsize of the x tick labels
    # plt.rc('ytick', labelsize=13)  # fontsize of the y tick labels
    # Figure Size
    fig, ax = plt.subplots(figsize=(25.5, 7))

    # Horizontal Bar Plot
    ax.barh(movies, abscounts)

    # Remove axes splines
    for s in ['top', 'bottom', 'left', 'right']:
        ax.spines[s].set_visible(False)

    # Remove x, y Ticks
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')

    # Add padding between axes and labels
    ax.xaxis.set_tick_params(pad=5)
    ax.yaxis.set_tick_params(pad=10)

    # Add x, y gridlines
    ax.grid(b=True, color='grey',
            linestyle='-.', linewidth=0.5,
            alpha=0.2)

    # Show top values
    ax.invert_yaxis()

    # Add annotation to bars
    for i in ax.patches:
        plt.text(i.get_width() + 0.2, i.get_y() + 0.5,
                 str(round((i.get_width()), 2)),
                 fontsize=15, fontweight='bold',
                 color='grey')

    # Add Plot Title
    ax.set_title('Items do dataset e a sua ocorrência',
                 loc='center')
    ax.set_ylabel('Filmes')
    ax.set_xlabel('Nº Ocorrências')

    # Show Plot
    plt.show()


# generate_bar_plot_frequent_items('datasets/userRatings5k.csv', True, 10)
