from flask import Flask
from flask import request, jsonify
import sys
import shopee
import lazada

application = Flask(__name__)

@application.route('/post', methods=['POST'])
def post():
    json = request.get_json()
    print(json, file=sys.stdout)
    #print('Error', file=sys.stderr)
    return jsonify({'success': True})

@application.route('/', methods=['GET'])
@application.route('/index', methods=['GET'])
def index():
    #print('Error', file=sys.stderr)
    # return jsonify({'success': True})
    return '<p>Hello! Nothing to show here!</p>\n'

@application.route('/nlp', methods=['GET'])
def nlp():
    review_num = request.args.get('review_num')
    # Default 10
    if review_num is None:
        review_num = 10
    else:
        review_num = int(review_num)
    reviews = shopee.get_reviews(1529516322, 66397495, review_num=review_num)
    only_review_text = []
    for review in reviews:
        only_review_text.append(review['review'])
    return {0: only_review_text}

@application.route('/did-you-mean', methods=['GET'])
def did_you_mean():
    keyword = request.args.get('keyword')
    search_num = request.args.get('search_num')
    offset = request.args.get('offset')
    if keyword is None:
        return {}
    if search_num is None:
        search_num = 10
    if offset is None:
        offset = 0
    recommendations = shopee.get_did_you_mean(keyword, search_num, offset)
    return {0: recommendations}

@application.route('/search', methods=['GET'])
def search():
    keyword = request.args.get('keyword')
    search_num = request.args.get('search_num')
    shopee_results = shopee.get_search_results(keyword, search_num)
    return


if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()