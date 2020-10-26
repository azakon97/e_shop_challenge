import pandas as pd

orders = pd.read_csv('data/orders.csv')
order_lines = pd.read_csv('data/order_lines.csv')
commissions = pd.read_csv('data/commissions.csv')
product_promotions = pd.read_csv('data/product_promotions.csv')

# 'created_at' is a column of timestamps so we convert it to date and save it in 'date' column
orders['date'] = pd.to_datetime(orders['created_at']).dt.floor('D')


def get_date_orders(date_string):
    return orders.loc[orders.date == pd.to_datetime(date_string)]


def get_date_order_ids_set(date_string):
    return set(get_date_orders(date_string).id)


def get_date_order_lines(date_string):
    return order_lines.loc[order_lines.order_id.isin(get_date_order_ids_set(date_string))]


def get_date_commissions(date_string):
    return commissions.loc[commissions.date == date_string]


def get_date_product_promotions(date_string):
    return product_promotions.loc[product_promotions.date == date_string]


def get_num_items(date_string):
    date_order_lines = get_date_order_lines(date_string)
    return sum(date_order_lines.quantity)


def get_num_customers(date_string):
    return len(list(get_date_orders(date_string).customer_id))


def get_total_discount(date_string):
    date_order_lines = get_date_order_lines(date_string)
    return sum(date_order_lines.full_price_amount * date_order_lines.discount_rate)


def get_average_discount_rate(date_string):
    date_order_lines = get_date_order_lines(date_string)
    return get_total_discount(date_string) / sum(date_order_lines.full_price_amount)


def get_avg_total_order(date_string):
    date_order_lines = get_date_order_lines(date_string)
    return sum(date_order_lines.total_amount) / len(set(date_order_lines.order_id))


def get_date_order_lines_with_commissions(date_string):
    date_orders = get_date_orders(date_string)
    date_order_lines = get_date_order_lines(date_string)
    order_lines_vendor = pd.merge(date_order_lines, date_orders, how='inner',
                                  left_on='order_id', right_on='id')[
        ['order_id', 'product_id', 'vendor_id', 'discounted_amount']]
    date_commissions = get_date_commissions(date_string)
    return pd.merge(order_lines_vendor, date_commissions, how='inner', on='vendor_id')


def get_total_commission(date_string):
    order_lines_commission = get_date_order_lines_with_commissions(date_string)
    return sum(order_lines_commission.discounted_amount * order_lines_commission.rate)


def get_avg_commission(date_string):
    return get_total_commission(date_string) / len(get_date_order_ids_set(date_string))


def get_commissions_per_promotion(date_string):
    order_lines_commission = get_date_order_lines_with_commissions(date_string)
    date_product_promotions = get_date_product_promotions(date_string)
    commission_promotion_df = pd.merge(order_lines_commission, date_product_promotions,
                                       how='inner', on='product_id')[['discounted_amount', 'rate', 'promotion_id']]
    commission_promotion_df['commission'] = commission_promotion_df.discounted_amount * commission_promotion_df.rate
    grouping = commission_promotion_df.groupby('promotion_id')
    return {str(k): round(v, 2) for k, v in grouping.discounted_amount.sum().to_dict().items()}
