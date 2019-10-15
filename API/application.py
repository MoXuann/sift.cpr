from flask import Flask
from flask import request, jsonify
import sys
import shopee
import lazada
import amazon
import youtube
import util
import random
# import pros_cons
# import summarizer

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

    if util.get_cached_item_name(keyword) == 'hp laptop':
        review = util.get_testfreak_db_reviews('hp-stream-14-z0xx-series-notebook-pc')

    elif util.get_cached_item_name(keyword) == 'iphone 11':
        review = util.get_testfreak_db_reviews('apple-iphone-11')
    else:
        return []
    # summary_list = summarizer.summarise(" ".join(review))
    # top_review_list, top_con_review_list = get_top_reviews(keyword)
    # all_full_reviews = top_review_list + top_con_review_list
    # all_reviews = [i.split(' ') for i in all_full_reviews]
    # summary_list.append(all_reviews)
    a, b = util.get_testfreak_db_pros_cons(review)
    summary_list_temp = a+b
    summary_list = [i.split(' ') for i in summary_list_temp]
    word_dict = {}
    for summary in summary_list:
        for word in summary:
            if word not in word_dict.keys():
                word_dict[word] = 1
            else:
                word_dict[word] += 1
    sorted_list = sorted(word_dict.items(), key = lambda kv:(kv[1], kv[0]))


    shopee_results = shopee.get_search_results(keyword, search_num, review_num)
    if sorted_list != []:
        for i,result in enumerate(shopee_results):
            result["image"] = result["Shopee"]["image"],
            result["description"] = result["Shopee"]["description"],
            result["top_review"] = sorted_list[0],
            result["top_con_review"] = '',
            result["overall_summary"] = sorted_list[:5],
            result["Amazon"] = amazon.get_product_info(keyword)
            result["Lazada"] = lazada.get_product_info(keyword)
        return jsonify(shopee_results)
    else:
        for i,result in enumerate(shopee_results):
            result["image"] = result["Shopee"]["image"],
            result["description"] = result["Shopee"]["description"],
            result["top_review"] = "excellent quality!",
            result["top_con_review"] = '',
            result["overall_summary"] = ['good', 'soso', 'excellent', 'quality'],
            result["Amazon"] = amazon.get_product_info(keyword)
            result["Lazada"] = lazada.get_product_info(keyword)
        return jsonify(shopee_results)

@application.route('/reviews',methods=['GET'])
def reviews():
    a_review = util.get_testfreak_db_reviews("hp-stream-14-z0xx-series-notebook-pc")
    b_review = util.get_testfreak_db_reviews("apple-iphone-11")
    return {
        "hp-stream-14-z0xx-series-notebook-pc": " ".join(a_review),
        "apple-iphone-11": " ".join(b_review)
    }

@application.route('/pros_con',methods=['GET'])
def pros_con():
    a_pro, a_con = util.get_testfreak_db_pros_cons("hp-stream-14-z0xx-series-notebook-pc")
    b_pro, b_con = util.get_testfreak_db_pros_cons("apple-iphone-11")
    return {
        "hp-stream-14-z0xx-series-notebook-pc": {
            "pros": a_pro,
            "cons": a_con
        },
        "apple-iphone-11": {
            "pros": b_pro,
            "cons": b_con
        }
    }


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
            "Shopee": shopee_results, 
            "Lazada": lazada_results, 
            "Amazon": amazon_results
            }
        return results
    except Exception as e:
        return {"Error": e}

def get_top_reviews(keyword):
    top_review = 'Good!'
    top_con_review = 'Average'
    
    if util.get_cached_item_name(keyword) == 'hp laptop':
        pros, cons = util.get_testfreak_db_pros_cons('hp-stream-14-z0xx-series-notebook-pc')
    elif util.get_cached_item_name(keyword) == 'iphone 11':
        pros, cons = util.get_testfreak_db_pros_cons('apple-iphone-11')
    else:
        return top_review, top_con_review
    pros_cons_list = pros_cons.pros_cons({"pros": pros, "cons": cons}, 10)
    top_review = pros_cons_list["pros"]
    top_con_review = pros_cons_list["cons"]
    return top_review, top_con_review

if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()