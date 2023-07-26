import pandas as pd
from make_driver import MakeDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

links_df = pd.read_csv('orgs_with_links.csv')
scraped_data = pd.read_csv('organizations.csv')
links_df = links_df[links_df['link'].apply(lambda l: str(l) not in list(scraped_data['link']))]

for idx, partner_type, link in links_df.to_records():
    print(idx, link)
    driver_obj = MakeDriver(link)
    driver_obj.create_driver()

    org_name_xpath = '//h1[@class="organization__name"]'
    WebDriverWait(driver_obj.website_driver, 5).until(
        EC.presence_of_element_located((By.XPATH, org_name_xpath))
    )

    organization_name = driver_obj.website_driver.find_element(By.XPATH, org_name_xpath).text

    org_desc_xpath = '//div[@class="organization__description"]/p'
    organization_description = driver_obj.website_driver.find_element(By.XPATH, org_desc_xpath).text.replace('\n', '').replace(',', ' ').replace("'", "")

    org_hq_xpath = '//dl[@class="column organization__profile__stats"]/dd'
    organization_headquarters = driver_obj.website_driver.find_element(By.XPATH, org_hq_xpath).text

    org_site_xpath = '//a[@class="organization__website--dark"]'
    organization_site = driver_obj.website_driver.find_element(By.XPATH, org_site_xpath).get_attribute('href')

    with open('organizations.csv', 'a') as f:
        f.write(f"""{organization_name},{organization_headquarters},{organization_site},{organization_description},{link},{partner_type}\n""")
