import time
import random
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Set up Selenium with headless Chrome
options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)

# URL of the reservation page
url = 'https://secure.ticketsage.net/websales.aspx?u=halekoa'

# Function to check for the reservation slot
def check_reservation():
    driver.get(url)
    try:
        # Scroll to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Wait for the page to load

        # Specific date for testing
        test_date_str = 'Wednesday, February 12, 2025 8:00 AM'

        # Find all div elements with the specific date
        div_elements = driver.find_elements(By.XPATH, f'//div[contains(@name, "PerformanceDiv") and .//span[@name="prfdatespan" and contains(text(), "{test_date_str}")]]')
        for div in div_elements:
            div.click()
            time.sleep(2)  # Wait for the page to load

        # Prioritize reservation slots
        priority_slots = [
            ('Tennis &amp; Pickleball-8am-PB-C', 'rgb(212, 212, 212)'),  # Grayed out if reserved
            ('Tennis &amp; Pickleball-8am-PB-D', 'rgb(255, 255, 0)'),    # Yellow
            ('Tennis &amp; Pickleball-8am-PB-A', 'rgb(0, 153, 255)'),    # Blue
            ('Tennis &amp; Pickleball-8am-PB-B', 'rgb(51, 204, 0)')      # Green
        ]

        for slot_name, expected_color in priority_slots:
            try:
                # Wait for the reservation slot to be present
                logging.info(f'Waiting for the reservation slot {slot_name} to be present...')
                slot = WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located((By.XPATH, f'//div[@title="{slot_name}"]'))
                )
                logging.info(f'Reservation slot {slot_name} found.')

                # Check if the slot is available (not grayed out)
                slot_color = slot.value_of_css_property('background-color')
                if slot_color != 'rgb(212, 212, 212)':  # Check if the color is not #D4D4D4
                    logging.info(f'Clicking on the reservation slot {slot_name}...')
                    slot.click()
                    time.sleep(1)  # Wait for the page to load
                else:
                    logging.info(f'Reservation slot {slot_name} is not available (grayed out).')
            except Exception as e:
                logging.info(f'Reservation slot {slot_name} not found. Trying next slot...')
                continue

        # Click the "Add and Go to Cart" button
        logging.info('Waiting for the "Add and Go to Cart" button to be present...')
        add_to_cart_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@id="Add_To_Cart_js"]'))
        )
        logging.info('"Add and Go to Cart" button found. Clicking on the button...')
        add_to_cart_button.click()
        time.sleep(2)  # Wait for the page to load

        # Fill out the required fields
        logging.info('Filling out the required fields...')
        driver.find_element(By.ID, 'patron_firstname1').send_keys('Jarrett')
        driver.find_element(By.ID, 'patron_lastname1').send_keys('Dominic')
        driver.find_element(By.ID, 'patron_zip').send_keys('96814')
        driver.find_element(By.ID, 'patron_phone').send_keys('8084792653')
        driver.find_element(By.ID, 'patron_email').send_keys('jarrettdominic@gmail.com')
        driver.find_element(By.ID, 'patron_custom6').send_keys('CAC')

        # Select "NO" for hotel reservation
        logging.info('Selecting "NO" for hotel reservation...')
        reservation_button = driver.find_element(By.XPATH, '//button[@data-id="patron_custom4"]')
        reservation_button.click()
        no_option = driver.find_element(By.XPATH, '//span[contains(text(), "NO")]')
        no_option.click()

        # Select "Website" for how you heard about us
        logging.info('Selecting "Website" for how you heard about us...')
        hear_about_us_button = driver.find_element(By.XPATH, '//button[@data-id="patron_custom1"]')
        hear_about_us_button.click()
        website_option = driver.find_element(By.XPATH, '//span[contains(text(), "Website")]')
        website_option.click()

        # Select "None" for vegans
        logging.info('Selecting "None" for vegans...')
        vegans_radio = driver.find_element(By.XPATH, '//input[@name="selpatron_custom7" and @value="None"]')
        vegans_radio.click()

        # Select "None" for gluten free
        logging.info('Selecting "None" for gluten free...')
        gluten_free_radio = driver.find_element(By.XPATH, '//input[@name="selpatron_custom9" and @value="None"]')
        gluten_free_radio.click()

        # Pause for debugging and testing
        input("Press Enter to continue after verifying the entered information...")

        # Submit the reservation
        '''
        logging.info('Waiting for the submit button to be present...')
        submit_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@name="prfbuytixpan"]'))
        )
        logging.info('Submit button found. Clicking on the submit button...')
        submit_button.click()
        logging.info(f'Reservation made at {datetime.now()}')
        return True
        '''

    except Exception as e:
        logging.error(f'Error checking reservation: {e}')
    return False

# Main loop to monitor the reservation page
def main():
    start_time = datetime.now().replace(hour=7, minute=55, second=0, microsecond=0)
    end_time = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
    
    while datetime.now() < start_time:
        time.sleep(1)
    
    while datetime.now() < end_time:
        if check_reservation():
            break
        time.sleep(random.randint(30, 60))
    
    while datetime.now() < end_time.replace(second=50):
        if check_reservation():
            break
        time.sleep(random.randint(2, 5))
    
    if not check_reservation():
        logging.info('Failed to make a reservation')

if __name__ == '__main__':
    main()
    driver.quit()