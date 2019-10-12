from flask import Flask
from flask import request, jsonify
import sys
import shopee
import lazada
import amazon
import youtube

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
    review_num = request.args.get('review_num')
    if keyword is None:
        return {}
    if search_num is None:
        search_num = 10
    shopee_results = shopee.get_search_results(keyword, search_num, review_num)
    for result in shopee_results:
        result["image"] = result["shopee"]["image"],
        result["description"] = result["shopee"]["description"],
        result["top_review"] = 'Top review. Wow.',
        result["Error"] = None,
        result["amazon"] = amazon.get_product_info(keyword)
        result["lazada"] = lazada.get_product_info(keyword)
    return {0: shopee_results}

def get_product(product_name, product_id, shop_id, review_num):
    try:
        if review_num is None:
            review_num = 10
        shopee_results = shopee.get_product_info(product_id, shop_id, review_num)
        lazada_results = lazada.get_product_info(product_name)
        amazon_results = amazon.get_product_info(product_name)
        results = {
            "image": shopee_results["image"],
            "description": shopee_results["description"],
            "top_review": 'Top review. Wow.',
            "shopee": shopee_results, 
            "lazada": lazada_results, 
            "amazon": amazon_results,
            "Error": None
            }
        return results
    except Exception as e:
        return {"Error": e}

@application.route('/test_lazada_search', methods=['GET'])
def test_lazada_search():
    keyword = request.args.get('keyword')
    search_num = request.args.get('search_num')
    if keyword is None:
        return {}
    if search_num is None:
        search_num = 10
    results = lazada.get_search_results(keyword, int(search_num))
    return {0: results}

@application.route('/youtube_search',methods=['GET'])
def youtube_search():
    video_title = request.args.get('video_title')
    max_result = request.args.get('max_result')
    
    if type(video_title) != str:
        video_title = "meme_video"
    if type(max_result) != str:
        max_result = 5
    else:
        max_result = int(max_result)
    
    return youtube.search_result(video_title, max_result)

if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()