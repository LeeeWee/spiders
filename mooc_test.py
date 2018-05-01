import selenium
from selenium import webdriver
import time

#stuId = input('请输入学号： ')
#password = input('请输入密码： ')
stuId = '2017202110062'
password = '143015'

moocUrl = 'http://www.mooc.whu.edu.cn/portal'
driver = webdriver.Chrome()
driver.get(moocUrl)

# find login button and click
driver.find_element_by_class_name('loginSub').click()
time.sleep(3)

driver.find_element_by_id('username').send_keys(stuId)
driver.find_element_by_id('password').send_keys(password)
driver.find_element_by_class_name('btn-login').click()
