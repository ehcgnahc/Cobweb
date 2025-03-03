from selenium import webdriver

request_url = "https://www.google.com"

driver = webdriver.Chrome()
driver.get(request_url)
source = driver.page_source
print(source)
driver.quit()