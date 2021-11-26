from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import requests
from captcha_solver import captcha_solver
from time import sleep
import pymongo
sms_count_ = 0

def sms_count():
    global sms_count_
    sms_count_+=1
    if sms_count_>=100:
        password = 'tiktok2021'
        database = 'Numbers'
        client = pymongo.MongoClient(f"mongodb+srv://tiktoksms:{password}@cluster0.vfggv.mongodb.net/{database}?retryWrites=true&w=majority")
        db = client['Numbers']
        col = db['sms_count']
        col.insert_one({'count':sms_count_})
        sms_count_ = 0
        client.close()
    return
def check_for_too_many_attempts(driver):
    try:
        WebDriverWait(driver, 4).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Too many attempts. Try again later.")]'))
        )
    except:
        return
    else:
        print('Too many attempts. IP is Bad')
        return 'Too many attempts. IP is Bad'


def verify_captcha(driver):
    while True:
        try:
            WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//span[contains(text(), "Drag the puzzle piece into place")]'))
            )
            captcha_image = WebDriverWait(driver, 2).until(
                EC.visibility_of_element_located(
                    (By.ID, 'captcha-verify-image'))
            )
            shigjeta = WebDriverWait(driver, 2).until(
                EC.visibility_of_element_located(
                    (By.CLASS_NAME, 'secsdk-captcha-drag-icon'))
            )
        except:
            return print('Captcha Verified')
        else:
            image_url = captcha_image.get_attribute('src')
            img_data = requests.get(image_url).content
            length = captcha_solver(img_data)
            action = ActionChains(driver)
            steps = [5 for i in range(int((length / 1.68) / 5))]
            action.move_to_element(shigjeta).click_and_hold().perform()
            for step in steps:
                action.move_by_offset(step, 0).perform()
            action.pause(0.5).release().perform()

def check_code(phone_number):
    url='http://88.99.226.11/getcode.php'
    data = {'phone' : phone_number}
    r = requests.post(url, data = data)
    if len(r.text[22:26])==4:
        code = r.text[22:26]
        sms_count()
        return code
    sleep(10)
    return None

def check_code_x_times(driver,phone_number,number_of_tries):
    if number_of_tries == 0:
        for i in range(5):
            code = check_code(phone_number)
            if code == None:
                print('Code never arrived...')
                return 'Code never arrived'
        return code
    code = None
    while number_of_tries>0 and code == None:
        resend_code_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//button[contains(text(), "Resend code")]'))
        )
        while resend_code_button.get_attribute('disabled') and code == None:
            code = check_code(phone_number)
            print(' Code Not Present. Requesting Again...')

        if not code:
            print(' Code Not Present for more than 1 minute. Resending Code... \n\n')
            resend_code_button.click()
            verify_captcha(driver)
            check_for_too_many_attempts(driver)
        number_of_tries -= 1
    for i in range(5):
        code = check_code(phone_number)
    if code:
        return code
    else:
        print('Code never arrived... \n\n')
        return 'Code never arrived'

def login_database_updater(collection,data):
    try:
        index = collection.find().sort('index', pymongo.DESCENDING)[0]['index']
    except:
        index = 0
    else:
        pass
    data['index'] = index
    collection.insert_one(data)
