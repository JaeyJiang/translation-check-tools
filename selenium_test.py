from selenium import webdriver
import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

d = webdriver.Firefox()
d.get('http://music.163.com/')
d.find_element_by_id("srch").send_keys('月亮惹的祸')
d.find_element_by_id("srch").send_keys(Keys.ENTER)
time.sleep(3)
d.switch_to.frame("contentFrame")
d.find_element_by_xpath('/html/body/div[3]/div/div[2]/div[2]/div/div/div[1]/div[2]/div/div/a/b/span').click()
time.sleep(3)
play_elem = d.find_element_by_xpath('/html/body/div[2]/div/div[1]/div[1]')
ActionChains(d).move_to_element(play_elem).perform()
time.sleep(10)
