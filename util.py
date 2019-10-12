import pandas as pd
from ast import literal_eval
import os

def read_urls_from_testfreak_db() -> list:
    db_path = './testfreak_db.csv'
    if not os.path.isfile(db_path):
        return []
    df = pd.read_csv(db_path)
    return df['url'].tolist()

def read_from_txt(filename) -> list:
    with open(filename) as f:
        lines = f.readlines()
    temp = [line for line in lines if line.strip() != '']
    return temp
