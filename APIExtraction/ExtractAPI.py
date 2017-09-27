# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from selenium import webdriver
import selenium
import logging
import logging.config
from selenium.webdriver.common.keys import Keys
import requests
import re
import os

logging.config.fileConfig('.\\APIExtraction\\logging.conf')
logger = logging.getLogger('main')

def getClasses(index_url):
    '''get classed of specify product in given index url
    
    Args: 
        index_url: Given api index url.
    
    Returns: 
        classes: dict of classes names and urls'''

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

def write_classes_index(index_output, api_url):
    '''write class name and class url index file to given output path

    Args: 
        index_output: Given index file path to write. 
        api_url: Given api url to read.'''

    classes = getClasses(api_url + 'index.html')
    f = open(index_output, 'w')
    for singleClass in classes:
        class_name = singleClass.replace('/', '.')[0:singleClass.index('.')]
        class_url = api_url + singleClass
        f.write(class_name + ' ' + class_url + '\n')
    print('Writing finished!')
    f.close()

def read_classes_index(index_path):
    '''read classes and urls and return a dict'''

    f = open(index_path, 'r')
    classes = {}
    for line in f.readlines():
        classes[line.split(' ')[0]] = line.split(' ')[1][0:line.split(' ')[1].index('\n')]
    return classes


def get_desciption(class_url):
    '''get class description in given class url

    Args: 
        class_url: Given class url to read
    
    Returns: 
        description: Description of specified class'''

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

def save_description(api_url, index_path, output_directory):
    '''save description of classes in specified api_url to output directory

    Args: 
        api_url: Given api_url, 
            e.g. 'http://help.eclipse.org/oxygen/topic/org.eclipse.jdt.doc.isv/reference/api/'
        index_path: Given index file path which contains classes names and urls, 
            if file doesn't exist, call write_classes_index method, e.g. 
            'D:\\data\\working\\api\\eclipse.jdt_api.i'
        output_directory: Given directory to save descriptions of classes, e.g.
            'D:\\data\\working\\api\\eclipse.jdt_api\\'  
    
    Raises: 
        selenium.common.exceptions.NoSuchFrameException
        UnicodeEncodeError'''

    if not os.path.exists(index_path):
        write_classes_index(index_path, api_url)
    classes = read_classes_index(index_path)
    count = 0
    logger.info('Begging to store api...')
    for single_class in classes:
        count += 1
        if os.path.exists(output_directory + single_class):
            continue
        logger.info('Loading api for ' + single_class)
        if count % 20 == 0:
            logger.info(str(count) + ' api stored!')
        try:
            f = open(output_directory + single_class, 'w', encoding='utf-8')
            description = get_desciption(classes[single_class])
            f.write(description)
            f.close()
        except selenium.common.exceptions.NoSuchFrameException as e :
            logger.error('selenium.common.exceptions.NoSuchFrameException: ' + single_class)


def get_error_classes(log_file, index_path):
    '''read extraction log file and extract classes with error

    Args: 
        log_file: Given extract_api log file.
        index_path: Given index file path which contains classes name and urls.

    Returns: 
        error_classes: Dict of classes with error.'''
    logger.info("Getting error classes...")
    f = open(log_file, 'r', encoding='utf-8')
    classes = read_classes_index(index_path)
    error_classes = {}
    for line in f.readlines():
        if re.match(r'.*- ERROR -.*', line):
            class_name = line.split(': ')[1].split('\n')[0]
            if not classes.get(class_name):
                continue
            error_classes[class_name] = classes[class_name]
    return error_classes

def extract_error_class_description(error_classes, output_directory):
    count = 0
    lenth = len(error_classes)
    if not lenth == 0:
        logger.info(str(lenth) + ' error classes left!')
        reserved_classes = {}
        for single_class in error_classes:
            count += 1
            logger.info('Loading api for ' + single_class)
            if count % 20 == 0:
                logger.info(str(count) + ' api stored!')
            try:
                f = open(output_directory + single_class, 'w', encoding='utf-8')
                description = get_desciption(error_classes[single_class])
                f.write(description)
                f.close()
            except selenium.common.exceptions.NoSuchFrameException as e :
                logger.error('selenium.common.exceptions.NoSuchFrameException: ' + single_class)
                reserved_classes[single_class] = error_classes[single_class]
        # Extract description for error classes iteratively.
        extract_error_class_description(reserved_classes, output_directory)


'''
if __name__ == "__main__":
    jdt_api_url = 'http://help.eclipse.org/oxygen/topic/org.eclipse.jdt.doc.isv/reference/api/'
    index_path = 'D:\\data\\working\\api\\eclipse.jdt_api.i'
    output_directory = 'D:\\data\\working\\api\\eclipse.jdt.ui\\'
    save_description(jdt_api_url, index_path, output_directory)
'''

if __name__ == '__main__':
    log_file = 'D:\\Data\\working\\api\\eclipse.jdt_api3.log'
    index_path =  'D:\\Data\\working\\api\\eclipse.jdt_api.i'
    output_directory = 'D:\\data\\working\\api\\eclipse.jdt.ui\\'
    error_classes = get_error_classes(log_file, index_path)
    extract_error_class_description(error_classes, output_directory)