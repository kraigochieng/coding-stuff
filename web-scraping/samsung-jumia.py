from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

# DRIVER_PATH = 'C:\\Users\\USER\\Documents\\coding-stuff\\web-scraping\\drivers'
driver = webdriver.Chrome()

driver.implicitly_wait(5)

driver.get('https://www.jumia.co.ke/mlp-samsung-shop/mobile-phones/?viewType=grid#catalog-listing')

assert driver.title
print(driver.title)

phones_element = driver.find_elements(By.CLASS_NAME, 'name')
phones_element = [phone_element.get_attribute('textContent').replace('Samsung ', '').replace('Galaxy ', '') for phone_element in phones_element]

prices = driver.find_elements(By.CLASS_NAME, 'prc')
prices = [price.get_attribute('textContent') for price in prices]

phones = []

for phone_element in phones_element:
    # Define Regular Expressions
    display_pattern = r'\d.\d["″\']'
    battery_pattern = r'\d{4}\s*mAh|\d\d\d\d\s*MAH'
    camera_pattern = r'\d{2}MP'
    dual_sim_pattern = r'\({0,1}Dual Sim\){0,1}'
    storage_and_ram_pattern = r'\d*\s*GB'
    broadband_pattern = r'\dG(?!\w)'

    # Extract Info
    display = ''.join(re.findall(display_pattern, phone_element))
    battery = ''.join(re.findall(battery_pattern, phone_element))
    camera = ''.join(re.findall(camera_pattern, phone_element))
    dual_sim = ''.join(re.findall(dual_sim_pattern, phone_element, re.IGNORECASE))
    storage_and_ram = re.findall(storage_and_ram_pattern, phone_element)
    broadband = ''.join(re.findall(broadband_pattern, phone_element))
    extra_pattern = "CAMERA|Battery|RAM|ROM|2G"

    # Remove extracted text
    new_string = re.sub(display_pattern, '', phone_element)
    new_string = re.sub(battery_pattern, '', new_string)
    new_string = re.sub(camera_pattern, '', new_string)
    new_string = re.sub(dual_sim_pattern, '', new_string, flags=re.IGNORECASE)
    new_string = re.sub(storage_and_ram_pattern, '', new_string)
    new_string = re.sub(broadband_pattern, '',new_string)
    new_string = re.sub(extra_pattern, '', new_string)

    # Storage First, RAM Second
    storage_and_ram = sorted(storage_and_ram, key = lambda x: int(x[:-2]), reverse=True)

    # Extract phone name
    comma_index = new_string.find(',')
    if comma_index == -1: comma_index = new_string.find('-')
    if comma_index == -1: comma_index = new_string.find('–')
    if comma_index == 0: comma_index = new_string.find(' ')
    name = new_string[0:comma_index]

    # Remove phone name for colour to be extracted
    new_string = re.sub(name, '', new_string)

    phone = {
        'name': name.replace('–', '').replace('\'', '').strip(),
        'broadband': broadband if broadband != '2G' else '' ,
        'display': display[:-1],
        'storage': storage_and_ram[0].replace(' ', '')[:-2],
        'ram': storage_and_ram[1].replace(' ', '')[:-2] if len(storage_and_ram) > 1 else '',
        'is_dual_sim':True if dual_sim else False,
        'camera': camera[:-2],
        'battery': battery.replace(' ', '')[:-3],
        'colour': new_string.replace(',', '').replace('+', '').replace('–','').replace('-','').replace('\'','').strip().title(),
    }

    phones.append(phone)

for phone in phones:
    print(phone)

driver.quit()