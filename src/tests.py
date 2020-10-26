import unittest
import pandas as pd
from utils import (get_num_customers, get_num_items, get_total_discount, get_average_discount_rate,
                  get_avg_total_order, get_total_commission, get_avg_commission, get_commissions_per_promotion)

orders = pd.read_csv('data/orders.csv')
order_lines = pd.read_csv('data/order_lines.csv')
commissions = pd.read_csv('data/commissions.csv')
product_promotions = pd.read_csv('data/product_promotions.csv')

# 'created_at' is a column of timestamps so we convert it to date and save it in 'date' column
orders['date'] = pd.to_datetime(orders['created_at']).dt.floor('D')

# list of all dates as strings
date_strings = sorted(list(set(commissions.date)))


def get_total_items_sold_overall():
    return sum(order_lines.quantity)


def get_total_customers_overall():
    return len(orders.customer_id)


def get_total_discount_overall():
    return sum(order_lines.full_price_amount * order_lines.discount_rate)


def get_average_discount_rate_overall():
    return get_total_discount_overall() / sum(order_lines.full_price_amount)


def get_average_order_total_overall():
    return sum(order_lines.total_amount) / len(set(order_lines.order_id))


class MyTestCase(unittest.TestCase):
    def test_sum_daily_items_equal_total_items(self):
        self.assertEqual(sum([get_num_items(date) for date in date_strings]), get_total_items_sold_overall())

    def test_sum_daily_customers_equal_total_customers(self):
        self.assertEqual(sum([get_num_customers(date) for date in date_strings]), get_total_customers_overall())

    def test_sum_daily_discount_equal_total_discount(self):
        self.assertAlmostEqual(sum([get_total_discount(date) for date in date_strings]), get_total_discount_overall(), 2)

    def test_mean_daily_average_discount_rate_equal_average_total_discount_rate(self):
        self.assertAlmostEqual(sum([get_average_discount_rate(date) for date in date_strings]) / len(date_strings),
                               get_average_discount_rate_overall(), 2)


if __name__ == '__main__':
    unittest.main()
