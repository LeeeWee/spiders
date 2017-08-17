from bs4 import BeautifulSoup
from selenium import webdriver
import selenium
import logging
import logging.config
from selenium.webdriver.common.keys import Keys
import requests
import re

def getClasses(index_url):
    driver = webdriver.PhantomJS()
    driver.get(index_url)
    driver.switch_to.frame("HelpFrame")
    driver.switch_to.frame("ContentFrame")
    driver.switch_to.frame("ContentViewFrame")
    driver.switch_to.frame("packageFrame")
    class_html = driver.page_source
    driver.quit()
    classes = {}
    soup = BeautifulSoup(class_html, 'html.parser')
    for li in soup.find_all('li'):
        # li sample: <li><a href="org/eclipse/jdt/launching/AbstractJavaLaunchConfigurationDelegate.html"
        # target="classFrame" title="class in org.eclipse.jdt.launching">AbstractJavaLaunchConfigurationDelegate</a></li>
        classes[li.a.get('href')] = li.a.string
    return classes

def write_classes_index(index_output, jdt_api_url):
    classes = getClasses(jdt_api_url + 'index.html')
    f = open(index_output, 'w')
    for singleClass in classes:
        class_name = singleClass.replace('/', '.')[0:singleClass.index('.')]
        class_url = jdt_api_url + singleClass
        f.write(class_name + ' ' + class_url + '\n')
    print 'Writing finished!'
    f.close()

def read_classes_index(index_path):
    f = open(index_path, 'r')
    classes = {}
    for line in f.readlines():
        classes[line.split(' ')[0]] = line.split(' ')[1][0:line.split(' ')[1].index('\n')]
    return classes

def get_desciption(class_url):
    driver = webdriver.PhantomJS()
    driver.get(class_url)
    driver.switch_to.frame("HelpFrame")
    driver.switch_to.frame("ContentFrame")
    driver.switch_to.frame("ContentViewFrame")
    class_html = driver.page_source
    driver.close()
    soup = BeautifulSoup(class_html, 'html.parser')
    description = soup.find("div", class_="description").get_text()
    return description

if __name__ == "__main__":
    logging.config.fileConfig('logging.conf')
    logger = logging.getLogger('main')

    jdt_api_url = 'http://help.eclipse.org/oxygen/topic/org.eclipse.jdt.doc.isv/reference/api/'
    index_path = 'D:\\data\\working\\eclipse.jdt_api.i'
    output_directory = 'D:\\data\\working\\api\\'
    # write_classes_index(index_path, jdt_api_url)
    classes = read_classes_index(index_path)
    count = 0
    logger.info('Begging to store api...')
    for single_class in classes:
        logger.info('Loading api for ' + single_class)
        count += 1
        if count % 20 == 0:
            logger.info(str(count) + ' api stored!')
        try:
            f = open(output_directory + single_class, 'w')
            description = get_desciption(classes[single_class])
            f.write(description)
            f.close()
        except selenium.common.exceptions.NoSuchFrameException, e:
            logger.error('selenium.common.exceptions.NoSuchFrameException: ' + single_class)
        except UnicodeEncodeError, e:
            logger.error('UnicodeEncodeError: ' + single_class)