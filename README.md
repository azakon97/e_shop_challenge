Suade Labs Python Challenge
This is a Python & Flask project representing a simple analytics component for an imaginary  e-shop with an api endpoint
which for a given date  will return a report that will contain the following metrics:
The total number of items sold on that day.
The total number of customers that made an order that day.
The total amount of discount given that day.
The average discount rate applied to the items sold that day.
The average order total for that day
The total amount of commissions generated that day.
The average amount of commissions per order for that day.
The total amount of commissions earned per promotion that day

Example endpoint response:
 {
 "customers": 877,
 "total_discount_amount": 23207660.62,
 "items": 291544,
 "order_total_avg": 14857290.47,
 "discount_rate_avg": 0.15,
 "commissions": {
     "promotions": {
         "1": 30789016.52,
         "3": 8054710.81,
         "2": 20082936.33,
         "5": 22946449.12,
         "4": 27573451.86
     },
     "total": 2532657169.95,
     "order_average": 2743940.59
     }
 }

# Usage:

Before running you need the following libraries installed: Flask, Pandas

To run in terminal:
1) python3 src/app.py
2) click on the url and enter forward slash, '/', followed by date in the right format: 'YYYY-MM-DD',
between 2019-08-01 and 2019-09-29 inclusive

