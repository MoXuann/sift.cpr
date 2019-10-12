import requests
import random
from proxy import proxy_list

_shopee_base_url = "https://shopee.sg"
_shopee_image_url = "https://cf.shopee.sg/file"
_user_agent_header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0"
}
proxy_dict = {"http": proxy_list[random.randrange(0, len(proxy_list))]}

def get_product_info(item_id, shop_id):
    '''Returns product name, itemId, shopId, imageLinks, models, minPrice, shippingFee, categories, description as dict'''
    product_json = _get_product(item_id, shop_id)
    if product_json == None:
        return {}

    # Only send back some essential information. Image strings are replaced with url strings to the image
    # Note that models may be [] (empty) and shipping fee is fetched from another get request.
    product = {
        "image": product_json['image'],
        "name": product_json['name'],
        "price": _normalize_price(product_json['price_min']),
        "description": product_json['description'],
        'product_url': '',
        "rating": product_json['item_rating']['rating_star'],
        "rating_num": sum(product_json['item_rating']['rating_count']),
        "reviews": get_reviews(item_id, shop_id),
        "Error": None
    }
    return product

def get_search_results(keyword):
    '''Gets the results of search from keyword'''
    # &matchid= after limit is ommited to simplify search
    get_url = _shopee_base_url + "/api/v2/search_items/?by=relevancy&keyword=" + str(keyword) \
        + "&limit=10&newest=0&order=desc&page_type=search"
    r = requests.get(get_url, headers=_user_agent_header, proxies=proxy_dict)
    items = r.json()['items']

    if items == None or items == []:
        return {"items": []}

    filtered = []
    for item in items:
        filtered.append({
            "itemId": item['itemid'],
            "shopId": item['shopid'],
            "images": _get_image_links(item['images']),
            "name": item['name'],
            #"minPrice": self._normalize_price(item['price_min'])
        })
    return {"items": filtered}

def get_reviews(item_id, shop_id, review_num=10):
    """ Returns [] if no rating
    """
    get_url = f"{_shopee_base_url}/api/v2/item/get_ratings?filter=0&flag=1&itemid={item_id}&limit={review_num}&offset=0&shopid={shop_id}"
    r = requests.get(get_url, headers=_user_agent_header, proxies=proxy_dict)
    ratings = r.json()['data']['ratings']
    reviews = []
    for rating in ratings:
        reviews.append({
            'author': rating['author_username'],
            'rating': rating['rating_star'],
            'review': rating['comment'], 
            'review_likes': rating['like_count']
            })
    return reviews

def _get_image_links(image_ids):
    '''Returns an array of image links from an array of image Ids'''
    result = []
    for image_id in image_ids:
        result.append(_shopee_image_url  + "/" + str(image_id))
    return result

def _normalize_price(price):
    '''Normalizes prizes by dividing by 100000 or returning original price if price is invalid'''
    SHOPEE_PRICE_NORMALIZATION_CONSTANT = 100000
    try:
        if price == None or price == 0:
            pass
        elif price != 0:
            price /= SHOPEE_PRICE_NORMALIZATION_CONSTANT
        return price
    except:
        return price

def _get_product(item_id, shop_id):
    '''Returns a shopee product JSON according to the product ID and shop ID'''
    get_url = _shopee_base_url + "/api/v2/item/get?itemid=" + str(item_id) + "&shopid=" + str(shop_id)
    r = requests.get(get_url, headers=_user_agent_header, proxies=proxy_dict)
    return r.json()['item']
