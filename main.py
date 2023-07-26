from make_driver import MakeDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

driver_obj = MakeDriver('https://www.weforum.org/partners#search')
driver_obj.create_driver()

partners_type_xpath = '(//div[@class="organisation-search__filter-group__content"])[1]/ul/li/a'
WebDriverWait(driver_obj.website_driver, 20).until(
    EC.presence_of_element_located((By.XPATH, partners_type_xpath))
)
partner_type_links = driver_obj.website_driver.find_elements(By.XPATH, partners_type_xpath)

organisations = []
for link in partner_type_links:
    print(link.text)
    if link.text.lower() == 'partners.all':
        continue

    link.click()
    # print('clicked')
    letter_xpath = '//div[@class="organisation-search__groups"]/div'
    letter_elements = driver_obj.website_driver.find_elements(By.XPATH, letter_xpath)
    
    org_hlinks_xpath = '//div[@class="organisation-search__groups"]/div/div/div/a'
    org_hlinks = driver_obj.website_driver.find_elements(By.XPATH, org_hlinks_xpath)
    # print(org_hlinks)
    for org_hlink in org_hlinks:
        organisations.append(
            {
                'partner_type': link.text.lower(),
                'link': org_hlink.get_attribute('href')
            }
        )
    # print('sleep 10s. . .')
    # time.sleep(10)

pd.DataFrame(organisations).to_csv('orgs_with_links.csv', index=False)

driver_obj.destroy_driver()