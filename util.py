from ast import literal_eval
import os
import json

db_path = './product.json'


def open_json(data_filename):
    with open(data_filename) as feedsjson:
        feeds = json.load(feedsjson)
    return feeds

def read_testfreak_db_urls() -> list:
    if not os.path.isfile(db_path):
        return []
    json_list = open_json(db_path)
    url_list = []
    for i,json in enumerate(json_list):
        url_list = json["url"]
    return url_list

def read_from_txt(filename) -> list:
    with open(filename) as f:
        lines = f.readlines()
    temp = [line for line in lines if line.strip() != '']
    return temp

def get_testfreak_db_pros_cons(product_name):
    json_list = open_json(db_path)
    for json in json_list:
        if json["product_name"] == product_name:
            return json["pros"], json["cons"]
    return [], []

def is_cached_item(item) -> bool:
    normalized_item = item.lower().split(' |,|-|_')
    if 'hp' in normalized_item or 'laptop' in normalized_item or 'notebook' in normalized_item:
        return True
    else:
        return False

def get_cached_item_name(item):
    normalized_item = item.lower().split(' |,|-|_')
    if 'hp' in normalized_item or 'laptop' in normalized_item or 'notebook' in normalized_item:
        return 'hp laptop'
    elif 'apple' in normalized_item or 'iphone' in normalized_item or 'phone' in normalized_item:
        return 'iphone 11'
    return ''
