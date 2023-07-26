from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

class MakeDriver:
    def __init__(self, url: str) -> None:
        self.website = url

    def create_driver(self) -> None:
        options = Options()
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--headless")
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.51 Safari/537.35'
        options.add_argument(f'user-agent={user_agent}')
        options.add_experimental_option("detach", True)

        self.website_driver = webdriver.Chrome(
            service=Service(
            ChromeDriverManager(driver_version='114.0.5735.90').install()
            ),
            options=options
        )
        self.website_driver.get(self.website)

    def destroy_driver(self) -> None:
        self.website_driver.quit()
