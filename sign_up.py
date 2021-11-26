import undetected_chromedriver.v2 as uc
from selenium import webdriver
from functions import *
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from time import sleep

def sign_up(phone_number,country,number_of_retries,country_code,date_of_birth,lock,proxy_port=None):
    if phone_number[0]=='+':
        api_number = phone_number
        cut = len(country_code)+1
        phone_number = phone_number[cut:]
    else:
        api_number = '+' + phone_number
        cut = len(country_code)
        phone_number = phone_number[cut:]
    software_names = [SoftwareName.CHROME.value]
    operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
    user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
    # Get Random User Agent String.
    lock.acquire()
    user_agent = user_agent_rotator.get_random_user_agent()
    user_agent = user_agent_rotator.get_random_user_agent()
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--headless")
    PROXY = f'127.0.0.1:{proxy_port}'
    chrome_options.add_argument('--proxy-server=%s' % PROXY)
    driver = uc.Chrome(options=chrome_options)
    driver.delete_all_cookies()
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": user_agent})
    driver.execute_script(
        "Object.defineProperty(navigator,'languages',{get:function(){return['en-US','en','en-AU']},});Object.defineProperty(navigator,'plugins',{get:function(){return[1,2,3,4,5]},});")
    driver.execute_script(
        "const getParameter=WebGLRenderingContext.getParameter;WebGLRenderingContext.prototype.getParameter=function(parameter){if(parameter===37445){return'Intel Open Source Technology Center'}if(parameter===37446){return'Mesa DRI Intel(R) Ivybridge Mobile '}return getParameter(parameter)};")
    driver.execute_script(
        "['height','width'].forEach(property=>{const imageDescriptor=Object.getOwnPropertyDescriptor(HTMLImageElement.prototype,property);Object.defineProperty(HTMLImageElement.prototype,property,{...imageDescriptor,get:function(){if(this.complete&&this.naturalHeight==0){return 20}return imageDescriptor.get.apply(this)},})});")
    driver.execute_script(
        "const elementDescriptor=Object.getOwnPropertyDescriptor(HTMLElement.prototype,'offsetHeight');Object.defineProperty(HTMLDivElement.prototype,'offsetHeight',{...elementDescriptor,get:function(){if(this.id==='modernizr'){return 1}return elementDescriptor.get.apply(this)},});")
    print(' Settings Up The browser... \n\n')
    lock.release()
    ################################################################################################################################################
    ################################################################################################################################################
    ################################################################################################################################################
    driver.get('https://www.tiktok.com/signup')
    print(' Opening Tiktok Sign Up Page... \n\n')

    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(text(),"Use phone")]'))
        )
    except:
        driver.quit()
        print('page not loaded')
        return 'page not loaded'
    else:
        sleep(1)
        element.click()

    ################################################################################################################################################
                 #Wait for page to load
    ################################################################################################################################################
    print(' Adding Personal Information... \n\n')

    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(text(),"When’s your birthday?")]'))
        )
    except:
        driver.quit()
        print('page not loaded')
        return 'page not loaded'
    else:
        sleep(1)
        element.click()


    month = date_of_birth[1]
    day = date_of_birth[0]
    year = date_of_birth[2]
    driver.find_element_by_xpath('//div[contains(text(),"Month")]').click()
    driver.find_element_by_xpath(f'//span[contains(text(),"{month}")]').click()
    sleep(0.5)
    driver.find_element_by_xpath('//div[contains(text(),"Day")]').click()
    driver.find_element_by_xpath(f'//span[contains(text(),"{day}")]').click()
    sleep(0.6)
    driver.find_element_by_xpath('//div[contains(text(),"Year")]').click()
    driver.find_element_by_xpath(f'//span[contains(text(),"{year}")]').click()
    sleep(0.4)
    driver.find_element_by_xpath('//div[contains(text(),"+")]').click()
    driver.find_element_by_xpath(f'//span[contains(text(),"{country}")]').click()
    sleep(0.5)
    print(' Adding Phone Number + Send Code... \n\n')


    phone_field = driver.find_element_by_xpath("//input[@placeholder='Phone number']")
    phone_field.send_keys(phone_number)
    send_code = driver.find_element_by_xpath('//button[contains(text(), "Send code")]')
    sleep(0.6)
    send_code.click()
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Too many attempts. Try again later.")]'))
        )
    except:
        pass
    else:
        send_code.click()
        sleep(2)
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//div[contains(text(), "Too many attempts. Try again later.")]'))
            )
        except:
            pass
        else:
            print('Too many attempts. IP is Bad')
            driver.quit()
            return 'Too many attempts. IP is Bad'


    ################################################################################################################################################
                 # Wait for captcha to load and verify captcha
    ################################################################################################################################################
    WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID,'captcha-verify-image'))
        )
    print(' Verifying Captcha... \n\n')
    verify_captcha(driver)
    too_many = check_for_too_many_attempts(driver)
    if too_many == 'Too many attempts. IP is Bad':
        driver.quit()
        return 'Too many attempts. IP is Bad'

    ################################################################################################################################################
                 # Wait for resend_code_button to be visible and Try x times to resend the code
    ################################################################################################################################################
    code = check_code_x_times(driver,api_number,number_of_retries)
    if code =='Code never arrived':
        driver.quit()
        return 'Code never arrived'
    code_field = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//input[@placeholder='Enter 4-digit code']"))
    )

    code_field.send_keys(code)
    WebDriverWait(driver, 2).until_not(EC.element_attribute_to_include((By.XPATH, '//button[contains(text(), "Next")]'),"disabled"))
    next_button = driver.find_element_by_xpath('//button[contains(text(), "Next")]')
    sleep(0.5)
    next_button.click()
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Too many attempts. Try again later.")]'))
        )
    except:
        pass
    else:
        sleep(0.2)
        next_button.click()
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//div[contains(text(), "Too many attempts. Try again later.")]'))
            )
        except:
            pass
        else:
            driver.quit()
            print('Too many attempts. IP is Bad')
            return 'Too many attempts. IP is Bad'

    ################################################################################################################################################
                 #Klik next dhe prit faqe tbehet load (Vendos username + pass)
    ################################################################################################################################################

    skip_button = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, '//button[contains(text(), "Skip")]'))
    )
    # driver.find_element_by_xpath("//input[@placeholder='Username']").send_keys(username)
    # driver.find_element_by_xpath("//input[@placeholder='Password']").send_keys(password)
    sleep(0.5)
    skip_button.click()
    #Todo

    ################################################################################################################################################
                 #Prit homepagin te behet load dhe shpeto te dhenat ne database
    ################################################################################################################################################
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//h2[contains(text(), "For You")]'))
        )
    except:
        driver.quit()
        return 'page not loaded'
    else:
        driver.quit()
        return 'sign_up_done'

if __name__ == '__main__':
    print('PyCharm')

