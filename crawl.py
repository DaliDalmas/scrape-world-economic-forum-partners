import pandas as pd
from make_driver import MakeDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
CONDITION = True
def run():
    links_df = pd.read_csv('orgs_with_links.csv')
    scraped_data = pd.read_csv('organizations.csv')
    links_df = links_df[links_df['link'].apply(lambda l: str(l) not in list(scraped_data['link']))]
    if len(links_df)==0:
        CONDITION = False
        raise Exception(" we are done")
    for idx, partner_type, link in links_df.to_records():
        print(idx, link)
        driver_obj = MakeDriver(link)
        driver_obj.create_driver()

        org_name_xpath = '//h1[@class="organization__name"]'
        WebDriverWait(driver_obj.website_driver, 10).until(
            EC.presence_of_element_located((By.XPATH, org_name_xpath))
        )

        organization_name = driver_obj.website_driver.find_element(By.XPATH, org_name_xpath).text.replace('\n', '').replace(',', ' ').replace("'", "")

        try:
            org_desc_xpath = '//div[@class="organization__description"]/p'
            organization_description = driver_obj.website_driver.find_element(By.XPATH, org_desc_xpath).text.replace('\n', '').replace(',', ' ').replace("'", "")
        except:
            organization_description = ''

        try:
            org_hq_xpath = '//dl[@class="column organization__profile__stats"]/dd'
            organization_headquarters = driver_obj.website_driver.find_element(By.XPATH, org_hq_xpath).text.replace('\n', '').replace(',', ' ').replace("'", "")
        except:
            org_hq_xpath = ''

        try:
            org_site_xpath = '//a[@class="organization__website--dark"]'
            organization_site = driver_obj.website_driver.find_element(By.XPATH, org_site_xpath).get_attribute('href').replace('\n', '').replace(',', ' ').replace("'", "")
        except:
            organization_site = ''

        with open('organizations.csv', 'a') as f:
            f.write(f"""{organization_name},{organization_headquarters},{organization_site},{organization_description},{link},{partner_type}\n""")
        
        driver_obj.destroy_driver()

if __name__=='__main__':
    
    while CONDITION:
        try:
            run()
        except Exception as e:
            print(e)
            print('connection stopped let sleep for a minute')
            time.sleep(60)
            try:
                run()
            except Exception as e:
                print(e)
                print('connection stopped twice let sleep for ten minutes')
                time.sleep(600)

