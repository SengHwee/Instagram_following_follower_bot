import os
import time
from selenium import webdriver


def get_followers_following(followersORfollowing, driver):
    driver.find_element_by_xpath("//a[contains(@href,'/{}')]".format(followersORfollowing)).click()
    time.sleep(1)
    scroll_box = driver.find_element_by_xpath("/html/body/div[4]/div/div/div[2]")
    last_ht, ht = 0, 1
    while last_ht != ht:
        time.sleep(2)
        last_ht = ht
        time.sleep(1)
        ht = driver.execute_script("""
            arguments[0].scrollTo(0, arguments[0].scrollHeight); 
            return arguments[0].scrollHeight;
            """, scroll_box)
    links = scroll_box.find_elements_by_tag_name('a')
    names = [name.text for name in links if name.text != '']

    # close button
    driver.find_element_by_xpath("/html/body/div[4]/div/div/div[1]/div/div[2]/button").click()
    time.sleep(1)
    return names


DRIVER_PATH = os.getcwd() + "\Driver\chromedriver.exe"

chrome_driver = webdriver.Chrome(DRIVER_PATH)
username = input("Handler for Instagram: ")
password = input("Password for Instagram: ")

chrome_driver.get("https://www.instagram.com")
time.sleep(2)
username_field = chrome_driver.find_element_by_xpath("//input[@name='username']")
username_field.send_keys(username)

password_field = chrome_driver.find_element_by_xpath("//input[@name='password']")
password_field.send_keys(password)

login_button = chrome_driver.find_element_by_xpath("//button[@type='submit']")
login_button.click()

time.sleep(4)

try:
    chrome_driver.find_element_by_xpath("//input[@name='verificationCode']")
    twoFA = True
except:
    twoFA = False

if twoFA:
    two_FA = input("2FA for Instagram: ")
    chrome_driver.find_element_by_xpath("//input[@name='verificationCode']").send_keys(two_FA)
    chrome_driver.find_element_by_xpath("//button[contains(text(), 'Confirm')]").click()
    time.sleep(4)
    

for i in range(2):
    chrome_driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]").click()
    time.sleep(2)
chrome_driver.find_element_by_xpath("//a[contains(@href, '/{}/')]".format(username)).click()
time.sleep(2)

followers_list=get_followers_following("followers", chrome_driver)
following_list=get_followers_following("following", chrome_driver)

not_following_back = [user for user in following_list if user not in followers_list]
print(not_following_back)






