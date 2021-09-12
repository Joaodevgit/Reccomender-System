import csv

import pandas as pd
from mlxtend.frequent_patterns import association_rules, fpgrowth
from mlxtend.preprocessing import TransactionEncoder


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


# print(len(read_data(filename='datasets/userRatings5k.csv', is_implicit=False)))
# print(json.dumps(filename=read_data('new_movies_id_small.csv', is_implicit=False), ensure_ascii=False, indent=2))


def calculate_kulczynski(sup_a, sup_b, sup_ab, total_transactions):
    """
    Method that calculates the Kulczynski metric of an association rule
    :param sup_a: support count of antecedents
    :type sup_a: float
    :param sup_b: support count of consequents
    :type sup_b: float
    :param sup_ab: support count of antecedents and consequents
    :type sup_ab: float
    :param total_transactions: number of total transactions
    :type total_transactions: integer
    :return: Kulczynski result of an association rule
    """
    # Absolute Support A
    abs_sup_countA = round(sup_a * total_transactions)

    # Absolute Support B
    abs_sup_countB = round(sup_b * total_transactions)

    # Absolute Support (A U B)
    abs_sup_countAB = round(sup_ab * total_transactions)

    # P(B|A)
    pBA = round(abs_sup_countAB / abs_sup_countA, 6)

    # P(A|B)
    pAB = round(abs_sup_countAB / abs_sup_countB, 6)

    return round(0.5 * (pAB + pBA), 6)


# Output: ~0.244106
# print(calculate_kulczynski(sup_a=0.052466, sup_b=0.255516, sup_ab=0.021251, total_transactions=9835))


def calculate_imbalance_ratio(sup_a, sup_b, sup_ab, total_transactions):
    """
    Method that calculates the imbalance ratio metric of an association rule
    :param sup_a: support count of antecedents
    :type sup_a: float
    :param sup_b: support count of consequents
    :type sup_b: float
    :param sup_ab: support count of antecedents and consequents
    :type sup_ab: float
    :param total_transactions: number of total transactions
    :type total_transactions: integer
    :return: Imbalance ratio result of an association rule
    """
    # Absolute Support A
    abs_sup_countA = round(sup_a * total_transactions)

    # Absolute Support B
    abs_sup_countB = round(sup_b * total_transactions)

    # Absolute Support (A U B)
    abs_sup_countAB = round(sup_ab * total_transactions)

    return round((abs(abs_sup_countA - abs_sup_countB)) / (abs_sup_countA + abs_sup_countB - abs_sup_countAB), 6)


# Output: 0.708156
# print(calculate_imbalance_ratio(sup_a=0.052466, sup_b=0.255516, sup_ab=0.021251, total_transactions=9835))


def generate_association_rules(filename, is_implicit, min_support, rule_metric, rule_metric_threshold):
    """
    Method that generates association rules
    :param filename: path where the csv file is located (this file must be in csv format and must contain
    the following columns: userId, movieTitle, rating)
    :type filename: string
    :param is_implicit: if the data is implicit or explicit (False = explicit data, True = implicit data)
    :type is_implicit: boolean
    :param min_support: minimum support for the association rules
    :type min_support: float
    :param rule_metric: metric rule for the association rules
    :type rule_metric: string (it only accepts support,confidence, lift, leverage, conviction)
    :param rule_metric_threshold: minimum value of metric rule
    :type rule_metric_threshold: float
    :param is_implicit: if the data is implicit or explicit (False = explicit data, True = implicit data)
    :type is_implicit: boolean
    :return: association rules in DataFrame type
    """
    trans_full = read_data(filename, is_implicit)
    # print(trans_full)  # Output of transfull (list of lists of items)
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

    # Generating association rules with a certain metric and its threshold value
    rules = association_rules(freq_prod, metric=rule_metric, min_threshold=rule_metric_threshold)

    return rules


# min_support=0.1 e min_confidence=0.6
# print(generate_association_rules(filename="datasets/userRatings5k.csv", is_implicit=True, min_support=0.1,
#                                  rule_metric="confidence",
#                                  rule_metric_threshold=0.6).to_string())


