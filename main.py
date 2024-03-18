#https://www.aliexpress.us/item/3256806069260228.html?channel=pinterest
import subprocess
import os
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
sys.path.append('..')
import helper

picture_folder = "C:\\Users\\USER\\Pictures\\"

# return a list of dictionaries 
def get_pinterest_links():
    filepath = helper.select_files()[0]
    id_list = []

    with open(filepath, 'r') as id_file:
        for line in id_file:
            id_list.append({'id':line.strip(), 'pinterest_link':f"https://pin.it/{line.strip()}"})

    return id_list

def process_pinterest_links(items): #Updates each dict with an aliexpress url

    # Set up Selenium WebDriver with Firefox
    for item in items:
        driver = webdriver.Firefox()
        # Open the website in the browser
        driver.get(item["pinterest_link"])
        # Give some time for the page to load and for any AJAX requests to complete
        time.sleep(5)
        #div_element = driver.find_element(By.XPATH, "name")
        div_element = driver.find_element(By.XPATH, '//div[@data-test-id="main-pin-section-visit-button"]')
        # Find the button element within the div element
        button_element = div_element.find_element(By.TAG_NAME, 'button')
        # Click on the button
        button_element.click()
        time.sleep(10)
        driver.switch_to.window(driver.window_handles[-1])
        new_tab_url = driver.current_url
        print("AliExpress Link: ", new_tab_url)
        if 'aliexpress' in new_tab_url:
            item["aliexpress_link"] = new_tab_url.strip()
        #close browser
        driver.quit()

    return items

def get_product_images(items):

    for item in test_urls:
        # Start the WebDriver
        driver = webdriver.Firefox()
        # Navigate to the webpage
        #driver.get(item["aliexpress_link"])
        driver.get(item)

        # Find all div elements with class name starting with "slider--slider"
        slider_divs = driver.find_elements(By.CSS_SELECTOR, 'div[class^="slider--slider"]')
        # Iterate through each div element
        imgs = []
        for div in slider_divs:
            # Find the img element within the div
            img_element = div.find_element(By.TAG_NAME, 'img')
            # Get the src attribute of the img element
            img_src = img_element.get_attribute('src')
            # Print the src content
            print("Image source:", img_src)

            parts = img_src.rsplit("_", 2)
            # Join the parts except the last two
            trimmed_url = "_".join(parts[:-2])
            imgs.append(trimmed_url)

        #path = f"{picture_folder}{item['id']}"
        path = f"{picture_folder}test"
        #if not os.path.exists(f"{picture_folder}{item['id']}"):
        if not os.path.exists(f"{picture_folder}test"):
            #os.makedirs(f"{picture_folder}{item['id']}")
            os.makedirs(f"{picture_folder}test")
        
        for img in imgs:
            cmd = f"curl -Uri '{img}' -OutFile '{path}'"
            subprocess.run(cmd, shell=True)
            print("img has been downloaded")


        # Close the WebDriver
        driver.quit()


#items = get_pinterest_links()
#get_product_images(process_pinterest_links(get_pinterest_links()))
get_product_images(items=None)
