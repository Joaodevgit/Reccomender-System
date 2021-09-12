import json
import csv
import pandas as pd
import numpy as np
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules, fpgrowth


# Data Extraction

def get_csv_headers(filename):
    # reading the csv file using read_csv
    # storing the data frame in variable called df
    df = pd.read_csv(filename)

    # creating a list of column names by
    # calling the .columns
    list_of_column_names = list(df.columns)

    return list_of_column_names


# print(get_csv_headers('Amazon.csv'))

def read_data(filename):
    """
    Method that reads from a csv file and returns a list of transactions with all users' items
    :param filename: path where the file is located (this file must be in csv)
    :type filename: string
    :return: list of transactions with all users' items
    """
    # Open the file
    with open(filename, encoding='utf-8') as fp:
        USERID, MOVIETITLE, RATING = 0, 1, 2
        reader = csv.reader(fp)
        next(reader, None)  # skip the headers
        ratingsDict = {}

        for line in reader:
            if line[USERID] in ratingsDict.keys():
                ratingsDict[line[USERID]].append((line[MOVIETITLE]))
            else:
                ratingsDict[line[USERID]] = [(line[MOVIETITLE])]
    return list(ratingsDict.values())


# print(read_data('ratings_sampled.csv')[0])

# print(json.dumps(read_data('new_movies_id_small.csv'), ensure_ascii=False, indent=2))


def calculate_kulczynski(supA, supB, supAB, totalTransactions):
    """
    :param supA: support count of antecedents
    :type float
    :param supB: support count of consequents
    :type float
    :param supAB: support count of antecedents and consequents
    :type float
    :param totalTransactions: number of total transations
    :type integer
    :return: kulczynski result of an association rule
    """
    # Absolute Support A
    abs_sup_countA = round(supA * totalTransactions)

    # Absolute Support B
    abs_sup_countB = round(supB * totalTransactions)

    # Absolute Support (A U B)
    abs_sup_countAB = round(supAB * totalTransactions)

    # P(B|A)
    pBA = round(abs_sup_countAB / abs_sup_countA, 6)

    # P(A|B)
    pAB = round(abs_sup_countAB / abs_sup_countB, 6)

    return round(0.5 * (pAB + pBA), 6)


# Output: ~0.244106
# print(calculate_kulczynski(0.052466, 0.255516, 0.021251, 9835))

def calculate_imbalance_ratio(supA, supB, supAB, listTransSize):
    """
    :param supA: support count of antecedents
    :type float
    :param supB: support count of consequents
    :type float
    :param supAB: support count of antecedents and consequents
    :type float
    :param totalTransactions: number of total transations
    :type integer
    :return: imbalance ratio result of an association rule
    """
    # Absolute Support A
    abs_sup_countA = round(supA * listTransSize)

    # Absolute Support B
    abs_sup_countB = round(supB * listTransSize)

    # Absolute Support (A U B)
    abs_sup_countAB = round(supAB * listTransSize)

    return round((abs(abs_sup_countA - abs_sup_countB)) / (abs_sup_countA + abs_sup_countB - abs_sup_countAB), 6)


# Output: 0.708156
# print(calculate_imbalance_ratio(0.052466, 0.255516, 0.021251, 9835))


