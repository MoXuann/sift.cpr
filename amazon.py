import db

def get_product_info(name):
    normalized_name = name.lower().split(' |,|-|_')
    if 'hp' in normalized_name or 'laptop' in normalized_name or 'notebook' in normalized_name:
        return db.HP_Notebook['amazon']
    else:
        return []
