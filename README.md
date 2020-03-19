## Google trends crawler  
Provides simple data from two types of trends from [Google Trends](https://trends.google.com/trends):  
* Realtime trends (provided against countries and categories)
* Daily Search Trends (provided against countries)

Because this is based on [Selenium](https://github.com/SeleniumHQ/selenium), it requires a webdriver. The webdriver chosen for this code is the chromedriver which can be downloaded from [here](https://chromedriver.chromium.org/downloads).  

### Usage:  
```python
import trends

chromeDirectory = "path/to/chromedriver"
driver = trends.setDriver(chromeDirectory)

# for realtime results
print(trends.getRealtimeTrends(driver, country = "Germany", category = "entertainment"))

# for daily
print(trends.getDailySearchTrends(driver, country = "United Kingdom"))
```
