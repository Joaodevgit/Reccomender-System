from FPGrowthAlgo import *
from DataPlots import *

# Generation of association rules with certain metrics
rules = generate_association_rules_kulc_imbalance(filename='datasets/userRatings5k.csv',
                                                  is_implicit=False,
                                                  min_support=0.1,
                                                  rule_metric="confidence", min_rule_metric_value=0.6,
                                                  min_kulc_value=0.6,
                                                  min_imbalance_ratio_value=0.3)


# print(sum(get_itemset_rules_tot(create_rules_dict(rules))["Itemsets"].values()))
# print(json.dumps(get_itemset_rules_tot(create_rules_dict(rules)), ensure_ascii=False, indent=2))

def get_labels_legend_dict_keys(rules_dict):
    """
    Method that returns a string list representing the number of rules in the interval of percentages
    :param rules_dict: dictionary in the following format:
                       { "antecedents": { "itemset": no. ocorrences }, "consequents": { "itemset": no. ocorrences } }
    :type rules_dict: dictionary
    :return: string list in the following format: "X% - Y% (No. of rules)"
    """
    pct = []
    for rule in rules_dict.keys():
        pct.append(rule + " (" + str(rules_dict[rule]) + " regras)")
    return pct


def get_label_pie_chart_dict_keys(rules_dict):
    """
    Method that returns a string list representing the interval of percentages
    :param rules_dict: dictionary in the following format:
                       { "antecedents": { "itemset": no. ocorrences }, "consequents": { "itemset": no. ocorrences } }
    :type rules_dict: dictionary
    :return: string list in the following format: "X% - Y%"
    """
    pct = []
    for rule in rules_dict.keys():
        pct.append(rule)
    return pct


def get_labels_size_dict_keys(rules_dict, rules_keys_arr):
    """
    Method that returns a list of float values associated to the number of ocorrences of a certain percentage
    :param rules_dict: dictionary in the following format:
                       { "antecedents": { "itemset": no. ocorrences }, "consequents": { "itemset": no. ocorrences } }
    :type rules_dict: dictionary
    :param rules_keys_arr: list of float values
    :type rules_keys_arr: float list
    :return: list of values in the following format: "X% - Y%"
    """
    pct = []
    for rule in rules_keys_arr:
        pct.append(rules_dict[rule])
    return pct


def create_metric_percentage_pie_chart(labels_legend_list, labels_piechart_list, metric_dict, legend_title,
                                       bbox_to_anchor_tuple, loc, fontsize, title_fontsize):
    """
    Method that will plot a pie chart containing occurrences in association rules metric (in percentage)
    :param labels_legend_list: list containing labels for legend
    :type labels_legend_list: list of string or integer
    :param labels_piechart_list: list containing labels for pie chart
    :type labels_piechart_list: list of string or integer
    :param metric_dict: dictionary in the following format:
                       { "0% - 5%": no. of rules that satisfy that interval of values }
    :type metric_dict: dictionary
    :param legend_title: legend's title
    :type legend_title: string
    :param bbox_to_anchor_tuple: if a 4-tuple or BboxBase is given, then it specifies the bbox (x, y, width, height), if
                                 a 2-tuple (x, y) places the corner of the legend specified by loc at x, y
    :type bbox_to_anchor_tuple: 2-tuple, or 4-tuple of floats
    :param loc: legend's location
    :type loc: string (it only accepts 'best', 'upper right', 'upper left', 'lower left', 'lower right', 'right',
                      'center left', 'center right', 'lower center', 'upper center', 'center')
    :param fontsize: legend's font size
    :type fontsize: int or string (it only accepts 'xx-small', 'x-small', 'small', 'medium', 'large', 'x-large',
                    'xx-large')
    :param title_fontsize: the font size of the legend's title.
    :type title_fontsize: int or string (it only accepts 'xx-small', 'x-small', 'small', 'medium', 'large', 'x-large',
                          'xx-large')
    """
    labels_legend = sorted(labels_legend_list)
    labels_pie_chart = sorted(labels_piechart_list)
    sizes = get_labels_size_dict_keys(metric_dict, labels_pie_chart)
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels_pie_chart, startangle=60)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    if fontsize == "" and title_fontsize != "":
        ax1.legend(labels_legend, title=legend_title, loc=loc,
                   bbox_to_anchor=bbox_to_anchor_tuple, title_fontsize=title_fontsize)
    elif fontsize != "" and title_fontsize == "":
        ax1.legend(labels_legend, title=legend_title, loc=loc,
                   bbox_to_anchor=bbox_to_anchor_tuple, fontsize=fontsize)
    elif fontsize != "" and title_fontsize != "":
        ax1.legend(labels_legend, title=legend_title, loc=loc,
                   bbox_to_anchor=bbox_to_anchor_tuple, fontsize=fontsize, title_fontsize=title_fontsize)
    else:
        ax1.legend(labels_legend, title=legend_title, loc=loc,
                   bbox_to_anchor=bbox_to_anchor_tuple)
    plt.show()


