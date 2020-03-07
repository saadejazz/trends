import trends

chromeDirectory = "chrome/chromedriver"

driver = trends.setDriver(chromeDirectory)

# for realtime results
print(trends.getRealtimeTrends(driver, country = "Germany", category = "entertainment"))

# for daily
print(trends.getDailySearchTrends(driver, country = "United Kingdom"))
