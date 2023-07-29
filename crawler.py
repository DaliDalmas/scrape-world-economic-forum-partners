import pandas as pd
from make_driver import MakeDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime
from constants import partners_type_xpath, org_hlinks_xpath, org_name_xpath,\
    organization_description_xpath, organization_headquarters_xpath, organization_site_xpath,\
    organization_file, website, links_file
import logging
logging.basicConfig(level = logging.INFO)


class Crawler:

    def __init__(self) -> None:
        self.CONDITION = True


    def fetch_urls(self):

        driver_obj = MakeDriver(website)
        driver_obj.create_driver()
        logging.info(f"{datetime.now()}: Driver created.")

        WebDriverWait(driver_obj.website_driver, 20).until(
            EC.presence_of_element_located((By.XPATH, partners_type_xpath))
        )
        partner_type_links = driver_obj.website_driver.find_elements(By.XPATH, partners_type_xpath)

        organisations = []
        for link in partner_type_links:
            logging.info(f"{datetime.now()}: Feching links for patner of type {link.text.lower()}")
            if link.text.lower() == 'partners.all':
                continue
            link.click()

            org_hlinks = driver_obj.website_driver.find_elements(By.XPATH, org_hlinks_xpath)

            for org_hlink in org_hlinks:
                organisations.append(
                    {
                        'partner_type': link.text.lower(),
                        'link': org_hlink.get_attribute('href')
                    }
                )

        logging.info(f"{datetime.now()}: Partner links fetched.")
        pd.DataFrame(organisations).to_csv(links_file, index=False)
        logging.info(f"{datetime.now()}: partner links saved to csv")
        driver_obj.destroy_driver()

    def __fetch_xpath_values(self, xpath, driver):
        try:
            return driver.website_driver.find_element(By.XPATH, xpath)\
                    .text.replace('\n', '')\
                    .replace(',', ' ')\
                    .replace("'", "")
        except:
            return ''

    def fetch_data(self):

        links_df = pd.read_csv(links_file)
        scraped_data = pd.read_csv(organization_file)
        links_df = links_df[
            links_df['link'].apply(
                lambda l: str(l) not in list(scraped_data['link'])
                )
            ]
        logging.info(f"{datetime.now()}: Partner links read from csv.")

        if len(links_df)==0:
            self.CONDITION = False
            raise Exception("We are done!")

        for idx, partner_type, link in links_df.to_records():
            logging.info(f"{datetime.now()}: Fetching data for partner: {idx} link: {link}.")
            driver_obj = MakeDriver(link)
            driver_obj.create_driver()

            
            WebDriverWait(driver_obj.website_driver, 10).until(
                EC.presence_of_element_located((By.XPATH, org_name_xpath))
            )

            organization_name = self.__fetch_xpath_values(org_name_xpath, driver_obj)
            organization_description = self.__fetch_xpath_values(organization_description_xpath, driver_obj)
            organization_headquarters = self.__fetch_xpath_values(organization_headquarters_xpath, driver_obj)
            organization_site = self.__fetch_xpath_values(organization_site_xpath, driver_obj)

            with open(organization_file, 'a') as f:
                f.write(f"""{organization_name},{organization_headquarters},{organization_site},{organization_description},{link},{partner_type}\n""")
            logging.info(f"{datetime.now()}: Data for partner: {idx} link: {link} saved in {organization_file}")
            
            driver_obj.destroy_driver()
