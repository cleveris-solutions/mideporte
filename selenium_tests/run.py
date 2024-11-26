import time

from common import *
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def main() -> None:
    load_dotenv()
    driver = initialize_driver()

    try:
        host = os.getenv("FRONTEND_ENDPOINT")
        dni = os.getenv("DNI_EXAMPLE")

        driver.get(f'{host}')
        time.sleep(4)

        dni_input = driver.find_element(By.XPATH, "//input[@placeholder='DNI:']")
        dni_input.send_keys(dni)

        submit_button = driver.find_element(By.XPATH, "//button[text()='Confirmar']")
        submit_button.click() 
        
        time.sleep(2)
        driver.get(f'{host}/reservas')
        time.sleep(2)
        driver.get(f'{host}/perfil')
        time.sleep(2)    
        driver.get(f'{host}/deportes')

        # I promise there's a good reason to have two loops :D 
        time.sleep(2)
        links = driver.find_elements(By.CLASS_NAME, "sport-link")
        hrefs = [link.get_dom_attribute('href') for link in links]
        for link in hrefs:
            driver.get(f'{host}{link}')
            time.sleep(2)
            
    except NoSuchElementException:
        raise AssertionError('Test failed!')

    finally:
        close_driver(driver)

if __name__ == '__main__':
    main()