def generate_association_rules_kulc_imbalance(filename, is_implicit, min_support, rule_metric, min_rule_metric_value,
                                              min_kulc_value,
                                              min_imbalance_ratio_value):
    """
    Method that will generate rules based on values assigned to Kulczynski and Imbalance Ratio
    :param filename: path where the csv file is located (this file must be in csv format and must contain
    the following columns: userId, movieTitle, rating)
    :param is_implicit: if the data is implicit or explicit (False = explicit data, True = implicit data)
    :type is_implicit: boolean
    :param min_support: minimum support for the association rules
    :type min_support: float
    :param rule_metric: metric rule for the association rules
    :type rule_metric: string (it only accepts support,confidence, lift, leverage, conviction)
    :param min_rule_metric_value: minimum value of metric rule
    :type min_rule_metric_value: float
    :param min_kulc_value: minimum value of Kulczynski metric
    :type min_kulc_value: float
    :param min_imbalance_ratio_value: minimum value of Imbalance Ratio metric
    :type min_imbalance_ratio_value: float
    :return: association rules (in dataframe) with the defined metrics
    """
    list_transactions_size = len(read_data(filename, is_implicit))
    association_rules = generate_association_rules(filename, is_implicit, min_support, rule_metric,
                                                   min_rule_metric_value)
    # print(association_rules.to_string()) # Output of all association rules with metrics applied
    temp_user_rules_association = []
    association_rules_list = []
    for ruleInfo in association_rules.itertuples():
        new_rule = {'antecedents': ruleInfo.antecedents,
                    'consequents': ruleInfo.consequents,
                    'antecedent support': ruleInfo._3,
                    'consequent support': ruleInfo._4,
                    'support': ruleInfo.support,
                    'confidence': ruleInfo.confidence,
                    'lift': ruleInfo.lift,
                    'kulczynski': calculate_kulczynski(sup_a=ruleInfo._3, sup_b=ruleInfo._4, sup_ab=ruleInfo.support,
                                                       total_transactions=list_transactions_size),
                    'imbalance ratio': calculate_imbalance_ratio(sup_a=ruleInfo._3, sup_b=ruleInfo._4,
                                                                 sup_ab=ruleInfo.support,
                                                                 total_transactions=list_transactions_size)}
        temp_user_rules_association.append(new_rule)

        # The more lesser Imbalance Ratio is, better (0 = perfectly balanced, 1 = unbalanced) and the more greater
        # Kulczynski is better (0.5 = not interesting rule, Close to 0 = itemsets negatively associated,
        # Close to 1 = itemsets positively associated)
    for userRuleAssociation in temp_user_rules_association:
        if userRuleAssociation['imbalance ratio'] <= min_imbalance_ratio_value and userRuleAssociation[
            'kulczynski'] >= min_kulc_value:
            association_rules_list.append(userRuleAssociation)

    rules = pd.DataFrame(association_rules_list)

    return rules


# rules = generate_association_rules_kulc_imbalance(filename='datasets/userRatings5k.csv',
#                                                   is_implicit=True,
#                                                   min_support=0.1,
#                                                   rule_metric="confidence", min_rule_metric_value=0.6,
#                                                   min_kulc_value=0.6,
#                                                   min_imbalance_ratio_value=0.3)


# print(rules.to_string())


# print(rules.shape[0])


def get_all_movies(movies_filename):
    """
    Method that returns a list of all movies in  a csv file
    :param movies_filename: path where the csv file is located (this file must be in csv format and must contain
    the following columns: movieId, title, genres, imdbid, tmdbid, release_date, year, poster)
    :type movies_filename: string
    :return: list of movies
    """
    with open(movies_filename, encoding='utf-8') as fp:
        reader = csv.reader(fp)
        next(reader, None)  # skip the headers
        movies_list = []
        MOVIEID, TITLE, GENRES, IMDBID, TMDBID, RELEASEDDATE, YEAR, POSTER = 0, 1, 2, 3, 4, 5, 6, 7
        for line in reader:
            movies_list.append(line[TITLE])
    fp.close()

    return movies_list


# print(get_all_movies('datasets/movies.csv'))


