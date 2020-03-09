from selenium import webdriver
from captcha_solver import CaptchaSolver
import wget
import time
import os
from python_anticaptcha import AnticaptchaClient, ImageToTextTask
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json


all_emails_and_passwords = {}

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--test-type")
options.binary_location ='/usr/bin/chromium'

quera_sign_up = 'https://quera.ir/accounts/registration/developer'
quera_problem_page = 'https://quera.ir/course/assignments/14549/problems/49157'
quera_class_registration = 'https://quera.ir/overview/add_to_course/course/5218'
fake_email_site = 'https://emailfake.com'
delay = 30
all_mails_file = 'mails.txt'



driver = webdriver.Chrome(options=options)
driver.set_page_load_timeout(delay)
fake_mail_driver = webdriver.Chrome(options=options)
fake_mail_driver.set_page_load_timeout(delay)




# *************************************                  functions                      *************************************

def make_my_fake_mail():
    global domain_mail

    fake_mail_driver.get(fake_email_site)

    email_username_input = fake_mail_driver.find_element_by_id('userName')
    email_username_input.clear()
    email_username_input.send_keys(mail)


    email_domain_input = fake_mail_driver.find_element_by_id('domainName2')
    domain_mail = email_domain_input.get_attribute('value')

    fake_mail_driver.find_element_by_id('copbtn').click()




def captcha_solver(captcha_element, captcha_input):
    
    # constant variables
    captcha_path = 'captcha.png'
    
    # delete last captcha
    try:
        os.remove(captcha_path)
    except:
        pass


    # downloading captcha image

    img_url = captcha_element.get_attribute('src')
    wget.download(img_url, captcha_path)


    # solving captcha

    api_key = '1eb7bf3dcc6b3d0ab33e6c92ef3de0d1'
    captcha_fp = open(captcha_path, 'rb')
    client = AnticaptchaClient(api_key)
    task = ImageToTextTask(captcha_fp)
    job = client.createTask(task)
    job.join()
    captcha_solved_text = job.get_captcha_text()


    # setting captcha in place

    captcha_input.send_keys(captcha_solved_text)

    print(captcha_solved_text)
    return captcha_input


def save_mails_to_file():
    j = json.dumps(dict)
    f = open(all_mails_file, "w+")
    f.write(j)
    f.close()



if __name__ == '__main__':
    

    for i in range(200, 202):


        i = 200
        mail = 'queraMailNumber' + str(i)
        domain_mail = ''
        password = mail 
        student_id = '2754' + str(i)
        
        make_my_fake_mail()
        
        
        # type my mail 
        driver.get(quera_sign_up)
        email_input = WebDriverWait(driver, 3 * delay).until(EC.presence_of_element_located((By.NAME, 'email')))
        email_input.send_keys(mail + '@' + domain_mail)

        # guess and type captcha
        captcha_image_element = driver.find_element_by_class_name('captcha')
        captcha_input = driver.find_element_by_name('captcha_1')
        captcha_solver(captcha_image_element, captcha_input).submit()

        # wait for sending email
        time.sleep(5)

        # confirm email
        fake_mail_driver.refresh()
        message_div = WebDriverWait(fake_mail_driver, 3 * delay).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@class, 'button-a-primary')]")))
        confirmation_url = message_div.get_attribute('href')


        # setting passwords
        driver.get(confirmation_url)
        driver.find_element_by_name('password1').send_keys(password)
        password2 = driver.find_element_by_name('password2')
        password2.send_keys(password)
        password2.submit()


        # save mail info to dict
        email = mail + '@' + domain_mail
        all_emails_and_passwords[email] = password


        # register to class
        driver.get(quera_class_registration)
        driver.find_element_by_name('identity').send_keys(student_id)

        # solving and submiting captcha
        captcha_image_element = driver.find_element_by_class_name('captcha')
        captcha_input = driver.find_element_by_name('captcha_1')
        captcha_solver(captcha_image_element, captcha_input).submit()


        # submiting homework
        driver.get(quera_problem_page)
        code = 'codes/' + str(i) + '.zip'
        file = driver.find_element_by_name('file')
        file.send_keys(code)
        file.submit()


        save_mails_to_file()




 
#  ********************* login *****************************

# driver.get(quera_problem_page)


# driver.find_element_by_name('login').send_keys(email)


# password = driver.find_element_by_name('password')
# password.send_keys(password)
# password.submit()



