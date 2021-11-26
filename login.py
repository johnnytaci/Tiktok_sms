from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from proxy import create_proxy_extention
from selenium.webdriver.common.action_chains import ActionChains
import requests
from captcha_solver import captcha_solver
import undetected_chromedriver.v2 as uc
from undetected_chromedriver.options import ChromeOptions
from time import sleep
from functions import *


phone_number = '506788664'


PATH = "C:\Program Files (x86)\chromedriver.exe"
chrome_options = ChromeOptions()
proxy = {
    'PROXY_HOST' :  None,
    'PROXY_PORT' :  None,
    'PROXY_USER' :  None,
    'PROXY_PASS' :  None,
}
if proxy['PROXY_HOST'] is not None:
    plugin_file = create_proxy_extention(proxy)
    chrome_options.add_extension(plugin_file)

# chrome_options.add_argument("--headless")
driver = uc.Chrome(options=chrome_options)

print(' Settings Up The browser... \n\n')
################################################################################################################################################
################################################################################################################################################
################################################################################################################################################
driver.get('https://www.tiktok.com/login')
print(' Opening Tiktok Sign Up Page... \n\n')

try:
    element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '//div[contains(text(),"Use phone")]'))
    )
except:
    driver.quit()
    print('page not loaded')
else:
    element.click()


WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.XPATH, '//div[contains(text(),"+")]'))
)

driver.find_element_by_xpath('//div[contains(text(),"+")]').click()
driver.find_element_by_xpath('//span[contains(text(),"Azer")]').click()

driver.find_element_by_xpath("//input[@placeholder='Phone number']").send_keys(phone_number)
driver.find_element_by_xpath('//button[contains(text(), "Send code")]').click()


try:
    WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Too many attempts. Try again later.")]'))
    )
except:
    pass
else:
    driver.quit()
    print('Too many attempts. IP is Bad')


################################################################################################################################################
             # Wait for captcha to load and verify captcha
################################################################################################################################################
WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID,'captcha-verify-image'))
    )
print(' Verifying Captcha... \n\n')
verify_captcha(driver)
check_for_too_many_attempts(driver)

################################################################################################################################################
             # Wait for resend_code_button to be visible and Try x times to resend the code
################################################################################################################################################
api_number = '+994' + phone_number
number_of_tries = 2
code = check_code_x_times(driver,api_number,number_of_tries)

code_field = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located(
        (By.XPATH, "//input[@placeholder='Enter 4-digit code']"))
)

code_field.send_keys(code)
WebDriverWait(driver, 2).until_not(EC.element_attribute_to_include((By.XPATH, '//button[contains(text(), "Log in")]'),"disabled"))
next_button = driver.find_element_by_xpath('//button[contains(text(), "Log in")]')
next_button.click()
# check_for_too_many_attempts(driver)


WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located(
        (By.XPATH, '//h2[contains(text(), "For You")]'))
)







# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print('PyCharm')
#
# # See PyCharm help at https://www.jetbrains.com/help/pycharm/
