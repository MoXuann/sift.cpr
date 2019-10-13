import pandas as pd
from ast import literal_eval
import os

db_path = './testfreak_db.csv'

def read_testfreak_db_urls() -> list:
    if not os.path.isfile(db_path):
        return []
    df = pd.read_csv(db_path)
    return df['url'].tolist()

def read_from_txt(filename) -> list:
    with open(filename) as f:
        lines = f.readlines()
    temp = [line for line in lines if line.strip() != '']
    return temp

def get_testfreak_db_pros_cons(product_name):
    df = pd.read_csv(db_path)
    pros_str = df[df['product_name'] == product_name]['pros'].values
    print('\n')
    print(pros_str)
    print('\n')
    pros = literal_eval(pros_str)
    cons = literal_eval(df[df['product_name'] == product_name]['cons'])
    return pros, cons

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
