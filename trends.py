from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
import json
import re

def setDriver(executable_path):
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    chrome_options.add_experimental_option("prefs",prefs)
    return webdriver.Chrome(executable_path = executable_path, chrome_options=chrome_options)

def getTrendsList(elements, extractGroup):
    results = []
    beautifyText = lambda text: " ".join([a for a in text.replace("\n", "").split() if not a == ""])
    for element in elements:
        result = {
            "keywords": "",
            "article_name": "",
            "article_link": ""
        }
        soup = BeautifulSoup(str(element))
        text = soup.find('div', {'class': 'details-top'})
        if text:
            result["keywords"] = beautifyText(text.text)
        else:
            continue
        text = soup.find('div', {'summary-text'})
        if text:
            text = text.find('a')
            result["article_name"] = beautifyText(text.text)
            result["article_link"] = text.get('href')
        results.append(result)
        if extractGroup == "daily":
            result["search_count"] = ""
            count = soup.find('div', {'class': 'search-count-title'})
            if count:
                result["search_count"] = count.text
    return results

def extractFromUrl(driver, url, maxIter = 1, extractType = "realtime"):
    iterations = 1
    driver.get(url)
    wait = WebDriverWait(driver, 4)
    while(iterations < maxIter):
        iterations += 1
        try:
            more = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'feed-load-more-button')))
            driver.execute_script("arguments[0].click();", more)
        except TimeoutException:
            break
    try:
        elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//md-list[contains(@class, "md-list-block")]')))
    except TimeoutException:
        return []
    return getTrendsList([element.get_attribute('innerHTML') for element in elements], extractGroup = extractType)

def getRealtimeTrends(driver, country = "united_states", category = "all", depth = 1):

    with open("codes/country_codes.json", "r") as jso:
        countryCodes = json.load(jso)
    with open("codes/category_codes.json", "r") as jso:
        categoryCodes = json.load(jso)
    
    smallify = lambda text: "_".join(str.lower(str(text)).split())
    country = smallify(country)
    category = smallify(category)

    if country not in countryCodes:
        print("Country not in index")
        return []
    if category not in categoryCodes:
        print("Invalid category")
        return []
    
    url = 'https://trends.google.com/trends/trendingsearches/realtime?'
    url = f'{url}geo={countryCodes[country]}&category={categoryCodes[category]}'
    return extractFromUrl(driver, url, depth)

def getDailySearchTrends(driver, country = "united_states", depth = 1):
    with open("codes/country_codes.json", "r") as jso:
        countryCodes = json.load(jso)
    smallify = lambda text: "_".join(str.lower(str(text)).split())
    country = smallify(country)
    if country not in countryCodes:
        print("Country not in index")
        return []
    url = 'https://trends.google.com/trends/trendingsearches/daily?'
    url = f'{url}geo={countryCodes[country]}'
    return extractFromUrl(driver, url, depth, extractType = "daily")
