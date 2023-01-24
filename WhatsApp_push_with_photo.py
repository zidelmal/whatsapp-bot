from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from time import sleep
import pandas as pd
from io import BytesIO
import win32clipboard
from PIL import Image
import time


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
    if sheet_name=='':
        recipients=pd.read_excel(xlsx_name+".xlsx", sheet_name='sheet1')
    else:
        recipients=pd.read_excel(xlsx_name+".xlsx", sheet_name=sheet_name)
    return recipients

def send_to_clipboard(clip_type, data):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(clip_type, data)
    win32clipboard.CloseClipboard()

def send_message(xlsx_name, sheet_name, image_name):
    if sheet_name == '':
        recipients=get_recipients(xlsx_name, 'Sheet1')
    else:
        recipients=get_recipients(xlsx_name, sheet_name)
    image = Image.open(image_name)
    output = BytesIO()
    image.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]
    output.close()
    driver = Connect_to_driver()
    successfully = 0
    fail =0
    failed_contacts = []
    input("Press ENTER after login into Whatsapp Web and your chats are visiable.")
    tic = a=time.perf_counter()
    print('Script Started Running')
    for recipient in recipients.index:
        try:
            url = 'https://web.whatsapp.com/send?phone=+{}&text={}'.format(str(int(recipients['Contact'][recipient])),recipients['Message'][recipient])
            driver.get(url)
            try:
                text= driver.find_element(By.XPATH,'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div/p')
            except Exception as e:
                print("Sorry message could not sent to " + str(recipients['Contact'][recipient]))#+str(e))
                fail+=1
                failed_contacts.append(recipients['Contact'][recipient])
                pass
            else:
                send_to_clipboard(win32clipboard.CF_DIB, data)
                text.send_keys(Keys.CONTROL+ "v")
                click_btn = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/div/div[2]/div[2]/div/div/span')
                click_btn.click()
                sleep(3)
                print('Message sent to: ' + str(recipients['Contact'][recipient]))
                successfully=successfully+1
        except Exception as e:
            print('Failed to send message to ' + str(recipients['Contact'][successfully]))#+str(e))
    driver.quit()
    toc = time.perf_counter()
    return print(f"Message sended in {toc - tic:0.4f} seconds"), print("\n SuccessFully Send Messages To "+ str(successfully) + " Contacts"), print("\n\n Unsuccessfully Send Messages To ",  failed_contacts)

send_message(xlsx_name=input('Enter the name of the EXCEL FILE : '), sheet_name=input('Enter the name of the SHEET : '), image_name=input('Enter the name of the image : '))
