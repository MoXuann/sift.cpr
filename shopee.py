import requests
import random
from copy import deepcopy
from proxy import proxy_list

_shopee_base_url = "https://shopee.sg"
_shopee_image_url = "https://cf.shopee.sg/file"
_user_agent_header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0"
}
proxy_dict = {"http": proxy_list[random.randrange(0, len(proxy_list))]}

def get_product_info(item_id, shop_id, review_num=10):
    try:
        product_json = _get_product(item_id, shop_id)
        if product_json == None:
            return {}

        product_link = _get_product_link(product_json['name'], product_json['itemid'], product_json['shopid'])

        # Only send back some essential information. Image strings are replaced with url strings to the image
        # Note that models may be [] (empty) and shipping fee is fetched from another get request.
        product = {
            "origin": "shopee",
            "image": _get_image_links(product_json['image'])[0],
            "name": product_json['name'],
            "price": _normalize_price(product_json['price_min']),
            "description": product_json['description'],
            'product_url': product_link,
            "rating": product_json['item_rating']['rating_star'],
            "rating_num": sum(product_json['item_rating']['rating_count']),
            "reviews": get_reviews(item_id, shop_id, review_num),
            "Error": None
        }
        return product
    except Exception as e:
        return{"Error": str(e)}

def get_search_results(keyword, search_num=10) -> list:
    '''Gets the results of search from keyword'''
    # &matchid= after limit is ommited to simplify search
    get_url = f"{_shopee_base_url}/api/v2/search_items/?by=relevancy&keyword={str(keyword)}&limit={str(search_num)}&newest=0&order=desc&page_type=search"
    r = requests.get(get_url, headers=_user_agent_header, proxies=proxy_dict)
    items = r.json()['items']

    if items == None or items == []:
        return []

    filtered = []
    for item in items:
        filtered.append({
            "brand": item['brand'],
            "image": _get_image_links(item['image'])[0],
            "name": item['name'],
            "item_id": item['itemid'],
            "shop_id": item['shopid'],
            "rating": item['item_rating']['rating_star']
        })
    return filtered

def get_reviews(item_id, shop_id, review_num=10) -> list:
    """ Returns [] if no rating
    """
    get_url = f"{_shopee_base_url}/api/v2/item/get_ratings?filter=0&flag=1&itemid={item_id}&limit={review_num}&offset=0&shopid={shop_id}"
    r = requests.get(get_url, headers=_user_agent_header, proxies=proxy_dict)
    ratings = r.json()['data']['ratings']
    reviews = []
    for rating in ratings:
        reviews.append({
            'origin': 'shopee',
            'author': rating['author_username'],
            'rating': rating['rating_star'],
            'review': rating['comment'], 
            'review_likes': rating['like_count'],
            'summary': 'Summary is very nice. Amazing!'
            })
    return reviews

def get_did_you_mean(keyword, keyword_num, offset) -> list:
    get_url = f"{_shopee_base_url}/api/v2/product_catalogue/get?keyword={keyword}&limit={str(keyword_num)}&offset={str(offset)}&sort_type=0"
    r = requests.get(get_url, headers=_user_agent_header, proxies=proxy_dict)
    catalogue_dict = r.json()['data']['items']
    catalogue_list = []
    for item in catalogue_dict:
        catalogue_list.append({
            'name': item['spu_name'],
            'image': _get_image_links(item['cover_img'])[0],
            'price': _normalize_price(item['average_price'])
            })
    search_hints = get_search_hint(keyword)
    for hint in search_hints:
        catalogue_list.append({
            'name': hint,
            'image': '',
            'price': ''
        })
    if len(catalogue_list) - 1 > int(keyword_num):
        catalogue_list = catalogue_list[:int(keyword_num)]
    item_list = []
    for item in catalogue_list:
        if item['name'].lower() != keyword.lower():
            item_list.append(item)
    return item_list

def get_search_hint(keyword) -> list:
    '''Gets related search hints according to keyword. For search bar.'''
    get_url = _shopee_base_url + "/api/v2/search_hint/get?keyword=" + str(keyword) +"&search_type=0"
    r = requests.get(get_url, headers=_user_agent_header, proxies=proxy_dict)
    items = r.json()['keywords']

    # Remove duplicate keyword names and category info. Some key suggestions have same names but different category
    item_list = []
    for item in items:
        key = item['keyword']
        if key not in item_list:
            item_list.append(key)

    return item_list

def _get_product_link(name, item_id, shop_id) -> str:
    temp = name.replace(' ', '-')
    url = f'{_shopee_base_url}/{temp}-i.{item_id}.{shop_id}'
    return url

def _get_image_links(image_ids) -> list:
    '''Returns an array of image links from an array of image Ids'''
    result = []
    for image_id in image_ids:
        result.append(_shopee_image_url  + "/" + str(image_id))
    return result

def _normalize_price(price) -> int:
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
