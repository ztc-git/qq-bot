from selenium import webdriver
import time

def text_generator(title):
    browser = webdriver.Chrome()
    url = 'https://suulnnka.github.io/BullshitGenerator/index.html'
    browser.get(url)

    # 输入题目
    input = browser.input = browser.find_element_by_xpath('//*[@id="主题"]/input')
    input.clear()
    input.send_keys(title)
    time.sleep(0.5)

    # 生成文章
    button = browser.find_element_by_xpath('//*[@id="主题"]/button')
    button.click()

    # 抓取
    text_list = browser.find_elements_by_xpath('//*[@id="文章"]/div')
    text = ''
    for i in text_list:
        text = text + '\n' + i.text

    browser.close()
    return text
