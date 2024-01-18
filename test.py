import time

from selenium import webdriver
from selenium.common import NoSuchElementException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

url_bank = 'https://srh.bankofchina.com/search/whpj/search_cn.jsp'
url_currency = 'https://www.11meigui.com/tools/currency'


def selenium_currency(url):
    """
    通过访问提供货币信息的网站，获取货币标准库。

    Parameters:
        url (str): 提供货币信息的网站 URL。

    Returns:
        dict: 包含货币标准符号和对应描述的字典。
    """
    currency_dic = {}
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    print('正在加载货币标准库，请稍等')

    # 循环遍历多个表格，获取货币信息
    for i in range(1, 6):
        j = 3
        while True:
            try:
                # 获取货币标准符号和描述，并添加到字典中
                currency_dic[driver.find_element(By.XPATH,
                                                 f'//*[@id="desc"]/table[{i}]/tbody/tr[{j}]/td[5]').text] = driver.find_element(
                    By.XPATH, f'//*[@id="desc"]/table[{i}]/tbody/tr[{j}]/td[2]').text
                j += 1
            except NoSuchElementException as _:
                break
    return currency_dic


def selenium_scrapy():
    """
    使用 Selenium 进行数据爬取和交互的主要函数。
    """
    # 获取货币标准库
    currency_dict = selenium_currency(url_currency)
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url_bank)

    while True:
        # 清空日期输入框
        driver.find_element(By.XPATH, f'//*[@id="historysearchform"]/div/table/tbody/tr/td[2]/div/input').clear()
        driver.find_element(By.XPATH, f'//*[@id="historysearchform"]/div/table/tbody/tr/td[4]/div/input').clear()

        # 获取用户输入
        input_ = input('请输入如下格式:货币标准符号(空格)日期(YYYYMMDD):')
        input_list = input_.split()

        if len(input_list) == 1:
            if input_list[0] == "N":
                break
            else:
                print('格式错误，请重新输入')
                continue

        currency, time_ = input_list[0], input_list[1]
        currency = currency.upper()

        # 在日期输入框中输入日期
        driver.find_element(By.XPATH, f'//*[@id="historysearchform"]/div/table/tbody/tr/td[2]/div/input').send_keys(
            time_)
        driver.find_element(By.XPATH, f'//*[@id="historysearchform"]/div/table/tbody/tr/td[4]/div/input').send_keys(
            time_)

        try:
            # 尝试选择货币标准符号
            Select(driver.find_element(By.XPATH, f'//*[@id="pjname"]')).select_by_visible_text(currency_dict[currency])
        except KeyError as _:
            print(f"货币格式错误")
            continue

        # 点击查询按钮
        driver.find_element(By.XPATH, f'//*[@id="historysearchform"]/div/table/tbody/tr/td[7]/input').click()
        time.sleep(1)

        try:
            # 尝试获取查询结果
            print(driver.find_element(By.XPATH, f'/html/body/div/div[4]/table/tbody/tr[2]/td[4]').text)
        except WebDriverException as _:
            print(f"输入错误")
            continue

        print('如果想结束，输入 N')

    # 关闭浏览器
    driver.quit()


if __name__ == '__main__':
    try:
        selenium_scrapy()
    except WebDriverException as e:
        print(f'网络连接错误:{e}')
