from flask import Flask
from flask import request, jsonify
import lazada
import shopee


# lazada.get_search_results("iphone")
# a = shopee.get_product_info(1529516322, 66397495)
reviews = shopee.get_reviews(1529516322, 66397495)
only_review_text = []
for review in reviews:
    only_review_text.append(review['review'])
print(only_review_text)