from selenium import webdriver
from time import sleep
from scrapy.selector import Selector
import csv
import parameters

def check_empty(entity):
    if entity:
        pass
    else:
        entity = ''
    return entity.strip()


driver = webdriver.Chrome("chromedriver.exe")
driver.get('https://www.linkedin.com/')
email = driver.find_element_by_class_name("login-email")
email.send_keys(parameters.linkedin_username)
sleep(0.5)
password = driver.find_element_by_class_name("login-password")
password.send_keys(parameters.linkedin_password)
sleep(0.5)
driver.find_element_by_id("login-submit").click()
sleep(3)
driver.get('http://google.com')
sleep(2)
search = driver.find_element_by_name('q')
sleep(1)
search.send_keys(parameters.search_query)
search.send_keys("\n")
sleep(2)

urls = driver.find_elements_by_xpath('//cite[@class="_Rm"]')
linkedin_urls = [url.text for url in urls]
writer = csv.writer(open(parameters.file_name, 'w'))
writer.writerow(['Name', 'Headline', 'Company', 'School', 'Location', 'URL'])

for linkedin_url in linkedin_urls:
    # print(linkedin_url)
    driver.get(linkedin_url)
    sel = Selector(text=driver.page_source)
    name = check_empty(sel.xpath('//*[starts-with(@class, "pv-top-card-section__name")]/text()').extract_first())
    headline = check_empty( sel.xpath('//*[starts-with(@class, "pv-top-card-section__headline")]/text()').extract_first())
    company = check_empty(sel.xpath('//*[starts-with(@class, "pv-top-card-section__company")]/text()').extract_first())
    school = check_empty(sel.xpath('//*[starts-with(@class, "pv-top-card-section__school")]/text()').extract_first())
    location = check_empty( sel.xpath('//*[starts-with(@class, "pv-top-card-section__location")]/text()').extract_first())
    linkedin_url = driver.current_url
    writer.writerow([name.encode('utf-8'),
                     headline.encode('utf-8'),
                     company.encode('utf-8'),
                     school.encode('utf-8'),
                     location.encode('utf-8'),
                     linkedin_url.encode('utf-8')])
    try:
        driver.find_element_by_xpath('//span[text()="Connect"]').click()
        sleep(3)

        driver.find_element_by_xpath('//*[@class="button-primary-large ml3"]').click()
        sleep(3)
    except:
        pass

sleep(3)
driver.close()