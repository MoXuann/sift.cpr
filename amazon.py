import db
import util

def get_product_info(name):
    if util.is_cached_item(name):
        return db.HP_Notebook['amazon']
    else:
        return []