# Pie Chart "Percentagem de suporte encontrado nas regras"
# rulesDictSupp = create_rules_metric_percentage_ocurrence_dict(rules, "support")
# labelsSuppLegendList = get_labels_legend_dict_keys(rulesDictSupp)
# labelsSuppPiechartList = get_label_pie_chart_dict_keys(rulesDictSupp)
#

# create_metric_percentage_pie_chart(labels_legend_list=labelsSuppLegendList, labels_piechart_list=labelsSuppPiechartList,
#                                    metric_dict=rulesDictSupp,
#                                    legend_title="% Suporte das Regras de Associação",
#                                    bbox_to_anchor_tuple=(0.5, 0.1, 0.5, 0.5), loc='best', fontsize="x-small",
#                                    title_fontsize="small")


# Pie Chart "Percentagem de confiança encontrada nas regras"
# rulesDictConf = create_rules_metric_percentage_ocurrence_dict(rules, "confidence")
# labelsSuppLegendList = get_labels_legend_dict_keys(rulesDictConf)
# labelsSuppPiechartList = get_label_pie_chart_dict_keys(rulesDictConf)
#
#
# create_metric_percentage_pie_chart(labels_legend_list=labelsSuppLegendList, labels_piechart_list=labelsSuppPiechartList,
#                                    metric_dict=rulesDictConf,
#                                    legend_title="% Confiança das Regras de Associação",
#                                    bbox_to_anchor_tuple=(-0.18, 0.9), loc='upper left', fontsize="x-small",
#                                    title_fontsize="small")

# Pie Chart "Percentagem de Kulczynski encontrado nas regras"
# rulesDictKulc = create_rules_metric_percentage_ocurrence_dict(rules, "kulczynski")
# labelsSuppLegendList = get_labels_legend_dict_keys(rulesDictKulc)
# labelsSuppPiechartList = get_label_pie_chart_dict_keys(rulesDictKulc)
#
#
# create_metric_percentage_pie_chart(labels_legend_list=labelsSuppLegendList, labels_piechart_list=labelsSuppPiechartList,
#                                    metric_dict=rulesDictKulc,
#                                    legend_title="% Kulczynski das Regras de Associação",
#                                    bbox_to_anchor_tuple=(-0.18, 0.77), loc='upper left',fontsize="x-small",
#                                    title_fontsize="small")

# Pie Chart "Percentagem de Rácio de Desequilíbrio encontrado nas regras"
# rulesDictIB = create_rules_metric_percentage_ocurrence_dict(rules, "imbalance ratio")
# labelsSuppLegendList = get_labels_legend_dict_keys(rulesDictIB)
# labelsSuppPiechartList = get_label_pie_chart_dict_keys(rulesDictIB)
#

# create_metric_percentage_pie_chart(labels_legend_list=labelsSuppLegendList, labels_piechart_list=labelsSuppPiechartList,
#                                    metric_dict=rulesDictIB,
#                                    legend_title="% Rácio de Desequilíbrio das Regras de Associação",
#                                    bbox_to_anchor_tuple=(-0.18, 1.11), loc='upper left', fontsize="x-small",
#                                    title_fontsize="small")