def generate_association_rules(filename, min_support, ruleMetric, ruleMetricThreshold):
    """
    Method that generates association rules
    :param filename: path where the file is located (this file must be in csv)
    :type filename: string
    :param min_support: minimum support for the association rules
    :type min_support: float
    :param ruleMetric: metric rule for the association rules
    :type ruleMetric: string (it only accepts support,confidence, lift, leverage, conviction)
    :param ruleMetricThreshold: minimum value of metric rule
    :type ruleMetricThreshold: float
    :return: association rules in DataFrame type
    """
    transFull = read_data(filename)
    # print(transFull)  # Output of transfull (list of lists of items)
    # Encoding transactions (Representation of the items in the list in 0's and 1's)

    # Initialize one hot encoding transactions
    one_hot_encoding = TransactionEncoder()

    # Data is transformed into one hot encoding format
    one_hot_trans = one_hot_encoding.fit(transFull).transform(transFull)

    # Converted into dataframe
    one_hot_trans_df = pd.DataFrame(one_hot_trans, columns=one_hot_encoding.columns_)
    # Output of items dataframe transformed into a binary data (one hot encoding)
    # print(one_hot_trans_df.head(5))
    # print('Number of columns :', one_hot_trans_df.shape[1])

    # Generating association rules
    freq_prod = fpgrowth(one_hot_trans_df, min_support=min_support, use_colnames=True)
    # print(freq_prod.to_string())  # Output of frequent products rules

    # Generating association rules with a certain metric and its threshold value
    rules = association_rules(freq_prod, metric=ruleMetric, min_threshold=ruleMetricThreshold)
    # print(rules.to_string()) # Output of rules associated to a certain ruleMetric
    # tempRules = []
    # for ruleInfo in rules.itertuples():
    #     new_rule = {'antecedents': list(ruleInfo.antecedents),
    #                 'consequents': list(ruleInfo.consequents),
    #                 'antecedent support': round(ruleInfo._4, 6),
    #                 'consequent support': round(ruleInfo._3, 6),
    #                 'support': round(ruleInfo.support, 6),
    #                 'confidence': round(ruleInfo.confidence, 6)}
    #     tempRules.append(new_rule)
    #
    # with open('temp2.csv', 'w', newline='', encoding='utf-8') as new_fp:
    #     write = csv.writer(new_fp)
    #     write.writerow(
    #         ["Antecedents", "Consequents", "Antecedent Support", "Consequent Support", "Support", "Confidence"])
    #     for item in tempRules:
    #         new_line = [item['antecedents'], item['consequents'], item['antecedent support'],
    #                     item['consequent support'], item['support'], item['confidence']]
    #         write.writerow(new_line)
    # print("Escrito com sucesso!")
    # new_fp.close()

    return rules


def recommend_to_user(listUserItems, filename, min_support, ruleMetric, minRuleMetricValue, minKulcValue,
                      minImbalanceRatioValue, topN):
    """
    Method that returns top n candidates recommended items given
    :param listUserItems: list of items that user liked/interacted
    :type listUserItems: string list
    :param filename: path where the file is located (this file must be in csv)
    :type filename: string
    :param min_support: minimum support for the association rules
    :type min_support: float
    :param ruleMetric: metric rule for the association rules
    :type ruleMetric: string (it only accepts support,confidence, lift, leverage, conviction)
    :param minRuleMetricValue: minimum value of metric rule
    :type minRuleMetricValue: float
    :param minKulcValue: minimum value of kulczynski metric
    :type minKulcValue: float
    :param minImbalanceRatioValue: minimum value of imbalance ratio
    :type minImbalanceRatioValue: float
    :param topN: number of best recommendations
    :type topN integer
    :return: list of the best recommended items for the user
    """
    listTransactionsSize = len(read_data(filename))
    associationRules = generate_association_rules(filename, min_support, ruleMetric, minRuleMetricValue)
    # print(associationRules.to_string()) # Output of all association rules with metrics applied
    tempUserRulesAssociation = []
    associationRulesList = []
    for ruleInfo in associationRules.itertuples():
        antecedents = list(frozenset(ruleInfo.antecedents))
        consequents = list(frozenset(ruleInfo.consequents))
        # Verify if an user item exists in antecedents columns in rules
        countAnte, countConse = 0, 0

        for item in listUserItems:
            if item in antecedents:
                countAnte += 1
            if item in consequents:
                countConse += 1

        if countAnte == len(antecedents) and countConse < len(consequents):
            new_rule = {'Antecedents': ruleInfo.antecedents,
                        'Consequents': ruleInfo.consequents,
                        'Antecedent Support': ruleInfo._4,
                        'Consequent Support': ruleInfo._3,
                        'Support': ruleInfo.support,
                        'Confidence': ruleInfo.confidence,
                        'Lift': ruleInfo.lift,
                        'Kulc': calculate_kulczynski(supA=ruleInfo._4, supB=ruleInfo._3, supAB=ruleInfo.support,
                                                     totalTransactions=listTransactionsSize),
                        'Imbalance Ratio': calculate_imbalance_ratio(supA=ruleInfo._4, supB=ruleInfo._3,
                                                                     supAB=ruleInfo.support,
                                                                     listTransSize=listTransactionsSize)}
            tempUserRulesAssociation.append(new_rule)

    # The more lesser Imbalance Ratio is, better (0 = perfectly balanced, 1 = unbalanced) and the more greater Kulculczynski
    # is better (0.5 = not interesting rule, Close to 0 = itemsets negatively associated, Close to 1 = itemsets positively associated)
    for userRuleAssociation in tempUserRulesAssociation:
        if userRuleAssociation['Imbalance Ratio'] <= minImbalanceRatioValue and userRuleAssociation[
            'Kulc'] >= minKulcValue:
            associationRulesList.append(userRuleAssociation)

    recommendedItems = pd.DataFrame(associationRulesList).sort_values('Imbalance Ratio', ascending=True)[0:topN]

    # print(recommendedItems.to_string()) # Output of topN recommended rules
    topNItems = []
    # Top N Recommended Items (Dataframe type)
    for recommendedItem in recommendedItems.itertuples():
        recommItemsList = list(frozenset(recommendedItem.Consequents))
        # Remove duplicated recommended items
        for item in recommItemsList:
            if item not in topNItems:
                if item not in listUserItems:
                    topNItems.append(item)
    return topNItems


