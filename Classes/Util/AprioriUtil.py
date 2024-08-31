import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.preprocessing import TransactionEncoder
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['admin']
users_collection = db['users']
products_collection = db['products']
browsing_history_collection = db['browsing_history']
purchase_history_collection = db['purchase_history']

documents = browsing_history_collection.find({"product_ids": {"$all": ["product_id_737"]}})
purchase_history = []
for document in documents:
    purchase_history.append(document["product_ids"])

transactions = [list(products) for products in purchase_history]

te = TransactionEncoder()
te_ary = te.fit(transactions).transform(transactions)
df = pd.DataFrame(te_ary, columns=te.columns_)

min_support = 3 / len(transactions)
frequent_item_sets = apriori(df, min_support=min_support, use_colnames=True)

frequent_item_sets = frequent_item_sets.sort_values(by='support', ascending=False)

list_ = []

for index, row in frequent_item_sets.iterrows():
    items = row['itemsets']
    support = row['support'] * len(transactions)
    list_.append([items, support])

for items, support in list_:
    if len(items) > 1:
        print(f'{items} ({support})')
    #     list_1 = [item for item in set(items) if item != "product_id_737"]
    #     print(f"{list_1} (Support: {support:.0f})")
