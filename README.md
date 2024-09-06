**A simple, CLI-based program for implementing a project to work with data using libraries.
The project is implemented and demonstrated in a simple way working with data for the product proposal system.**

To start the program, you first need to install the program prerequisites.
Please build a Virtual environment first to ensure and activate the virtual environment.:

Linux:

```
python3 -m venv venv && source venv/bin/activate # Activate the virtual environment for Linux
```

Windows:

```shell
python -m venv venv && source venv/Scripts/activate # Activate the virtual environment for Windows
```

Then it is necessary to install the prerequisites of the program:

```
pip install -r requirements.txt
```

You can now run the `main.py` file to start the program.

#### Optional:

To enter the sample information you can run the `Database_service/Sample_datasets/Sample_datasets.py` file so that the
information enters the database as many times as you want.

# Algorithm Class

AlgorithmUtil is a Python class that provides various utility functions for analyzing product data, user behavior, and
generating recommendations. This class is designed to work with local service classes for browsing, product, and
purchase data.

## Features

1. Apriori Algorithm for Frequent Itemsets
2. Top Selling Products Retrieval
3. Product Recommendations Based on Browsing History

## Dependencies

- pandas
- mlxtend
- collections (Counter)

## Usage

### Apriori Algorithm

```python
related_products = AlgorithmUtil.apriori(product_id)
```

This method uses the Apriori algorithm to find frequently purchased items together. It returns a list of
related `Product` objects. For more information on the Apriori algorithm, refer to
the [documentation](https://www.dbs.ifi.lmu.de/Lehre/KDD/SS16/skript/3_FrequentItemsetMining.pdf).

### Top Selling Products

```python
top_products = AlgorithmUtil.get_top_selling_products(user_id, limit=10)
```

Retrieves the best-selling products, excluding those already purchased or browsed by the specified user. Returns a list
of `Product` objects.

### Products by Browsing History

```python
recommended_products = AlgorithmUtil.get_products_by_browsing_history(user_id, cart)
```

Generates product recommendations based on the user's browsing history and the items currently in their cart. Returns a
list of `Product` objects.

## Private Methods

- `__get_product(product_ids)`: Retrieves product details by product IDs.

## Note

This utility class relies on local service classes (`BrowsingLocalService`, `ProductLocalService`,
and `PurchaseLocalService`) to fetch data. Ensure these services are properly set up and accessible.

## Future Improvements

1. Implement caching for frequently accessed data to improve performance.
2. Add more recommendation algorithms (e.g., collaborative filtering, content-based filtering).