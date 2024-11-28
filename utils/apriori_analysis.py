import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

def get_top_products(data):
    """Renvoie les 30 produits les plus achetés triés par ordre alphabétique."""
    top_products = (
        data.groupby("product_name")["order_id"]
        .count()
        .sort_values(ascending=False)
        .head(30)
        .index.tolist()
    )
    return sorted(top_products)

def apriori_analysis(data, product):
    """Analyse Apriori pour trouver les produits complémentaires."""
    # Préparer les données pour l'analyse
    basket = (
        data.groupby(["order_id", "product_name"])["quantity_float"]
        .sum()
        .unstack()
        .fillna(0)
        .applymap(lambda x: 1 if x > 0 else 0)
    )

    # Appliquer Apriori
    frequent_itemsets = apriori(basket, min_support=0.01, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.0)

    # Filtrer les règles pour le produit donné
    relevant_rules = rules[rules["antecedents"].apply(lambda x: product in x)]
    relevant_rules = relevant_rules[["consequents", "support", "confidence", "lift"]]
    relevant_rules["consequents"] = relevant_rules["consequents"].apply(list)
    return relevant_rules.sort_values(by="confidence", ascending=False)
