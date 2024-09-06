import unittest
from unittest.mock import patch, MagicMock

from Classes.Product import Product
from Classes.Util.AlgorithmUtil import AlgorithmUtil


class UnitTest(unittest.TestCase):

    def setUp(self):
        self.product1 = Product("1", "Product 1", "Category A", 10.0)
        self.product2 = Product("2", "Product 2", "Category B", 20.0)
        self.product3 = Product("3", "Product 3", "Category A", 30.0)
        self.product4 = Product("4", "Product 4", "Category C", 40.0)
        self.product5 = Product("5", "Product 5", "Category B", 50.0)

    @patch('Classes.API_service.ProductLocalService.ProductLocalService.get_product')
    def test_get_product(self, mock_get_product):
        mock_get_product.side_effect = [self.product1, self.product2]

        result = AlgorithmUtil._AlgorithmUtil__get_product(["product_id_1", "product_id_2"])

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].product_id, "1")
        self.assertEqual(result[1].product_id, "2")

    @patch('Classes.API_service.PurchaseLocalService.PurchaseLocalService.get_purchase_histories_by_product')
    @patch('Classes.API_service.ProductLocalService.ProductLocalService.get_product')
    def test_apriori(self, mock_get_product, mock_get_histories):
        mock_get_histories.return_value = [
            {"product_ids": ["product_id_1", "product_id_2", "product_id_3"]},
            {"product_ids": ["product_id_1", "product_id_3", "product_id_4"]},
            {"product_ids": ["product_id_1", "product_id_3", "product_id_5"]},
            {"product_ids": ["product_id_1", "product_id_2", "product_id_4"]},
            {"product_ids": ["product_id_1", "product_id_2", "product_id_3", "product_id_4", "product_id_5"]},
            {"product_ids": ["product_id_1", "product_id_3", "product_id_5"]},
            {"product_ids": ["product_id_1", "product_id_2", "product_id_3", "product_id_4"]},
            {"product_ids": ["product_id_2", "product_id_4", "product_id_1"]},
            {"product_ids": ["product_id_1", "product_id_3", "product_id_4", "product_id_5"]},
            {"product_ids": ["product_id_1", "product_id_2", "product_id_3", "product_id_5"]},
        ]

        def get_product_side_effect(product_id):
            product_map = {
                "1": self.product1,
                "2": self.product2,
                "3": self.product3,
                "4": self.product4,
                "5": self.product5,
            }
            # Extract the number from product_id_X
            prod_num = product_id.split('_')[-1]
            return product_map.get(prod_num,
                                   MagicMock(product_id=prod_num, name=f"Product {prod_num}", category="Unknown",
                                             price=0.0))

        mock_get_product.side_effect = get_product_side_effect

        result = AlgorithmUtil.apriori("product_id_1")

        self.assertGreater(len(result), 0)
        for product in result:
            self.assertNotEqual(product.product_id, "1")
            self.assertIn(product.product_id, ["2", "3", "4", "5"])

    @patch('Classes.API_service.PurchaseLocalService.PurchaseLocalService.get_all_purchase_histories')
    @patch('Classes.API_service.PurchaseLocalService.PurchaseLocalService.get_purchase_histories_by_user_id')
    @patch('Classes.API_service.BrowsingLocalService.BrowsingLocalService.get_browsing_histories_by_user_id')
    @patch('Classes.API_service.ProductLocalService.ProductLocalService.get_product')
    def test_get_top_selling_products(self, mock_get_product, mock_get_browsing, mock_get_user_purchases,
                                      mock_get_all_purchases):
        mock_get_all_purchases.return_value = [
            {"product_ids": ["product_id_1", "product_id_2"]},
            {"product_ids": ["product_id_1", "product_id_3"]},
            {"product_ids": ["product_id_2", "product_id_3"]},
        ]
        mock_get_user_purchases.return_value = [{"product_ids": ["product_id_1"]}]
        mock_get_browsing.return_value = [{"product_ids": ["product_id_2"]}]
        mock_get_product.return_value = self.product3

        result = AlgorithmUtil.get_top_selling_products("user_id_1")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].product_id, "3")

    @patch('Classes.API_service.BrowsingLocalService.BrowsingLocalService.get_browsing_histories_by_user_id')
    @patch('Classes.API_service.ProductLocalService.ProductLocalService.get_product')
    def test_get_products_by_browsing_history(self, mock_get_product, mock_get_browsing):
        mock_get_browsing.return_value = [{"product_ids": ["product_id_1", "product_id_2", "product_id_3"]}]
        mock_get_product.side_effect = [self.product1, self.product2, self.product3, self.product1]

        result = AlgorithmUtil.get_products_by_browsing_history("user_id_1", ["product_id_1"])

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].product_id, "3")


if __name__ == '__main__':
    unittest.main()
