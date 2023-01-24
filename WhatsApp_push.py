from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
from time import sleep
import pandas as pd


def Connect_to_driver():    
    options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    options.add_experimental_option("prefs",prefs)
    options.add_argument("no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=800x600")
    options.add_argument("--disable-dev-shm-usage")
    #options.add_argument('headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get('https://web.whatsapp.com')
    driver.implicitly_wait(30)
    return driver

def get_recipients(xlsx_name, sheet_name):
    recipients=pd.read_excel(xlsx_name+".xlsx", sheet_name=sheet_name)
    return recipients

def send_message(xlsx_name, sheet_name):
    if sheet_name == '':
        recipients=get_recipients(xlsx_name, 'Sheet1')[53:]
    else:
        recipients=get_recipients(xlsx_name, sheet_name)
    driver=Connect_to_driver()
    successfully = 0
    fail =0
    failed_contacts = []
    to_send_contacts = []
    input("Press ENTER after login into Whatsapp Web and your chats are visiable.")
    tic = time.perf_counter()
    print('Script Started Running')

    limit = 50
    offset = 0
    while True : 
        for index, row in recipients[offset:limit+offset].iterrows():
            try:
                url = 'https://web.whatsapp.com/send?phone=+{}&text={}'.format(str(int(row['Phone'])),row['Message'])
                driver.get(url)
                sleep(2)
                try:
                    click_btn = driver.find_element (by=By.XPATH,value='//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span')
                except Exception as e:
                    print("Sorry message could not sent to " + str(row['Phone']))#+str(e))
                    fail+=1
                    to_send_contacts.append(row['Phone'])
                else:
                    click_btn.click()
                    sleep(1)
                    print('Message sent to: ' + str(row['Phone']))
                    successfully=successfully+1
            except Exception as e:
                print('Failed to send message to ' + str(row['Phone']))#+str(e))
        print('we did crawl on :', index, 'numbers')
        offset += limit
        sleep(300)
        if index+1 % recipients.shape[0]==0:
            driver.quit()
            toc = time.perf_counter()
            break
    
    return print(f"Message sended in {toc - tic:0.4f} seconds"), print("\n SuccessFully Send Messages To "+ str(successfully) + " Contacts"), print("\n\n Unsuccessfully Send Messages To ",  failed_contacts), print('\n\n\n Trye Again for:', to_send_contacts)

send_message(xlsx_name=input('Enter the name of the EXCEL FILE : '), sheet_name=input('Enter the name of the SHEET : '))