def verify_movie_exists(movies_filename, user_list_movies):
    """
    Method that given a user list movies verifies if any movie exists or not
    :param movies_filename: path where the csv file is located (this file must be in csv format and must contain
    the following columns: movieId, title, genres, imdbid, tmdbid, release_date, year, poster)
    :type movies_filename: string
    :param user_list_movies: user list movies
    :type user_list_movies: list of string
    :return:
    """
    movies = get_all_movies(movies_filename)
    movies_not_found = []
    for userMovie in user_list_movies:
        if userMovie not in movies:
            movies_not_found.append(userMovie)

    return movies_not_found


# print(verify_movie_exists('new_movies.csv'))

def get_popular_rules_movies(rules, no_movies, user_movies):
    """
    Method that returns the most popular movies based on the user movies list
    :param rules: association rules generated
    :type rules: dataframe
    :param no_movies: number of popular movies
    :type no_movies: integer
    :param user_movies: user movies list
    :type user_movies: list of strings
    :return: list of popular movies with lenght of noMovies
    """
    pop_items = []
    for popRule in rules.sort_values('confidence', ascending=False).itertuples():
        consequents = list(frozenset(popRule.consequents))
        for consequent in consequents:
            if consequent not in pop_items and len(pop_items) < no_movies and consequent not in user_movies:
                pop_items.append(consequent)
            if len(pop_items) == no_movies:
                return pop_items


def recommend_to_user(list_user_movies, is_implicit, filename, movies_filename, min_support, rule_metric,
                      min_rule_metric_value,
                      min_kulc_value,
                      min_imbalance_ratio_value, top_n):
    """
    Method that returns top n recommended items
    :param list_user_movies: list of items that user liked/interacted with
    :type list_user_movies: string list
    :param is_implicit: if the data is implicit or explicit (False = explicit data, True = implicit data)
    :type is_implicit: boolean
    :param filename: path where the csv file is located (this file must be in csv format and must contain
    the following columns: userId, movieTitle, rating)
    :type filename: string
    :param min_support: minimum support for the association rules
    :type min_support: float (values between 0.0 and 1.0)
    :param rule_metric: metric rule for the association rules
    :type rule_metric: string (it only accepts support,confidence, lift, leverage, conviction)
    :param min_rule_metric_value: minimum value of metric rule
    :type min_rule_metric_value: float
    :param min_kulc_value: minimum value of kulczynski metric
    :type min_kulc_value: float (values between 0.0 and 1.0)
    :param min_imbalance_ratio_value: minimum value of imbalance ratio
    :type min_imbalance_ratio_value: float (values between 0.0 and 1.0)
    :param top_n: number of best recommendations
    :type top_n: integer
    :return: list of the best recommended items for the user or if some of the movies do
    """

    if len(verify_movie_exists(movies_filename, list_user_movies)) > 0:
        movieStr = ""
        for movie in verify_movie_exists(movies_filename, list_user_movies):
            movieStr += movie + " "
        return "Não foi possível recomendar itens, pois o(s) seguinte(s) filme(s) não existe(m): " + movieStr
    else:
        list_transactions_size = len(read_data(filename, is_implicit))
        association_rules = generate_association_rules(filename, is_implicit, min_support, rule_metric,
                                                       min_rule_metric_value)
        # print(association_rules.to_string()) # Output of all association rules with metrics applied
        temp_user_rules_association = []
        association_rules_list = []
        for ruleInfo in association_rules.itertuples():
            antecedents = list(frozenset(ruleInfo.antecedents))
            # Verify if an user item exists in antecedents columns in rules
            count_ante = 0

            for rule_consequent in list_user_movies:
                if rule_consequent in antecedents:
                    count_ante += 1

            if 1 <= count_ante <= len(antecedents):
                new_rule = {'antecedents': ruleInfo.antecedents,
                            'consequents': ruleInfo.consequents,
                            'antecedent support': ruleInfo._3,
                            'consequent support': ruleInfo._4,
                            'support': ruleInfo.support,
                            'confidence': ruleInfo.confidence,
                            'lift': ruleInfo.lift,
                            'kulczynski': calculate_kulczynski(sup_a=ruleInfo._3, sup_b=ruleInfo._4,
                                                               sup_ab=ruleInfo.support,
                                                               total_transactions=list_transactions_size),
                            'imbalance ratio': calculate_imbalance_ratio(sup_a=ruleInfo._3, sup_b=ruleInfo._4,
                                                                         sup_ab=ruleInfo.support,
                                                                         total_transactions=list_transactions_size)}
                temp_user_rules_association.append(new_rule)

        # The more lesser Imbalance Ratio is, better (0 = perfectly balanced, 1 = unbalanced) and the more greater
        # Kulczynski is better (0.5 = not interesting rule, Close to 0 = itemsets negatively associated,
        # Close to 1 = itemsets positively associated)
        for userRuleAssociation in temp_user_rules_association:
            if userRuleAssociation['imbalance ratio'] <= min_imbalance_ratio_value and userRuleAssociation[
                'kulczynski'] >= min_kulc_value:
                association_rules_list.append(userRuleAssociation)

        # If there isn't any rule generated it will be recommended to the user the popular items
        if len(association_rules_list) == 0:
            print("Não foi possível recomendar items, items populares:")
            return get_popular_rules_movies(association_rules, top_n, list_user_movies)

        all_filtered_rules = pd.DataFrame(association_rules_list).sort_values('confidence', ascending=False)

        # print(recommended_items.to_string()) # Output of topN recommended rules
        top_n_items = []
        # Top N Recommended Items (Dataframe type)
        for filtered_rule in all_filtered_rules.itertuples():
            rule_consequents = list(frozenset(filtered_rule.consequents))
            # Remove duplicated recommended items
            for rule_consequent in rule_consequents:
                if rule_consequent not in top_n_items:
                    if rule_consequent not in list_user_movies:
                        if len(top_n_items) < top_n:
                            top_n_items.append(rule_consequent)
                        else:
                            break

        if len(top_n_items) == 0:
            print("Não foi possível recomendar items, items populares:")
            return get_popular_rules_movies(association_rules, top_n, list_user_movies)
    return top_n_items


