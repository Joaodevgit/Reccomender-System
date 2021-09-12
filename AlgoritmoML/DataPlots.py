import matplotlib.pyplot as plt
from FPGrowthAlgo import *


# Generation of association rules with certain metrics
rules = generate_association_rules_kulc_imbalance(filename='datasets/userRatings5k.csv',
                                                  is_implicit=True,
                                                  min_support=0.1,
                                                  rule_metric="confidence", min_rule_metric_value=0.6, min_kulc_value=0.6,
                                                  min_imbalance_ratio_value=0.3)
# print(rules.to_string())


def create_rules_dict(rules):
    """
    Method that, given association rules, returns a dictionary with a following format:
    { "antecedents": { "itemset": no. ocorrences }, "consequents": { "itemset": no. ocorrences } }
    :param rules: association rules
    :type rules: dataframe
    :return: dictionary with a following format: { "antecedents": { "itemset": no. ocorrences }, "consequents": { "itemset": no. ocorrences } }
    """
    # Pandas(Index, antecedents, consequents, _3 (antecedent support), _4 (consequent support), support, confidence, lift, kulczynski, _9 (imbalance ratio))
    # rulesDict = { "antecedents": { "itemset": no. ocorrences }, "consequents": { "itemset": no. ocorrences } }
    rules_dict = {"antecedents": {}, "consequents": {}}
    for ruleInfo in rules.itertuples():
        if str(list(ruleInfo.antecedents)) in rules_dict["antecedents"].keys():
            rules_dict["antecedents"][str(list(ruleInfo.antecedents))] += 1
        else:
            rules_dict["antecedents"].update({str(list(ruleInfo.antecedents)): 1})
        if str(list(ruleInfo.consequents)) in rules_dict["consequents"].keys():
            rules_dict["consequents"][str(list(ruleInfo.consequents))] += 1
        else:
            rules_dict["consequents"].update({str(list(ruleInfo.consequents)): 1})

    return rules_dict


# print(json.dumps(create_rules_dict(rules), ensure_ascii=False, indent=2))

def create_rules_metric_percentage_ocurrence_dict(rules, metric):
    """
    Method that, given association rules and a certain metric, returns a dictionary
    :param rules: association rules
    :type rules: dataframe
    :param metric: metric to be considered in association rules
    :type metric: string (it only accepts support,confidence, lift, kulczynski, imbalance ratio)
    :return: dictionary in the following format: { "0% - 5%": no. of rules that satisfy that interval of values }
    """
    rules_dict = {}
    for rule in rules[metric]:
        if 0 <= (float(rule) * 100) < 5.0:
            if "0% - 5%" in rules_dict.keys():
                rules_dict["0% - 5%"] += 1
            else:
                rules_dict["0% - 5%"] = 1
            pass
        if 5.0 <= (float(rule) * 100) < 10.0:
            if "05% - 10%" in rules_dict.keys():
                rules_dict["05% - 10%"] += 1
            else:
                rules_dict["05% - 10%"] = 1
            pass
        if 10.0 <= (float(rule) * 100) < 15.0:
            if "10% - 15%" in rules_dict.keys():
                rules_dict["10% - 15%"] += 1
            else:
                rules_dict["10% - 15%"] = 1
            pass
        if 15.0 <= (float(rule) * 100) < 20.0:
            if "15% - 20%" in rules_dict.keys():
                rules_dict["15% - 20%"] += 1
            else:
                rules_dict["15% - 20%"] = 1
            pass
        if 20.0 <= (float(rule) * 100) < 25.0:
            if "20% - 25%" in rules_dict.keys():
                rules_dict["20% - 25%"] += 1
            else:
                rules_dict["20% - 25%"] = 1
            pass
        if 25.0 <= (float(rule) * 100) < 30.0:
            if "25% - 30%" in rules_dict.keys():
                rules_dict["25% - 30%"] += 1
            else:
                rules_dict["25% - 30%"] = 1
            pass
        if 30.0 <= (float(rule) * 100) < 35.0:
            if "30% - 35%" in rules_dict.keys():
                rules_dict["30% - 35%"] += 1
            else:
                rules_dict["30% - 35%"] = 1
            pass
        if 35.0 <= (float(rule) * 100) < 40.0:
            if "35% - 40%" in rules_dict.keys():
                rules_dict["35% - 40%"] += 1
            else:
                rules_dict["35% - 40%"] = 1
            pass
        if 40.0 <= (float(rule) * 100) < 45.0:
            if "40% - 45%" in rules_dict.keys():
                rules_dict["40% - 45%"] += 1
            else:
                rules_dict["40% - 45%"] = 1
            pass
        if 45.0 <= (float(rule) * 100) < 50.0:
            if "45% - 50%" in rules_dict.keys():
                rules_dict["45% - 50%"] += 1
            else:
                rules_dict["45% - 50%"] = 1
            pass
        if 50.0 <= (float(rule) * 100) < 55.0:
            if "40% - 45%" in rules_dict.keys():
                rules_dict["50% - 55%"] += 1
            else:
                rules_dict["50% - 55%"] = 1
            pass
        if 55.0 <= (float(rule) * 100) < 60.0:
            if "55% - 60%" in rules_dict.keys():
                rules_dict["55% - 60%"] += 1
            else:
                rules_dict["55% - 60%"] = 1
            pass
        if 60.0 <= (float(rule) * 100) < 65.0:
            if "60% - 65%" in rules_dict.keys():
                rules_dict["60% - 65%"] += 1
            else:
                rules_dict["60% - 65%"] = 1
            pass
        if 65.0 <= (float(rule) * 100) < 70.0:
            if "65% - 70%" in rules_dict.keys():
                rules_dict["65% - 70%"] += 1
            else:
                rules_dict["65% - 70%"] = 1
            pass
        if 70.0 <= (float(rule) * 100) < 75.0:
            if "70% - 75%" in rules_dict.keys():
                rules_dict["70% - 75%"] += 1
            else:
                rules_dict["70% - 75%"] = 1
            pass
        if 75.0 <= (float(rule) * 100) < 80.0:
            if "75% - 80%" in rules_dict.keys():
                rules_dict["75% - 80%"] += 1
            else:
                rules_dict["75% - 80%"] = 1
            pass
        if 80.0 <= (float(rule) * 100) < 85.0:
            if "80% - 85%" in rules_dict.keys():
                rules_dict["80% - 85%"] += 1
            else:
                rules_dict["80% - 85%"] = 1
            pass
        if 85.0 <= (float(rule) * 100) < 90.0:
            if "85% - 90%" in rules_dict.keys():
                rules_dict["85% - 90%"] += 1
            else:
                rules_dict["85% - 90%"] = 1
            pass
        if 90.0 <= (float(rule) * 100) < 95.0:
            if "90% - 95%" in rules_dict.keys():
                rules_dict["90% - 95%"] += 1
            else:
                rules_dict["90% - 95%"] = 1
            pass
        if 95.0 <= (float(rule) * 100) < 100.0:
            if "95% - 100%" in rules_dict.keys():
                rules_dict["95% - 100%"] += 1
            else:
                rules_dict["95% - 100%"] = 1
    return rules_dict


