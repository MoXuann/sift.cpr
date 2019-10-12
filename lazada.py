# Image link format
# https://my-test-11.slatic.net/p/0cda36dd9e6cf038d3234768ce235a3a.jpg_720x720q80.jpg_.webp

# Product data format
# https://pdpdesc-m.lazada.sg/recommend?shop_id=3147&category_id=155&item_id=336748901&anonymous_id=b2772457-7c90-4974-b5e5-e56de60b1485&regional_key=030101020000&is_ab=false&sku=336748901_SGAMZ-734722704&seller_id=2297&is_tbc=0&_=1570857661416&brand_id=30229

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
import random
from proxy import proxy_list

def get_search_results(search_term, count=0):
    link = r'https://www.lazada.sg/catalog/?q='+ search_term + r'&_keyori=ss&from=input&spm=a2o42.pdp.search.go'
    try:
        proxy = Proxy()
        proxy.proxy_type = ProxyType.MANUAL
        proxy.http_proxy = proxy_list[random.randrange(0, len(proxy_list))]
        # prox.socks_proxy = "ip_addr:port"
        # prox.ssl_proxy = "ip_addr:port"

        options = Options()
        options.headless = True
        driver = webdriver.Firefox(options=options, proxy=proxy, executable_path='./geckodriver')

        driver.get(link)
        web_result = driver.execute_script('return pageData.mods.listItems')
        driver.quit()

        search_data = {}
        if len(web_result) > 10:
            web_result = web_result[:10]
        for i,result in enumerate(web_result):
            search_data[i] = {
                'brand_name': result['brandName'], 
                'image': result['image'],
                'name': result['name'],
                'price': result['priceShow'],
                'description': '',
                'product_url': result['productUrl'].strip("/"),
                'rating': result['ratingScore'],
                'rating_num': result['review'],
                'Error': None
                }
        return search_data
    except ReferenceError as e:
        print("Captcha encountered")
        print(e)
        if count < 10:
            get_search_results(search_term, count=count+1)
        else:
            return {"Error": "Captcha encountered. Unable to circumvent."}
    except Exception as e:
        print("Error encountered.")
        print(e)
        return {"Error:": str(e)}