# MovieLens 5k (min_sup = 0.1 e min_conf= 0.3) ->  4705 regras
# MovieLens 5k (min_sup = 0.1 e min_conf= 0.1) ->  4769 regras

# MovieLens 10k (min_sup = 0.1 e min_conf= 0.3) -> 4840 regras
# MovieLens 10k (min_sup = 0.1 e min_conf= 0.1) -> 4899 regras

# MovieLens 50k (min_sup = 0.1 e min_conf= 0.3) -> 4747 regras
# MovieLens 50k (min_sup = 0.1 e min_conf= 0.1) -> 4821 regras

# MovieLens 100k (min_sup = 0.1 e min_conf= 0.3) -> 4661 regras
# MovieLens 100k (min_sup = 0.1 e min_conf= 0.1) -> 4723 regras

# MovieLens 150k (min_sup = 0.1 e min_conf= 0.3) -> 5019 regras
# MovieLens 150k (min_sup = 0.1 e min_conf= 0.1) -> 5093 regras

# MovieLens 200k (min_sup = 0.1 e min_conf= 0.3) -> 5142 regras
# MovieLens 200k (min_sup = 0.1 e min_conf= 0.1) -> 5215 regras

# MovieLens com um grupo restrito 10k filmes (min_sup = 0.1 e min_conf= 0.3) -> 204 regras
# MovieLens com um grupo restrito 10k filmes (min_sup = 0.1 e min_conf= 0.1) -> 217 regras

# min_support=0.1 e min_confidence=0.6
# Adicionar rating e géneros, nos antecedents passo a ter mais info
print(generate_association_rules(filename="../datasets/userRatings5k.csv", min_support=0.1, ruleMetric="confidence",
                                 ruleMetricThreshold=0.6).to_string())

# recommItems = recommend_to_user(listUserItems=["Blind Turn (2012)"],
#                                 filename='ratings_sampled.csv',
#                                 min_support=0.1,
#                                 ruleMetric="confidence", minRuleMetricValue=0.1, minKulcValue=0.1,
#                                 minImbalanceRatioValue=0.99,
#                                 topN=5)
# print(recommItems)