# print(json.dumps(create_rules_metric_percentage_ocurrence_dict(rules, "confidence"), ensure_ascii=False, indent=2))

def get_itemset_rules_ocurrences(item_name, rules_dict):
    """
    Method that, given an item name and a dictionary of association rules, returns a message
    saying how many times that item appeared in association rules (antecedents and consequents)
    :param item_name: item's name
    :type item_name: string
    :param rules_dict: dictionary of association rules in the following format:
                      { "antecedents": { "itemset": no. ocorrences }, "consequents": { "itemset": no. ocorrences } }
    :type rules_dict: dictionary
    :return: string containing how many times that item appeared in association rules (antecedents and consequents)
    """
    total_ant = 0
    total_cons = 0
    for rule in rules_dict["antecedents"].keys():
        if item_name in rule:
            total_ant += rules_dict["antecedents"][rule]
    for rule in rules_dict["consequents"].keys():
        if item_name in rule:
            total_cons += rules_dict["consequents"][rule]

    return "O item " + item_name + " aparece " + str(total_ant) + "x nos antecedentes e aparece " + str(
        total_cons) + "x nos consequentes"


# print(get_itemset_rules_ocurrences("Lord of the Rings: The Two Towers, The (2002)", create_rules_dict(rules)))


def get_itemset_rules_tot(rules_dict):
    """
    Method that, given a dictionary of rules, returns another dictionary with the itemsets occorrences in antecedents
    and in ocorrences of association rules
    :param rules_dict: dictionary of association rules in the following format:
                      { "antecedents": { "itemset": no. ocorrences }, "consequents": { "itemset": no. ocorrences } }
    :type rules_dict: dictionary
    :return: dictionary in the following format: { "itemsets": { "ItemsetA": no. ocorrences } }
    """
    rule_itemsets = []
    itemset_dict = {"itemsets": {}}
    for rule in rules_dict["antecedents"].keys():
        if rule not in rule_itemsets:
            rule_itemsets.append(rule)
    for rule in rules_dict["consequents"].keys():
        if rule not in rule_itemsets:
            rule_itemsets.append(rule)

    for rule_itemset in rule_itemsets:
        total = 0
        if rule_itemset in rules_dict["antecedents"].keys():
            total += rules_dict["antecedents"][rule_itemset]
        if rule_itemset in rules_dict["consequents"].keys():
            total += rules_dict["consequents"][rule_itemset]
        if rule_itemset in itemset_dict.keys():
            itemset_dict["itemsets"][rule_itemset] += total
        else:
            itemset_dict["itemsets"][rule_itemset] = total

    return itemset_dict


# print(json.dumps(get_itemset_rules_tot(create_rules_dict(rules)), ensure_ascii=False, indent=2))

def create_scatter_plot(rules, metric_a, metric_b):
    """
    Method that, given association rules and 2 different metrics of it, plots a scatter plot that will show the
    relationship between the 2 chosen association rules metrics
    :param rules: association rules
    :type rules: string
    :param metric_a: metric in association rules that will be plotted on the X axis in the scatter plot
    :type metric_a: string (it only accepts support, confidence, lift, kulczynski, imbalance ratio)
    :param metric_b: metric in association rules that will be plotted on the Y axis in the scatter plot
    :type metric_b: string (it only accepts support, confidence, lift, kulczynski, imbalance ratio)
    """
    if metric_a != metric_b:
        axis_x = metric_a.capitalize()
        axis_y = metric_b.capitalize()
        plt.scatter(rules[metric_a], rules[metric_b], alpha=0.5)
        plt.xlabel(axis_x)
        plt.ylabel(axis_y)
        plotTitle = axis_x + " vs " + axis_y
        plt.title(plotTitle)
        plt.show()
    else:
        print("Erro as 2 métricas são iguais!")

create_scatter_plot(rules, "confidence", "support")
