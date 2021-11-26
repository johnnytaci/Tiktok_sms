import undetected_chromedriver.v2 as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

def login():
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--headless")
    driver = uc.Chrome(options=chrome_options)
    driver.get('http://127.0.0.1:22999')

    sign_in_button = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '//button[contains(text(), "Sign in")]'))
    )


    driver.find_element_by_xpath("//input[@type='password']").send_keys('Hellon@12')
    driver.find_element_by_xpath("//input[@type='email']").send_keys('johnnytaci2021@gmail.com')

    sign_in_button.click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button[contains(text(), "Add new port")]'))
    )
    driver.quit()


def add_ports(number):
    for i in enumerate(range(24001, (24001 + number))):
        command = r'curl -X POST "http://127.0.0.1:22999/api/proxies" -H "Content-Type: application/json" -d "{\"proxy\":{\"port\":%s,\"zone\":\"static\",\"proxy_type\":\"persist\",\"customer\":\"hl_3de3ecb2\",\"password\":\"9zfy81w22bu3\",\"whitelist_ips\":[]}}"' % (i[1])
        os.system(command)

def update_ports(start,finish):
    for i in range(start,finish):
        command = (r'curl -X PUT "http://127.0.0.1:22999/api/proxies/%s" -H "Content-Type: application/json" -d "{\"proxy\":{\"port\":%s,\"zone\":\"static\",\"proxy_type\":\"persist\",\"customer\":\"hl_3de3ecb2\",\"password\":\"9zfy81w22bu3\",\"country\":\"Any\",\"whitelist_ips\":[]}}"') % (i,i)
        os.system(command)

def delete_ports(start, finish):
    for i in range(start, finish):
        command = r'curl -X DELETE "http://127.0.0.1:22999/api/proxies/%s"' % (i)
        os.system(command)

delete_ports(24013,24101)