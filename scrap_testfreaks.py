from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from textblob import TextBlob
import pandas as pd
import time
import random
import os
from proxy import proxy_list
import util

def update_testfreak_db(url):
    # cap = DesiredCapabilities().FIREFOX
    # cap["marionette"] = False
    geckodriver_path = './geckodriver'

    proxy = Proxy()
    proxy.proxy_type = ProxyType.MANUAL
    proxy.http_proxy = proxy_list[random.randrange(0, len(proxy_list))]

    options = Options()
    options.headless = True

    browser = webdriver.Firefox(options=options, proxy=proxy, executable_path=geckodriver_path)

    browser.get(url)
    # browser.implicitly_wait(5)

    # element = browser.find_element_by_xpath("//div[@class='container']" \
    #                               +"//div[@class='row']"\
    #                               +"//div[@class='col-sm-12']"\
    #                               +"//div[@id='tf-tabs']"\
    #                               +"//div[@class='testfreaks-reviews']"\
    #                               +"//div[@id='testfreaks']"\
    #                               +"//div[@class='tf-tabs-panels']"\
    #                               +"//div[@id='tf-panel-pro']"\
    #                               +"//div[@class='article review']"\
    #                               +"//div[@class='content']"\
    #                               +"//div[@class='extract']"\
    #                               +"//p[@class='formatted']");
    #                               # +"//div[@class='read-more iconmore']");
    # element = browser.find_element_by_class_name("formatted")
    # print (element.text)

    element2 = browser.find_element_by_class_name("read-more")

    browser.execute_script("arguments [0].click();", element2)
    time.sleep(3)
    element3 = browser.find_elements_by_xpath("//p[@class='formatted']")
    # pros_element = browser.find_elements_by_class_name("pros")
    pros_element = browser.find_elements_by_xpath("//div[@class='content']//div[@class='pros']")
    cons_element = browser.find_elements_by_class_name("cons")

    review_list = []
    for x in range(len(element3)):
        textblobr = TextBlob(element3[x].text)
        if (textblobr.detect_language() != 'en'):
            translatedr = str(textblobr.translate(to='en'))  # powered by Google Translate
        else:
            translatedr = str(textblobr)
        # print("Original text:========")
        # print(element3[x].text)
        # print("Translated text:========")
        # print(translatedr)
        review_list.append(translatedr)

    ptranslatedr_list = []
    ctranslatedr_list = []
    for x in range(len(pros_element)):
        ptextblobr = TextBlob(pros_element[x].text)
        ctextblobr = TextBlob(cons_element[x].text)
        if (ptextblobr.detect_language() != 'en'):
            ptranslatedr = str(ptextblobr.translate(to='en'))  # powered by Google Translate
        else:
            ptranslatedr = str(ptextblobr)
        if (ctextblobr.detect_language() != 'en'):
            ctranslatedr = str(ctextblobr.translate(to='en'))  # powered by Google Translate
        else:
            ctranslatedr = str(ctextblobr)
        # print(ptranslatedr)
        # print(ctranslatedr)
        ptranslatedr_list.append(ptranslatedr[5:])
        ctranslatedr_list.append(ctranslatedr[5:])

    browser.quit()

    name = url.split('/')[-2]
    df = pd.DataFrame({
        'product_name': name, 
        'url': url,
        'review': [review_list],
        'pros': [ptranslatedr_list],
        'cons': [ctranslatedr_list]
    })

    db_path = "./testfreak_db.csv"
    if os.path.isfile(db_path):
        old_df = pd.read_csv(db_path)
        old_df = old_df.append(df, ignore_index=True, sort=False)
        old_df.to_csv(db_path, index=False)
    else:
        df.to_csv(db_path, index=False)
    print(f'Scraped product from: {url}')

urls = util.read_from_txt('scrape_urls.txt')
testfreak_db_urls = util.read_urls_from_testfreak_db()
for url in urls:
    if url not in testfreak_db_urls:
        update_testfreak_db(url)