# Feedback Implícito
# MovieLens 5k (min_sup = 0.1, min_conf= 0.6, min_kulc=0.6, min_imb_ratio=0.3) ->  543 regras

# Feedback Explícito
# MovieLens 5k (min_sup = 0.1, min_conf= 0.6, min_kulc=0.6, min_imb_ratio=0.3) -> 129 regras


# recommItems = recommend_to_user(
#     list_user_movies=["No More School (2000)", 'Lord of the Rings: The Fellowship of the Ring, The (2001)'],
#     is_implicit=True,
#     filename='datasets/userRatings5k.csv',
#     movies_filename='datasets/movies.csv',
#     min_support=0.1,
#     rule_metric="confidence", min_rule_metric_value=0.6, min_kulc_value=0.6,
#     min_imbalance_ratio_value=0.3,
#     top_n=5)
#
# print(recommItems.to_string())


def write_rules_csv(to_csv_file, rules):
    """
    Method that writes association rules into a csv file
    :param to_csv_file: path where the csv file is located (this file must be in csv format)
    :type to_csv_file: string
    :param rules: association rules
    :type rules: dataframe
    """
    with open(to_csv_file, 'w', newline='', encoding='utf-8') as new_fp:
        # Pandas(Index, Antecedents, Consequents, _3 (antecedent support), _4 (consequent support), Support, Confidence, Lift=, Kulc, _9 (Imbalance Ratio))
        write = csv.writer(new_fp)
        write.writerow(
            ["id", "antecedents", "consequents", "antecedent_support", "consequent_support", "support", "confidence",
             "kulczynski",
             "imbalance_ratio"])
        i = 1
        for item in rules.itertuples():
            new_line = [i, list(item.antecedents), list(item.consequents), round(item._3, 6),
                        round(item._4, 6), round(item.support, 6), round(item.confidence, 6), round(item.kulczynski, 6),
                        round(item._9, 6)]
            write.writerow(new_line)
            i += 1
        print("Escrito com sucesso!")
    new_fp.close()

# write_rules_csv('rulesCsv/rules5kUsersImp.csv', rules)
