from flask import Flask, jsonify, request
from utils import (get_num_customers, get_num_items, get_total_discount, get_average_discount_rate,
                  get_avg_total_order, get_total_commission, get_avg_commission, get_commissions_per_promotion)

app = Flask(__name__)


@app.route('/')
def first_api():
    return jsonify(message='To get report for a chosen date, add \'/\' to the URL followed by a date with the '
                           'following format: \'YYYY-MM-DD\' between 2019-08-01 and 2019-09-29'), 200


@app.route('/<string:date>')
def get_report(date):
    try:
        report = {
            "customers": get_num_customers(date),
            "total_discount_amount": round(get_total_discount(date), 2),
            "items": get_num_items(date),
            "order_total_avg": round(get_avg_total_order(date), 2),
            "discount_rate_avg": round(get_average_discount_rate(date), 2),
            "commissions": {
                "total": round(get_total_commission(date), 2),
                "order_average": round(get_avg_commission(date), 2),
                "promotions": get_commissions_per_promotion(date)
            },
        }
        return report
    except:
        return jsonify(message="Date format is incorrect or date out of range. "
                               "The date must be between 2019-08-01 and 2019-09-29"), 404


if __name__ == '__main__':
    app.run()
