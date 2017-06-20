import re

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
from config import *
import pymysql.cursors

conn = pymysql.connect(host=MYSQL_URL,
                       port=MYSQL_PORT,
                       user=MYSQL_USER,
                       password=MYSQL_PASSWORD,
                       db=MYSQL_DB,
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

driver = webdriver.Chrome()
# driver = webdriver.PhantomJS(service_args=SERVICE_ARGS)
driver.set_window_size(1200, 900)
wait = WebDriverWait(driver, 10)


def save_to_mysql(result):
    values = []
    for k,v in sorted(result.items()):
        values.append(v)
    try:
        with conn.cursor() as cursor:
            sql = 'INSERT INTO ' + MYSQL_TABLE_JD + '(Comment,Image,Price,Shop,Title) VALUES(%s,%s,%s,%s,%s)'
            cursor.execute(sql, values)
        # connection is not autocommit by default. So you must commit to save your changes.
        conn.commit()
        with conn.cursor() as cursor:
            sql = 'SELECT * FROM ' + MYSQL_TABLE_JD + ' WHERE ' \
                                                      'Comment=%s AND ' \
                                                      'Image=%s AND ' \
                                                      'Price=%s AND ' \
                                                      'Shop=%s AND ' \
                                                      'Title=%s'
            cursor.execute(sql, values)
            query = cursor.fetchone()
            print(query)
    except Exception:
        print("Save MYSQL FAILED")


def get_products():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#J_goodsList .gl-item')))
    html = driver.page_source
    doc = pq(html)
    items = doc('#J_goodsList .gl-item').items()
    for item in items:
        product = {
            'image': item.find('.p-img .err-product').attr('src'),
            'price': item.find('.p-price').text(),
            'comment': item.find('.p-commit').text(),
            'title': item.find('.p-name').text(),
            'shop': item.find('.p-shop').text(),

        }
        print(product)
        # save_to_mysql(product)

def search():
    print("---搜索关键字: " + KEY_WORD_JD)
    try:
        driver.get("http://www.jd.com")
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#key"))
        )
        input.send_keys(KEY_WORD_JD)
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#search > div > div.form > button > i"))
        )
        submit.click()
        get_products()
    except TimeoutError:
        return search()


def get_page_number():
    total = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#J_bottomPage > span.p-skip > em:nth-child(1)"))
    )
    total = re.compile('(\d+)').search(total.text).group(1)
    return int(total)


def next_page(page_number):
    print("---开始翻页: " + str(page_number))
    try:
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#J_bottomPage > span.p-skip > input"))
        )
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#J_bottomPage > span.p-skip > a"))
        )
        input.clear()
        input.send_keys(page_number)
        submit.click()
        wait.until(
            EC.text_to_be_present_in_element(
                (By.CSS_SELECTOR, '#J_bottomPage > span.p-num > a.curr'), str(page_number))
        )
        get_products()
    except TimeoutException:
        next_page(page_number)


def main():
    try:
        search()
        total = get_page_number()
        print("Total: " + str(total))
        for page_number in range(2, total+1):
            next_page(page_number)
    except Exception:
        print("ERROR!")
    finally:
        driver.close()
        conn.close()

if __name__ == '__main__':
    main()