def create_itemsets_ocurrences_pie_chart(labels_legend_list, labels_piechart_list, sizes_list, legend_title,
                                         bbox_to_anchor_tuple, loc, fontsize, title_fontsize):
    """
    Method that will plot a pie chart containing itemsets occurrences in association rules
    :param labels_legend_list: dataframe series containing labels for legend
    :type labels_legend_list: dataframe series
    :param labels_piechart_list: dataframe series containing labels for pie chart
    :type labels_piechart_list: dataframe series
    :param sizes_list: wedge's sizes
    :type sizes_list: dataframe series
    :param legend_title: legend's title
    :type legend_title: string
    :param bbox_to_anchor_tuple: if a 4-tuple or BboxBase is given, then it specifies the bbox (x, y, width, height), if
                                 a 2-tuple (x, y) places the corner of the legend specified by loc at x, y
    :type bbox_to_anchor_tuple: 2-tuple, or 4-tuple of floats
    :param loc: legend's location
    :type loc: string (it only accepts 'best', 'upper right', 'upper left', 'lower left', 'lower right', 'right',
                       'center left', 'center right','lower center','upper center', 'center')
    :param fontsize: legend's font size
    :type fontsize: int or string (it only accepts 'xx-small', 'x-small', 'small', 'medium', 'large', 'x-large',
                    'xx-large')
    :param title_fontsize: the font size of the legend's title.
    :type title_fontsize: int or string (it only accepts 'xx-small', 'x-small', 'small', 'medium', 'large', 'x-large',
                          'xx-large')
    """
    labels_legend = labels_legend_list
    labels_pie_chart = labels_piechart_list
    sizes = sizes_list
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels_pie_chart, startangle=60)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    if fontsize == "" and title_fontsize != "":
        ax1.legend(labels_legend, title=legend_title, loc=loc,
                   bbox_to_anchor=bbox_to_anchor_tuple, title_fontsize=title_fontsize)
    elif fontsize != "" and title_fontsize == "":
        ax1.legend(labels_legend, title=legend_title, loc=loc,
                   bbox_to_anchor=bbox_to_anchor_tuple, fontsize=fontsize)
    elif fontsize != "" and title_fontsize != "":
        ax1.legend(labels_legend, title=legend_title, loc=loc,
                   bbox_to_anchor=bbox_to_anchor_tuple, fontsize=fontsize, title_fontsize=title_fontsize)
    else:
        ax1.legend(labels_legend, title=legend_title, loc=loc,
                   bbox_to_anchor=bbox_to_anchor_tuple)
    plt.show()


# Pie Chart "Ocorrência dos Itemsets nos Antecedentes das Regras de Associação"
# rulesDictAsceOcu = create_rules_dict(rules)
# df = pd.DataFrame(list(rulesDictAsceOcu["antecedents"].items()), columns=['Antecedents', 'Ocurrences no.']).sort_values(
#     'Ocurrences no.', ascending=False)[0:10]
#
# create_itemsets_ocurrences_pie_chart(labels_legend_list=df["Antecedents"], labels_piechart_list=df["Ocurrences no."],
#                                      sizes_list=df["Ocurrences no."],
#                                      legend_title="Ocorrência dos Itemsets nos Antecedentes das Regras de Associação (Top 10)",
#                                      bbox_to_anchor_tuple=(-0.16, 1.15), loc='upper left', fontsize="xx-small",
#                                      title_fontsize="")

# Pie Chart "Ocorrência dos Itemsets nos Consequentes das Regras de Associação"

# rulesDictConseOcu = create_rules_dict(rules)
# df = pd.DataFrame(list(rulesDictConseOcu["consequents"].items()), columns=['Consequents', 'Ocurrences no.']).sort_values(
#     'Ocurrences no.', ascending=False)[0:10]
#
#
# create_itemsets_ocurrences_pie_chart(labels_legend_list=df["Consequents"], labels_piechart_list=df["Ocurrences no."],
#                                      sizes_list=df["Ocurrences no."],
#                                      legend_title="Ocorrência dos Itemsets nos Consequentes das Regras de Associação (Top 5)",
#                                      bbox_to_anchor_tuple=(-0.16, 0.9), loc='upper left', fontsize="xx-small",
#                                      title_fontsize="")

# Pie Chart "Ocorrência dos Itemsets nas Regras de Associação"

# rulesDictAsceConsTot = get_itemset_rules_tot(create_rules_dict(rules))
# df = pd.DataFrame(list(rulesDictAsceConsTot["itemsets"].items()), columns=['Itemsets', 'Ocurrences no.']).sort_values(
#     'Ocurrences no.', ascending=False)[0:10]
#
# create_itemsets_ocurrences_pie_chart(labels_legend_list=df["Itemsets"], labels_piechart_list=df["Ocurrences no."],
#                                      sizes_list=df["Ocurrences no."],
#                                      legend_title="Ocorrência dos Itemsets nas Regras de Associação (Top 10)",
#                                      bbox_to_anchor_tuple=(-0.16, 1.11), loc='upper left', fontsize="xx-small",
#                                      title_fontsize="")
