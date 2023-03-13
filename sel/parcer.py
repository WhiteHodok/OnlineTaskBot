import datetime
from selenium import webdriver

today = datetime.date.today()
today_str = today.strftime("%d.%m.%Y")

url = f"https://rasp.omgtu.ru/?t={today_str}"
group = 'АТП-221'

options = webdriver.ChromeOptions()
options.add_argument('headless')
browser = webdriver.Chrome(options=options)
browser.get(url)
input_field = browser.find_element_by_id('group')
input_field.send_keys(group)
button = browser.find_element_by_xpath('//button[text()="Найти"]')
button.click()
table = browser.find_element_by_xpath('//table[@Class="table table-bordered table-striped table-hover"]')
print(table.text)
browser.quit()